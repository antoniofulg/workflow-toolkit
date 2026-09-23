#!/usr/bin/env node

import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const ADOPTION_FILE = '.my-workflow/adoption.json';
const JOURNAL_FILE = '.my-workflow/migration.json';
const BACKUP_ROOT = '.my-workflow/migration-backups';

// These are the entries written by the retired installer. Removing only exact lines keeps
// consumer ignore rules intact while allowing an old adoption to leave cleanly.
export const LEGACY_IGNORE_ENTRIES = [
  '.wtk.toml',
  '.claude/agents/',
  '.codex/agents/',
  '.cursor/agents/',
  '!.wtk-deep-review/',
  '.wtk-deep-review/*',
  '!.wtk-deep-review/learnings.md',
  'graft/',
  'graphify-out/',
  '.repository-intelligence/',
];
export const LEGACY_SEARCHIGNORE_ENTRIES = [
  '!graft/',
  'graft/.cache/',
  'graft/.graph/',
  'graphify-out/',
  '.repository-intelligence/',
];
const PROVIDERS = ['claude', 'codex', 'cursor'];
const ROLES = ['planner', 'implementer', 'verifier', 'explorer', 'deep-reviewer', 'designer'];
const packetRelative = (provider, role) => `.${provider}/agents/${role}.${provider === 'codex' ? 'toml' : 'md'}`;
const packetTemplate = (provider, role) => `.agents/skills/wtk-config/assets/agents/${provider}/${role}.${provider === 'codex' ? 'toml' : 'md'}`;

export class MigrationError extends Error {}

const fail = (message) => {
  throw new MigrationError(message);
};

const asRoot = (value) => path.resolve(value || process.cwd());
const toPosix = (value) => value.split(path.sep).join('/');
const relativePath = (root, file) => toPosix(path.relative(root, file));
export const sha256 = (value) => crypto.createHash('sha256').update(value).digest('hex');

function ensureRelative(relative) {
  if (
    typeof relative !== 'string' ||
    !relative ||
    path.posix.isAbsolute(relative) ||
    relative.split('/').some((part) => !part || part === '.' || part === '..') ||
    toPosix(relative) !== relative
  ) {
    fail(`migration path is unsafe: ${relative}`);
  }
  return relative;
}

function safePath(root, relative, label = 'migration path') {
  ensureRelative(relative);
  const base = asRoot(root);
  const target = path.join(base, ...relative.split('/'));
  let current = base;
  for (const part of relative.split('/')) {
    current = path.join(current, part);
    if (fs.existsSync(current) && fs.lstatSync(current).isSymbolicLink()) {
      fail(`${label} ${relative} uses symlink ${toPosix(path.relative(base, current))}`);
    }
    if (current !== target && fs.existsSync(current) && !fs.lstatSync(current).isDirectory()) {
      fail(`${label} parent ${toPosix(path.relative(base, current))} must be a directory`);
    }
  }
  return target;
}

function safeLinkPath(root, relative, label = 'migration link') {
  ensureRelative(relative);
  const base = asRoot(root);
  const parts = relative.split('/');
  let current = base;
  for (const part of parts.slice(0, -1)) {
    current = path.join(current, part);
    if (fs.existsSync(current) && fs.lstatSync(current).isSymbolicLink()) {
      fail(`${label} ${relative} uses symlink parent ${toPosix(path.relative(base, current))}`);
    }
    if (fs.existsSync(current) && !fs.lstatSync(current).isDirectory()) {
      fail(`${label} parent ${toPosix(path.relative(base, current))} must be a directory`);
    }
  }
  return path.join(base, ...parts);
}

function readJson(file, label) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    fail(`invalid ${label}: ${error.message}`);
  }
}

function readAdoption(root) {
  const file = safePath(root, ADOPTION_FILE, 'adoption manifest');
  if (!fs.existsSync(file)) return null;
  if (!fs.lstatSync(file).isFile()) fail('adoption manifest must be a regular file');
  const manifest = readJson(file, 'adoption manifest');
  if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest)) {
    fail('adoption manifest must be an object');
  }
  if (manifest.schema !== 1 || typeof manifest.workflow_version !== 'string') {
    fail('adoption manifest has an unsupported schema');
  }
  if (!manifest.files || typeof manifest.files !== 'object' || Array.isArray(manifest.files)) {
    fail('adoption manifest files must be an object');
  }
  if (!manifest.blocks || typeof manifest.blocks !== 'object' || Array.isArray(manifest.blocks)) {
    fail('adoption manifest blocks must be an object');
  }
  return manifest;
}

function checkRegularFile(root, relative, expected, label) {
  const file = safePath(root, relative, label);
  if (!fs.existsSync(file)) return { file, conflict: `${relative}: managed file is missing` };
  const stat = fs.lstatSync(file);
  if (!stat.isFile()) return { file, conflict: `${relative}: managed path is not a regular file` };
  const bytes = fs.readFileSync(file);
  if (expected !== sha256(bytes)) {
    return { file, conflict: `${relative}: content differs from the recorded hash` };
  }
  return { file, bytes, mode: stat.mode & 0o7777 };
}

function blockParts(key) {
  const separator = key.lastIndexOf(':');
  if (separator < 1) fail(`invalid managed block key: ${key}`);
  const relative = key.slice(0, separator);
  const owner = key.slice(separator + 1);
  ensureRelative(relative);
  if (!['AGENTS.md', 'CLAUDE.md'].includes(relative) || !['core', 'quality'].includes(owner)) {
    fail(`invalid managed block key: ${key}`);
  }
  return { key, relative, owner };
}

function blockRange(text, owner) {
  const start = `<!-- my-workflow:${owner}:start -->`;
  const end = `<!-- my-workflow:${owner}:end -->`;
  const first = text.indexOf(start);
  const last = text.indexOf(end);
  if (first < 0 && last < 0) return null;
  if (first < 0 || last < 0 || last < first) return { error: 'managed block is incomplete' };
  if (text.indexOf(start, first + start.length) >= 0 || text.indexOf(end, last + end.length) >= 0) {
    return { error: 'managed block is duplicated' };
  }
  return { start: first, end: last + end.length, bytes: Buffer.from(text.slice(first, last + end.length)) };
}

function managedSkillNames(manifest) {
  const names = new Set();
  for (const relative of Object.keys(manifest.files || {})) {
    const match = /^\.agents\/skills\/([^/]+)\//.exec(relative);
    if (match) names.add(match[1]);
  }
  return names;
}

function findLinks(root, manifest) {
  const directory = safePath(root, '.claude/skills', 'Claude skill links');
  if (!fs.existsSync(directory)) return [];
  if (!fs.lstatSync(directory).isDirectory()) fail('Claude skill links directory must be a directory');
  const names = managedSkillNames(manifest);
  return fs.readdirSync(directory).sort().flatMap((name) => {
    if (!names.has(name)) return [];
    const relative = `.claude/skills/${name}`;
    const target = path.join(directory, name);
    if (!fs.lstatSync(target).isSymbolicLink()) return [];
    const link = fs.readlinkSync(target);
    if (link !== `../../.agents/skills/${name}`) return [];
    return [{ type: 'remove-link', path: relative, target: link }];
  });
}

function ignoreActions(root, relative, entries) {
  const file = safePath(root, relative, 'ignore file');
  if (!fs.existsSync(file)) return [];
  if (!fs.lstatSync(file).isFile()) fail(`ignore file ${relative} must be a regular file`);
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  const removals = lines.filter((line) => entries.includes(line));
  if (!removals.length) return [];
  return [{ type: 'update-ignore', path: relative, remove: [...new Set(removals)] }];
}

function normalizePacket(text, provider) {
  if (provider === 'codex') return text.replace(/^model\s*=\s*"[^\n]*"\s*$/gm, '').replace(/^model_reasoning_effort\s*=\s*"[^\n]*"\s*$/gm, '');
  if (provider === 'cursor') return text.replace(/^model:\s*[^\n]*$/gm, '');
  return text.replace(/^model:\s*[^\n]*$/gm, '').replace(/^effort:\s*[^\n]*$/gm, '');
}

function providerPacketActions(root, sourceRoot) {
  const source = asRoot(sourceRoot || process.cwd());
  const actions = [];
  for (const provider of PROVIDERS) for (const role of ROLES) {
    const relative = packetRelative(provider, role);
    const target = safePath(root, relative, 'provider packet');
    const template = path.join(source, ...packetTemplate(provider, role).split('/'));
    if (!fs.existsSync(target) || !fs.existsSync(template)) continue;
    if (!fs.lstatSync(target).isFile() || !fs.lstatSync(template).isFile()) continue;
    if (normalizePacket(fs.readFileSync(target, 'utf8'), provider) === normalizePacket(fs.readFileSync(template, 'utf8'), provider)) {
      actions.push({ type: 'remove-file', path: relative, reason: 'retired generated provider packet' });
    }
  }
  return actions;
}

function legacyProse(root, blockActions) {
  const result = [];
  for (const relative of ['AGENTS.md', 'CLAUDE.md']) {
    const file = safePath(root, relative, 'instruction file');
    if (!fs.existsSync(file) || !fs.lstatSync(file).isFile()) continue;
    let text = fs.readFileSync(file, 'utf8');
    for (const action of blockActions.filter((item) => item.path === relative)) {
      const range = blockRange(text, action.owner);
      if (range && !range.error) text = text.slice(0, range.start) + text.slice(range.end);
    }
    const lines = text.split(/\r?\n/);
    const matches = lines.flatMap((line, index) => {
      if (!/\b(?:workflow|my-workflow|wtk(?:[- ]|\b)|ponytail|security-(?:spec|review|implementation|threat)|feature\s*[-→>]\s*slice)\b/i.test(line)) return [];
      return [{ line: index + 1, text: line }];
    });
    if (matches.length) result.push({ path: relative, lines: matches });
  }
  return result;
}

function migrationReport(root, manifest, sourceRoot) {
  const report = {
    root,
    status: manifest ? 'ready' : 'not-installed',
    adoption: manifest ? ADOPTION_FILE : null,
    actions: [],
    managedFiles: [],
    managedBlocks: [],
    links: [],
    conflicts: [],
    manualReview: [],
  };
  if (!manifest) return report;

  for (const [relative, record] of Object.entries(manifest.files).sort(([a], [b]) => a.localeCompare(b))) {
    ensureRelative(relative);
    if (record?.ownership !== 'managed') continue;
    if (typeof record.installed_sha256 !== 'string' || !/^[0-9a-f]{64}$/.test(record.installed_sha256)) {
      report.conflicts.push({ path: relative, reason: 'managed record has no valid installed hash' });
      continue;
    }
    const checked = checkRegularFile(root, relative, record.installed_sha256, 'managed file');
    if (checked.conflict) report.conflicts.push({ path: relative, reason: checked.conflict });
    else report.actions.push({ type: 'remove-file', path: relative, mode: checked.mode });
  }

  for (const [key, record] of Object.entries(manifest.blocks).sort(([a], [b]) => a.localeCompare(b))) {
    const block = blockParts(key);
    const expected = record?.sha256;
    if (typeof expected !== 'string' || !/^[0-9a-f]{64}$/.test(expected)) {
      report.conflicts.push({ path: key, reason: 'managed block has no valid hash' });
      continue;
    }
    const file = safePath(root, block.relative, 'managed instruction');
    if (!fs.existsSync(file)) {
      report.conflicts.push({ path: key, reason: 'managed instruction file is missing' });
      continue;
    }
    if (!fs.lstatSync(file).isFile()) {
      report.conflicts.push({ path: key, reason: 'managed instruction path is not a regular file' });
      continue;
    }
    const range = blockRange(fs.readFileSync(file, 'utf8'), block.owner);
    if (!range || range.error) {
      report.conflicts.push({ path: key, reason: range?.error || 'managed block is missing' });
      continue;
    }
    if (sha256(range.bytes) !== expected) {
      report.conflicts.push({ path: key, reason: 'managed block differs from the recorded hash' });
      continue;
    }
    report.actions.push({ type: 'remove-block', path: block.relative, owner: block.owner, key });
  }

  report.actions.push(...providerPacketActions(root, sourceRoot));
  report.actions.push(...findLinks(root, manifest));
  report.actions.push(...ignoreActions(root, '.gitignore', LEGACY_IGNORE_ENTRIES));
  report.actions.push(...ignoreActions(root, '.ignore', LEGACY_SEARCHIGNORE_ENTRIES));
  report.managedFiles = report.actions.filter((item) => item.type === 'remove-file').map((item) => item.path);
  report.managedBlocks = report.actions.filter((item) => item.type === 'remove-block').map((item) => item.key);
  report.links = report.actions.filter((item) => item.type === 'remove-link').map((item) => ({ path: item.path, target: item.target }));
  report.manualReview = legacyProse(root, report.actions.filter((item) => item.type === 'remove-block'));
  if (report.conflicts.length) report.status = 'conflict';
  return report;
}

export function previewMigration(options = {}) {
  const root = asRoot(options.targetRoot ?? options.root);
  return migrationReport(root, readAdoption(root), options.sourceRoot);
}

function stateFor(root, relative) {
  const file = safeLinkPath(root, relative, 'migration target');
  if (!fs.existsSync(file)) return { path: relative, type: 'absent' };
  const stat = fs.lstatSync(file);
  if (stat.isSymbolicLink()) return { path: relative, type: 'symlink', target: fs.readlinkSync(file) };
  if (!stat.isFile()) fail(`migration target ${relative} must be a regular file or symlink`);
  return { path: relative, type: 'file', bytes: fs.readFileSync(file), mode: stat.mode & 0o7777 };
}

function writeFile(root, relative, bytes, mode) {
  const file = safePath(root, relative, 'migration destination');
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, bytes);
  if (mode !== undefined) fs.chmodSync(file, mode);
}

function removeTarget(root, relative) {
  const file = safeLinkPath(root, relative, 'migration target');
  if (fs.existsSync(file) || fs.lstatSync(file, { throwIfNoEntry: false })) fs.rmSync(file, { force: true });
}

function restoreState(root, state) {
  const file = safeLinkPath(root, state.path, 'migration restore target');
  if (state.type === 'absent') {
    if (fs.existsSync(file) || fs.lstatSync(file, { throwIfNoEntry: false })) fs.rmSync(file, { force: true });
    return;
  }
  if (fs.existsSync(file) || fs.lstatSync(file, { throwIfNoEntry: false })) fs.rmSync(file, { force: true });
  fs.mkdirSync(path.dirname(file), { recursive: true });
  if (state.type === 'symlink') fs.symlinkSync(state.target, file);
  else writeFile(root, state.path, state.bytes, state.mode);
}

function backupState(root, backupRoot, states) {
  const files = path.join(root, backupRoot, 'files');
  fs.mkdirSync(files, { recursive: true });
  const modes = {};
  const links = {};
  for (const state of states) {
    if (state.type === 'file') {
      const destination = path.join(files, ...state.path.split('/'));
      fs.mkdirSync(path.dirname(destination), { recursive: true });
      fs.writeFileSync(destination, state.bytes);
      fs.chmodSync(destination, state.mode);
      modes[state.path] = state.mode;
    } else if (state.type === 'symlink') {
      links[state.path] = state.target;
    }
  }
  fs.writeFileSync(path.join(root, backupRoot, 'modes.json'), `${JSON.stringify(modes, null, 2)}\n`);
  fs.writeFileSync(path.join(root, backupRoot, 'links.json'), `${JSON.stringify(links, null, 2)}\n`);
}

function backupStatePath(root, backupRoot, relative) {
  return path.join(root, backupRoot, 'files', ...relative.split('/'));
}

function restoreFromBackup(root, journal) {
  for (const state of journal.states) {
    if (state.type === 'file') {
      const backup = backupStatePath(root, journal.backup, state.path);
      restoreState(root, { ...state, bytes: fs.readFileSync(backup) });
    } else restoreState(root, state);
  }
}

function removeEmptyParents(root, relative) {
  let current = path.dirname(safePath(root, relative, 'cleanup path'));
  const base = asRoot(root);
  while (current !== base && current !== path.join(base, '.my-workflow')) {
    try {
      if (fs.readdirSync(current).length) break;
      fs.rmdirSync(current);
    } catch {
      break;
    }
    current = path.dirname(current);
  }
}

function maybeFail(options, action, index) {
  if (options.failAfter === index || options.failAfter === action.path) {
    throw new Error(`simulated migration publication failure after ${action.path}`);
  }
}

function timestamp(options) {
  return options.backupId || new Date().toISOString().replace(/[:.]/g, '-') + `-${process.pid}`;
}

export function applyMigration(options = {}) {
  const root = asRoot(options.targetRoot ?? options.root);
  const report = migrationReport(root, readAdoption(root), options.sourceRoot);
  if (report.status === 'not-installed') return { ...report, applied: false, backup: null };
  if (report.conflicts.length) {
    fail(`migration refused modified owned content: ${report.conflicts.map((item) => item.path).join(', ')}`);
  }

  const changedPaths = new Set(report.actions.map((item) => item.path));
  changedPaths.add(ADOPTION_FILE);
  const states = [...changedPaths].sort().map((relative) => stateFor(root, relative));
  const backup = `${BACKUP_ROOT}/${timestamp(options)}`;
  const backupDirectory = path.join(root, backup);
  fs.mkdirSync(backupDirectory, { recursive: true });
  backupState(root, backup, states);
  fs.writeFileSync(path.join(root, backup, 'manifest.json'), `${JSON.stringify(readAdoption(root), null, 2)}\n`);
  const journal = { version: 1, backup, states: states.map(({ path: relative, type, target, mode }) => ({ path: relative, type, target, mode })) };
  fs.writeFileSync(path.join(root, JOURNAL_FILE), `${JSON.stringify(journal, null, 2)}\n`);

  try {
    let index = 0;
    const blockActions = report.actions.filter((item) => item.type === 'remove-block');
    const blockFiles = new Map();
    for (const action of blockActions) {
      const file = safePath(root, action.path, 'managed instruction');
      const current = fs.readFileSync(file, 'utf8');
      const range = blockRange(current, action.owner);
      if (!range || range.error) fail(`managed block changed during migration: ${action.key}`);
      const next = current.slice(0, range.start) + current.slice(range.end);
      blockFiles.set(action.path, Buffer.from(next));
    }
    for (const [relative, bytes] of blockFiles) {
      const state = states.find((item) => item.path === relative);
      writeFile(root, relative, bytes, state?.mode);
      maybeFail(options, { path: relative }, index++);
    }
    for (const action of report.actions.filter((item) => item.type === 'remove-file')) {
      removeTarget(root, action.path);
      removeEmptyParents(root, action.path);
      maybeFail(options, action, index++);
    }
    for (const action of report.actions.filter((item) => item.type === 'remove-link')) {
      removeTarget(root, action.path);
      removeEmptyParents(root, action.path);
      maybeFail(options, action, index++);
    }
    for (const action of report.actions.filter((item) => item.type === 'update-ignore')) {
      const file = safePath(root, action.path, 'ignore file');
      const current = fs.readFileSync(file, 'utf8');
      const next = current
        .split(/\r?\n/)
        .filter((line) => !action.remove.includes(line))
        .join('\n');
      writeFile(root, action.path, Buffer.from(next), states.find((item) => item.path === action.path)?.mode);
      maybeFail(options, action, index++);
    }
    removeTarget(root, ADOPTION_FILE);
    maybeFail(options, { path: ADOPTION_FILE }, index++);
    fs.rmSync(path.join(root, JOURNAL_FILE), { force: true });
    return { ...report, applied: true, backup };
  } catch (error) {
    try {
      restoreFromBackup(root, journal);
      fs.rmSync(path.join(root, JOURNAL_FILE), { force: true });
      fs.rmSync(backupDirectory, { recursive: true, force: true });
      const migrationDirectory = path.dirname(backupDirectory);
      if (fs.existsSync(migrationDirectory) && !fs.readdirSync(migrationDirectory).length) fs.rmdirSync(migrationDirectory);
    } catch (restoreError) {
      throw new MigrationError(`migration failed and rollback failed: ${restoreError.message}`);
    }
    throw new MigrationError(`migration publication failed; previous repository state was restored: ${error.message}`);
  }
}

export function restoreInterruptedMigration(options = {}) {
  const root = asRoot(options.targetRoot ?? options.root);
  const journalPath = safePath(root, JOURNAL_FILE, 'migration journal');
  if (!fs.existsSync(journalPath)) return { restored: false, root };
  const journal = readJson(journalPath, 'migration journal');
  restoreFromBackup(root, journal);
  fs.rmSync(journalPath, { force: true });
  fs.rmSync(path.join(root, journal.backup), { recursive: true, force: true });
  return { restored: true, root };
}

export function migrate(options = {}) {
  return options.apply ? applyMigration(options) : previewMigration(options);
}

export function formatReport(report) {
  const lines = [`Migration ${report.status}: ${report.root}`];
  for (const action of report.actions) {
    const label = action.type === 'remove-block' ? 'REMOVE BLOCK' : action.type === 'remove-link' ? 'REMOVE LINK' : action.type === 'update-ignore' ? 'UPDATE IGNORE' : 'REMOVE FILE';
    lines.push(`  ${label.padEnd(13)} ${action.key || action.path}`);
  }
  for (const conflict of report.conflicts) lines.push(`  CONFLICT      ${conflict.path} (${conflict.reason})`);
  for (const item of report.manualReview) lines.push(`  REVIEW        ${item.path}:${item.lines.map((line) => line.line).join(',')}`);
  if (!report.actions.length && !report.conflicts.length && !report.manualReview.length) lines.push('  No toolkit-owned content found.');
  return lines.join('\n');
}

function cli(argv) {
  const args = new Set(argv);
  const rootIndex = argv.indexOf('--root');
  const root = rootIndex >= 0 ? argv[rootIndex + 1] : process.cwd();
  if (args.has('--help') || args.has('-h')) {
    process.stdout.write('Usage: node scripts/migrate.js [--root <project>] [--apply] [--json]\n');
    return 0;
  }
  if (rootIndex >= 0 && (!root || root.startsWith('--'))) {
    process.stderr.write('--root requires a project path\n');
    return 2;
  }
  try {
    const result = migrate({ root, apply: args.has('--apply') });
    process.stdout.write(args.has('--json') ? `${JSON.stringify(result, null, 2)}\n` : `${formatReport(result)}\n`);
    return 0;
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    return 1;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname)) {
  process.exitCode = cli(process.argv.slice(2));
}
