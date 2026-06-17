---
description: "Prepare a pull-request summary from bead artifacts, verification evidence, and review findings."
argument-hint: "<bead-id>"
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:
1. `.beads/artifacts/$ARGUMENTS/review-report.md` exists with verdict `approved`.
2. All verification checks pass (no `failedChecks` without resolution).
3. `git diff` shows changes to propose.

If no review: STOP. Tell the user: "Run /review first — no review report for $ARGUMENTS."
If review has `changes-requested` or `blocked`: STOP. Tell the user: "Review found issues — address before PR."
Do NOT proceed. Do NOT "helpfully" skip ahead.

Prepare the PR package for the active bead.

## Phase 1: Gather Context

```bash
br show "$ARGUMENTS" --json                    # Bead details
git diff --stat                              # Changed files summary
```

Read all artifacts: `prd.md`, `plan.md`, `completion-evidence.json`, `review-report.md`.

## Phase 2: Summarize

Produce concise reviewer-facing output:

1. **What changed** — files + high-level description (2-3 sentences)
2. **Why** — link to PRD problem statement
3. **How verified** — key checks from evidence (list passing checks)
4. **Residual risks** — from review findings

## Phase 3: Create PR

Use `gh pr create` with the summary:

```bash
gh pr create \
  --title "<bead-id>: <short description>" \
  --body "<summary from Phase 2>" \
  --base main
```

## Phase 4: Report

```
PR: <url>
Bead: $ARGUMENTS
Verification: <N>/<N> checks passed
Review: <verdict> (<N> findings)
Residual risks: <N>
Next: /close $ARGUMENTS (after merge)
```
