import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const root = path.resolve(import.meta.dirname, '../..');
const wtkSkills = fs.readdirSync(path.join(root, '.agents/skills'), { withFileTypes: true })
  .filter((entry) => entry.isDirectory() && (entry.name === 'wtk' || entry.name.startsWith('wtk-')))
  .map((entry) => entry.name)
  .sort();
const optionalSkills = ['ponytail', 'prompt-review', 'security-implementation', 'security-review', 'security-spec', 'security-threat-model'];
const read = (relative) => fs.readFileSync(path.join(root, relative), 'utf8');

test('published WTK skills resolve every local reference', () => {
  assert.deepEqual(wtkSkills, [
    'wtk', 'wtk-config', 'wtk-deep-review', 'wtk-discover', 'wtk-implement',
    'wtk-knowledge-check', 'wtk-lean', 'wtk-plan', 'wtk-qa', 'wtk-qa-execute',
    'wtk-qa-plan', 'wtk-reuse-review', 'wtk-ship',
  ]);
  for (const skill of wtkSkills) {
    const skillRoot = path.join(root, '.agents/skills', skill);
    assert.equal(fs.statSync(path.join(skillRoot, 'SKILL.md')).isFile(), true, skill);
    const files = walk(skillRoot);
    for (const relative of files) {
      const source = fs.readFileSync(path.join(skillRoot, relative), 'utf8');
      for (const match of source.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
        const target = match[1].split('#')[0];
        if (!target || target.includes('[') || target.includes('*') || target.includes('?') || target.startsWith('http://') || target.startsWith('https://') || target.startsWith('mailto:')) continue;
        assert.equal(fs.existsSync(path.resolve(path.dirname(path.join(skillRoot, relative)), target)), true, `${skill}/${relative}: ${target}`);
      }
      for (const match of source.matchAll(/(?:^|[ `(])((?:references|scripts)\/[A-Za-z0-9_.()/-]+\.(?:md|py|mjs|ts))(?=$|[` )])/gm)) {
        if (match[1].includes('[') || match[1].includes('*') || match[1].includes('?')) continue;
        assert.equal(fs.existsSync(path.join(skillRoot, match[1])), true, `${skill}/${relative}: ${match[1]}`);
      }
    }
  }
});

test('Skills CLI discovers every WTK skill when the source lock has no self entries', () => {
  const source = fs.mkdtempSync(path.join(os.tmpdir(), 'wtk-discovery-'));
  try {
    for (const skill of wtkSkills) fs.cpSync(path.join(root, '.agents/skills', skill), path.join(source, '.agents/skills', skill), { recursive: true });
    const cli = path.join(root, 'node_modules/skills/dist/cli.mjs');
    const clean = spawnSync(process.execPath, [cli, 'add', source, '--list', '--full-depth'], { cwd: source, encoding: 'utf8' });
    assert.equal(clean.status, 0, clean.stderr);
    assert.match(clean.stdout, /Found 13 skills/);

    fs.writeFileSync(path.join(source, 'skills-lock.json'), JSON.stringify({ version: 1, skills: { wtk: {}, 'wtk-lean': {}, 'wtk-deep-review': {} } }));
    const locked = spawnSync(process.execPath, [cli, 'add', source, '--list', '--full-depth'], { cwd: source, encoding: 'utf8' });
    assert.equal(locked.status, 0, locked.stderr);
    assert.match(locked.stdout, /Found 10 skills/);
  } finally {
    fs.rmSync(source, { recursive: true, force: true });
  }
});

test('skill installation leaves project harness files untouched', () => {
  const target = fs.mkdtempSync(path.join(os.tmpdir(), 'wtk-skills-target-'));
  const sentinels = {
    'AGENTS.md': 'project instructions\n',
    'CLAUDE.md': '@AGENTS.md\n',
    '.wtk.toml': 'project config\n',
    '.wtk.toml.example': 'project config example\n',
    '.gitignore': 'project ignore\n',
    '.ignore': 'project search ignore\n',
    '.claude/agents/planner.md': 'project planner\n',
    '.codex/agents/planner.toml': 'project codex\n',
    '.cursor/agents/planner.md': 'project cursor\n',
    'knowledge/AGENTS.md': 'project knowledge\n',
    'knowledge/raw/README.md': 'project raw\n',
  };
  for (const [relative, bytes] of Object.entries(sentinels)) {
    const destination = path.join(target, ...relative.split('/'));
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.writeFileSync(destination, bytes);
  }
  const before = Object.fromEntries(Object.entries(sentinels).map(([relative]) => [relative, fs.readFileSync(path.join(target, ...relative.split('/')))]));
  for (const skill of wtkSkills) fs.cpSync(path.join(root, '.agents/skills', skill), path.join(target, '.agents/skills', skill), { recursive: true });
  for (const [relative, bytes] of Object.entries(before)) assert.deepEqual(fs.readFileSync(path.join(target, ...relative.split('/'))), bytes, relative);
  assert.equal(fs.existsSync(path.join(target, '.my-workflow')), false);
  assert.equal(fs.existsSync(path.join(target, 'templates')), false);
});

test('distribution has no npm install command or adoption manifest', () => {
  const packageJson = JSON.parse(read('package.json'));
  assert.equal(packageJson.private, true);
  assert.equal('bin' in packageJson, false);
  assert.equal(fs.existsSync(path.join(root, 'bin/wtk.js')), false);
  assert.equal(fs.existsSync(path.join(root, 'scripts/installer')), false);
  assert.equal(fs.existsSync(path.join(root, 'templates/adoption')), false);
  assert.equal(read('README.md').includes('npx workflow-toolkit install'), false);
  assert.equal(read('README.md').includes('wtk install'), false);
  assert.match(read('README.md'), /skill installer/i);
  assert.match(read('README.md'), /npx skills add antoniofulg\/workflow-toolkit/);
  assert.match(read('README.md'), /skills update/);
  assert.equal(packageJson.files.some((entry) => entry.includes('scripts/installer') || entry.includes('templates/adoption')), false);
});

test('WTK routes resolve references without optional companions', () => {
  const optionalPaths = optionalSkills.map((skill) => path.join(root, '.agents/skills', skill));
  for (const optionalPath of optionalPaths) assert.equal(fs.existsSync(optionalPath), false, optionalPath);
  const routed = wtkSkills.flatMap((skill) => walk(path.join(root, '.agents/skills', skill)).map((relative) => path.join(skill, relative)));
  for (const relative of routed) {
    const source = read(path.join('.agents/skills', relative));
    assert.doesNotMatch(source, /docs\/toolkit\/guidelines\//, relative);
  }
  assert.match(read('.agents/skills/wtk/references/security.md'), /optional `security-(?:implementation|spec|threat-model|review)` skill/i);
  assert.match(read('.agents/skills/wtk-deep-review/SKILL.md'), /failed or absent Graft falls back/i);
  assert.match(read('.agents/skills/wtk-deep-review/references/orchestration.md'), /plain repository inspection/i);
});

test('skills-only documentation and phase contracts remain reachable', () => {
  const readme = read('README.md');
  for (const name of ['wtk', 'wtk-lean', 'wtk-plan', 'wtk-implement', 'wtk-qa', 'wtk-deep-review', 'wtk-ship']) assert.match(readme, new RegExp(`\`${name}\``));
  assert.match(readme, /optional project instructions/i);
  assert.match(readme, /Ponytail/);
  assert.match(readme, /Security lifecycle/);
  assert.match(readme, /Adaptive Guidelines/);
  assert.match(readme, /Graphify/);
  assert.match(readme, /Graft/);
  assert.match(readme, /dietrichgebert\/ponytail/);
  assert.match(readme, /antoniofulg\/security-lifecycle/);
  assert.match(readme, /github.com\/trailhq\/Graft/);
  assert.match(readme, /pypi.org\/project\/graphifyy/);
  assert.match(read('.agents/skills/wtk-lean/SKILL.md'), /one fresh Verifier/);
  assert.match(read('.agents/skills/wtk-lean/references/checks.md'), /Coverage/);
  assert.match(read('.agents/skills/wtk/references/validation.md'), /full gate/);
  assert.match(read('.agents/skills/wtk/references/review-rounds.md'), /Technical Verifier/);
  assert.match(read('.agents/skills/wtk-qa/references/qa-scenarios.md'), /scenario/i);
  assert.match(read('.agents/skills/wtk-qa-execute/SKILL.md'), /independent confirmation/i);
  assert.match(read('.agents/skills/wtk-ship/SKILL.md'), /authoriz/i);
});

function walk(directory) {
  const result = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    if (entry.name === '__pycache__' || entry.name.endsWith('.pyc')) continue;
    const full = path.join(directory, entry.name);
    if (entry.isDirectory()) result.push(...walk(full).map((relative) => path.join(entry.name, relative)));
    else if (entry.isFile()) result.push(entry.name);
  }
  return result;
}
