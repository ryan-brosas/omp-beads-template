---
name: br
description: Use br as the source of truth for bead state, ownership, and artifact location. br is the beads_rust CLI — local-first, dependency-aware issue tracker backed by SQLite + JSONL.
---

# br — Beads Rust Issue Tracker

> **Non-invasive:** br NEVER runs git commands. Sync and commit are YOUR responsibility.

## Critical Rules

| Rule | Why |
|------|-----|
| **Binary is `br`** | NEVER `bd` (that is the old Go version) |
| **ALWAYS use `--json`** | Structured output for parsing. Without it you get colored terminal text. |
| **Resolve actor at runtime** | Use `ACTOR="${BR_ACTOR:-assistant}"` and pass `--actor "$ACTOR"` on all mutating commands |
| **Sync is EXPLICIT** | `br sync --flush-only` exports DB to JSONL only. You must `git add .beads/ && git commit` |
| **Git is YOUR job** | br only touches `.beads/` — it never commits, pushes, or pulls |
| **No cycles allowed** | `br dep cycles` must return empty. Circular dependencies break `br ready` |
| **NEVER run bare `bv`** | Always use `bv --robot-*` flags. Bare `bv` launches an interactive TUI that blocks the session |

## When to use

- You need to inspect, create, claim, update, or close a bead.
- You need the canonical bead id before writing workflow artifacts.
- You need to understand current status before implementation or review.

## When not to use

- You only need code intelligence inside the repository. Use OMP tools first.
- You are guessing bead state from filenames or memory. Inspect br instead.

## Actor Resolution

All mutating commands need an actor. Set once per session:

```bash
ACTOR="${BR_ACTOR:-assistant}"
```

Then pass `--actor "$ACTOR"` on every `create`, `update`, `close`, `reopen`, `comment` command.

## Priority Scale

| Priority | Meaning | Use numbers, not words |
|----------|---------|------------------------|
| 0 | Critical | Immediate action required |
| 1 | High | Important, do soon |
| 2 | Medium (default) | Normal priority |
| 3 | Low | When time permits |
| 4 | Backlog | Future consideration |

## Issue Types

`task`, `bug`, `feature`, `epic`, `question`, `docs`

## Essential Commands

### Finding work

```bash
br ready --json                              # Actionable work (no blockers)
br list --status open --sort priority --json # All open, sorted
br list --status open --status in_progress --json  # Active work
br blocked --json                            # Blocked issues
br show <id> --json                          # Single issue with dependencies
```

### Lifecycle

```bash
ACTOR="${BR_ACTOR:-assistant}"

br init                                              # Initialize .beads/ workspace
br create --actor "$ACTOR" "Title" -p 1 -t task      # Create issue
br q --actor "$ACTOR" "Quick note"                   # Quick capture (outputs ID only)
br update --actor "$ACTOR" <id> --status in_progress --claim  # Claim and start
br update --actor "$ACTOR" <id> --priority 0         # Change priority
br close --actor "$ACTOR" <id> --reason "Done"       # Close with reason
br close --actor "$ACTOR" <id1> <id2> --reason "..."  # Close multiple
br reopen --actor "$ACTOR" <id> --reason "Reopening" # Reopen closed issue
```

### Create with full options

```bash
br create --actor "$ACTOR" "Title" \
  --priority 1 \
  --type feature \
  --assignee "user@..." \
  --labels backend,auth \
  --description "Longer description here"
```

### Dependencies

```bash
br dep add <child> <parent>               # child depends on parent (child blocked until parent closes)
br dep add <id> <depends-on> --type blocks # Explicit block type
br dep remove <child> <parent>            # Remove dependency
br dep list <id> --json                   # Dependencies for an issue
br dep tree <id> --json                   # Full dependency tree
br dep cycles --json                      # Find circular deps (MUST be empty!)
```

### Labels

```bash
br label add <id> backend auth            # Add multiple labels
br label remove <id> urgent               # Remove a label
br label list <id>                        # List issue's labels
br label list-all                         # All labels in project
```

### Comments

```bash
br comments add --actor "$ACTOR" <id> --message "Triage note" --json
br comments list <id> --json
```

### Querying

```bash
br list --json                              # All issues
br list --status open --sort priority --json  # Filter and sort
br list --priority 0-1 --json               # Priority range
br list --assignee alice --json             # By assignee
br search "keyword" --json                  # Full-text search
br stale --days 30 --json                   # Stale issues
br count --by status --json                 # Count with grouping
br stats --json                             # Project statistics
br lint --json                              # Lint for problems
```

## Sync Workflow

Mutations auto-flush JSONL by default. Run a final export check before committing:

```bash
# After making changes
br sync --flush-only
git add .beads/ && git commit -m "Update issues"

# After pulling remote changes
git pull --rebase
br sync --import-only
```

## Session Ending Pattern

Before ending any work session:

```bash
git pull --rebase
br sync --flush-only
git add .beads/ && git commit -m "Update issues"
git push
git status  # MUST show "up to date with origin"
```

## Output Formats

| Flag | Use case |
|------|----------|
| `--json` | **Default for agents** — full structured data |
| `--format toon` | Token-optimized alternative for context-window-sensitive agents |
| (no flag) | Human-readable terminal output — do NOT use in agent context |

## Diagnostics

```bash
br doctor                            # Full diagnostics
br where                             # Show workspace location
br version                           # Show version
br config list                       # Show all configuration
```

## Process

1. **Inspect before mutating.**
   - `br show <id> --json` for a single bead.
   - `br list --status open --status in_progress --json` to find active work.
   - `br ready --json` to find unblocked work.
2. **Mutate state explicitly.**
   - Claim: `br update --actor "$ACTOR" <id> --claim`
   - Status/metadata: `br update --actor "$ACTOR" <id> --status in_progress`
   - Close only after verification evidence exists: `br close --actor "$ACTOR" <id> --reason "..." --json`
3. **Write artifacts under `.beads/artifacts/<bead-id>/`.**
4. **Keep one active bead in focus** unless the user asks for triage across many beads.
5. **Sync after meaningful state changes.**
   - `br sync --flush-only` → `git add .beads/ && git commit`

## Minimum Checks

- Confirm the bead id with `br show <id> --json`.
- Confirm current status — is it `open`, `in_progress`, or `closed`?
- Confirm the artifact directory matches the bead id.
- Confirm `prd.md` exists before planning.
- Confirm `plan.md` exists before implementation.
- Confirm `br dep cycles --json` returns empty.
