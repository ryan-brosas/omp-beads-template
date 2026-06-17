---
description: "Formalize work into a br bead + PRD. Graph-informed — uses bv for dedup, classification, and placement."
argument-hint: "<description of work>"
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:
1. User provided input ($ARGUMENTS) describing what to build.

If no input: STOP. Ask the user: "What are we building? Provide a description or run /brainstorm first."
Do NOT proceed. Do NOT "helpfully" skip ahead.

You are formalizing work into a tracked br bead. The bead is the backbone.

## Phase 1: Graph Context

```bash
bv --robot-triage --format json              # Project state
bv --robot-suggest --format json             # Duplicates, missing deps, label suggestions
bv --robot-plan --format json                # Execution tracks — where does new work fit?
br search "$ARGUMENTS" --status open --status in_progress --json  # Exact dedup
```

If a matching bead exists, surface it. Ask: work on existing or create new?

## Phase 2: Classify

| Signal | Type | Slug prefix |
|--------|------|-------------|
| add/build/create/new | feature | `feat-` |
| fix/crash/error/broken | bug | `fix-` |
| refactor/migrate/cleanup | task | `task-` |
| multi-phase/complex | epic | `epic-` |
| test/docs/ci/config | chore | `chore-` |

Priority: P0=critical | P1=high | P2=default | P3=low | P4=backlog

Check `bv --robot-priority --format json` — if this unblocks mispriorized work, adjust priority accordingly.

## Phase 3: Create

```bash
ACTOR="${BR_ACTOR:-assistant}"
br create --actor "$ACTOR" "$ARGUMENTS" \
  --type <type> \
  --priority <0-4> \
  --json
```

Capture the bead ID from output.

## Phase 4: Artifacts

Create `.beads/artifacts/<bead-id>/`:

**prd.md** — Use `.omp/templates/prd.md` as the shape:
- Problem: WHEN {actor} THEN {outcome} BECAUSE {root cause}
- Scope: In Scope / Out of Scope lists
- Requirements table: #, Requirement, Priority (MUST/SHOULD), Acceptance
- Technical Context: key files, APIs, existing patterns
- Approach: how we'll solve it
- Risks table: risk, likelihood, impact, mitigation
- Success Criteria: observable outcomes

**prd.json** — Use `.omp/templates/prd.json` as the shape. Machine-readable requirements + success criteria.

**decisions.md** — Use `.omp/templates/decisions.md` as the shape:
- Decision Log: #, Decision, Rationale, Confidence
- Rejected Alternatives: #, Alternative, Why Rejected, Risk if Re-introduced
- Assumptions: #, Assumption, Validation, Invalidation Impact

## Phase 5: Verify

```bash
br show <bead-id> --json              # Confirm creation
br dep cycles --json                  # Must be empty
ls .beads/artifacts/<bead-id>/        # Confirm artifacts
br sync --flush-only
```

## Phase 6: Report

```
Bead: <bead-id> | Type: <type> | Priority: P<n>
Graph fit: <where this sits in execution tracks>
Impact: <what this unblocks per robot-plan>
Artifacts: .beads/artifacts/<bead-id>/ (prd.md, prd.json, decisions.md)
Next: /plan <bead-id>
```
