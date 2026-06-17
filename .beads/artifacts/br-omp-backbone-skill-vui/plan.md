<!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin (waves undefined, tasks lack code outlines, verification hand-wavy). -->
# Plan: br-omp-backbone-skill-vui

**Goal:** Review, verify, stage, and commit pre-existing uncommitted changes that migrate design system files to `.omp/skills/design-system/`, synchronize density targets to "≥600", add PR footer worktree path, and register the git-clean command. All substantive changes already exist in the working tree — this bead is about quality gating and formal commit.

## Graph Context

- **Blast radius:** 16 files (8 design deleted + moved, 5 command/template docs, 1 gate code, 1 tech-stack cleanup, 1 new command tracked)
- **Unblocks:** Nothing — all beads are orphans (0 edges)
- **Blocked by:** Nothing — orphan node
- **Critical path:** No — 0 downstream dependents
- **Forecast:** 10 minutes (confidence 0.9) — work is already done; just verify, stage, commit
- **Hotspots touched:** None — template repo, no code files tracked

**Graph metrics:**
- Node count: 11 (10 closed + this bead), Edge count: 0, Density: 0
- No cycles, all orphans, uniform PageRank 0.1
- Velocity: 10 closed in 7 days

## Observable Truths

1. `ls design/ 2>&1` returns "No such file or directory"
2. `ls DESIGN.md 2>&1` returns "No such file or directory"
3. `ls .omp/skills/design-system/tokens.css` exists and is tracked
4. `ls .omp/skills/design-system/craft/typography.md` exists and is tracked
5. For all 8 migrated files: `diff <(git show HEAD~1:old) new` returns 0 (byte-identical)
6. `grep -r "500-700" .omp/commands/ .omp/templates/` returns 0 matches
7. `grep -r "300-600" .omp/commands/ .omp/templates/` returns 0 matches
8. `grep -c "≥600"` returns ≥6 across commands + templates + extensions
9. `grep -c "Worktree:" .omp/commands/pr.md` ≥1
10. `git ls-files .omp/commands/git-clean.md` returns the file
11. `grep -c "git-clean" .omp/AGENTS.md` ≥1
12. `grep "design/" .omp/memory/project/tech-stack.md` returns 0
13. `br dep cycles --json` → `"count": 0`
14. `bv --robot-triage --format json` → alerts array empty
15. `git diff --stat HEAD` after commit shows expected files only

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| Migrated design files (8) | Design system assets at correct location | `.omp/skills/design-system/` | Verify + stage |
| tech-stack.md (cleaned) | No stale path references | `.omp/memory/project/tech-stack.md` | Verify already changed |
| Density-synced commands (2) | Consistent "≥600" targets | `.omp/commands/create.md`, `plan.md` | Verify already changed |
| Density-synced templates (3) | Consistent "≥600" targets | `.omp/templates/prd.md`, `plan.md`, `tasks.md` | Verify already changed |
| Workflow-gate (hardened) | Density enforcement with informative errors | `.omp/extensions/workflow-gate.ts` | Verify already changed |
| PR footer (updated) | Worktree path in PR body | `.omp/commands/pr.md` | Verify already changed |
| git-clean command (tracked) | Worktree cleanup automation | `.omp/commands/git-clean.md` | Verify + stage |
| AGENTS.md (updated) | git-clean in command reference | `.omp/AGENTS.md` | Edit |
| completion-evidence.json | Verification results | `.beads/artifacts/br-omp-backbone-skill-vui/completion-evidence.json` | New |

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | 1.1 (content diff), 1.2 (stage design), 1.3 (rm old), 1.4 (tech-stack) | Sequential | PRD approved, bead claimed | Truths 1-5, 12 |
| 2 | 2.1 (verify density docs), 2.2 (verify gate code), 2.3 (verify PR footer) | Sequential (read-only) | Wave 1 verified | Truths 6-9 |
| 3 | 3.1 (review git-clean), 3.2 (add to AGENTS.md), 3.3 (stage git-clean) | Sequential | Wave 2 verified | Truths 10-11 |
| 4 | 4.1 (commit), 4.2 (full verify) | Immediate | Wave 3 verified | Truths 13-15 |

## Tasks

### Wave 1: Design System Migration Verification + Staging

All files already deleted from old location, present as untracked at new location. Wave 1 verifies identity, stages the move, cleans tech-stack.

#### Task 1.1: Content Identity Verification

**What it does:** For each of 8 migrated files, diffs the HEAD~1 version at the old path against the current file at the new path. Confirms byte-identical content.

**Verification commands:**
```bash
for old in DESIGN.md design/tokens.css design/primitives.css design/base.css \
  design/craft/animation-discipline.md design/craft/anti-ai-slop.md \
  design/craft/color.md design/craft/typography.md; do
  new=".omp/skills/design-system/${old#design/}"
  [ "$old" = "DESIGN.md" ] && new=".omp/skills/design-system/DESIGN.md"
  if diff <(git show "HEAD~1:$old" 2>/dev/null) "$new" > /dev/null 2>&1; then
    echo "  IDENTICAL: $old"
  else
    echo "  DIFFERS: $old — STOP"
    exit 1
  fi
done
```

**Expected:** All 8 files show "IDENTICAL". Any "DIFFERS" means the cp+rm migration modified content — restore from git history.

**If any DIFFERS:** `git show HEAD~1:<old-path> > <new-path>` to restore original, then re-verify.

**Estimated:** 1 minute

#### Task 1.2: Stage New Design Files

**What it does:** `git add` all design system files at their new location.

**Commands:**
```bash
git add .omp/skills/design-system/tokens.css
git add .omp/skills/design-system/primitives.css
git add .omp/skills/design-system/base.css
git add .omp/skills/design-system/craft/
```

**Verification:** `git status .omp/skills/design-system/` shows files as staged (A).

**Estimated:** 1 minute

#### Task 1.3: Confirm Old File Deletions

**What it does:** `git rm` all old design system files.

**Commands:**
```bash
git rm DESIGN.md
git rm design/tokens.css design/primitives.css design/base.css
git rm design/craft/animation-discipline.md design/craft/anti-ai-slop.md design/craft/color.md design/craft/typography.md
```

**Verification:** `git ls-files design/ DESIGN.md` returns nothing.

**Estimated:** 1 minute

#### Task 1.4: Verify tech-stack.md Clean

**What it does:** Confirm stale "Design Assets" table removed from tech-stack.md.

**Verification:**
```bash
grep "design/" .omp/memory/project/tech-stack.md && echo "FAIL" || echo "PASS"
wc -l .omp/memory/project/tech-stack.md
# Expected: > 30 lines (only the Design Assets table was removed)
```

**Estimated:** 0.5 minute

### Wave 2: Density Documentation Verification

All density documentation changes already exist in the working tree. Wave 2 verifies they're complete and consistent — no edits needed.

#### Task 2.1: Verify Command Density Targets

**Verification:**
```bash
# create.md: old range gone, new minimum present
grep "500-700" .omp/commands/create.md && echo "FAIL" || echo "PASS: create.md clean"
grep "≥600" .omp/commands/create.md && echo "PASS: create.md updated" || echo "FAIL"

# plan.md: old range gone, new minimum present
grep "500-700\|300-600" .omp/commands/plan.md && echo "FAIL" || echo "PASS: plan.md clean"
grep "≥600" .omp/commands/plan.md && echo "PASS: plan.md updated" || echo "FAIL"
```

**Estimated:** 0.5 minute

#### Task 2.2: Verify Template Density Headers

**Verification:**
```bash
head -1 .omp/templates/prd.md | grep -q "≥600" && echo "PASS: prd" || echo "FAIL: prd"
head -1 .omp/templates/plan.md | grep -q "≥600" && echo "PASS: plan" || echo "FAIL: plan"
head -1 .omp/templates/tasks.md | grep -q "≥600" && echo "PASS: tasks" || echo "FAIL: tasks"
```

**Estimated:** 0.5 minute

#### Task 2.3: Verify Workflow-Gate Code

**Verification:**
```bash
grep "MIN_LINES = 600" .omp/extensions/workflow-gate.ts && echo "PASS: constant" || echo "FAIL"
grep "checkDensity" .omp/extensions/workflow-gate.ts && echo "PASS: function" || echo "FAIL"
grep "readFileSync" .omp/extensions/workflow-gate.ts && echo "PASS: import" || echo "FAIL"
```

**Estimated:** 0.5 minute

#### Task 2.4: Verify PR Footer

**Verification:**
```bash
grep "Worktree:" .omp/commands/pr.md && echo "PASS" || echo "FAIL"
```

**Estimated:** 0.2 minute

### Wave 3: Infrastructure Registration

#### Task 3.1: Review git-clean.md Content

**Verification:**
```bash
head -5 .omp/commands/git-clean.md | grep -q "allowed-tools" && echo "PASS: frontmatter" || echo "WARN"
grep -c "Phase" .omp/commands/git-clean.md
grep -c ".worktree/" .omp/commands/git-clean.md
```

**Estimated:** 0.5 minute

#### Task 3.2: Add git-clean to AGENTS.md Command Table

**What it does:** Insert a new row for git-clean in the command reference table after the `/init` row.

**Current:** The `/init` row is the last entry in the command reference table.
**Insert after:** `| `/init` | Bootstrap workspace + br init | — | `.beads/` | — |`
**New row:** `| `/git-clean` | Remove merged worktrees and local branches | — | — | — |`

**Verification:**
```bash
grep -c "git-clean" .omp/AGENTS.md
# Expected: >= 1
```

**Estimated:** 1 minute

#### Task 3.3: Stage git-clean.md

**Command:**
```bash
git add .omp/commands/git-clean.md
```

**Verification:**
```bash
git ls-files .omp/commands/git-clean.md
```

**Estimated:** 0.2 minute

### Wave 4: Commit + Full Verification

#### Task 4.1: Single Atomic Commit

**Command:**
```bash
git commit -m "feat: migrate design system to .omp/skills/, sync density gates to >=600, register git-clean (br-omp-backbone-skill-vui)

- Move 8 design files from root (design/*, DESIGN.md) to .omp/skills/design-system/
- Remove stale Design Assets table from tech-stack.md
- Synchronize density targets: 500-700 to >=600 across all templates, commands, and gate
- Add density enforcement with informative error messages to workflow-gate.ts
- Add worktree path to PR footer for post-merge cleanup
- Register .omp/commands/git-clean.md as tracked command
- Add git-clean entry to AGENTS.md command reference table"
```

**Estimated:** 0.5 minute

#### Task 4.2: Full Verification Battery

Run all 13 checks, record results in completion-evidence.json.

**Estimated:** 2 minutes

## Pre-Commit Checklist

- [ ] All 8 old design files confirmed deleted from tracking
- [ ] All 8 new design files staged in `.omp/skills/design-system/`
- [ ] Content identity confirmed for all 8 files (Task 1.1)
- [ ] tech-stack.md "Design Assets" section removed
- [ ] Density headers synchronized in all 5 template/command files
- [ ] Workflow-gate density enforcement code present
- [ ] PR footer worktree injection present
- [ ] git-clean.md staged for tracking
- [ ] git-clean referenced in AGENTS.md
- [ ] br dep cycles = 0
- [ ] bv triage has 0 alerts

## Edge Cases

- **DESIGN.md already at new location:** If `.omp/skills/design-system/DESIGN.md` is already committed, skip the git add for it — only verify content identity with HEAD~1.
- **Some old files not in HEAD~1:** If design files were never committed (added in a prior uncommitted state), `git show HEAD~1:old-path` will fail. In that case, verify the new file exists and has reasonable content; skip the diff.
- **git-clean.md has merge conflicts or is incomplete:** Task 3.1 reviews content. If the file is incomplete, abort and report what's missing.

## Rollback

```bash
git reset HEAD~1
git checkout -- DESIGN.md design/ .omp/memory/project/tech-stack.md
git rm --cached .omp/commands/git-clean.md
```
