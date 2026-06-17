---
name: beads-ship
description: Implement the active bead only after PRD and plan exist.
---

Ship the active bead.

User input: $ARGUMENTS

Requirements:
- Confirm the active bead.
- Refuse to skip `prd.md` or `plan.md`.
- Use bv and repository discovery to scope the implementation before editing.
- Keep changes limited to the current bead.
- Update artifacts if the plan changes materially.
- End with what changed, what remains risky, and which verification command should run next.
