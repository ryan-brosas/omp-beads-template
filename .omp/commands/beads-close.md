---
name: beads-close
description: Close the active bead only after evidence exists and the remaining follow-ups are explicit.
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:

1. `.beads/artifacts/$1/completion-evidence.json` exists with passing verification.
2. `.beads/artifacts/$1/review-report.md` exists with `ready_for_close: true` or verdict `approved`.

If no evidence: STOP. Tell the user: "Run /verify first — no completion evidence for $1."
If no review: STOP. Tell the user: "Run /review first — no review report for $1."
If review found unresolved issues: STOP. List the unresolved findings. "Address these before closing."
If no bead id provided: STOP. Ask: "Which bead? Provide the bead id."
Do NOT proceed. Do NOT "helpfully" skip ahead.

Close the active bead.

User input: $ARGUMENTS

## Requirements

1. **Read the review report** before closing — confirm no unresolved findings.
2. **Close through br**:
   ```bash
   ACTOR="${BR_ACTOR:-assistant}"
   br close --actor "$ACTOR" $1 --reason "Completed. See .beads/artifacts/$1/ for evidence."
   ```
3. **Summarize final status**: what was built, verification results, explicit follow-ups.
4. **Sync bead state**:
   ```bash
   br sync --flush-only
   git add .beads/ && git commit -m "close: $1"
   ```
5. **If evidence is missing or review found unresolved issues**, STOP and say exactly why closure is blocked.
6. **End with**: closed bead id, one-line summary, explicit follow-ups as new bead suggestions.
