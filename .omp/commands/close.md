---
description: "Close the active bead only after evidence exists and the remaining follow-ups are explicit."
argument-hint: "<bead-id>"
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:
1. `.beads/artifacts/$ARGUMENTS/completion-evidence.json` exists with passing verification.
2. `.beads/artifacts/$ARGUMENTS/review-report.md` exists with `ready_for_close: true` or verdict `approved`.

If no evidence: STOP. Tell the user: "Run /verify first — no completion evidence for $ARGUMENTS."
If no review: STOP. Tell the user: "Run /review first — no review report for $ARGUMENTS."
If review found unresolved issues: STOP. List the unresolved findings. "Address these before closing."
Do NOT proceed. Do NOT "helpfully" skip ahead.

Close the active bead.

## Phase 1: Read Review

Read `.beads/artifacts/$ARGUMENTS/review-report.md`. Confirm:
- No unresolved findings (severity `critical` or `high` must be addressed)
- `ready_for_close` is `true`
- Residual risks are documented and accepted

## Phase 2: Close

```bash
ACTOR="${BR_ACTOR:-assistant}"
br close --actor "$ACTOR" "$ARGUMENTS" --reason "Completed. See .beads/artifacts/$ARGUMENTS/ for evidence." --json
```

## Phase 3: Check Queue Impact

```bash
br ready --json                              # Newly unblocked work
br blocked --json                            # Confirm no new blockers
```

## Phase 4: Sync

```bash
br sync --flush-only
git add .beads/ && git commit -m "close: $ARGUMENTS"
```

## Phase 5: Session End

```bash
git pull --rebase
br sync --flush-only
git add .beads/ && git commit -m "Update issues"
git push
git status  # MUST show "up to date with origin"
```

## Phase 6: Report

```
Closed: $ARGUMENTS
Summary: <one-line summary of what was built>
Evidence: .beads/artifacts/$ARGUMENTS/
Unblocks: <list of newly actionable beads, or "None">
Follow-ups: <suggested new beads for residual work, or "None">
```
