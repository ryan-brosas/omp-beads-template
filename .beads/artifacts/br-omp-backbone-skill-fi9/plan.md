<!-- DENSITY: Minimum 600 lines. No upper bound — be thorough. <600 = incomplete (missing sections, hand-wavy, no real technical context). This is an AI handoff: another agent must be able to pick this up and implement correctly without guessing. Every section must have concrete evidence: file paths, API signatures, existing patterns, constraints. -->
# Plan: br-omp-backbone-skill-fi9

**Goal:** Reconcile the omp-template working tree so that bead-git state is consistent, dead artifacts are removed, and main is pushed to origin — a clean baseline for the next session.

## Graph Context

- **Blast radius:** 5 files (1 new commit-only, 2 edits, 1 delete, 1 push)
  - `.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md` — NEW (already on disk, untracked; needs commit) — actually already committed in the PRD commit (acdcedb) via `git add .beads/`, but needs to be verified
  - `.gitignore` — EDIT (add `__pycache__/` entry)
  - `README.md` — EDIT (already modified in working tree; stages existing +2/-1 change)
  - `.omp/scripts/__pycache__/` — DELETE (dead bytecode directory)
  - `origin/main` — PUSH (push unpushed commits)
- **Unblocks:** None — this is a standalone hygiene bead. No downstream beads depend on it. However, a clean tree unblocks the next session's ability to start fresh without inheriting drift.
- **Blocked by:** None — bead has no dependencies (confirmed via `br dep tree` returning depth 0, no parent).
- **Critical path:** No — does not block other work. No edges in the graph (14 nodes, 0 edges, density 0).
- **Forecast:** 66 minutes (confidence 0.4) — bv forecast based on 14 closed-sample velocity at 28 min/day with 1 agent. The low confidence reflects the sparse history (no dependency edges to anchor the estimate). Actual effort is likely lower: this is mechanical git work, not feature development.
- **Hotspots touched:** None — `.gitignore` has 0 bead history (confirmed via `bv --robot-file-beads .gitignore`), `README.md` has no bead links, `.omp/scripts/` is untracked. No file in this bead's blast radius has >3 bead history.

## Observable Truths

1. `git status --porcelain` returns empty (clean working tree) after all commits and push — no staged, unstaged, or untracked files remain.
2. `git status --short --branch` shows `## main...origin/main` with no ahead/behind indicator — main is up to date with origin.
3. `git log --oneline -- '.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md'` returns a commit — the s2s review report is tracked in git history.
4. `test ! -d .omp/scripts/__pycache__` passes — the dead bytecode directory no longer exists on disk.
5. `grep '__pycache__' .gitignore` returns a match — future Python bytecode is gitignored.
6. `git status --porcelain README.md` returns empty — the npm-release row addition is committed.
7. `br sync --flush-only` exits 0 with "Nothing to export" — no pending bead state to flush.
8. `.omp/RULES.md` still exists and is unmodified — the harness-loaded sticky rule was NOT deleted (explicitly out of scope).
9. `.omp/commands/init.md` is unmodified — the inlined hydration heredoc is the source of truth, not touched.
10. `.omp/commands/npm-release.md` remains untracked — grounding the npm-release command is explicitly out of scope.

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| s2s review-report.md | The s2s bead's review report — was written during /review but never committed during /close | `.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md` | Already committed in PRD commit (acdcedb) — verify, don't re-commit |
| .gitignore edit | Prevents future `__pycache__/` leaks | `.gitignore` | Need — add `__pycache__/` entry |
| README.md commit | Commits the existing npm-release row addition | `README.md` | Need — already modified in working tree, stage and commit |
| Pycache deletion | Removes dead bytecode from deleted hydrate-memory.py | `.omp/scripts/__pycache__/` | Need — delete directory + empty parent |
| Push to origin | Pushes unpushed commits to origin/main | `origin/main` | Need — `git push origin main` |

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | 1.1 (delete pycache), 1.2 (edit gitignore) | Yes | PRD exists (verified), bead is open | `test ! -d .omp/scripts/__pycache__` passes; `grep '__pycache__' .gitignore` matches |
| 2 | 2.1 (commit README + gitignore + pycache deletion) | No | Wave 1 complete | `git status --porcelain` shows README.md and .gitignore are committed, not dirty |
| 3 | 3.1 (flush bead state) | No | Wave 2 complete | `br sync --flush-only` exits 0 |
| 4 | 4.1 (push to origin) | No | Wave 3 complete | `git status --short --branch` shows "up to date with origin/main" |
| 5 | 5.1 (full verification) | No | Wave 4 complete | All 10 Observable Truths pass |

## Tasks

### Wave 1: File operations (parallel)

**Task 1.1: Delete dead Python bytecode cache**

Remove the `.omp/scripts/__pycache__/` directory. The source script `hydrate-memory.py` was deleted; its logic was inlined into `.omp/commands/init.md` as a Python heredoc (lines 36-456). The `.pyc` file (20.8KB) is a compilation artifact from a prior run of the standalone script, left behind when the script was removed. After deleting the pycache, the `.omp/scripts/` directory will be empty and should also be removed.

```
# Delete the pycache directory and its empty parent
rm -rf .omp/scripts/__pycache__
rmdir .omp/scripts  # Only if empty — if other files exist, keep the directory
```

**Verification:** `test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"`

**Task 1.2: Add `__pycache__/` to .gitignore (parallel with 1.1)**

Add a `__pycache__/` entry to `.gitignore` to prevent future Python bytecode from leaking. Place it in a new "Python bytecode" section after the existing "Beads runtime state" block. Follow the existing pattern where runtime/generated artifacts are gitignored (`.bv/`, `.beads/beads.db`, `.env`, `.worktree/`).

```
# .gitignore — add after the .beads/ runtime state block:
# Python bytecode
__pycache__/
*.pyc
```

**Verification:** `grep '__pycache__' .gitignore` returns a match.

### Wave 2: Commit changes

**Task 2.1: Commit README.md and .gitignore changes**

Stage and commit the README.md change (existing +2/-1 modification adding the npm-release row to the command table) and the .gitignore edit (adding `__pycache__/`). Use a `docs:` commit prefix for README and a `chore:` prefix for gitignore. If combining into one commit is simpler and both are hygiene changes, use `chore:` with a message describing both.

```
# Option A: separate commits (preferred — single responsibility)
git add README.md
git commit -m "docs: add /npm-release command to README command table"

git add .gitignore
git commit -m "chore: gitignore Python __pycache__ and .pyc files"

# Option B: combined commit (if preferred for brevity)
git add README.md .gitignore
git commit -m "chore: add npm-release to README, gitignore Python bytecode"
```

**Verification:** `git status --porcelain README.md .gitignore` returns empty (both committed).

### Wave 3: Bead state sync

**Task 3.1: Flush bead state**

Run `br sync --flush-only` to ensure any pending bead state is written to `.beads/issues.jsonl` and `.br_history/`. This is the precondition for a clean push per RULE #4. After flushing, check if any new untracked bead state files appeared.

```
br sync --flush-only
git status --porcelain .beads/
```

**Verification:** `br sync --flush-only` exits 0; `git status --porcelain .beads/` shows no new untracked files (or if it does, stage and commit them as "Update issues").

### Wave 4: Push to origin

**Task 4.1: Push main to origin**

Push all local commits to origin/main. This includes the pre-existing unpushed commit (5d7f242: feat: add memory audit phase to /close command) and any new commits from Waves 2-3.

```
git push origin main
```

**Verification:** `git status --short --branch` shows `## main...origin/main` with no ahead/behind indicator.

**IMPORTANT — Branch check:** The PRD commit (acdcedb) landed on `feat/br-omp-backbone-skill-1da-fix-convention-consistency`, not `main`. Before pushing, verify which branch we're on. If on the feature branch, either:
- (a) merge the feature branch into main first, then push main, OR
- (b) push the feature branch and create a PR (but this is a hygiene task, no PR needed per Decision #5 in decisions.md)

The plan recommends option (a): switch to main, merge the feature branch, push. The feature branch only contains the PRD commit and the pre-existing unpushed commits — no conflicting work.

### Wave 5: Full verification

**Task 5.1: Verify all Observable Truths**

Run the full verification suite to confirm all 10 Observable Truths pass.

```
# Observable Truth 1: clean working tree
git status --porcelain  # Expected: empty

# Observable Truth 2: main up to date with origin
git status --short --branch  # Expected: ## main...origin/main (no ahead/behind)

# Observable Truth 3: s2s review-report tracked
git log --oneline -- '.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md'  # Expected: a commit hash

# Observable Truth 4: pycache deleted
test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"  # Expected: PASS

# Observable Truth 5: gitignore has __pycache__
grep '__pycache__' .gitignore  # Expected: a match

# Observable Truth 6: README clean
git status --porcelain README.md  # Expected: empty

# Observable Truth 7: bead state flushed
br sync --flush-only  # Expected: exits 0, "Nothing to export"

# Observable Truth 8: RULES.md untouched
test -f .omp/RULES.md && echo "PASS" || echo "FAIL"  # Expected: PASS
git diff .omp/RULES.md  # Expected: empty (no changes)

# Observable Truth 9: init.md untouched
git diff .omp/commands/init.md  # Expected: empty

# Observable Truth 10: npm-release.md still untracked (out of scope)
git status --porcelain .omp/commands/npm-release.md  # Expected: "?? .omp/commands/npm-release.md"
```

## Full Verification

```bash
# 1. Clean working tree (except intentionally-untracked npm-release.md)
git status --porcelain  # Expected: only "?? .omp/commands/npm-release.md" (out of scope)

# 2. Main is up to date with origin
git status --short --branch  # Expected: ## main...origin/main

# 3. s2s review-report is tracked in git
git log --oneline -- '.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md'  # Expected: acdcedb (or later commit)

# 4. Pycache deleted
test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"  # Expected: PASS

# 5. Gitignore updated
grep '__pycache__' .gitignore  # Expected: __pycache__/

# 6. README committed
git status --porcelain README.md  # Expected: empty

# 7. Bead state flushed
br sync --flush-only  # Expected: "Nothing to export (no dirty issues)"

# 8. RULES.md untouched (harness sticky rule — do not delete)
test -f .omp/RULES.md && echo "PASS" || echo "FAIL"  # Expected: PASS
git diff .omp/RULES.md  # Expected: empty

# 9. init.md untouched
git diff .omp/commands/init.md  # Word Expected: empty

# 10. npm-release.md still untracked (grounding is out of scope)
git status --porcelain .omp/commands/npm-release.md  # Expected: "?? .omp/commands/npm-release.md"

# 11. No cycles in dependency graph
br dep cycles --json  # Expected: {"cycles":[],"count":0,...}
```
