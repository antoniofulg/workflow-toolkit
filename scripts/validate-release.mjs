import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const releaseTag = process.env.RELEASE_TAG ?? '';
const stableTag = /^v\d+\.\d+\.\d+$/;

function fail(message) {
  console.error(`release validation failed: ${message}`);
  process.exit(1);
}

if (!stableTag.test(releaseTag)) {
  fail(`tag must match vX.Y.Z: ${releaseTag}`);
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
try {
  execFileSync('git', ['merge-base', '--is-ancestor', tagCommit, 'refs/remotes/origin/main'], {
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
