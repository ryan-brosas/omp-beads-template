---
description: "Multi-agent code review with confidence scoring. 5 parallel agents independently review, then findings are scored and filtered at ≥80 threshold."
argument-hint: "<bead-id or defaults to HEAD changes>"
---

## Bead ID Resolution

`$ARGUMENTS` may be a short suffix (3-6 chars, e.g. `0ks`) or a full ID. Resolve it:

1. Try `br show "$ARGUMENTS" --json` — if it returns the bead, use that ID.
2. If it fails, suffix-match: `br list --status open --status in_progress --status closed --json`, filter IDs ending with `$ARGUMENTS`.
3. If exactly one match → use it. If multiple → list them and ask the user. If none → STOP: "No bead found matching $ARGUMENTS."

Use the resolved ID as `BEAD_ID` for all steps below.

## Prerequisites (CHECK FIRST)

1. `.beads/artifacts/$BEAD_ID/completion-evidence.json` exists with verification results.
2. `git diff HEAD~1` (or `git diff main...HEAD`) shows changes to review.
3. Bead status is not `closed`.

If no evidence: STOP. "Run /verify first — no verification evidence for $BEAD_ID."
If no changes: STOP. "No changes to review. Run /ship first."
If closed: STOP. "$BEAD_ID is already closed."

## Phase 0: Skip Check

Before launching review agents, check if review is needed:

| Condition | Action |
|-----------|--------|
| `.beads/artifacts/$BEAD_ID/review-report.md` already exists with `approved` | Skip — already reviewed. Report existing findings. |
| Bead is `draft` status | Skip — draft beads aren't ready for review. |
| Diff is trivial (< 20 lines, only comments/whitespace) | Skip — "Trivial change. Mark `approved` with note." |

If skipping: write a minimal review-report.md with `verdict: approved`, `findings: []`, reason for skip. Then report and stop.

## Phase 1: Graph Context

```bash
bv --robot-file-hotspots --format json       # Files with most bead activity
bv --robot-file-relations <changed-files> --format json  # Co-change patterns
br show "$BEAD_ID" --json                    # Bead details
```

Use this to understand blast radius and risk context. Skip if bv unavailable.

## Phase 2: Read PRD + Plan

Read `.beads/artifacts/$BEAD_ID/prd.md` and `.beads/artifacts/$BEAD_ID/plan.md`. Extract:
- Requirements checklist (from PRD)
- Implementation tasks (from plan)
- Non-goals and constraints

These are the spec the implementation must satisfy.

## Phase 3: Read Changed Files

For each changed production file:
```bash
bv --robot-file-beads <file> --format json   # What tasks touched this file?
git log --oneline -5 -- <file>               # Recent history
```

Read the full file changes via `git diff`. Focus on the diff, not the whole file.

## Phase 4: Launch 5 Parallel Review Agents

Launch each via `task` subagents. All run in parallel. Each returns a list of findings with preliminary confidence scores.

### Agent 1: Spec Compliance (PRD)
```
# Assignment
Read .beads/artifacts/$BEAD_ID/prd.md. For each requirement:
- Does the implementation satisfy it?
- Is anything missing or incomplete?
- Did the implementation add scope beyond the PRD?

Return: [{ requirement, satisfied: true/false, issue: string|null, confidence: 0-100 }]
```

### Agent 2: Spec Compliance (Plan)
```
# Assignment
Read .beads/artifacts/$BEAD_ID/plan.md. For each task:
- Was it completed?
- Are there stubs, TODOs, or placeholder implementations?
- Does the implementation match the task description?

Return: [{ task, completed: true/false, issue: string|null, confidence: 0-100 }]
```

### Agent 3: Bug Scan
```
# Assignment
Read ONLY the git diff (changed lines, not whole files). Scan for:
- Obvious logic errors (off-by-one, inverted conditions, missing null checks)
- Error handling gaps (uncaught promises, missing try/catch on fallible ops)
- Resource leaks (unclosed handles, missing cleanup)
- Race conditions (shared mutable state without synchronization)

Focus on LARGE bugs. Skip pedantic nitpicks and style issues.
Ignore pre-existing bugs in unchanged code.
Ignore issues linters/typecheckers would catch.

Return: [{ file, line, issue: string, severity: critical|high|medium, confidence: 0-100 }]
```

### Agent 4: Git History Context
```
# Assignment
For each changed file, check `git blame` and `git log` on the modified lines:
- Do recent changes to the same lines reveal a pattern of bugs?
- Do the modified functions have a history of reverts or hotfixes?
- Do commit messages on nearby code mention related issues?

Return: [{ file, line, issue: string, evidence: string, confidence: 0-100 }]
```

### Agent 5: Code Comment Compliance
```
# Assignment
Read comments in the changed files (not the diff — the actual file). For each comment that states a rule, constraint, or warning (e.g. "// IMPORTANT: always check X before Y"):
- Does the implementation comply?
- Are comments now stale/misleading after this change?

Return: [{ file, line, comment: string, complies: true/false, issue: string|null, confidence: 0-100 }]
```

## Phase 5: Confidence Scoring

For each finding from Phase 4, launch a parallel scoring pass. Use the rubric below verbatim:

| Score | Meaning |
|-------|---------|
| 0 | Not confident. False positive that doesn't stand up to light scrutiny, or pre-existing issue. |
| 25 | Somewhat confident. Might be real, might be false positive. Could not verify. |
| 50 | Moderately confident. Verified real, but minor or rare. Not important relative to the PR. |
| 75 | Highly confident. Double-checked. Very likely real and important. Directly impacts functionality. |
| 100 | Absolutely certain. Double-checked. Definitely real, happens frequently, evidence confirms. |

For PRD/Plan compliance issues: verify the requirement/task is actually in the artifact, not interpreted.
For bug findings: verify the bug is in changed lines, not pre-existing.
For history findings: verify the evidence supports the claim.

## Phase 6: Filter and Write Report

Filter: keep only findings scored ≥80. If none survive: report "No high-confidence issues."

Write `.beads/artifacts/$BEAD_ID/review-report.md` using `.omp/templates/review-report.md` as shape:

```markdown
# Review Report: $BEAD_ID

## Verdict

`approved` — all findings addressed or scored below threshold.

## Review Summary

- Agents run: 5 (spec-PRD, spec-plan, bug-scan, history, comments)
- Total raw findings: <N>
- High-confidence (≥80): <M>
- False positives filtered: <N-M>

## Findings

### #1: <title> (confidence: <score>)
**Agent:** <which agent>
**Severity:** critical|high|medium
**File:** <path>#L<line>
**Issue:** <description>
**Recommendation:** <concrete fix>

### #2: ...
```

## Phase 7: Report

```
Bead: $BEAD_ID | Verdict: <approved|changes-requested|blocked>
Agents: 5 run | Findings: <N> raw → <M> high-confidence (≥80)
Severity: <critical> critical, <high> high, <medium> medium
Ready for close: <true/false>
Next: /pr $BEAD_ID (if approved) or address findings above
```

Set verdict:
- `approved` — 0 high-confidence findings, or all addressed
- `changes-requested` — ≥1 high-confidence finding, no criticals
- `blocked` — ≥1 critical finding
