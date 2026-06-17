---
name: br
description: Official skill for beads_rust (`br`), a local-first, dependency-aware issue tracker for AI agents. Use when creating issues, triaging backlogs, managing dependencies, finding ready work, updating status, or syncing to git via JSONL.
---

# br — Beads Rust Issue Tracker (Official Skill)

> **Non-invasive:** br NEVER runs git commands. Sync and commit are YOUR responsibility.

## Before You Start

Verify the tools are available:

```bash
which br      # Must be installed. If missing: cargo install beads_rust or brew install br
which bv      # Must be installed. If missing: see beads_viewer README for install
which python3 # Used for JSON parsing in resolution. Available on all modern systems.
```

**jq note:** Some commands use `jq` for quick field extraction. If `jq` is not installed, use `python3 -c "import json,sys; ..."` instead. Both work — prefer `jq` when available for readability.
## Critical Rules for Agents

| Rule | Why |
|------|-----|
| **Binary is `br`** | NEVER `bd` (that is the old Go version) |
| **ALWAYS use `--json`** | Structured output for parsing. `--format toon` for reduced tokens. |
| **NEVER run bare `bv`** | Blocks session in interactive TUI mode |
| **Sync is EXPLICIT** | `br sync --flush-only` exports DB to JSONL only |
| **Git is YOUR job** | br only touches `.beads/` — you must `git add .beads/ && git commit` |
| **No cycles allowed** | `br dep cycles --json` must return empty |
| **Resolve actor at runtime** | `ACTOR="${BR_ACTOR:-assistant}"` then pass `--actor "$ACTOR"` on all mutating commands |

## Resolving Short Bead IDs

Users often type short suffixes (`0ks`, `ag5`) instead of full bead IDs (`pi-feat-workflow-gate-0ks`). Resolve them:

```bash
# Step 1: Try br show first — works if it's already a full ID
FULL=$(br show "$SHORT" --json 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['id'])" 2>/dev/null)

# Step 2: If Step 1 failed, suffix-match against all beads
if [ -z "$FULL" ]; then
  FULL=$(br list --status open --status in_progress --status closed --json 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
issues = d if isinstance(d, list) else d.get('issues',[])
matches=[i['id'] for i in issues if i.get('id','').endswith('$SHORT')]
if len(matches)==1: print(matches[0])
elif len(matches)>1: print('AMBIGUOUS:'+','.join(matches))
")
fi

# If FULL is empty or starts with AMBIGUOUS, ask the user for the full ID
```

**Never guess.** If resolution is ambiguous, list the candidates and ask the user.
## Quick Workflow

```bash
ACTOR="${BR_ACTOR:-assistant}"

# 1. Find work
br ready --json

# 2. Pick and inspect
br show <id> --json

# 3. Claim it
br update --actor "$ACTOR" <id> --status in_progress --claim

# 4. Do the work...

# 5. Close with evidence
br close --actor "$ACTOR" <id> --reason "Implemented X in commit abc123"

# 6. Check queue impact
br ready --json && br blocked --json

# 7. Sync to git (EXPLICIT!)
br sync --flush-only
git add .beads/ && git commit -m "feat: X (<id>)"
git push
```

## Issue Lifecycle

```bash
ACTOR="${BR_ACTOR:-assistant}"

br init                                              # Initialize .beads/ workspace
br create --actor "$ACTOR" "Title" -p 1 -t task      # Create issue (priority 0-4)
br q --actor "$ACTOR" "Quick note"                   # Quick capture (outputs ID only)
br show <id> --json                                  # Issue details with dependencies
br update --actor "$ACTOR" <id> --status in_progress # Update status
br update --actor "$ACTOR" <id> --priority 0         # Change priority
br close --actor "$ACTOR" <id> --reason "Done"       # Close with reason
br close --actor "$ACTOR" <id1> <id2> --reason "..." # Close multiple at once
br reopen --actor "$ACTOR" <id>                      # Reopen closed issue
```

## Create Options

```bash
br create --actor "$ACTOR" "Title" \
  --priority 1 \             # 0-4 scale (0=critical, 4=backlog)
  --type feature \           # task, bug, feature, epic, question, docs
  --assignee "user@..." \    # Optional assignee
  --labels backend,auth \    # Comma-separated labels
  --description "..."        # Detailed description
```

## Update Options

```bash
br update --actor "$ACTOR" <id> \
  --title "New title" \
  --priority 0 \
  --status in_progress \     # open, in_progress, closed
  --assignee "new@..." \
  --add-label reliability \
  --parent <parent-id> \
  --claim                    # Shorthand for claim-and-start: --status in_progress + self-assign
```

### Bulk Update

```bash
br update --actor "$ACTOR" <id1> <id2> <id3> --priority 2 --add-label triage-reviewed --json
```

Use for batch triage — raising/lowering priority across a wave, adding labels in bulk.

## Querying (always use --json for agents)

```bash
br ready --json                              # Actionable work (no blockers) — THE starting query
br list --json                               # All issues
br list --status open --sort priority --json # Filter by status + sort
br list --status open --status in_progress --json  # Active work
br list --priority 0-1 --json                # Priority range filter
br list --assignee alice --json              # Filter by assignee
br blocked --json                            # Show blocked issues
br search "keyword" --json                   # Full-text search across title/description
br show <id> --json                          # Single issue with dependencies
br stale --days 30 --json                    # Issues untouched for N days
br count --by status --json                  # Count with grouping
br stats --json                              # Project statistics
```

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

## Output Formats

| Flag | Use case |
|------|----------|
| `--json` | **Default for agents** — full structured data |
| `--format toon` | Token-optimized alternative for context-window-sensitive agents |
| (no flag) | Human-readable terminal output with colors — do NOT use in agent context |

## Dependencies

```bash
br dep add <child> <parent>               # child depends on parent (child blocked until parent closes)
br dep add <id> <depends-on> --type blocks # Explicit block type
br dep remove <child> <parent>            # Remove dependency
br dep list <id> --json                   # Dependencies for an issue
br dep tree <id> --json                   # Full dependency tree
br dep cycles --json                      # Find circular deps — MUST be empty!
```

**Critical:** `br dep cycles --json` must return empty. Circular dependencies break the dependency graph and make `br ready` unreliable.

## Labels

```bash
br label add <id> backend auth            # Add multiple labels
br label remove <id> urgent               # Remove a label
br label list <id>                        # List issue's labels
br label list-all                         # All labels in project
```

## Comments

```bash
ACTOR="${BR_ACTOR:-assistant}"
br comments add --actor "$ACTOR" <id> --message "Triage note" --json
br comments list <id> --json
```

## Sync (EXPLICIT — never automatic)

```bash
br sync --flush-only                 # Export DB to JSONL → do this BEFORE git commit
br sync --import-only                # Import JSONL to DB → do this AFTER git pull
br sync --status                     # Check sync status
```

Workflow after making changes:
```bash
br sync --flush-only
git add .beads/ && git commit -m "Update issues"
```

Workflow after pulling:
```bash
git pull --rebase
br sync --import-only
```

## System and Diagnostics

```bash
br doctor                            # Full diagnostics
br stats --json                      # Project statistics
br config list                       # Show all configuration
br config get id.prefix              # Get specific value
br config set defaults.priority=1    # Set value
br where                             # Show workspace location
br version                           # Show version
br upgrade                           # Self-update (if enabled)
br lint --json                       # Lint issues for problems
```

## Triage Decision Matrix

During triage, classify each open issue into exactly one category:

| Classification | Action |
|---------------|--------|
| `implemented` | Close with evidence: commit SHA, PR URL, file path, or observed behavior |
| `out-of-scope` | Close with explicit boundary reason — what domain is this out of scope for? |
| `needs-clarification` | Comment with specific unanswered questions. Do NOT close. |
| `actionable` | Keep open. Correct status, priority, labels, and dependencies. |

**Never invent evidence for closure.** If you cannot point to a commit, file, or test that proves completion, comment instead.

**During large triage efforts, checkpoint every few updates:**
```bash
br ready --json    # Confirm the queue is still coherent
br blocked --json  # Confirm no new blockers emerged
```

## Agent Mail Coordination

Use bead ID as the coordination anchor for multi-agent work:

| Concept | Value |
|---------|-------|
| Mail `thread_id` | `bd-###` (the issue ID) |
| Mail subject | `[bd-###] ...` |
| File reservation `reason` | `bd-###` |
| Commit messages | Include `bd-###` for traceability |

```python
# 1. Reserve files for bead
file_reservation_paths(..., reason="bd-123")

# 2. Announce work in thread
send_message(..., thread_id="bd-123", subject="[bd-123] Starting...")

# 3. Do work...

# 4. Close bead and release
br close --actor "$ACTOR" bd-123 --reason "Completed"
release_file_reservations(...)
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

## Standard Agent Workflow (Full)

```bash
ACTOR="${BR_ACTOR:-assistant}"

# 1. Verify workspace
br where
br ready --json
br blocked --json
br list --status open --sort priority --json

# 2. Pick highest-priority ready work
br show <id> --json

# 3. Claim it
br update --actor "$ACTOR" <id> --status in_progress --claim

# 4. Do work...

# 5. Close with evidence
br close --actor "$ACTOR" <id> --reason "Implemented X in commit abc123"

# 6. Check queue impact
br ready --json
br blocked --json

# 7. Sync to git
br sync --flush-only
git add .beads/ && git commit -m "feat: X (<id>)"
git push
```

## Storage Layout

```
.beads/
  beads.db        # SQLite database (primary storage)
  beads.db-shm    # SQLite shared memory (WAL mode)
  beads.db-wal    # SQLite write-ahead log
  issues.jsonl    # JSONL export (for git version control)
  config.yaml     # Project configuration
  metadata.json   # Workspace metadata
```

## Troubleshooting

```bash
br doctor                    # Full diagnostics — run first
br dep cycles --json         # Must be empty
br config list               # Check settings
which br                     # Verify br is installed
```

**"Database locked":** Check for other `br` processes: `pgrep -f "br "`

**Worktree error** (`'main' is already checked out`):
```bash
git branch beads-sync main
br config set sync.branch beads-sync
```

**Verbose debugging:**
```bash
br -v list                   # Verbose
br -vv list                  # Debug
RUST_LOG=debug br list       # Detailed trace logs
```

## Anti-Patterns

- Running `br sync` without `--flush-only` or `--import-only`
- Forgetting sync before git commit
- Creating circular dependencies
- Running bare `bv` (blocks session)
- Assuming auto-commit behavior (br NEVER auto-commits)
- **Inventing evidence for closure** — if unsure, comment instead
- Modifying unrelated issues during triage
- Adding speculative dependencies without confirmed blocking relationship

## Process

1. **Inspect before mutating.**
   - `br ready --json` to find unblocked work.
   - `br show <id> --json` for full context on a single bead.
   - `br list --status open --status in_progress --json` to see all active work.
2. **Mutate state explicitly.**
   - Claim: `br update --actor "$ACTOR" <id> --status in_progress --claim`
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
- Confirm `br sync --status` shows clean state before committing.
