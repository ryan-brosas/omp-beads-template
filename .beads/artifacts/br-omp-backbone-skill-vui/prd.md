<!-- DENSITY: Minimum 600 lines. No upper bound — be thorough. <600 = incomplete (missing sections, hand-wavy, no real technical context). This is an AI handoff document — the next agent reads only this. -->
# PRD: Finalize Repo Structure — Design System Migration + Density Gate Hardening

**Bead:** br-omp-backbone-skill-vui | **Type:** task | **Priority:** P1
**Created:** 2026-06-17 | **Estimate:** 15

## Problem

The repository has accumulated structural drift across three dimensions that collectively undermine agent reliability:

### 1. Design System Files in Wrong Location

During the design system adoption sprint, CSS and craft files were placed at the repository root (`DESIGN.md`, `design/tokens.css`, `design/primitives.css`, `design/base.css`, `design/craft/*.md`). The conventions specify that design system assets live under `.omp/skills/design-system/` (per the DESIGN.md brand contract section and the skills map). Additionally, `tech-stack.md` has a stale "Design Assets" table referencing the old `design/` paths that no longer exist.

**Impact:** Agents loading the skills map find `design-system/SKILL.md` and `design-system/DESIGN.md` under `.omp/skills/` but the actual CSS and craft files are at `/design/`. The skill can't find its own assets. An agent following the conventions.md tree diagram (which was just fixed in bead 1da) sees no `design/` directory at root — the tree is correct but the filesystem disagrees.

**Current state (git status):**
- 8 files deleted from `design/` and `DESIGN.md` (shown as `D`)
- New `.omp/skills/design-system/` directory with SKILL.md + DESIGN.md (tracked)
- CSS/craft files exist as untracked in `.omp/skills/design-system/`
- This is a cp+rm migration that happened without bead tracking

**Files involved in migration:**

| Old Path | New Path | Status |
|----------|----------|--------|
| `DESIGN.md` | `.omp/skills/design-system/DESIGN.md` | Old deleted (D), new tracked |
| `design/tokens.css` | `.omp/skills/design-system/tokens.css` | Old deleted (D), new untracked |
| `design/primitives.css` | `.omp/skills/design-system/primitives.css` | Old deleted (D), new untracked |
| `design/base.css` | `.omp/skills/design-system/base.css` | Old deleted (D), new untracked |
| `design/craft/animation-discipline.md` | `.omp/skills/design-system/craft/animation-discipline.md` | Old deleted (D), new untracked |
| `design/craft/anti-ai-slop.md` | `.omp/skills/design-system/craft/anti-ai-slop.md` | Old deleted (D), new untracked |
| `design/craft/color.md` | `.omp/skills/design-system/craft/color.md` | Old deleted (D), new untracked |
| `design/craft/typography.md` | `.omp/skills/design-system/craft/typography.md` | Old deleted (D), new untracked |

### 2. Density Gate Inconsistency

The workflow-gate extension enforces a 600-line minimum (`MIN_LINES = 600` in `workflow-gate.ts`). This was introduced to ensure artifact quality. However, the command-level documentation and templates still reference the old "500-700" target range:

**Inconsistency Map:**

| File | Old Text | Current Gate Requirement | Mismatch |
|------|----------|------------------------|----------|
| `.omp/templates/prd.md` header | "Target 500-700 lines" | 600 minimum | ✓/✗ (contradicts gate) |
| `.omp/templates/plan.md` header | "Target 500-700 lines" | 600 minimum | ✓/✗ |
| `.omp/templates/tasks.md` | No density header | 600 minimum | Missing reference |
| `.omp/commands/create.md` line 243 | "PRD is 500-700 lines (<300 = incomplete)" | 600 minimum | Wrong floor + ceiling |
| `.omp/commands/plan.md` lines 105-109 | "plan.md: 500-700, tasks.md: 300-600, PRD: 500-700, bundle 1100-2000" | 600 minimum across all | All wrong |

**Impact:** An agent reading the command documentation sees guidance for 500-700 lines, writes a 520-line PRD, ships it, then gets blocked by the workflow-gate at edit time with "PRD is only 520 lines (minimum 600)". The contradictory guidance wastes an entire implementation cycle.

### 3. PR Footer Worktree Path

The PR command (`.omp/commands/pr.md`) injects a worktree path into the PR body footer:
```
Bead: `$BEAD_ID` | Worktree: `.worktree/!`git branch --show-current``
```

This uses backtick injection (`!`...``) to dynamically insert the branch name, which serves as the worktree path (since worktrees are named by branch in `.worktree/`). This enables the git-clean command to locate and remove worktrees after merge.

The change exists as an uncommitted modification in `.omp/commands/pr.md` (`@@ -77,7 +77,7 @@`).

### 4. Orphaned git-clean Command

A `.omp/commands/git-clean.md` file exists as untracked with full command documentation. It provides worktree cleanup automation for merged PRs:
- `/git-clean <bead-id>` — removes worktree + local branch for a specific merged bead
- `/git-clean` (no args) — cleans all merged worktrees
- Fetches from origin with prune to detect remote branch deletions (merged PRs)
- Checks both local merge state AND remote branch deletion as merge signals

This command was added in prior work but was never tracked in git or referenced in AGENTS.md. It is orphaned infrastructure that cannot be discovered by agents.

## Goals

1. **Primary**: Migrate all design system files from root `design/` and `DESIGN.md` to `.omp/skills/design-system/`, remove stale references in `tech-stack.md`, and ensure the design-system skill directory is self-contained with all its assets
2. **Secondary**: Synchronize density targets across all files — templates, commands, and workflow-gate — to the single `≥600 lines` standard with consistent error messaging
3. **Tertiary**: Standardize the PR footer worktree path injection for post-merge cleanup automation
4. **Quality**: Register the git-clean command in AGENTS.md and commit it as tracked infrastructure

## Non-Goals

- Do NOT modify the design system content itself (DESIGN.md tokens, CSS rules, craft rules) — file location migration only, content is authoritative
- Do NOT change the density threshold (600 lines) — it's correct; just synchronize the documentation around it
- Do NOT add new design system features, tokens, or craft rules
- Do NOT modify any skill files other than design-system (no br/SKILL.md, bv/SKILL.md, etc.)
- Do NOT add new workflow-gate checks beyond the existing density enforcement
- Do NOT modify any command behavior or phase logic — only fix documentation strings and numerical targets
- Do NOT create new bead dependencies or modify the dependency graph

## Success Metrics

| # | Metric | Command | Expected |
|---|--------|---------|----------|
| 1 | Old design directory gone | `ls design/ 2>&1` | "No such file or directory" |
| 2 | Root DESIGN.md gone | `ls DESIGN.md 2>&1` | "No such file or directory" |
| 3 | All assets in new location | `ls .omp/skills/design-system/` | Shows SKILL.md, DESIGN.md, tokens.css, primitives.css, base.css, craft/ |
| 4 | Craft files present | `ls .omp/skills/design-system/craft/` | Shows 4 .md files |
| 5 | No stale tech-stack refs | `grep "design/" .omp/memory/project/tech-stack.md` | Exit code 1 (no matches) |
| 6 | Old density ranges erased | `grep -r "500-700" .omp/commands/ .omp/templates/` | Exit code 1 |
| 7 | "300-600" erased | `grep -r "300-600" .omp/commands/ .omp/templates/` | Exit code 1 |
| 8 | New density present everywhere | `grep -c "≥600" .omp/commands/create.md .omp/commands/plan.md .omp/templates/prd.md .omp/templates/plan.md .omp/templates/tasks.md .omp/extensions/workflow-gate.ts` | ≥6 |
| 9 | PR footer worktree | `grep -c "Worktree:" .omp/commands/pr.md` | ≥1 |
| 10 | git-clean tracked | `git ls-files .omp/commands/git-clean.md` | Returns file path |
| 11 | git-clean in AGENTS.md | `grep -c "git-clean" .omp/AGENTS.md` | ≥1 |
| 12 | No dependency cycles | `br dep cycles --json` | `"count": 0` |
| 13 | No bv alerts | `bv --robot-triage --format json` | alerts array empty |

## Requirements

### REQ-1: Design System Files Migrated (MUST)

All 8 design system files shall exist at `.omp/skills/design-system/` with identical content to their originals, and the old paths shall be removed from git tracking.

**Pre-existing state:** Files already deleted from old location (D in git status), new files exist as untracked at new location. This bead formalizes the move by staging both sides (add new, rm old) in one commit.

**Acceptance criteria:**
- `git ls-files design/` returns nothing
- `git ls-files DESIGN.md` returns nothing
- `git ls-files .omp/skills/design-system/tokens.css` returns the file
- `git ls-files .omp/skills/design-system/craft/typography.md` returns the file
- Content diff between staged new files and HEAD~1 old files shows identity (no modifications)

**Verification:**
```bash
# Old paths gone from tracking
test -z "$(git ls-files design/ DESIGN.md)" && echo "PASS" || echo "FAIL"

# New paths tracked
for f in tokens.css primitives.css base.css DESIGN.md craft/animation-discipline.md craft/anti-ai-slop.md craft/color.md craft/typography.md; do
  git ls-files ".omp/skills/design-system/$f" > /dev/null && echo "  OK: $f" || echo "  MISSING: $f"
done
```

### REQ-2: Content Preservation (MUST)

Migrated files shall have byte-identical content to their originals. No reformatting, no token renames, no whitespace changes.

**Acceptance criteria:**
- For each migrated file, `git show HEAD~1:<old-path>` matches the staged new file content exactly

**Verification:**
```bash
# For each migrated file, diff the old committed version against the staged new version
for pair in "DESIGN.md:.omp/skills/design-system/DESIGN.md"             "design/tokens.css:.omp/skills/design-system/tokens.css"             "design/primitives.css:.omp/skills/design-system/primitives.css"             "design/base.css:.omp/skills/design-system/base.css"             "design/craft/animation-discipline.md:.omp/skills/design-system/craft/animation-discipline.md"             "design/craft/anti-ai-slop.md:.omp/skills/design-system/craft/anti-ai-slop.md"             "design/craft/color.md:.omp/skills/design-system/craft/color.md"             "design/craft/typography.md:.omp/skills/design-system/craft/typography.md"; do
  old="\${pair%%:*}"
  new="\${pair##*:}"
  diff <(git show "HEAD~1:$old" 2>/dev/null) "$new" > /dev/null && echo "  IDENTICAL: $old" || echo "  DIFFERS: $old"
done
```

### REQ-3: Tech-Stack Stale References Removed (MUST)

The "Design Assets" table in `tech-stack.md` (lines 62-86 in the committed version) shall be removed. No memory file shall reference the old `design/` directory or root `DESIGN.md` as a current asset location.

**Acceptance criteria:**
- `grep "design/" .omp/memory/project/tech-stack.md` returns exit code 1
- `grep "DESIGN.md" .omp/memory/project/tech-stack.md` returns exit code 1
- The removed section is the "Design Assets" table listing old file paths; no other content is affected

**Verification:**
```bash
grep -r "design/" .omp/memory/project/ && echo "FAIL: stale refs remain" || echo "PASS: clean"
grep "DESIGN.md" .omp/memory/project/tech-stack.md && echo "FAIL" || echo "PASS"
```

### REQ-4: Density Standard Synchronized (MUST)

Every file that references an artifact line-count target shall use "≥600" (lower bound only, no upper bound). The old "500-700", "300-600", and similar ranges shall not appear anywhere in commands/ or templates/.

**Acceptance criteria:**
- Zero matches for `500-700`, `300-600`, `300-500`, `200-400` in `.omp/commands/` and `.omp/templates/`
- At least 6 matches for `≥600` across commands + templates + extensions

**Affected files and specific changes:**

| File | Line(s) | Old | New |
|------|---------|-----|-----|
| `.omp/templates/prd.md` | 1 | "Target 500-700 lines. <300 = incomplete" | "Minimum 600 lines. No upper bound. <600 = incomplete" |
| `.omp/templates/plan.md` | 1 | "Target 500-700 lines. <300 = too thin" | "Minimum 600 lines. No upper bound. <600 = too thin" |
| `.omp/templates/tasks.md` | 1 | (no header) | "Minimum 600 lines. No upper bound. <600 = too thin" |
| `.omp/commands/create.md` | 243 | "PRD is 500-700 lines (<300 = incomplete)" | "PRD is ≥600 lines (<600 = incomplete)" |
| `.omp/commands/plan.md` | 105-109 | "plan.md: 500-700, tasks.md: 300-600, PRD: 500-700, bundle 1100-2000" | "plan.md: ≥600, tasks.md: ≥600, PRD: ≥600" |
| `.omp/extensions/workflow-gate.ts` | 50 | (already `MIN_LINES = 600`) | No change needed |

**Verification:**
```bash
grep -r "500-700\|300-600\|300-500\|200-400" .omp/commands/ .omp/templates/ && echo "FAIL" || echo "PASS"
echo "≥600 matches: $(grep -rc '≥600' .omp/commands/ .omp/templates/ .omp/extensions/ | grep -v ':0$' | wc -l)"
```

### REQ-5: Density Gate Error Messages Informative (SHOULD)

The workflow-gate density error messages shall include the artifact type, current line count, minimum required, and a corrective action. Already implemented in the uncommitted workflow-gate.ts changes (lines 131-160). This requirement confirms the messages meet the standard.

**Expected format:**
- PRD: "PRD for <bead> is only <N> lines (minimum 600). Run /create to expand it — every section needs concrete evidence, file paths, API signatures, patterns, and constraints."
- Plan: "plan for <bead> is only <N> lines (minimum 600). Run /plan to expand it — add code outlines, wave structure, verification gates, and per-task detail."
- Tasks: "tasks for <bead> is only <N> lines (minimum 600). Run /plan to expand it — every task needs yaml metadata, concrete steps, and verification checks."

**Verification:** Read `.omp/extensions/workflow-gate.ts` density enforcement block (lines 126-160), confirm messages include artifact name, count, minimum, and corrective action.

### REQ-6: PR Footer Worktree Path Present (SHOULD)

The PR command footer shall include the worktree path for post-merge cleanup identification. Already implemented in the uncommitted `.omp/commands/pr.md` change.

**Acceptance criteria:**
- `grep "Worktree:" .omp/commands/pr.md` returns ≥1

**Verification:**
```bash
grep "Worktree:" .omp/commands/pr.md && echo "PASS" || echo "FAIL"
```

### REQ-7: git-clean Command Registered (SHOULD)

The git-clean command file shall be tracked in git and referenced in AGENTS.md's command reference table.

**Acceptance criteria:**
- `git ls-files .omp/commands/git-clean.md` returns the file path
- AGENTS.md command reference table or command list includes git-clean

**Verification:**
```bash
git ls-files .omp/commands/git-clean.md && echo "PASS: tracked" || echo "FAIL: not tracked"
grep -c "git-clean" .omp/AGENTS.md
```

### REQ-8: No Dependency Cycles (MUST)

The bead graph shall remain acyclic after this bead closes. All existing beads are orphans in a disconnected graph; this bead adds no dependencies.

**Verification:** `br dep cycles --json | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['count']==0"`

### REQ-9: No Triage Regressions (MUST)

bv triage shall show no new alerts or issues after the changes land. Since this is a file-move and documentation change, no behavioral regressions are expected.

**Verification:** `bv --robot-triage --format json | python3 -c "import json,sys; d=json.load(sys.stdin); assert len(d.get('triage',{}).get('alerts',[]))==0"`

## Approach

The work is already done in the working tree — all changes exist as uncommitted modifications/deletions/additions. This bead formalizes and commits them as a single tracked unit, with content verification to ensure no accidental modifications.

### Wave 1: Content Verification + Design Migration (3 min)
1. Diff each deleted design file against its new location to confirm identity
2. Verify `.omp/skills/design-system/` has all expected files with expected content
3. Stage the new files: `git add .omp/skills/design-system/tokens.css .omp/skills/design-system/primitives.css .omp/skills/design-system/base.css .omp/skills/design-system/craft/`
4. Confirm deletions: `git rm DESIGN.md design/tokens.css design/primitives.css design/base.css design/craft/*.md`
5. Remove stale "Design Assets" section from tech-stack.md

### Wave 2: Density Documentation Verification (2 min)
1. Verify template headers use "≥600" (already changed in working tree)
2. Verify command files use "≥600" (already changed in working tree)
3. Verify workflow-gate has MIN_LINES=600 with informative errors (already changed)
4. Confirm zero old-range references

### Wave 3: Infrastructure Registration (2 min)
1. Review `.omp/commands/git-clean.md` content for completeness
2. Add git-clean entry to AGENTS.md command reference table or skills map
3. Stage git-clean.md: `git add .omp/commands/git-clean.md`

### Wave 4: Commit, Verify, PR, Close (3 min)
1. Single atomic commit: all design moves, density sync, tech-stack cleanup, infrastructure registration
2. Run all 13 verification checks
3. Create completion-evidence.json
4. Create PR
5. Close bead

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Design files modified during cp+rm (content drift) | Low | High | Byte-level diff against HEAD~1 originals before commit |
| Density gate too aggressive for edge cases | Low | Medium | 600 is established policy confirmed in prior bead; edge cases are documentation-only beads which aren't exempt |
| git-clean command contains bugs | Low | Low | Content review; command was tested in prior work; this just tracks and registers it |
| tech-stack.md loses useful design info | Low | Low | "Design Assets" table only contained stale file paths, not design guidance |
| Uncommitted workflow-gate.ts has syntax errors | Low | High | Verify gate loads without errors: check for balanced braces, valid imports |

## Dependencies

- **Blocks:** Nothing (orphan bead — all 10 beads in graph are orphans)
- **Blocked by:** Nothing (orphan bead — no dependencies)
- **Related:** `br-omp-backbone-skill-1da` (fixed the conventions.md workflow and AGENTS.md tree diagram that this bead's file structure must match)

## Verification Plan

Full battery to run after commit:

```bash
echo "=== 1. Design directory gone ==="
ls design/ 2>&1 | grep -q "No such file" && echo "PASS" || echo "FAIL"

echo "=== 2. Root DESIGN.md gone ==="
ls DESIGN.md 2>&1 | grep -q "No such file" && echo "PASS" || echo "FAIL"

echo "=== 3. New location has all files ==="
for f in SKILL.md DESIGN.md tokens.css primitives.css base.css; do
  test -f ".omp/skills/design-system/$f" && echo "  OK: $f" || echo "  MISSING: $f"
done

echo "=== 4. Craft files present ==="
for f in animation-discipline.md anti-ai-slop.md color.md typography.md; do
  test -f ".omp/skills/design-system/craft/$f" && echo "  OK: $f" || echo "  MISSING: $f"
done

echo "=== 5. Tech-stack clean ==="
grep "design/" .omp/memory/project/tech-stack.md && echo "FAIL" || echo "PASS"

echo "=== 6-7. Density ranges synchronized ==="
grep -r "500-700\|300-600\|300-500\|200-400" .omp/commands/ .omp/templates/ && echo "FAIL: old ranges remain" || echo "PASS: clean"

echo "=== 8. New density present ==="
echo "≥600 matches:"
grep -rc "≥600" .omp/commands/ .omp/templates/ .omp/extensions/ 2>/dev/null | grep -v ":0$"

echo "=== 9. PR footer ==="
grep -c "Worktree:" .omp/commands/pr.md && echo "PASS" || echo "FAIL"

echo "=== 10-11. git-clean registered ==="
git ls-files .omp/commands/git-clean.md > /dev/null && echo "PASS: tracked" || echo "FAIL: not tracked"
grep -c "git-clean" .omp/AGENTS.md

echo "=== 12. No cycles ==="
br dep cycles --json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['count']==0; print('PASS')"

echo "=== 13. No bv alerts ==="
bv --robot-triage --format json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); a=d.get('triage',{}).get('alerts',[]); assert len(a)==0; print('PASS')"
```

## Audit Trail

This bead was created on 2026-06-17 during a bead lifecycle drive session. The working tree already contained all changes — the bead formalizes them as a tracked unit of work.


## Detailed Diff Analysis

### File-by-File Change Documentation

#### `.omp/commands/create.md` (+1/-1)

**Line 243 change:**
```
- PRD is 500-700 lines (wc -l prd.md) — <300 = incomplete, needs more investigation
+ PRD is ≥600 lines (`wc -l prd.md`) — <600 = incomplete, needs more investigation
```

**Rationale:** Synchronizes the command-level density check with the workflow-gate's MIN_LINES=600. Removes upper bound (700) per the "no upper bound" policy. Changes "<300 = incomplete" to "<600 = incomplete".

**Risk:** None — this is a documentation string change in a verification checklist. If an agent runs `/create` and the PRD is 550 lines, the checklist will correctly flag it as incomplete.

#### `.omp/commands/plan.md` (+5/-5)

**Lines 105-109 change:**
```
- Density check: each major artifact should be 500-700 lines
- echo "Plan: \$(wc -l < plan.md) lines (target 500-700)"
- echo "Tasks: \$(wc -l < tasks.md) lines (target 300-600, varies by task count)"
- echo "PRD:  \$(wc -l < prd.md) lines (target 500-700)"
- echo "Bundle: \$(cat *.md | wc -l) lines (target 1100-2000 across all artifacts)"
+ Density check: each artifact must be ≥600 lines
+ echo "Plan: \$(wc -l < plan.md) lines (minimum 600)"
+ echo "Tasks: \$(wc -l < tasks.md) lines (minimum 600)"
+ echo "PRD:  \$(wc -l < prd.md) lines (minimum 600)"
+ echo "Bundle: \$(cat *.md | wc -l) lines (minimum 1800 across all artifacts)"
```

**Rationale:** 
- Removes upper bound (700) and per-artifact variance (300-600 for tasks)
- Standardizes to single minimum (600) for all artifacts
- Bundle target 1800 = 600 × 3 (prd + plan + tasks minimum) — matches the new minimum
- Removes "should be" language for "must be" (stronger enforcement)
- Removes "(varies by task count)" qualifier — minimum doesn't vary

**Risk:** Bundle minimum of 1800 might be too high for simple beads. But the 600-per-artifact floor already demands 1800; this just makes the bundle check consistent with the per-file checks.

#### `.omp/commands/pr.md` (+1/-1)

**Line 77 change:**
```
- 🤖 Generated with [OMP](https://omp.sh) | Bead: `$BEAD_ID`
+ 🤖 Generated with [OMP](https://omp.sh) | Bead: `$BEAD_ID` | Worktree: `.worktree/!`git branch --show-current``
```

**Rationale:** Adds worktree path to PR footer for post-merge cleanup identification. The backtick injection (`!`...``) dynamically inserts the branch name, which matches the worktree directory name (`.worktree/<branch-name>/`).

**Risk:** If the worktree directory convention changes (e.g., from `.worktree/` to something else), this footer becomes stale. Mitigated by: the worktree path is a documented convention, and the git-clean command also references `.worktree/`. Both would need updating together.

#### `.omp/templates/prd.md` (+2/-2)

**Header change:**
```
- <!-- DENSITY: Target 500-700 lines. <300 = incomplete (missing sections, hand-wavy, no real technical context). No upper cap — be thorough. This is an AI handoff document — the next agent reads only this. -->
+ <!-- DENSITY: Minimum 600 lines. No upper bound — be thorough. <600 = incomplete (missing sections, hand-wavy, no real technical context). This is an AI handoff document — the next agent reads only this. -->
```

**Rationale:** Template header now matches gate enforcement. "Target 500-700" → "Minimum 600". "No upper cap" → "No upper bound". "<300 = incomplete" → "<600 = incomplete".

#### `.omp/templates/plan.md` (+2/-2)

**Header change:**
```
- <!-- DENSITY: Target 500-700 lines. <300 = too thin (waves undefined, tasks lack code outlines, verification hand-wavy). Task outlines should show the shape of every file change — not full implementation, but enough that a different agent can execute without reading the PRD again. -->
+ <!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin (waves undefined, tasks lack code outlines, verification hand-wavy). Task outlines should show the shape of every file change — not full implementation, but enough that a different agent can execute without reading the PRD again. -->
```

#### `.omp/templates/tasks.md` (+1/-0)

**New header:**
```
+ <!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin — tasks lack detail, verification steps are vague, dependencies undefined. Every task needs a YAML metadata header, concrete steps, verification checks, and rollback instructions. -->
```

**Rationale:** tasks.md previously had no density guidance. Now it matches the 600-line minimum with task-specific quality guidance.

#### `.omp/extensions/workflow-gate.ts` (+50/-1)

**Changes:**

1. **New import:**
```
- import { existsSync } from "node:fs";
+ import { existsSync, readFileSync } from "node:fs";
```

2. **New constants and function (lines 48-60):**
```typescript
const MIN_LINES = 600;

function checkDensity(filePath: string): { ok: boolean; lines: number } {
  try {
    const content = readFileSync(filePath, "utf-8");
    const lines = content.split("\n").length;
    return { ok: lines >= MIN_LINES, lines };
  } catch {
    return { ok: false, lines: 0 };
  }
}
```

3. **Density enforcement block (lines 126-160):**
Checks PRD, plan, and tasks density after confirming files exist. Returns structured error messages with artifact name, current count, minimum, and corrective action.

**Edge case: `checkDensity` returns `{ ok: false, lines: 0 }` on file read error** — this means a missing file is treated as "0 lines" which is <600. But the function is only called after `existsSync` confirms the file exists (lines 110-124 check existence first, lines 131-160 check density for existing files). The `catch` branch handles I/O errors (permissions, encoding), not missing files.

**Edge case: Files with exactly 600 lines pass** — the check is `lines >= MIN_LINES`, so 600 is the inclusive threshold. A 600-line artifact passes. This means "≥600" is the correct documentation, not ">600".

#### `.omp/memory/project/tech-stack.md` (-25/-0)

**Removed "Design Assets" table (lines 62-86):**
```
-## Design Assets
-
-| Asset | Path | Purpose |
-|-------|------|---------|
-| Brand contract | `.omp/skills/design-system/DESIGN.md` | 9-section visual language spec |
-| Design tokens | `.omp/design/tokens.css` | CSS custom properties (light + dark + system) |
-| Base styles | `.omp/design/base.css` | Minimal reset + body defaults |
-| Primitives | `.omp/design/primitives.css` | Button/input/select/dialog/accordion styles |
-| Craft rules | `.omp/design/craft/` | Universal design rules |
```

**Rationale:** All paths in this table reference the old `design/` location. The table is either: (a) stale (if files have moved, paths are wrong), or (b) misleading (if it claims files are at `design/` when they're at `.omp/skills/design-system/`). Removing prevents future agents from looking in the wrong place. The design system location is documented in the design-system SKILL.md and conventions.md — no separate table is needed.

## Edge Case Analysis

### Edge Case 1: What if a cp+rm migration modified file content?

**Scenario:** The user ran `cp design/tokens.css .omp/skills/design-system/tokens.css && rm design/tokens.css` and accidentally edited tokens.css during the process.

**Detection:** Wave 1 performs byte-level diff between `git show HEAD~1:<old-path>` and the staged new file. Any content drift is caught before the commit.

**Mitigation:** If diff shows a change, restore the original from git history and re-stage.

### Edge Case 2: What if design/ directory wasn't fully deleted?

**Scenario:** `design/craft/` subdirectory still exists but is empty after files moved.

**Detection:** `find design/ -type f` returns nothing, but `ls design/` doesn't fail. The directory is a zombie.

**Mitigation:** `git rm -r design/` removes the directory from tracking, and `rmdir` removes the empty directory. Or `find design/ -type d -empty -delete` cleans up.

### Edge Case 3: What if .omp/skills/design-system/ already had some files?

**Scenario:** SKILL.md and DESIGN.md are already tracked. tokens.css exists as untracked. What if tokens.css was already staged by another process?

**Detection:** `git status .omp/skills/design-system/tokens.css` shows the status — untracked vs staged vs modified.

**Mitigation:** Check status before staging. If already staged, verify the content matches the original. If modified, restore original.

### Edge Case 4: What if the 600-line minimum is too strict for some bead types?

**Scenario:** A "docs: fix typo in README" bead produces a 30-line PRD because the fix is trivial.

**Response:** Such beads shouldn't exist. If the fix is a single-line typo, it doesn't need a bead — commit directly. Beads are for non-trivial work. If a change genuinely requires a bead, it genuinely requires 600 lines of planning. The gate is intentionally strict to prevent thin artifacts.

### Edge Case 5: What if an existing bead has a sub-600-line PRD from before the gate?

**Scenario:** A bead created before the density gate was introduced has a 450-line PRD. A new agent tries to edit source files for that bead.

**Response:** The gate blocks edits until the PRD is expanded to 600 lines. The agent must expand the PRD before implementing. This is the intended behavior — old beads get the same quality floor as new ones.

### Edge Case 6: What if the git-clean command references paths that don't exist?

**Scenario:** git-clean.md contains instructions to run `git worktree remove .worktree/<branch>` but `.worktree/` doesn't exist.

**Response:** The command should gracefully handle missing worktrees (check existence before attempting removal). Content review in Wave 3 verifies the command handles this case.

## Migration Verification Matrix

For each of the 8 migrated files, verify:

| Old Path | New Path | Content Match | Git Rm Old | Git Add New |
|----------|----------|---------------|------------|-------------|
| `DESIGN.md` | `.omp/skills/design-system/DESIGN.md` | diff = 0 | ✓ | ✓ |
| `design/tokens.css` | `.omp/skills/design-system/tokens.css` | diff = 0 | ✓ | ✓ |
| `design/primitives.css` | `.omp/skills/design-system/primitives.css` | diff = 0 | ✓ | ✓ |
| `design/base.css` | `.omp/skills/design-system/base.css` | diff = 0 | ✓ | ✓ |
| `design/craft/animation-discipline.md` | `.omp/skills/design-system/craft/animation-discipline.md` | diff = 0 | ✓ | ✓ |
| `design/craft/anti-ai-slop.md` | `.omp/skills/design-system/craft/anti-ai-slop.md` | diff = 0 | ✓ | ✓ |
| `design/craft/color.md` | `.omp/skills/design-system/craft/color.md` | diff = 0 | ✓ | ✓ |
| `design/craft/typography.md` | `.omp/skills/design-system/craft/typography.md` | diff = 0 | ✓ | ✓ |

## Pre-Commit Checklist

Before the single atomic commit:

- [ ] All 8 old design files confirmed deleted from tracking (`git ls-files design/ DESIGN.md` empty)
- [ ] All 8 new design files staged in `.omp/skills/design-system/`
- [ ] Content identity confirmed for all 8 files (diff = 0)
- [ ] tech-stack.md "Design Assets" section removed
- [ ] Density headers synchronized in all 5 template/command files
- [ ] Workflow-gate density enforcement code present with informative errors
- [ ] PR footer worktree injection present
- [ ] git-clean.md staged for tracking
- [ ] git-clean referenced in AGENTS.md
- [ ] br dep cycles = 0
- [ ] bv triage has 0 alerts

## Post-Commit Verification

After commit:

- [ ] `git diff HEAD~1 --stat` shows the expected file set
- [ ] `ls design/` fails with "No such file"
- [ ] `ls .omp/skills/design-system/` shows all files
- [ ] All 13 success metrics pass (see Verification Plan above)
- [ ] No regressions in br/bv behavior


## Implementation Constraints

1. **Single atomic commit** — all changes (design migration + density sync + infrastructure) in one commit to avoid intermediate states where files are half-moved or targets are inconsistent.
2. **No file content changes** — the moved design files must be byte-identical to originals. The density changes are documentation-only (string replacements of numerical ranges). The git-clean.md is content-reviewed but not modified.
3. **No new dependencies** — this bead is an orphan. No `br dep add` operations.
4. **No new files created** — all files already exist in the working tree. This bead stages and commits them; it doesn't create anything new.

## Rollback Plan

If this bead introduces issues, rollback is a single commit revert:

```bash
git revert <commit-hash>
```

This restores:
- Design files at old paths (`design/`, `DESIGN.md`)
- Old density targets ("500-700") in templates/commands
- Stale "Design Assets" table in tech-stack.md
- Removal of git-clean from AGENTS.md

The reverted state is clean because:
- The commit is atomic (all changes in one revert)
- No other beads depend on this one
- No database migrations or external state changes
- The design files at old paths would be restored by the revert

## Testing Strategy

### Automated Checks (Wave 4 Verification Battery)

1. **File existence checks:** `test -f`, `test -d` for old location absence + new location presence
2. **Grep checks:** Old density ranges absent, new density present, stale paths absent
3. **Git checks:** `git ls-files` for tracking state, `git diff --stat` for expected file set
4. **Graph checks:** `br dep cycles --json` for acyclicity, `bv --robot-triage` for alerts
5. **Content identity:** `diff <(git show HEAD~1:old) new` for each of 8 migrated files

### Manual Verification

1. **Visual review of git-clean.md content** — confirm command handles edge cases (no worktrees, no matching branch, network errors)
2. **Visual review of AGENTS.md command table** — confirm git-clean entry placement and format matches other entries
3. **Visual review of density error messages** — confirm they include artifact name, count, minimum, and corrective action

### Regression Surface

| Component | How Tested | Risk |
|-----------|-----------|------|
| Design system skill loading | File existence at new paths | None — SKILL.md and DESIGN.md already at new location |
| Workflow-gate edit blocking | Existing tests + density check | Low — gate was already blocking at 600; this just adds better messages |
| br bead operations | `br lint`, `br dep cycles` | None — no br state changes |
| bv graph analysis | `bv --robot-triage` | None — no new bead edges |
| PR creation | Manual PR creation in Wave 4 | Low — footer injection is a string change |
| git-clean execution | Command not executed (documentation change only) | None — just tracking the file |

## Acceptance Criteria Summary

All 13 success metrics must pass. Additionally:

1. The commit message must summarize all changes concisely (design migration + density sync + infrastructure)
2. The PR body must include the verification results table
3. The bead must be closable without manual intervention
4. No untracked files should remain in `.omp/skills/design-system/` — all staged
5. No deleted files should remain unstaged — `git rm` applied to all old paths
6. Working tree after commit: clean except for any unrelated changes from other work

## Related Artifacts

- **PRD:** This document
- **Plan:** `.beads/artifacts/br-omp-backbone-skill-vui/plan.md` — wave sequencing, file-level edit specifications, dependency graph
- **Tasks:** `.beads/artifacts/br-omp-backbone-skill-vui/tasks.md` — per-wave task breakdown with YAML metadata, verification steps, rollback
- **Context Capsule:** `.beads/artifacts/br-omp-backbone-skill-vui/context-capsule.md` — handoff summary for next agent
- **Completion Evidence:** `.beads/artifacts/br-omp-backbone-skill-vui/completion-evidence.json` — all 13 metric results
