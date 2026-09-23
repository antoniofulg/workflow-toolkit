import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { describe, expect, it } from "bun:test";

const repositoryRoot = process.cwd();

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

function tracked(relativePath: string): string {
  return execFileSync("git", ["ls-files", "--", relativePath], {
    cwd: repositoryRoot,
    encoding: "utf8",
  }).trim();
}

function parseSkillMetadata(source: string, relativePath: string): { name: string; description: string } {
  const frontmatter = source.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1];
  const name = frontmatter?.match(/^name:\s*(.+)$/m)?.[1]?.trim();
  const description = frontmatter?.match(/^description:\s*(.+)$/m)?.[1]?.trim();

  if (!name || !description) {
    throw new Error(`Missing valid initial frontmatter in ${relativePath}`);
  }

  return { name, description };
}

function skillMetadata(relativePath: string): { name: string; description: string } {
  return parseSkillMetadata(readRepositoryFile(relativePath), relativePath);
}

function normalizePacket(source: string): string {
  return source.replaceAll("`", "").replace(/\s+/g, " ").trim();
}

function runBunVersionSensor(versionSource: string, replacement: string): void {
  const root = mkdtempSync(join(tmpdir(), "bun-version-sensor-"));
  const preload = join(root, "preload.ts");
  const marker = join(root, "marker.txt");
  const suite = join(root, "marker.test.ts");

  try {
    writeFileSync(preload, versionSource.replace("Bun.version", replacement), "utf8");
    writeFileSync(
      suite,
      `import { writeFileSync } from "node:fs";\nwriteFileSync(${JSON.stringify(marker)}, "ran");\n`,
      "utf8",
    );

    const result = spawnSync(process.execPath, ["test", "--preload", preload, suite], {
      cwd: root,
      encoding: "utf8",
    });

    expect(result.status).not.toBe(0);
    expect(existsSync(marker)).toBe(false);
    expect(`${result.stdout}${result.stderr}`).toContain("Bun 1.4.x is required");
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

const activeAuthorityRoots = [
  "AGENTS.md",
  "README.md",
  "docs/adoption-prompt.md",
  "docs/toolkit/guidelines",
  "docs/qa",
  "docs/toolkit",
  "knowledge",
  "package.json",
  "bunfig.toml",
  "scripts",
  "tools",
  ".agents/skills",
".agents/skills/wtk-config/assets/agents",
] as const;

const historicalAuthorityAllowlist = [
  /^CHANGELOG\.md$/,
  /^\.specs\//,
  /^knowledge\/raw\//,
  /^docs\/qa\/(?:evidence|reports|charters|bugs)\//,
  /^docs\/qa\/journeys\//,
  /^docs\/qa\/scenarios\/(?!REL-report-current-workflow-release\.md$)/,
] as const;

// Scenarios are exempt from the command-authority scan but stay editable: QA-SCENARIOS.md
// requires resetting an affected scenario to `untested`, so they are never frozen history.
const frozenQaRoots = [
  "docs/qa/evidence",
  "docs/qa/reports",
  "docs/qa/charters",
  "docs/qa/bugs",
] as const;

function trackedRepositoryPaths(): string[] {
  return execFileSync("git", ["ls-files"], {
    cwd: repositoryRoot,
    encoding: "utf8",
  })
    .trim()
    .split("\n")
    .filter(Boolean);
}

function isUnderRoot(relativePath: string, root: string): boolean {
  return relativePath === root || relativePath.startsWith(`${root}/`);
}

function isHistoricalAuthority(relativePath: string): boolean {
  return historicalAuthorityAllowlist.some((pattern) => pattern.test(relativePath));
}

function isFrozenQaArtifact(relativePath: string): boolean {
  return frozenQaRoots.some((root) => isUnderRoot(relativePath, root));
}

function isTestSource(relativePath: string): boolean {
  return /(?:^|\/)(?:test_[^/]*\.py|[^/]*\.test\.ts)$/.test(relativePath);
}

type RepositoryReader = (relativePath: string) => string;

function activeAuthorityPaths(paths: string[]): string[] {
  return paths.filter(
    (relativePath) =>
      existsSync(join(repositoryRoot, relativePath)) &&
      activeAuthorityRoots.some((root) => isUnderRoot(relativePath, root)) &&
      !isHistoricalAuthority(relativePath) &&
      !isTestSource(relativePath),
  );
}

function forbiddenAuthorityViolations(
  paths: string[],
  read: RepositoryReader = readRepositoryFile,
): string[] {
  const scannedPaths = activeAuthorityPaths(paths);
  const forbiddenCommands = [
    /(?:^|[`$>#;&|]\s*)npm\s+(?!(?:pack\s+--pack-destination\s+\S+(?:\s*#.*)?$|install\s+--save-dev\s+--save-exact\s+@nanonets\/graft@0\.10\.1$|exec\s+--yes\s+--package\s+\S+\s+--\s+my-workflow\s+(?:plan|apply|resolve|status)\b))\S+/i,
    /(?:^|[`$>#;&|]\s*)npx\s+(?!(?:skills\s+(?:add|list|update)\b|workflow-toolkit\s+install|wtk\s+install|scripts\s+install|--yes\s+<approved-package>@<exact-version>(?:\s+(?:plan|apply|resolve|status)\b|(?=\s*`|$))))\S+/i,
    /\bvitest\s+(?:run|--|[A-Za-z])/i,
    /\btsx\s+(?:--|[A-Za-z])/i,
    /(?:from|require)\s*[(]?['"]yaml['"]/i,
  ];
  return scannedPaths.flatMap((relativePath) => {
    const lines = read(relativePath).replace(/\\\r?\n\s*/g, " ").split(/\r?\n/);
    return lines.flatMap((line, index) =>
      forbiddenCommands.some((pattern) => pattern.test(line))
        ? [`${relativePath}:${index + 1}: ${line.trim()}`]
        : [],
    );
  });
}

function documentedBunScripts(
  paths: string[],
  read: RepositoryReader = readRepositoryFile,
): string[] {
  const scripts = new Set<string>();
  for (const relativePath of activeAuthorityPaths(paths)) {
    for (const match of read(relativePath).matchAll(/\bbun run ([A-Za-z0-9][A-Za-z0-9:_-]*)\b/g)) {
      scripts.add(match[1]);
    }
  }
  return [...scripts].sort();
}

const historicalQaBaseline = "b3b42c7bd0a8ab8e72d4c5367f4559df31f8d647";

function changedHistoricalQaArtifacts(
  root = repositoryRoot,
  sourceRef = historicalQaBaseline,
): string[] {
  const gitOptions = { cwd: root, encoding: "utf8" as const };
  const baselinePaths = new Set(
    execFileSync(
      "git",
      ["ls-tree", "-r", "--name-only", sourceRef, "--", ...frozenQaRoots],
      gitOptions,
    )
      .trim()
      .split(/\r?\n/)
      .filter(Boolean),
  );
  const committed = execFileSync(
    "git",
    ["diff", "--name-only", `${sourceRef}...HEAD`, "--", ...frozenQaRoots],
    gitOptions,
  );
  const working = execFileSync(
    "git",
    ["diff", "--name-only", "HEAD", "--", ...frozenQaRoots],
    gitOptions,
  );
  const staged = execFileSync(
    "git",
    ["diff", "--cached", "--name-only", "--", ...frozenQaRoots],
    gitOptions,
  );
  return [...new Set(`${committed}${working}${staged}`.split(/\r?\n/).filter(Boolean))]
    .filter(isFrozenQaArtifact)
    .filter((relativePath) => baselinePaths.has(relativePath))
    .sort();
}

function commitFixture(root: string, message: string): string {
  execFileSync("git", ["add", "--", "."], { cwd: root, stdio: "ignore" });
  execFileSync(
    "git",
    [
      "-c",
      "user.name=QA fixture",
      "-c",
      "user.email=qa-fixture@example.invalid",
      "commit",
      "--quiet",
      "-m",
      message,
    ],
    { cwd: root, stdio: "ignore" },
  );
  return execFileSync("git", ["rev-parse", "HEAD"], {
    cwd: root,
    encoding: "utf8",
  }).trim();
}

const verifierPacketPaths = [
".agents/skills/wtk-config/assets/agents/cursor/verifier.md",
".agents/skills/wtk-config/assets/agents/claude/verifier.md",
".agents/skills/wtk-config/assets/agents/codex/verifier.toml",
] as const;

describe("QA workflow artifact policy", () => {
  it("IT-025 routes behavior-preserving UI corrections by intent and evidence", () => {
    const gates = readRepositoryFile(".agents/skills/wtk/references/validation.md");
    const qaExecution = readRepositoryFile(".agents/skills/wtk-qa-execute/references/qa-execution.md");
    const scenarios = readRepositoryFile(".agents/skills/wtk-qa/references/qa-scenarios.md");
    const review = readRepositoryFile(".agents/skills/wtk/references/review-rounds.md");
    const implement = readRepositoryFile(".agents/skills/wtk-implement/SKILL.md");
    const tasks = readRepositoryFile(".agents/skills/wtk-plan/SKILL.md");
    const checklist = readRepositoryFile(".agents/skills/wtk-implement/references/checklist-format.md");
    expect(gates).toContain("not promoted to full e2e");
    expect(qaExecution).toContain("receives no QA Plan/Execute cycle");
    expect(scenarios).toContain("does not create/reset a scenario or start a QA");
    expect(review).toContain("issue` is neutral");
    expect(implement).toContain("Every check names its **proof**");
    expect(implement).not.toContain("Build + lint + all tests");
    expect(tasks).toContain("observable criteria with concrete values");
    expect(checklist).toContain("one** observable claim");
    expect(checklist).toContain("Proof:");
    expect(checklist).not.toContain("[full gate command");
  });

  it("IT-007 ignores generated Deep Review output but keeps learnings eligible", () => {
    const gitignore = readRepositoryFile(".gitignore");

    expect(gitignore).toContain(".wtk-deep-review/*");
    expect(gitignore).toContain("!.wtk-deep-review/learnings.md");
    expect(isIgnored(".wtk-deep-review/findings.md")).toBe(true);
    expect(isIgnored(".wtk-deep-review/qa-skills-t1/agents/cohort-c01.json")).toBe(true);
    expect(isIgnored(".wtk-deep-review/learnings.md")).toBe(false);
  });

  it("IT-014 keeps feature workflow state versioned and documents legacy migration", () => {
    const readme = readRepositoryFile("README.md");
    const artifactLifecycle = readRepositoryFile(".agents/skills/wtk/references/artifacts.md");

    expect(isIgnored(".specs/features/qa-skills/spec.md")).toBe(false);
    expect(isIgnored(".specs/STATE.md")).toBe(false);
    expect(isIgnored(".specs/AD-INDEX.md")).toBe(false);
    expect(tracked(".specs/STATE.md")).toBe(".specs/STATE.md");
    expect(tracked(".specs/AD-INDEX.md")).toBe(".specs/AD-INDEX.md");
    expect(readme.replace(/\s+/g, " ")).toContain(
      "Feature workflow state follows the [artifact lifecycle]",
    );
    const lifecycle = artifactLifecycle.replace(/\s+/g, " ");
    expect(lifecycle).toContain("`.specs/features/` is transient Lean workflow state");
    expect(lifecycle).toContain("exact legacy managed `.specs/features/` ignore line");
    expect(readme).toContain("never stages or commits files");
  });

  it("IT-015 treats Lean proof state as the commit precondition", () => {
    const agents = readRepositoryFile("AGENTS.md");
    const loop = readRepositoryFile("docs/toolkit/loop.md");
    const lean = readRepositoryFile(".agents/skills/wtk-lean/SKILL.md");
    const implementer = readRepositoryFile(".agents/skills/wtk-implement/SKILL.md");
    const memory = readRepositoryFile(".agents/skills/wtk-lean/references/memory.md");
    const providerPackets = [
      readRepositoryFile(".agents/skills/wtk-config/assets/agents/cursor/implementer.md"),
      readRepositoryFile(".agents/skills/wtk-config/assets/agents/claude/implementer.md"),
      readRepositoryFile(".agents/skills/wtk-config/assets/agents/codex/implementer.toml"),
    ];

    expect(agents).toContain("Feature -> Slice -> Check");
    expect(loop).toContain("checks.md");
    expect(lean).toContain("checks.md");
    expect(lean).toContain("verification.md");
    expect(memory).toContain("checks.md");
    expect(implementer).toContain("Every check names its **proof**");
    for (const packet of providerPackets) {
      expect(packet).toContain("checks.md");
      expect(packet).toContain("current Lean check traceability");
      expect(packet).toContain("wtk-implement");
      expect(packet).toMatch(/select\s+`?wtk-lean/i);
    }
  });

});

describe("canonical QA skills", () => {
  const qaPlanPath = ".agents/skills/wtk-qa-plan/SKILL.md";
  const qaExecutePath = ".agents/skills/wtk-qa-execute/SKILL.md";

  it("UT-001 installs one attributed slice-native workflow authority", () => {
    const skill = readRepositoryFile(".agents/skills/wtk/SKILL.md");
    const notice = readRepositoryFile(".agents/skills/wtk-lean/NOTICE.md");
    const validator = readRepositoryFile(".agents/skills/wtk-lean/SKILL.md");
    const tasksReference = [
      readRepositoryFile(".agents/skills/wtk-plan/SKILL.md"),
      readRepositoryFile(".agents/skills/wtk-plan/references/document-format.md"),
    ].join("\n");
    const activeContract = [
      skill,
      notice,
      readRepositoryFile(".agents/skills/wtk-lean/references/build.md"),
      tasksReference,
      readRepositoryFile(".agents/skills/wtk-implement/SKILL.md"),
    ].join("\n");

    expect(skillMetadata(".agents/skills/wtk/SKILL.md").name).toBe("wtk");
    expect(existsSync(join(repositoryRoot, ".agents/skills/tlc-spec-driven"))).toBe(false);
    expect(notice).toContain("Felipe Rodrigues");
    expect(notice).toContain("CC BY 4.0");
    expect(notice).toContain(
      "https://github.com/tech-leads-club/agent-skills/tree/main/packages/skills-catalog/skills/(development)/tlc-spec-lean",
    );
    expect(activeContract).not.toMatch(/phase[- ]batch|Batch complete|opt[- ]in/i);
    expect(activeContract).not.toMatch(/after the last task of the feature/i);
    expect(tasksReference).toContain("one task for the whole source");
    expect(tasksReference).not.toMatch(
      /task-budgeted dispatch|whole phases|phases? (?:run|are ordered|complete) in sequence|phase boundaries/i,
    );
    expect(activeContract).toContain("whole slices");
    expect(activeContract).toContain("fresh Verifier");
    expect(validator).toContain("one fresh Verifier over `<feature base>..HEAD`");
    expect(validator).toContain("whole slices");
    expect(validator).not.toContain("After all tasks for a feature (or priority group) are done");
  });

  it("IT-001 exposes model-invoked skills with matching names", () => {
    for (const [relativePath, expectedName, inspirationUrl] of [
      [qaPlanPath, "wtk-qa-plan", "https://github.com/pedronauck/skills/tree/main/skills/mine/qa-report"],
      [qaExecutePath, "wtk-qa-execute", "https://github.com/pedronauck/skills/tree/main/skills/mine/qa-execution"],
    ] as const) {
      const source = readRepositoryFile(relativePath);
      const metadata = skillMetadata(relativePath);

      expect(metadata.name).toBe(expectedName);
      expect(source).toContain("metadata:");
      expect(source).toContain("author: Antonio Fulgêncio");
      expect(source).toContain("## Provenance");
      expect(source).toContain("Pedro Nauck");
      expect(source).toContain("original project-owned adaptation");
      expect(source).toContain(inspirationUrl);
      expect(source).not.toMatch(/\b(?:copied verbatim|literal copy|copied literally)\b/i);
      expect(source).not.toContain("disable-model-invocation");
      expect(source).toContain("Use when");
      expect(source).toContain("Don't use for");
    }
  });

  it("IT-022 keeps companion skills optional", () => {
    for (const name of ["ponytail", "prompt-review", "security-review"] as const) {
      expect(existsSync(join(repositoryRoot, ".agents/skills", name))).toBe(false);
    }
    const readme = readRepositoryFile("README.md");
    expect(readme).toContain("dietrichgebert/ponytail");
    expect(readme).toContain("antoniofulg/security-lifecycle");
  });

  it("IT-002 keeps QA routes, references, and non-author boundaries intact", () => {
    const qaPlan = normalizePacket(readRepositoryFile(qaPlanPath));
    const qaExecute = normalizePacket(readRepositoryFile(qaExecutePath));

    for (const [source, references] of [
      [qaPlan, ["docs/qa/journeys/", "docs/qa/scenarios/", "docs/qa/charters/", "wtk-qa-execute"]],
      [qaExecute, ["docs/qa/reports/", "docs/qa/bugs/", "references/fix-loop.md", "references/session-protocol.md"]],
    ] as const) {
      for (const reference of references) expect(source).toContain(reference);
      expect(source).toContain("qa-scenarios.md");
    }
    for (const reference of ["fix-loop.md", "session-protocol.md"]) {
      expect(existsSync(join(repositoryRoot, ".agents/skills/wtk-qa-execute/references", reference))).toBe(true);
    }
    // Semantic boundaries tolerate wrapping; prose style and probe counts are not contracts.
    expect(qaPlan).toMatch(/standalone planning request stops/i);
    expect(qaPlan).toMatch(/Neither phase changes product code/);
    expect(qaExecute).toMatch(/does not write product code, install a framework, invent a command, or replace the automated gate/);
    expect(qaExecute).toMatch(/Stop unsafe or dependent paths/);
    expect(qaExecute).toMatch(/independent paths on the same frozen snapshot/);
    expect(qaExecute).toMatch(/same non-author Verifier may resume/);
    expect(qaExecute).toMatch(/identifying the new snapshot and resetting the environment/);
  });

  it("IT-023 keeps Jev as a driver and the oracle independent", () => {
    const qaExecute = normalizePacket(readRepositoryFile(qaExecutePath));
    const session = normalizePacket(readRepositoryFile(".agents/skills/wtk-qa-execute/references/session-protocol.md"));

    expect(qaExecute).toContain("jev_adapter.py");
    expect(qaExecute).toContain("completed/DONE result is driver evidence only");
    expect(qaExecute).toContain("never a QA pass");
    expect(qaExecute).toContain("independent read path and reload");
    expect(qaExecute).toContain("does not provide a Playwright MCP, Orca Browser, or Maestri Portal bridge");
    expect(session).toContain("independent read path and after a reload");
  });

  it("IT-027 routes the configured QA browser adapter", () => {
    const qaExecute = normalizePacket(readRepositoryFile(qaExecutePath));
    const workflowConfig = readRepositoryFile(".agents/skills/wtk-config/scripts/workflow_config.py");
    const installerConfig = readRepositoryFile(".agents/skills/wtk-config/scripts/packets.js");
    const jevAdapter = readRepositoryFile(".agents/skills/wtk-qa-execute/jev_adapter.py");

    expect(qaExecute).toContain("[qa].browser_adapter");
    for (const value of ["auto", "jev", "playwright-mcp", "orca", "maestri", "manual"]) {
      expect(qaExecute).toContain(value);
    }
    expect(qaExecute).toMatch(/auto tries Jev first/);
    expect(qaExecute).toContain("then LLM + Playwright MCP");
    expect(qaExecute).toContain("exactly one IDE-native Orca or Maestri adapter");
    expect(qaExecute).toContain("Orca before Maestri");
    expect(qaExecute).toContain("A direct value selects only that adapter");
    expect(qaExecute).toContain("jev-ultrafast is not a public alias");
    expect(workflowConfig).toContain('QA_BROWSER_ADAPTERS = ("auto", "jev", "playwright-mcp", "orca", "maestri", "manual")');
    expect(installerConfig).toContain("const QA_BROWSER_ADAPTERS = ['auto', 'jev', 'playwright-mcp', 'orca', 'maestri', 'manual']");
    expect(jevAdapter).toContain("from jev_ultrafast import Agent");
  });

  it("IT-028 forbids unsafe Jev replay", () => {
    const qaExecute = normalizePacket(readRepositoryFile(qaExecutePath));
    const jevAdapter = normalizePacket(readRepositoryFile(".agents/skills/wtk-qa-execute/jev_adapter.py"));

    expect(qaExecute).toContain("pre-action-timeout");
    expect(qaExecute).toContain("fallback_safe: true");
    expect(qaExecute).toContain("fallback_safe: false");
    expect(qaExecute).toContain("fallback_adapter");
    expect(qaExecute).toContain("Once Agent.run() starts, a timeout is unsafe to replay");
    expect(qaExecute).toContain("stop and inspect or reset the fixture before another driver acts");
    expect(jevAdapter).toContain("pre-action-timeout");
    expect(jevAdapter).toContain("post-action-timeout");
    expect(jevAdapter).toContain("ambiguous-timeout");
    expect(qaExecute).toContain("omits raw exception text");
  });

  it("IT-024 packages the optional Jev QA adapter without owning installation", () => {
    const packageJson = JSON.parse(readRepositoryFile("package.json")) as { files: string[]; dependencies?: Record<string, string> };
    const qaExecute = normalizePacket(readRepositoryFile(qaExecutePath));
    const helper = ".agents/skills/wtk-qa-execute/jev_adapter.py";

    expect(existsSync(join(repositoryRoot, helper))).toBe(true);
    expect(packageJson.files).toContain(".agents/skills/wtk-qa-execute");
    expect(qaExecute).toContain("installs neither Jev Ultrafast nor Browser Harness");
    expect(qaExecute).toContain("non-consequential fixture journey");
    expect(qaExecute).toContain("exactly one IDE-native Orca or Maestri adapter");
    expect(qaExecute).toContain("dedicated CDP endpoint");
    expect(Object.keys(packageJson.dependencies ?? {})).not.toContain("jev-ultrafast");
    expect(Object.keys(packageJson.dependencies ?? {})).not.toContain("browser-harness");
  });

  it("routes execution receipts and delivery reporting to one bundled metrics reference", () => {
    const reference = ".agents/skills/wtk/references/execution-metrics.md";
    expect(existsSync(join(repositoryRoot, reference))).toBe(true);
    for (const owner of [
      ".agents/skills/wtk/SKILL.md",
      ".agents/skills/wtk-lean/SKILL.md",
      ".agents/skills/wtk-implement/SKILL.md",
      ".agents/skills/wtk-ship/SKILL.md",
      ".agents/skills/wtk/references/evidence.md",
    ]) {
      const links = [...readRepositoryFile(owner).matchAll(/\[[^\]]+\]\(([^)]+)\)/g)]
        .map((match) => resolve(repositoryRoot, dirname(owner), match[1]));
      expect(links).toContain(resolve(repositoryRoot, reference));
    }
  });

  it("IT-008 keeps both descriptions within the authoring contract", () => {
    for (const relativePath of [qaPlanPath, qaExecutePath]) {
      const { name, description } = skillMetadata(relativePath);

      expect(name).toMatch(/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
      expect(name.length).toBeLessThanOrEqual(64);
      expect(description.length).toBeLessThan(1024);
      expect(description.trim().length).toBeGreaterThan(0);
    }

    expect(() => parseSkillMetadata("name: wtk-qa-plan\ndescription: misplaced", "fixture")).toThrow(
      "Missing valid initial frontmatter",
    );

    const reviewRounds = readRepositoryFile(".agents/skills/wtk/references/review-rounds.md");
    expect(reviewRounds).toContain("fingerprint = requirement + root cause + failure path");
    expect(reviewRounds).toContain("independent cumulative failed-remediation counter and append-only generation history");
    expect(reviewRounds).toContain("live `[remediation].stall_attempts` threshold");
    expect(reviewRounds).toContain("every failed post-fix Verifier result, whether or not the build gate is green");
    expect(reviewRounds).toContain("Rewording or reopening a finding preserves its fingerprint and counter");
    expect(reviewRounds).toContain("A distinct finding starts at count zero and does not consume another fingerprint's counter");
    expect(reviewRounds).not.toMatch(/one global (?:remediation|blocker) counter/i);

    for (const relativePath of [
      "docs/toolkit/reviews.md",
      "docs/toolkit/README.md",
      "docs/toolkit/purpose.md",
    ]) {
      const source = readRepositoryFile(relativePath);
      expect(source).toContain("review-rounds");
      expect(source).toContain("fingerprint");
    }
    // The router no longer restates the loop; it routes to the phase skills that own it.
    const router = readRepositoryFile(".agents/skills/wtk/SKILL.md");
    expect(router).toContain("wtk-implement");
    expect(router).toContain("wtk-lean");
    expect(readRepositoryFile(".agents/skills/wtk-lean/SKILL.md")).toContain(
      "validate_verification.py",
    );
    const convergence = readRepositoryFile(".agents/skills/wtk-ship/scripts/review_convergence.py");
    expect(convergence).toContain("failed_remediations");
    expect(convergence).toContain("os.replace");
  });

  it("IT-003 dispatches all QA phases through each existing Verifier", () => {
    for (const relativePath of verifierPacketPaths) {
      const source = readRepositoryFile(relativePath);
      const normalized = normalizePacket(source);
      const routing = normalized.slice(normalized.indexOf("## Routing"), normalized.indexOf("## Result"));

      expect(normalized.match(/phase: exactly one of [^.]+\./)?.[0]).toBe(
        "phase: exactly one of technical, wtk-qa-plan, or wtk-qa-execute.",
      );
      expect(routing).toContain("Run exactly one phase per packet");
      expect(routing).toContain("For technical, check each AC against file:line assertions");
      expect(routing).toContain("For wtk-qa-plan, invoke the canonical wtk-qa-plan skill");
      expect(routing).toContain("For wtk-qa-execute, invoke the canonical wtk-qa-execute skill");
      expect(routing).not.toContain("For wtk-qa-plan, invoke the canonical wtk-qa-execute skill");
      expect(routing).not.toContain("For wtk-qa-execute, invoke the canonical wtk-qa-plan skill");
      expect(normalized).toContain("Author and verifier identities must differ");
      expect(normalized).toContain("same non-author QA session");
      expect(normalized).toContain("pause walks during remediation");
      expect(source).toContain("purely internal refactor");
      expect(source).toMatch(/UI.*API.*CLI.*mobile.*adoption.*docs-as-interface/s);
      expect(source).not.toMatch(/separate QA reviewer/i);
    }

    const reviewRounds = readRepositoryFile(".agents/skills/wtk/references/review-rounds.md");
    const workflowConfig = readRepositoryFile(".agents/skills/wtk-config/SKILL.md");
    const wtkShip = readRepositoryFile(".agents/skills/wtk-ship/SKILL.md");

    expect(reviewRounds).toContain("The provider `verifier` executes exactly one phase per packet");
    expect(reviewRounds).toContain("Deep-review is a separate orchestrator stage, not a Verifier phase");
    expect(reviewRounds).not.toContain("The existing provider `verifier` performs all stages");
    expect(reviewRounds).not.toMatch(/provider `verifier`[^.]*wtk-deep-review/i);
    expect(readRepositoryFile("docs/toolkit/reviews.md")).toContain(
      "Deep-review is a separate stage, not a Verifier phase.",
    );
    expect(workflowConfig).toContain("[remediation]` table");
    const remediation = reviewRounds.slice(
      reviewRounds.indexOf("## Escalation"),
      reviewRounds.indexOf("## Requirement and contract parity"),
    );
    expect(remediation).toContain("While a remediation check leaves a Critical/Major open");
    expect(remediation).toContain("run its scoped gate after every attempt");
    expect(remediation).toContain(
      "stable signature from sorted failing-test identifiers after removing timings, absolute paths, and line numbers",
    );
    expect(remediation).toContain(
      "current failing-test set that is a strict subset of the running minimum failing-test set resets the counter",
    );
    expect(remediation).toContain("equal-size set, including one with different members");
    expect(remediation).toContain("a larger set increments it");
    expect(remediation).toContain("`stall_attempts = 0` is unbounded");
    expect(remediation).toContain(
      "when a nonzero threshold is reached, halt with the repeated signature, attempt count, and fixes tried",
    );
    expect(remediation).toContain(
      "If the gate is unavailable, halt immediately without another remediation check",
    );
    expect(remediation).toContain("An open Critical alone does not halt while attempts establish new minima");
    expect(remediation.indexOf("While a remediation check leaves a Critical/Major open")).toBeLessThan(
      remediation.indexOf("run its scoped gate after every attempt"),
    );
    expect(remediation.indexOf("run its scoped gate after every attempt")).toBeLessThan(
      remediation.indexOf("stable signature from sorted failing-test identifiers"),
    );
    expect(remediation.indexOf("stable signature from sorted failing-test identifiers")).toBeLessThan(
      remediation.indexOf("strict subset of the running minimum"),
    );
    expect(remediation.indexOf("strict subset of the running minimum")).toBeLessThan(
      remediation.indexOf("when a nonzero threshold is reached"),
    );
    expect(remediation.indexOf("a larger set increments it")).toBeGreaterThan(
      remediation.indexOf("strict subset of the running minimum"),
    );
    expect(wtkShip).toContain("close_feature.py");
    expect(wtkShip).toContain("feature branch push, one pull request, and merge");
  });

  it("IT-004 keeps QA scenario fields and statuses in one authoritative guideline", () => {
    const scenarioGuideline = readRepositoryFile(".agents/skills/wtk-qa/references/qa-scenarios.md");
    const executionGuideline = readRepositoryFile(".agents/skills/wtk-qa-execute/references/qa-execution.md");
    const reviewGuideline = readRepositoryFile(".agents/skills/wtk/references/review-rounds.md");

    expect(scenarioGuideline).toContain("Field rules");
    expect(scenarioGuideline).toContain("Status enums");
    expect(executionGuideline).toContain("qa-scenarios.md");
    expect(executionGuideline).toContain("wtk-qa-plan");
    expect(executionGuideline).toContain("wtk-qa-execute");
    expect(executionGuideline).not.toMatch(/(?:^|\n)(?:id|qa_status|fix_status|retest_status):/);
    expect(executionGuideline).not.toContain("docs/qa/protocol.md");
    expect(executionGuideline).not.toContain("docs/qa/tours.md");
    expect(executionGuideline).not.toContain("docs/qa/edge-cases.md");
    expect(executionGuideline.split(/\r?\n/).length).toBeLessThanOrEqual(60);
    expect(reviewGuideline).toContain("qa-scenarios.md");
    expect(reviewGuideline.trimEnd().split(/\r?\n/).length).toBeLessThanOrEqual(160);

    const approvedLoopRule =
      normalizePacket(reviewGuideline).match(/2\. \*\*Nitpicks never trigger a review\.\*.*?(?=3\. \*\*)/)?.[0] ?? "";
    for (const anchor of [
      "active, already-approved review loop",
      "fix blocking findings",
      "without new human approval",
      "one remediation batch, then one remediation check",
      "scoped gate",
      "after each correction",
      "a one-job incremental wtk-deep-review over reviewed_head..HEAD",
      "Repeat batch + check until no Critical/Major is open",
      "[remediation].stall_attempts halts",
      "escalate only",
      "post-fix gate fails",
      "stall threshold is reached for the same fingerprint",
      "remote actions retain separate approval requirements",
    ]) {
      expect(approvedLoopRule).toContain(anchor);
    }
    expect(approvedLoopRule.indexOf("one remediation batch, then one remediation check")).toBeLessThan(
      approvedLoopRule.indexOf("Repeat batch + check until no Critical/Major is open"),
    );
    expect(approvedLoopRule.indexOf("Repeat batch + check until no Critical/Major is open")).toBeLessThan(
      approvedLoopRule.indexOf("without new human approval"),
    );
    expect(approvedLoopRule.indexOf("without new human approval")).toBeLessThan(
      approvedLoopRule.indexOf("scoped gate after each correction"),
    );
    expect(approvedLoopRule.indexOf("scoped gate after each correction")).toBeLessThan(
      approvedLoopRule.indexOf("escalate only"),
    );
    expect(approvedLoopRule.indexOf("escalate only")).toBeLessThan(
      approvedLoopRule.indexOf("stall threshold is reached for the same fingerprint"),
    );
    expect(approvedLoopRule).not.toMatch(/ask(?: the human)? whether to fix/i);
    expect(readRepositoryFile(".agents/skills/wtk-deep-review/SKILL.md")).toContain(
      "FIX_BEFORE_SHIP` is actionable, not a prompt for approval",
    );

    for (const relativePath of verifierPacketPaths) {
      const packet = readRepositoryFile(relativePath);

      expect(packet).toContain("qa-scenarios.md");
      expect(packet).not.toMatch(
        /(?:^|\n)\s*(?:id|area|title|persona|journey|expected|entry_points|qa_status|bug_ids|fix_status|retest_status|fix_commits|evidence|last_report|overlaps):/m,
      );
      expect(packet).not.toMatch(/(?:Field rules|Status enums|qa_status:\s*(?:untested|pass|fail))/i);
    }
  });

  it("IT-022 reconciles reusable QA charters, spec-anchored cases, and filed-issue QA", () => {
    const execution = readRepositoryFile(".agents/skills/wtk-qa-execute/references/qa-execution.md");
    const qaPlan = readRepositoryFile(".agents/skills/wtk-qa-plan/SKILL.md");
    const testContract = readRepositoryFile(".agents/skills/wtk/references/test-contract.md");
    const reviewRounds = readRepositoryFile(".agents/skills/wtk/references/review-rounds.md");

    expect(normalizePacket(qaPlan)).toMatch(/Reuse an existing charter/);
    expect(normalizePacket(qaPlan)).toMatch(/preserve historical charters/);
    expect(normalizePacket(qaPlan)).toMatch(/only for a new or changed mission/);
    expect(execution).toContain(".agents/skills/wtk-qa-execute/references/fix-loop.md");

    expect(testContract).toContain("Every case maps to a spec acceptance criterion");
    expect(testContract).toContain("clarify the acceptance criterion before adding a case");
    expect(testContract).toContain("Never create a case solely because a");
    expect(testContract).toContain("[Lean checks reference](../../wtk-lean/references/checks.md)");
    expect(testContract).toContain("only schema and");
    expect(testContract).toContain("standard` and `ui` inject faults; `light` does not");
    expect(testContract).toContain("owning check or slice");
    expect(testContract).not.toContain("## Unit");
    expect(testContract).not.toContain("Every ID is assigned to exactly one check");
    expect(testContract).not.toContain("Every check has one proof");
    expect(testContract).not.toContain("Test Coverage Matrix");
    expect(testContract).not.toContain("implementing task");
    expect(testContract).not.toContain("Unit cases come from every component");
    expect(testContract).not.toContain("integration cases from every component boundary");

    const filedIssueRule = reviewRounds.slice(
      reviewRounds.indexOf("## Fixing a filed issue"),
      reviewRounds.indexOf("## Escalation"),
    );
    expect(filedIssueRule).toContain("If the fix changes user-visible behaviour");
    expect(filedIssueRule).toContain("flag its scenario");
    expect(filedIssueRule).toContain("walk it");
  });

  it("IT-013 records the selected QA adapter and checkout-local evidence", () => {
    const qaExecute = readRepositoryFile(".agents/skills/wtk-qa-execute/SKILL.md");

    expect(qaExecute).toContain("docs/qa/README.md");
    expect(qaExecute).toMatch(/Report the exact adapter, path, evidence, and\s+limitation/);
    expect(qaExecute).toMatch(/does not write product code, install a framework, invent a\s+command/);

    for (const relativePath of verifierPacketPaths) {
      const source = readRepositoryFile(relativePath);

      expect(source).toContain("docs/qa/README.md");
      expect(source).toContain("existing adapter");
      expect(source).toContain("exact path");
      expect(source).toContain("evidence");
      expect(source).toContain("limitation");
      expect(source).toMatch(/never install.*invent/s);
      expect(source).toContain("checkout-local");
    }
  });
});

describe("configurable review policy", () => {
  it("uses the canonical hierarchy and resolved wtk-deep-review groups", () => {
    const agents = readRepositoryFile("AGENTS.md");
    const reviewRounds = readRepositoryFile(".agents/skills/wtk/references/review-rounds.md");
    const reviews = readRepositoryFile("docs/toolkit/reviews.md");
    const wtkShip = readRepositoryFile(".agents/skills/wtk-ship/SKILL.md");
    const loop = readRepositoryFile("docs/toolkit/loop.md");
    const tour = readRepositoryFile("docs/toolkit/README.md");
    const readme = readRepositoryFile("README.md");

    expect(agents).toContain("Feature -> Slice -> Check");
    expect(agents).toContain(".agents/skills/wtk-config/SKILL.md");

    const reviewConfigPointer = ".agents/skills/wtk-config/SKILL.md";
    expect(reviewRounds).toContain(reviewConfigPointer);
    expect(reviewRounds.indexOf(reviewConfigPointer)).toBeLessThan(
      reviewRounds.indexOf("## The feature closing step"),
    );
    for (const repeatedCadenceText of [
      "`slice`, `feature`, or `grouped.N`",
      "absent config means",
      "four-slice feature",
      "3+1",
    ]) {
      expect(reviewRounds).not.toContain(repeatedCadenceText);
    }

    expect(reviews).toContain(reviewConfigPointer);
    expect(reviews.indexOf(reviewConfigPointer)).toBeLessThan(
      reviews.indexOf("## One Verifier role, several phases"),
    );
    expect(reviews).not.toContain("`slice`, `feature`, or balanced `grouped.N`");
    expect(reviews).not.toContain("absent config defaults to `grouped.3`");

    const wtkShipPointer = ".agents/skills/wtk-config";
    expect(wtkShip).toContain(wtkShipPointer);
    expect(wtkShip.indexOf(wtkShipPointer)).toBeGreaterThanOrEqual(0);

    const loopPointer = "Resolve cadence with `wtk-config` before dispatch.";
    expect(loop).toContain(loopPointer);
    expect(loop.indexOf(loopPointer)).toBeLessThan(loop.indexOf("## Stages"));

    const tourPointer = ".agents/skills/wtk-config/SKILL.md";
    expect(tour).toContain(tourPointer);
    expect(tour.indexOf(tourPointer)).toBeLessThan(tour.indexOf("A filed issue skips the ceremony"));
    expect(readme).toContain("The `wtk-config` cadence controls the selected wtk-deep-review groups.");
    expect(readme).toContain("CLI override > profile > native provider");
    expect(readme).toContain(".specs/features/<feature>/workflow.json");
    expect(reviewRounds).toContain("wtk-deep-review** (resolved implementation groups)");
    expect(reviewRounds).not.toContain("wtk-deep-review** (every slice)");
    const finalGroupInstruction =
      "Before final QA, complete the final pending implementation wtk-deep-review group; cadence `skip` resolves no groups, so nothing waits for wtk-deep-review.";
    expect(readme).toContain("`skip` resolves to\nno groups (`[]`)");
    expect(readRepositoryFile(".wtk.toml.example")).toMatch(/^cadence = "skip".*\bon demand\b/m);
    const qaHeading = "## The feature closing step";
    const remediationInstruction =
      "For QA code remediation, review only `reviewed_head..HEAD`, then re-walk affected scenario rows.";
    expect(reviewRounds).toContain(finalGroupInstruction);
    expect(reviewRounds.indexOf(finalGroupInstruction)).toBeLessThan(reviewRounds.indexOf(qaHeading));
    expect(reviewRounds).toContain(remediationInstruction);
    const deltaIndex = reviewRounds.indexOf("review only `reviewed_head..HEAD`");
    const rerunIndex = reviewRounds.indexOf("then re-walk affected scenario rows");
    expect(deltaIndex).toBeGreaterThan(-1);
    expect(deltaIndex).toBeLessThan(rerunIndex);
    expect(wtkShip).toContain("selected `wtk-deep-review`");
    expect(loop).toContain("wtk-deep-review follows resolved");
    expect(tour).toContain("wtk-deep-review groups from wtk-config");
  });

  it("fixes every wtk-deep-review defect inside the originating feature run", () => {
    const reviewRounds = readRepositoryFile(".agents/skills/wtk/references/review-rounds.md");
    const reviews = readRepositoryFile("docs/toolkit/reviews.md");
    const wtkShip = readRepositoryFile(".agents/skills/wtk-ship/SKILL.md");
    const pack = readRepositoryFile("docs/toolkit/pack.md");
    const implement = readRepositoryFile(".agents/skills/wtk-implement/SKILL.md");
    const reviewOutput = readRepositoryFile(
      ".agents/skills/wtk-deep-review/references/output-contracts.md",
    );
    expect(reviewRounds).toContain("Fix every confirmed wtk-deep-review defect");
    expect(reviewRounds).toContain("a Minor-only batch starts no fresh Technical Verifier, QA phase, or remediation check");
    expect(reviewRounds).toContain("Trivials and advisories become follow-ups");
    expect(reviews).toContain("Every wtk-deep-review defect is fixed inside the feature run");
    expect(reviews).toContain("Fix in one current-run batch, scoped gate, one commit");
    expect(reviewOutput).toContain("mandatory current-feature closeout batch");
    expect(wtkShip).toContain("Confirmed Critical, Major,");
    expect(pack).toContain("no Critical, Major, or Minor left");
    expect(implement).toContain("coherent pieces");
    expect(implement).toContain("fresh sub-agent");
  });

  it("bridges workflow resolution and feature-closing QA ordering", () => {
    const specDriven = readRepositoryFile(".agents/skills/wtk/SKILL.md");
    const qaScenarios = readRepositoryFile(".agents/skills/wtk-qa/references/qa-scenarios.md");
    const gates = readRepositoryFile(".agents/skills/wtk/references/validation.md");
    const testContract = readRepositoryFile(".agents/skills/wtk/references/test-contract.md");
    const normalizedTestContract = testContract.replace(/\s+/g, " ");
    expect(specDriven).toContain("wtk-config");
    expect(readRepositoryFile(".agents/skills/wtk-config/SKILL.md")).toContain("workflow.json");

    const closingQa =
      "The feature-closing QA session runs after the final implementation wtk-deep-review group";
    expect(qaScenarios).toContain(closingQa);
    expect(qaScenarios).not.toContain("The feature's last slice runs");
    expect(qaScenarios).not.toContain("A slice walks what it flags");
    for (const source of [
      readRepositoryFile(".agents/skills/wtk-qa-execute/references/qa-execution.md"),
      readRepositoryFile(".agents/skills/wtk/references/review-rounds.md"),
      readRepositoryFile("docs/toolkit/loop.md"),
      readRepositoryFile("docs/toolkit/reviews.md"),
    ]) {
      expect(source).toContain("no slice runs QA");
      expect(source).not.toMatch(/public slices?|per-slice QA/i);
    }
    expect(gates).toContain(
      "| Closing a task with a browser surface | The consuming project's browser scoped gate, filtered by `@feature:<slug>` |",
    );
    expect(normalizedTestContract).toContain(
      "The `@feature:<slug>` tag is the selector the consuming project's browser scoped gate uses",
    );
  });
});

describe("repository intelligence policy", () => {
  it("IT-023 keeps routed tools standard, source-authoritative, and OpenDesign optional", () => {
    const readme = readRepositoryFile("README.md");
    const uiux = readRepositoryFile(".agents/skills/wtk/references/ui-ux.md");
    const security = readRepositoryFile(".agents/skills/wtk/references/security.md");
    const state = readRepositoryFile(".specs/STATE.md");
    const normalizedUiux = uiux.replace(/\s+/g, " ");
    const normalizedSecurity = security.replace(/\s+/g, " ");

    expect(readme).toContain("Graphify");
    expect(readme).toContain("Graft");
    expect(readme).toContain("optional tool was unavailable");
    expect(readme).not.toContain("Graft can enrich wtk-deep-review context");
    const repositoryIntelligence = readRepositoryFile("docs/toolkit/repository-intelligence.md");
    expect(repositoryIntelligence).toContain("Graphify and Graft are standard development tools");
    expect(repositoryIntelligence).toContain("Deep Review always prepares fresh Graft context");
    expect(repositoryIntelligence).toContain("10–20 distinct terminal tasks");
    expect(normalizedUiux).toContain("repository stores only the approved handoff");
    expect(normalizedUiux).toContain("`spec.md` → `uiux.md` → approved design");
    expect(normalizedUiux).toContain("tool or plugin output, then legacy mockup");
    expect(normalizedUiux).toContain("tool absence or failure falls back to the normal repository artifacts");
    expect(normalizedSecurity).toContain("isolated environment or with explicitly allowed directories");
    expect(normalizedSecurity).toContain("Validate destination paths and symlinks before the first write");
    expect(normalizedSecurity).toContain("never delete them automatically");
    expect(normalizedSecurity).toContain("SEC IDs trace to native `C<n>` checks, not tasks");
    expect(normalizedSecurity).toContain("Examples only — not a `checks.md` schema");
    expect(normalizedSecurity).not.toContain("assigned to exactly one task");
    expect(state).toContain("### AD-033");
    expect(state).toContain("This supersedes AD-005 and AD-006");
    expect(state).toContain("OpenDesign remains an");
    expect(state).toContain("Graft");
    expect(state).toContain("OpenDesign");
  });
});

describe("agent configuration", () => {
  it("IT-018 keeps the three harness matrices and dedicated Deep Review agents aligned", () => {
    const frontmatterValue = (source: string, key: string): string =>
      source.match(new RegExp(`^${key}:\\s*(.+)$`, "m"))?.[1]?.trim() ?? "";
    const tomlValue = (source: string, key: string): string =>
      source.match(new RegExp(`^${key}\\s*=\\s*"([^"]+)"$`, "m"))?.[1] ?? "";
    const value = (source: string, format: "frontmatter" | "toml", key: string): string =>
      format === "toml" ? tomlValue(source, key) : frontmatterValue(source, key);

    const config = readRepositoryFile(".wtk.toml.example");
    const settings = new Map<string, { model: string; effort: string }>();
    const section = /\[models\.(claude|codex|cursor)\.(planner|implementer|verifier|explorer|deep_reviewer|designer)\]\s+model = "([^"]+)"\s+effort = "([^"]+)"/g;
    for (const match of config.matchAll(section)) {
      settings.set(`${match[1]}.${match[2]}`, { model: match[3], effort: match[4] });
    }
    expect(settings.size).toBe(18);

    for (const provider of ["claude", "codex", "cursor"] as const) {
      for (const role of ["planner", "implementer", "verifier", "explorer", "deep_reviewer", "designer"] as const) {
        const agentName = role === "deep_reviewer" ? "deep-reviewer" : role;
        const extension = provider === "codex" ? "toml" : "md";
        const format = provider === "codex" ? "toml" : "frontmatter";
        const relativePath = `.agents/skills/wtk-config/assets/agents/${provider}/${agentName}.${extension}`;
        const source = readRepositoryFile(relativePath);
        const expected = settings.get(`${provider}.${role}`)!;
        expect(source).toContain("docs/product/AGENT-CONTEXT.md");
        expect(source).toContain("role/task");
        expect(value(source, format, "name")).toBe(agentName);
        if (provider === "cursor") {
          expect(value(source, format, "model")).toBe(`${expected.model}[effort=${expected.effort}]`);
        } else {
          expect(value(source, format, "model")).toBe(expected.model);
          const effortKey = provider === "codex" ? "model_reasoning_effort" : "effort";
          expect(value(source, format, effortKey)).toBe(expected.effort);
        }
        if (role === "deep_reviewer") {
          expect(source).toContain("Do not edit source, tests, or configuration.");
          expect(source).toMatch(/one materialized Deep Review job/i);
          expect(source).toMatch(/one output artifact/i);
          expect(source).toMatch(/findings through .*schema/i);
        }
      }
    }

    expect(readRepositoryFile(".agents/skills/wtk-config/assets/agents/claude/deep-reviewer.md")).toMatch(
      /^tools:\s*Read, Grep, Glob, Bash$/m,
    );
    const cursorDeepReviewer = readRepositoryFile(".agents/skills/wtk-config/assets/agents/cursor/deep-reviewer.md");
    expect(cursorDeepReviewer).not.toMatch(/^readonly:\s*true$/m);

    const runtime = readRepositoryFile(".agents/skills/wtk-deep-review/references/subagent-runtimes.md");
    const orchestration = readRepositoryFile(".agents/skills/wtk-deep-review/references/orchestration.md");
    const deepReviewSkill = readRepositoryFile(".agents/skills/wtk-deep-review/SKILL.md");

    expect(deepReviewSkill).toMatch(
      /\| `--no-workflow` \|.*Named native `deep-reviewer` when the host supports it; role-free Workflow fallback/,
    );
    expect(deepReviewSkill).not.toContain("Workflow when available");
    expect(deepReviewSkill.indexOf("Named native `deep-reviewer`")).toBeLessThan(
      deepReviewSkill.indexOf("role-free Workflow fallback"),
    );
    expect(deepReviewSkill).toContain("Named native `deep-reviewer`");
    expect(orchestration).toContain("**Named native dispatch (default when host supports it).**");
    expect(orchestration).toContain("**Workflow fallback (when named native dispatch is unavailable).**");

    const codexRuntime = runtime.match(/^\|\s*`codex`\s*\|([^\n]+)$/m)?.[1] ?? "";
    expect(codexRuntime).toContain("gpt-5.6-luna");
    expect(codexRuntime).toContain("--reasoning-effort high");
    expect(codexRuntime).not.toContain("gpt-5.6-sol");
    expect(codexRuntime).not.toContain("xhigh");

    const native = orchestration.slice(
      orchestration.indexOf("**Named native dispatch"),
      orchestration.indexOf("**Workflow fallback"),
    );
    const workflow = orchestration.slice(
      orchestration.indexOf("**Workflow fallback"),
      orchestration.indexOf("**Agent fallback"),
    );
    const fallback = orchestration.slice(orchestration.indexOf("**Agent fallback"));

    expect(native).toMatch(/default when host supports it/i);
    expect(native).toContain('subagent_type: "deep-reviewer"');
    expect(native).toContain('subagentType: { custom: "deep-reviewer" }');
    expect(native).toMatch(/custom agent name\/type `deep-reviewer`/i);
    expect(workflow).toMatch(/fallback/i);
    expect(workflow).toMatch(/agent\(/);
    expect(workflow).toMatch(/role-free/i);
    expect(workflow).not.toMatch(/\(default\)/i);
    expect(fallback).toMatch(/named native selectors/i);
    expect(fallback).toMatch(/generic prompt-only subagent dispatch/i);
    expect(fallback).toMatch(/unsupported role\s+argument/i);
  });
});

describe("adoption and public setup", () => {
  it("IT-005 publishes provenance for TLC, Deep Review, and QA inspirations", () => {
    const readme = readRepositoryFile("README.md");

    expect(readme).toContain("Antonio Fulgêncio");
    expect(readme).toContain("Tech Leads Club");
    expect(readme).toContain("https://github.com/tech-leads-club/agent-skills/tree/main/skills");
    expect(readme).toContain("Pedro Nauck");
    expect(readme).toContain("https://github.com/pedronauck/skills/tree/main/skills/mine");
  });

  it("IT-006 keeps the public README product-neutral", () => {
    const readme = readRepositoryFile("README.md");

    expect(readme).toContain("stack-agnostic");
    expect(readme).not.toMatch(/Creatista|antclips|hono|drizzle|tanstack|shadcn|better-auth|graphile/);
  });

  it("IT-010 makes adoption reviewable and routes QA by observability", () => {
    const readme = readRepositoryFile("README.md");
    const prompt = readRepositoryFile("docs/adoption-prompt.md");
    const adopt = readRepositoryFile(".agents/skills/wtk-config/SKILL.md");

    expect(readme).toContain("skill installer");
    expect(readme).toContain("Optional project instructions");
    expect(prompt).toContain("git status --short");
    expect(prompt).toContain("read-only");
    expect(prompt).toContain("skill installer");
    expect(prompt).toContain("byte-for-byte");
    expect(prompt).toContain("never overwrite existing content");
    const qaPolicyPath = ".agents/skills/wtk-qa-execute/references/qa-execution.md";
    expect(prompt).toContain(qaPolicyPath);
    const qaPolicy = readRepositoryFile(qaPolicyPath);
    for (const phase of ["wtk-qa-plan", "wtk-qa-execute"]) expect(qaPolicy).toContain(phase);
    expect(prompt).toContain("optional companion");
    expect(prompt).toContain("manual review");
    expect(adopt).toContain(".wtk.toml");
    expect(adopt).toContain("wtk-config");
  });

  it("IT-009 exposes the fixed layered adoption boundary", () => {
    const readme = readRepositoryFile("README.md");

    expect(readme).toContain("`wtk`");
    expect(readme).toContain("`wtk-lean`");
    expect(readme).toContain("`wtk-qa`");
    expect(readme).toContain("skill installer");
  });

  it("IT-019 keeps README installation prerequisites and bundled skills authoritative", () => {
    const readme = readRepositoryFile("README.md");

    expect(readme).toContain("self-contained");
    expect(readme).toContain("does not edit");
    expect(readme).toContain("Ponytail");
    expect(readme).toContain("Security lifecycle");
    expect(readme).toContain("Graphify");
    expect(readme).toContain("Graft");
  });

  it("IT-021 keeps Ponytail active from workflow start through the full cycle", () => {
    const agents = readRepositoryFile("AGENTS.md");
    const loop = readRepositoryFile("docs/toolkit/loop.md");
    const prompt = readRepositoryFile("docs/adoption-prompt.md");

    expect(normalizePacket(agents)).toMatch(/Ponytail is an optional companion skill/);
    expect(loop).toContain("Ponytail is an optional companion skill");
    expect(normalizePacket(prompt)).toMatch(/Optional companion/);
    expect(existsSync(join(repositoryRoot, ".agents/skills/ponytail"))).toBe(false);
  });

  it("IT-020 keeps the pack guide source-only for adopted consumers", () => {
    const tour = readRepositoryFile("docs/toolkit/README.md");
    const pack = readRepositoryFile("docs/toolkit/pack.md");

    expect(tour).toContain("[Skills and optional extensions](pack.md)");
    expect(pack).toContain("skill directories");
  });

  it("IT-011 keeps stack-specific QA capabilities in the operational profile", () => {
    const profile = readRepositoryFile("docs/qa/README.md");

    for (const heading of [
      "## Public interfaces and area codes",
      "## Runner and adapter",
      "## Build, start, and health",
      "## Authentication and test data",
      "## Evidence and limitations",
    ]) {
      expect(profile).toContain(heading);
    }
    expect(profile).toContain("manifests or CI");
    expect(profile.toLowerCase()).toContain("fixtures or seed");
    expect(profile.toLowerCase()).toContain("cleanup");
    expect(profile.toLowerCase()).toContain("residue");
    expect(profile.toLowerCase()).toContain("raw evidence");
    expect(profile).toContain("does not install a framework or invent commands");
  });

  it("IT-012 leaves adapter choice with the consuming project", () => {
    const profile = readRepositoryFile("docs/qa/README.md");
    const qaExecute = readRepositoryFile(".agents/skills/wtk-qa-execute/SKILL.md");

    for (const adapter of ["browser", "API", "CLI", "mobile", "manual"]) {
      expect(profile.toLowerCase()).toContain(adapter.toLowerCase());
      expect(qaExecute.toLowerCase()).toContain(adapter.toLowerCase());
    }
    expect(qaExecute).toContain("existing browser, API, CLI, mobile, or manual adapter");
    expect(qaExecute).toContain("does not write product code, install a framework, invent a");
  });

  it("IT-005 / AIM-11 reports release version and Bun lock identity consistently", () => {
    const manifest = JSON.parse(readRepositoryFile("package.json")) as {
      name?: string;
      version?: string;
      private?: boolean;
      packageManager?: string;
      scripts?: { test?: string };
    };
    const changelog = readRepositoryFile("CHANGELOG.md");
    const releaseScenario = readRepositoryFile("docs/qa/scenarios/REL-report-current-workflow-release.md");
    const currentScenarioVersion = releaseScenario.match(
      /^Version-neutral owner for public release consistency\. For release `(\d+\.\d+\.\d+)`/m,
    )?.[1];
    const latestHeading = changelog.match(/^## \[(\d+\.\d+\.\d+)\]/m)?.[1];
    const releaseStart = changelog.indexOf(`## [${manifest.version}]`);
    const nextRelease = changelog.indexOf("\n## [", releaseStart + 1);
    const latestRelease = changelog.slice(releaseStart, nextRelease === -1 ? undefined : nextRelease);

    expect(manifest.version).toMatch(/^\d+\.\d+\.\d+$/);
    expect(manifest.name).toBe("workflow-toolkit");
    expect(manifest.private).toBe(true);
    expect(manifest.packageManager).toBe("bun@1.4.0");
    expect(manifest.scripts?.test).toBe("bun test && node --test tests/skills/*.test.js");
    expect(readRepositoryFile("bun.lock")).toContain('"name": "workflow-toolkit"');
    expect(existsSync(join(repositoryRoot, "package-lock.json"))).toBe(false);
    expect(latestHeading).toBe(manifest.version);
    expect(currentScenarioVersion).toBe(manifest.version);
    expect(releaseScenario.match(/^expected: (.+)$/m)?.[1]?.trim().length).toBeGreaterThan(0);
    expect(latestRelease).not.toContain("npx wtk install");

    const pack = spawnSync(process.execPath, ["pm", "pack", "--dry-run", "--ignore-scripts"], {
      cwd: repositoryRoot,
      encoding: "utf8",
    });
    expect(pack.status).toBe(0);
    const packOutput = `${pack.stdout}${pack.stderr}`;
    for (const requiredPath of [
      ".agents/skills/wtk-lean/scripts/validate_verification.py",
      ".agents/skills/wtk-ship/scripts/close_feature.py",
      ".agents/skills/wtk-deep-review/SKILL.md",
      ".agents/skills/wtk-ship/remediation.py",
      ".agents/skills/wtk/references/execution-metrics.md",
      "scripts/migrate.js",
    ]) {
      expect(packOutput).toContain(requiredPath);
    }
    expect(readdirSync(repositoryRoot).filter((entry) => entry.endsWith(".tgz"))).toEqual([]);
  });
});

describe("Bun tooling runtime contract", () => {
  it("pins the Bun engine, discovery boundary, and exact Bun-to-Python gate", () => {
    const manifest = JSON.parse(readRepositoryFile("package.json")) as {
      engines?: { bun?: string };
      scripts?: { test?: string; [name: string]: string | undefined };
    };
    const bunfig = readRepositoryFile("bunfig.toml");
    const pythonSuites = trackedRepositoryPaths()
      .filter((relativePath) => /^(?:scripts|tools)\/test_[^/]+\.py$/.test(relativePath))
      .sort();
    const expectedPythonSuites = [
      "tools/test_ad_index.py",
      "tools/test_deep_review_contract.py",
      "tools/test_deep_review_symlink_manifest.py",
      "tools/test_deep_review_token_metrics.py",
      "tools/test_gate_cache.py",
      "tools/test_jev_qa_adapter.py",
      "tools/test_phase_skills.py",
      "tools/test_remediation.py",
      "tools/test_repository_intelligence.py",
      "tools/test_review_convergence.py",
      "tools/test_tlc_validators.py",
      "tools/test_workflow_config.py",
      "tools/test_wtk_contract.py",
      "tools/test_wtk_deep_review_contract.py",
      "tools/test_wtk_forward.py",
      "tools/test_wtk_lifecycle.py",
    ];
    const pythonLoop = "git ls-files -- 'scripts/test_*.py' 'tools/test_*.py' | sort | while read test; do python3 \"$test\" || exit $?; done";

    expect(manifest.engines?.bun).toBe(">=1.4.0 <1.5.0");
    expect(bunfig).toContain("[test]");
    expect(bunfig).toContain('root = "./tools"');
    expect(bunfig).toContain('preload = ["./tools/shared/src/bun-version.ts"]');
    expect(manifest.scripts?.test).toBe("bun test && node --test tests/skills/*.test.js");
    expect(manifest.scripts?.["test:all"]).toBe("bun run test && bun run test:python");
    expect(pythonSuites).toEqual(expectedPythonSuites);
    expect(manifest.scripts?.["test:python"]).toBe(pythonLoop);
  });

  it("keeps every tools test on bun:test and removes forbidden active runner authority", () => {
    const suites = execFileSync("find", ["tools", "-type", "f", "-name", "*.test.ts"], {
      cwd: repositoryRoot,
      encoding: "utf8",
    })
      .trim()
      .split("\n")
      .filter(Boolean);
    const manifest = readRepositoryFile("package.json");

    expect(suites.length).toBeGreaterThan(0);
    for (const suite of suites) {
      expect(readRepositoryFile(suite)).toMatch(/from ["']bun:test["']/);
    }
    expect(manifest).not.toMatch(/"(?:vitest|tsx|yaml)"\s*:/);
    expect(readRepositoryFile(".agents/skills/wtk-knowledge-check/scripts/frontmatter.ts")).not.toMatch(/from ["']yaml["']/);
    expect(readRepositoryFile(".agents/skills/wtk-knowledge-check/scripts/frontmatter.ts")).toContain("Bun.YAML.parse");
  });

  it("IT-006 keeps Bun as the active command authority while allowing historical evidence", () => {
    const trackedPaths = trackedRepositoryPaths();
    const scannedPaths = activeAuthorityPaths(trackedPaths);
    const violations = forbiddenAuthorityViolations(trackedPaths);

    expect(scannedPaths).toContain("README.md");
    expect(scannedPaths).toContain("docs/qa/README.md");
    expect(scannedPaths).toContain("knowledge/AGENTS.md");
    expect(scannedPaths).toContain(".agents/skills/wtk-config/assets/agents/codex/planner.toml");
    expect(violations).toEqual([]);

    const historicalPaths = trackedPaths.filter(isHistoricalAuthority);
    expect(historicalPaths.length).toBeGreaterThan(0);
    expect(
      historicalPaths.some((relativePath) =>
        /\b(?:npm|npx|vitest|tsx)\b|package-lock\.json/i.test(readRepositoryFile(relativePath)),
      ),
    ).toBe(true);

    for (const relativePath of [
      ".agents/skills/wtk-config/assets/agents/codex/planner.toml",
    ]) {
      for (const command of [
        "npm run forbidden",
        "npm start",
        "npx foo",
        "npx --yes eslint",
        "npm exec eslint",
        "npm pack foo",
        "npm pack --pack-destination /tmp/release unrelated-package",
        "npm exec --yes --package ./antoniofulg-scripts-0.10.0.tgz -- \\\neslint",
      ]) {
        const mutated = new Map([[relativePath, `${readRepositoryFile(relativePath)}\n${command}\n`]]);
        const mutationViolations = forbiddenAuthorityViolations(
          [relativePath],
          (path) => mutated.get(path) ?? readRepositoryFile(path),
        );
        expect(mutationViolations).toHaveLength(1);
        expect(mutationViolations[0]).toContain(relativePath);
      }

      const descriptive = new Map([
        [relativePath, `${readRepositoryFile(relativePath)}\nThe npm and npx commands are historical mentions.\n`],
      ]);
      expect(
        forbiddenAuthorityViolations(
          [relativePath],
          (path) => descriptive.get(path) ?? readRepositoryFile(path),
        ),
      ).toEqual([]);

      const allowed = new Map([
        [
          relativePath,
          `${readRepositoryFile(relativePath)}\nnpm pack --pack-destination /tmp/release\nnpm exec --yes --package ./antoniofulg-scripts-0.10.0.tgz -- my-workflow apply /tmp/target\nnpm exec --yes --package ./antoniofulg-scripts-0.10.0.tgz -- \\\n  my-workflow status /tmp/target\nnpx --yes <approved-package>@<exact-version> apply /tmp/target\n`,
        ],
      ]);
      expect(
        forbiddenAuthorityViolations(
          [relativePath],
          (path) => allowed.get(path) ?? readRepositoryFile(path),
        ),
      ).toEqual([]);
    }

    const manifest = JSON.parse(readRepositoryFile("package.json")) as {
      scripts?: Record<string, string>;
    };
    const documentedScripts = documentedBunScripts(trackedPaths);
    expect(documentedScripts.length).toBeGreaterThan(0);
    expect(Object.keys(manifest.scripts ?? {})).toEqual(
      expect.arrayContaining(documentedScripts),
    );
    expect(changedHistoricalQaArtifacts()).toEqual([]);
  });

  it("detects historical QA changes from a local baseline without a remote ref", () => {
    const root = mkdtempSync(join(tmpdir(), "historical-qa-baseline-"));

    try {
      execFileSync("git", ["init", "--quiet", "--initial-branch=main"], { cwd: root });
      mkdirSync(join(root, "docs/qa/reports"), { recursive: true });
      mkdirSync(join(root, "docs/qa/scenarios"), { recursive: true });
      writeFileSync(join(root, "docs/qa/reports/historical.md"), "original\n", "utf8");
      writeFileSync(
        join(root, "docs/qa/scenarios/ADP-baseline.md"),
        "qa_status: pass\n",
        "utf8",
      );
      const baseline = commitFixture(root, "baseline");
      writeFileSync(join(root, "docs/qa/reports/historical.md"), "changed\n", "utf8");
      writeFileSync(
        join(root, "docs/qa/scenarios/ADP-baseline.md"),
        "qa_status: untested\n",
        "utf8",
      );
      mkdirSync(join(root, "docs/qa/charters"), { recursive: true });
      writeFileSync(join(root, "docs/qa/charters/current-cycle.md"), "new charter\n", "utf8");
      commitFixture(root, "historical change");

      expect(changedHistoricalQaArtifacts(root, baseline)).toEqual([
        "docs/qa/reports/historical.md",
      ]);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("fails closed for unsupported and malformed Bun versions before a suite marker runs", () => {
    const versionSource = readRepositoryFile("tools/shared/src/bun-version.ts");

    runBunVersionSensor(versionSource.replace('"1.4.x"', '"9.x"'), "Bun.version");
    runBunVersionSensor(versionSource, JSON.stringify("not-a-version"));
  });
});
