# Task 02: Continue Jev fallback safely

- Objective: close C5-C7 for typed pre-action timeouts, unsafe/ambiguous failures, redaction, and oracle-owned verdicts.
- S1 is committed at `7ef7175b101c2eb745edf6089038d2be8d66cfd9`; C1-C4 are green.
- Keep failure classification tied to the phase boundary: only a `TimeoutError` from Agent construction proves no product action began; any error after `Agent.run()` starts forbids automatic replay.
- C5-C7 and `IT-028` pass. Failure metadata is bounded to class, eligibility, next adapter, and action state; evidence retains no exception text.
- Offline suites passed: 9 Jev adapter, 38 QA-skill, 64 Python config, 9 Bun config, and 78 installer packet/terminal tests. No live provider or browser was used.
- Preserve the uncommitted QA scenario/journey updates. Leave `.specs/features/default-jev-qa/workflow.json` untouched; it is a checkout-local resolver snapshot.
