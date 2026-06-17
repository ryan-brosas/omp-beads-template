<!-- DENSITY: Minimum 600 lines. No upper bound — be thorough. <600 = incomplete (missing sections, hand-wavy, no real technical context). This is an AI handoff: another agent must be able to pick this up and implement correctly without guessing. Every section must have concrete evidence: file paths, API signatures, existing patterns, constraints. -->
# PRD: Add Memory File Staleness Audit Phase to /close Command

**Bead:** br-omp-backbone-skill-close-memory-audit-tkt | **Type:** task | **Priority:** P2
**Created:** 2026-06-17 | **Estimate:** 45

## Problem

WHEN an agent runs `/close` on a completed bead THEN no memory file audit occurs BECAUSE `close.md` has zero phases that read or check memory files, despite `conventions.md`, `AGENTS.md`, and `gotchas.md` all mandating a memory audit on every close.

The `/close` command (`.omp/commands/close.md`, 74 lines, 6 phases) is the final gate in the bead lifecycle. It checks that review evidence exists (Phase 1), closes the bead in br (Phase 2), checks queue impact (Phase 3), syncs to git (Phase 4-5), and reports a summary (Phase 6). At no point does it read any of the five memory files under `.omp/memory/project/`. This is a structural gap that violates three separate project contracts:

1. **conventions.md § Memory File Maintenance** (line 92-93): "Every `/close`: agent checks if any conventions/decisions/gotchas were discovered during the bead and proposes updates."
2. **AGENTS.md § Memory Protocol Rules** (line 116): "Update on `/close` — every bead completion checks if conventions/decisions/gotchas changed"
3. **gotchas.md § Active Warnings** (line 30): "Stale memory is worse than no memory | Agents learn wrong conventions, make wrong decisions | Update on every milestone. Audit during `/close`."

The consequence is memory file drift. Without an automated checkpoint, conventions, decisions, and gotchas discovered during a bead are never surfaced for inclusion in the project's durable memory. Over multiple beads, memory files become increasingly stale — the project's self-documentation diverges from reality. Since these files are the primary context loaded by every agent session (Tier 1: `project.md` and `conventions.md` are inlined into `.omp/AGENTS.md` via `@` imports), stale memory directly degrades every subsequent agent's decision quality.

This is not hypothetical. The template already has 8 closed beads. None of them executed a memory audit at close time. Any conventions, decisions, or gotchas discovered during those beads were either manually added (if the developer remembered) or silently lost. The "stale memory is worse than no memory" gotcha is itself evidence of the pattern: the project knows this is a risk but hasn't closed the process gap.

## Scope

### In Scope
- `.omp/commands/close.md` — EDIT (~74 lines → ~180 lines): Add a new Memory Audit phase between Phase 1 (Read Review) and Phase 2 (Close)
- The new phase must read all 5 memory files and compare against bead artifacts (PRD, plan, completion-evidence)
- The new phase must detect drift in each memory file and propose specific, actionable updates
- The new phase must require explicit user approval before memory files are edited
- The new phase must gate the close: if drift is detected and user rejects ALL updates, the agent MUST NOT proceed to Phase 2
- The AGENTS.md command reference table row for `/close` must be updated to reflect the new Reads/Writes columns

### Out of Scope
- Retroactively auditing memory files for already-closed beads — forward-looking only
- Adding memory audit to `/verify`, `/review`, or `/pr` — those phases have their own purposes
- Automated memory file editing without user approval — the phase proposes, the user decides
- Changing the format or structure of any memory file — only content updates within existing sections
- Adding a `progress.txt` or `decisions.md` audit (bead-level artifacts, not project-level memory)
- A full "memory health score" or quantitative staleness metric — qualitative human-readable drift detection
- Scripting the drift detection — this is an agent reasoning task, not a script
- Adding this to `/brainstorm`, `/create`, or `/plan` — those are planning phases; memory audit belongs at close

## Requirements

| # | Requirement | Priority | Acceptance Criteria |
|---|------------|----------|---------------------|
| REQ-1 | `/close` must include a Memory Audit phase that reads all 5 project memory files before closing the bead | MUST | `grep -c "Phase.*Memory Audit\|Phase.*memory.*audit\|Phase.*Memory File" .omp/commands/close.md` returns ≥1 |
| REQ-2 | The Memory Audit phase must compare bead artifacts (PRD, plan, completion-evidence) against current memory file state to detect drift | MUST | When `/close` is executed on a bead that changed conventions, the agent must identify the gap and propose a conventions.md update before proceeding to `br close` |
| REQ-3 | The Memory Audit phase must propose specific, actionable updates for each memory file where drift is detected, showing the current content and the proposed change | MUST | The agent output during `/close` must include a diff-like display for each proposed memory file update |
| REQ-4 | The Memory Audit phase must require explicit user approval (yes/no per file) before any memory file is edited | MUST | The agent must wait for user response after proposing updates; it must not proceed to Phase 2 (Close) until all proposals are resolved |
| REQ-5 | If no drift is detected in any memory file, the phase must report "No memory file updates needed" and proceed directly to Phase 2 | MUST | On a bead with no memory-relevant changes, `/close` must still complete successfully without blocking |
| REQ-6 | If drift is detected but the user rejects ALL proposed updates, the agent must STOP and document the rejection — it must not proceed to Phase 2 | MUST | After user rejects all proposals, `br show $BEAD_ID --json` must show the bead still open (not closed) |
| REQ-7 | The phase must check each of the 5 memory files against a specific, documented checklist | MUST | The close.md command text must contain a table or checklist enumerating exactly what to check for each memory file |
| REQ-8 | The AGENTS.md command reference table must be updated to reflect `/close` now reads memory files and may write to them | MUST | The `/close` row in `.omp/AGENTS.md`'s Command Reference table must list memory files under "Reads" and "Writes" |
| REQ-9 | The new phase must be inserted between Phase 1 (Read Review) and Phase 2 (Close) without breaking existing phase numbering or flow | MUST | Phase renumbering must be consistent: old Phase 2-6 become Phase 3-7, and all internal references are updated |
| REQ-10 | The phase must handle the case where a memory file is missing or unreadable, reporting the error and asking whether to proceed | SHOULD | If `project.md` is deleted, `/close` must report "Missing: .omp/memory/project/project.md" and ask the user whether to continue or abort |

## Technical Context

**Key files:**

- `.omp/commands/close.md` — EDIT (~74 lines → ~180 lines). Current structure:
  - Bead ID Resolution block (lines 6-13)
  - Prerequisites block (lines 15-24)
  - Phase 1: Read Review (lines 28-33) — reads review-report.md
  - Phase 2: Close (lines 35-40) — `br close`
  - Phase 3: Check Queue Impact (lines 42-47) — `br ready`, `br blocked`
  - Phase 4: Sync (lines 49-54) — `br sync --flush-only`, `git commit`
  - Phase 5: Session End (lines 56-64) — `git pull --rebase`, sync, push
  - Phase 6: Report (lines 66-74) — summary output
  - No phase reads any `.omp/memory/project/` file

- `.omp/AGENTS.md` — EDIT (~272 lines, 1 row change). The Command Reference table (lines 22-31) has a `/close` row:
  ```
  | `/close` | Close bead, suggest next | all artifacts | — | suggest, next, capacity |
  ```
  The "Reads" column says "all artifacts" but does not mention memory files. The "Writes" column says "—" but the new phase will write to memory files on user approval.

- `.omp/memory/project/project.md` — READ (~24 lines). Contains Current Phase with Status, Milestone, and Next fields. The audit must check if the bead's completion changes these fields.

- `.omp/memory/project/conventions.md` — READ (~100 lines). Contains Naming, Languages, Skill Structure, Command Structure, Git, Workflow, Agent Conventions, Honcho Memory, Memory File Maintenance, and UI Design sections. The audit must check if the bead introduced new naming rules, workflow changes, or agent conventions.

- `.omp/memory/project/decisions.md` — READ (~29 lines). Contains a Decision Log table with 5 entries. The audit must check if the bead made any architecture decisions that should be recorded.

- `.omp/memory/project/gotchas.md` — READ (~43 lines). Contains Active Warnings and Template Bootstrap Gotchas tables. The audit must check if the bead discovered any pitfalls that should be documented.

- `.omp/memory/project/tech-stack.md` — READ (~65 lines). Contains Runtime, Key Dependencies, Verification Commands, Security, and Constraints sections. The audit must check if the bead changed any tool versions, dependencies, or verification commands.

**APIs / systems touched:**
- br CLI (`br close`, `br show`, `br list`, `br ready`, `br blocked`)
- git (`git diff`, `git log`)
- File system reads/writes to `.omp/memory/project/`
- Bead artifact reads from `.beads/artifacts/$BEAD_ID/`

**Existing patterns to follow:**

1. **Command phase structure**: Every phase in close.md follows this pattern:
   ```
   ## Phase N: Name
   
   Description of what to do.
   
   ```bash
   command --flags
   ```
   ```
   The new phase must follow this exact pattern.

2. **Memory file reading**: The only command that reads memory files is `/init` (`.omp/commands/init.md`), which hydrates them in Phase 2.5 and verifies them in Phase 5. The init command uses `grep` for placeholder detection — a pattern that could be adapted for staleness detection.

3. **Approval gates in commands**: Close.md already has approval gates in its Prerequisites block (lines 15-24): STOP conditions that prevent proceeding. The new phase extends this pattern with a user-interaction gate.

4. **Checklist format**: The conventions.md Memory File Maintenance table (lines 83-89) provides the canonical checklist structure — a table with File, What goes there, and When to update columns. The new phase's drift checklist should mirror this structure.

5. **Phase insertion**: No existing command inserts a phase between existing phases, so this is novel. Precedent from the template's own history: `close.md` was created from scratch in commit `bf4b40e` and has been modified several times since.

**Existing code to NOT modify:**
- `.omp/commands/brainstorm.md` — planning phase, unrelated
- `.omp/commands/create.md` — bead creation, unrelated (though it creates PRDs that the audit reads)
- `.omp/commands/plan.md` — planning, unrelated
- `.omp/commands/ship.md` — implementation, unrelated
- `.omp/commands/verify.md` — verification, unrelated
- `.omp/commands/review.md` — review, unrelated (though its report is read in Phase 1)
- `.omp/commands/pr.md` — PR creation, unrelated
- `.omp/commands/init.md` — initialization, unrelated (read for patterns only)
- `.omp/commands/git-clean.md` — cleanup, unrelated
- `.omp/extensions/workflow-gate.ts` — gate logic, unrelated to close-time audit
- `.omp/skills/` — all skills are out of scope
- `.omp/templates/` — all templates are out of scope

**Constraints:**
- The close.md file must remain a valid markdown command file — no executable code, no scripts, no machinery (per Decision #2: "Commands + skills only, no scripts")
- The phase must be deterministic enough that different agent models produce consistent results
- The phase must not add more than ~100 lines to close.md (from 74 to ~180)
- The phase must not require new tools beyond what agents already have (read, edit, bash, br, git)
- User approval mechanism must work within the chat interface — no GUI, no webhooks, no external services
- Memory files must not exceed their target sizes after updates (project.md ≤1KB, conventions.md ≤4KB, others ≤2KB per AGENTS.md lines 100-102)

**Prior art:**
- Commit `bf4b40e`: "fix: /pr → /close, human merges separately" — last structural change to close.md workflow
- Commit `927df1e`: "feat: close plugin gaps — executable /pr, multi-agent /review, security sink catalog" — last feature addition to close flow
- No prior bead has attempted memory audit at close time. `br search "memory audit"` returns only this bead.
- `bv --robot-file-beads .omp/commands/close.md` returns 0 beads — close.md has never been the primary target of any bead before.

## Approach

### Core Design: A New Phase Between Review and Close

The Memory Audit phase is inserted between Phase 1 (Read Review) and Phase 2 (Close). This placement is intentional: the review report has already confirmed the bead's work is correct, but the bead hasn't been closed yet. If memory updates are needed, they must happen before `br close` — closing the bead is the point of no return.

The phase has five sub-steps, following the pattern established by `/create`'s Phase 3 (Investigate) which also uses sub-steps (3a-3e):

**Step 1: Gather Evidence.** The agent reads the bead's artifacts to understand what changed:
- `.beads/artifacts/$BEAD_ID/prd.md` — what was supposed to change
- `.beads/artifacts/$BEAD_ID/plan.md` — what was planned (if it exists)
- `.beads/artifacts/$BEAD_ID/completion-evidence.json` — what actually happened
- The git diff for the bead's branch — what files actually changed

This gives the agent a complete picture of the bead's impact: intended scope (PRD), planned implementation (plan), actual implementation (evidence), and file-level changes (diff).

**Step 2: Read Current Memory State.** The agent reads all 5 memory files exactly as they exist on disk:
1. `.omp/memory/project/project.md`
2. `.omp/memory/project/conventions.md`
3. `.omp/memory/project/decisions.md`
4. `.omp/memory/project/gotchas.md`
5. `.omp/memory/project/tech-stack.md`

**Step 3: Detect Drift.** For each memory file, the agent compares what the bead delivered against what the file currently says. The comparison is guided by a mandatory checklist that mirrors the Memory File Maintenance table in conventions.md (lines 83-89):

| Memory File | Check |
|---|---|
| `project.md` | Does "Current Phase" > "Status", "Milestone", and "Next" still reflect reality after this bead? |
| `conventions.md` | Were any naming rules, workflow steps, skill structures, command structures, git conventions, or agent conventions introduced or changed? |
| `decisions.md` | Were any architecture decisions made during this bead that aren't recorded? |
| `gotchas.md` | Were any pitfalls, workarounds, or warnings discovered during implementation? |
| `tech-stack.md` | Were any tool versions, dependencies, or verification commands added, removed, or changed? |

The agent must answer each question explicitly. A "no" answer must be stated in the output — silence is not evidence of checking.

**Step 4: Propose Updates.** For each file where drift is detected:
- Show the current content of the relevant section (verbatim quote from the file)
- Show the proposed update (what the section should become)
- Ask: "Apply this update to `<file>`? (yes/no/skip)"

If no drift is detected in any file: output "No memory file updates needed." and proceed to Phase 2. This is the fast path — most beads won't need memory updates.

**Step 5: Apply or Reject.** For each user response:
- "yes" → edit the memory file with the proposed change, then re-read to confirm
- "no" → document that the proposal was rejected, do not edit
- "skip" → defer (e.g., "I'll handle this manually later"), document and move on

After all proposals are resolved:
- If at least one "yes": apply all approved edits, show the final diff, proceed to Phase 2
- If all proposals were "no" or "skip" with no "yes": STOP. Output "Memory audit blocked close — user rejected all proposed updates." Do NOT proceed to Phase 2. The bead remains open.

### Why This Design

**Why not a script?** Decision #2 mandates "Commands + skills only, no scripts." A Python script to detect drift would be fragile (requiring parsing of freeform markdown tables) and would add a maintenance burden. The agent's reasoning capability is better suited to detecting semantic drift than any regex-based script.

**Why not a separate `/audit-memory` command?** A standalone command would require users to remember to run it. Embedding it in `/close` makes it structural — you can't close a bead without auditing memory. This is the same reasoning behind embedding prerequisites in `/close` rather than making them a separate check.

**Why user approval for every edit?** Automated memory edits are dangerous. The agent could misunderstand what changed, hallucinate a gotcha, or propose a decision that wasn't actually made. User approval is the safety valve. This aligns with the guardrail "Ask before destructive — confirm before deleting user code."

**Why between Phase 1 and Phase 2?** Alternative placements considered:
- Before Phase 1: Can't audit without review context (need to know the bead is actually complete)
- After Phase 2: Too late — bead is already closed, can't block
- After Phase 6: Possible but would require reopening the bead to update, which is worse UX
- Between Phase 1 and Phase 2: Review is done, bead is confirmed ready, but we can still block close. This is the correct placement.

### Drift Detection Algorithm (Detailed)

The agent must perform these specific checks for each memory file. This is not a suggestion — the close.md command text will embed this as a mandatory checklist.

**project.md audit:**
1. Read the "Current Phase" section.
2. Compare "Status" against bead completion: if this bead was a major milestone, should Status change?
3. Compare "Milestone" against bead PRD: if the PRD describes a milestone, should it be recorded?
4. Compare "Next" against bead PRD: does the "Next" field still reflect the highest-priority upcoming work, or has this bead changed priorities?
5. If the bead touched project infrastructure (commands, skills, memory files, extensions), check if the project description in "The Goal" section needs refinement.

**conventions.md audit:**
1. Read all convention sections: Naming, Languages, Skill Structure, Command Structure, Git, Workflow, Agent Conventions, Honcho Memory, Memory File Maintenance, UI Design.
2. For each section, ask: did this bead add, remove, or change any convention in this category?
3. Specific triggers:
   - New command added → Command Structure section
   - Branch naming or commit format changed → Git section
   - New agent rule introduced → Agent Conventions section
   - Workflow phases added/removed/reordered → Workflow section
   - New memory file or memory rule → Memory File Maintenance section
4. Also check: does the "updated" frontmatter date reflect the current date?

**decisions.md audit:**
1. Read the Decision Log table.
2. Compare against bead PRD and plan: did this bead make an architecture decision?
3. A "decision" is: a choice between 2+ alternatives where the unchosen alternative was viable and the choice has long-term consequences.
4. Not a decision: "used a for-loop" (implementation detail), "wrote tests" (process), "fixed a bug" (repair).
5. If a decision was made: extract the next sequential #, date, decision text, rationale, and confidence.

**gotchas.md audit:**
1. Read the Active Warnings and Template Bootstrap Gotchas tables.
2. Ask: did this bead encounter unexpected behavior in the tooling, workflow, or codebase that another developer might hit?
3. A gotcha must have: Date, Area, Gotcha, Impact, Mitigation — all 5 columns.
4. Also check: are any Template Bootstrap Gotchas now stale? (E.g., if the underlying issue was fixed by a previous bead.)
5. Also check: does the "updated" frontmatter date reflect the current date?

**tech-stack.md audit:**
1. Read Runtime, Key Dependencies, Verification Commands, Security, and Constraints sections.
2. For each: did the bead add, remove, or change any entry?
3. Specific triggers:
   - New br/bv version requirement → Runtime table
   - New tool dependency → Key Dependencies table
   - New verification command → Verification Commands section
   - New constraint → Constraints section
4. Also check: does the "updated" frontmatter date reflect the current date?

### What "No Drift" Looks Like

For a typical bugfix bead that changes a single source file and adds tests:
- project.md: No change — status/milestone/next unchanged
- conventions.md: No change — no new conventions introduced
- decisions.md: No change — no architecture decisions made
- gotchas.md: No change — no new pitfalls discovered
- tech-stack.md: No change — no dependency changes

The agent outputs: "No memory file updates needed." and proceeds. This is the common case — most beads are implementation-only.

### What "Drift Detected" Looks Like

For this bead (adding a memory audit phase to /close):
- project.md: "Next" field currently says "Audit and harden the /close command to check memory file staleness on bead completion" — after this bead, that's DONE. Update "Next" to the next priority.
- conventions.md: The Memory File Maintenance "Update workflow" (lines 91-94) currently describes the audit as a manual step. After this bead, it's structural. The description should be updated.
- decisions.md: This bead makes a decision (where to insert the new phase, why not a script). Add Decision #6.
- gotchas.md: The "stale memory is worse than no memory" gotcha (line 30) can now be downgraded — there's a structural check. Update the mitigation.
- tech-stack.md: No change — no dependency changes.

Each of these is a proposed update, shown as a diff, and requires user approval.

## User Stories

### US-1: Closing a Bead That Changed Conventions

**As a** developer who just completed a bead that added a new agent convention,
**I want** `/close` to detect that conventions.md doesn't reflect the new rule,
**So that** the next agent session loads the updated convention.

**Scenario:**
- Bead `br-omp-add-retry-policy` added a "max 3 retries" convention to the workflow
- I run `/close br-omp-add-retry-policy`
- The Memory Audit phase reads conventions.md, compares against the bead's PRD
- Agent detects: "Agent Conventions section is missing 'max 3 retries before escalation'"
- Agent proposes: add `- Max 3 fix cycles — if a bug survives 3 attempts, escalate. Don't loop.` to Agent Conventions
- I approve
- Agent edits conventions.md, shows the diff, proceeds to close

### US-2: Closing a Bead That Discovered a Gotcha

**As a** developer who just completed a bead where I discovered that `bv` errors on empty repos,
**I want** `/close` to prompt me to record this as a gotcha,
**So that** future developers don't waste time debugging the same issue.

**Scenario:**
- Bead `br-omp-fix-bv-empty-repo` discovered that `bv --robot-triage` returns empty when no commits exist
- I run `/close`
- Memory Audit phase reads gotchas.md
- Agent detects: "No gotcha recorded for bv empty-repo behavior"
- Agent proposes: add a new row to the Active Warnings table with Date=2026-06, Area=bv, Gotcha="bv requires at least one commit...", Impact="Graph queries fail silently", Mitigation="Create at least one commit before relying on bv"
- I approve
- Agent edits gotchas.md, proceeds to close

### US-3: Closing a Trivial Bugfix Bead

**As a** developer who just completed a one-line typo fix,
**I want** `/close` to confirm no memory updates are needed and proceed quickly,
**So that** the close workflow isn't slowed down for trivial changes.

**Scenario:**
- Bead `br-omp-fix-typo-readme` changed one word in README.md
- I run `/close`
- Memory Audit phase reads all 5 memory files, compares against bead artifacts
- Agent detects: no drift in any file
- Agent outputs: "No memory file updates needed."
- Agent proceeds directly to Phase 2 (Close)

### US-4: Rejecting a Proposed Memory Update

**As a** developer who disagrees with the agent's proposed gotcha,
**I want** `/close` to respect my rejection and not force the update,
**So that** I maintain control over the project's durable memory.

**Scenario:**
- The agent proposes adding a gotcha I don't think is correct
- I respond "no"
- Agent documents the rejection: "Rejected: gotchas.md update for <gotcha description>"
- Agent continues checking remaining files
- If I reject ALL proposals: agent STOPS, bead remains open
- If I approve some and reject others: agent applies approved, documents rejected, proceeds to close

### US-5: Memory File Already Up to Date

**As a** developer who manually updated conventions.md during the bead,
**I want** `/close` to detect that the file is already current and not double-ask,
**So that** I don't have to reject proposals for work I already did.

**Scenario:**
- During the bead, I already added the new decision to decisions.md
- I run `/close`
- Memory Audit phase reads decisions.md
- Agent detects: the decision IS already recorded (content matches)
- Agent reports: "decisions.md: up to date (decision already recorded)"
- Agent does not propose a duplicate update

## Edge Cases

### EC-1: Memory File Is Missing
If any of the 5 memory files doesn't exist (e.g., `gotchas.md` was accidentally deleted):
- Agent reports: "Missing: .omp/memory/project/gotchas.md"
- Agent asks: "Continue without gotchas.md audit? (yes/no)"
- If yes: skip that file, audit the remaining 4
- If no: STOP, bead remains open

### EC-2: Memory File Is Malformed
If a memory file has broken markdown (e.g., table column mismatch, unterminated code fence):
- Agent reports: "Warning: .omp/memory/project/tech-stack.md appears malformed — <specific issue>"
- Agent proposes: fix the malformation as part of the audit
- User can approve the fix separately from content updates

### EC-3: PRD or Plan Doesn't Exist
If `.beads/artifacts/$BEAD_ID/prd.md` doesn't exist (possible for beads created outside /create):
- Agent reports: "Missing: PRD artifact — cannot perform full memory audit"
- Agent falls back to: git diff only (what files actually changed)
- Agent notes: "Audit is partial — no PRD context available. Memory drift detection may be incomplete."

### EC-4: Bead Touched Memory Files Directly
If the bead's git diff shows changes to `.omp/memory/project/*`:
- Agent reports: "This bead directly modified memory files. Verifying consistency..."
- Agent checks: do the direct modifications align with the bead's PRD?
- If yes: "Memory file changes consistent with bead scope."
- If no: "Warning: memory file changes may conflict with bead scope. Review manually."

### EC-5: Bead Has No Git Diff (Squash/Merge Artifact)
If `git diff` for the bead returns empty (possible if the bead's branch was squashed into main):
- Agent reports: "No git diff available — using PRD and completion-evidence only"
- Audit proceeds with available evidence, noting the limitation

### EC-6: Multiple Memory Files Need the Same Update
If a convention change affects both conventions.md AND AGENTS.md:
- Agent should detect and propose both independently
- Each gets separate user approval
- If user approves one but not the other, the approved one is applied

### EC-7: User Provides Partial Approval ("yes to project.md, no to gotchas.md")
- Agent applies the approved edit to project.md
- Agent documents the rejected gotchas.md proposal
- Agent proceeds: at least one "yes" means the audit is satisfied
- Agent reports: "Applied: project.md. Rejected: gotchas.md."

### EC-8: Memory File Update Would Exceed Size Target
If the proposed update would push a memory file past its target size (project.md >1KB, conventions.md >4KB, others >2KB per AGENTS.md lines 100-102):
- Agent warns: "Proposed update would exceed target size for conventions.md (~X bytes over)"
- Agent asks: "Apply anyway? (yes/no/trim)"
- If "trim": agent proposes a more concise version
- If "yes": applies as-is
- If "no": skips

### EC-9: Agent Can't Determine If Drift Exists
If the bead's changes are ambiguous and the agent genuinely can't tell if a memory file needs updating:
- Agent reports: "Uncertain: <file> — <specific reason for uncertainty>"
- Agent asks: "Review this file manually? Current content: <quote relevant section>"
- This is a valid outcome — better to flag uncertainty than to silently miss drift

### EC-10: User Aborts Mid-Audit
If the user says "stop" or "cancel" during the audit:
- Agent stops immediately
- No memory files are edited
- Bead remains open
- Agent reports: "Memory audit aborted by user. Bead still open."

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Agent hallucinates drift that doesn't exist, proposing spurious memory file edits | Medium | Medium — user wastes time reviewing false proposals, may accidentally approve wrong edit | Every proposal shows exact current content + proposed content as diff. User MUST approve before any edit. The "show diff before edit" protocol makes hallucination visible. |
| Agent misses genuine drift, failing to propose a needed memory update | Medium | High — memory files become stale, future agents make decisions on outdated context | Mandatory checklist forces the agent to consider each file explicitly. "No drift" must be stated, not assumed. Agent must cite specific evidence from bead artifacts. |
| Phase makes /close significantly slower, frustrating users who just want to close | Low | Medium — user friction, may skip /close or work around it | Fast path for no-drift beads: the agent reads 5 files (fast with read tool) and reports "no updates." Only slows down when drift exists, which is when the pause is warranted. |
| User approves wrong edit because the diff display is confusing | Low | High — incorrect memory file content degrades all future agent sessions | Diff format is standard unified diff (same as git diff). Agent must state "I will now edit <file> to change <X> to <Y>." before applying. |
| Phase conflicts with future close.md changes (e.g., if someone adds Phase 2.5) | Low | Low — phase insertion is mechanical, renumbering is straightforward | Insert between Phase 1 and old Phase 2. Future changes must accommodate this. This is inherent to sequential phase numbering — any phase insertion creates this risk. |
| Memory files are edited during audit by another process (race condition) | Very Low | Medium — edit applies to stale content, may lose concurrent changes | Agent re-reads the file immediately before editing. The `read` tool returns the current snapshot. If content changed since the initial read, agent warns and re-proposes. |
| The new phase violates the "Commands + skills only, no scripts" decision | None | — | The phase is pure markdown instruction, not a script. The agent reads files, reasons about drift, proposes edits — exactly what commands are designed to guide. |
| The checklists are too vague and agents interpret them inconsistently across models | Medium | Medium — different agents may detect different drift, leading to inconsistent /close behavior | Checklists use concrete, yes/no questions with specific triggers. Each file has a documented audit procedure with examples. The "What Drift Looks Like" section in the approach provides concrete scenarios. |

## Acceptance Criteria

- [ ] AC-1: `close.md` contains a new phase (between Read Review and Close) that reads all 5 memory files
    - Verify: `grep -c "Phase.*memory\|Phase.*Memory\|Phase.*Audit" .omp/commands/close.md` returns ≥1
    - Verify: The new phase appears after "Phase 1: Read Review" and before "Phase 2: Close" (or whatever Phase 2 becomes after renumbering)

- [ ] AC-2: The new phase includes a mandatory checklist enumerating what to check for each memory file
    - Verify: `grep -c "project.md\|conventions.md\|decisions.md\|gotchas.md\|tech-stack.md" .omp/commands/close.md` returns ≥5 (each memory file mentioned at least once in the audit phase)

- [ ] AC-3: The command requires explicit user approval before editing any memory file
    - Verify: The close.md text contains a directive like "Ask the user" or "Require user approval" or "Do NOT proceed until the user responds"

- [ ] AC-4: If no drift is detected, the command reports this and proceeds without blocking
    - Verify: The close.md text contains a "No memory file updates needed" or equivalent pass-through path

- [ ] AC-5: If all proposed updates are rejected, the command STOPS and does not close the bead
    - Verify: The close.md text contains a STOP condition after the audit phase when all proposals are rejected

- [ ] AC-6: Phase renumbering is consistent — old Phase 2-6 become Phase 3-7
    - Verify: `grep -c "^## Phase" .omp/commands/close.md` returns 7 (was 6, +1 for new phase)
    - Verify: Phase numbers are sequential (Phase 1, Phase 2, ..., Phase 7, no gaps)

- [ ] AC-7: AGENTS.md Command Reference table reflects memory file reads and writes for `/close`
    - Verify: The `/close` row in `.omp/AGENTS.md` line 29 has "Reads" column mentioning memory files and "Writes" column mentioning memory files (when approved)

- [ ] AC-8: No other command files are modified
    - Verify: `git diff --stat -- .omp/commands/` shows only `close.md` changed

- [ ] AC-9: The new phase does not add scripts or executable code — it's pure agent instruction
    - Verify: `grep -c '```python\|```bash\|```sh'` in the new phase section returns 0 (the only bash blocks should be pre-existing ones in other phases)

- [ ] AC-10: The Memory File Maintenance section in conventions.md does NOT need updating as part of THIS bead — it already mandates the audit; this bead implements it
    - Verify: conventions.md lines 91-94 remain unchanged after this bead (the contract is already correct; the implementation was missing)

- [ ] AC-11: The "Next" field in project.md is updated to reflect completion of this bead
    - Verify: After `/close`, `grep "Next:" .omp/memory/project/project.md` shows the next priority item, not this one

- [ ] AC-12: The gotchas.md "stale memory" entry can be updated to reference the new structural check
    - Verify: gotchas.md line 30 mitigation text mentions the /close memory audit as part of the mitigation

- [ ] AC-13: A decision is recorded in decisions.md for the design choices made in this bead
    - Verify: decisions.md contains a new Decision #6 (or next sequential) documenting the phase placement, approval protocol, and checklist design

## Design Rationale

### Why This Is a Phase, Not a Separate Command

A separate `/audit-memory` command was considered and rejected. The argument for separation: clean separation of concerns, no close.md bloat. The argument against: structural guarantees. A separate command can be skipped. The whole point of this bead is that memory audit is NOT optional — it must happen on every close. Embedding it in `/close` makes skipping it a deliberate act (ignoring a STOP condition) rather than an oversight (forgetting to run a command).

This follows the same reasoning as the prerequisites block in close.md (lines 15-24): the command itself checks its prerequisites rather than expecting the user to run a separate `/check-prerequisites` command. The cost is ~100 extra lines in close.md. The benefit is that every close, on every bead, audits memory. No exceptions.

### Why User Approval Per File, Not Batch

A single "approve all" or "reject all" prompt was considered. It's simpler and faster. But it creates an all-or-nothing dynamic: if one proposal is wrong, the user must reject all proposals to avoid it, losing good updates. Or they must accept all, including the bad one. Per-file approval lets the user accept the good proposals and reject the bad ones independently. The extra interaction cost (~1-2 user responses per file with drift) is acceptable because drift is the exception, not the rule — most beads have zero drift.

### Why Checklist Over Algorithm

A fully specified algorithm ("if PRD mentions a new dependency, check tech-stack.md row X for matching entry") was considered. It's more deterministic and would produce consistent results across models. But it's brittle: memory files have freeform markdown tables, PRDs have varying structure, and `completion-evidence.json` is a sparse format. Any algorithmic check would have a high false-positive and false-negative rate. A checklist that guides agent reasoning is more robust — the agent can read the actual content and reason about semantic drift, not just pattern-match. The cost is model-dependent consistency, but the user approval gate mitigates this: if the agent hallucinates, the user rejects.

### Why Not Also Add to /review

The `/review` command could also check memory files — it already reads artifacts and the git diff. Adding memory audit there would catch drift earlier (before /pr and /close). This was rejected because:
1. `/review` is about code quality and correctness, not project documentation
2. Adding memory audit to review would couple those concerns, making review reports longer and harder to parse
3. Memory audit requires user interaction (approval), but review is an automated parallel agent run
4. Close-time is the right moment: the bead is definitively done, all evidence is final, and the user is actively wrapping up

Future beads could add memory-health checks to `/review` as advisory (non-blocking) warnings, but the approval-gated audit belongs at close.

### Why the STOP Condition on Full Rejection

If a user rejects all memory update proposals, it means either: (a) the agent hallucinated every proposal (the audit is broken), or (b) the user is refusing to update memory that genuinely needs updating (the user is breaking the contract). In both cases, proceeding to close would violate the conventions.md mandate. The STOP is a hard gate: resolve the disagreement before closing. The user can:
- Re-run `/close` (agent may propose different updates in a fresh context)
- Manually edit the memory files to their satisfaction, then re-run `/close` (agent will detect no drift and proceed)
- Accept that memory needs updating and approve at least one proposal

This is the same pattern as the prerequisites block: "Do NOT proceed. Do NOT 'helpfully' skip ahead."

## Implementation Notes for /ship

### Exact Phase Insertion Point

The current close.md structure is:

```
Bead ID Resolution (lines 6-13)
Prerequisites (lines 15-24)
Phase 1: Read Review (lines 28-33)
Phase 2: Close (lines 35-40)
Phase 3: Check Queue Impact (lines 42-47)
Phase 4: Sync (lines 49-54)
Phase 5: Session End (lines 56-64)
Phase 6: Report (lines 66-74)
```

The target structure after this bead:

```
Bead ID Resolution (unchanged)
Prerequisites (unchanged)
Phase 1: Read Review (unchanged)
Phase 1.5: Memory Audit (NEW — ~100 lines)
  Sub-step a: Gather Evidence
  Sub-step b: Read Current Memory State
  Sub-step c: Detect Drift
  Sub-step d: Propose Updates
  Sub-step e: Apply or Reject
Phase 2: Close (was Phase 2, unchanged content, renumbered)
Phase 3: Check Queue Impact (was Phase 3, unchanged content, renumbered)
Phase 4: Sync (was Phase 4, unchanged content, renumbered)
Phase 5: Session End (was Phase 5, unchanged content, renumbered)
Phase 6: Report (was Phase 6, unchanged content, renumbered)
```

Renumbering is mechanical: Phase 2→3, Phase 3→4, Phase 4→5, Phase 5→6, Phase 6→7. All internal bash commands and references remain unchanged — only the phase header numbers change.

### AGENTS.md Table Update

Current `/close` row (line 29):
```
| `/close` | Close bead, suggest next | all artifacts | — | suggest, next, capacity |
```

Target `/close` row:
```
| `/close` | Close bead, suggest next | all artifacts, memory files | memory files (on user approval) | suggest, next, capacity |
```

This is the only change to AGENTS.md. No other rows or sections are modified.

### What the Agent Must NOT Do During Audit

The following behaviors must be explicitly prohibited in the close.md command text:
- Auto-approving proposals: the agent must never assume "yes"
- Editing memory files without showing the diff first
- Proceeding to close if any proposal was explicitly rejected (unless at least one was approved)
- Skipping the audit because "the bead was small"
- Using `honcho_remember` as a substitute for memory file updates (Honcho is complementary, not replacement)
- Proposing vague updates ("consider updating X" without concrete text)
- Proposing updates that delete user-authored content without explicit justification

### Testing the Phase

Since close.md is a markdown command (not executable code), "testing" means:
1. Structural verification: phase numbering, grep for required strings, line count
2. Dry-run execution: run `/close` on a completed bead and observe the agent's behavior
3. Drift detection accuracy: create a bead that SHOULD trigger memory updates and verify the agent detects them
4. No-drift pass-through: create a bead that should NOT trigger updates and verify the agent passes through
5. Rejection handling: reject all proposals and verify the bead remains open

These tests cannot be automated — they're behavioral tests that require an agent to execute `/close` and a human to verify the output. The completion-evidence.json for this bead will document manual verification steps.

## Migration Path

### For Existing Closed Beads

The 8 beads already closed were closed without memory audit. Their memory impact is unknown. Options:
1. **Do nothing** — accept that pre-audit beads may have left memory stale (chosen: this is out of scope)
2. **Retrospective audit** — manually review each closed bead's PRD and check if memory files should be updated
3. **One-time sweep** — create a bead specifically for auditing all closed beads

Option 1 is chosen for this bead. Options 2 and 3 are candidates for future beads if memory staleness becomes apparent.

### For the Current conventions.md Contract

The conventions.md Memory File Maintenance section (lines 79-94) currently describes the audit as a manual process in its "Update workflow" subsection. After this bead, the audit is structural — it happens automatically during `/close`. However, the conventions.md text is NOT being updated in this bead because:
1. The text is still correct: "Every `/close`: agent checks..." — it describes WHAT happens, not HOW
2. The implementation (close.md) honors the contract — no need to change the contract
3. Updating conventions.md would be a self-referential change that could confuse future readers ("wait, was this convention added by the bead that implements it?")

If future beads add new memory-related conventions, the conventions.md update workflow should be revisited. For now, the contract stands as-is.

<!-- VERIFIED: 600+ lines. All sections filled. No placeholders remain. Ready for /plan. -->
