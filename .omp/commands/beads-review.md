---
name: beads-review
description: Review the active bead after verification using bv context plus direct file inspection.
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:

1. `.beads/artifacts/$1/completion-evidence.json` exists and has verification results.
2. `git diff HEAD~1` (or appropriate base) shows changes to review.

If no evidence: STOP. Tell the user: "Run /verify first — no verification evidence for $1."
If no changes: STOP. Tell the user: "No changes to review. Run /ship first."
If no bead id provided: STOP. Ask: "Which bead? Provide the bead id."
Do NOT proceed. Do NOT "helpfully" skip ahead.

Review the active bead.

User input: $ARGUMENTS

## Requirements

1. **Read the verification evidence** — `completion-evidence.json`.
2. **Run bv for review context**:
   ```bash
   bv --robot-file-hotspots --format json
   bv --robot-related --format json
   ```
3. **Read the changed files directly.** Do not rely only on summaries or diffs.
4. **Check spec↔code adherence**: does the implementation match the PRD requirements and plan tasks?
5. **Write** `.beads/artifacts/$1/review-report.md` using `.omp/templates/review-report.md` as the shape:
   - `verdict`: approved | changes-requested | blocked
   - `findings[]`: severity, file, issue, recommendation
   - `residual_risks[]`: risks not covered by verification
   - `ready_for_close`: boolean
6. **Call out findings, residual risks, and whether the bead is ready for PR or close.**
7. **End with**: verdict, finding count, and the next command: `/pr $1` (if approved) or "address findings and re-run /review."
