# Plan: {bead-id}

**Goal:** {One sentence — what does "done" look like?}

## Graph Context

- **Blast radius:** {N files} ({M new, O edits, P deletes})
- **Unblocks:** {bead-ids this enables, or "None"}
- **Blocked by:** {bead-ids this depends on, or "None"}
- **Critical path:** {Yes|No — does this block other work?}
- **Forecast:** {minutes} (confidence {0.0-1.0})
- **Hotspots touched:** {Files with >3 bead history, or "None"}

## Observable Truths

{Numbered list of concrete, verifiable statements. Each one must be falsifiable — you can look at the result and say "yes this is true" or "no it isn't."}

1. {Observable truth — e.g. "resolve-bead.sh 0ks returns pi-feat-workflow-gate-0ks"}
2. {Observable truth}

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| {File name} | {What it delivers} | `{path}` | {Need|Have} |

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | {task IDs} | {Yes|No} | {What must be done first} | {How to verify this wave} |
| 2 | {task IDs} | {Yes|No} | {What must be done first} | {How to verify this wave} |

## Tasks

### Wave 1: {Wave name}

**Task 1.1: {Task name}**

{2-3 sentence description of what to build. Include key design decisions.}

```
{Code outline or pseudocode — NOT implementation, just the shape}
```

**Verification:** {How to verify this task independently}

### Wave 2: {Wave name} {parallel}

**Task 2.1: {Task name}**

{Description. These tasks can run in parallel — no dependencies between them.}

**Verification:** {How to verify}

## Full Verification

```bash
# Commands that prove the implementation works end-to-end
{command}  # Expected: {output}
{command}  # Expected: {output}
```
