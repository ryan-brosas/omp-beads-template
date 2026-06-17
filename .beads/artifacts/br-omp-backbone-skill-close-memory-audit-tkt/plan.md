<!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin (waves undefined, tasks lack code outlines, verification hand-wavy). Task outlines should show the shape of every file change — not full implementation, but enough that a different agent can execute without reading the PRD again. -->
# Plan: br-omp-backbone-skill-close-memory-audit-tkt

**Goal:** Insert a Memory Audit phase into `/close` that reads all 5 project memory files, detects drift against bead artifacts, proposes updates with user approval gating, and blocks close on full rejection. Update AGENTS.md command reference accordingly.

## Graph Context

- **Blast radius:** 2 files (0 new, 2 edits, 0 deletes)
- **Unblocks:** br-omp-backbone-skill-m7y (next memory maintenance bead, if the audit reveals staleness)
- **Blocked by:** None — no upstream dependencies
- **Critical path:** Yes — `/close` is the final gate in the bead lifecycle; any regression blocks all bead completions
- **Forecast:** 45 minutes (confidence 0.95)
- **Hotspots touched:** None — close.md has zero bead history in this repo

## Observable Truths

Each maps to at least one PRD acceptance criterion. Every one is falsifiable.

1. `grep -c "Phase.*memory\|Phase.*Memory\|Phase.*Audit" .omp/commands/close.md` returns ≥1 (AC-1).
2. The new phase appears between `## Phase 1: Read Review` and `## Phase 2: Close` (AC-1 positional).
3. Each of the 5 memory file paths appears at least once in the `close.md` audit phase text — `grep -c "project.md\|conventions.md\|decisions.md\|gotchas.md\|tech-stack.md" .omp/commands/close.md` returns ≥5 (AC-2).
4. The close.md audit phase contains a directive requiring explicit user approval before any memory file edit — e.g., "Ask the user," "Require user approval," or "Do NOT proceed until the user responds" (AC-3).
5. The close.md audit phase contains a "No memory file updates needed" or equivalent pass-through statement for the zero-drift fast path (AC-4).
6. The close.md audit phase contains a STOP condition when all proposals are rejected (AC-5).
7. `grep -c "^## Phase" .omp/commands/close.md` returns 7 — Phase 1, Phase 1.5, Phase 2, Phase 3, Phase 4, Phase 5, Phase 6 (AC-6).
8. The `/close` row in `.omp/AGENTS.md`'s Command Reference table has "Reads" column mentioning memory files and "Writes" column mentioning memory files — `grep "/close" .omp/AGENTS.md` confirms (AC-7).
9. `git diff --stat -- .omp/commands/` after this bead shows only `close.md` changed (AC-8).
10. The new phase contains zero ` ```python`, ` ```bash`, or ` ```sh` code fences — `grep -c '```python\|```bash\|```sh'` on the audit phase body returns 0 (AC-9).
11. `.omp/memory/project/conventions.md` lines 91-94 are unchanged — the contract was already correct (AC-10).
12. After `/close`, `grep "Next:" .omp/memory/project/project.md` shows a new next-priority item, not "Audit and harden the /close command" (AC-11).
13. `.omp/memory/project/gotchas.md` line 30 mitigation text references the `/close` memory audit (AC-12).
14. `.omp/memory/project/decisions.md` contains Decision #6 documenting phase placement, approval protocol, and checklist design (AC-13).
15. `close.md` line count increases from ~74 to ~180 lines (±10).
16. No other command files, skills, templates, or extensions are modified.

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| Modified close.md | New Phase 1.5 with checklist, approval gate, STOP condition | `.omp/commands/close.md` | Need |
| Modified AGENTS.md | Updated /close row in Command Reference table | `.omp/AGENTS.md` | Need |

## Architecture

### Overview

The `/close` command is a 74-line markdown instruction file with 6 sequential phases. This bead inserts a new phase between Phase 1 (Read Review) and Phase 2 (Close). Per Decision #2, the new phase is numbered `Phase 1.5` to signal its insertion-point nature without renumbering all subsequent phases. Phase 2-6 retain their identity — agents and users already know "Phase 2 = Close."

The new phase is pure agent instruction — no executable code, no scripts, no new tooling. It follows the same structural pattern as existing phases: a `## Phase N: Name` header, a prose description of what to do, and where applicable, bash command blocks. The phase guides the agent through a 5-sub-step audit: gather evidence, read current memory state, detect drift against a mandatory checklist, propose updates as diffs, and gate on user approval before either applying edits or stopping.

```
┌─────────────────────────────────────────────────────────────┐
│                      /close Command                          │
│                                                              │
│  Phase 1: Read Review                                        │
│    Reads review-report.md, confirms ready_for_close          │
│                          │                                   │
│                          ▼                                   │
│  Phase 1.5: Memory Audit  ←── NEW                           │
│    ┌──────────────────────────────────────────┐             │
│    │ a. Gather Evidence                       │             │
│    │    Read PRD, plan, completion-evidence,  │             │
│    │    git diff                               │             │
│    │                     │                    │             │
│    │                     ▼                    │             │
│    │ b. Read Current Memory State             │             │
│    │    Read 5 memory files on disk           │             │
│    │                     │                    │             │
│    │                     ▼                    │             │
│    │ c. Detect Drift (mandatory checklist)    │             │
│    │    project.md ──► Status/Milestone/Next  │             │
│    │    conventions.md ──► New rules/patterns  │             │
│    │    decisions.md ──► Unrecorded decisions  │             │
│    │    gotchas.md ──► Undocumented pitfalls   │             │
│    │    tech-stack.md ──► Version/Dep changes  │             │
│    │                     │                    │             │
│    │        ┌────────────┴────────────┐       │             │
│    │        ▼                         ▼       │             │
│    │   No drift detected         Drift found  │             │
│    │        │                         │       │             │
│    │        ▼                         ▼       │             │
│    │   "No updates               d. Propose   │             │
│    │    needed" →                  Updates    │             │
│    │    Phase 2                      │        │             │
│    │                                 ▼        │             │
│    │                          e. Apply/Reject │             │
│    │                          ┌──────┬──────┐ │             │
│    │                          ▼      ▼      ▼ │             │
│    │                        yes    no    skip  │             │
│    │                          │      │      │  │             │
│    │        ┌─────────────────┘      │      │  │             │
│    │        ▼                        ▼      │  │             │
│    │   Apply edit +            Document    │  │             │
│    │   re-read to confirm      rejection   │  │             │
│    │        │                        │      │  │             │
│    │        └────────┬───────────────┘      │  │             │
│    │                 ▼                      │  │             │
│    │          At least 1 yes?               │  │             │
│    │          ┌──────┴──────┐               │  │             │
│    │          ▼              ▼               │  │             │
│    │         Yes            No               │  │             │
│    │          │              │               │  │             │
│    │          ▼              ▼               │  │             │
│    │      Phase 2      STOP: Bead           │  │             │
│    │      (Close)       remains open        │  │             │
│    └──────────────────────────────────────────┘             │
│                          │                                   │
│                          ▼                                   │
│  Phase 2: Close                                              │
│    br close $BEAD_ID                                         │
│                          │                                   │
│                          ▼                                   │
│  Phase 3: Check Queue Impact                                 │
│    br ready, br blocked                                      │
│                          │                                   │
│                          ▼                                   │
│  Phase 4: Sync                                               │
│    br sync --flush-only, git commit                          │
│                          │                                   │
│                          ▼                                   │
│  Phase 5: Session End                                        │
│    git pull --rebase, sync, push, git status                 │
│                          │                                   │
│                          ▼                                   │
│  Phase 6: Report                                             │
│    Summary output                                            │
└─────────────────────────────────────────────────────────────┘
```

### Design Decisions Encoded in Architecture

**Decision D1 (Phase 1.5 naming):** Per bead Decision #2, the phase is named "Phase 1.5: Memory Audit." This preserves Phase 2-6 identity. The alternative (renumbering Phase 2→3, 3→4, etc.) was rejected because it would break muscle memory for users and agents who already know "Phase 2 = Close."

**Decision D2 (mandatory checklist over algorithm):** Per bead Decision #3, drift detection uses a human-readable checklist rather than algorithmic parsing. Memory files have freeform markdown tables with varying structure. Any regex or script would produce high false-positive/negative rates. The checklist guides agent reasoning — the agent reads actual content and reasons about semantic drift. User approval mitigates hallucination risk.

**Decision D3 (per-file approval over batch):** Per bead Decision #4, each memory file proposal requires independent user approval (yes/no/skip). A single wrong proposal doesn't force rejection of all. The extra interaction cost is acceptable because drift is the exception — most beads need zero updates.

**Decision D4 (hard STOP on full rejection):** Per bead Decision #5, if the user rejects all proposals, the agent must NOT proceed to Phase 2. The bead remains open. This forces resolution: either the agent hallucinated (audit broken) or the user refuses to update stale memory (contract violation). In both cases, closing would violate conventions.md.

**Decision D5 (no auto-approve):** Per bead Decision #6, no memory edit is applied without explicit user confirmation. Every proposal must be shown as a diff before asking. The agent must never assume "yes."

### Phase Interaction with Existing Phases

The new phase sits between Phase 1 and Phase 2. It reads from Phase 1's output (review report confirms the bead is correct) but doesn't modify it. It gates Phase 2: Close cannot execute until the audit is resolved. Phases 3-7 are unaffected — they only execute after Phase 2 succeeds.

The phase interacts with the Prerequisites block indirectly: prerequisites ensure `completion-evidence.json` and `review-report.md` exist before Phase 1. Phase 1.5 reads these artifacts as part of evidence gathering. If prerequisites fail, Phase 1 never runs, and Phase 1.5 is never reached.

## Component Breakdown

### Component 1: close.md New Phase Body (~106 lines)

The new phase body is inserted after `## Phase 1: Read Review`'s closing content (line 33) and before `## Phase 2: Close` (currently line 35). The body follows the established command phase pattern: header + prose + checklist. No bash code blocks within the phase — all file reads use the `read` tool, all edits use the `edit` tool, and all br/git commands are in existing phases only.

Structure of the new lines:

```
## Phase 1.5: Memory Audit

[Prose: why this phase exists, what it gates, reference to conventions.md mandate]

### Sub-step a: Gather Evidence

[Prose: read PRD, plan, completion-evidence, git diff — these tell us what the bead delivered]

### Sub-step b: Read Current Memory State

[Prose: read all 5 memory files on disk — exact paths listed]

### Sub-step c: Detect Drift

[Prose: for each memory file, answer the checklist questions. Each "no" or "yes" must be stated.]

[Checklist table — one row per memory file with concrete yes/no questions]

### Sub-step d: Propose Updates

[Prose: for each file with drift, show current content + proposed content as diff. Ask for approval.]

[IMPORTANT: Do NOT auto-approve. Do NOT edit without user confirmation.]

### Sub-step e: Apply or Reject

[Prose: on "yes" → edit file, re-read to confirm. On "no" → document. On "skip" → document.]

[STOP condition: if ALL proposals rejected, STOP. Do not proceed to Phase 2.]

[Pass-through: if NO drift detected, output "No memory file updates needed." Proceed to Phase 2.]
```

#### Checklist Table Design

The checklist mirrors `.omp/memory/project/conventions.md` Memory File Maintenance table (lines 83-89). Each row asks a concrete yes/no question with specific triggers:

| Memory File | Check Question | Triggers |
|---|---|---|
| `project.md` | Does "Current Phase" still reflect reality? | Bead completed a milestone → update Status. PRD describes a milestone → update Milestone. Bead changed priorities → update Next. Bead touched infrastructure → review Goal. |
| `conventions.md` | Were any naming rules, workflow steps, skill structures, command structures, git conventions, or agent conventions introduced or changed? | New command → Command Structure. Branch/commit format change → Git. New agent rule → Agent Conventions. Workflow phase change → Workflow. New memory rule → Memory File Maintenance. |
| `decisions.md` | Were any architecture decisions made that aren't recorded? | A "decision" = choice between 2+ viable alternatives with long-term consequences. NOT: implementation details, process steps, bug fixes. |
| `gotchas.md` | Were any pitfalls, warnings, or workarounds discovered during implementation? | 5-column entry: Date, Area, Gotcha, Impact, Mitigation. Also check: are existing gotchas now stale? |
| `tech-stack.md` | Were any tool versions, dependencies, or verification commands added, removed, or changed? | New br/bv version requirement. New tool dependency. New verification command. New constraint. |

#### Sub-step c: Agent Instructions for Drift Detection

The agent must, for each of the 5 files:

1. **Read** the file's current on-disk content.
2. **Compare** against bead evidence (PRD scope, plan scope, actual diff, completion-evidence).
3. **Answer** the checklist question explicitly — "Yes, drift detected: <specific section> needs <specific change>." or "No drift in <file>: <specific reason why not>."
4. **Never** be silent about any file. Every file must have a stated conclusion.
5. **Never** skip a file because "the bead was small." All 5 files are audited every time.

#### Sub-step d: Proposal Format

For each file where drift is detected, the agent outputs:

```
--- .omp/memory/project/<file> (current)
+++ .omp/memory/project/<file> (proposed)
@@ <context>
-<current text>
+<proposed text>

Apply this update to <file>? (yes/no/skip)
```

The diff must show the exact current content (verbatim quote from the `read` output) and the exact proposed content. Vagueness ("consider updating X") is prohibited. The proposal must be a concrete, apply-able edit.

#### Sub-step e: Application and Gating Logic

```
# Fast path — no drift in any file
if no drift detected:
    output: "No memory file updates needed."
    proceed to Phase 2

# Normal path — drift detected, user approves some
for each proposal:
    if user responds "yes":
        edit the file with the proposed change  # use edit tool
        re-read the file to confirm  # use read tool
        report: "Applied: <file>"
    elif user responds "no":
        report: "Rejected: <file> — <description of rejected proposal>"
    elif user responds "skip":
        report: "Skipped: <file> — user will handle manually"

# Gate check
if at least one "yes":
    report: "Memory audit complete. Applied: <list>. Rejected: <list>. Skipped: <list>."
    proceed to Phase 2
else:
    # All proposals were "no" or "skip" with zero "yes"
    STOP
    output: "Memory audit blocked close — user rejected all proposed updates."
    output: "Bead $BEAD_ID remains open. Resolve memory drift manually or re-run /close."
    Do NOT proceed to Phase 2. Do NOT run br close.
```

#### Prohibited Behaviors (Must Be Enumerated in close.md)

1. Auto-approving proposals — the agent must never assume "yes" or skip the approval prompt.
2. Editing memory files without showing the diff first.
3. Proceeding to close if any proposal was explicitly rejected AND zero proposals were approved.
4. Skipping the audit because "the bead was small."
5. Using `honcho_remember` as a substitute for memory file updates.
6. Proposing vague updates ("consider updating X" without concrete text).
7. Proposing updates that delete user-authored content without explicit justification.
8. Proposing an edit without re-reading the file immediately before applying (race condition defense).

### Component 2: AGENTS.md Command Reference Row Update (1 line change)

The `/close` row in the Command Reference table (line 29) changes from:

```
| `/close` | Close bead, suggest next | all artifacts | — | suggest, next, capacity |
```

To:

```
| `/close` | Close bead, suggest next | all artifacts, memory files | memory files (on user approval) | suggest, next, capacity |
```

The "Reads" column adds "memory files" because Phase 1.5 reads all 5 files. The "Writes" column changes from "—" to "memory files (on user approval)" because Phase 1.5 writes to memory files when the user approves. The parenthetical "(on user approval)" reflects the gating mechanism — writes are conditional, not automatic.

No other rows are modified. No other sections in AGENTS.md are changed.

## Data Models

### Memory File Checklist (the Mandatory Checklist Table)

This is the structured data the agent uses in sub-step c. It is embedded directly in close.md as a markdown table — no separate file, no schema, no serialization format. The agent reads the table as part of executing the command.

```
| Memory File | Check Question | Specific Triggers |
|-------------|----------------|-------------------|
| project.md | Does "Current Phase" reflect reality after this bead? | Status changed? Milestone achieved? "Next" field stale? "The Goal" needs refinement? |
| conventions.md | Were any conventions introduced, changed, or removed? | New command, git rule, workflow step, agent convention, memory rule, or skill structure change |
| decisions.md | Were any architecture decisions made that aren't recorded? | Choice between 2+ viable alternatives with long-term consequences |
| gotchas.md | Were any pitfalls or workarounds discovered? Did existing gotchas become stale? | New 5-column entry needed? Template bootstrap gotcha now obsolete? |
| tech-stack.md | Were any tool versions, dependencies, or verification commands changed? | New br/bv version, new dependency, new verification command, new constraint |
```

### Drift Detection Output Model

The agent's output during sub-step c must follow this format for each file:

```
**<file>:** <conclusion> — <specific evidence>
```

Where `<conclusion>` is one of:
- `No drift` — file is current; bead didn't affect this category
- `Drift detected` — file needs updating; followed by the specific section and proposed change
- `Uncertain` — agent can't determine; followed by the reason and a request for manual review

Example outputs:
```
**project.md:** No drift — Status is "stable" (unchanged), Milestone is current (unchanged), Next references this bead (correct — will update after close).
**conventions.md:** Drift detected — Agent Conventions section should add "Must audit memory on /close" rule.
**decisions.md:** Drift detected — Phase placement decision (1.5 vs renumbering) should be recorded as Decision #6.
**gotchas.md:** Drift detected — "Stale memory is worse than no memory" mitigation can reference new structural check.
**tech-stack.md:** No drift — no dependency changes in this bead.
```

### Proposal Output Model

Each proposal in sub-step d follows this format:

```
--- <file-path> (current, from disk)
+++ <file-path> (proposed)
@@ <section context>
-<verbatim current content>
+<verbatim proposed content>

Apply this update to <file>? (yes/no/skip)
```

### User Response Model

The agent accepts three responses per proposal:
- `yes` → apply the edit, re-read to confirm
- `no` → document rejection, do not edit, continue to next proposal
- `skip` → document deferral, do not edit, continue to next proposal

Any other response → re-prompt: "Please respond with yes, no, or skip."

### Gating State Machine

```
                   ┌─────────────────┐
                   │  Phase 1.5      │
                   │  Initial State  │
                   └────────┬────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
    ┌─────────────────┐         ┌─────────────────┐
    │ No drift in any │         │ Drift detected  │
    │ file            │         │ in ≥1 file      │
    └────────┬────────┘         └────────┬────────┘
             │                           │
             ▼                           ▼
    ┌─────────────────┐         ┌─────────────────┐
    │ Report "No      │         │ Propose updates │
    │ updates needed" │         │ (sub-step d)    │
    └────────┬────────┘         └────────┬────────┘
             │                           │
             ▼                           ▼
    ┌─────────────────┐         ┌─────────────────┐
    │ → Phase 2       │         │ Collect user    │
    └─────────────────┘         │ responses       │
                                └────────┬────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         ▼                               ▼
               ┌─────────────────┐             ┌─────────────────┐
               │ ≥1 "yes"        │             │ Zero "yes"      │
               │ (may include    │             │ (all "no" or    │
               │  "no"/"skip")   │             │  "skip")        │
               └────────┬────────┘             └────────┬────────┘
                        │                               │
                        ▼                               ▼
               ┌─────────────────┐             ┌─────────────────┐
               │ Apply approved  │             │ STOP            │
               │ edits. Report   │             │ Bead remains    │
               │ accepted/       │             │ open. Output    │
               │ rejected/       │             │ reason.         │
               │ skipped.        │             │                 │
               └────────┬────────┘             └─────────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │ → Phase 2       │
               └─────────────────┘
```

### Edge Case Handling (Embedded in close.md Text)

| Edge Case | Agent Behavior | Output |
|-----------|---------------|--------|
| Memory file missing | Report missing. Ask: continue or abort? | "Missing: .omp/memory/project/<file>. Continue without it? (yes/no)" |
| Memory file malformed | Report issue. Propose fix separately. | "Warning: <file> appears malformed — <specific issue>. Fix as part of audit? (yes/no)" |
| PRD doesn't exist | Fall back to git diff only. Note limitation. | "Missing: PRD artifact — audit is partial. No PRD context available." |
| Bead touched memory files | Report. Verify alignment. | "This bead directly modified <file>. Verifying consistency with bead scope..." |
| No git diff available | Note limitation. Proceed with available evidence. | "No git diff available — using PRD and completion-evidence only." |
| Multiple files need same update | Propose independently. Separate approval. | Each file gets its own proposal + prompt. |
| Update exceeds size target | Warn. Offer trim option. | "Proposed update would exceed target size for <file> (~X bytes over). Apply anyway / trim / skip?" |
| User aborts mid-audit | Stop immediately. Don't edit. | "Memory audit aborted by user. Bead still open." |
| Agent can't determine drift | Flag as uncertain. Ask for manual review. | "Uncertain: <file> — <reason>. Review manually? Current content: <quote>." |
| Concurrent edit detected | Re-read before edit. If content changed since initial read, warn and re-propose. | "Warning: <file> changed since initial read. Reloading and re-checking..." |

## API Contracts

### br CLI Operations Used

| Operation | Phase | Command | JSON Flag | Purpose |
|-----------|-------|---------|-----------|---------|
| Show bead | Resolution | `br show $ARGUMENTS --json` | yes | Resolve short ID to full ID |
| List beads | Resolution | `br list --status open --status in_progress --status closed --json` | yes | Suffix match fallback |
| Close bead | Phase 2 | `br close --actor "$ACTOR" "$BEAD_ID" --reason "..." --json` | yes | Close the bead |
| Check ready | Phase 3 | `br ready --json` | yes | Newly unblocked work |
| Check blocked | Phase 3 | `br blocked --json` | yes | Confirm no new blockers |
| Sync | Phase 4, 5 | `br sync --flush-only` | no | Flush bead state to disk |

Note: No new br commands are needed. The audit phase only reads files and edits memory — it does not mutate bead state.

### git Operations Used

| Operation | Phase | Command | Purpose |
|-----------|-------|---------|---------|
| Diff | Phase 1.5a | `git diff <bead-branch>..<base>` | Gather evidence of what files changed |
| Log | Phase 1.5a | `git log <bead-branch> --oneline` | Gather commit history |
| Add + Commit | Phase 4 | `git add .beads/ && git commit -m "close: $BEAD_ID"` | Commit bead state |
| Pull + Push | Phase 5 | `git pull --rebase && git push` | Sync with remote |
| Status | Phase 5 | `git status` | Confirm clean state |

### Filesystem Operations Used

| Operation | Phase | Tool | Files |
|-----------|-------|------|-------|
| Read artifacts | Phase 1.5a | `read` | `.beads/artifacts/$BEAD_ID/prd.md`, `plan.md`, `completion-evidence.json` |
| Read memory | Phase 1.5b | `read` | `.omp/memory/project/project.md`, `conventions.md`, `decisions.md`, `gotchas.md`, `tech-stack.md` |
| Edit memory | Phase 1.5e | `edit` | Any memory file with an approved proposal |
| Confirm edit | Phase 1.5e | `read` | Edited memory file (re-read to verify) |

### Immutable Contracts

The following must NOT be modified by this bead:
- All other `.omp/commands/*.md` files (brainstorm, create, plan, ship, verify, review, pr, init, git-clean)
- `.omp/extensions/workflow-gate.ts`
- `.omp/skills/` (all skills)
- `.omp/templates/` (all templates)
- `.omp/memory/project/conventions.md` lines 91-94 (the contract is correct; this bead implements it)
- The Prerequisites block in close.md (lines 15-24)
- All br/git commands in Phases 2-7 (renumbered from 1.5 insertion)
- The Bead ID Resolution block (lines 6-13)

## Test Strategy

Since close.md is a markdown command (not executable code), testing has two layers: structural verification (can be automated) and behavioral verification (requires an agent executing `/close`).

### Layer 1: Structural Verification (Automated)

These are bash/grep checks that can run without an agent:

```bash
# T1: Phase count — must be 7
grep -c "^## Phase" .omp/commands/close.md  # Expected: 7

# T2: Phase headers are sequential and correctly numbered
grep "^## Phase [0-9]" .omp/commands/close.md  # Expected: Phase 1, Phase 1.5, Phase 2-6

# T3: Phase 1.5 exists between Phase 1 and Phase 2
awk '/^## Phase 1: Read Review/,/^## Phase 1\.5/' .omp/commands/close.md | grep -q "Phase 1.5"  # Expected: match

# T4: All 5 memory files mentioned in audit phase
grep -c "project.md\|conventions.md\|decisions.md\|gotchas.md\|tech-stack.md" .omp/commands/close.md  # Expected: >= 5

# T5: User approval directive present
grep -qi "ask the user\|user approval\|do NOT proceed until the user" .omp/commands/close.md  # Expected: match

# T6: Pass-through path present
grep -qi "no memory file updates needed\|no updates needed\|no drift.*proceed" .omp/commands/close.md  # Expected: match

# T7: STOP condition present
grep -qi "STOP\|Do NOT proceed to Phase 2\|bead remains open" .omp/commands/close.md  # Expected: match

# T8: No new code fences in audit phase body
# Extract the lines between Phase 1.5 and Phase 2, count code fences
sed -n '/^## Phase 1\.5:/,/^## Phase 2:/p' .omp/commands/close.md | grep -c '```'  # Expected: 0

# T9: AGENTS.md row updated
grep "/close" .omp/AGENTS.md | grep -q "memory files"  # Expected: match
grep "/close" .omp/AGENTS.md | grep -q "on user approval"  # Expected: match

# T10: Only close.md changed in commands/
git diff --stat -- .omp/commands/  # Expected: only close.md

# T11: conventions.md audit section unchanged
git diff -- .omp/memory/project/conventions.md  # Expected: empty (no changes)

# T12: Line count in target range
wc -l .omp/commands/close.md  # Expected: ~170-190
```

### Layer 2: Behavioral Verification (Agent-Driven Dry Run)

These tests require an agent to execute `/close` on a bead and a human (or observing agent) to verify behavior.

#### BT-1: No-Drift Pass-Through (US-3)

**Setup:** Create a trivial bead (e.g., fix one word in README.md), complete /verify and /review.
**Execute:** `/close <bead-id>`
**Expected:**
- Agent reads all 5 memory files
- Agent outputs explicit "No drift" for each file
- Agent outputs "No memory file updates needed."
- Agent proceeds to Phase 2 (br close)
- Bead is closed successfully

#### BT-2: Drift Detected + User Approves (US-1)

**Setup:** Create a bead that adds a new agent convention (e.g., "always quote variables in bash"). Complete /verify and /review.
**Execute:** `/close <bead-id>`
**Expected:**
- Agent detects drift in conventions.md (Agent Conventions section)
- Agent shows current conventions.md Agent Conventions list + proposed addition as diff
- Agent asks for approval
- User responds "yes"
- Agent edits conventions.md, re-reads to confirm
- Agent reports "Applied: conventions.md"
- Agent proceeds to Phase 2
- Bead is closed

#### BT-3: Drift Detected + User Rejects All (US-4)

**Setup:** Same as BT-2.
**Execute:** `/close <bead-id>`
**Expected:**
- Agent proposes drift updates
- User responds "no" to ALL proposals
- Agent documents each rejection
- Agent outputs STOP message: "Memory audit blocked close — user rejected all proposed updates."
- Agent does NOT run `br close`
- `br show $BEAD_ID --json` confirms bead is still open

#### BT-4: Partial Approval (US-4 + EC-7)

**Setup:** A bead that triggers drift in both conventions.md and gotchas.md.
**Execute:** `/close <bead-id>`
**Expected:**
- Agent proposes updates for both files independently
- User responds "yes" to conventions.md, "no" to gotchas.md
- Agent applies conventions.md edit, documents gotchas.md rejection
- Agent reports "Applied: conventions.md. Rejected: gotchas.md."
- Agent proceeds to Phase 2 (at least one "yes")
- Bead is closed

#### BT-5: Memory File Already Current (US-5)

**Setup:** Create a bead. During the bead, manually add a decision to decisions.md.
**Execute:** `/close <bead-id>`
**Expected:**
- Agent reads decisions.md
- Agent detects the decision is already recorded (content matches)
- Agent reports "decisions.md: up to date (decision already recorded)"
- Agent does NOT propose a duplicate update

#### BT-6: Missing Memory File (EC-1)

**Setup:** Temporarily move `.omp/memory/project/gotchas.md` to `.omp/memory/project/gotchas.md.bak`.
**Execute:** `/close <bead-id>`
**Expected:**
- Agent reports "Missing: .omp/memory/project/gotchas.md"
- Agent asks "Continue without gotchas.md audit?"
- User responds "yes" → agent skips gotchas and audits remaining 4 files
- User responds "no" → agent STOPS, bead remains open

#### BT-7: Update Exceeds Size Target (EC-8)

**Setup:** Add a proposed update to conventions.md that would push it past 4KB.
**Execute:** `/close <bead-id>`
**Expected:**
- Agent warns about size target
- Agent offers trim/skip/apply options
- User can choose any option

### Test Execution Order

Structural tests (T1-T12) run first. They are fast, deterministic, and catch the most common failure modes (wrong phase count, missing checklist, wrong table format). Behavioral tests (BT-1 through BT-7) run after structural tests pass, prioritizing BT-1 (no-drift fast path, the most common real-world scenario) and BT-4 (partial approval, the most complex gating logic).

## Migration Plan

### Forward Compatibility

This bead is forward-looking only. The 8 beads already closed in this repo were closed without memory audit. Per bead Decision #7, retrospective audit is out of scope — a separate bead candidate if staleness is detected.

### For the Current conventions.md Contract

The conventions.md Memory File Maintenance section (lines 79-94) is NOT being updated. Per bead Decision #8, the contract text is already correct: "Every `/close`: agent checks if any conventions/decisions/gotchas were discovered during the bead and proposes updates." This bead implements the HOW (close.md phase), not the WHAT (the convention). Updating conventions.md would be a self-referential change — the convention didn't change, the implementation did.

### For the Current project.md "Next" Field

After this bead completes, the project.md "Next" field should be updated from "Audit and harden the /close command to check memory file staleness on bead completion" to the actual next priority item. This update happens during this bead's own `/close` — the Phase 1.5 audit detects that "Next" is stale (this bead just did what "Next" describes) and proposes an update. It's a self-referential but correct application of the new phase.

### For the Current gotchas.md "Stale Memory" Entry

The gotchas.md line 30 entry ("Stale memory is worse than no memory") currently has mitigation "Update on every milestone. Audit during `/close`." After this bead, the mitigation should reference the new structural check: "Update on every milestone. The `/close` command now includes a mandatory Memory Audit phase that detects and proposes memory file updates." The Phase 1.5 audit during this bead's own `/close` should detect and propose this update.

### For the New Decision in decisions.md

This bead should record Decision #6 in the project's decisions.md, documenting the phase placement (1.5 vs renumbering), approval protocol (per-file), and checklist design (mandatory checklist over algorithm). The Phase 1.5 audit during this bead's own `/close` should detect that a decision was made but not yet recorded, and propose it.

## Rollback Plan

### Revert Procedure

If the Memory Audit phase causes issues (blocks legitimate closes, produces excessive false positives, or confuses agents), rollback is straightforward:

1. **Revert close.md:** Remove the Phase 1.5 block (lines between Phase 1 and Phase 2), restoring Phase 2-6 to their original numbering. The block is self-contained — no other phases depend on it.
2. **Revert AGENTS.md:** Restore the `/close` row to its original:
   ```
   | `/close` | Close bead, suggest next | all artifacts | — | suggest, next, capacity |
   ```
3. **Commit:** `git commit -m "revert: remove memory audit phase from /close"`

### Rollback Triggers

| Trigger | Detection | Action |
|---------|-----------|--------|
| False-positive rate exceeds 50% over 10 beads | Manual observation during /close | Tighten checklist triggers OR add "batch approve-all" escape hatch |
| Agent consistently misses real drift | Manual observation during /close | Make checklist more specific with additional trigger examples |
| Phase blocks close for >5 minutes on no-drift beads | User complaint | Optimize sub-step instruction brevity |
| AGENTS.md row change breaks orchestrator or other tooling | orchestrator skill failure | Revert AGENTS.md row, investigate why tooling depends on exact row text |
| Memory files grow past size targets from audit-driven edits | Manual observation | Add stricter size enforcement in sub-step d |

### Recovery from Failed Audit

If the agent's audit produces hallucinated proposals that the user accidentally approves, recovery is:

1. `git diff` to see what the audit changed in memory files
2. `git checkout -- .omp/memory/project/<file>` to revert individual files
3. Re-run `/close` — the agent will re-audit with fresh context

### Data Integrity During Audit

The audit phase only reads files until the user says "yes." No files are modified during sub-steps a-d. In sub-step e, only files with explicit "yes" responses are edited — one edit per approved proposal. The agent re-reads each file after editing to confirm the edit applied correctly. If the file changed since the initial read (race condition), the agent warns and re-proposes.

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | T1.1 (close.md), T1.2 (AGENTS.md) | Yes | PRD read, decisions internalized | Structural tests T1-T12 pass. Behavioral dry-run BT-1 passes. |
| 2 | T2.1 (Self-audit dry run) | No | Wave 1 complete | Behavioral tests BT-2 through BT-7 pass. All 13 ACs satisfied. |
| 3 | T3.1 (Verification + evidence) | No | Wave 2 complete | completion-evidence.json generated. All 13 ACs confirmed. |

Wave 1 is the implementation. Wave 2 validates against behavioral scenarios. Wave 3 generates evidence artifacts.

## Tasks

### Wave 1: Implement Phase 1.5 + AGENTS.md Update {parallel}

Wave 1 has two independent tasks: close.md editing and AGENTS.md row update. They touch different files with no dependency between them.

**Task 1.1: Insert Phase 1.5 into close.md**

Edit `.omp/commands/close.md` to insert the new Memory Audit phase between `## Phase 1: Read Review` and `## Phase 2: Close`. The phase body is ~106 lines of pure markdown instruction — no bash code blocks, no scripts. Follow the existing command phase structure: header, prose, sub-steps.

The phase body consists of:
- A `## Phase 1.5: Memory Audit` header
- Prose explaining why the phase exists (reference conventions.md mandate)
- Sub-step a: Gather Evidence (read PRD, plan, completion-evidence, git diff)
- Sub-step b: Read Current Memory State (read 5 files with exact paths)
- Sub-step c: Detect Drift (mandatory checklist table with concrete yes/no questions per file)
- Sub-step d: Propose Updates (diff format, user approval prompt per file, no auto-approve directive)
- Sub-step e: Apply or Reject (yes/no/skip handling, STOP condition on full rejection, pass-through on no drift)
- Prohibited behaviors list (8 items)

The existing Phase 2-6 headers remain unchanged. Phase 2 is still `## Phase 2: Close`, not `## Phase 3: Close`. Per Decision #2, Phase 1.5 signals insertion without renumbering.

Insertion point: after line 33 (end of Phase 1 body) and before line 35 (`## Phase 2: Close`).

Target line count: close.md grows from ~74 to ~180 lines.

```
## Phase 1.5: Memory Audit

Before closing the bead, audit the project's durable memory files. The conventions.md
Memory File Maintenance section (line 93) mandates: "Every `/close`: agent checks if any
conventions/decisions/gotchas were discovered during the bead and proposes updates."

This phase is a structural gate — you cannot close a bead without auditing memory.
Stale memory degrades every subsequent agent's decision quality.

### Sub-step a: Gather Evidence

Read the bead's artifacts to understand what changed:

```bash
# What was supposed to change
cat .beads/artifacts/$BEAD_ID/prd.md
# What was planned
cat .beads/artifacts/$BEAD_ID/plan.md  # if exists
# What actually happened
cat .beads/artifacts/$BEAD_ID/completion-evidence.json
# What files changed
git diff <branch>..<base>  # adapt to the bead's branch structure
```

### Sub-step b: Read Current Memory State

Read all 5 memory files exactly as they exist on disk:

1. `.omp/memory/project/project.md`
2. `.omp/memory/project/conventions.md`
3. `.omp/memory/project/decisions.md`
4. `.omp/memory/project/gotchas.md`
5. `.omp/memory/project/tech-stack.md`

### Sub-step c: Detect Drift

For each memory file, answer the checklist question explicitly. You MUST state
a conclusion for every file — silence is not evidence of checking.

| Memory File | Check Question | Specific Triggers |
|-------------|----------------|-------------------|
| project.md | Does "Current Phase" reflect reality after this bead? | Status changed? Milestone achieved? "Next" field stale? "The Goal" needs refinement? |
| conventions.md | Were any conventions introduced, changed, or removed? | New command, new git rule, workflow step change, new agent convention, memory rule change, skill structure change |
| decisions.md | Were any architecture decisions made that aren't recorded? | Choice between 2+ viable alternatives with long-term consequences. NOT: implementation details, process steps, bug fixes |
| gotchas.md | Were any pitfalls or workarounds discovered? Did any existing gotchas become stale? | New 5-column entry (Date, Area, Gotcha, Impact, Mitigation) needed? Template bootstrap gotcha now obsolete? |
| tech-stack.md | Were any tool versions, dependencies, or verification commands changed? | New br/bv version, new dependency, new verification command, new constraint |

For each file, output:

```
**<file>:** <No drift | Drift detected | Uncertain> — <evidence>
```

### Sub-step d: Propose Updates

For each file where drift is detected, show the exact current content and
the proposed change:

```
--- <file-path> (current)
+++ <file-path> (proposed)
@@ <section>
-<current verbatim text>
+<proposed verbatim text>

Apply this update to <file>? (yes/no/skip)
```

IMPORTANT: Do NOT auto-approve any proposal. Do NOT edit any file without
explicit user confirmation. Every proposal must be shown as a diff first.
Proposals must be concrete — verbatim text to add/change/remove. No vagueness.

If no drift is detected in any file:
- Output: "No memory file updates needed."
- Proceed directly to Phase 2.

### Sub-step e: Apply or Reject

For each user response:
- "yes" → Apply the edit using the edit tool. Re-read the file to confirm
  the change applied correctly.
- "no" → Document: "Rejected: <file> — <description>"
- "skip" → Document: "Skipped: <file> — user will handle manually"

After all proposals are resolved:

IF at least one "yes":
  - Apply all approved edits
  - Report: "Memory audit complete. Applied: <list>. Rejected: <list>. Skipped: <list>."
  - Proceed to Phase 2.

IF zero "yes" (all "no" or "skip"):
  - STOP. Do NOT proceed to Phase 2.
  - Output: "Memory audit blocked close — user rejected all proposed updates."
  - Output: "Bead $BEAD_ID remains open. Resolve memory drift manually or re-run /close."
  - Do NOT run `br close`.

### Prohibited Behaviors

- NEVER auto-approve or skip the approval prompt — every edit requires user "yes"
- NEVER edit a memory file without showing the diff first
- NEVER proceed to Phase 2 if ALL proposals were rejected
- NEVER skip the audit because "the bead was small" — audit every close, every time
- NEVER use `honcho_remember` as a substitute for memory file updates
- NEVER propose vague updates ("consider updating X") — be concrete
- NEVER delete user-authored content without explicit justification in the proposal
- NEVER edit a file without re-reading it immediately before applying (race condition defense)

### Edge Cases

| Situation | Action |
|-----------|--------|
| Memory file is missing | Report "Missing: <path>". Ask "Continue without it? (yes/no)". If no → STOP. |
| Memory file is malformed | Report "Warning: <file> appears malformed — <issue>". Propose fix separately. |
| PRD missing | Fall back to git diff only. Note "Partial audit — no PRD context." |
| Bead directly touched memory files | Report and verify consistency with bead scope. |
| No git diff available | Note limitation. Proceed with available evidence. |
| Update exceeds size target | Warn. Offer: apply anyway / trim / skip. |
| User aborts mid-audit | Stop immediately. No edits. Report "Audit aborted. Bead still open." |
| Can't determine if drift exists | Report "Uncertain: <file> — <reason>". Ask for manual review. |
```

**Verification:** Structural tests T1-T12 pass. `grep -c "^## Phase" .omp/commands/close.md` returns 7. No code fences in the new phase body. All 5 memory files referenced. User approval directive present.

**Dependency:** None — independent of Task 1.2.

---

**Task 1.2: Update AGENTS.md Command Reference Row**

Edit `.omp/AGENTS.md` line 29 to update the `/close` row in the Command Reference table. Change the "Reads" column from `all artifacts` to `all artifacts, memory files`. Change the "Writes" column from `—` to `memory files (on user approval)`.

Current row (line 29):
```
| `/close` | Close bead, suggest next | all artifacts | — | suggest, next, capacity |
```

Target row:
```
| `/close` | Close bead, suggest next | all artifacts, memory files | memory files (on user approval) | suggest, next, capacity |
```

This is a single-line change. No other rows are touched. No other sections in AGENTS.md are modified.

**Verification:** `grep "/close" .omp/AGENTS.md | grep -q "memory files"` returns 0 (matches). The row is aligned with other table rows (column count unchanged: 5).

**Dependency:** None — independent of Task 1.1.

### Wave 2: Behavioral Verification {sequential}

Wave 2 validates the implementation against behavioral scenarios. This cannot be parallelized with Wave 1 — the implementation must exist before it can be tested.

**Task 2.1: Dry-Run Behavioral Tests**

Execute the following behavioral test scenarios sequentially. Each builds on the previous.

1. **BT-1 (No-Drift Fast Path):** Execute `/close` on a trivial bead (e.g., a previous bead that changed only README.md). Verify agent reads all 5 memory files, outputs "No drift" for each, outputs "No memory file updates needed," and proceeds to Phase 2. This is the most common scenario — it must work flawlessly.

2. **BT-2 (Drift Detected + Approve):** Execute `/close` on this bead itself. Verify agent detects drift in at least: project.md (Next field), decisions.md (Decision #6 not yet recorded), and gotchas.md (stale memory mitigation). Approve each proposal. Verify agent applies edits and proceeds to Phase 2.

3. **BT-3 (Reject All):** If BT-2 was not on this bead, create a scenario where all proposals are rejected. Verify agent STOPS, outputs the rejection message, and does NOT run `br close`. Verify `br show $BEAD_ID --json` shows bead still open.

4. **BT-4 (Partial Approval):** Create a bead with drift in 2 files. Approve one, reject the other. Verify agent applies the approved edit, documents the rejection, and proceeds to Phase 2.

5. **BT-5 (Already Current):** Verify the agent doesn't double-propose when a memory file already has the update.

6. **BT-6 (Missing File):** Temporarily move a memory file, verify agent reports missing and gates on user response.

7. **BT-7 (Size Target):** Create a proposal that would push a file past its size target, verify agent warns and offers options.

After each test, reset memory files to their pre-test state if the test was destructive.

**Verification:** All behavioral tests pass. Agent correctly follows the gating logic in all scenarios.

**Dependency:** Wave 1 must be complete.

### Wave 3: Verification + Evidence Generation {sequential}

**Task 3.1: Generate completion-evidence.json**

Run all structural tests (T1-T12). Record each result with the exact command, expected output, and actual output. Document which behavioral tests passed and how they were verified.

Generate `.beads/artifacts/$BEAD_ID/completion-evidence.json` with:
- All 13 PRD acceptance criteria, each marked passing/failing with evidence
- Structural test results (T1-T12)
- Behavioral test results (BT-1 through BT-7)
- Cross-reference to PRD AC numbers

Also verify:
- AC-10: conventions.md lines 91-94 unchanged
- AC-11: project.md "Next" field updated (happens during this bead's own /close)
- AC-12: gotchas.md mitigation text updated (happens during this bead's own /close)
- AC-13: Decision #6 recorded in decisions.md (happens during this bead's own /close)

**Verification:** All 13 ACs confirmed passing. completion-evidence.json written.

**Dependency:** Wave 2 must be complete.

## Full Verification

```bash
# === Structural Verification ===

# T1: Phase count
grep -c "^## Phase" .omp/commands/close.md
# Expected: 7

# T2: Phase 1.5 exists between Phase 1 and Phase 2
grep "^## Phase" .omp/commands/close.md
# Expected output includes: "## Phase 1: Read Review", "## Phase 1.5: Memory Audit", "## Phase 2: Close" ... "## Phase 6: Report"

# T3: All 5 memory files mentioned
grep -c "project.md\|conventions.md\|decisions.md\|gotchas.md\|tech-stack.md" .omp/commands/close.md
# Expected: >= 5

# T4: User approval directive
grep -qi "ask the user\|user approval\|do NOT proceed\|Do NOT auto-approve" .omp/commands/close.md
# Expected: 0 (match found)

# T5: Pass-through fast path
grep -qi "No memory file updates needed\|no drift.*proceed\|no updates needed" .omp/commands/close.md
# Expected: 0 (match found)

# T6: STOP condition on full rejection
grep -qi "STOP\|Do NOT proceed to Phase 2\|bead remains open" .omp/commands/close.md
# Expected: 0 (match found)

# T7: No bash code fences in new phase body
sed -n '/^## Phase 1\.5:/,/^## Phase 2:/p' .omp/commands/close.md | grep -c '```bash'
# Expected: 0

# T8: AGENTS.md row updated
grep "/close" .omp/AGENTS.md | grep "memory files"
# Expected: shows the updated row with "memory files" in Reads and Writes

# T9: Only close.md changed in commands/
git diff --stat -- .omp/commands/
# Expected: only close.md

# T10: conventions.md Memory File Maintenance section unchanged
git diff -- .omp/memory/project/conventions.md
# Expected: empty (no diff)

# T11: close.md line count in range
wc -l .omp/commands/close.md
# Expected: 170-190

# T12: Phase 1.5 contains prohibited behaviors list
grep -c "NEVER" .omp/commands/close.md
# Expected: >= 4 (at least the 4 NEVER directives in prohibited behaviors)
```

## Timeline

| Wave | Tasks | Estimated Time | Cumulative |
|------|-------|---------------|------------|
| 1 | T1.1 (close.md edit), T1.2 (AGENTS.md edit) | 15 min | 15 min |
| 2 | T2.1 (Behavioral dry-run) | 20 min | 35 min |
| 3 | T3.1 (Evidence generation) | 10 min | 45 min |

Total estimated: 45 minutes. This matches the PRD estimate.

## Risks and Mitigations (from PRD)

| Risk | Mitigation in Plan |
|------|--------------------|
| Agent hallucinates drift | Task 2.1 BT-2/3/4 test proposal quality. Every proposal shows diff before edit. User approval gate prevents application of hallucinated edits. |
| Agent misses genuine drift | Mandatory checklist forces explicit answer per file. Task 2.1 BT-2 specifically tests drift detection on a bead known to need updates (this bead). |
| Phase makes /close slower | Task 1.1 includes explicit fast-path: "No drift → 'No updates needed' → Phase 2." For no-drift beads, the only cost is reading 5 small files. |
| Phase conflicts with future changes | Phase 1.5 is self-contained between Phase 1 and Phase 2. Future phase insertions can use Phase 1.3, 1.7, 2.5, etc. without touching this phase. |
| Race condition on memory file edits | Sub-step e mandates re-reading file immediately before editing. If content changed since initial read, agent warns and re-proposes. |
| Memory files exceed size targets from audit edits | Sub-step d includes size target check (EC-8 in close.md). Agent warns before proposing edit that would exceed target. |
