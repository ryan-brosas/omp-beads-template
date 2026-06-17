<!-- DENSITY: Minimum 600 lines. No upper bound. Every task must include YAML metadata header, exact file paths, line numbers, old/new text shapes, verification grep commands, rollback instructions, and dependency context. -->
# Tasks: br-omp-backbone-skill-1da

```yaml
bead_id: br-omp-backbone-skill-1da
title: "Audit and fix command file consistency with conventions.md"
created: 2026-06-17
status: ready
total_tasks: 7
total_waves: 4
estimated_minutes: 14
files_touched: 3
files_created: 2
```

## Goal

Fix 11 audit-discovered inconsistencies across 3 files. Each fix is grep-verifiable and surgically minimal. No command files, skills, templates, or workflow-gate code touched.

## Wave Summary

```yaml
waves:
  - wave: 1
    file: .omp/memory/project/conventions.md
    tasks: [1.1, 1.2]
    gates: [truths 1-7, 10]
    estimated_minutes: 3
  - wave: 2
    file: .omp/AGENTS.md
    tasks: [2.1, 2.2, 2.3]
    gates: [truths 8-9, 11-12]
    estimated_minutes: 7
  - wave: 3
    file: .omp/memory/project/project.md
    tasks: [3.1]
    gates: [truth 13]
    estimated_minutes: 1
  - wave: 4
    file: all (verification only)
    tasks: [4.1, 4.2]
    gates: [truths 14-15]
    estimated_minutes: 3
```

## Dependency Graph

```
1.1 (workflow block) ──┐
                        ├── 2.1 (1KB note) ──→ 2.2 (prefix) ──→ 2.3 (tree) ──→ 3.1 (phase) ──→ 4.1 (verify) ──→ 4.2 (evidence)
1.2 (prefix)         ──┘
```

Tasks within a wave are sequential (same file, each edit depends on prior edit completing). Waves are strictly sequential — Wave N's output is Wave N+1's input file state.

---

## Task 1.1 — Replace Workflow Block in conventions.md

```yaml
task_id: "1.1"
wave: 1
file: .omp/memory/project/conventions.md
type: block_replacement
priority: P0
estimated_minutes: 2
rollback: "git checkout -- .omp/memory/project/conventions.md"
verification: [grep_absence, grep_presence, step_count]
```

### Problem

The workflow section at lines 47-55 describes a 7-step workflow that does not match the actual 8-phase lifecycle:
- Step 1 says "Triage" — should be "Brainstorm" (triage is done at every phase, not a standalone step)
- Step 2 says `/create` produces "PRD + plan + tasks" — actually produces "PRD + decisions.md"
- No `/plan` step exists — the planning phase is entirely missing from the workflow chain
- Step 3 says "Implement" — command is named `/ship`
- Step 5 says "runs parallel agents, confidence filter" — actually runs 5 agents with ≥80 confidence threshold
- Only 7 steps when 8 are needed (Brainstorm, Create, Plan, Ship, Verify, Review, PR, Close)

### Change

Replace the entire `## Workflow` block atomically. Individual line edits would create intermediate states with mismatched step numbers.

**Old text (lines 47-55 in the current file):**
```
## Workflow

1. **Triage** — `bv --robot-triage` before any action
2. **Create** — `/create` produces PRD + plan + tasks
3. **Implement** — `/ship` follows plan, no scope creep
4. **Verify** — `/verify` runs checks, records evidence
5. **Review** — `/review` runs parallel agents, confidence filter
6. **PR** — `/pr` opens PR, single-turn execution
7. **Close** — `/close` after merge, suggests next bead
```

**New text:**
```
## Workflow

1. **Brainstorm** — `/brainstorm` explores codebase, identifies work
2. **Create** — `/create` produces PRD + decisions.md
3. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md
4. **Ship** — `/ship` implements per plan, no scope creep
5. **Verify** — `/verify` runs checks, records evidence
6. **Review** — `/review` runs 5 parallel agents, confidence filter ≥80
7. **PR** — `/pr` opens PR, single-turn execution
8. **Close** — `/close` after merge, suggests next bead
```

### Audit Finding Traceability

| Finding | Fix Applied | PRD Requirement |
|---------|-------------|-----------------|
| F1: /create output wrong | "PRD + decisions.md" replaces "PRD + plan + tasks" | Req 1 (MUST) |
| F2: /brainstorm missing | Step 1 added: Brainstorm | Req 2 (MUST) |
| F3: /plan missing | Step 3 added: Plan with outputs | Req 3 (SHOULD) |
| F4: "Implement" vs "Ship" | Step 4 renamed to "Ship" | Req 9 (SHOULD) |
| F5: Review description vague | "5 parallel agents, confidence filter ≥80" | Req 5 (MAY) |
| F11: Triage mentioned | Removed as standalone step (done at every phase) | Req 8 (MUST) |
| F12: Close description | Kept as-is (no change requested for this line) | — |

### Verification Commands

```bash
# === TRUTH 1: Bug line erased ===
grep "PRD + plan + tasks" .omp/memory/project/conventions.md
# Expected: exit code 1 (no matches)

# === TRUTH 2: Correct /create output present ===
grep "PRD + decisions" .omp/memory/project/conventions.md
# Expected: 1 match — "2. **Create** — `/create` produces PRD + decisions.md"

# === TRUTH 3: /brainstorm step exists ===
grep -c "Brainstorm.*brainstorm" .omp/memory/project/conventions.md
# Expected: >= 1

# === TRUTH 4: /plan step with outputs exists ===
grep -c "Plan.*plan.*produces" .omp/memory/project/conventions.md
# Expected: >= 1

# === TRUTH 5: 8 numbered steps in workflow ===
grep -cP '^\d+\.\s+\*\*' .omp/memory/project/conventions.md
# Expected: 8 (one per step: Brainstorm, Create, Plan, Ship, Verify, Review, PR, Close)

# === TRUTH 6: "Ship" label present, "Implement" gone ===
grep -c "Ship.*ship" .omp/memory/project/conventions.md
# Expected: >= 1
grep "Implement.*ship" .omp/memory/project/conventions.md
# Expected: exit code 1 (no matches)

# === TRUTH 10: Review description accurate ===
grep "5 parallel agents.*confidence.*≥80" .omp/memory/project/conventions.md
# Expected: 1 match

# === Additional sanity: Plan outputs explicit ===
grep "plan\.md.*tasks\.md.*context-capsule" .omp/memory/project/conventions.md
# Expected: 1 match

# === Additional sanity: Workflow heading intact ===
grep "^## Workflow" .omp/memory/project/conventions.md
# Expected: 1 match

# === Additional sanity: Steps are sequential 1-8 ===
grep -A8 "^## Workflow" .omp/memory/project/conventions.md | grep -P '^\d'
# Expected: shows 1. through 8. in order
```

### Edge Cases

- **What if the file has been modified since the plan was written?** Read the current file first. If the workflow section text does not match the "old text" above, STOP and report the discrepancy.
- **What if a step number appears elsewhere in the file (e.g. in a code block)?** The numbered-step grep uses `^\d+\.\s+\*\*` which matches lines starting with a digit-dot-space-bold pattern — unique to the workflow section.
- **What if Triage should stay?** The PRD's "Should be" block shows 8 steps without Triage. Brainstorm replaces it as step 1. Triage (`bv --robot-triage`) is described in the per-phase quick reference table and is done at every phase — not a standalone workflow step.

---

## Task 1.2 — Add Bead Prefix to Naming Section in conventions.md

```yaml
task_id: "1.2"
wave: 1
file: .omp/memory/project/conventions.md
type: line_insertion
priority: P2
estimated_minutes: 1
rollback: "git checkout -- .omp/memory/project/conventions.md"
verification: [grep_presence]
depends_on: "1.1"
```

### Problem

AGENTS.md documents the bead prefix (`br-omp`) but conventions.md does not. conventions.md should be self-contained — an agent reading only conventions.md should know all naming conventions including the prefix.

### Change

Add `- **Bead prefix:** `br-omp`` after the existing bead slug line in the Naming section.

**Current text (under `## Naming`, currently line 15 area):**
```
- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, `fix-null-check`)
```

**New text:**
```
- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, `fix-null-check`)
- **Bead prefix:** `br-omp`
```

### Audit Finding Traceability

| Finding | Fix Applied | PRD Requirement |
|---------|-------------|-----------------|
| F6: No br prefix in conventions.md | New line added under Naming section | Req 7 (SHOULD) |

### Why This Location

The `## Naming` section already lists file naming conventions (kebab-case), function naming (camelCase/snake_case/PascalCase), constants, and bead slugs. The bead prefix is a naming convention — it belongs here, not in the Workflow section.

### Verification Commands

```bash
# === TRUTH 7: Prefix in conventions.md ===
grep "br-omp" .omp/memory/project/conventions.md
# Expected: at least 1 match

grep "Bead prefix" .omp/memory/project/conventions.md
# Expected: exactly 1 match

# === Sanity: Bead slugs line still present ===
grep "Bead slugs.*kebab-case" .omp/memory/project/conventions.md
# Expected: 1 match

# === Sanity: New line is adjacent to bead slugs ===
grep -A1 "Bead slugs" .omp/memory/project/conventions.md | tail -1
# Expected: "- **Bead prefix:** `br-omp`"
```

### Edge Cases

- **What if the bead slugs line has been modified?** Read current file. If the slugs line doesn't match, adapt the insertion point — the prefix line should still go right after whatever bead naming conventions exist.
- **What if the prefix already exists?** Check first: `grep "Bead prefix" .omp/memory/project/conventions.md`. If already present, skip this task (already done by someone else).

---

## Task 2.1 — Update 1KB Memory Target in AGENTS.md

```yaml
task_id: "2.1"
wave: 2
file: .omp/AGENTS.md
type: line_replacement
priority: P3
estimated_minutes: 1
rollback: "git checkout -- .omp/AGENTS.md"
verification: [grep_absence, grep_presence]
depends_on: "Wave 1 complete"
```

### Problem

AGENTS.md line 101 says "Keep each under 1KB." under Tier 1 memory. Actual current sizes: conventions.md 6,871B (6.8x over), decisions.md 1,651B, gotchas.md 3,533B, tech-stack.md 1,841B. Only project.md (1,259B) is close. A blanket, consistently-violated rule trains agents to ignore all memory guidance.

### Change

Replace with a tiered, per-file target based on actual sizes and purposes.

**Current text (line 101):**
```
Keep each under 1KB.
```

**New text:**
```
Keep each focused and concise. Target ≤1KB for project.md (vision + current phase), ≤4KB for conventions.md (workflow + naming + rules), and ≤2KB for other Tier 1 files. Prune stale entries before adding new ones.
```

### Why These Specific Targets

| File | Current Size | Purpose | Target | Rationale |
|------|-------------|---------|--------|-----------|
| project.md | 1,259 B | Vision, goals, current phase | ≤1KB | Short-lived, frequently updated — fits |
| conventions.md | 6,871 B | Naming, workflow, agent rules | ≤4KB | Dense reference — needs room for all conventions |
| decisions.md | 1,651 B | Architecture decisions | ≤2KB | Grows with project; prune old decisions |
| gotchas.md | 3,533 B | Pitfalls, warnings | ≤2KB | Needs pruning; many entries are stale |
| tech-stack.md | 1,841 B | Versions, commands | ≤2KB | Stable; changes only on dependency updates |

### Audit Finding Traceability

| Finding | Fix Applied | PRD Requirement |
|---------|-------------|-----------------|
| F9: 1KB target unrealistic | Tiered targets replace blanket rule | Req 6 (SHOULD) |

### Verification Commands

```bash
# === TRUTH 12a: Old blanket text gone ===
grep "Keep each under 1KB" .omp/AGENTS.md
# Expected: exit code 1 (no matches)

# === TRUTH 12b: New tiered guidance present ===
grep "≤1KB" .omp/AGENTS.md
# Expected: at least 1 match

grep "≤4KB" .omp/AGENTS.md
# Expected: at least 1 match

grep "≤2KB" .omp/AGENTS.md
# Expected: at least 1 match (or 2 if "other Tier 1" and "Tier 2" both have targets)

grep "Prune stale" .omp/AGENTS.md
# Expected: at least 1 match

# === Sanity: Tier 1 context still intact ===
grep "Tier 1 — Always In Context" .omp/AGENTS.md
# Expected: 1 match

# === Sanity: Memory Protocol heading still intact ===
grep "## Memory Protocol" .omp/AGENTS.md
# Expected: 1 match
```

### Edge Cases

- **What if the Tier 2 targets should also be updated?** Tier 2 says "On-Demand (load when relevant)" — no size target stated. This is correct. Tier 2 files load dynamically and don't need size caps (context window is larger on-demand). Only Tier 1 (always-in-context) needs size guidance.
- **What if a future agent sees "≤4KB" and expands conventions.md to exactly 4KB?** The target is a ceiling, not a goal. The "Keep each focused and concise" preamble and "Prune stale entries" instruction push toward smaller, not larger.

---

## Task 2.2 — Fix Bead Prefix Declaration in AGENTS.md

```yaml
task_id: "2.2"
wave: 2
file: .omp/AGENTS.md
type: line_replacement
priority: P2
estimated_minutes: 1
rollback: "git checkout -- .omp/AGENTS.md"
verification: [grep_presence, grep_absence]
depends_on: "2.1"
```

### Problem

AGENTS.md line 83 says `Prefix: omp` with examples `omp-a1b2, omp-c3d4`. Actual beads use `br-omp-backbone-skill-*` (double prefix: `br-` + `omp-`). An agent trying to resolve or create bead IDs using the documented prefix would produce wrong IDs.

### Change

Update prefix to `br-omp` and use a real bead ID as the example.

**Current text (line 83, under `## br Conventions`):**
```
- **Prefix:** `omp` (beads are `omp-a1b2`, `omp-c3d4`, ...)
```

**New text:**
```
- **Prefix:** `br-omp` (beads are `br-omp-<purpose>-<short-id>`, e.g. `br-omp-backbone-skill-1da`)
```

### Why This Format

- `br-omp` — the actual prefix br uses (confirmed via `br list --json` — all bead IDs start with `br-omp-`)
- `<purpose>-<short-id>` — documents the pattern for new beads (the purpose part explains the bead's domain)
- `br-omp-backbone-skill-1da` — a real, current bead ID, not a fabricated example

### Audit Finding Traceability

| Finding | Fix Applied | PRD Requirement |
|---------|-------------|-----------------|
| F7: Prefix wrong in AGENTS.md | `omp` → `br-omp`, stale examples replaced | Req 4 (MUST) |

### Verification Commands

```bash
# === TRUTH 8: Prefix corrected ===
grep "Prefix.*br-omp" .omp/AGENTS.md
# Expected: exactly 1 match

# === TRUTH 9: Stale examples gone ===
grep "omp-a1b2" .omp/AGENTS.md
# Expected: exit code 1

grep "omp-c3d4" .omp/AGENTS.md
# Expected: exit code 1

# === Sanity: Real example present ===
grep "br-omp-backbone-skill" .omp/AGENTS.md
# Expected: at least 1 match

# === Sanity: br Conventions heading intact ===
grep "## br Conventions" .omp/AGENTS.md
# Expected: 1 match

# === Sanity: Full br conventions block still coherent ===
grep -A12 "^## br Conventions" .omp/AGENTS.md
# Expected: shows prefix, artifacts, inspect, claim, sync, actor, one-bead, priority, notes entries
```

### Edge Cases

- **What if the br prefix actually changes in the future?** This is the documented prefix matching the current br configuration. If br config changes, a separate bead should update this line.
- **What if other files also reference `omp-a1b2`?** Check: `grep -r "omp-a1b2" .omp/`. If found in other files, those are separate bugs (out of scope for this bead). AGENTS.md is the only file with stale examples per the audit.

---

## Task 2.3 — Restructure Tree Diagram in AGENTS.md

```yaml
task_id: "2.3"
wave: 2
file: .omp/AGENTS.md
type: block_replacement
priority: P3
estimated_minutes: 5
rollback: "git checkout -- .omp/AGENTS.md"
verification: [visual_inspection, grep_structure]
depends_on: "2.2"
```

### Problem

The tree diagram at lines 191-230 has five structural issues that confuse agents about where files actually live:

1. **Missing `artifacts/<bead-id>/` in `.beads/`** — artifact files (`prd.md`, `plan.md`, etc.) appear at `│   │   ├──` depth, implying they're directly under `.beads/`. They're actually under `.beads/artifacts/<bead-id>/`.
2. **`.omp/AGENTS.md` visually under `.beads/`** — uses `│   ├──` prefix (same level as `.beads/` children), not under a separate `.omp/` branch.
3. **All `.omp/` content at `.beads/` depth** — `commands/`, `skills/`, `extensions/`, `templates/`, `memory/` all use `.beads/`-child prefix levels.
4. **CSS files incorrectly placed under `memory/project/`** — `tokens.css`, `base.css`, `primitives.css`, `craft/` are design-system assets, not memory files.
5. **Memory markdown files at wrong indentation** — `project.md`, `conventions.md`, etc. appear at root-adjacent `│       ├──` depth which doesn't match any parent branch.

### Change

Replace the entire tree block with a correctly structured version.

**Current tree:** Lines 191-230 (the full ` ``` ` fenced block including the opening and closing fences).

**New tree:**

````
```
omp-template/
├── AGENTS.md                          # Delegates to .omp/AGENTS.md
├── .beads/                            # br workspace (SQLite + JSONL)
│   ├── beads.db                       # SQLite database
│   ├── beads.jsonl                    # Append-only journal
│   └── artifacts/                     # Per-bead artifact directories
│       └── <bead-id>/                 # e.g. br-omp-backbone-skill-1da
│           ├── prd.md                 # Problem, outcome, acceptance criteria
│           ├── prd.json               # Machine-readable requirements mirror
│           ├── plan.md                # Scope, blast radius, steps, risks, verification
│           ├── tasks.md               # Ordered task list with dependencies
│           ├── decisions.md           # Architecture and design decisions
│           ├── context-capsule.md     # Handoff for the next agent
│           ├── completion-evidence.json  # Verification commands and results
│           └── review-report.md       # Parallel review findings and verdict
├── .omp/                              # OMP harness configuration
│   ├── AGENTS.md                      # Canonical project context (loaded by OMP)
│   ├── commands/                      # Slash commands (9)
│   │   ├── brainstorm.md
│   │   ├── create.md
│   │   ├── plan.md
│   │   ├── ship.md
│   │   ├── verify.md
│   │   ├── review.md
│   │   ├── pr.md
│   │   ├── close.md
│   │   └── init.md
│   ├── skills/                        # Agent skills (17)
│   │   ├── br/SKILL.md
│   │   ├── bv/SKILL.md
│   │   ├── backbone/SKILL.md
│   │   ├── orchestrator/SKILL.md
│   │   ├── design-system/
│   │   │   ├── SKILL.md               # Brand contract + craft rules
│   │   │   └── DESIGN.md              # 9-section visual language spec
│   │   └── <cognitive-tool>/SKILL.md   # decision-tree pattern
│   ├── extensions/                    # OMP tool extensions
│   │   └── workflow-gate.ts           # edit/write gating based on bead state
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── context-capsule.md
│   │   └── review-report.md
│   └── memory/project/                # Durable project knowledge
│       ├── project.md                 # Vision, goals, current phase
│       ├── conventions.md             # Naming, workflow, agent rules
│       ├── decisions.md               # Architecture decision records
│       ├── gotchas.md                 # Known pitfalls and mitigations
│       └── tech-stack.md              # Versions, verification commands, constraints
├── .gitignore
└── README.md
```
````

### Structural Changes Applied

| # | Change | Old | New |
|---|--------|-----|-----|
| 1 | `.beads/` shows actual files | Artifacts at wrong depth, no `beads.db`/`beads.jsonl` | Shows `beads.db`, `beads.jsonl`, `artifacts/` → `<bead-id>/` → files at correct 4-level depth |
| 2 | `.omp/` is separate root branch | `.omp/` content mixed at `.beads/` depth | `.omp/` is a `├──` branch under `omp-template/`, parallel to `.beads/` |
| 3 | `.omp/AGENTS.md` first under `.omp/` | Appeared at `.beads/` child depth | First entry under `.omp/` (recognizable entry point) |
| 4 | Design-system nested under skills | `design-system/SKILL.md` and `DESIGN.md` as separate skill entries | Nested under `skills/design-system/` directory |
| 5 | CSS files removed from memory | `tokens.css`, `base.css`, `primitives.css`, `craft/` under `memory/project/` | Removed (these are design assets, not memory files) |
| 6 | Memory files at correct depth | `project.md` etc. at ambiguous root-adjacent level | Under `.omp/memory/project/` at correct 3-level depth |
| 7 | Templates enumerated | Single line `prd.md, plan.md, tasks.md, review-report.md, ...` | Individual lines for each template file |
| 8 | Commands enumerated | Single line `brainstorm.md, create.md, ...` | Individual lines for each of 9 command files |

### Audit Finding Traceability

| Finding | Fix Applied | PRD Requirement |
|---------|-------------|-----------------|
| F8: Tree diagram broken | Full restructure with 8 specific fixes listed above | Req 10 (MAY) |

### Verification Commands

```bash
# === TRUTH 11a: .omp/ is a root-level branch ===
grep -c "├── .omp/" .omp/AGENTS.md
# Expected: exactly 1

# === TRUTH 11b: .omp/AGENTS.md is under .omp/ branch ===
# Read the tree and verify: the line "├── AGENTS.md" appears twice:
# - Once at root (delegates to .omp/AGENTS.md)
# - Once under .omp/ (the canonical file)
grep "├── AGENTS.md" .omp/AGENTS.md
# Expected: exactly 2 matches

# === TRUTH 11c: Artifacts at correct depth ===
grep "└── review-report.md" .omp/AGENTS.md
# Expected: 1 match (deepest leaf under artifacts/<bead-id>/)

# === TRUTH 11d: No CSS files under memory/project/ ===
grep "tokens.css" .omp/AGENTS.md
# Expected: exit code 1
grep "base.css" .omp/AGENTS.md
# Expected: exit code 1
grep "primitives.css" .omp/AGENTS.md
# Expected: exit code 1
grep "craft/" .omp/AGENTS.md
# Expected: exit code 1 (or only in skills/design-system context, not memory)

# === TRUTH 11e: beads.db and beads.jsonl present ===
grep "beads.db" .omp/AGENTS.md
# Expected: 1 match
grep "beads.jsonl" .omp/AGENTS.md
# Expected: 1 match

# === TRUTH 11f: Tree block is properly fenced ===
# Count backtick triples around the tree — should be exactly 2 (opening + closing)
grep -c '^```$' .omp/AGENTS.md
# Expected: multiple (other code blocks in the file), but tree block must have balanced fences

# === Visual verification ===
# Read the tree block and manually verify:
# - .omp/ items have │   ├── prefix (one level under omp-template/)
# - .beads/ items have │   ├── prefix (one level under omp-template/)
# - artifact files have │   │   │   ├── prefix (four levels under omp-template/)
# - memory files have │   │   ├── prefix (three levels under omp-template/)
read .omp/AGENTS.md offset=191 limit=85
```

### Edge Cases

- **What if the actual directory structure has changed since this plan?** The tree should reflect the intended structure, not necessarily every transient file. The `.gitignore` and `README.md` at root are universal. The CSS/design files exist elsewhere — they're intentionally omitted from `memory/project/`.
- **What if the number of skills or commands changes?** The counts (9 commands, 17 skills) should match reality. If they've changed, update them during the edit.
- **What about `.worktree/`?** It's gitignored and not part of the canonical repo structure — correctly absent from the tree.

---

## Task 3.1 — Update Current Phase in project.md

```yaml
task_id: "3.1"
wave: 3
file: .omp/memory/project/project.md
type: block_replacement
priority: P2
estimated_minutes: 1
rollback: "git checkout -- .omp/memory/project/project.md"
verification: [grep_presence, grep_absence]
depends_on: "Wave 2 complete"
```

### Problem

project.md's Current Phase section shows "Memory file hydration — project identity hardening" as the milestone and "Audit command files for consistency with conventions.md" as Next. The audit is now in progress (this bead), so the milestone should reflect that, and Next should point to the subsequent step.

### Change

Update the `## Current Phase` block.

**Current text (lines ~22-26):**
```
## Current Phase

- **Status:** active
- **Milestone:** Memory file hydration — project identity hardening
- **Next:** Audit command files for consistency with conventions.md
```

**New text:**
```
## Current Phase

- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md fix
```

### Why This Next Milestone

The conventions.md fix changes the workflow guidance that every agent reads. The logical next step is to verify that all phases actually work correctly when an agent follows the corrected conventions. A hands-on end-to-end test catches any remaining inconsistencies the audit missed.

### Audit Finding Traceability

| Finding | Fix Applied | PRD Requirement |
|---------|-------------|-----------------|
| F10: project.md "Next" stale | Updated to reflect current bead + next milestone | Req 11 (MAY) |

### Verification Commands

```bash
# === TRUTH 13: Current phase updated ===
grep "Command–convention consistency audit" .omp/memory/project/project.md
# Expected: exactly 1 match

grep "br-omp-backbone-skill-1da" .omp/memory/project/project.md
# Expected: exactly 1 match

grep "Workflow verification" .omp/memory/project/project.md
# Expected: exactly 1 match

# === Sanity: Old milestone gone ===
grep "Memory file hydration" .omp/memory/project/project.md
# Expected: exit code 1

# === Sanity: Old next gone ===
grep "Audit command files for consistency" .omp/memory/project/project.md
# Expected: exit code 1

# === Sanity: Section heading intact ===
grep "^## Current Phase" .omp/memory/project/project.md
# Expected: 1 match
```

### Edge Cases

- **What if project.md has been updated by someone else?** Read current file. If the Current Phase section text doesn't match the "old text" above, adapt — the key changes are (1) milestone should mention this bead, (2) Next should point to workflow verification.
- **What if the Status should change to "in_progress" or "complete"?** "active" is correct — the project is active, the audit is one milestone within it. Don't change status unless the entire project status changes.

---

## Task 4.1 — Run Full Verification Battery

```yaml
task_id: "4.1"
wave: 4
file: all (verification only — no edits)
type: verification_battery
priority: P0
estimated_minutes: 2
depends_on: "Wave 3 complete"
```

### Purpose

Confirm all 15 observable truths hold after all edits are applied. This gates `/review`, `/pr`, and `/close`.

### Step 4.1.1 — conventions.md Verification

```bash
echo "========================================"
echo "WAVE 1 VERIFICATION: conventions.md"
echo "========================================"

echo ""
echo "--- Truth 1: Bug line 'PRD + plan + tasks' erased ---"
grep "PRD + plan + tasks" .omp/memory/project/conventions.md && echo "RESULT: FAIL" || echo "RESULT: PASS"

echo ""
echo "--- Truth 2: Correct /create output 'PRD + decisions' present ---"
grep -c "PRD + decisions" .omp/memory/project/conventions.md
# Expected: 1

echo ""
echo "--- Truth 3: /brainstorm step exists ---"
grep -c "Brainstorm.*brainstorm" .omp/memory/project/conventions.md
# Expected: >= 1

echo ""
echo "--- Truth 4: /plan step with outputs exists ---"
grep -c "Plan.*plan.*produces" .omp/memory/project/conventions.md
# Expected: >= 1

echo ""
echo "--- Truth 5: 8 numbered steps in workflow ---"
grep -cP '^\d+\.\s+\*\*' .omp/memory/project/conventions.md
# Expected: 8

echo ""
echo "--- Truth 6: 'Ship' label present, 'Implement' gone ---"
grep -c "Ship.*ship" .omp/memory/project/conventions.md
# Expected: >= 1
grep "Implement.*ship" .omp/memory/project/conventions.md && echo "WARN: Implement still present" || echo "OK: Implement gone"

echo ""
echo "--- Truth 7: br-omp prefix in conventions.md ---"
grep -c "br-omp" .omp/memory/project/conventions.md
# Expected: >= 1

echo ""
echo "--- Truth 10: Review description accurate (5 agents, ≥80) ---"
grep -c "5 parallel agents.*confidence.*≥80" .omp/memory/project/conventions.md
# Expected: 1
```

### Step 4.1.2 — AGENTS.md Verification

```bash
echo ""
echo "========================================"
echo "WAVE 2 VERIFICATION: AGENTS.md"
echo "========================================"

echo ""
echo "--- Truth 8: Prefix corrected to br-omp ---"
grep -c "Prefix.*br-omp" .omp/AGENTS.md
# Expected: >= 1

echo ""
echo "--- Truth 9: Stale examples (omp-a1b2, omp-c3d4) gone ---"
grep "omp-a1b2" .omp/AGENTS.md && echo "RESULT: FAIL" || echo "RESULT: PASS"
grep "omp-c3d4" .omp/AGENTS.md && echo "RESULT: FAIL" || echo "RESULT: PASS"

echo ""
echo "--- Truth 11: Tree diagram structural checks ---"
echo "  .omp/ root branch count: $(grep -c '├── .omp/' .omp/AGENTS.md)"
echo "  AGENTS.md entries: $(grep -c '├── AGENTS.md' .omp/AGENTS.md)"
echo "  review-report.md depth: $(grep -c '└── review-report.md' .omp/AGENTS.md)"
echo "  tokens.css in tree: $(grep -c 'tokens.css' .omp/AGENTS.md)"
echo "  beads.db in tree: $(grep -c 'beads.db' .omp/AGENTS.md)"
echo "  beads.jsonl in tree: $(grep -c 'beads.jsonl' .omp/AGENTS.md)"

echo ""
echo "--- Truth 12: 1KB note updated ---"
grep "Keep each under 1KB" .omp/AGENTS.md && echo "RESULT: FAIL" || echo "RESULT: PASS"
grep -c "≤1KB" .omp/AGENTS.md
# Expected: >= 1
grep -c "Prune stale" .omp/AGENTS.md
# Expected: >= 1
```

### Step 4.1.3 — project.md Verification

```bash
echo ""
echo "========================================"
echo "WAVE 3 VERIFICATION: project.md"
echo "========================================"

echo ""
echo "--- Truth 13: Current phase updated ---"
grep -c "Command–convention consistency audit" .omp/memory/project/project.md
# Expected: 1
grep -c "br-omp-backbone-skill-1da" .omp/memory/project/project.md
# Expected: 1
grep -c "Workflow verification" .omp/memory/project/project.md
# Expected: 1

echo ""
echo "--- Old text gone ---"
grep "Memory file hydration" .omp/memory/project/project.md && echo "WARN: old milestone still present" || echo "OK: old milestone gone"
grep "Audit command files for consistency" .omp/memory/project/project.md && echo "WARN: old next still present" || echo "OK: old next gone"
```

### Step 4.1.4 — Global Verification

```bash
echo ""
echo "========================================"
echo "GLOBAL VERIFICATION"
echo "========================================"

echo ""
echo "--- Truth 14: Only 3 files changed ---"
echo "Files changed:"
git diff --name-only HEAD
echo ""
echo "Diff stat:"
git diff --stat HEAD

echo ""
echo "--- Truth 15: Valid markdown (manual) ---"
echo "Check conventions.md, AGENTS.md, project.md for:"
echo "  - Orphan backticks"
echo "  - Inconsistent heading levels"
echo "  - Broken tables"
echo "  - Unclosed code fences"

echo ""
echo "--- br lint ---"
br lint br-omp-backbone-skill-1da --json 2>&1

echo ""
echo "--- bv triage ---"
bv --robot-triage --format json 2>&1 | python3 -c "
import json, sys
d = json.load(sys.stdin)
recs = d.get('triage', {}).get('recommendations', [])
alerts = d.get('triage', {}).get('alerts', [])
print(f'Triage OK: {len(recs)} recommendations, {len(alerts)} alerts')
" 2>&1

echo ""
echo "--- br dep cycles ---"
br dep cycles --json 2>&1

echo ""
echo "========================================"
echo "VERIFICATION COMPLETE"
echo "========================================"
```

### Expected Results

| Truth | File | Check | Expected |
|-------|------|-------|----------|
| 1 | conventions.md | grep "PRD + plan + tasks" | exit 1 |
| 2 | conventions.md | grep -c "PRD + decisions" | 1 |
| 3 | conventions.md | grep -c "Brainstorm.*brainstorm" | ≥1 |
| 4 | conventions.md | grep -c "Plan.*plan.*produces" | ≥1 |
| 5 | conventions.md | grep -cP '^\d+\.\s+\*\*' | 8 |
| 6 | conventions.md | grep -c "Ship.*ship" | ≥1 |
| 7 | conventions.md | grep -c "br-omp" | ≥1 |
| 8 | AGENTS.md | grep -c "Prefix.*br-omp" | ≥1 |
| 9 | AGENTS.md | grep "omp-a1b2" | exit 1 |
| 10 | conventions.md | grep -c "5 parallel.*≥80" | 1 |
| 11 | AGENTS.md | Tree structural greps | See substeps |
| 12 | AGENTS.md | grep "Keep each under 1KB" | exit 1 |
| 13 | project.md | grep -c "Command–convention" | 1 |
| 14 | git | diff --name-only count | 3 |
| 15 | all | Manual markdown inspection | No orphans/broken fences |

---

## Task 4.2 — Write completion-evidence.json

```yaml
task_id: "4.2"
wave: 4
file: .beads/artifacts/br-omp-backbone-skill-1da/completion-evidence.json (new)
type: artifact_creation
priority: P0
estimated_minutes: 1
depends_on: "4.1"
```

### Purpose

Record all verification results in machine-readable form. Required by `/review`, `/pr`, and `/close`.

### Schema

```json
{
  "bead_id": "br-omp-backbone-skill-1da",
  "completed_at": "<ISO 8601 timestamp>",
  "truths": {
    "1": { "pass": true, "evidence": "grep 'PRD + plan + tasks' returned exit 1" },
    "2": { "pass": true, "evidence": "grep -c 'PRD + decisions' returned 1" },
    "3": { "pass": true, "evidence": "grep -c 'Brainstorm.*brainstorm' returned 1" },
    "4": { "pass": true, "evidence": "grep -c 'Plan.*plan.*produces' returned 1" },
    "5": { "pass": true, "evidence": "grep -cP '^\\d+\\.\\s+\\*\\*' returned 8" },
    "6": { "pass": true, "evidence": "grep -c 'Ship.*ship' returned >=1, 'Implement.*ship' returned exit 1" },
    "7": { "pass": true, "evidence": "grep -c 'br-omp' returned >=1" },
    "8": { "pass": true, "evidence": "grep -c 'Prefix.*br-omp' returned 1" },
    "9": { "pass": true, "evidence": "grep 'omp-a1b2' returned exit 1" },
    "10": { "pass": true, "evidence": "grep -c '5 parallel agents.*confidence.*≥80' returned 1" },
    "11": { "pass": true, "evidence": "Tree diagram structural greps all passed; manual visual inspection confirmed" },
    "12": { "pass": true, "evidence": "grep 'Keep each under 1KB' returned exit 1; '≤1KB' and 'Prune stale' present" },
    "13": { "pass": true, "evidence": "grep -c 'Command–convention consistency audit' returned 1" },
    "14": { "pass": true, "evidence": "git diff --name-only HEAD shows exactly 3 files" },
    "15": { "pass": true, "evidence": "Manual inspection: no orphan backticks, consistent heading levels, no broken tables" }
  },
  "files_changed": [
    ".omp/memory/project/conventions.md",
    ".omp/AGENTS.md",
    ".omp/memory/project/project.md"
  ],
  "git_diff_stat": "<output of git diff --stat HEAD>",
  "br_lint": { "pass": true, "output": "<br lint output>" },
  "bv_triage": { "pass": true, "issues": 1, "alerts": 0 },
  "br_dep_cycles": { "count": 0 }
}
```

### Verification

```bash
python3 -m json.tool .beads/artifacts/br-omp-backbone-skill-1da/completion-evidence.json > /dev/null && echo "JSON valid" || echo "JSON INVALID"
```
