import { execFileSync, spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "bun:test";

const repositoryRoot = process.cwd();
const validatorPath = join(repositoryRoot, "scripts/validate-release.mjs");

function read(relativePath: string): string {
  return readFileSync(join(repositoryRoot, relativePath), "utf8");
}

function jobBlock(source: string, name: string): string {
  const start = source.indexOf(`  ${name}:\n`);
  if (start === -1) return "";
  const nextJob = source.slice(start + 1).search(/\n  [a-z][\w-]*:\n/);
  return source.slice(start, nextJob === -1 ? undefined : start + 1 + nextJob);
}

function git(root: string, ...args: string[]): string {
  return execFileSync("git", args, {
    cwd: root,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  }).trim();
}

function stepBlock(source: string, name: string): string {
  const start = source.indexOf(`- name: ${name}`);
  const end = source.indexOf("\n      - name:", start + 1);
  return start === -1 ? "" : source.slice(start, end === -1 ? undefined : end);
}

function fixture({ name = "workflow-toolkit", version = "1.2.3" } = {}) {
  const root = mkdtempSync(join(tmpdir(), "publish-workflow-"));
  git(root, "init", "--initial-branch=main");
  git(root, "config", "user.email", "tests@example.invalid");
  git(root, "config", "user.name", "Workflow tests");
  writeFileSync(join(root, "package.json"), JSON.stringify({ name, version }) + "\n");
  git(root, "add", "package.json");
  git(root, "commit", "-m", "fixture");
  git(root, "update-ref", "refs/remotes/origin/main", "HEAD");
  return root;
}

function validate(root: string, tag: string, sha: string) {
  return spawnSync("node", [validatorPath], {
    cwd: root,
    env: { ...process.env, RELEASE_TAG: tag, RELEASE_SHA: sha },
    encoding: "utf8",
  });
}

function releaseCanPublish(event: { action: string; release: { prerelease: boolean; tag_name: string } }): boolean {
  return event.action === "published" && !event.release.prerelease && /^v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)$/.test(event.release.tag_name);
}

describe("release publication workflow", () => {
  const workflow = read(".github/workflows/publish.yml");
  const testJob = jobBlock(workflow, "test");
  const publishJob = jobBlock(workflow, "publish");

  it("PUB-001 release trigger publishes stable tags and skips prereleases", () => {
    expect(workflow).toContain("release:");
    expect(workflow).toContain("types: [published]");
    expect(workflow).toContain("if: ${{ !github.event.release.prerelease }}");
    expect(workflow).toContain("RELEASE_SHA: ${{ github.sha }}");
    expect(workflow).toContain("ref: ${{ github.sha }}");
    expect(testJob).toContain("ref: ${{ github.sha }}");
    expect(publishJob).toContain("ref: ${{ github.sha }}");
    expect(publishJob).toContain("needs: test");

    expect(releaseCanPublish({ action: "published", release: { prerelease: false, tag_name: "v1.2.3" } })).toBe(true);
    expect(releaseCanPublish({ action: "published", release: { prerelease: true, tag_name: "v1.2.3-rc.1" } })).toBe(false);
    expect(releaseCanPublish({ action: "created", release: { prerelease: false, tag_name: "v1.2.3" } })).toBe(false);
  });

  it("PUB-002 release identity rejects malformed tags, non-main commits, and manifest mismatches", () => {
    expect(testJob.indexOf("Validate release identity")).toBeGreaterThan(-1);
    expect(testJob.indexOf("Validate release identity")).toBeLessThan(testJob.indexOf("Install npm CLI"));
    expect(testJob.indexOf("Validate release identity")).toBeLessThan(testJob.indexOf("bun install --frozen-lockfile"));
    expect(publishJob).not.toContain("Validate release identity");
    expect(publishJob.indexOf("Download tested package")).toBeGreaterThan(-1);
    expect(testJob).toContain("RELEASE_TAG: ${{ github.event.release.tag_name }}");
    expect(publishJob).toContain("RELEASE_TAG: ${{ github.event.release.tag_name }}");

    const cases: Array<{ tag: string; name?: string; version?: string; expected: boolean }> = [
      { tag: "v1.2.3", expected: true },
      { tag: "v1.2.3-rc.1", expected: false },
      { tag: "v1.2.3", name: "other-package", expected: false },
      { tag: "v1.2.3", version: "1.2.4", expected: false },
    ];

    for (const testCase of cases) {
      const root = fixture({ name: testCase.name, version: testCase.version });
      try {
        git(root, "tag", testCase.tag);
        const result = validate(root, testCase.tag, git(root, "rev-parse", "HEAD"));
        expect(result.status === 0).toBe(testCase.expected);
      } finally {
        rmSync(root, { recursive: true, force: true });
      }
    }

    const nonMain = fixture();
    try {
      git(nonMain, "checkout", "-b", "release-only");
      writeFileSync(join(nonMain, "release-marker.txt"), "release-only\n");
      git(nonMain, "add", "release-marker.txt");
      git(nonMain, "commit", "-m", "release outside main");
      git(nonMain, "tag", "v1.2.3");
      const result = validate(nonMain, "v1.2.3", git(nonMain, "rev-parse", "HEAD"));
      expect(result.status).not.toBe(0);
      expect(`${result.stdout}${result.stderr}`).toContain("not reachable from main");
    } finally {
      rmSync(nonMain, { recursive: true, force: true });
    }

    const movedTag = fixture();
    try {
      const eventSha = git(movedTag, "rev-parse", "HEAD");
      git(movedTag, "tag", "v1.2.3");
      writeFileSync(join(movedTag, "release-marker.txt"), "moved-tag\n");
      git(movedTag, "add", "release-marker.txt");
      git(movedTag, "commit", "-m", "move tag target");
      git(movedTag, "update-ref", "refs/remotes/origin/main", "HEAD");
      git(movedTag, "tag", "--force", "v1.2.3");
      git(movedTag, "checkout", "--detach", eventSha);
      const result = validate(movedTag, "v1.2.3", eventSha);
      expect(result.status).not.toBe(0);
      expect(`${result.stdout}${result.stderr}`).toContain("does not match event commit");
    } finally {
      rmSync(movedTag, { recursive: true, force: true });
    }

    const deletedTag = fixture();
    try {
      const eventSha = git(deletedTag, "rev-parse", "HEAD");
      git(deletedTag, "tag", "v1.2.3");
      git(deletedTag, "tag", "--delete", "v1.2.3");
      const result = validate(deletedTag, "v1.2.3", eventSha);
      expect(result.status).not.toBe(0);
    } finally {
      rmSync(deletedTag, { recursive: true, force: true });
    }

    const mismatchedHead = fixture();
    try {
      git(mismatchedHead, "tag", "v1.2.3");
      const result = validate(mismatchedHead, "v1.2.3", "0".repeat(40));
      expect(result.status).not.toBe(0);
      expect(`${result.stdout}${result.stderr}`).toContain("does not match event commit");
    } finally {
      rmSync(mismatchedHead, { recursive: true, force: true });
    }
  });

  it("PUB-003 gate ordering runs frozen install and test:all before publication", () => {
    const install = testJob.indexOf("bun install --frozen-lockfile");
    const gate = testJob.indexOf("bun run test:all");
    const packageArchive = testJob.indexOf("npm pack --ignore-scripts");

    expect(install).toBeGreaterThan(-1);
    expect(gate).toBeGreaterThan(install);
    expect(packageArchive).toBeGreaterThan(gate);
    expect(publishJob).toContain("needs: test");
    expect(publishJob).toContain("Verify tested package");
    expect(publishJob).not.toMatch(/\bbun[ \t]+(?:install|run)\b/);
    expect(publishJob).not.toMatch(/\bnpm[ \t]+(?:ci|run|test|pack)\b/);
    expect(publishJob).not.toMatch(/\bnpm[ \t]+install(?![ \t]+--global[ \t]+npm@11\.5\.1\b)/);
    const gateStep = stepBlock(testJob, "Run the full test gate");
    expect(gateStep).toMatch(/^\s+run: bun run test:all$/m);
    expect(gateStep).not.toMatch(/continue-on-error|always\(\)|\|\|/);
  });

  it("PUB-004 trusted publisher uses provenance and public latest without a static token", () => {
    const verifyIndex = publishJob.indexOf("- name: Verify tested package");
    const publishIndex = publishJob.indexOf("- name: Publish tested archive to npm");
    const checksumComparison = 'test "$actual" = "$EXPECTED_PACKAGE_SHA256"';
    const artifactChecksumComparison = 'test "$(awk \'{print $1}\' "$RUNNER_TEMP/release-package/workflow-toolkit.tgz.sha256")" = "$actual"';
    const archiveManifest = 'tar -xOf "$archive" package/package.json | node --input-type=module -e';

    expect(verifyIndex).toBeGreaterThan(-1);
    expect(publishIndex).toBeGreaterThan(verifyIndex);
    expect(publishJob.indexOf(checksumComparison)).toBeGreaterThan(verifyIndex);
    expect(publishJob.indexOf(artifactChecksumComparison)).toBeGreaterThan(publishJob.indexOf(checksumComparison));
    expect(publishJob.indexOf(archiveManifest)).toBeGreaterThan(publishJob.indexOf(artifactChecksumComparison));
    expect(publishIndex).toBeGreaterThan(publishJob.indexOf(archiveManifest));
    expect(publishJob).not.toContain("scripts/validate-release.mjs");
    expect(publishJob.slice(0, verifyIndex)).not.toMatch(/\b(?:node|bun)[ \t]+(?:scripts\/|\.\/)/);
    expect(testJob).not.toContain("id-token: write");
    expect(publishJob).toContain("id-token: write");
    expect(publishJob).toContain("EXPECTED_PACKAGE_SHA256");
    expect(publishJob).toContain("workflow-toolkit.tgz");
    expect(publishJob).toContain("--ignore-scripts --provenance --access public --tag latest --registry=https://registry.npmjs.org");
    expect(workflow).not.toMatch(/\b(?:NPM_TOKEN|NODE_AUTH_TOKEN)\b/);
  });

  it("PUB-005 publish failure is terminal and does not mutate the GitHub release", () => {
    const publishStep = stepBlock(publishJob, "Publish tested archive to npm");
    expect(publishStep).toMatch(/^\s+run: npm publish "\$RUNNER_TEMP\/release-package\/workflow-toolkit\.tgz" --ignore-scripts --provenance --access public --tag latest --registry=https:\/\/registry\.npmjs\.org$/m);
    expect(publishStep).not.toMatch(/continue-on-error|retry|for\s+attempt|while\s|until\s|gh\s+(?:release|api)|github-script/i);
  });

  it("PUB-006 publish identity has least privilege and the required runtime metadata", () => {
    expect(testJob).toContain("runs-on: ubuntu-latest");
    expect(publishJob).toContain("runs-on: ubuntu-latest");
    const testPermissions = testJob.match(/    permissions:\n((?:      [^\n]+\n)+)/)?.[1] ?? "";
    const publishPermissions = publishJob.match(/    permissions:\n((?:      [^\n]+\n)+)/)?.[1] ?? "";
    expect(testPermissions).toBe("      contents: read\n");
    expect(publishPermissions).toBe("      contents: read\n      id-token: write\n");
    expect(testJob).toContain("node-version: 22.14.0");
    expect(publishJob).toContain("node-version: 22.14.0");
    expect(testJob).toContain("npm@11.5.1");
    expect(publishJob).toContain("npm@11.5.1");

    const manifest = JSON.parse(read("package.json")) as { repository?: { type?: string; url?: string } };
    expect(manifest.repository).toEqual({
      type: "git",
      url: "https://github.com/antoniofulg/workflow-toolkit",
    });
  });

  it("PUB-007 maintainer setup documents the trusted publisher and release trigger", () => {
    const readme = read("README.md");
    expect(readme).toContain("GitHub release");
    expect(readme).toContain(".github/workflows/publish.yml");
    expect(readme).toContain("antoniofulg");
    expect(readme).toContain("workflow-toolkit");
    expect(readme).toContain("publish.yml");
    expect(readme).toContain("direct publish");
    expect(readme).toContain("trusted publisher");
  });
});
