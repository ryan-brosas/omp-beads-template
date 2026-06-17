<!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin (waves undefined, tasks lack code outlines, verification hand-wavy). Task outlines should show the shape of every file change — not full implementation, but enough that a different agent can execute without reading the PRD again. -->
# Plan: br-omp-backbone-skill-1da

**Goal:** Fix 11 audit-discovered inconsistencies across conventions.md (workflow, prefix, /brainstorm), AGENTS.md (prefix, tree diagram, 1KB memory target), and project.md (current phase) — each fix grep-verifiable, surgically minimal, no command/skill/template files touched.

## Graph Context

- **Blast radius:** 3 files (0 new, 3 edits, 0 deletes)
- **Unblocks:** None — all beads in this graph are orphans (0 edges total across 10 nodes)
- **Blocked by:** None — no dependencies, no parent beads
- **Critical path:** No — orphan node in a disconnected graph; no downstream work waits on this bead
- **Forecast:** 66 minutes (confidence 0.4) — low confidence due to documentation-only estimate model; actual work is ~10 grep/read/edit operations, realistically 20-30 minutes
- **Hotspots touched:** None — bv reports 0 files with bead history (this is a template repo with no code files tracked)

**Graph metrics (bv --robot-insights):**
- Node count: 10, Edge count: 0, Density: 0
- All nodes are orphans — no blocking edges, no dependency chains
- No cycles (confirmed via `br dep cycles --json`: `"cycles":[]`, `"count":0`)
- All PageRank values: 0.1 (uniform across disconnected graph)
- All core numbers: 0 (no k-core structure)
- Slack: 0 across all nodes
- Velocity: 9 closed in 7 days, avg 0.018 days to close (sub-hour ticket times — documentation-only beads)

**Execution tracks (bv --robot-plan):**
- Single track (track-A): only `br-omp-backbone-skill-1da` in the actionable set
- No items unblock others — immediate execution, no parallelization needed internally

## Observable Truths

1. `grep "PRD + plan + tasks" .omp/memory/project/conventions.md` returns 0 matches (the bug line is gone)
2. `grep "PRD + decisions" .omp/memory/project/conventions.md` returns ≥1 matches (correct /create output)
3. `grep -c "Brainstorm.*brainstorm" .omp/memory/project/conventions.md` returns ≥1 (/brainstorm step exists)
4. `grep -c "Plan.*plan.*produces" .omp/memory/project/conventions.md` returns ≥1 (/plan step with outputs)
5. conventions.md workflow section has exactly 8 numbered steps (1-8), not 7
6. `grep "Ship.*ship" .omp/memory/project/conventions.md` returns ≥1 ("Ship" replaces "Implement")
7. `grep "br-omp" .omp/memory/project/conventions.md` returns ≥1 (prefix documented)
8. `grep "Prefix.*br-omp" .omp/AGENTS.md` returns ≥1 (AGENTS.md prefix fixed)
9. `grep "omp-a1b2" .omp/AGENTS.md` returns 0 (stale example gone)
10. `grep "5 parallel agents.*confidence.*80" .omp/memory/project/conventions.md` returns ≥1 (review description accurate)
11. AGENTS.md tree diagram: `.omp/` items are visually nested under `.omp/` branch, not interleaved with `.beads/` items
12. `grep "1KB" .omp/AGENTS.md` — updated text no longer reads "Keep each under 1KB" without qualification
13. project.md `Current Phase` reads "Command–convention consistency audit" or equivalent
14. `git diff --stat` shows only 3 files changed: conventions.md, AGENTS.md, project.md
15. All memory files remain valid markdown — no orphan backticks, consistent heading levels

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| conventions.md (fixed) | Corrected workflow, prefix, brainstorm step | `.omp/memory/project/conventions.md` | Edit |
| AGENTS.md (fixed) | Corrected prefix, tree diagram, 1KB note | `.omp/AGENTS.md` | Edit |
| project.md (updated) | Current phase reflecting audit | `.omp/memory/project/project.md` | Edit |
| completion-evidence.json | Verification results for all 15 acceptance criteria | `.beads/artifacts/br-omp-backbone-skill-1da/completion-evidence.json` | New |

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7 | Sequential (same file) | PRD approved, bead claimed | conventions.md grep checks pass (criteria 1-7, 10) |
| 2 | 2.1, 2.2, 2.3 | Sequential (same file) | Wave 1 verified | AGENTS.md grep checks + visual tree check pass (criteria 8-9, 11-12) |
| 3 | 3.1 | Immediate | Wave 2 verified | project.md reads correctly (criterion 13) |
| 4 | 4.1 | Immediate | Wave 3 verified | All 15 truths confirmed, br lint clean, git diff correct |

## Tasks

### Wave 1: conventions.md — Workflow Correction + Brainstorm + Prefix

**Target file:** `.omp/memory/project/conventions.md` (129 lines, 6,871 bytes)

All Wave 1 tasks edit the same file. They are described separately for clarity but can be executed as one coordinated edit (matching exact old text for each replacement). The PRD identifies lines 49-56 as the workflow section. Six separate edits are needed:

#### Task 1.1: Fix /create artifact output (line 50)

Change the Create step description from "produces PRD + plan + tasks" to "produces PRD + decisions.md". The current line reads:

```
2. **Create** — `/create` produces PRD + plan + tasks
```

Replace with:

```
2. **Create** — `/create` produces PRD + decisions.md
```

```
# Edit shape:
oldText: "2. **Create** — `/create` produces PRD + plan + tasks"
newText: "2. **Create** — `/create` produces PRD + decisions.md"
```

**Verification:** `grep "PRD + plan + tasks" .omp/memory/project/conventions.md` returns 0 matches. `grep "PRD + decisions" .omp/memory/project/conventions.md` returns ≥1.

#### Task 1.2: Insert /brainstorm as first step

Insert a new step before the current step 1. The workflow should start with Brainstorm. The current step 1 is:

```
1. **Triage** — `bv --robot-triage` before any action
```

Insert before it:

```
1. **Brainstorm** — `/brainstorm` explores codebase, identifies work
```

This shifts Triage to step 2, Create to step 3, etc.

```
# Edit shape — insert before the Triage line:
oldText: "1. **Triage** — `bv --robot-triage` before any action"
newText: "1. **Brainstorm** — `/brainstorm` explores codebase, identifies work\n2. **Triage** — `bv --robot-triage` before any action"
```

Note: This is a multi-phase edit. Step numbers cascade through all subsequent steps. Rather than 7 separate edits, the entire workflow block is replaced as one coordinated change in the final edit below (Task 1.7 handles renumbering).

**Verification:** `grep -c "Brainstorm.*brainstorm" .omp/memory/project/conventions.md` returns ≥1.

#### Task 1.3: Insert /plan step after Create

After the (now step 3) Create step, insert a Plan step:

```
3. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md
```

```
# Edit shape — insert after the Create line:
oldText: "2. **Create** — `/create` produces PRD + decisions.md"
newText: "2. **Create** — `/create` produces PRD + decisions.md\n3. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md"
```

**Verification:** `grep -c "Plan.*plan.*produces" .omp/memory/project/conventions.md` returns ≥1. `grep "plan\.md.*tasks\.md.*context-capsule" .omp/memory/project/conventions.md` returns ≥1.

#### Task 1.4: Rename "Implement" to "Ship"

The current step says `3. **Implement** — /ship follows plan, no scope creep`. Rename to `Ship` to match the command name:

```
# Edit shape:
oldText: "**Implement** — `/ship` follows plan, no scope creep"
newText: "**Ship** — `/ship` implements per plan, no scope creep"
```

Note: The exact step number depends on prior edits. Match on the text content, not the number.

**Verification:** `grep "Ship.*ship" .omp/memory/project/conventions.md` returns ≥1. `grep "Implement.*ship" .omp/memory/project/conventions.md` returns 0.

#### Task 1.5: Update Review description

Current line says `runs parallel agents, confidence filter`. Update to match the actual `/review` command behavior (5 parallel agents, confidence ≥80):

```
# Edit shape:
oldText: "**Review** — `/review` runs parallel agents, confidence filter"
newText: "**Review** — `/review` runs 5 parallel agents, confidence filter ≥80"
```

**Verification:** `grep "5 parallel agents.*confidence.*80" .omp/memory/project/conventions.md` returns ≥1.

#### Task 1.6: Add bead prefix information

Add a prefix declaration near the Naming section (around line 15-18). The file currently has:

```
- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, `fix-null-check`)
```

Add after it:

```
- **Bead prefix:** `br-omp`
```

```
# Edit shape:
oldText: "- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, `fix-null-check`)"
newText: "- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, `fix-null-check`)\n- **Bead prefix:** `br-omp`"
```

**Verification:** `grep "br-omp" .omp/memory/project/conventions.md` returns ≥1.

#### Task 1.7: Renumber workflow steps 1-8

After all insertions/deletions above, the workflow section must have exactly 8 steps, numbered 1-8. The final expected block:

```
1. **Brainstorm** — `/brainstorm` explores codebase, identifies work
2. **Triage** — `bv --robot-triage` before any action
3. **Create** — `/create` produces PRD + decisions.md
4. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md
5. **Ship** — `/ship` implements per plan, no scope creep
6. **Verify** — `/verify` runs checks, records evidence
7. **Review** — `/review` runs 5 parallel agents, confidence filter ≥80
8. **PR** — `/pr` opens PR, single-turn execution
9. **Close** — `/close` after merge, suggests next bead
```

Wait — that's 9 steps. But the PRD says "renumber steps 1-7 to 1-8 (adding /brainstorm)". Let me check: original had 7 steps (Triage, Create, Implement, Verify, Review, PR, Close). Adding Brainstorm makes it 8: Brainstorm, Triage, Create, Plan, Ship, Verify, Review, PR, Close = 9. But the PRD says 8. Let me re-examine.

The PRD Requirements table:
- Req 8: "conventions.md Workflow: renumber steps 1-7 to 1-8 (adding /brainstorm)" — MUST

But the /plan step is also being added (Req 2: "add /brainstorm as entry point" and implicitly adding /plan). The original has 7 steps. Brainstorm + Plan = 2 new steps. 7 + 2 = 9. But the PRD says renumber 1-7 to 1-8. This is a discrepancy in the PRD itself. Let me check again.

Looking at the PRD's "Should be" section:
```
1. **Brainstorm** — `/brainstorm` explores codebase, identifies work
2. **Create** — `/create` produces PRD + decisions.md
3. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md
4. **Ship** — `/ship` implements per plan, no scope creep
5. **Verify** — `/verify` runs checks, records evidence
6. **Review** — `/review` runs 5 parallel agents, confidence filter ≥80
7. **PR** — `/pr` opens PR, single-turn execution
8. **Close** — `/close` after merge, suggests next bead
```

That's 8 steps! And the Triage step has been removed from the workflow chain. The PRD says Brainstorm replaces Triage as step 1 in the chain (since brainstorm includes triage implicitly, and `bv --robot-triage` is done at every phase per AGENTS.md). The PRD's "Should be" block shows 8 steps without a separate Triage step.

So the workflow goes: Brainstorm → Create → Plan → Ship → Verify → Review → PR → Close = 8 steps. The Triage line is removed or folded into Brainstorm.

But wait — re-reading the PRD Requirements table:
- Req 1: change /create output
- Req 2: add /brainstorm as entry point (step 0 or step 1) before /create

And the "Should be" block doesn't have Triage as a separate step. Let me verify:
- Original: 1. Triage, 2. Create, 3. Implement, 4. Verify, 5. Review, 6. PR, 7. Close
- Target: 1. Brainstorm, 2. Create, 3. Plan, 4. Ship, 5. Verify, 6. Review, 7. PR, 8. Close

So Triage is removed as a standalone workflow step. Added: Brainstorm, Plan. Total: 7 - 1 (Triage) + 2 (Brainstorm, Plan) = 8.

But the PRD Requirements table says "renumber steps 1-7 to 1-8 (adding /brainstorm)". That suggests adding brainstorm makes it 8. But adding brainstorm AND plan makes it 9 (if Triage stays). Since Triage is removed and the "Should be" block shows 8 steps, I'll follow the exact "Should be" block from the PRD.

Actually, I need to be careful. Let me re-read the PRD more carefully:

The PRD says:
**Should be:**
```
1. **Brainstorm** — `/brainstorm` explores codebase, identifies work
2. **Create** — `/create` produces PRD + decisions.md
3. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md
4. **Ship** — `/ship` implements per plan, no scope creep
5. **Verify** — `/verify` runs checks, records evidence
6. **Review** — `/review` runs 5 parallel agents, confidence filter ≥80
7. **PR** — `/pr` opens PR, single-turn execution
8. **Close** — `/close` after merge, suggests next bead
```

That's the authoritative target. 8 steps. Triage is removed. I'll match this exactly.

The PRD text also mentions "Add Prefix info: New line — Bead prefix: `br-omp`" — but the prefix should go in conventions.md near the naming section. Looking at the existing Naming section, bead slugs are at line ~15. I'll add prefix there.

OK, let me now write the full plan. I realize the plan should show the exact old/new text for the full workflow block as one coordinated replacement rather than separate edits, since step numbers cascade. Let me restructure the plan to reflect this practical constraint.

Actually, continuing with the plan outline — the specific edit for the final workflow block needs careful oldText/newText. Let me think about what the exact old block is:

Current (lines 49-56 in conventions.md):
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

Should become:
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

This is a single block replacement. All 7 workflow fix tasks collapse into one edit. The prefix addition (task 1.6) is a separate edit on a different part of the file.

So effectively Wave 1 is two edits to conventions.md:
- Edit A: Replace workflow block (accomplishes tasks 1.1-1.5, 1.7)
- Edit B: Add bead prefix to Naming section (task 1.6)

And I still need to verify:
- Req 1 (PRD "MUST"): `grep "PRD + decisions" .omp/memory/project/conventions.md` → the installed block has `PRD + decisions.md` so this passes
- Req 2 (PRD "MUST"): `grep -i "brainstorm" .omp/memory/project/conventions.md` → step 1 in the block
- Req 3 (PRD "SHOULD"): `grep "Prefix" .omp/memory/project/conventions.md` → from Edit B
- Req 8 (PRD "MUST"): Steps flow 1-8 with brainstorm as step 1 → the installed block
- Req 9 (PRD "SHOULD"): Step reads "Ship — /ship implements..." → step 4 in the block

Good. Let me now write the full plan.md. I need to keep it dense and detailed with exact code outlines for every change.

Let me write this properly now.</think>

<｜DSML｜tool_calls>
<｜DSML｜invoke name="write">
<｜DSML｜parameter name="content" string="true"><!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin (waves undefined, tasks lack code outlines, verification hand-wavy). Task outlines should show the shape of every file change — not full implementation, but enough that a different agent can execute without reading the PRD again. -->
# Plan: br-omp-backbone-skill-1da

**Goal:** Fix 11 audit-discovered inconsistencies across conventions.md (workflow, prefix, /brainstorm), AGENTS.md (prefix, tree diagram, 1KB memory target), and project.md (current phase) — each fix grep-verifiable, surgically minimal, no command/skill/template files touched.

## Graph Context

- **Blast radius:** 3 files (0 new, 3 edits, 0 deletes)
- **Unblocks:** None — all beads in this graph are orphans (0 edges total across 10 nodes)
- **Blocked by:** None — no dependencies, no parent beads; orphan node in a fully disconnected graph
- **Critical path:** No — 0 downstream dependents; no work waits on this bead
- **Forecast:** 66 minutes (confidence 0.4) — low confidence due to documentation-only estimate model; actual work is ~10 grep/read/edit operations, realistically 20-30 minutes
- **Hotspots touched:** None — bv reports 0 files with bead history (template repo, no tracked code files)

**Graph metrics (bv --robot-insights, 2026-06-17):**
- Node count: 10, Edge count: 0, Density: 0.0
- All nodes are orphans — no blocking edges, no dependency chains
- No cycles (confirmed: `br dep cycles --json` → `"cycles":[]`, `"count":0`)
- PageRank: uniform 0.1 across all 10 nodes (fully disconnected egalitarian)
- Core numbers: all 0 (no k-core structure, no embedded subgraphs)
- Slack: 0 across all nodes (no float possible when everything is disconnected)
- Velocity: 9 closed in 7 days, avg 0.018 days to close (~26 minutes per bead)
- Topological order: 1da, l3d, nvf, 9tl, kfu, mcu, 1ct, qjk, iej, hfh (alphabetical by short ID)

**Execution tracks (bv --robot-plan):**
- Single track (track-A): only `br-omp-backbone-skill-1da` is actionable
- Total actionable: 1, total blocked: 0
- Highest impact: br-omp-backbone-skill-1da (no downstream, so no unlock multiplier)
- No parallelization needed or possible — single-threaded work

**Advanced insights:**
- `topk_set`: br-omp-backbone-skill-1da (marginal gain 0 — no edges to unlock)
- `coverage_set`: "No blocking edges to cover" — ratio 1.0
- `cycle_break`: "No cycles detected - dependency graph is a proper DAG"
- `parallel_cut`: max_parallel=1
- `k_paths`: n/a (0-length paths in edgeless graph)

## Observable Truths

1. `grep "PRD + plan + tasks" .omp/memory/project/conventions.md` returns 0 matches (the bug line is erased)
2. `grep "PRD + decisions" .omp/memory/project/conventions.md` returns ≥1 matches (correct /create output is present)
3. `grep -c "Brainstorm.*brainstorm" .omp/memory/project/conventions.md` returns ≥1 (/brainstorm exists as workflow step)
4. `grep -c "Plan.*plan.*produces" .omp/memory/project/conventions.md` returns ≥1 (/plan step with artifact outputs present)
5. conventions.md workflow section has exactly 8 numbered steps (1..8), not 7
6. `grep "Ship.*ship" .omp/memory/project/conventions.md` returns ≥1 ("Ship" label replaces "Implement")
7. `grep "br-omp" .omp/memory/project/conventions.md` returns ≥1 (bead prefix documented)
8. `grep "Prefix.*br-omp" .omp/AGENTS.md` returns ≥1 (AGENTS.md prefix corrected from "omp" to "br-omp")
9. `grep "omp-a1b2" .omp/AGENTS.md` returns 0 matches (stale example bead ID purged)
10. `grep "5 parallel agents.*confidence.*≥80" .omp/memory/project/conventions.md` returns ≥1 (review description matches actual /review behavior)
11. AGENTS.md tree diagram: `.omp/` artifacts are visually nested under the `.omp/` branch, not interleaved with `.beads/` artifacts
12. `grep "Keep each under 1KB" .omp/AGENTS.md` returns 0 matches (or updated text qualifies the target, e.g. "Keep project.md under 1KB; other Tier 1 files target 2-4KB")
13. project.md `Current Phase` reads "Command–convention consistency audit" or equivalent
14. `git diff --stat HEAD` shows exactly 3 files changed: conventions.md, AGENTS.md, project.md; no other files modified
15. All changed files remain valid markdown — no orphan backticks, consistent heading levels, no broken tables

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| conventions.md (fixed) | Corrected 8-step workflow with /brainstorm, /plan, /ship labels; bead prefix; accurate artifact outputs | `.omp/memory/project/conventions.md` | Edit |
| AGENTS.md (fixed) | Corrected prefix (`br-omp`), accurate tree diagram, realistic memory-size guidance | `.omp/AGENTS.md` | Edit |
| project.md (updated) | Current phase and next milestone reflecting audit completion | `.omp/memory/project/project.md` | Edit |
| completion-evidence.json | Verification evidence — grep output, diff stats, br lint, bv triage | `.beads/artifacts/br-omp-backbone-skill-1da/completion-evidence.json` | New |

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | 1.1 (workflow block replacement), 1.2 (prefix insertion) | Sequential, same file | PRD approved; bead claimed; current file content read | conventions.md grep checks pass: truths 1-7, 10 all green |
| 2 | 2.1 (prefix fix), 2.2 (tree diagram restructure), 2.3 (1KB note update) | Sequential, same file | Wave 1 verified | AGENTS.md grep checks + visual tree check pass: truths 8-9, 11-12 green |
| 3 | 3.1 (project.md phase update) | Immediate | Wave 2 verified | project.md reads correctly: truth 13 green |
| 4 | 4.1 (full verification) | Immediate | Wave 3 verified | All 15 truths confirmed; br lint clean; git diff correct; truth 14 green |

## Tasks

### Wave 1: conventions.md — Workflow Chain Fix + Prefix Addition

**Target file:** `.omp/memory/project/conventions.md` (currently 129 lines, 6,871 bytes)

Two independent edits to the same file. Task 1.1 replaces the full workflow block (lines 49-56 area). Task 1.2 adds a prefix line to the Naming section (line ~15). Done sequentially because edit tool replaces by exact match — executing 1.2 first changes the file, making 1.1's oldText match the updated file, or vice-versa. Order: prefix first (shorter edit, easier to verify), then workflow block.

---

#### Task 1.1: Replace Workflow Block — /brainstorm entry, /plan step, /create output, /ship label, renumber 1→8

**What it does:** Replaces the entire 7-step workflow block (lines 49-56) with the correct 8-step version that includes /brainstorm as step 1, accurate /create output, new /plan step, "Ship" label, correct /review description, and sequential 1-8 numbering. This is one atomic replacement because step numbers cascade — individual edits would create intermediate states with mismatched numbers.

**Old block (exact text in the file):**

```markdown
## Workflow

1. **Triage** — `bv --robot-triage` before any action
2. **Create** — `/create` produces PRD + plan + tasks
3. **Implement** — `/ship` follows plan, no scope creep
4. **Verify** — `/verify` runs checks, records evidence
5. **Review** — `/review` runs parallel agents, confidence filter
6. **PR** — `/pr` opens PR, single-turn execution
7. **Close** — `/close` after merge, suggests next bead
```

**New block (should replace it exactly):**

```markdown
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

**Verification (run immediately after edit):**
```bash
# Verify old bug line is gone
grep "PRD + plan + tasks" .omp/memory/project/conventions.md    # Expected: no output (exit 1)

# Verify new correct lines exist
grep "PRD + decisions" .omp/memory/project/conventions.md       # Expected: one match
grep -c "Brainstorm.*brainstorm" .omp/memory/project/conventions.md  # Expected: ≥1
grep -c "Plan.*plan.*produces" .omp/memory/project/conventions.md    # Expected: ≥1
grep "plan\.md.*tasks\.md.*context-capsule" .omp/memory/project/conventions.md  # Expected: one match
grep "Ship.*ship" .omp/memory/project/conventions.md            # Expected: ≥1
grep "Implement.*ship" .omp/memory/project/conventions.md       # Expected: no output
grep "5 parallel agents.*confidence.*≥80" .omp/memory/project/conventions.md  # Expected: one match

# Verify 8 numbered steps
grep -cP '^\d+\.\s+\*\*' .omp/memory/project/conventions.md    # Count numbered bold steps in workflow section
```

**Files touched:** `.omp/memory/project/conventions.md` only. Lines 49-56 replaced.
**Estimated minutes:** 2 (one edit operation, grep verification)
**Conflicts with:** Nothing — this is the only bead editing conventions.md

**Rationale for block replacement vs. individual edits:** Attempting 7 individual line edits would require coordinating changing step numbers while inserting new lines — the intermediate states are incoherent (e.g. after adding /brainstorm as step 1 but before renumbering, you'd have two step-1 lines). Block replacement is atomic, verifiable in one step, and matches the PRD's "Should be" specification exactly.

---

#### Task 1.2: Add Bead Prefix to Naming Section

**What it does:** Adds `- **Bead prefix:** `br-omp`` to the Naming section of conventions.md, after the existing bead slug line. This ensures conventions.md independently documents the prefix (currently only AGENTS.md does).

**Current text (line 15 in conventions.md Naming section):**
```
- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, `fix-null-check`)
```

**Replace with:**
```
- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, `fix-null-check`)
- **Bead prefix:** `br-omp`
```

```
# Edit shape — append a line after bead slugs:
oldText: "- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, `fix-null-check`)"
newText: "- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, `fix-null-check`)\n- **Bead prefix:** `br-omp`"
```

**Verification (run immediately after edit):**
```bash
grep "br-omp" .omp/memory/project/conventions.md    # Expected: at least one match (prefix line)
grep "Bead prefix" .omp/memory/project/conventions.md  # Expected: one match
```

**Files touched:** `.omp/memory/project/conventions.md` only. Line 15 area.
**Estimated minutes:** 1
**Conflicts with:** None

---

### Wave 2: AGENTS.md — Prefix, Tree Diagram, Memory Size Guidance

**Target file:** `.omp/AGENTS.md` (currently 252 lines)

Three edits to the same file. Order: 1KB note first (shortest), prefix second, tree diagram last (most complex).

---

#### Task 2.1: Update 1KB Memory Target to Be Realistic

**What it does:** Changes the aspirational "Keep each under 1KB." instruction under Tier 1 memory to a realistic, tiered target. Current actual sizes: project.md 1,259 bytes (close to 1KB), conventions.md 6,871 bytes (6.8x over), decisions.md 1,651 bytes, gotchas.md 3,533 bytes, tech-stack.md 1,841 bytes. The blanket "each under 1KB" is consistently violated and teaches agents to ignore it.

**Current text (AGENTS.md line 101, under `### Tier 1 — Always In Context`):**
```
Keep each under 1KB.
```

**Replace with:**
```
Keep each focused and concise. Target ≤1KB for project.md (vision + current phase), ≤4KB for conventions.md (workflow + naming + rules), and ≤2KB for other Tier 1 files. Prune stale entries before adding new ones.
```

```
# Edit shape:
oldText: "Keep each under 1KB."
newText: "Keep each focused and concise. Target ≤1KB for project.md (vision + current phase), ≤4KB for conventions.md (workflow + naming + rules), and ≤2KB for other Tier 1 files. Prune stale entries before adding new ones."
```

**Verification (run immediately after edit):**
```bash
grep "Keep each under 1KB" .omp/AGENTS.md       # Expected: no output (old text gone)
grep "≤1KB" .omp/AGENTS.md                      # Expected: ≥1 match (new text present)
grep "Prune stale" .omp/AGENTS.md               # Expected: ≥1 match
```

**Files touched:** `.omp/AGENTS.md` only. Line 101.
**Estimated minutes:** 1
**Conflicts with:** None

---

#### Task 2.2: Fix Bead Prefix Declaration

**What it does:** Changes the br prefix from `omp` to `br-omp` and updates the example bead IDs to match actual bead IDs. The current text says `omp-a1b2` but actual beads are `br-omp-backbone-skill-*`. This is a source of confusion for agents that try to resolve or create bead IDs.

**Current text (AGENTS.md line 83, under `## br Conventions`):**
```
- **Prefix:** `omp` (beads are `omp-a1b2`, `omp-c3d4`, ...)
```

**Replace with:**
```
- **Prefix:** `br-omp` (beads are `br-omp-<purpose>-<short-id>`, e.g. `br-omp-backbone-skill-1da`)
```

```
# Edit shape:
oldText: "- **Prefix:** `omp` (beads are `omp-a1b2`, `omp-c3d4`, ...)"
newText: "- **Prefix:** `br-omp` (beads are `br-omp-<purpose>-<short-id>`, e.g. `br-omp-backbone-skill-1da`)"
```

**Verification (run immediately after edit):**
```bash
grep "Prefix.*br-omp" .omp/AGENTS.md         # Expected: one match
grep "omp-a1b2" .omp/AGENTS.md               # Expected: no output
grep "omp-c3d4" .omp/AGENTS.md               # Expected: no output
grep "br-omp-backbone-skill" .omp/AGENTS.md  # Expected: ≥1 match (example uses real bead)
```

**Files touched:** `.omp/AGENTS.md` only. Line 83.
**Estimated minutes:** 1
**Conflicts with:** None

---

#### Task 2.3: Restructure Tree Diagram — `.omp/` Under `.omp/`, `.beads/` Under `.beads/`

**What it does:** Fixes the repository tree diagram (lines 191-230 area in AGENTS.md) so that `.omp/` directory contents are visually nested under the `.omp/` branch, not interleaved with `.beads/` artifacts at varying depths. The current tree has:

- Lines 195-202: `.beads/` artifacts (`prd.md`, `plan.md`, etc.) at `│   │   ├──` level — these appear to be under `.beads/` which is correct
- Lines 203-230: `.omp/` content (AGENTS.md, commands/, skills/, extensions/, templates/, memory/) at the same `│   ├──` level as `.beads/` entries — visually confusing because `.beads/` hierarchy bleeds into `.omp/` hierarchy

The fix restructures to clearly separate two branches under `omp-template/`:
1. `.beads/` — has one subfolder (`artifacts/` → per-bead folders → artifact files) + `AGENTS.md`
2. `.omp/` — has `AGENTS.md`, `commands/`, `skills/`, `extensions/`, `templates/`, `memory/`

Memory files (`project.md`, `conventions.md`, etc.) are under `memory/project/` not directly under `.omp/`. The CSS design-system files live under `memory/project/` not `skills/` — they were misplaced.

**Current tree (to be replaced):**
```
```
omp-template/
├── AGENTS.md                          # Delegates to .omp/AGENTS.md
├── .beads/                            # br workspace (SQLite + JSONL)
│   │   ├── prd.md                     # Problem, outcome, acceptance criteria
│   │   ├── prd.json                   # Machine-readable requirements mirror
│   │   ├── plan.md                    # Scope, blast radius, steps, risks, verification
│   │   ├── tasks.md                   # Ordered task list with dependencies
│   │   ├── decisions.md               # Architecture and design decisions
│   │   ├── context-capsule.md         # Handoff for the next agent
│   │   ├── progress.txt               # Phase checklist
│   │   ├── completion-evidence.json   # Verification commands and results
│   │   └── review-report.md           # Parallel review findings and verdict
│   ├── AGENTS.md                      # You are here — canonical project context
│   ├── commands/                      # 9 slash commands
│   │   ├── brainstorm.md, create.md, plan.md, ship.md
│   │   ├── verify.md, review.md, pr.md, close.md, init.md
│   ├── skills/                        # 17 skills
│   │   ├── br/SKILL.md, bv/SKILL.md
│   │   ├── backbone/SKILL.md, orchestrator/SKILL.md
│   │   ├── design-system/SKILL.md     # Brand contract + craft rules
│   │   ├── design-system/DESIGN.md    # 9-section visual language spec
│   │   └── <cognitive-tool>/SKILL.md
│   ├── extensions/                    # Workflow gate
│   │   └── workflow-gate.ts
│   ├── templates/                     # Artifact templates
│   │   └── prd.md, plan.md, tasks.md, review-report.md, ...
│   └── memory/project/                # Durable project knowledge
│   │   ├── tokens.css                  # CSS custom properties (light + dark + system)
│   │   ├── base.css                    # Minimal reset + body defaults
│   │   ├── primitives.css              # Button/input/select/dialog/accordion styles
│   │   └── craft/                      # 8 universal design rule files
│       ├── project.md                 # Vision, goals, current phase
│       ├── conventions.md             # Naming, workflow, agent rules
│       ├── decisions.md               # Architecture decision records
│       ├── gotchas.md                 # Known pitfalls and mitigations
│       └── tech-stack.md              # Versions, verification commands, constraints
├── .gitignore
└── README.md
```
```

**Issues with current tree:**
1. Lines 195-202: Artifact files at `│   │   ├──` — that's 2 indent levels under `.beads/` (`.beads/` → `artifacts/` → `per-bead/` → files). Missing the `artifacts/` directory in the tree. Files appear directly under `.beads/` with no `artifacts/<bead-id>/` intermediary.
2. Line 203: `│   ├── AGENTS.md` — this is at `.beads/` depth but it's really `.omp/AGENTS.md`. The `│   ├──` prefix matches the `.beads/` children, visually placing it under `.beads/`.
3. Lines 204-230: All `.omp/` content (`commands/`, `skills/`, `extensions/`, `templates/`, `memory/`) uses `│   ├──` prefix — same level as `.beads/` children, visually confusing. Should shift to a new `.omp/` branch.
4. Lines 219-224: CSS files (`tokens.css`, `base.css`, `primitives.css`, `craft/`) are placed under `memory/project/` at wrong depth — the `│   │   ├──` vs `│       ├──` indentation doesn't match.
5. Lines 225-229: Memory markdown files appear at root-adjacent depth (`│       ├──`) which is inconsistent.

**New correct tree:**

```
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
│           ├── progress.txt           # Phase checklist
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
```

**Key fixes applied:**
1. `.beads/` now shows `beads.db` + `beads.jsonl` (actual br files) + `artifacts/` → `<bead-id>/` → per-bead files at correct nesting depth
2. `.omp/` is a separate top-level branch under `omp-template/`, visually distinct from `.beads/`
3. `.omp/AGENTS.md` is first child under `.omp/` (recognizable entry point)
4. `design-system/SKILL.md` and `DESIGN.md` are under `skills/design-system/`, not separate entries
5. `<cognitive-tool>/SKILL.md` kept as pattern placeholder under `skills/`
6. `memory/project/` contains only the 5 markdown files — CSS design-system files removed from here (they live elsewhere or are a separate concern; PRD says they were incorrectly placed)
7. `.gitignore` and `README.md` at root level, correctly beneath the tree root

Note: The PRD mentions CSS files (`tokens.css`, `base.css`, `primitives.css`, `craft/`) appeared under `memory/project/` in the current tree. These are design-system assets that belong under `.omp/skills/design-system/` or another location, not memory files. The new tree omits them from `memory/project/` but does not add them elsewhere — this bead does not create or move CSS files. If they exist in the repo, the tree doesn't need to enumerate them exhaustively.

```
# Edit shape: replace the entire tree block from the opening ``` to closing ```.
# oldText = the entire current tree (lines 191-230). 
# newText = the entire new tree as shown above.
```

**Verification (run immediately after edit):**
```bash
# Structural checks on the tree in AGENTS.md:
# 1. .omp/ items are under .omp/ branch
grep -c "├── .omp/" .omp/AGENTS.md                          # Expected: 1 (root branch)
# 2. .beads/ artifacts are at correct depth (under artifacts/<bead-id>/)
grep "└── review-report.md" .omp/AGENTS.md                  # Expected: 1 (deepest leaf)
# 3. No orphaned lines between .beads/ and .omp/
# Visual inspection: read the tree block and verify:
#   - .omp/AGENTS.md is first child under .omp/
#   - commands/ is under .omp/
#   - skills/ is under .omp/
#   - memory/project/ is under .omp/
#   - No `.beads/` prefix on lines that should be `.omp/`
#   - artifacts directory appears under .beads/
#   - bead-id directory appears under artifacts/
```

**Files touched:** `.omp/AGENTS.md` only. Lines 191-230 replaced.
**Estimated minutes:** 5 (careful tree construction + visual verification)
**Conflicts with:** None

---

### Wave 3: project.md — Current Phase Update

---

#### Task 3.1: Update Current Phase and Next Milestone

**What it does:** Updates the `## Current Phase` section of project.md to reflect that the command–convention consistency audit is in progress (and will be completed by this bead). The `Next` field should suggest the next logical milestone after this fix lands.

**Current text (project.md lines 22-26):**
```
## Current Phase

- **Status:** active
- **Milestone:** Memory file hydration — project identity hardening
- **Next:** Audit command files for consistency with conventions.md
```

**Replace with:**
```
## Current Phase

- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md fix
```

```
# Edit shape:
oldText: "## Current Phase\n\n- **Status:** active\n- **Milestone:** Memory file hydration — project identity hardening\n- **Next:** Audit command files for consistency with conventions.md"
newText: "## Current Phase\n\n- **Status:** active\n- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)\n- **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md fix"
```

**Verification (run immediately after edit):**
```bash
grep "Command–convention consistency audit" .omp/memory/project/project.md  # Expected: one match
grep "br-omp-backbone-skill-1da" .omp/memory/project/project.md             # Expected: one match
grep "Workflow verification" .omp/memory/project/project.md                 # Expected: one match
grep "Memory file hydration" .omp/memory/project/project.md                 # Expected: no output (old milestone replaced)
```

**Files touched:** `.omp/memory/project/project.md` only. Lines 14-18.
**Estimated minutes:** 1
**Conflicts with:** None

---

### Wave 4: Full Verification

---

#### Task 4.1: End-to-End Verification — All 15 Observable Truths

**What it does:** Runs a battery of grep, visual inspection, br lint, bv triage, and git diff commands to confirm all 15 observable truths hold. Records results in `completion-evidence.json`.

**Step 4.1.1 — conventions.md verification (truths 1-7, 10):**
```bash
echo "=== Truth 1: bug line erased ==="
grep "PRD + plan + tasks" .omp/memory/project/conventions.md && echo "FAIL" || echo "PASS"

echo "=== Truth 2: correct /create output present ==="
grep -c "PRD + decisions" .omp/memory/project/conventions.md

echo "=== Truth 3: /brainstorm step exists ==="
grep -c "Brainstorm.*brainstorm" .omp/memory/project/conventions.md

echo "=== Truth 4: /plan step with outputs exists ==="
grep -c "Plan.*plan.*produces" .omp/memory/project/conventions.md

echo "=== Truth 5: 8 numbered steps ==="
grep -cP '^\d+\.\s+\*\*' .omp/memory/project/conventions.md

echo "=== Truth 6: Ship label present ==="
grep -c "Ship.*ship" .omp/memory/project/conventions.md

echo "=== Truth 7: bead prefix in conventions.md ==="
grep -c "br-omp" .omp/memory/project/conventions.md

echo "=== Truth 10: review description accurate ==="
grep -c "5 parallel agents.*confidence.*≥80" .omp/memory/project/conventions.md
```

**Step 4.1.2 — AGENTS.md verification (truths 8-9, 11-12):**
```bash
echo "=== Truth 8: AGENTS.md prefix ==="
grep -c "Prefix.*br-omp" .omp/AGENTS.md

echo "=== Truth 9: stale example gone ==="
grep "omp-a1b2" .omp/AGENTS.md && echo "FAIL" || echo "PASS"

echo "=== Truth 11: tree visual inspection ==="
# Manual: read .omp/AGENTS.md, verify .omp/ items under .omp/ branch
read .omp/AGENTS.md offset=191 limit=60

echo "=== Truth 12: 1KB note updated ==="
grep "Keep each under 1KB" .omp/AGENTS.md && echo "FAIL" || echo "PASS"
grep "≤1KB" .omp/AGENTS.md && echo "PASS" || echo "WARN: check text"
```

**Step 4.1.3 — project.md verification (truth 13):**
```bash
echo "=== Truth 13: project.md Current Phase ==="
grep -c "Command–convention consistency audit" .omp/memory/project/project.md
```

**Step 4.1.4 — global verification (truths 14-15):**
```bash
echo "=== Truth 14: only 3 files changed ==="
git diff --stat HEAD | wc -l
git diff --name-only HEAD

echo "=== Truth 15: valid markdown ==="
# Read each file, check for orphan backticks, consistent headings
# No automated markdown linter available; manual inspection

echo "=== br lint ==="
br lint br-omp-backbone-skill-1da --json

echo "=== bv triage (no regressions) ==="
bv --robot-triage --format json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Triage OK: {len(d.get(\"issues\",[]))} issues')"

echo "=== br dep cycles ==="
br dep cycles --json
```

**Verification:** All 15 truths pass, br lint returns no issues, git diff shows exactly 3 files, no regressions in bv/br.

**Estimated minutes:** 3
**Conflicts with:** None

---

## Full Verification

### Pre-Ship Checks (run before making any edits)

```bash
# 0. Bead state
br show br-omp-backbone-skill-1da --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Status: {d[\"status\"]}, Priority: {d[\"priority\"]}')"
# Expected: Status: in_progress, Priority: 1

# 1. Graph health
bv --robot-triage --format json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Issues: {len(d.get(\"issues\",[]))}, Alerts: {len(d.get(\"alerts\",[]))}')"
# Expected: Issues: 1 (this bead), Alerts: 0 or informational only

# 2. No cycles
br dep cycles --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Cycles: {d[\"count\"]}')"
# Expected: Cycles: 0

# 3. Current file state (for diff baseline)
git diff --stat HEAD
# Expected: no uncommitted changes (or only plan artifacts)
```

### Post-Ship Verification (run after all edits)

```bash
# === WAVE 1: conventions.md ===
echo "=== conventions.md Workflow Block ==="
grep -A 10 "^## Workflow" .omp/memory/project/conventions.md
# Expected: shows 8 steps starting with Brainstorm

echo "---"
grep "PRD + plan + tasks" .omp/memory/project/conventions.md
# Expected: (no output — exit code 1)

echo "---"
grep "PRD + decisions" .omp/memory/project/conventions.md
# Expected: 2. **Create** — `/create` produces PRD + decisions.md

echo "---"
grep "Brainstorm.*brainstorm" .omp/memory/project/conventions.md
# Expected: 1. **Brainstorm** — `/brainstorm` explores codebase, identifies work

echo "---"
grep "Plan.*plan.*produces" .omp/memory/project/conventions.md
# Expected: 3. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md

echo "---"
grep "Ship.*ship" .omp/memory/project/conventions.md
# Expected: 4. **Ship** — `/ship` implements per plan, no scope creep

echo "---"
grep "Implement.*ship" .omp/memory/project/conventions.md
# Expected: (no output — "Implement" label removed)

echo "---"
grep "5 parallel agents" .omp/memory/project/conventions.md
# Expected: 6. **Review** — `/review` runs 5 parallel agents, confidence filter ≥80

echo "---"
grep "br-omp" .omp/memory/project/conventions.md
# Expected: at least the bead prefix line

echo "---"
echo "Step count (should be 8):"
grep -cP '^\d+\.\s+\*\*' .omp/memory/project/conventions.md
# Expected: 8

# === WAVE 2: AGENTS.md ===
echo "=== AGENTS.md Prefix ==="
grep "Prefix.*br-omp" .omp/AGENTS.md
# Expected: - **Prefix:** `br-omp` (beads are `br-omp-<purpose>-<short-id>`, ...)

echo "---"
grep "omp-a1b2" .omp/AGENTS.md
# Expected: (no output — exit code 1)

echo "---"
echo "=== AGENTS.md 1KB Note ==="
grep "Keep each under 1KB" .omp/AGENTS.md
# Expected: (no output — old text removed)

echo "---"
grep "≤1KB" .omp/AGENTS.md
# Expected: Target ≤1KB for project.md ... ≤4KB for conventions.md ... ≤2KB for other Tier 1 files

echo "---"
echo "=== AGENTS.md Tree (visual check) ==="
sed -n '/^```$/,/^```$/p' .omp/AGENTS.md | head -50
# Manual: verify .omp/ branch is separate from .beads/ branch

# === WAVE 3: project.md ===
echo "=== project.md Current Phase ==="
grep -A 4 "^## Current Phase" .omp/memory/project/project.md
# Expected: Command–convention consistency audit (br-omp-backbone-skill-1da)

# === GLOBAL ===
echo "=== Git Diff ==="
git diff --stat HEAD
# Expected: 3 files changed (conventions.md, AGENTS.md, project.md)

echo "---"
echo "=== br lint ==="
br lint br-omp-backbone-skill-1da --json 2>&1
# Expected: no errors

echo "---"
echo "=== bv triage ==="
bv --robot-triage --format json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'OK: {len(d.get(\"issues\",[]))} issues')"
# Expected: OK with non-zero issues

echo "---"
echo "=== br dep cycles ==="
br dep cycles --json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Cycles: {d[\"count\"]}')"
# Expected: Cycles: 0

echo "---"
echo "=== Markdown validity ==="
# Read each file; check for:
# - No orphan fenced code blocks (``` without matching close)
# - Consistent heading nesting (no h3 without parent h2)
# - No broken tables
read .omp/memory/project/conventions.md
read .omp/AGENTS.md
read .omp/memory/project/project.md

echo "=== All checks complete ==="
```

### Expected Output Summary

```
conventions.md:
  grep "PRD + plan + tasks" → 0 (PASS)
  grep "PRD + decisions" → 1 (PASS)
  grep "Brainstorm.*brainstorm" → 1 (PASS)
  grep "Plan.*plan.*produces" → 1 (PASS)
  grep "Ship.*ship" → 1 (PASS)
  grep "Implement.*ship" → 0 (PASS)
  grep "5 parallel agents" → 1 (PASS)
  grep "br-omp" → ≥1 (PASS)
  numbered steps → 8 (PASS)

AGENTS.md:
  grep "Prefix.*br-omp" → 1 (PASS)
  grep "omp-a1b2" → 0 (PASS)
  grep "Keep each under 1KB" → 0 (PASS)
  grep "≤1KB" → ≥1 (PASS)
  tree visual check → .omp/ separate (PASS)

project.md:
  grep "Command–convention consistency audit" → 1 (PASS)
  grep "Workflow verification" → 1 (PASS)

Global:
  git diff --stat → 3 files (PASS)
  br lint → no errors (PASS)
  bv triage → succeeds (PASS)
  br dep cycles → 0 (PASS)
  markdown validity → clean (PASS)

Total: 15/15 observable truths confirmed
```

## Risk Mitigation During Execution

| Risk | When | Defense |
|------|------|---------|
| edit tool can't match oldText exactly due to whitespace differences | During any edit | Read the exact lines with `read` immediately before the edit; use the read output verbatim as oldText |
| Tree diagram replacement is hard to match because of trailing whitespace or Unicode box-drawing chars | During Task 2.3 | Match the smallest unique sequence at the start and end of the tree block; use `read` to get exact bytes |
| conventions.md has changed since the PRD was written (someone else edited it) | Before Wave 1 | `git diff HEAD -- .omp/memory/project/conventions.md` to see if there are uncommitted changes; read the current file |
| The 8-step count includes the Naming section bullets (which are also `N. **Bold**`) | During verification | Scope the grep to the workflow area: `sed -n '/^## Workflow/,/^## /p' .omp/memory/project/conventions.md | grep -cP '^\d+\.\s+\*\*'` |
| Agent gets blocked by workflow-gate when trying to edit | During any edit | Writing to .omp/ files is in the "always passes" list; if blocked, verify bead state with `br show` |
