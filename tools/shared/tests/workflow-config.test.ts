import { cpSync, existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, expect, it } from "bun:test";
import { parse } from "smol-toml";
import { readWorkflowConfig, stageAgentPackets, validateWorkflowConfig } from "../../../scripts/installer/packets.js";

const repositoryRoot = process.cwd();
const skillPath = ".agents/skills/wtk-config/SKILL.md";
const roles = ["implementer", "verifier", "explorer", "deep-reviewer", "designer"] as const;
const resolverRoles = ["implementer", "verifier", "explorer", "deep_reviewer", "designer"] as const;
const providers = ["claude", "cursor", "codex"] as const;

function readRepositoryFile(relativePath: string): string {
  return readFileSync(join(repositoryRoot, relativePath), "utf8");
}

function isIgnored(relativePath: string): boolean {
  try {
    execFileSync("git", ["check-ignore", "--no-index", "--quiet", "--", relativePath], {
      cwd: repositoryRoot,
      stdio: "ignore",
    });
    return true;
  } catch {
    return false;
  }
}

function checkoutPorcelain(): string {
  return execFileSync("git", ["status", "--porcelain=v1", "--untracked-files=all"], {
    cwd: repositoryRoot,
    encoding: "utf8",
  });
}

function packagedFiles(): string[] {
  const destination = mkdtempSync(join(tmpdir(), "workflow-package-"));
  const tarball = join(destination, "workflow.tgz");
  const before = checkoutPorcelain();
  try {
    execFileSync("bun", ["pm", "pack", "--filename", tarball, "--ignore-scripts"], {
      cwd: repositoryRoot,
      encoding: "utf8",
    });
    return execFileSync("tar", ["-tzf", tarball], { encoding: "utf8" })
      .trim()
      .split("\n")
      .filter(Boolean)
      .map((path) => path.replace(/^package\//, ""));
  } finally {
    rmSync(destination, { recursive: true, force: true });
    expect(checkoutPorcelain()).toBe(before);
  }
}

describe("workflow configuration skill", () => {
  it("accepts the QA browser adapter contract", () => {
    const accepted = ["auto", "jev", "playwright-mcp", "orca", "maestri", "manual"] as const;
    const validValues = accepted.join(", ");
    const example = parse(readRepositoryFile(".wtk.toml.example")) as Record<string, any>;
    const absent = structuredClone(example);
    delete absent.qa;
    expect(validateWorkflowConfig(absent).qa.browser_adapter).toBe("auto");

    const missingAdapter = structuredClone(example);
    delete missingAdapter.qa.browser_adapter;
    expect(validateWorkflowConfig(missingAdapter).qa.browser_adapter).toBe("auto");

    for (const value of accepted) {
      const config = structuredClone(example);
      config.qa.browser_adapter = value;
      expect(validateWorkflowConfig(config).qa.browser_adapter).toBe(value);
    }

    for (const value of ["jev-ultrafast", "unapproved"]) {
      const config = structuredClone(example);
      config.qa.browser_adapter = value;
      expect(() => validateWorkflowConfig(config)).toThrow(validValues);
    }

    const unknownKey = structuredClone(example);
    unknownKey.qa.credential = "credential-sentinel";
    try {
      validateWorkflowConfig(unknownKey);
      throw new Error("Expected unknown QA key to fail");
    } catch (error) {
      expect(String(error)).toContain(validValues);
      expect(String(error)).not.toContain("credential-sentinel");
    }

    const temporary = mkdtempSync(join(tmpdir(), "wtk-qa-config-"));
    try {
      const withoutQa = readRepositoryFile(".wtk.toml.example").replace(
        /^\[qa\]\nbrowser_adapter = "auto".*\n/m,
        "",
      );
      writeFileSync(join(temporary, ".wtk.toml"), withoutQa);
      expect(readWorkflowConfig(temporary).qa.browser_adapter).toBe("auto");
    } finally {
      rmSync(temporary, { recursive: true, force: true });
    }
  });

  it("documents and preserves the default QA browser adapter", () => {
    const exampleText = readRepositoryFile(".wtk.toml.example");
    expect(exampleText).toContain('[qa]\nbrowser_adapter = "auto"');
    expect(exampleText).toContain("Valid values: auto, jev, playwright-mcp, orca, maestri, manual");

    const temporary = mkdtempSync(join(tmpdir(), "wtk-qa-adoption-"));
    try {
      const withoutQa = exampleText.replace(/^\[qa\]\nbrowser_adapter = "auto".*\n/m, "");
      const configPath = join(temporary, ".wtk.toml");
      writeFileSync(configPath, withoutQa);
      const original = readFileSync(configPath);
      expect(readWorkflowConfig(temporary).qa.browser_adapter).toBe("auto");

      const generated = stageAgentPackets(repositoryRoot, temporary);
      expect(generated[".wtk.toml"]).toBeUndefined();
      expect(readFileSync(configPath)).toEqual(original);
    } finally {
      rmSync(temporary, { recursive: true, force: true });
    }
  });

  it("defines resolution, resume, refresh, and explicit provider failure", () => {
    const skill = readRepositoryFile(skillPath);

    expect(skill).toMatch(/^---\nname: wtk-config\ndescription: .+\n---/);
    expect(skill).toContain("python3 .agents/skills/wtk-config/scripts/workflow_config.py");
    expect(skill).toContain("--refresh");
    expect(skill).toContain("Read the existing feature snapshot before dispatch");
    expect(skill).toMatch(/Halt with the\s+provider and role named/);
    expect(skill).toContain("without merging definitions or silently");
    expect(skill).not.toContain("wtk-deep-review after every slice");
  });

  it("defaults to standard and accepts all upstream Lean profiles", () => {
    const resolver = readRepositoryFile(".agents/skills/wtk-config/scripts/workflow_config.py");
    const lean = readRepositoryFile(".agents/skills/wtk-lean/SKILL.md");
    expect(resolver).toContain('selected = requested or approved or "standard"');
    expect(resolver).toContain('LEAN_PROFILES = ("light", "standard", "ui")');
    expect(lean).toContain("`standard`");
    expect(resolver).toContain("does not match checks.md profile");
  });

  it("keeps modular and integrated artifact contracts distinct", () => {
    const plan = readRepositoryFile(".agents/skills/wtk-plan/SKILL.md");
    const implement = readRepositoryFile(".agents/skills/wtk-implement/SKILL.md");
    const lean = readRepositoryFile(".agents/skills/wtk-lean/SKILL.md");

    const discover = readRepositoryFile(".agents/skills/wtk-discover/SKILL.md");
    expect(discover).toContain(".design/<name>.md");
    expect(plan).toContain(".tasks/<name>.md");
    expect(implement).toContain(".checks/<feature>.md");
    expect(lean.replace(/\s+/g, " ")).toContain(".specs/features/lockfile-v2/plan.md");
    expect(plan).not.toContain(".specs/features/<feature>/plan.md");
    expect(implement).not.toContain(".specs/features/<feature>/plan.md");
  });

  it("identifies a complete agent definition for every supported role and provider", () => {
    for (const provider of providers) {
      for (const role of roles) {
        const extension = provider === "codex" ? "toml" : "md";
const path = `.agents/skills/wtk-config/assets/agents/${provider}/${role}.${extension}`;
        expect(existsSync(join(repositoryRoot, path)), path).toBe(true);
        expect(readRepositoryFile(path).trim(), path).not.toBe("");
      }
    }
  });

  it("keeps local config/runtimes ignored and packages only example/templates", () => {
    expect(execFileSync("git", ["ls-files", "--", ".wtk.toml"], {
      cwd: repositoryRoot,
      encoding: "utf8",
    }).trim()).toBe("");
    expect(execFileSync("git", ["ls-files", "--", ".wtk.toml.example", ".agents/skills/wtk-config/assets/agents"], {
      cwd: repositoryRoot,
      encoding: "utf8",
    })).toContain(".wtk.toml.example");
    for (const relativePath of [
      ".wtk.toml",
      ".claude/agents/planner.md",
      ".codex/agents/planner.toml",
      ".cursor/agents/planner.md",
    ]) {
      expect(isIgnored(relativePath), relativePath).toBe(true);
    }
    const packaged = packagedFiles();
    expect(packaged).toContain(".wtk.toml.example");
    expect(packaged).toContain(".agents/skills/wtk-config/assets/agents/claude/planner.md");
    expect(packaged).toContain(".agents/skills/wtk-config/assets/agents/codex/planner.toml");
    expect(packaged).toContain(".agents/skills/wtk-config/assets/agents/cursor/planner.md");
    expect(packaged).not.toContain(".wtk.toml");
    expect(packaged.some((path) => path.startsWith(".claude/agents/"))).toBe(false);
    expect(packaged.some((path) => path.startsWith(".codex/agents/"))).toBe(false);
    expect(packaged.some((path) => path.startsWith(".cursor/agents/"))).toBe(false);
  }, 30_000);

  it("resolves the shipped mixed profile to its exact provider routes", () => {
    const example = readRepositoryFile(".wtk.toml.example");
    expect(example).toContain(
      "[profiles.mixed]\nimplementer = \"claude\"\nverifier = \"codex\"\nexplorer = \"cursor\"\ndeep_reviewer = \"codex\"",
    );

    const temporaryRoot = mkdtempSync(join(tmpdir(), "workflow-profile-"));
    try {
      cpSync(join(repositoryRoot, ".agents/skills"), join(temporaryRoot, ".agents/skills"), {
        recursive: true,
      });
      cpSync(join(repositoryRoot, ".wtk.toml.example"), join(temporaryRoot, ".wtk.toml.example"));
      execFileSync("git", ["init", "-q"], { cwd: temporaryRoot });
      execFileSync(
        "git",
        ["-c", "user.email=test@example.com", "-c", "user.name=Test", "commit", "--allow-empty", "-qm", "seed"],
        { cwd: temporaryRoot },
      );
      const resolver = join(
        repositoryRoot,
        ".agents/skills/wtk-config/scripts/workflow_config.py",
      );
      execFileSync("python3", [resolver, "--root", temporaryRoot, "--sync-agents"], { encoding: "utf8" });
      const snapshot = JSON.parse(
        execFileSync(
          "python3",
          [
            resolver,
            "--root",
            temporaryRoot,
            "--feature",
            "mixed-profile-contract",
            "--slices",
            "1",
            "--native-provider",
            "cursor",
            "--profile",
            "mixed",
          ],
          { encoding: "utf8" },
        ),
      ) as { roles: Record<string, { provider: string }> };
      expect(snapshot.roles).toMatchObject({
        implementer: { provider: "claude" },
        verifier: { provider: "codex" },
        explorer: { provider: "cursor" },
        deep_reviewer: { provider: "codex" },
      });
    } finally {
      rmSync(temporaryRoot, { recursive: true, force: true });
    }
  }, 30_000);

  it("asserts resolver-returned agent files for every non-native provider route", () => {
    const temporaryRoot = mkdtempSync(join(tmpdir(), "wtk-config-"));
    try {
      cpSync(join(repositoryRoot, ".agents/skills"), join(temporaryRoot, ".agents/skills"), {
        recursive: true,
      });
      cpSync(join(repositoryRoot, ".wtk.toml.example"), join(temporaryRoot, ".wtk.toml.example"));
      execFileSync("git", ["init", "-q"], { cwd: temporaryRoot });
      execFileSync(
        "git",
        [
          "-c",
          "user.email=test@example.com",
          "-c",
          "user.name=Test",
          "commit",
          "--allow-empty",
          "-qm",
          "seed",
        ],
        { cwd: temporaryRoot },
      );

      const resolver = join(
        repositoryRoot,
        ".agents/skills/wtk-config/scripts/workflow_config.py",
      );
      execFileSync("python3", [resolver, "--root", temporaryRoot, "--sync-agents"], {
        encoding: "utf8",
      });
      const agentNames: Record<string, string> = {
        implementer: "implementer",
        verifier: "verifier",
        explorer: "explorer",
        deep_reviewer: "deep-reviewer",
        designer: "designer",
      };
      for (const provider of providers) {
        const nativeProvider = provider === "codex" ? "claude" : "codex";
        for (const role of resolverRoles) {
          const snapshot = JSON.parse(
            execFileSync(
              "python3",
              [
                resolver,
                "--root",
                temporaryRoot,
                "--feature",
                `it003-${provider}-${role.replaceAll("_", "-")}`,
                "--slices",
                "1",
                "--native-provider",
                nativeProvider,
                "--override",
                `${role}=${provider}`,
              ],
              { encoding: "utf8" },
            ),
          ) as { roles: Record<string, { provider: string; agent_file: string }> };
          const route = snapshot.roles[role];
          expect(route.provider).toBe(provider);
          const extension = provider === "codex" ? "toml" : "md";
          const expectedAgentFile = `.${provider}/agents/${agentNames[role]}.${extension}`;
          expect(route.agent_file).toBe(expectedAgentFile);
          expect(existsSync(join(temporaryRoot, route.agent_file))).toBe(true);
        }
      }
    } finally {
      rmSync(temporaryRoot, { recursive: true, force: true });
    }
  }, 30_000);
});
