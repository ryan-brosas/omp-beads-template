<!-- DENSITY: Target 80-120 lines. <60 = incomplete (missing sections, hand-wavy answers). >150 = cut fluff (be more specific, not more wordy). This is an AI handoff — every line must carry a fact, decision, or constraint. -->
# PRD: {title}

**Bead:** {bead-id} | **Type:** {feature|bugfix|chore|research|epic} | **Priority:** {P0|P1|P2|P3}
**Created:** {YYYY-MM-DD} | **Estimate:** {minutes}

## Problem

WHEN {actor} THEN {outcome} BECAUSE {root cause}.

{2-3 sentences expanding on who is affected, why now, what happens if we don't fix it.}

## Scope

### In Scope
- {Specific deliverable — file, feature, behavior}
- {Be precise. "Implement X" not "Improve X"}

### Out of Scope
- {Explicitly excluded — prevents scope creep}
- {Things the agent might "helpfully" do but shouldn't}

## Requirements

| # | Requirement | Priority | Acceptance Criteria |
|---|------------|----------|---------------------|
| 1 | {What must be true} | MUST | {How to verify it's true} |
| 2 | {What should be true} | SHOULD | {How to verify it's true} |

## Technical Context

**Key files:**
- `{path}` — {NEW|EDIT|DELETE} ({~lines} lines)
- `{path}` — {NEW|EDIT|DELETE} ({~lines} lines)

**APIs / systems touched:**
- {Extension API, CLI, database, external service}

**Existing code to NOT modify:**
- {List files/extensions that are off-limits}

## Approach

{2-4 paragraphs describing how each requirement maps to implementation. Include architecture decisions, data flow, key algorithms. Avoid pseudocode — describe what, not how.}

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {What could go wrong} | {Low|Medium|High} | {Low|Medium|High} | {How we handle it} |

## Acceptance Criteria

- [ ] {Criterion 1}
    - Verify: `{command or observable behavior}`
- [ ] {Criterion 2}
    - Verify: `{command or observable behavior}`
