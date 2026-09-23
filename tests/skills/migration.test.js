import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { applyMigration, LEGACY_PACKET_HASHES, previewMigration, sha256 as migrationSha256 } from '../../scripts/migrate.js';

const temp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'wtk-migration-'));
const file = (root, relative) => path.join(root, ...relative.split('/'));
const hash = (value) => crypto.createHash('sha256').update(value).digest('hex');
const fixtureRoot = path.resolve(import.meta.dirname, '../fixtures/legacy-packets');
const providers = ['claude', 'codex', 'cursor'];
const roles = ['planner', 'implementer', 'verifier', 'explorer', 'deep-reviewer', 'designer'];

function packetRelative(provider, role) {
  return `.${provider}/agents/${role}.${provider === 'codex' ? 'toml' : 'md'}`;
}

function copyLegacyPacket(root, provider, role, suffix = '') {
  const relative = packetRelative(provider, role);
  const source = path.join(fixtureRoot, provider, `${role}.${provider === 'codex' ? 'toml' : 'md'}`);
  write(root, relative, `${fs.readFileSync(source, 'utf8')}${suffix}`);
  return relative;
}

function write(root, relative, content, mode = 0o644) {
  const target = file(root, relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, content);
  fs.chmodSync(target, mode);
}

function adoption(root, files = {}, blocks = {}) {
  write(root, '.my-workflow/adoption.json', `${JSON.stringify({
    schema: 1,
    workflow_version: '1.4.1',
    layers: ['core'],
    files,
    blocks,
  }, null, 2)}\n`);
}

function managedFile(root, relative, content, mode) {
  write(root, relative, content, mode);
  return {
    layer: 'core',
    ownership: 'managed',
    source_sha256: hash(content),
    installed_sha256: hash(content),
  };
}

function managedBlock(root, relative, owner, body) {
  const content = `before project prose\n<!-- my-workflow:${owner}:start -->\n${body}\n<!-- my-workflow:${owner}:end -->\nafter project prose\n`;
  write(root, relative, content, 0o640);
  const block = `<!-- my-workflow:${owner}:start -->\n${body}\n<!-- my-workflow:${owner}:end -->`;
  return { content, key: `${relative}:${owner}`, record: { sha256: hash(block) } };
}

function blockRecord(owner, body) {
  const block = `<!-- my-workflow:${owner}:start -->\n${body}\n<!-- my-workflow:${owner}:end -->`;
  return { sha256: hash(block) };
}

test('migration preview is complete and read only', () => {
  const root = temp();
  const oldSkill = Buffer.from('old skill\n');
  const fileRecord = managedFile(root, '.agents/skills/wtk/SKILL.md', oldSkill);
  const block = managedBlock(root, 'AGENTS.md', 'core', 'legacy workflow instruction');
  fs.mkdirSync(file(root, '.claude/skills'), { recursive: true });
  fs.symlinkSync('../../.agents/skills/wtk', file(root, '.claude/skills/wtk'));
  write(root, '.gitignore', '.gitignore header\n.wtk.toml\nconsumer-rule\n');
  adoption(root, { '.agents/skills/wtk/SKILL.md': fileRecord }, { [block.key]: block.record });

  const before = snapshot(root);
  const result = previewMigration({ root });

  assert.equal(result.status, 'ready');
  assert.deepEqual(result.managedFiles, ['.agents/skills/wtk/SKILL.md']);
  assert.deepEqual(result.managedBlocks, ['AGENTS.md:core']);
  assert.deepEqual(result.links, [{ path: '.claude/skills/wtk', target: '../../.agents/skills/wtk' }]);
  assert.ok(result.actions.some((action) => action.type === 'update-ignore' && action.path === '.gitignore'));
  assert.deepEqual(snapshot(root), before);
});

test('migration retires historical packets without templates', () => {
  const root = temp();
  assert.equal(Object.keys(LEGACY_PACKET_HASHES).length, 18);
  for (const provider of ['claude', 'codex', 'cursor']) {
    for (const role of ['planner', 'implementer', 'verifier', 'explorer', 'deep-reviewer', 'designer']) {
      assert.match(LEGACY_PACKET_HASHES[`${provider}/${role}`], /^[0-9a-f]{64}$/);
    }
  }
  const managed = Buffer.from('retired toolkit file\n');
  const managedRecord = managedFile(root, 'docs/toolkit/README.md', managed);
  const block = managedBlock(root, 'AGENTS.md', 'core', 'legacy workflow instruction');
  fs.appendFileSync(file(root, 'AGENTS.md'), 'legacy workflow prose\n');
  const packetPaths = providers.flatMap((provider) => roles.map((role) => copyLegacyPacket(root, provider, role)));
  write(root, 'consumer.txt', 'keep this file\n', 0o600);
  write(root, '.gitignore', '.wtk.toml\nconsumer-rule\n');
  adoption(root, { 'docs/toolkit/README.md': managedRecord }, { [block.key]: block.record });

  const preview = previewMigration({ root });
  assert.deepEqual(
    new Set(preview.managedFiles),
    new Set(['docs/toolkit/README.md', ...packetPaths]),
  );

  const result = applyMigration({ root, backupId: 'success' });

  assert.equal(result.applied, true);
  assert.equal(fs.existsSync(file(root, 'docs/toolkit/README.md')), false);
  for (const relative of packetPaths) assert.equal(fs.existsSync(file(root, relative)), false, relative);
  assert.equal(fs.readFileSync(file(root, 'AGENTS.md'), 'utf8'), 'before project prose\n\nafter project prose\nlegacy workflow prose\n');
  assert.equal(fs.readFileSync(file(root, 'consumer.txt'), 'utf8'), 'keep this file\n');
  assert.equal(fs.readFileSync(file(root, '.gitignore'), 'utf8'), 'consumer-rule\n');
  assert.equal(fs.existsSync(file(root, '.my-workflow/adoption.json')), false);
  assert.equal(result.manualReview[0].path, 'AGENTS.md');
  assert.equal(fs.existsSync(file(root, '.my-workflow/migration-backups/success/files/AGENTS.md')), true);
  assert.equal(fs.statSync(file(root, '.my-workflow/migration-backups/success/files/AGENTS.md')).mode & 0o7777, 0o640);
});

test('migration refuses edited historical provider packets', () => {
  for (const provider of providers) {
    for (const role of roles) {
      const root = temp();
      const relative = copyLegacyPacket(root, provider, role, '\nconsumer edit\n');
      adoption(root);

      const preview = previewMigration({ root });
      assert.equal(preview.actions.some((action) => action.path === relative), false, relative);
      assert.equal(fs.readFileSync(file(root, relative), 'utf8').endsWith('consumer edit\n'), true, relative);
    }
  }
});

test('migration removes multiple verified blocks from one instruction file exactly', () => {
  const root = temp();
  const core = 'core workflow block';
  const quality = 'quality review block';
  write(root, 'AGENTS.md', [
    'project before',
    '<!-- my-workflow:core:start -->', core, '<!-- my-workflow:core:end -->',
    'project between',
    '<!-- my-workflow:quality:start -->', quality, '<!-- my-workflow:quality:end -->',
    'project after',
    '',
  ].join('\n'), 0o640);
  adoption(root, {}, {
    'AGENTS.md:core': blockRecord('core', core),
    'AGENTS.md:quality': blockRecord('quality', quality),
  });

  const result = applyMigration({ root, backupId: 'two-blocks' });

  assert.equal(result.applied, true);
  assert.equal(fs.readFileSync(file(root, 'AGENTS.md'), 'utf8'), 'project before\n\nproject between\n\nproject after\n');
  assert.deepEqual(result.managedBlocks.sort(), ['AGENTS.md:core', 'AGENTS.md:quality']);
});

test('migration refuses modified owned content without writes', () => {
  const root = temp();
  const record = managedFile(root, '.agents/skills/wtk/SKILL.md', Buffer.from('original\n'));
  write(root, '.agents/skills/wtk/SKILL.md', 'consumer edit\n');
  adoption(root, { '.agents/skills/wtk/SKILL.md': record });
  const before = snapshot(root);

  assert.throws(() => applyMigration({ root }), /migration refused modified owned content/);
  assert.deepEqual(snapshot(root), before);
});

test('migration rollback restores exact prior state', () => {
  const root = temp();
  const record = managedFile(root, '.agents/skills/wtk/SKILL.md', Buffer.from('old skill\n'), 0o640);
  const block = managedBlock(root, 'AGENTS.md', 'core', 'legacy workflow instruction');
  write(root, '.gitignore', '.wtk.toml\nconsumer-rule\n', 0o600);
  adoption(root, { '.agents/skills/wtk/SKILL.md': record }, { [block.key]: block.record });
  const before = snapshot(root);

  assert.throws(() => applyMigration({ root, backupId: 'rollback', failAfter: 'AGENTS.md' }), /previous repository state was restored/);
  assert.deepEqual(snapshot(root), before);
  assert.equal(fs.existsSync(file(root, '.my-workflow/migration.json')), false);
  assert.equal(fs.existsSync(file(root, '.my-workflow/migration-backups/rollback')), false);
});

function snapshot(root) {
  const result = {};
  const walk = (directory) => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const full = path.join(directory, entry.name);
      const relative = path.relative(root, full).split(path.sep).join('/');
      if (entry.isDirectory() && !entry.isSymbolicLink()) walk(full);
      else if (entry.isFile()) result[relative] = { type: 'file', bytes: fs.readFileSync(full).toString('base64'), mode: fs.statSync(full).mode & 0o7777 };
      else if (entry.isSymbolicLink()) result[relative] = { type: 'symlink', target: fs.readlinkSync(full) };
    }
  };
  walk(root);
  return result;
}

assert.equal(typeof migrationSha256, 'function');
