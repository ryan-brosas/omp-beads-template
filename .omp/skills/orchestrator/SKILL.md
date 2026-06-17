---
name: orchestrator
description: Route the current request to the correct beads phase and keep the workflow moving without skipping prerequisites.
---

# orchestrator

## Goal

Keep the session in the right beads phase.

## Routing rules

- No bead yet or idea still fuzzy: brainstorm.
- Work item chosen but not formalized: create.
- PRD exists but implementation path is unclear: plan.
- PRD and plan exist and code must change: ship.
- Code changed and behavior must be proven: verify.
- Verification complete and risk must be assessed: review.
- Review complete and change must be summarized upstream: pr or close.

## Operating rules

- Do not skip create or plan.
- Use br for state and bv for context before acting.
- Prefer the namespaced commands over ad-hoc prompting when the user clearly wants a workflow phase.
- If the current phase is blocked, state the missing artifact or decision and move to the prerequisite.
