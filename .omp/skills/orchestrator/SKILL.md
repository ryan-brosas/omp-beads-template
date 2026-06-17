---
name: orchestrator
description: Strict workflow recipe. Run each prompt in sequence. No skipping. No deciding.
---

# orchestrator

## The Sequence

Follow this sequence. Run each prompt in FULL. Do not skip phases.

| Step | Command | Produces | Gate |
|------|---------|----------|------|
| 1 | `/brainstorm [topic]` | Candidate work items | User confirms direction |
| 2 | `/create [description]` | `prd.md`, `prd.json`, `decisions.md` | All sections filled, no placeholders |
| 3 | `/plan <bead-id>` | `plan.md`, `tasks.md`, `context-capsule.md` | Observable truths defined, verification plan exists |
| 4 | `/ship <bead-id>` | Working code, `progress.txt` | Plan verification gates pass per wave |
| 5 | `/verify <bead-id>` | `completion-evidence.json` | All checks pass |
| 6 | `/review <bead-id>` | `review-report.md` | Verdict: approved |
| 7 | `/pr <bead-id>` | PR summary | — |
| 8 | `/close <bead-id>` | Closed bead, synced JSONL | Evidence + review exist |

## Rules

- **Run each prompt in FULL.** Every section, every step. Do not abbreviate.
- **Do not skip phases.** Brainstorm before create, create before plan, plan before ship.
- **Do not "helpfully" proceed if the prompt says STOP.** If blocked, run the prerequisite prompt.
- **The workflow-gate extension enforces this.** It blocks `edit`/`write` until PRD and plan exist. Don't fight it.
- **If the user says "just do X"**, route them to the right phase. "That's a /ship step — let's /plan first."
- **If a phase fails verification**, stay in that phase. Do not advance until the gate clears.

## Routing

- No bead yet or idea still fuzzy → `/brainstorm`
- Work item chosen but not formalized → `/create`
- PRD exists but implementation path is unclear → `/plan`
- PRD and plan exist and code must change → `/ship`
- Code changed and behavior must be proven → `/verify`
- Verification complete and risk must be assessed → `/review`
- Review complete and change must be summarized upstream → `/pr`
- PR merged/reviewed and bead must be finalized → `/close`

## Artifacts Per Phase

| Phase | Artifacts |
|-------|-----------|
| `/create` | `prd.md`, `prd.json`, `decisions.md` |
| `/plan` | `plan.md`, `tasks.md`, `context-capsule.md` |
| `/ship` | Implementation changes, `progress.txt` |
| `/verify` | `completion-evidence.json` |
| `/review` | `review-report.md` |
| `/pr` | PR summary (terminal output) |
| `/close` | Closed bead in br, synced JSONL |
