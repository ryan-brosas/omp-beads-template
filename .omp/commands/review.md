---
description: "Lean code review. Graph-informed single-pass review for normal workflow."
argument-hint: "<bead-id or defaults to uncommitted changes>"
---

## Resolve Bead ID

```bash
BEAD_ID=$(bash .omp/scripts/resolve-bead.sh "$ARGUMENTS") || exit 1
```

Use `$BEAD_ID` (not `$ARGUMENTS`) in all commands below.

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:
1. `.beads/artifacts/$BEAD_ID/completion-evidence.json` exists and has verification results.
2. `git diff HEAD~1` (or appropriate base) shows changes to review.

If no evidence: STOP. Tell the user: "Run /verify first — no verification evidence for $BEAD_ID."
If no changes: STOP. Tell the user: "No changes to review. Run /ship first."
Do NOT proceed. Do NOT "helpfully" skip ahead.

You are reviewing code in the default lean workflow. Use the graph to understand impact, but keep this pass single-agent and focused.

## Phase 1: Lean Graph Context

```bash
bv --robot-file-hotspots --format json       # Files with most bead activity
br show "$BEAD_ID" --json                    # Bead details
```

Use heavier graph commands only when the lightweight context reveals unusual risk:

```bash
bv --robot-insights --format json            # Only when priority/centrality matters
```

## Phase 2: File Context

For changed production files, check history before judging the diff:

```bash
bv --robot-file-beads <file> --format json   # What tasks touched this file?
bv --robot-file-relations <file> --format json # What files co-change with this?
```

## Phase 3: Read the Evidence

Read `.beads/artifacts/$BEAD_ID/completion-evidence.json`. Check:
- Are all verification commands listed with results?
- Do any `failedChecks` remain unresolved?
- Are `uncheckedRisks` documented and acknowledged?

## Phase 4: Spec ↔ Code Adherence

Read the PRD requirements and plan tasks. For each:
- Does the implementation match the requirement?
- Are there missing requirements?
- Did the implementation add scope beyond the PRD?

## Phase 5: Write Review Report

Write `.beads/artifacts/$BEAD_ID/review-report.md` using `.omp/templates/review-report.md` as the shape:

- **verdict**: `approved` | `changes-requested` | `blocked`
- **ready_for_close**: `true` | `false`
- **findings[]**: severity (critical|high|medium|low), file, issue, recommendation
- **residual_risks[]**: risks not covered by verification
- **Spec ↔ Code Adherence**: PRD requirement coverage (N/M), plan task coverage, drift from plan
- **Summary**: 2-3 sentences — what passed, what needs attention

## Phase 6: Report

```
Bead: $BEAD_ID | Verdict: <approved/changes-requested/blocked>
Findings: <N> (<M critical, O high, P medium, Q low)
Ready for close: <true/false>
Next: /pr $BEAD_ID (if approved) or address findings
```
