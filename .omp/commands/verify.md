---
description: "Test + evidence. Graph-informed — checks completeness against impact, file history, and downstream effects."
argument-hint: "<bead-id>"
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:
1. Bead $ARGUMENTS is claimed or in_progress: `br show "$ARGUMENTS" --json` — status must be `in_progress` or have changes to verify.
2. `.beads/artifacts/$ARGUMENTS/plan.md` exists — the verification section specifies what to check.

If bead not started: STOP. Tell the user: "Run /ship first — bead not in progress."
If plan missing: STOP. Tell the user: "Run /plan first — no verification plan exists."
Do NOT proceed. Do NOT "helpfully" skip ahead.

You are verifying bead $ARGUMENTS. Use the graph to check completeness.

## Phase 1: Graph Context

```bash
bv --robot-triage --format json              # Is this bead still relevant?
bv --robot-alerts --format json              # Any alerts on this bead?
br show "$ARGUMENTS" --json                    # Bead details
```

## Phase 2: File Coverage

Check that all expected files were actually changed:

```bash
git diff --name-only HEAD~1                  # Actual changed files
```

Compare against the plan's blast radius. If blast radius includes files not changed, verify they were intentionally skipped.

## Phase 3: Run Verification

Read the plan's verification section: `.beads/artifacts/$ARGUMENTS/plan.md` → Full Verification.

Run only the checks that prove the changed behavior:
- Feature: run the project's test suite (`npm test`, `cargo test`, `pytest`)
- Bugfix: reproduce the original symptom — it should now pass
- Task/chore: build succeeds, lint clean

Run the actual commands. Do not claim pass without output.

```bash
br lint "$ARGUMENTS" --json                    # Lint the bead
bv --robot-suggest --format json             # Hygiene check
```

## Phase 4: Write Completion Evidence

Write `.beads/artifacts/$ARGUMENTS/completion-evidence.json` using `.omp/templates/completion-evidence.json` as the shape:

```json
{
  "beadId": "$ARGUMENTS",
  "status": "verified",
  "summary": "<one-line verdict>",
  "passedChecks": [{"command": "<cmd>", "expected": "<expected>", "result": "<actual>"}],
  "failedChecks": [{"command": "<cmd>", "expected": "<expected>", "result": "<actual>"}],
  "uncheckedRisks": ["<risk from plan not covered>"],
  "artifacts": [{"path": "<path>", "purpose": "<why>"}]
}
```

Separate passed, failed, and unchecked. Be honest.

## Phase 5: Report

```
Bead: $ARGUMENTS | Status: VERIFIED/FAILED
Checks passed: <N>/<N> | Failed: <N>
Evidence: .beads/artifacts/$ARGUMENTS/completion-evidence.json
Next: /review $ARGUMENTS (if verified) or fix issues (if failed)
```
