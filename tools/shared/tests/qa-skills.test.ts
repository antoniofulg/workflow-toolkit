import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
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
  "knowledge",
  "package.json",
  "bunfig.toml",
  "scripts",
  "tools",
  ".agents/skills",
] as const;

const historicalAuthorityAllowlist = [
  /^CHANGELOG\.md$/,
  /^\.specs\//,
  /^knowledge\/raw\//,
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
      scripts.add(match[1]!);
    }
  }
  return [...scripts].sort();
}

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

  it("IT-014 leaves feature workflow state to consuming projects", () => {
    const readme = readRepositoryFile("README.md");
    const artifactLifecycle = readRepositoryFile(".agents/skills/wtk/references/artifacts.md");

    expect(isIgnored(".specs/features/qa-skills/spec.md")).toBe(false);
    expect(isIgnored(".specs/STATE.md")).toBe(false);
    expect(isIgnored(".specs/AD-INDEX.md")).toBe(false);
    expect(existsSync(join(repositoryRoot, ".specs"))).toBe(false);
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
    const lean = readRepositoryFile(".agents/skills/wtk-lean/SKILL.md");
    const implementer = readRepositoryFile(".agents/skills/wtk-implement/SKILL.md");
    const memory = readRepositoryFile(".agents/skills/wtk-lean/references/memory.md");

    expect(agents).toContain("Feature -> Slice -> Check");
    expect(lean).toContain("checks.md");
    expect(lean).toContain("verification.md");
    expect(memory).toContain("checks.md");
    expect(implementer).toContain("Every check names its **proof**");
    expect(lean).toContain("checks.md");
    expect(lean).toContain("same turn after the feature's last commit");
    expect(lean).toContain("one fresh Verifier");
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

  it("routes the configured QA browser adapter", () => {
    const qaExecute = normalizePacket(readRepositoryFile(qaExecutePath));
    const session = normalizePacket(readRepositoryFile(".agents/skills/wtk-qa-execute/references/session-protocol.md"));

    expect(qaExecute).toContain("task-scoped QA adapter choice");
    expect(qaExecute).toContain("Without one, use auto");
    for (const value of ["auto", "playwright-mcp", "orca", "maestri", "manual"]) {
      expect(qaExecute).toContain(value);
    }
    expect(qaExecute).toContain("auto tries LLM + Playwright MCP first");
    expect(qaExecute).toContain("exactly one IDE-native Orca or Maestri adapter");
    expect(qaExecute).toContain("Orca before Maestri");
    expect(qaExecute).toContain("A direct value selects only that adapter");
    expect(qaExecute).toContain("inspect or reset the fixture and confirm known isolated state");
    expect(session).toContain("independent read path and after a reload");
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
        .map((match) => resolve(repositoryRoot, dirname(owner), match[1]!));
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
    expect(reviewRounds).toContain("fixed default threshold of three attempts");
    expect(reviewRounds).toContain("every failed post-fix Verifier result, whether or not the build gate is green");
    expect(reviewRounds).toContain("Rewording or reopening a finding preserves its fingerprint and counter");
    expect(reviewRounds).toContain("A distinct finding starts at count zero and does not consume another fingerprint's counter");
    expect(reviewRounds).not.toMatch(/one global (?:remediation|blocker) counter/i);

    expect(readRepositoryFile(".agents/skills/wtk-ship/SKILL.md")).toContain("Confirmed Critical, Major,");
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
    const lean = readRepositoryFile(".agents/skills/wtk-lean/SKILL.md");
    const qaPlan = readRepositoryFile(".agents/skills/wtk-qa-plan/SKILL.md");
    const qaExecute = readRepositoryFile(".agents/skills/wtk-qa-execute/SKILL.md");
    const reviewRounds = readRepositoryFile(".agents/skills/wtk/references/review-rounds.md");
    const wtkShip = readRepositoryFile(".agents/skills/wtk-ship/SKILL.md");

    expect(lean).toContain("one fresh Verifier over `<feature base>..HEAD` with every check");
    expect(qaPlan).toContain("wtk-qa-execute");
    expect(qaExecute).toContain("same non-author Verifier");
    expect(qaExecute).toContain("Do not walk a tree while it is being changed");
    expect(reviewRounds).toContain("The provider `verifier` executes exactly one phase per packet");
    expect(reviewRounds).toContain("Deep-review is a separate orchestrator stage, not a Verifier phase");
    expect(reviewRounds).not.toContain("The existing provider `verifier` performs all stages");
    expect(reviewRounds).not.toMatch(/provider `verifier`[^.]*wtk-deep-review/i);
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
    expect(remediation).toContain(
      "when the third stall is reached, halt with the repeated signature, attempt count, and fixes tried",
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
      remediation.indexOf("when the third stall is reached"),
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
      "default three-attempt stall bound halts",
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

    expect(executionGuideline).toContain("docs/qa/README.md");
    expect(executionGuideline).not.toMatch(
      /(?:^|\n)\s*(?:id|area|title|persona|journey|expected|entry_points|qa_status|bug_ids|fix_status|retest_status|fix_commits|evidence|last_report|overlaps):/m,
    );
    expect(executionGuideline).not.toMatch(/(?:Field rules|Status enums|qa_status:\s*(?:untested|pass|fail))/i);
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

    expect(qaExecute).toContain("existing browser, API, CLI, mobile, or manual adapter");
    expect(qaExecute).toMatch(/Report the exact adapter, path, evidence, and\s+limitation/);
    expect(qaExecute).toContain("raw evidence");
  });
});

describe("configurable review policy", () => {
  it("uses the canonical hierarchy and project-native workflow defaults", () => {
    const agents = readRepositoryFile("AGENTS.md");
    const reviewRounds = readRepositoryFile(".agents/skills/wtk/references/review-rounds.md");
    const wtkShip = readRepositoryFile(".agents/skills/wtk-ship/SKILL.md");
    const readme = readRepositoryFile("README.md");

    expect(agents).toContain("Feature -> Slice -> Check");
    expect(agents).toContain("Project-native agent files own provider, model, and effort settings");
    expect(reviewRounds).toContain("wtk-lean/scripts/workflow_route.py");
    expect(reviewRounds).toContain("Deep Review is on demand by default");
    expect(wtkShip).not.toContain("wtk-config");

    expect(readme).toContain("native agent model and effort settings");
    expect(readme).toContain("fixed default `stall_attempts = 3`");
    expect(readme).toContain(".specs/features/<feature>/workflow.json");
    expect(readme).toContain("model and effort remain in the project's native agent files");
    expect(reviewRounds).toContain("wtk-deep-review** (resolved implementation groups)");
    expect(reviewRounds).not.toContain("wtk-deep-review** (every slice)");
    const finalGroupInstruction =
      "Before final QA, complete the final pending implementation wtk-deep-review group; cadence `skip` resolves no groups, so nothing waits for wtk-deep-review.";
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
    for (const source of [agents, reviewRounds, wtkShip, readme]) {
      expect(source).not.toContain("wtk-config");
      expect(source).not.toContain("workflow_config.py");
    }
  });

  it("fixes every wtk-deep-review defect inside the originating feature run", () => {
    const reviewRounds = readRepositoryFile(".agents/skills/wtk/references/review-rounds.md");
    const wtkShip = readRepositoryFile(".agents/skills/wtk-ship/SKILL.md");
    const implement = readRepositoryFile(".agents/skills/wtk-implement/SKILL.md");
    const reviewOutput = readRepositoryFile(
      ".agents/skills/wtk-deep-review/references/output-contracts.md",
    );
    expect(reviewRounds).toContain("Fix every confirmed wtk-deep-review defect");
    expect(reviewRounds).toContain("a Minor-only batch starts no fresh Technical Verifier, QA phase, or remediation check");
    expect(reviewRounds).toContain("Trivials and advisories become follow-ups");
    expect(reviewOutput).toContain("mandatory current-feature closeout batch");
    expect(wtkShip).toContain("Confirmed Critical, Major,");
    expect(implement).toContain("coherent pieces");
    expect(implement).toContain("fresh sub-agent");
  });

  it("bridges workflow resolution and feature-closing QA ordering", () => {
    const specDriven = readRepositoryFile(".agents/skills/wtk/SKILL.md");
    const qaScenarios = readRepositoryFile(".agents/skills/wtk-qa/references/qa-scenarios.md");
    const gates = readRepositoryFile(".agents/skills/wtk/references/validation.md");
    const testContract = readRepositoryFile(".agents/skills/wtk/references/test-contract.md");
    const normalizedTestContract = testContract.replace(/\s+/g, " ");
    expect(specDriven).toContain("wtk-lean");
    expect(readRepositoryFile(".agents/skills/wtk-lean/scripts/workflow_route.py")).toContain("workflow.json");
    expect(specDriven).not.toContain("wtk-config");

    const closingQa =
      "The feature-closing QA session runs after the final implementation wtk-deep-review group";
    expect(qaScenarios).toContain(closingQa);
    expect(qaScenarios).not.toContain("The feature's last slice runs");
    expect(qaScenarios).not.toContain("A slice walks what it flags");
    for (const source of [
      readRepositoryFile(".agents/skills/wtk-qa-execute/references/qa-execution.md"),
      readRepositoryFile(".agents/skills/wtk/references/review-rounds.md"),
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
    const normalizedUiux = uiux.replace(/\s+/g, " ");
    const normalizedSecurity = security.replace(/\s+/g, " ");

    expect(readme).toContain("Graphify");
    expect(readme).toContain("Graft");
    expect(readme).toContain("optional tool was unavailable");
    expect(readme).not.toContain("Graft can enrich wtk-deep-review context");
    const repositoryIntelligence = readRepositoryFile(".agents/skills/wtk-deep-review/references/orchestration.md");
    expect(repositoryIntelligence).toContain("prepares the pinned Graft context");
    expect(repositoryIntelligence).toContain("falls back to plain repository inspection");
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
  });
});

describe("agent configuration", () => {
  it("IT-018 keeps project-native role metadata and dedicated Deep Review dispatch aligned", () => {
    const route = readRepositoryFile(".agents/skills/wtk-lean/scripts/workflow_route.py");
    const lean = readRepositoryFile(".agents/skills/wtk-lean/SKILL.md");
    const packageJson = JSON.parse(readRepositoryFile("package.json")) as { files: string[] };

    expect(route).not.toContain("model");
    expect(route).not.toContain("effort");
    expect(lean).toContain("native agent-file identity");
    expect(lean).toContain("Projects own");
    expect(packageJson.files).not.toContain(".agents/skills/wtk-config");
    expect(existsSync(join(repositoryRoot, ".wtk.toml.example"))).toBe(false);

    for (const provider of ["claude", "codex", "cursor"] as const) {
      for (const role of ["planner", "implementer", "verifier", "explorer", "deep-reviewer", "designer"] as const) {
        const extension = provider === "codex" ? "toml" : "md";
        const relativePath = `.${provider}/agents/${role}.${extension}`;
        const source = readRepositoryFile(relativePath);
        expect(source).toMatch(provider === "codex" ? /^model = ".+"$/m : /^model: .+$/m);
        if (provider === "codex") expect(source).toMatch(/^model_reasoning_effort = ".+"$/m);
        if (provider === "claude") expect(source).toMatch(/^effort: .+$/m);
        if (provider === "cursor") expect(source).toMatch(/^model: .+\[effort=.+\]$/m);
      }
    }

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
    const route = readRepositoryFile(".agents/skills/wtk-lean/scripts/workflow_route.py");

    expect(readme).toContain("skill installer");
    expect(readme).toContain("Optional project instructions");
    const qaPolicyPath = ".agents/skills/wtk-qa-execute/references/qa-execution.md";
    const qaPolicy = readRepositoryFile(qaPolicyPath);
    for (const phase of ["wtk-qa-plan", "wtk-qa-execute"]) expect(qaPolicy).toContain(phase);
    expect(readme).toContain("Recommended companion skills and tools");
    expect(readme).toContain("native model and effort metadata");
    expect(route).toContain("native_provider");
    expect(route).not.toContain(".wtk.toml");
    expect(route).not.toContain('"model"');
    expect(route).not.toContain('"effort"');
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
    const readme = readRepositoryFile("README.md");

    expect(normalizePacket(agents)).toMatch(/Ponytail is an optional companion skill/);
    expect(readme).toContain("Ponytail");
    expect(existsSync(join(repositoryRoot, ".agents/skills/ponytail"))).toBe(false);
  });

  it("IT-020 keeps the source pack free of project documentation", () => {
    expect(existsSync(join(repositoryRoot, "docs"))).toBe(false);
    expect(readRepositoryFile("README.md")).toContain("only that skill's files");
  });

  it("IT-011 keeps stack-specific QA capabilities in the operational profile", () => {
    const profile = readRepositoryFile(".agents/skills/wtk-qa-plan/references/profile.md");

    for (const capability of [
      "Public interfaces and area codes",
      "Runner or adapter",
      "Build/start path and health signal",
      "Authentication and session setup",
      "Limitations and unavailable surfaces",
    ]) expect(profile).toContain(capability);
    expect(profile).toContain("manifests or CI");
    expect(profile.toLowerCase()).toContain("fixtures or seed");
    expect(profile.toLowerCase()).toContain("cleanup");
    expect(profile.toLowerCase()).toContain("residue");
    expect(profile).toContain("Framework installation is");
  });

  it("IT-012 leaves adapter choice with the consuming project", () => {
    const profile = readRepositoryFile(".agents/skills/wtk-qa-execute/SKILL.md");
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
    const latestHeading = changelog.match(/^## \[(\d+\.\d+\.\d+)\]/m)?.[1];
    const unreleasedStart = changelog.indexOf("## [Unreleased]");
    const firstRelease = changelog.indexOf("\n## [", unreleasedStart + 1);
    const unreleased = changelog.slice(unreleasedStart, firstRelease === -1 ? undefined : firstRelease).replace(/\s+/g, " ");
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
    expect(latestRelease).not.toContain("npx wtk install");
    expect(latestRelease).toContain("complete set of 12 `wtk*` skills");
    expect(readRepositoryFile("README.md")).toContain("npx skills add antoniofulg/workflow-toolkit");
    expect(latestRelease).toContain("Ponytail, security lifecycle, and other companion skills");
    expect(latestRelease).toContain("Retired the package installer");
    expect(latestRelease).toContain("CLEANUP.md");
    expect(unreleased).not.toMatch(/npx workflow-toolkit(?:@[^ ]+)? install/);
    expect(unreleased).not.toContain("install_security_skills");

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
      "tools/test_native_agent_routing.py",
      "tools/test_phase_skills.py",
      "tools/test_remediation.py",
      "tools/test_repository_intelligence.py",
      "tools/test_review_convergence.py",
      "tools/test_tlc_validators.py",
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
    expect(scannedPaths).toContain(".agents/skills/wtk-qa-execute/SKILL.md");
    expect(scannedPaths).toContain("knowledge/AGENTS.md");
    expect(scannedPaths).toContain(".agents/skills/wtk-lean/scripts/workflow_route.py");
    expect(violations).toEqual([]);

    const historicalPaths = trackedPaths.filter(isHistoricalAuthority);
    expect(historicalPaths.length).toBeGreaterThan(0);
    expect(
      historicalPaths.some((relativePath) =>
        /\b(?:npm|npx|vitest|tsx)\b|package-lock\.json/i.test(readRepositoryFile(relativePath)),
      ),
    ).toBe(true);

    for (const relativePath of [
      ".agents/skills/wtk-lean/scripts/workflow_route.py",
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
  });

  it("fails closed for unsupported and malformed Bun versions before a suite marker runs", () => {
    const versionSource = readRepositoryFile("tools/shared/src/bun-version.ts");

    runBunVersionSensor(versionSource.replace('"1.4.x"', '"9.x"'), "Bun.version");
    runBunVersionSensor(versionSource, JSON.stringify("not-a-version"));
  });
});
