---
name: beads-brainstorm
description: Use bv and current bead state to surface the next best work items before formalizing one.
---

## Prerequisites (CHECK FIRST)

None. This is the entry point. If the user provided no input, ask: "What area or problem are we exploring?"

Brainstorm candidate work using the beads workflow.

User input: $ARGUMENTS

## Requirements

1. **Run `bv --robot-triage --format json`**. This is non-negotiable — it returns `quick_ref`, `recommendations`, `quick_wins`, `blockers_to_clear`, and `project_health` in one call.
2. **Run `br list --status open --status in_progress --json`**. Cross-reference with bv output to avoid duplicates.
3. **Do not implement code.** This is read-only exploration.
4. **Produce concrete candidate beads** with a short description and priority for each.
5. **If one candidate is clearly best**, say why — score, unblock impact, urgency.
6. **If a bead already exists for the request**, point to it instead of inventing a duplicate.
7. **End with a recommendation**: which bead to create, or whether to `/create` next.

## Output

A concise triage summary: top 3-5 candidates, existing related work, recommended next action. No files written.
