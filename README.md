# OMP Beads Template

OMP-native project template with **br** and **bv** as the backbone of planning, execution, verification, and review.

## What you get

- `.omp/` — skills, commands, agents, extensions, and templates for the beads workflow
- `.beads/` — bead state directory (br database, artifact storage)
- Workflow gate — blocks implementation edits until PRD and plan exist
- Nine slash commands covering the full bead lifecycle
- Review agents (correctness, performance, security)

## Quickstart

```bash
# 1. Clone to start a new project
git clone https://github.com/ryan-brosas/omp-beads-template.git my-project
cd my-project

# 2. Initialize bead tracking
omp
/beads-init

# 3. Start working
/beads-brainstorm
/beads-create
/beads-plan
/beads-ship
/beads-verify
/beads-review
/beads-pr
/beads-close
```

That's it. Open `omp` in the project directory and the template is active.

## Workflow

| Phase | Command | What happens |
|---|---|---|
| Init | `/beads-init` | Seeds bead tracking database |
| Brainstorm | `/beads-brainstorm` | Understand repo state and candidate work with bv |
| Create | `/beads-create` | Select or create a bead; write `prd.md` |
| Plan | `/beads-plan` | Write `plan.md` with blast radius, risks, verification |
| Ship | `/beads-ship` | Implement only the active bead |
| Verify | `/beads-verify` | Run targeted checks; record evidence |
| Review | `/beads-review` | Inspect diff and risks; write review report |
| PR | `/beads-pr` | Open pull request with summary |
| Close | `/beads-close` | Close bead once evidence exists |

## Escape hatch

```bash
export OMP_SKIP_BEADS_WORKFLOW=1
```

Skips the workflow gate for emergencies or template bootstrap work.

## Artifact layout

```
.beads/artifacts/<bead-id>/
  prd.md
  plan.md
  completion-evidence.json
  review-report.md
```
