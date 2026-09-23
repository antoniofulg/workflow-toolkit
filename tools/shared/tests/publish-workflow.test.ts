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

function git(root: string, ...args: string[]): string {
  return execFileSync("git", args, {
    cwd: root,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  }).trim();
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

function validate(root: string, tag: string) {
  return spawnSync("node", [validatorPath], {
    cwd: root,
    env: { ...process.env, RELEASE_TAG: tag },
    encoding: "utf8",
  });
}

function releaseCanPublish(event: { action: string; release: { prerelease: boolean; tag_name: string } }): boolean {
  return event.action === "published" && !event.release.prerelease && /^v\d+\.\d+\.\d+$/.test(event.release.tag_name);
}

describe("release publication workflow", () => {
  const workflow = read(".github/workflows/publish.yml");

  it("PUB-001 release trigger publishes stable tags and skips prereleases", () => {
    expect(workflow).toContain("release:");
    expect(workflow).toContain("types: [published]");
    expect(workflow).toContain("if: ${{ !github.event.release.prerelease }}");
    expect(workflow).toContain("ref: ${{ github.event.release.tag_name }}");

    expect(releaseCanPublish({ action: "published", release: { prerelease: false, tag_name: "v1.2.3" } })).toBe(true);
    expect(releaseCanPublish({ action: "published", release: { prerelease: true, tag_name: "v1.2.3-rc.1" } })).toBe(false);
    expect(releaseCanPublish({ action: "created", release: { prerelease: false, tag_name: "v1.2.3" } })).toBe(false);
  });

  it("PUB-002 release identity rejects malformed tags, non-main commits, and manifest mismatches", () => {
    expect(workflow.indexOf("Validate release identity")).toBeGreaterThan(-1);
    expect(workflow.indexOf("Validate release identity")).toBeLessThan(workflow.indexOf("Install npm CLI"));
    expect(workflow.indexOf("Validate release identity")).toBeLessThan(workflow.indexOf("bun install --frozen-lockfile"));

    const cases: Array<{ tag: string; name?: string; version?: string; expected: boolean }> = [
      { tag: "v1.2.3", expected: true },
      { tag: "v1.2.3-rc.1", expected: false },
      { tag: "v1.2.3", name: "other-package", expected: false },
      { tag: "v1.2.3", version: "1.2.4", expected: false },
    ];

    for (const testCase of cases) {
      const root = fixture({ name: testCase.name, version: testCase.version });
      try {
        if (testCase.expected && testCase.tag === "v1.2.3") git(root, "tag", testCase.tag);
        else if (testCase.tag === "v1.2.3-rc.1") git(root, "tag", testCase.tag);
        else git(root, "tag", testCase.tag);
        const result = validate(root, testCase.tag);
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
      const result = validate(nonMain, "v1.2.3");
      expect(result.status).not.toBe(0);
      expect(`${result.stdout}${result.stderr}`).toContain("not reachable from main");
    } finally {
      rmSync(nonMain, { recursive: true, force: true });
    }
  });

  it("PUB-003 gate ordering runs frozen install and test:all before publication", () => {
    const install = workflow.indexOf("bun install --frozen-lockfile");
    const gate = workflow.indexOf("bun run test:all");
    const publish = workflow.indexOf("npm publish");

    expect(install).toBeGreaterThan(-1);
    expect(gate).toBeGreaterThan(install);
    expect(publish).toBeGreaterThan(gate);
    expect(workflow).not.toMatch(/continue-on-error:\s*true/);
    expect(workflow).not.toMatch(/if:\s*\$\{\{\s*always\(\)/);
  });

  it("PUB-004 trusted publisher uses provenance and public latest without a static token", () => {
    expect(workflow).toContain("id-token: write");
    expect(workflow).toContain("npm publish --provenance --access public --tag latest --registry=https://registry.npmjs.org");
    expect(workflow).not.toMatch(/\b(?:NPM_TOKEN|NODE_AUTH_TOKEN)\b/);
    expect(workflow).toContain("RELEASE_TAG: ${{ github.event.release.tag_name }}");
  });

  it("PUB-005 publish failure is terminal and does not mutate the GitHub release", () => {
    expect(workflow.match(/\bnpm publish\b/g)).toHaveLength(1);
    expect(workflow).not.toMatch(/continue-on-error|retry|gh\s+(?:release|api)|github-script/i);
  });

  it("PUB-006 publish identity has least privilege and the required runtime metadata", () => {
    const job = workflow.match(/jobs:\n  publish:\n([\s\S]*)/)?.[1] ?? "";
    expect(job).toContain("runs-on: ubuntu-latest");
    expect(job).toMatch(/permissions:\n\s+contents: read\n\s+id-token: write/);
    expect(job).toContain("node-version: 22.14.0");
    expect(job).toContain("npm@11.5.1");

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
