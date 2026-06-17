---
name: beads-pr
description: Prepare a pull-request summary from bead artifacts, verification evidence, and review findings.
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:

1. `.beads/artifacts/$1/review-report.md` exists with verdict `approved`.
2. All verification checks pass (no `failedChecks` without resolution).
3. `git diff` shows changes to propose.

If no review: STOP. Tell the user: "Run /review first — no review report for $1."
If review has `changes-requested` or `blocked`: STOP. Tell the user: "Review found issues — address before PR."
If no bead id provided: STOP. Ask: "Which bead? Provide the bead id."
Do NOT proceed. Do NOT "helpfully" skip ahead.

Prepare the PR package for the active bead.

User input: $ARGUMENTS

## Requirements

1. **Read all artifacts**: `prd.md`, `plan.md`, `completion-evidence.json`, `review-report.md`.
2. **Summarize**:
   - What changed (files + high-level description)
   - Why it changed (link to PRD problem statement)
   - How it was verified (key checks from evidence)
   - What remains risky (from review residual risks)
3. **Produce concise reviewer-facing output.** No implementation details unless they're surprising.
4. **Do not invent checks or findings** that were not recorded in evidence or review.
5. **End with**: the PR summary, suggested reviewers (if applicable), and the next command: `/close $1`.
