---
name: beads-close
description: Close the active bead only after evidence exists and the remaining follow-ups are explicit.
---

Close the active bead.

User input: $ARGUMENTS

Requirements:
- Confirm `completion-evidence.json` exists.
- Read the review report before closing.
- Summarize final status and explicit follow-ups.
- Close the bead through br only when evidence supports it.
- If evidence is missing or review found unresolved issues, stop and say exactly why closure is blocked.
