import { createHash } from "node:crypto";
import { existsSync, lstatSync, mkdtempSync, readFileSync, readdirSync, readlinkSync, realpathSync, statSync, writeFileSync, mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "bun:test";
import { buildPlan } from "../../../scripts/installer/engine.js";
import { runInstallWizard } from "../../../scripts/installer/terminal.js";

const root = process.cwd();
const ref = "bd1ae10f1db3d38e12166b8c789f0ec9d33253e3";
const skills = {
  "security-audit-coordinator": "491d60e2a70c459adf2a93999347ac8c43dfc4bd764a0894d3335a1d570bbb61",
  "security-implementation": "f0bfed3977e599c3c6edefec373a4d6630b46385367cc5e2d71aaa9035d4c86e",
  "security-review": "03dfd6618116004aefea74f075660a89e724ab99dfbd0c726206ff21594d5508",
  "security-spec": "89282e3cdf4f217d209950f918e1348bc3fe486662c7d00822cef449c16fd8b5",
  "security-threat-model": "fbf78b50ad2e4c6439a32989a9024ba4eabe4596ae96ffba8a3f848a41322f7c",
} as const;

function files(directory: string, base = directory): string[] {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    if ([".git", "node_modules"].includes(entry.name)) return [];
    const path = join(directory, entry.name);
    if (entry.isDirectory()) return files(path, base);
    return entry.isFile() ? [path.slice(base.length + 1).replaceAll("\\", "/")] : [];
  }).sort();
}

function treeHash(directory: string): string {
  const digest = createHash("sha256");
  for (const relative of files(directory)) {
    digest.update(relative);
    digest.update(readFileSync(join(directory, relative)));
  }
  return digest.digest("hex");
}

const feed = (answers: string[], output: string[] = []) => {
  let index = 0;
  return { input: async () => answers[index++], write: (value: string) => output.push(value) };
};

describe("bundled security skill installation", () => {
  it("pins every reviewed tree to exact upstream provenance", () => {
    const lock = JSON.parse(readFileSync(join(root, "skills-lock.json"), "utf8"));
    for (const [name, hash] of Object.entries(skills)) {
      expect(lock.skills[name]).toEqual({
        source: "antoniofulg/security-lifecycle",
        sourceType: "github",
        skillPath: `skills/${name}/SKILL.md`,
        cliVersion: "1.5.23",
        ref,
        computedHash: hash,
      });
      expect(treeHash(join(root, ".agents/skills", name))).toBe(hash);
    }
  });

  it("packages all five trees and removes the network installer", () => {
    const pkg = JSON.parse(readFileSync(join(root, "package.json"), "utf8"));
    for (const name of Object.keys(skills)) {
      expect(pkg.files).toContain(`.agents/skills/${name}`);
      expect(existsSync(join(root, ".agents/skills", name, "SKILL.md"))).toBe(true);
    }
    expect(pkg.files).not.toContain("scripts/install_security_skills.py");
    expect(existsSync(join(root, "scripts/install_security_skills.py"))).toBe(false);
  });

  it("puts every security tree and Claude alias in core", () => {
    const target = mkdtempSync(join(tmpdir(), "security-core-plan-"));
    const result = buildPlan({ sourceRoot: root, targetRoot: target, selectedModules: ["core"] });
    for (const name of Object.keys(skills)) {
      expect(result.staged[`.agents/skills/${name}/SKILL.md`]).toBeDefined();
      expect(result.links[`.claude/skills/${name}`]).toBe(`../../.agents/skills/${name}`);
      expect(result.manifest.files[`.agents/skills/${name}/SKILL.md`]?.layer).toBe("core");
    }
  });

  it("installs exact packaged trees offline and re-runs as a no-op", async () => {
    const target = mkdtempSync(join(tmpdir(), "security-core-install-"));
    const output: string[] = [];
    const first = await runInstallWizard({ sourceRoot: root, targetRoot: target, ...feed(["1", "y", "y"], output) });
    expect(first.code).toBe(0);
    expect(output.join("\n")).not.toContain("install_security_skills.py");
    expect(output.join("\n")).not.toContain("security gate remains uncovered");
    for (const name of Object.keys(skills)) {
      const installed = join(target, ".agents/skills", name);
      const alias = join(target, ".claude/skills", name);
      expect(treeHash(installed)).toBe(treeHash(join(root, ".agents/skills", name)));
      expect(lstatSync(alias).isSymbolicLink()).toBe(true);
      expect(readlinkSync(alias)).toBe(`../../.agents/skills/${name}`);
      expect(realpathSync(alias)).toBe(realpathSync(installed));
      expect(statSync(join(alias, "SKILL.md")).isFile()).toBe(true);
    }
    const before = readFileSync(join(target, ".my-workflow/adoption.json"));
    const secondOutput: string[] = [];
    const second = await runInstallWizard({ sourceRoot: root, targetRoot: target, ...feed(["1", "y"], secondOutput) });
    expect(second.code).toBe(0);
    expect(second.plan.actions).toHaveLength(0);
    expect(secondOutput.join("\n")).toContain("Selected modules are up to date. No files will change.");
    expect(readFileSync(join(target, ".my-workflow/adoption.json"))).toEqual(before);
  });

  it("treats consumer-owned security content as a conflict with zero writes on cancel", async () => {
    const target = mkdtempSync(join(tmpdir(), "security-core-conflict-"));
    const file = join(target, ".agents/skills/security-review/SKILL.md");
    mkdirSync(join(target, ".agents/skills/security-review"), { recursive: true });
    writeFileSync(file, "consumer-owned\n");
    const result = await runInstallWizard({ sourceRoot: root, targetRoot: target, ...feed(["1", "y", "3"]) });
    expect(result.cancelled).toBe(true);
    expect(readFileSync(file, "utf8")).toBe("consumer-owned\n");
    expect(existsSync(join(target, ".my-workflow"))).toBe(false);
  });
});
