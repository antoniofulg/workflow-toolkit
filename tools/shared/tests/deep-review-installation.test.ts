import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "bun:test";

const repositoryRoot = process.cwd();
const skillDirectory = join(repositoryRoot, ".agents", "skills", "wtk-deep-review");

function readJson(path: string): unknown {
  return JSON.parse(readFileSync(path, "utf8"));
}

describe("wtk-deep-review installation", { timeout: 30_000 }, () => {
  it("keeps the skill, lock metadata, release version, and project discovery aligned", () => {
    expect(existsSync(join(skillDirectory, "SKILL.md"))).toBe(true);

    const lock = readJson(join(repositoryRoot, "skills-lock.json")) as {
      skills?: Record<string, unknown>;
    };
    const lockEntry = lock.skills?.["wtk-deep-review"] as
      | { source?: string; sourceType?: string; skillPath?: string }
      | undefined;
    expect(lockEntry).toEqual({
      source: "./local",
      sourceType: "local",
      skillPath: ".agents/skills/wtk-deep-review/SKILL.md",
    });

    const packageManifest = readJson(join(repositoryRoot, "package.json")) as {
      version?: string;
      packageManager?: string;
      devDependencies?: Record<string, string>;
    };
    expect(packageManifest.version).toMatch(/^\d+\.\d+\.\d+$/);
    expect(packageManifest.packageManager).toBe("bun@1.4.0");
    expect(existsSync(join(repositoryRoot, "bun.lock"))).toBe(true);
    expect(existsSync(join(repositoryRoot, "package-lock.json"))).toBe(false);
    expect(packageManifest.devDependencies?.skills).toBe("1.5.23");
    expect(
      (readJson(join(repositoryRoot, "node_modules", "skills", "package.json")) as {
        version?: string;
      }).version,
    ).toBe("1.5.23");

    const discovered = JSON.parse(
      execFileSync(join(repositoryRoot, "node_modules", ".bin", "skills"), ["list", "--json"], {
        cwd: repositoryRoot,
        encoding: "utf8",
      }),
    ) as Array<Record<string, unknown>>;
    expect(discovered.find((skill) => skill.name === "wtk-deep-review")).toMatchObject({
      name: "wtk-deep-review",
      path: skillDirectory,
      scope: "project",
      agents: expect.any(Array),
      sourceType: "local",
    });
  });
});
