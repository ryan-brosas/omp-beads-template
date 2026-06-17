---
name: beads-verify
description: Run targeted verification for the active bead and record the evidence.
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:

1. Bead $1 is claimed or in_progress: `br show $1 --json` — status must be `in_progress` or the bead must have changes to verify.
2. `.beads/artifacts/$1/plan.md` exists — the verification section specifies what to check.

If bead not started: STOP. Tell the user: "Run /ship first — bead not in progress."
If plan missing: STOP. Tell the user: "Run /plan first — no verification plan exists."
If no bead id provided: STOP. Ask: "Which bead? Provide the bead id."
Do NOT proceed. Do NOT "helpfully" skip ahead.

Verify the active bead.

User input: $ARGUMENTS

## Requirements

1. **Read the plan's verification section** — `.beads/artifacts/$1/plan.md` → Full Verification.
2. **Run only the checks that prove the changed behavior.** Do not run unrelated test suites.
3. **Record results** in `.beads/artifacts/$1/completion-evidence.json` using `.omp/templates/completion-evidence.json` as the shape:
   - `passedChecks`: array of `{ command, result }` for passing checks
   - `failedChecks`: array of `{ command, result }` for failing checks
   - `uncheckedRisks`: risks from the plan that were not verified
   - `summary`: one-line verdict
4. **Separate passed, failed, and unchecked.** Be honest.
5. **If verification is partial**, say exactly what remains and why.
6. **Do not claim completion without evidence.**
7. **End with**: pass/fail counts, any failures that need addressing, and the next command: `/review $1` (if all pass) or "fix failures and re-run /verify."
