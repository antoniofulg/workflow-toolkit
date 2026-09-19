import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { KNOWLEDGE_DESTINATIONS, safePath, sha256, validateRelative, InstallerError } from './engine.js';

const fail = (message) => { throw new InstallerError(message); };
const atomicWrite = (file, content) => { fs.mkdirSync(path.dirname(file), { recursive: true }); const temporary = path.join(path.dirname(file), `.${path.basename(file)}.${process.pid}.${crypto.randomUUID()}.tmp`); try { const fd = fs.openSync(temporary, 'w', 0o600); fs.writeFileSync(fd, content); fs.fsyncSync(fd); fs.closeSync(fd); fs.renameSync(temporary, file); } finally { if (fs.existsSync(temporary)) fs.unlinkSync(temporary); } };
const targetOf = (input) => path.resolve(input?.targetRoot || input?.target || process.cwd());
const timestamp = (clock) => new Date(typeof clock === 'function' ? clock() : clock || Date.now()).toISOString().replace(/:/g, '-');
const journalPath = (root) => path.join(root, '.my-workflow', 'transaction.json');
function ensureDirectory(root, relative) { let current = root; for (const part of relative.split('/')) { current = path.join(current, part); if (fs.existsSync(current) && (!fs.lstatSync(current).isDirectory() || fs.lstatSync(current).isSymbolicLink())) fail(`backup parent ${relative} uses symlink or non-directory: ${part}`); } }

function actionPath(action) { return action.path.includes(':') && !action.path.startsWith('.my-workflow/') ? action.path.split(':')[0] : action.path; }
function destructive(action) { return ['update', 'replace', 'remove'].includes(action.kind || action.action); }
function linkDestination(root, relative, target) {
  validateRelative(relative);
  if (typeof target !== 'string' || !target || path.posix.isAbsolute(target) || path.posix.normalize(target) !== target) fail(`Claude skill link target is unsafe: ${relative}`);
  ensureDirectory(root, path.posix.dirname(relative));
  const destination = path.join(root, ...relative.split('/'));
  const resolved = path.resolve(path.dirname(destination), target);
  const base = path.resolve(root);
  if (resolved !== path.resolve(root, `.agents/skills/${relative.split('/').at(-1)}`) || !resolved.startsWith(`${base}${path.sep}`)) fail(`Claude skill link target escapes target: ${relative}`);
  const current = fs.lstatSync(destination, { throwIfNoEntry: false });
  if (current && (!current.isSymbolicLink() || fs.readlinkSync(destination) !== target)) fail(`Claude skill link ${relative} is an unsafe collision`);
  return destination;
}

function publishLink(root, relative, target) {
  const destination = linkDestination(root, relative, target);
  if (fs.existsSync(destination) || fs.lstatSync(destination, { throwIfNoEntry: false })) return;
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  linkDestination(root, relative, target);
  fs.symlinkSync(target, destination);
}

function removeLink(root, relative) {
  validateRelative(relative);
  ensureDirectory(root, path.posix.dirname(relative));
  const destination = path.join(root, ...relative.split('/'));
  const current = fs.lstatSync(destination, { throwIfNoEntry: false });
  if (!current) return;
  if (!current.isSymbolicLink()) fail(`restore cleanup ${relative} is not a symlink`);
  fs.unlinkSync(destination);
}
function entry(root, action, backupRoot) {
  const relative = actionPath(action); const file = safePath(root, relative, 'backup source'); if (!fs.existsSync(file)) return null; const stat = fs.lstatSync(file); if (!stat.isFile() || stat.isSymbolicLink()) fail(`backup failed: ${relative} is not a regular file`); const bytes = fs.readFileSync(file); const backup = path.join(backupRoot, 'files', ...relative.split('/')); fs.mkdirSync(path.dirname(backup), { recursive: true }); fs.writeFileSync(backup, bytes, { mode: stat.mode & 0o7777 }); const copied = fs.readFileSync(backup); if (sha256(bytes) !== sha256(copied) || (fs.statSync(backup).mode & 0o7777) !== (stat.mode & 0o7777)) fail(`backup failed: ${relative} could not be verified`); return { path: relative, action: action.kind || action.action, sha256: sha256(bytes), mode: stat.mode & 0o7777, backup: posix(path.relative(backupRoot, backup)) }; }
const posix = (value) => value.split(path.sep).join('/');

export function prepareBackup(input, maybeTarget) {
  const value = input?.plan ? input : { plan: input, targetRoot: maybeTarget }; const root = targetOf(value); const plan = value.plan || {}; const staged = value.staged || {}; const links = value.links || {}; const actions = (plan.actions || []).filter(destructive); for (const [relative, target] of Object.entries(links)) linkDestination(root, relative, target); if (!actions.length && !Object.keys(staged).length && !Object.keys(links).length) return { targetRoot: root, plan, staged, links, backup: null, journal: null, entries: [] };
  const removeLinks = Object.keys(links).filter((relative) => !fs.lstatSync(path.join(root, ...relative.split('/')), { throwIfNoEntry: false }));
  if (!actions.length) { ensureDirectory(root, '.my-workflow'); const adoption = path.join(root, '.my-workflow', 'adoption.json'); const journal = { schema: 1, state: 'prepared', backup: null, restore: [], removeOnRestore: Object.keys(staged).filter((relative) => !fs.existsSync(path.join(root, relative))), removeLinksOnRestore: removeLinks, previousAdoptionState: fs.existsSync(adoption) ? fs.readFileSync(adoption, 'utf8') : null }; atomicWrite(journalPath(root), Buffer.from(`${JSON.stringify(journal, null, 2)}\n`)); return { targetRoot: root, plan, staged, links, backup: null, journal, entries: [] }; }
  const backupRelative = `.my-workflow/backups/${timestamp(value.clock)}`; ensureDirectory(root, '.my-workflow'); ensureDirectory(root, '.my-workflow/backups'); const backupRoot = path.join(root, ...backupRelative.split('/')); if (fs.existsSync(backupRoot)) fail(`backup already exists: ${backupRelative}`); fs.mkdirSync(path.join(backupRoot, 'files'), { recursive: true });
  const entries = []; const seen = new Set(); try { for (const action of actions) { const relative = actionPath(action); if (seen.has(relative)) continue; seen.add(relative); if (value.failBackup === relative) fail(`backup failed: ${relative} could not be verified`); const backupEntry = entry(root, action, backupRoot); if (backupEntry) entries.push(backupEntry); } const manifest = { created_at: new Date(typeof value.clock === 'function' ? value.clock() : value.clock || Date.now()).toISOString(), package: 'workflow-toolkit', version: plan.packageVersion || '1.1.0', target: '.', files: entries }; atomicWrite(path.join(backupRoot, 'manifest.json'), Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`)); const knowledge = (value.knowledgeActions || []).filter((action) => KNOWLEDGE_DESTINATIONS[actionPath(action)]).map((action) => { const relative = actionPath(action); const destination = KNOWLEDGE_DESTINATIONS[relative]; return { source: `${backupRelative}/files/${relative}`, destination: destination.destination, reason: destination.reason, status: 'Pending human transfer' }; }); if (knowledge.length) { if (value.failChecklist) fail('checklist write failed'); const lines = ['# Knowledge transfer', '', 'Review these consumer-owned sources and transfer content manually.', '']; for (const item of knowledge) lines.push(`- Source: ${item.source}`, `  Destination: ${item.destination}`, `  Reason: ${item.reason}`, `  Status: ${item.status}`, ''); atomicWrite(path.join(backupRoot, 'knowledge-transfer.md'), Buffer.from(`${lines.join('\n')}\n`)); } const adoption = safePath(root, '.my-workflow/adoption.json', 'adoption state'); const journal = { schema: 1, state: 'prepared', backup: backupRelative, restore: entries, removeOnRestore: Object.keys(staged).filter((relative) => !fs.existsSync(path.join(root, relative))), removeLinksOnRestore: removeLinks, previousAdoptionState: fs.existsSync(adoption) ? fs.readFileSync(adoption, 'utf8') : null }; atomicWrite(journalPath(root), Buffer.from(`${JSON.stringify(journal, null, 2)}\n`)); return { targetRoot: root, plan, staged, links, backup: backupRelative, journal, entries }; } catch (error) { removePath(backupRoot); const parent = path.dirname(backupRoot); if (fs.existsSync(parent) && fs.readdirSync(parent).length === 0) fs.rmdirSync(parent); throw error; } }

function removePath(target) { if (!fs.existsSync(target) && !fs.lstatSync(target, { throwIfNoEntry: false })) return; const stat = fs.lstatSync(target); if (stat.isDirectory() && !stat.isSymbolicLink()) for (const child of fs.readdirSync(target)) removePath(path.join(target, child)); fs.rmSync(target, { recursive: true, force: true }); }
function publishBytes(root, relative, bytes) { const destination = safePath(root, relative, 'publication destination'); atomicWrite(destination, bytes); }

export function publish(prepared, options = {}) {
  const root = targetOf(prepared); const plan = prepared.plan || {}; const staged = prepared.staged || {}; const links = prepared.links || {}; const entries = prepared.entries || []; const journal = prepared.journal || null; const order = (relative) => relative === '.my-workflow/adoption.json' ? 2 : relative === '.wtk.toml' || relative.startsWith('.claude/agents/') || relative.startsWith('.codex/agents/') || relative.startsWith('.cursor/agents/') ? 1 : 0;
  try { for (const [relative, bytes] of Object.entries(staged).sort(([a], [b]) => order(a) - order(b) || a.localeCompare(b))) { if (relative === '.my-workflow/adoption.json') continue; if (options.failAfter && options.failAfter === relative) fail(`injected publication failure: ${relative}`); publishBytes(root, relative, bytes); options.onPublish?.(relative); } for (const [relative, target] of Object.entries(links).sort(([a], [b]) => a.localeCompare(b))) { if (options.failAfter && options.failAfter === relative) fail(`injected publication failure: ${relative}`); publishLink(root, relative, target); options.onPublish?.(relative); } for (const action of plan.actions || []) if ((action.kind || action.action) === 'remove') { const relative = actionPath(action); const destination = safePath(root, relative, 'retired destination'); if (fs.existsSync(destination)) { if (!fs.lstatSync(destination).isFile()) fail(`retired destination is no longer a file: ${relative}`); fs.unlinkSync(destination); options.onPublish?.(relative); } } if (staged['.my-workflow/adoption.json']) { publishBytes(root, '.my-workflow/adoption.json', staged['.my-workflow/adoption.json']); options.onPublish?.('.my-workflow/adoption.json'); } if (journal && fs.existsSync(journalPath(root))) fs.unlinkSync(journalPath(root)); return { ok: true, backup: prepared.backup }; } catch (error) { if (journal) { try { restoreInterrupted({ targetRoot: root, journal }); } catch (restoreError) { fail(`publication failed and rollback failed: ${restoreError.message}`); } } throw new InstallerError(`publication failed; previous repository state was restored: ${error.message}`); }
}

export function applyTransaction(input, options = {}) { const prepared = prepareBackup(input); return publish(prepared, options); }

export function restoreInterrupted(input) {
  const root = targetOf(input); const journal = input?.journal || (() => { const file = journalPath(root); if (!fs.existsSync(file)) return null; safePath(root, '.my-workflow/transaction.json', 'transaction journal'); try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch (error) { fail(`invalid transaction journal: ${error.message}`); } })(); if (!journal) return { restored: false, reason: 'none' }; if (journal.schema !== 1 || journal.state !== 'prepared' || (journal.backup !== null && typeof journal.backup !== 'string')) fail('invalid transaction journal'); if (journal.backup !== null) { validateRelative(journal.backup); if (!journal.backup.startsWith('.my-workflow/backups/')) fail('transaction backup must stay inside .my-workflow/backups'); const backupRoot = path.resolve(root, ...journal.backup.split('/')); if (backupRoot !== root && !backupRoot.startsWith(`${root}${path.sep}`)) fail('transaction backup must stay inside target'); ensureDirectory(root, '.my-workflow'); ensureDirectory(root, '.my-workflow/backups'); ensureDirectory(root, journal.backup); }
  for (const record of journal.restore || []) { const target = safePath(root, record.path, 'restore target'); const backup = safePath(path.join(root, ...journal.backup.split('/')), record.backup, 'restore backup'); if (!fs.existsSync(backup) || sha256(fs.readFileSync(backup)) !== record.sha256) fail(`backup verification failed: ${record.path}`); publishBytes(root, record.path, fs.readFileSync(backup)); fs.chmodSync(target, record.mode); }
  for (const relative of journal.removeOnRestore || []) { const target = safePath(root, relative, 'restore cleanup'); if (fs.existsSync(target)) removePath(target); }
  for (const relative of journal.removeLinksOnRestore || []) removeLink(root, relative);
  ensureDirectory(root, '.my-workflow'); const adoption = safePath(root, '.my-workflow/adoption.json', 'adoption state'); if (journal.previousAdoptionState === null) { if (fs.existsSync(adoption)) fs.unlinkSync(adoption); } else atomicWrite(adoption, Buffer.from(journal.previousAdoptionState)); if (fs.existsSync(journalPath(root))) fs.unlinkSync(journalPath(root)); return { restored: true, backup: journal.backup };
}

export function hasInterruptedTransaction(root = process.cwd()) { const target = path.resolve(root); const file = journalPath(target); if (!fs.existsSync(file)) return false; safePath(target, '.my-workflow/transaction.json', 'transaction journal'); return true; }
export default { prepareBackup, publish, applyTransaction, restoreInterrupted, hasInterruptedTransaction };
