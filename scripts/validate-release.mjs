import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const releaseTag = process.env.RELEASE_TAG ?? '';
const releaseSha = process.env.RELEASE_SHA ?? '';
const stableTag = /^v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)$/;
const commitSha = /^[0-9a-f]{40}$/;

function fail(message) {
  console.error(`release validation failed: ${message}`);
  process.exit(1);
}

if (!stableTag.test(releaseTag)) {
  fail('tag must match vX.Y.Z');
}
if (!commitSha.test(releaseSha)) {
  fail('event commit must be a 40-character commit SHA');
}

function git(args) {
  try {
    return execFileSync('git', args, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    }).trim();
  } catch {
    fail(`git could not resolve ${args.join(' ')}`);
  }
}

const tagCommit = git(['rev-parse', '--verify', `${releaseTag}^{commit}`]);
const headCommit = git(['rev-parse', '--verify', 'HEAD^{commit}']);
if (headCommit !== releaseSha) {
  fail(`HEAD ${headCommit} does not match event commit ${releaseSha}`);
}
if (tagCommit !== releaseSha) {
  fail(`tag ${releaseTag} does not match event commit ${releaseSha}`);
}
try {
  execFileSync('git', ['merge-base', '--is-ancestor', releaseSha, 'refs/remotes/origin/main'], {
    stdio: 'ignore',
  });
} catch {
  fail(`tag ${releaseTag} is not reachable from main`);
}

let manifest;
try {
  manifest = JSON.parse(readFileSync('package.json', 'utf8'));
} catch {
  fail('package.json is not valid JSON');
}

const expectedVersion = releaseTag.slice(1);
if (manifest.name !== 'workflow-toolkit') {
  fail(`package name must be workflow-toolkit, found ${manifest.name ?? '<missing>'}`);
}
if (manifest.version !== expectedVersion) {
  fail(`package version must be ${expectedVersion}, found ${manifest.version ?? '<missing>'}`);
}

console.log(`validated ${releaseTag} at ${tagCommit} for ${manifest.name}@${manifest.version}`);
