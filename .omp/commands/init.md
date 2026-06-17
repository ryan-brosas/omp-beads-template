---
description: "Initialize or inspect the beads workflow backbone for this repository."
argument-hint: "[optional: bead prefix]"
---

## Prerequisites

None. This command bootstraps the workflow itself.

Initialize the repository for the beads workflow.

## Phase 1: Detect State

```bash
br where 2>/dev/null && echo "INITIALIZED" || echo "NEEDS_INIT"
```

If already initialized, report current state and skip to Phase 4.

## Phase 2: Initialize br

```bash
br init ${ARGUMENTS:+--prefix "$ARGUMENTS"}
```

Uses a sensible prefix derived from the repo name. Pass a prefix as `$ARGUMENTS` to override.

## Phase 3: Verify Backbone

Check that these directories exist:
- `.omp/commands/`, `.omp/skills/`, `.omp/templates/`, `.omp/agents/`, `.omp/extensions/`
- `.beads/artifacts/` (create with `.gitkeep` if missing)

Confirm `.omp/scripts/resolve-bead.sh` is executable.

## Phase 4: Check Agent Files

Verify these are present and current:
- `.omp/AGENTS.md` — the main agent context file
- `.omp/RULES.md` — the 4 rules
- `.omp/memory/project/*.md` — project conventions, tech-stack, decisions, gotchas

## Phase 5: Report

```
Workspace: <path from br where>
br version: <br version>
Bead prefix: <prefix>
Beads: <N open, M closed>
Backbone: .omp/ <healthy/missing>
Next: /brainstorm
```
