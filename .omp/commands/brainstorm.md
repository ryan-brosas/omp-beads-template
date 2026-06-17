---
description: "Ideation. Graph-informed — uses bv triage, suggest, priority, and label analysis to find high-impact work."
argument-hint: "<topic or problem to brainstorm>"
---

## Prerequisites

None. This is the entry point.

You are brainstorming work. Use the project graph to inform ideation — don't brainstorm in a vacuum.

## Phase 1: Graph Context

```bash
bv --robot-triage --format json              # Project state: open, blocked, in progress
bv --robot-suggest --format json             # Hygiene: duplicates, missing deps, cycle warnings
bv --robot-priority --format json            # Priority misalignment: graph importance vs assigned
bv --robot-label-attention --format json     # Labels needing focus (stale, high-impact)
bv --robot-plan --format json                # Execution tracks — where work fits
```

From triage, extract:
- What's blocked and why — unblocking work is high-impact
- What's on the critical path — delays here delay everything
- What's mispriorized — graph says P1 but assigned P3
- What's stale — neglected work that needs attention
- What's missing — suggest finds gaps (missing deps, duplicates)

## Phase 2: Dedup

```bash
br search "$ARGUMENTS" --status open --status in_progress --json
```

If matching work exists, surface it. Don't brainstorm duplicates.

## Phase 3: Ideation

Generate 3-5 alternatives. For each:
- What it solves (link to graph data)
- What it unblocks (check robot-plan tracks)
- Effort estimate
- Risk

## Phase 4: Decision Gate

Pick one. Criteria:
- **Impact** — does it unblock downstream work? (robot-plan)
- **Alignment** — is priority misaligned? (robot-priority)
- **Effort** — is it achievable in one session?
- **Hygiene** — does it fix a suggest warning? (robot-suggest)

## Phase 5: Output

```
Decision: <chosen alternative>
Rationale: <why, citing graph data>
Impact: <what it unblocks>
Open questions: <what we don't know yet>
Suggested scope: <in/out boundaries>
Next: /create "<scoped description>"
```
