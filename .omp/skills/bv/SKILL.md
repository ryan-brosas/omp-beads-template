---
name: bv
description: Use bv before action to get graph-informed triage, impact analysis, and review context. bv is beads_viewer — a graph-aware TUI with a robot-mode JSON API for agents.
---

# bv — Beads Viewer (Robot Mode)

> **CRITICAL: NEVER run bare `bv`.** It launches an interactive TUI that blocks your session. Always use `--robot-*` flags.

## When to use

- You are about to brainstorm, plan, ship, verify, or review.
- You need file hotspots, related work, blast radius, or blockers.
- You need a graph-informed view before choosing the next bead.

## When not to use

- You already have the exact file, symbol, or callsite. Use OMP discovery tools directly.
- You want to skip inspection and jump to editing. Run bv first when the phase depends on context.

## Robot Mode: The Agent Interface

All robot commands output JSON to stdout, diagnostics to stderr, exit 0 on success. Add `--format toon` for token-optimized output.

### Primary entry points

| Command | Returns | When to use |
|---------|---------|-------------|
| `bv --robot-triage --format json` | `quick_ref`, `recommendations`, `quick_wins`, `blockers_to_clear`, `project_health`, copy-paste `commands` | **Every `/brainstorm`** — single-call mega-command |
| `bv --robot-next --format json` | Single top pick + claim command | Quick "what should I do now?" |
| `bv --robot-plan --format json` | `plan.summary.highest_impact`, parallel tracks with `unblocks` lists | **Every `/plan`** — feeds wave structure |

### Triage output structure

`bv --robot-triage` returns:

- **`quick_ref`**: open/blocked/in_progress/actionable counts, top 3 picks by score
- **`recommendations`**: ranked actionable items, each with `score`, `reason`, `unblock_info`
- **`quick_wins`**: low-effort high-impact items
- **`blockers_to_clear`**: items that unblock the most downstream work
- **`project_health`**: status/type/priority distributions, graph metrics (cycles, density)
- **`commands`**: copy-paste shell commands for next steps (claim, show, etc)

### Count semantics

| Field | Meaning |
|-------|---------|
| `open_count` | Status exactly `open` |
| `blocked_count` | Status exactly `blocked` |
| `in_progress_count` | Status exactly `in_progress` |
| `actionable_count` | Non-closed, no open blocking dependencies (ready to work) |
| `not_actionable_count` | Non-closed, blocked by open dependencies |
| `not_closed_count` | `open` + `in_progress` + `blocked` + `deferred` |

Partition invariant: `not_closed == actionable + not_actionable`

### Planning output structure

`bv --robot-plan` returns:

- **`plan.summary`**: `highest_impact` (best unblock target), `total_work_items`, `parallel_tracks`
- **`plan.tracks[]`**: each track has `items[]`, `unblocks` (what this track enables), `estimated_effort`
- Use `unblocks` to structure plan waves — items in the same track can run in parallel

### Recipe system

Pre-filter before analysis:

```bash
bv --recipe actionable --robot-plan --format json     # Only ready-to-work items
bv --recipe high-impact --robot-triage --format json   # Top PageRank scores
```

### Other robot commands

**Impact & Risk:**
| Command | Returns |
|---------|---------|
| `bv --robot-insights --format json` | Full metrics: PageRank, betweenness, HITS, eigenvector, critical path, cycles, k-core, articulation points, slack |
| `bv --robot-priority --format json` | Priority misalignment detection with confidence |
| `bv --robot-alerts --format json` | Stale issues, blocking cascades, priority mismatches |
| `bv --robot-suggest --format json` | Hygiene: duplicates, missing deps, label suggestions, cycle breaks |

**Files:**
| Command | Returns |
|---------|---------|
| `bv --robot-file-hotspots --format json` | Files with most bead activity |
| `bv --robot-file-beads <path> --format json` | Beads touching a specific file |
| `bv --robot-file-relations --format json` | File co-change patterns |

**History:**
| Command | Returns |
|---------|---------|
| `bv --robot-history --format json` | Bead-to-commit correlations |
| `bv --robot-diff --diff-since <ref> --format json` | Changes since a git ref |

**Graph:**
| Command | Returns |
|---------|---------|
| `bv --robot-graph --graph-format json` | Full dependency graph |
| `bv --robot-forecast <id\|all> --format json` | ETA predictions with dependency-aware scheduling |

### Two-phase analysis

- **Phase 1 (instant):** degree, topo sort, density — always available
- **Phase 2 (async, 500ms timeout):** PageRank, betweenness, HITS, eigenvector, cycles — check `status` flags (`computed`, `approx`, `timeout`, `skipped`)

For large graphs (>500 nodes), some metrics may be approximated or skipped. Always check `status`.

### jq quick reference

```bash
bv --robot-triage | jq '.quick_ref'                      # At-a-glance summary
bv --robot-triage | jq '.recommendations[0]'              # Top recommendation
bv --robot-triage | jq '.blockers_to_clear[0]'            # Best unblock target
bv --robot-plan | jq '.plan.summary.highest_impact'       # Best unblock target for planning
bv --robot-plan | jq '.plan.tracks[] | {items, unblocks}' # Parallel tracks
bv --robot-insights | jq '.Cycles'                        # Circular deps (must be empty!)
bv --robot-insights | jq '.status'                        # Check metric readiness
```

## Process

1. **Start each phase with the smallest bv query** that answers the decision in front of you.
   - `/brainstorm` → `bv --robot-triage --format json`
   - `/plan` → `bv --robot-plan --format json`
   - `/review` → `bv --robot-file-hotspots --format json` + `bv --robot-related --format json`
2. **Capture the concrete result** that changes the plan: files, risks, dependencies, or missing work.
3. **Use that result to scope edits, checks, or review.**
4. **Re-run bv when the phase changes or the blast radius grows.**

## Anti-patterns

- Running bare `bv` — blocks the session.
- Running the whole robot suite every time — pick the smallest query.
- Treating bv output as proof without checking the underlying files.
- Using bv as a substitute for verification after implementation.
- Ignoring `status` flags — a metric marked `timeout` or `skipped` is not trustworthy.
