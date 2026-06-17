<!-- DENSITY: Minimum 600 lines. No upper bound — be thorough. <600 = too thin (waves undefined, tasks lack code outlines, verification hand-wavy). Task outlines should show the shape of every file change — not full implementation, but enough that a different agent can execute without reading the PRD again. -->
# Plan: br-omp-backbone-skill-fi9

**Goal:** Reconcile the diverged feature branch and main via merge with conflict resolution, clean dead artifacts, and push the result to origin — leaving a single consistent branch state with no divergence.

## Graph Context

- **Blast radius:** 8 files (5 conflict resolutions, 1 delete, 1 edit, 1 push)
  - `.omp/memory/project/conventions.md` — CONFLICT RESOLUTION (favor feature: 1-line UI Design pointer)
  - `.omp/memory/project/project.md` — CONFLICT RESOLUTION (favor feature + add Success Criterion #4)
  - `.omp/memory/project/tech-stack.md` — CONFLICT RESOLUTION (favor feature: `true #` bash blocks)
  - `.omp/skills/design-system/DESIGN.md` — CONFLICT RESOLUTION (favor feature: concrete Open Design content)
  - `.omp/skills/design-system/SKILL.md` — CONFLICT RESOLUTION (favor feature: 127-line concrete version)
  - `.omp/scripts/__pycache__/` — DELETE (dead bytecode directory)
  - `.gitignore` — EDIT (add `__pycache__/` and `*.pyc`)
  - `README.md` — EDIT (already modified, stages existing +2/-1 change)
  - `origin/main` — PUSH (push reconciled branch)
- **Unblocks:** None — this is a standalone hygiene bead. No downstream beads depend on it. However, a clean tree unblocks the next session's ability to start fresh without inheriting divergence.
- **Blocked by:** None — bead has no dependencies (confirmed via `br dep tree` returning depth 0, no parent).
- **Critical path:** No — does not block other work. No edges in the graph (15 nodes, 0 edges, density 0).
- **Forecast:** 66 minutes (confidence 0.4) — bv forecast based on 14 closed-sample velocity at 28 min/day with 1 agent. The low confidence reflects the sparse history. Actual effort may be higher than the original estimate due to the merge conflict resolution, which was not accounted for in the original brainstorm.
- **Hotspots touched:** None — none of the 5 conflicting files have >3 bead history. The highest is conventions.md with 2 bead touches (s2s on main, m6y on feature).

## Observable Truths

1. `git log --oneline --merges -1` returns a merge commit — the branch divergence is reconciled.
2. `git diff --name-only --diff-filter=U` returns empty — no unresolved merge conflicts remain.
3. `grep -rn '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/ .omp/skills/design-system/` returns no matches — no conflict markers left in files.
4. `grep -c 'load.*design-system/SKILL.md' .omp/memory/project/conventions.md` returns ≥1 — conventions.md has the 1-line UI Design pointer (feature side).
5. `grep 'stable' .omp/memory/project/project.md` returns a match — project.md has feature-side status.
6. `grep 'close-memory-audit' .omp/memory/project/project.md` returns a match — project.md has the latest milestone.
7. `grep 'Zero broken file references' .omp/memory/project/project.md` returns a match — Success Criterion #4 preserved from main.
8. `grep -c 'true  #' .omp/memory/project/tech-stack.md` returns ≥5 — bash blocks are valid shell.
9. `grep -c 'N/A' .omp/memory/project/tech-stack.md` returns 0 — no invalid N/A placeholders remain.
10. `grep -c '\[FILL\]' .omp/skills/design-system/DESIGN.md` returns 0 — DESIGN.md has concrete content, not template placeholders.
11. `test ! -d .omp/scripts/__pycache__` passes — dead bytecode directory removed.
12. `grep '__pycache__' .gitignore` returns a match — future bytecode is gitignored.
13. `git status --porcelain README.md` returns empty — README change committed.
14. `git status --short --branch` shows no ahead/behind indicator — main is up to date with origin.
15. `br sync --flush-only` exits 0 — no pending bead state.
16. `test -f .omp/RULES.md` passes and `git diff .omp/RULES.md` is empty — harness sticky rule untouched.
17. `git diff .omp/commands/init.md` is empty — inlined hydration heredoc untouched.
18. `git status --porcelain .omp/commands/npm-release.md` shows `??` — npm-release command still untracked (out of scope).

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| Merge commit | Reconciles branch divergence — brings main's 2 commits into the feature branch with 5 conflicts resolved | git history | Need — `git merge main` + conflict resolution |
| conventions.md (resolved) | 1-line UI Design pointer to design-system skill (feature side) | `.omp/memory/project/conventions.md` | Need — `git checkout --ours` |
| project.md (resolved) | Feature-side status/milestone + Success Criterion #4 from main | `.omp/memory/project/project.md` | Need — `git checkout --ours` + manual edit |
| tech-stack.md (resolved) | Valid `true #` bash blocks (feature side) | `.omp/memory/project/tech-stack.md` | Need — `git checkout --ours` |
| DESIGN.md (resolved) | Concrete Open Design content (feature side) | `.omp/skills/design-system/DESIGN.md` | Need — `git checkout --ours` |
| SKILL.md (resolved) | 127-line concrete design-system skill (feature side) | `.omp/skills/design-system/SKILL.md` | Need — `git checkout --ours` |
| Pycache deletion | Removes dead bytecode from deleted hydrate-memory.py | `.omp/scripts/__pycache__/` | Need — `rm -rf` |
| .gitignore edit | Prevents future `__pycache__/` leaks | `.gitignore` | Need — add `__pycache__/` and `*.pyc` |
| README.md commit | Commits existing npm-release row addition | `README.md` | Need — stage and commit |
| Push to origin | Pushes reconciled branch to origin/main | `origin/main` | Need — `git push origin main` |

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | 1.1 (flush bead state), 1.2 (delete pycache), 1.3 (edit gitignore) | Yes | PRD exists, bead is open, on feature branch | `br sync --flush-only` exits 0; `test ! -d .omp/scripts/__pycache__`; `grep '__pycache__' .gitignore` matches |
| 2 | 2.1 (initiate merge) | No | Wave 1 complete | Merge stops with 5 conflicts (expected) |
| 3 | 3.1-3.5 (resolve 5 conflicts, parallel where no file overlap) | Yes | Wave 2 complete (merge in progress) | All 5 files have no conflict markers; `git add` on all 5 |
| 4 | 4.1 (commit README + gitignore), 4.2 (complete merge commit) | No | Wave 3 complete | `git status --porcelain README.md` empty; merge commit exists |
| 5 | 5.1 (flush + reset main + push) | No | Wave 4 complete | `git status --short --branch` shows up to date with origin |
| 6 | 6.1 (full verification) | No | Wave 5 complete | All 18 Observable Truths pass |

## Tasks

### Wave 1: Pre-merge cleanup (parallel)

**Task 1.1: Flush bead state**

Run `br sync --flush-only` before the merge to ensure any pending bead state is written to JSONL files. This prevents the merge from conflicting with unflushed bead state.

```
br sync --flush-only
# Expected: "Nothing to export (no dirty issues)" or "Exported N issues"
```

**Verification:** `br sync --flush-only` exits 0; `git status --porcelain .beads/` shows no new untracked files.

**Task 1.2: Delete dead Python bytecode cache (parallel with 1.1, 1.3)**

Remove the `.omp/scripts/__pycache__/` directory. The source script `hydrate-memory.py` was deleted; its logic was inlined into `.omp/commands/init.md` as a Python heredoc (lines 36-456). The `.pyc` file (20.8KB) is a compilation artifact from a prior run of the standalone script, left behind when the script was removed. After deleting the pycache, the `.omp/scripts/` directory will be empty and should also be removed.

```
# Delete the pycache directory and its empty parent
rm -rf .omp/scripts/__pycache__
rmdir .omp/scripts  # Only if empty — if other files exist, keep the directory

# Verify deletion
test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"
# Expected: PASS
```

**Verification:** `test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"` returns PASS.

**Task 1.3: Add `__pycache__/` to .gitignore (parallel with 1.1, 1.2)**

Add a `__pycache__/` entry to `.gitignore` to prevent future Python bytecode from leaking. Place it in a new "Python bytecode" section after the existing "Beads runtime state" block (after line 10, `.beads/issues.jsonl`).

```
# .gitignore — current state (14 lines):
#   line 1:  # bv (beads viewer) local config and caches
#   line 2:  .bv/
#   line 3:  (blank)
#   line 4:  # Beads runtime state (SQLite, locks, touch files)
#   line 5:  .beads/beads.db
#   line 6:  .beads/beads.db-shm
#   line 7:  .beads/beads.db-wal
#   line 8:  .beads/.write.lock
#   line 9:  .beads/last-touched
#   line 10: .beads/issues.jsonl
#   line 11: (blank)
#   line 12: # Local Honcho/OMP environment overrides
#   line 13: .env
#   line 14: .worktree/

# Insert after line 11 (blank line after .beads/issues.jsonl), before line 12:
# Python bytecode
__pycache__/
*.pyc
```

The resulting .gitignore will have 17 lines:

```
# bv (beads viewer) local config and caches
.bv/

# Beads runtime state (SQLite, locks, touch files)
.beads/beads.db
.beads/beads.db-shm
.beads/beads.db-wal
.beads/.write.lock
.beads/last-touched
.beads/issues.jsonl

# Python bytecode
__pycache__/
*.pyc

# Local Honcho/OMP environment overrides
.env
.worktree/
```

**Verification:** `grep '__pycache__' .gitignore` returns a match; `grep '\*.pyc' .gitignore` returns a match.

### Wave 2: Initiate merge

**Task 2.1: Initiate merge of main into feature branch**

Run `git merge main` on the feature branch. This will attempt to merge main's 2 commits (665479d s2s, 94807b4 1da close) into the feature branch. The merge will produce 5 content conflicts (confirmed via dry-run `git merge --no-commit --no-ff main`).

```
git merge main
# Expected output:
# Auto-merging .omp/memory/project/conventions.md
# CONFLICT (content): Merge conflict in .omp/memory/project/conventions.md
# Auto-merging .omp/memory/project/project.md
# CONFLICT (content): Merge conflict in .omp/memory/project/project.md
# Auto-merging .omp/memory/project/tech-stack.md
# CONFLICT (content): Merge conflict in .omp/memory/project/tech-stack.md
# Auto-merging .omp/skills/design-system/DESIGN.md
# CONFLICT (add/add): Merge conflict in .omp/skills/design-system/DESIGN.md
# Auto-merging .omp/skills/design-system/SKILL.md
# CONFLICT (add/add): Merge conflict in .omp/skills/design-system/SKILL.md
# Automatic merge failed; fix conflicts and then commit the result.
```

**Verification:** `git diff --name-only --diff-filter=U` returns exactly these 5 files:
```
.omp/memory/project/conventions.md
.omp/memory/project/project.md
.omp/memory/project/tech-stack.md
.omp/skills/design-system/DESIGN.md
.omp/skills/design-system/SKILL.md
```

### Wave 3: Resolve conflicts (parallel where no file overlap)

**Task 3.1: Resolve conventions.md (favor feature side)**

We are ON the feature branch, merging main INTO feature. `--ours` = feature (HEAD), `--theirs` = main (the branch being merged in). We want the feature side.

```
git checkout --ours .omp/memory/project/conventions.md
git add .omp/memory/project/conventions.md
```

**After resolution, the file should have:**
- 100 lines (not 138 from main)
- UI Design section is a 1-line pointer: `For UI design rules (animation, components, icons, theme, craft), load design-system/SKILL.md. The design system is on-demand — not inlined in every session.`
- No full Animation Philosophy, CSS Ownership, Component Variants, Craft Rules, Theme, or Icons subsections (those were trimmed by m6y)

**Verification:** `grep -c 'load.*design-system/SKILL.md' .omp/memory/project/conventions.md` returns ≥1; `grep -c '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/conventions.md` returns 0.

**Task 3.2: Resolve project.md (favor feature side + add Success Criterion #4, parallel with 3.1)**

Take the feature-side version, then manually add Success Criterion #4 from main.

```
git checkout --ours .omp/memory/project/project.md
```

Then edit the file to add Success Criterion #4 after Criterion #3. The exact text to add:

```
4. **Zero broken file references in memory files** — `grep -oP '\.omp/[\w/.-]+\.\w+' .omp/memory/project/*.md | while read f; do test -f "$f" || echo "$f"; done` returns no output
```

Also update the criteria count line if it says "Keep to 3-5 criteria" — it should remain as-is since 4 is within 3-5.

```
git add .omp/memory/project/project.md
```

**After resolution, the file should have:**
- Status: `stable` (not `active` from main)
- Milestone: `Memory audit phase integrated into /close — memory file drift detection, user approval gate, STOP on full rejection (br-omp-backbone-skill-close-memory-audit-tkt)` (not s2s from main)
- Next: `Brainstorm new beads — memory maintenance cycle complete`
- Success Criterion #1: has `--exclude=project.md` (feature-side fix for self-matching grep)
- Success Criterion #4: Zero broken file references (preserved from main)

**Verification:** `grep 'stable' .omp/memory/project/project.md` returns a match; `grep 'close-memory-audit' .omp/memory/project/project.md` returns a match; `grep 'Zero broken file references' .omp/memory/project/project.md` returns a match; `grep -c '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/project.md` returns 0.

**Task 3.3: Resolve tech-stack.md (favor feature side, parallel with 3.1, 3.2)**

```
git checkout --ours .omp/memory/project/tech-stack.md
git add .omp/memory/project/tech-stack.md
```

**After resolution, the file should have:**
- 64 lines (not 63 from main)
- Bash verification blocks use `true  # <description>` (not `N/A`)
- No Design Assets or Craft References tables (both sides removed these)
- Trailing newline present

**Verification:** `grep -c 'true  #' .omp/memory/project/tech-stack.md` returns ≥5; `grep -c 'N/A' .omp/memory/project/tech-stack.md` returns 0; `grep -c '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/tech-stack.md` returns 0.

**Task 3.4: Resolve DESIGN.md (favor feature side, parallel with 3.1, 3.2, 3.3)**

```
git checkout --ours .omp/skills/design-system/DESIGN.md
git add .omp/skills/design-system/DESIGN.md
```

**After resolution, the file should have:**
- 102 lines (not 183 from main)
- Concrete Open Design content — actual color values, typography specs, spacing tokens, animation rules
- No `[FILL]` placeholders (main had 95)
- Attribution: Apache 2.0 + Open Design

**Verification:** `grep -c '\[FILL\]' .omp/skills/design-system/DESIGN.md` returns 0; `grep -c '<<<<<<<\|=======\|>>>>>>>' .omp/skills/design-system/DESIGN.md` returns 0.

**Task 3.5: Resolve SKILL.md (favor feature side, parallel with 3.1, 3.2, 3.3, 3.4)**

```
git checkout --ours .omp/skills/design-system/SKILL.md
git add .omp/skills/design-system/SKILL.md
```

**After resolution, the file should have:**
- 127 lines (not 95 from main)
- Concrete design-system skill content — actual rules, CSS ownership, component variants, theme, icons, craft rules
- Attribution: Apache 2.0 + Open Design

**Verification:** `wc -l .omp/skills/design-system/SKILL.md` returns ~127; `grep -c '<<<<<<<\|=======\|>>>>>>>' .omp/skills/design-system/SKILL.md` returns 0.

### Wave 4: Commit changes

**Task 4.1: Commit README.md and .gitignore changes**

Stage and commit the README.md change (existing +2/-1 modification adding the npm-release row to the command table) and the .gitignore edit (adding `__pycache__/` and `*.pyc`).

```
git add README.md .gitignore
git commit -m "chore: add npm-release to README, gitignore Python bytecode"
```

Note: This commit happens while the merge is in progress (MERGE_HEAD exists). Git allows making additional commits during a merge before completing the merge commit. Alternatively, these changes can be staged and included in the merge commit itself.

**Verification:** `git status --porcelain README.md .gitignore` returns empty (both committed).

**Task 4.2: Complete the merge commit**

After all conflicts are resolved (Wave 3) and additional changes are committed (Task 4.1), complete the merge commit.

```
git commit -m "Merge main into feat/br-omp-backbone-skill-1da-fix-convention-consistency — resolve 5 conflicts favoring feature side (vui/m6y/close-memory-audit work supersedes s2s content)"
```

**Verification:** `git log --oneline --merges -1` returns a merge commit; `git diff --name-only --diff-filter=U` returns empty.

### Wave 5: Sync, reset main, push

**Task 5.1: Flush bead state, reset main, push to origin**

Run `br sync --flush-only` one final time. Then update local main to point to the merged result. Then push.

```
# Flush any remaining bead state
br sync --flush-only

# Switch to main and fast-forward to the merged feature branch
git switch main
git reset --hard feat/br-omp-backbone-skill-1da-fix-convention-consistency

# Verify the push will be clean (no force needed)
git push --dry-run origin main

# Push
git push origin main
```

The `git reset --hard` is safe here because:
- We're on `main`, which is currently at 665479d (2 commits ahead of merge-base)
- The feature branch contains all of main's commits plus 13 more (the merge brings main's 2 commits into feature)
- After the merge, the feature branch contains everything main has, plus the feature-side work
- `git reset --hard feat/...` simply moves main's pointer forward to the merged result
- No commits are lost — main's 2 commits are in the merged history

**Verification:** `git status --short --branch` shows `## main...origin/main` with no ahead/behind indicator.

### Wave 6: Full verification

**Task 6.1: Verify all Observable Truths**

Run the full verification suite to confirm all 18 Observable Truths pass.

```
# Observable Truth 1: Merge commit exists
git log --oneline --merges -1  # Expected: a merge commit

# Observable Truth 2: No unresolved conflicts
git diff --name-only --diff-filter=U  # Expected: empty

# Observable Truth 3: No conflict markers
grep -rn '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/ .omp/skills/design-system/  # Expected: no matches

# Observable Truth 4: conventions.md has 1-line pointer
grep -c 'load.*design-system/SKILL.md' .omp/memory/project/conventions.md  # Expected: ≥1

# Observable Truth 5: project.md has stable status
grep 'stable' .omp/memory/project/project.md  # Expected: match

# Observable Truth 6: project.md has close-memory-audit milestone
grep 'close-memory-audit' .omp/memory/project/project.md  # Expected: match

# Observable Truth 7: project.md has Success Criterion #4
grep 'Zero broken file references' .omp/memory/project/project.md  # Expected: match

# Observable Truth 8: tech-stack.md has valid bash blocks
grep -c 'true  #' .omp/memory/project/tech-stack.md  # Expected: ≥5

# Observable Truth 9: tech-stack.md has no N/A placeholders
grep -c 'N/A' .omp/memory/project/tech-stack.md  # Expected: 0

# Observable Truth 10: DESIGN.md has no [FILL] placeholders
grep -c '\[FILL\]' .omp/skills/design-system/DESIGN.md  # Expected: 0

# Observable Truth 11: Pycache deleted
test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"  # Expected: PASS

# Observable Truth 12: Gitignore updated
grep '__pycache__' .gitignore  # Expected: match

# Observable Truth 13: README committed
git status --porcelain README.md  # Expected: empty

# Observable Truth 14: Main up to date with origin
git status --short --branch  # Expected: ## main...origin/main

# Observable Truth 15: Bead state flushed
br sync --flush-only  # Expected: exits 0

# Observable Truth 16: RULES.md untouched
test -f .omp/RULES.md && echo "PASS" || echo "FAIL"  # Expected: PASS
git diff .omp/RULES.md  # Expected: empty

# Observable Truth 17: init.md untouched
git diff .omp/commands/init.md  # Expected: empty

# Observable Truth 18: npm-release.md still untracked
git status --porcelain .omp/commands/npm-release.md  # Expected: "?? .omp/commands/npm-release.md"
```

## Full Verification

```bash
# 1. Merge completed with all conflicts resolved
git log --oneline --merges -1  # Expected: a merge commit
git diff --name-only --diff-filter=U  # Expected: empty

# 2. No conflict markers remain
grep -rn '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/ .omp/skills/design-system/  # Expected: no matches

# 3. conventions.md: feature-side content (1-line pointer)
grep -c 'load.*design-system/SKILL.md' .omp/memory/project/conventions.md  # Expected: ≥1
wc -l .omp/memory/project/conventions.md  # Expected: ~100 lines

# 4. project.md: feature-side content + Success Criterion #4
grep 'stable' .omp/memory/project/project.md  # Expected: match
grep 'close-memory-audit' .omp/memory/project/project.md  # Expected: match
grep 'Zero broken file references' .omp/memory/project/project.md  # Expected: match

# 5. tech-stack.md: valid bash blocks
grep -c 'true  #' .omp/memory/project/tech-stack.md  # Expected: ≥5
grep -c 'N/A' .omp/memory/project/tech-stack.md  # Expected: 0

# 6. DESIGN.md: concrete content (no [FILL])
grep -c '\[FILL\]' .omp/skills/design-system/DESIGN.md  # Expected: 0

# 7. SKILL.md: feature-side content
wc -l .omp/skills/design-system/SKILL.md  # Expected: ~127 lines

# 8. Pycache deleted
test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"  # Expected: PASS

# 9. Gitignore updated
grep '__pycache__' .gitignore  # Expected: match

# 10. README committed
git status --porcelain README.md  # Expected: empty

# 11. Main up to date with origin
git status --short --branch  # Expected: ## main...origin/main

# 12. Bead state flushed
br sync --flush-only  # Expected: "Nothing to export (no dirty issues)"

# 13. RULES.md untouched
test -f .omp/RULES.md && echo "PASS" || echo "FAIL"  # Expected: PASS
git diff .omp/RULES.md  # Expected: empty

# 14. init.md untouched
git diff .omp/commands/init.md  # Expected: empty

# 15. npm-release.md still untracked (out of scope)
git status --porcelain .omp/commands/npm-release.md  # Expected: "?? .omp/commands/npm-release.md"

# 16. No dependency cycles
br dep cycles --json  # Expected: {"cycles":[],"count":0,...}
```
