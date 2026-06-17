<!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin — missing patterns, constraints, file ownership, or graph context that the next agent needs to execute without reading the PRD or plan. -->
# Context Capsule: br-omp-backbone-skill-1da

## Objective

Fix 11 inconsistencies between `.omp/memory/project/conventions.md`, `.omp/AGENTS.md`, and `.omp/memory/project/project.md` discovered during a per-tick pipeline audit. The primary bug: conventions.md line 50 incorrectly states `/create` produces "PRD + plan + tasks" when it actually produces only `prd.md` + `decisions.md` (the `/plan` command separately produces `plan.md` + `tasks.md` + `context-capsule.md`). This causes agents to skip `/plan` and go directly to `/ship` — losing the entire planning and wave-sequencing phase. Secondary fixes: add missing `/brainstorm` step, add missing `/plan` step, rename "Implement" to "Ship" to match command name, fix bead prefix from `omp` to `br-omp` in AGENTS.md, fix tree diagram nesting, update aspirational 1KB memory target to realistic tiered sizes, and update project.md "Current Phase" to reflect audit work.

Every fix is grep-verifiable, surgically minimal (≤5 lines changed per file), and touches no command/skill/template files. The bead is documentation-only — no code changes, no tool changes, no behavioral changes to br or bv.

### Why This Matters

When an agent loads conventions.md, it believes the workflow is:

1. Triage → 2. Create (produces PRD + plan + tasks) → 3. Implement → 4-7. Verify/Review/PR/Close

Under this belief, the agent sees `/create` as a one-stop planning command that produces everything needed. It has no reason to run `/plan` separately — the conventions say `/create` already produced the plan and tasks. So the agent proceeds directly to `/ship` after `/create`. The workflow gate blocks the edit/write tools because no plan exists for the active bead. The error message says "Run /plan first" but conventions.md says `/create` already did the plan. Confusion, loops, wasted tokens.

After this fix, conventions.md will read:

1. Brainstorm → 2. Create (produces PRD + decisions.md) → 3. Plan (produces plan.md + tasks.md + context-capsule.md) → 4-8. Ship/Verify/Review/PR/Close

The agent now knows `/create` produces a PRD and decisions, and `/plan` is a separate required phase. The workflow chain is complete, sequential, and matches actual command behavior.

### Audit Discovery Process

The PRD documents a systematic audit across 3 files:

1. Read each file line by line
2. For every line that describes command behavior, check the actual command file (e.g., if conventions.md says `/create` produces X, read `.omp/commands/create.md` and check the Writes column)
3. For every line that describes naming conventions (prefix, bead IDs), check actual data (e.g., run `br list --json` and inspect actual bead IDs)
4. For every structural claim (tree diagram), check actual file layout (`find .omp/ -type f` vs tree diagram)
5. For every guidance claim (1KB memory target), measure actual sizes (`wc -c`)

The audit found 11 discrepancies across 3 files. This bead fixes all of them.

## Key Patterns

### Pattern 1: Block Replacement Over Line-by-Line Editing

When editing a numbered list where insertions/deletions cascade step numbers, replace the entire block atomically. Individual line edits produce intermediate states with duplicate numbers.

**Example from this bead:** The 7-step workflow block in conventions.md needs:
- Step 1 (Triage) removed
- New step 1 (Brainstorm) inserted
- Step 2 text changed ("PRD + plan + tasks" → "PRD + decisions.md")
- New step 3 (Plan) inserted
- Step 3 renamed ("Implement" → "Ship")
- Step 5 text changed ("parallel agents, confidence filter" → "5 parallel agents, confidence filter ≥80")
- All steps renumbered 1-8

Attempting 7 individual line edits:
- Edit 1: Insert Brainstorm as step 1 → now have two step-1 lines (Brainstorm + Triage)
- Edit 2: Renumber Triage to step 2 → now step 2 has two entries (Triage + Create)
- ... and so on. The intermediate states are incoherent.

Block replacement:
- One edit: oldText = entire current workflow block, newText = entire corrected workflow block
- Atomic, verifiable in one step, no intermediate incoherence

**Reference:** `plan.md` task 1.2 — the complete old/new block text with exact formatting.

**When to use block replacement:**
- Numbered lists being reordered/renumbered
- Tables being restructured (column additions)
- Any contiguous region where multiple insertions affect line positions of subsequent items
- Tree diagrams or fenced code blocks (the entire block is self-contained)

**When NOT to use block replacement:**
- Single-line text changes in isolation (prefix fix, 1KB note) — use precision line edits
- Changes in different sections of the same file — separate edits for safety
- When the block is very large (>100 lines) — risk of mismatched oldText increases; consider narrowing the match window

### Pattern 2: Exact oldText From Immediate Read

Never guess oldText. Read the target lines with `read` immediately before every `edit` call. Files can change between planning and execution — another agent, a parallel worktree, or an interrupted edit cycle could modify the file between when you plan and when you execute.

**The rule:** Maximum 30 seconds between `read` and `edit` on the same file. If you get distracted, re-read.

**Example from this bead:**
```bash
# Before editing conventions.md workflow:
read .omp/memory/project/conventions.md offset=45 limit=25
# Confirm the output matches expected oldText
# Now edit — use the exact output as oldText
```

**What to read:**
- The exact lines being replaced (oldText source)
- 2-3 lines of context before and after (to confirm the edit target is correct)
- The section heading (to confirm you're in the right section)

**What NOT to do:**
- Do not use the oldText from this context-capsule or the plan — these were written at planning time and files may have changed
- Do not type oldText from memory — trailing whitespace, Unicode characters, and line endings are invisible
- Do not assume the line numbers in this capsule are still correct — offsets shift when lines are added/removed

### Pattern 3: Verification-First Workflow

After every single edit, run grep checks before proceeding. Never batch edits and verify later. If verification fails, fix immediately before the next edit.

**The rule:** Edit → Verify → Proceed. Not: Edit → Edit → Edit → Verify.

**Why this matters for this bead:** Each edit changes a file that subsequent edits depend on. If task 1.1 (prefix addition) introduces a formatting error in the Naming section, and we proceed to task 1.2 (workflow block replacement), we now have a file with two defects. Diagnosis is harder because the second edit's oldText might not match (the prefix addition shifted line numbers). Fixing one defect might require reverting both edits.

**Verification pattern for every task:**
1. Read file section → confirm expected oldText
2. Execute edit
3. Run immediate grep checks (2-5 commands)
4. If all pass → proceed to next task
5. If any fail → diagnose, fix, or rollback

### Pattern 4: Rollback on Failure

Every task has `rollback: "git checkout -- <file>"` in its YAML. If an edit produces unrecoverable state, revert and re-plan. Don't try to patch a bad edit in place.

**When to rollback:**
- The edit tool reports success but verification shows corrupted content
- The edit tool reports "oldText not found" and the file has clearly been modified since last read
- The edit produces valid content but changes wrong lines (off-by-one section)

**When NOT to rollback:**
- A grep check fails but the content is actually correct (the grep regex is wrong) — fix the verification, not the file
- A visual check reveals an unrelated pre-existing issue — note it, don't fix it (scope discipline)

### Pattern 5: No Collateral Edits

The "scope to the active bead" convention is absolute. conventions.md has a bug in its Workflow section. We fix the Workflow section. We do not:
- Clean up the Naming section's formatting (lines 10-18)
- Fix the Languages by Purpose table (if any cell is misaligned)
- Rewrite the Honcho Memory section for clarity
- Add missing entries to the Memory File Maintenance table

**The discipline:** Every line changed must map to a specific requirement in the PRD. If you find an issue not covered by the PRD, write it down for a separate bead. Do not fix it now.

**In this bead:**
- PRD Requirement 1 → conventions.md line 50 (fix /create output) → ALLOWED
- PRD Requirement 2 → conventions.md workflow section (add /brainstorm) → ALLOWED
- PRD Requirement 3 → conventions.md Naming section (add prefix) → ALLOWED
- conventions.md line 35 has a typo? → NOT ALLOWED (not in any PRD requirement)

### Pattern 6: Grep-Verifiable Truth

Every fix must be traceable to a `grep` command that unambiguously proves the fix was applied. No subjective "looks better" fixes.

**Good verification:**
```bash
grep "PRD + plan + tasks" .omp/memory/project/conventions.md
# Expected: exit code 1 (no matches) → bug line is gone
```
This is binary — the line is either present or absent. No interpretation needed.

**Bad verification:**
```
Read the file and confirm the workflow "feels right"
```
Subjective. Different agents might have different standards for "feels right."

**All 15 observable truths from the plan are grep-verifiable except Truth 11 (tree diagram visual check) and Truth 15 (markdown validity visual check).** Even Truth 11 has structural grep checks (`.omp/` branch line exists, `.beads/` branch line exists) — the "visual" part confirms nesting/indentation which grep can't verify.

## Constraints

1. **MUST NOT modify any `.omp/commands/*.md` file** — The commands are correct. conventions.md is wrong. The commands define the actual behavior; conventions.md documents it (incorrectly, currently).
2. **MUST NOT modify any `.omp/skills/*/SKILL.md` file** — Skills are unaffected by this audit. None of the skill SKILL.md files reference the workflow chain artifacts that are being corrected.
3. **MUST NOT modify `.omp/templates/*`** — Templates are correct. They define artifact structure; conventions.md describes when artifacts are produced.
4. **MUST NOT modify `.omp/extensions/workflow-gate.ts`** — The gate is correct. It blocks edit/write based on bead artifact existence, not based on what conventions.md says.
5. **MUST NOT modify `.omp/RULES.md`** — Rules are correct and unaffected.
6. **MUST NOT change the actual workflow** — Adding /brainstorm and /plan is correcting the documentation to match the actual workflow that already exists in AGENTS.md. No new workflow phase is being added. No command behavior is changing. The `/brainstorm`, `/plan`, and `/ship` commands already exist and operate exactly as their command files describe. conventions.md was simply out of sync.
7. **MUST NOT remove any sections from conventions.md, AGENTS.md, or project.md** — Only inline text replacements and block replacements. No section deletions. Every `## ` heading that exists before the edits must exist after.
8. **MUST NOT add new sections** — No new `##` headings. Prefix information goes in existing Naming section (under `## Naming`). No new memory files. No new markdown sections.
9. **MUST keep every change grep-verifiable** — Each edit must map to at least one `grep` command that unambiguously proves correctness. The 15 observable truths cover every change.
10. **MUST read before edit** — Every edit must be preceded by a `read` of the exact lines to be changed. This is a project-wide convention (AGENTS.md Guardrails: "Read before edit — never guess file content").
11. **SHOULD target ≤1KB for project.md, ≤4KB for conventions.md, ≤2KB for other Tier 1 memory files** — Per the updated AGENTS.md guidance. conventions.md is currently 6,871 bytes (~6.8KB), already over the new ≤4KB target. The workflow block replacement is roughly size-neutral (7 lines → 8 lines, similar character count). The prefix addition adds ~30 bytes. Net change is minimal — conventions.md will still be ~6.8KB. A future bead should address conventions.md bloat, but not this one.
12. **SHOULD prune stale entries before adding new ones** — Per the updated memory guidance. If a line can be removed rather than replaced, prefer removal. In this bead: the "Triage" step is removed (not replaced) because it's documented elsewhere; /brainstorm and /plan are inserted. Net: -1 line (Triage), +2 lines (Brainstorm, Plan) = +1 net line. The "Implement" label is replaced with "Ship" (same line count). Acceptable.
13. **SHOULD NOT expand conventions.md beyond its current size** — Already at 6.8KB vs. ≤4KB target. The fixes in this bead are size-neutral to size-slightly-positive. Do not add commentary, explanatory text, or "why we changed this" notes. The fixes must be self-documenting — the corrected text is the documentation.

## File Ownership

| Task | Allowed | Forbidden |
|------|---------|-----------|
| 1.1 | `.omp/memory/project/conventions.md` (Naming section, line ~15) | All other files; all other sections of conventions.md (Workflow, Languages, Skill Structure, Command Structure, Git, Agent Conventions, Honcho Memory, Memory File Maintenance, UI Design) |
| 1.2 | `.omp/memory/project/conventions.md` (Workflow section, lines 49-56) | All other files; all other sections of conventions.md |
| 2.1 | `.omp/AGENTS.md` (Tier 1 memory note, line ~101) | All other files; all other sections of AGENTS.md (Workflow, Command Reference, Workflow Enforcement, bv Capabilities, br Conventions, Memory Protocol, Honcho Operating Protocol, Skills Map, Philosophy, Guardrails) |
| 2.2 | `.omp/AGENTS.md` (br Conventions prefix bullet, line ~83) | All other files; all other sections of AGENTS.md |
| 2.3 | `.omp/AGENTS.md` (tree diagram fenced code block, lines 191-230) | All other files; all other sections of AGENTS.md |
| 3.1 | `.omp/memory/project/project.md` (Current Phase block, lines 14-18) | All other files; all other sections of project.md (The Goal, Success Criteria) |
| 4.1 | (read-only: all 3 changed files + bv/br tools) | (no writes) |
| 4.2 | (read-only: bv/br tools) | (no writes) |
| 4.3 | `.beads/artifacts/br-omp-backbone-skill-1da/completion-evidence.json` | All other files |

**Enforcement note:** The workflow-gate extension allows writes to `.omp/` and `.beads/` by default (see AGENTS.md Workflow Enforcement: "What always passes: Writing to `.beads/` and `.omp/` (workflow files)"). No bypass needed. Each task touches exactly one file and one section within it.

**Why this strict ownership matters:** conventions.md at 129 lines is the longest of the 3 target files. If task 1.2 accidentally changes a line in the Agent Conventions section instead of Workflow, it could break other conventions (e.g., the "always --json" rule). The ownership table prevents scope creep and accidental collateral damage.

## Graph Context

- **Blast radius:** 3 files (0 new, 3 edits, 0 deletes)
  - `.omp/memory/project/conventions.md` — 2 edits (prefix addition, workflow block replacement)
  - `.omp/AGENTS.md` — 3 edits (1KB note, prefix fix, tree diagram replacement)
  - `.omp/memory/project/project.md` — 1 edit (Current Phase update)

- **Related beads:** 0 — This bead is an orphan in a fully disconnected graph (0 edges across 10 nodes). No bead depends on this one; this bead depends on no other bead. This is a standalone documentation fix with no downstream blockers or upstream dependencies.

- **File history (bv --robot-file-hotspots):** No hotspots reported — 0 files with bead history. This is a template repo with no code files tracked by bv for change frequency. Memory files are documentation, not analyzed for churn.

- **Graph topology (detailed):**
  - 10 beads total in the graph
  - All beads have 0 in-degree and 0 out-degree (no edges exist between any pair)
  - All beads are orphans — no dependency edges of any kind
  - Graph density: 0.0 (no connections)
  - PageRank: uniform 0.1 across all nodes (disconnected graph property)
  - Core numbers: all 0 (no k-core structure)
  - Slack: 0 across all nodes (no slack without dependencies)
  - Cycles: none (confirmed: `br dep cycles --json` → `"cycles":[],"count":0`)
  - Topological order: 1da, l3d, nvf, 9tl, kfu, mcu, 1ct, qjk, iej, hfh
  - This is not a dependency graph — it's a flat task list where each bead is independently actionable

- **Velocity context:**
  - 9 beads closed in the last 7 days
  - Average 0.018 days to close (~26 minutes per bead)
  - All closed beads are documentation-only (template setup, hydration, workflow creation)
  - This bead is within the velocity envelope — estimated 20-30 minutes actual vs. 66 minutes bv forecast
  - Forecast is inflated because the documentation-type estimation model applies a depth factor (1.10) and uses global velocity (18 min/day per agent) rather than per-type velocity

- **No critical path:** With 0 edges, no critical path exists. This bead can be worked independently at any time. No coordination needed with other beads. No sequencing constraints.

- **Execution track (bv --robot-plan):**
  - Single track: track-A
  - Contents: [br-omp-backbone-skill-1da]
  - Total actionable: 1, total blocked: 0
  - No parallelization possible — single bead, single track
  - Work is linear: Wave 1 → Wave 2 → Wave 3 → Wave 4

- **Within-wave parallelism:** Tasks 1.1 and 1.2 touch different sections of the same file. They could theoretically be done in any order, but the plan sequences them 1.1 first because:
  - 1.1 is shorter and simpler (1 line added)
  - 1.1 verifies that the edit mechanics work correctly (oldText matching, newText formatting)
  - If 1.1 fails, we learn about edit tool issues before attempting the larger block replacement
  - The prefix addition shifts line numbers below it by +1, which could affect 1.2's oldText if we did them in reverse order — but the workflow block is far enough away that this shouldn't matter

## Implementation Notes

### File-by-File Edit Specifications

#### conventions.md — Before State (Annotated)

```
## Naming                                                    ← Section heading (unchanged)

- **Files:** `kebab-case.md`, `kebab-case.json`, ...          ← Unchanged
- **Functions:** `camelCase` (TypeScript), ...                ← Unchanged
- **Classes/Components:** `PascalCase`                        ← Unchanged
- **Constants:** `UPPER_SNAKE_CASE`                           ← Unchanged
- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, ...)  ← EDIT: append prefix line after this
                                                                NEW: - **Bead prefix:** `br-omp`
                                                                This is the task 1.1 insertion point.
                                                                Must match exactly for oldText.

... (30 lines of other content) ...

## Workflow                                                  ← Section heading (unchanged)

1. **Triage** — `bv --robot-triage` before any action          ← REMOVED (not in new chain)
2. **Create** — `/create` produces PRD + plan + tasks          ← CHANGED: "PRD + plan + tasks" → "PRD + decisions.md"
3. **Implement** — `/ship` follows plan, no scope creep        ← CHANGED: "Implement" → "Ship", renumbered
4. **Verify** — `/verify` runs checks, records evidence        ← RENUMBERED only
5. **Review** — `/review` runs parallel agents, confidence filter ← CHANGED: adds "5" + "≥80"
6. **PR** — `/pr` opens PR, single-turn execution              ← RENUMBERED only
7. **Close** — `/close` after merge, suggests next bead        ← RENUMBERED only
                                                                 NEW: step 1 (Brainstorm), step 3 (Plan)
                                                                 This ENTIRE BLOCK is replaced in task 1.2.
                                                                 oldText = from "## Workflow" to "suggests next bead"
                                                                 newText = 8-step version (see plan.md task 1.2)

## Agent Conventions                                        ← Next section (verify unchanged after edit)
```

#### conventions.md — After State (Annotated)

```
## Naming

- **Files:** `kebab-case.md`, ...
- **Functions:** `camelCase` (TypeScript), ...
- **Classes/Components:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, ...)
- **Bead prefix:** `br-omp`                                   ← ADDED by task 1.1

## Workflow

1. **Brainstorm** — `/brainstorm` explores codebase, identifies work       ← NEW step 1
2. **Create** — `/create` produces PRD + decisions.md                      ← FIXED output
3. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md     ← NEW step 3
4. **Ship** — `/ship` implements per plan, no scope creep                   ← RENAMED
5. **Verify** — `/verify` runs checks, records evidence                     ← RENUMBERED
6. **Review** — `/review` runs 5 parallel agents, confidence filter ≥80     ← UPDATED desc
7. **PR** — `/pr` opens PR, single-turn execution                           ← RENUMBERED
8. **Close** — `/close` after merge, suggests next bead                     ← RENUMBERED
```

#### AGENTS.md — Before State (Annotated, Key Sections Only)

```
## br Conventions                                              ← Section heading (unchanged)

- **Prefix:** `omp` (beads are `omp-a1b2`, `omp-c3d4`, ...)    ← EDIT task 2.2: `omp` → `br-omp`
                                                                  `omp-a1b2` → `br-omp-<purpose>-<short-id>`
                                                                  `omp-c3d4` → example using real bead ID
- **Artifacts:** `.beads/artifacts/<bead-id>/` ...              ← Unchanged
- **Inspect before mutate:** ...                                ← Unchanged
... (other br convention bullets unchanged)

---

### Tier 1 — Always In Context                                   ← Section heading (unchanged)

`@memory/project/project.md` and `@memory/project/conventions.md` ...  ← Unchanged
They are always present in the agent's context ...               ← Unchanged

Keep each under 1KB.                                             ← EDIT task 2.1: replace with tiered targets
                                                                    NEW: Target ≤1KB for project.md, ≤4KB for conventions.md,
                                                                    ≤2KB for other Tier 1 files. Prune stale entries before adding new ones.

### Tier 2 — On-Demand ...                                       ← Unchanged

---

(fenced code block with tree diagram, lines ~191-230)            ← EDIT task 2.3: replace entire tree
                                                                    Current tree has 6 issues (see plan.md appendix)
                                                                    New tree has .beads/ and .omp/ as sibling branches
```

#### AGENTS.md — After State (Key Sections)

```
- **Prefix:** `br-omp` (beads are `br-omp-<purpose>-<short-id>`, e.g. `br-omp-backbone-skill-1da`)
  → task 2.2: prefix corrected, real example used

Keep each focused and concise. Target ≤1KB for project.md (vision + current phase), ≤4KB for conventions.md (workflow + naming + rules), and ≤2KB for other Tier 1 files. Prune stale entries before adding new ones.
  → task 2.1: realistic tiered targets

(tree diagram — task 2.3: two clear branches, .beads/ and .omp/, no interleaving)
```

#### project.md — Before/After

```
Before (task 3.1 oldText):
## Current Phase
- **Status:** active
- **Milestone:** Memory file hydration — project identity hardening
- **Next:** Audit command files for consistency with conventions.md

After (task 3.1 newText):
## Current Phase
- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md fix
```

### Edit Mechanics Gotchas

1. **Box-drawing characters:** The tree diagram uses Unicode box-drawing characters (├ ─ │ └). These must be preserved exactly in oldText and newText. The edit tool uses exact string matching — if any character differs (e.g., ASCII `|` instead of Unicode `│`), the edit fails. Read the exact bytes with `read` before constructing oldText. Do not retype these characters from memory.

2. **Fenced code block boundaries:** The tree diagram is inside a ``` fenced code block. The oldText for task 2.3 must include the opening and closing ``` lines. If oldText is only the tree content without fences, the edit tool might match a different fenced block (the file has several) or fail to find a unique match. The fence delimiters provide the uniqueness constraint.

3. **Backtick handling:** Both old and new text contain backticks (e.g., `` `omp` ``, `` `br-omp` ``). In the edit tool's oldText parameter, backticks are literal characters — they are not markdown formatting and do not need escaping. However, if the tool uses backticks for string delimiting (e.g., JSON string values), ensure the encoding doesn't conflict.

4. **Multi-line oldText matching:** The edit tool matches exact text including whitespace and line endings. If the file has trailing spaces on any line, the oldText must include them. Read with `read` and use the output verbatim — do not retype. Trailing whitespace is invisible in most editors and will cause "oldText not found" errors.

5. **Edit order within a file:** Tasks 1.1 and 1.2 both edit conventions.md. If 1.1 is executed first (adding prefix line), the file content changes — the Naming section gains a line, shifting all content below by 1 line. Task 1.2's oldText (the workflow block) is in a different section (30+ lines away) and should still match exactly — the workflow block text doesn't change because of a prefix addition. But verify by re-reading the workflow section after 1.1 completes, before executing 1.2. The read-then-edit window should be tight (≤30 seconds).

6. **Section boundary detection:** When replacing "lines 49-56" (the workflow block), the exact line numbers may shift if the file has been edited. Match by content, not by line number. The oldText should be the semantic block — from `## Workflow` to the blank line before `## Agent Conventions`. Include just enough context to be unique.

7. **Unicode in general:** The tree diagram, the ≥ character, the – (en dash) in "Command–convention" — all must be exact Unicode characters. Copy from the read output, not from the plan document (which may normalize characters).

### Verification Strategy

Every task has three verification phases:

1. **Immediate verification** (run after each edit, before next task)
   - 2-8 grep commands specific to the change
   - Confirms the edit was applied correctly
   - Confirms surrounding content is unchanged
   - If any check fails: stop, diagnose, fix, re-verify

2. **Wave gate verification** (end of each wave: tasks 1.3, 2.4, 3.2)
   - Re-runs ALL immediate checks from tasks in this wave
   - Adds full-file read and visual scan
   - Adds `git diff` review to confirm only intended changes
   - Gate decision: PROCEED or STOP

3. **Global verification** (Wave 4: tasks 4.1, 4.2, 4.3)
   - All 15 observable truths from the plan
   - br/bv tool health checks
   - Completion evidence JSON assembly
   - This is the final gate before /verify

The gate pattern prevents cascading errors. If Wave 1 verification fails, we stop and fix conventions.md before touching AGENTS.md. If Wave 2 fails, we fix AGENTS.md before touching project.md. We never proceed with a known-bad file.

### Truth Mapping for /verify

The 15 observable truths map directly to acceptance criteria in the PRD:

| Truth | PRD AC # | What It Checks | Verifier |
|-------|----------|----------------|----------|
| 1 | #1 | Bug line "PRD + plan + tasks" removed from conventions.md | `grep` exit code |
| 2 | #1 | Correct "/create produces PRD + decisions.md" present | `grep -c` ≥1 |
| 3 | #2 | /brainstorm step added to workflow | `grep -c` ≥1 |
| 4 | — | /plan step with correct artifact outputs | `grep -c` ≥1 |
| 5 | #8 | 8 numbered steps (1-8) in workflow section | `sed`/grep count |
| 6 | #9 | "Ship" label replaces "Implement" | `grep -c` ≥1 and 0 |
| 7 | #3 | Bead prefix `br-omp` in conventions.md | `grep -c` ≥1 |
| 8 | #4 | AGENTS.md prefix corrected to `br-omp` | `grep -c` ≥1 |
| 9 | #4 | Stale `omp-a1b2` example removed from AGENTS.md | `grep` exit code |
| 10 | — | Review description: "5 parallel agents, confidence ≥80" | `grep -c` ≥1 |
| 11 | #5 | Tree diagram: .omp/ items under .omp/ branch | Visual + structural grep |
| 12 | #6 | 1KB note updated (aspirational → tiered targets) | `grep` exit code + presence |
| 13 | #7 | project.md Current Phase reflects audit work | `grep -c` ≥1 |
| 14 | #10 | Only 3 files changed (conventions.md, AGENTS.md, project.md) | `git diff --name-only` |
| 15 | #13 | All changed files are valid markdown | Visual scan of 3 files |

### When Things Go Wrong

**Scenario A: oldText not found by edit tool**
The file changed between planning and execution. Diagnostic steps:
1. Re-read the target lines immediately: `read <file> offset=<N> limit=<M>`
2. Compare to expected oldText from the plan — what's different?
3. If the semantic meaning is the same (minor formatting difference): construct corrected oldText from actual file content and retry
4. If the semantic meaning is different (someone already applied this fix): check if this bead is partially or fully redundant — run the verification grep checks to see which truths already hold
5. If the file is completely different (restructured since planning): stop — the plan may need revision

**Scenario B: Edit produces garbled output**
The edit succeeded (tool reported OK) but the file now has broken formatting.
1. Read the area around the edit: `read <file> offset=<N-5> limit=<M+10>`
2. Check for common issues: doubled lines, missing newlines, encoding artifacts, wrong Unicode characters
3. If fixable with a follow-up edit: do so (e.g., replace garbled line with correct one)
4. If unfixable or the cause is unclear: `git checkout -- <file>` and redo the edit
5. If the same garbling recurs: the newText may have invisible characters (zero-width spaces, non-standard line endings, mixed tabs/spaces). Reconstruct newText from the plan's exact specification, character by character if needed.

**Scenario C: Tree diagram indentation broken after edit**
Box-drawing characters look correct individually but the visual nesting is wrong.
1. Check if the edit tool normalized any whitespace (trailing spaces removed, tabs converted to spaces)
2. Check if the continuation bars (`│   `) have exactly 3 spaces after the pipe — fewer or more breaks alignment
3. Check if branch characters (`├──`, `└──`) use the correct Unicode codepoints, not ASCII fallbacks
4. If unfixable: `git checkout -- .omp/AGENTS.md` and try a broader oldText match (include Skills Map heading as anchor) to ensure the edit tool targets the right ``` block

**Scenario D: Grep verification passes but visual check reveals a problem**
Grep is necessary but not sufficient.
1. Tree diagram: grep can confirm `.omp/` branch exists, but can't verify indentation level. Visual confirmation required.
2. Markdown validity: grep can't detect orphan backticks or heading level inconsistency. Visual scan required.
3. If grep passes but visual fails: the edit is still wrong — fix it. Trust the visual check over grep for structural issues.

**Scenario E: Workflow-gate blocks the edit tool**
The gate blocks edit/write tools when required artifacts are missing.
1. Verify bead state: `br show br-omp-backbone-skill-1da --json` — status should be `in_progress`
2. If status is not `in_progress`: `br update br-omp-backbone-skill-1da --status in_progress --json`
3. If the gate blocks writing to `.omp/` files: this should not happen — `.omp/` writes are in the "always passes" list per AGENTS.md. If blocked, check the gate extension logic.
4. Emergency bypass: `OMP_SKIP_BEADS_WORKFLOW=1` (but this should not be needed)

**Scenario F: br lint fails after edits**
br lint checks bead state, not file content. Documentation edits to conventions.md/AGENTS.md/project.md should not affect br lint.
1. Check bead database integrity: `ls -la .beads/` — are beads.db and beads.jsonl present and non-empty?
2. Check this bead specifically: `br show br-omp-backbone-skill-1da --json` — are all fields populated?
3. If br lint reports missing sections (like "Acceptance Criteria"): this is an informational warning, not a blocking error. The PRD has Acceptance Criteria. br lint may be checking a different location.
4. If br lint reports database corruption: `br sync --flush-only` to flush journal to database, then retry.

## Verification Checklist (Quick Reference for /ship Agent)

Copy-paste this checklist and tick boxes as you go. This is a condensed version of tasks.md for fast scanning during execution.

### Wave 1: conventions.md

- [ ] **1.1: Read** Naming section → confirm bead slugs line matches expected
- [ ] **1.1: Edit** → append `- **Bead prefix:** `br-omp`` after bead slugs line
- [ ] **1.1: Verify** → `grep "br-omp" .omp/memory/project/conventions.md` returns ≥1, grep "Bead prefix" returns exactly 1
- [ ] **1.2: Read** Workflow section (lines 49-56 area) → confirm 7-step block matches expected oldText
- [ ] **1.2: Edit** → replace entire workflow block with 8-step version
- [ ] **1.2: Verify** → `grep "PRD + plan + tasks"` returns 0; `grep "PRD + decisions"` returns ≥1
- [ ] **1.2: Verify** → `grep "Brainstorm"` returns ≥1; `grep "Plan.*plan.*produces"` returns ≥1
- [ ] **1.2: Verify** → `grep "Ship.*ship"` returns ≥1; `grep "Implement.*ship"` returns 0
- [ ] **1.2: Verify** → `grep "5 parallel agents.*confidence.*≥80"` returns ≥1
- [ ] **1.2: Verify** → step count in workflow section = 8
- [ ] **1.2: Verify** → read full conventions.md → visual scan: no formatting damage
- [ ] **1.3: Gate** → git diff conventions.md → only Naming + Workflow changed
- [ ] **1.3: Gate** → PASS → proceed to Wave 2

### Wave 2: AGENTS.md

- [ ] **2.1: Read** Tier 1 section (line ~101) → confirm "Keep each under 1KB." is present
- [ ] **2.1: Edit** → replace with tiered targets (≤1KB, ≤4KB, ≤2KB + prune note)
- [ ] **2.1: Verify** → `grep "Keep each under 1KB"` returns 0; `grep "≤1KB"` returns ≥1
- [ ] **2.1: Verify** → `grep "≤4KB"` returns ≥1; `grep "Prune stale"` returns ≥1
- [ ] **2.2: Read** br Conventions section (line ~83) → confirm prefix line reads `omp`
- [ ] **2.2: Edit** → replace with `br-omp` + real bead example
- [ ] **2.2: Verify** → `grep "Prefix.*br-omp"` returns 1; `grep "omp-a1b2"` returns 0
- [ ] **2.2: Verify** → `grep "omp-c3d4"` returns 0
- [ ] **2.3: Read** tree diagram fenced block (lines 191-230) → confirm old tree matches expected
- [ ] **2.3: Edit** → replace entire tree block with corrected two-branch version
- [ ] **2.3: Verify** → `.omp/` branch line exists: `grep "├── .omp/" .omp/AGENTS.md`
- [ ] **2.3: Verify** → `.beads/` branch shows beads.db + beads.jsonl + artifacts/
- [ ] **2.3: Verify** → visual scan: .omp/ and .beads/ are separate sibling branches
- [ ] **2.3: Verify** → no interleaving between .beads/ and .omp/ content
- [ ] **2.4: Gate** → re-run all Wave 2 checks → all pass
- [ ] **2.4: Gate** → read full AGENTS.md → all sections intact, no collateral damage
- [ ] **2.4: Gate** → git diff AGENTS.md → only prefix, 1KB note, tree changed
- [ ] **2.4: Gate** → PASS → proceed to Wave 3

### Wave 3: project.md

- [ ] **3.1: Read** Current Phase (lines 14-18) → confirm old milestone text matches expected
- [ ] **3.1: Edit** → replace with audit milestone + workflow verification next step
- [ ] **3.1: Verify** → `grep "Command–convention consistency audit"` returns 1
- [ ] **3.1: Verify** → `grep "br-omp-backbone-skill-1da"` returns 1
- [ ] **3.1: Verify** → `grep "Workflow verification"` returns 1
- [ ] **3.1: Verify** → `grep "Memory file hydration"` returns 0 (old milestone gone)
- [ ] **3.2: Gate** → read full project.md → Goal + Success Criteria unchanged
- [ ] **3.2: Gate** → git diff project.md → only Current Phase changed
- [ ] **3.2: Gate** → PASS → proceed to Wave 4

### Wave 4: Global Verification

- [ ] **4.1: Run** all 15 truth checks → record PASS/FAIL for each
- [ ] **4.1: Failures?** → if any FAIL, stop, diagnose, fix, re-run
- [ ] **4.1: All PASS?** → proceed
- [ ] **4.2: br lint** → no errors (warning about Acceptance Criteria is OK)
- [ ] **4.2: br dep cycles** → count = 0
- [ ] **4.2: bv triage** → succeeds, returns issues
- [ ] **4.2: bv plan** → succeeds, returns tracks
- [ ] **4.3: Write** completion-evidence.json with actual results
- [ ] **4.3: Validate** JSON → `python3 -c "import json; json.load(open('...'))"` succeeds
- [ ] **4.3: br sync** → `br sync --flush-only` → no errors

## Expected Diffs (Line-by-Line)

For the /review phase, the reviewer will see these specific diffs. Use this as a pre-flight check before running git diff.

### conventions.md diff (expected ~15 lines changed)

```diff
 ## Naming
 
 - **Files:** `kebab-case.md`, ...
 - **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, `fix-null-check`)
+- **Bead prefix:** `br-omp`
 
 ## Languages by Purpose
 ...
 ## Workflow
 
-1. **Triage** — `bv --robot-triage` before any action
-2. **Create** — `/create` produces PRD + plan + tasks
-3. **Implement** — `/ship` follows plan, no scope creep
-4. **Verify** — `/verify` runs checks, records evidence
-5. **Review** — `/review` runs parallel agents, confidence filter
-6. **PR** — `/pr` opens PR, single-turn execution
-7. **Close** — `/close` after merge, suggests next bead
+1. **Brainstorm** — `/brainstorm` explores codebase, identifies work
+2. **Create** — `/create` produces PRD + decisions.md
+3. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md
+4. **Ship** — `/ship` implements per plan, no scope creep
+5. **Verify** — `/verify` runs checks, records evidence
+6. **Review** — `/review` runs 5 parallel agents, confidence filter ≥80
+7. **PR** — `/pr` opens PR, single-turn execution
+8. **Close** — `/close` after merge, suggests next bead
 
 ## Agent Conventions
```

### AGENTS.md diff (expected ~45 lines changed, mostly tree diagram)

```diff
 ## br Conventions
 
-- **Prefix:** `omp` (beads are `omp-a1b2`, `omp-c3d4`, ...)
+- **Prefix:** `br-omp` (beads are `br-omp-<purpose>-<short-id>`, e.g. `br-omp-backbone-skill-1da`)
 ...
 ### Tier 1 — Always In Context
 
 ... inlined into this file via OMP `@` imports ...
 
-Keep each under 1KB.
+Keep each focused and concise. Target ≤1KB for project.md (vision + current phase), ≤4KB for conventions.md (workflow + naming + rules), and ≤2KB for other Tier 1 files. Prune stale entries before adding new ones.
 
 ### Tier 2 — On-Demand ...
 ...
-(tree diagram: old version with interleaved .beads/.omp, missing artifacts/ nesting, misplaced CSS files, wrong prefix)
+(tree diagram: new version with separate .beads/ and .omp/ branches, correct artifacts/ nesting, no CSS in memory/)
```

### project.md diff (expected ~4 lines changed)

```diff
 ## Current Phase
 
 - **Status:** active
-- **Milestone:** Memory file hydration — project identity hardening
-- **Next:** Audit command files for consistency with conventions.md
+- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
+- **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md fix
```

## Acceptance Criteria Mapping (for /verify Agent)

The PRD lists 13 acceptance criteria. Here is the exact grep command + expected output for each:

| AC# | grep Command | Expected Output |
|-----|-------------|-----------------|
| #1 | `grep "PRD + plan + tasks" .omp/memory/project/conventions.md` | exit code 1 (no matches) |
| #2 | `grep -c "Brainstorm.*brainstorm" .omp/memory/project/conventions.md` | ≥1 |
| #3 | `grep -c "Plan.*plan.*produces" .omp/memory/project/conventions.md` | ≥1 |
| #4 | Workflow step count (sed pipeline) | 8 |
| #5 | `grep "Ship.*ship" .omp/memory/project/conventions.md` | ≥1 match |
| #6 | `grep "br-omp" .omp/memory/project/conventions.md` | ≥1 match |
| #7 | `grep "Prefix.*br-omp" .omp/AGENTS.md` | ≥1 match |
| #8 | `grep "omp-a1b2" .omp/AGENTS.md` | exit code 1 (no matches) |
| #9 | Visual: tree diagram in AGENTS.md | .omp/ branch separate from .beads/ |
| #10 | `grep "Keep each under 1KB" .omp/AGENTS.md` AND `grep "≤1KB" .omp/AGENTS.md` | exit 1 AND ≥1 |
| #11 | `grep "Command–convention consistency audit" .omp/memory/project/project.md` | ≥1 match |
| #12 | `br lint br-omp-backbone-skill-1da --json` + `bv --robot-triage --format json` | both succeed |
| #13 | Visual: read all 3 files | no orphan backticks, consistent headings |

**Execution order for AC verification:** Run AC#1-8 and AC#10-11 with grep in any order (they're independent). Then do AC#9 and AC#13 as visual checks. Finally AC#12 as the tool health check.

## Post-Completion Checklist (Before /close)

After all Waves complete and verification passes:

- [ ] All 15 observable truths are PASS
- [ ] completion-evidence.json exists and is valid JSON with all 15 truth entries
- [ ] `br sync --flush-only` has been run
- [ ] `git status` shows only the 3 expected files modified
- [ ] Agent has committed changes with conventional commit messages:
  - [ ] `docs: fix conventions.md workflow — add /brainstorm + /plan steps, correct /create output, add bead prefix`
  - [ ] `docs: fix AGENTS.md — correct br-omp prefix, tiered memory targets, restructure tree diagram`
  - [ ] `docs: update project.md — current phase reflects audit work`
- [ ] Or, if using scoped auto-commit (per br-omp-backbone-skill-qjk conventions):
  - [ ] Single commit: `docs: audit and fix command–convention consistency across 3 files (br-omp-backbone-skill-1da)`
- [ ] Bead notes updated: `COMPLETED: Fixed 11 discrepancies across conventions.md, AGENTS.md, project.md. Verified: 15/15 truths passed. NEXT: /verify`
- [ ] Ready for `/verify` → `/review` → `/pr` → `/close`

## Handoff Summary

**What this bead does:** Three documentation files get 6 surgical edits. conventions.md gets a corrected 8-step workflow with /brainstorm and /plan steps, accurate /create output, "Ship" label, and bead prefix. AGENTS.md gets correct prefix, tiered memory-size guidance, and a properly nested tree diagram with separate `.beads/` and `.omp/` branches. project.md gets an updated Current Phase reflecting audit work in progress.

**What this bead does NOT do:** Modify any command, skill, template, or extension file. Change the actual workflow behavior. Add or remove sections. Touch CSS or design-system files. Modify br database schema. Fix unrelated conventions.md formatting issues.

**For the next agent (executing /ship):**
1. Claim the bead: `br update br-omp-backbone-skill-1da --claim --json`
2. Read the current state of all 3 target files — confirm they match the "Before State" descriptions in this capsule
3. Follow tasks.md sequentially — Pre-edit read → Edit → Immediate verify → Next task
4. Do not skip Wave gates (tasks 1.3, 2.4, 3.2) — verify each wave before proceeding
5. Read before every edit — within 30 seconds of the edit call
6. Run the full 15-truth battery in Wave 4 (task 4.1) — every truth must PASS
7. Write completion-evidence.json with actual, observed verification results (task 4.3)
8. Run `br sync --flush-only`
9. Ready for /verify and /review

**Estimated actual time:** 20-30 minutes (6 edits × ~2 min each + verification). bv forecast: 66 minutes (inflated by documentation-type model). This is a fast bead — the bottleneck is reading and verifying, not editing.

**Risk level:** Low. Documentation-only, no code changes, no tool changes. Worst case: `git checkout -- <file>` for any of the 3 files. The only complexity is the tree diagram restructure (task 2.3) which requires careful box-drawing character handling.
