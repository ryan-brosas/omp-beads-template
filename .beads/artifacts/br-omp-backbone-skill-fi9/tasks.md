<!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin — tasks lack detail, verification steps are vague, dependencies undefined. Every task needs a yaml block, concrete verification steps, and enough detail for parallel execution without reading the PRD or plan. -->
# Tasks: br-omp-backbone-skill-fi9

## 1. File operations (Wave 1 — parallel)

### 1.1 Delete dead Python bytecode cache

```yaml
depends_on: []
parallel: true
conflicts_with: ["1.2"]
files: [".omp/scripts/__pycache__/hydrate-memory.cpython-311.pyc", ".omp/scripts/"]
estimated_minutes: 2
```

- [ ] Confirm the `.omp/scripts/` directory contains only the `__pycache__/` subdirectory (no other files that should be preserved)
- [ ] Delete the `__pycache__/` directory: `rm -rf .omp/scripts/__pycache__`
- [ ] Remove the now-empty `.omp/scripts/` directory: `rmdir .omp/scripts` (only if empty — if other files exist, keep the directory and skip this step)
- [ ] Verify: `test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"` — Expected: PASS
- [ ] Verify: `test ! -d .omp/scripts && echo "PASS" || echo "FAIL"` — Expected: PASS (directory removed if it was empty)

### 1.2 Add `__pycache__/` to .gitignore (parallel with 1.1)

```yaml
depends_on: []
parallel: true
conflicts_with: ["1.2"]
files: [".gitignore"]
estimated_minutes: 2
```

- [ ] Read the current `.gitignore` file to understand the existing structure and comment style
- [ ] Add a new section after the "Beads runtime state" block (after the `.beads/issues.jsonl` line) with a comment header and the `__pycache__/` pattern
- [ ] Also add `*.pyc` to catch standalone bytecode files that might appear outside `__pycache__/` directories
- [ ] The added lines should be:
  ```
  # Python bytecode
  __pycache__/
  *.pyc
  ```
- [ ] Verify: `grep '__pycache__' .gitignore` returns a match
- [ ] Verify: `grep '\*.pyc' .gitignore` returns a match

## 2. Commit changes (Wave 2 — sequential)

### 2.1 Commit README.md and .gitignore changes

```yaml
depends_on: ["1.1", "1.2"]
parallel: false
conflicts_with: []
files: ["README.md", ".gitignore"]
estimated_minutes: 5
```

- [ ] Stage the README.md change: `git add README.md`
- [ ] Stage the .gitignore change: `git add .gitignore`
- [ ] Commit with a combined message (both are hygiene changes): `git commit -m "chore: add npm-release to README, gitignore Python bytecode"`
- [ ] Alternatively, use two separate commits for single-responsibility:
  - `git commit -m "docs: add /npm-release command to README command table" README.md`
  - `git commit -m "chore: gitignore Python __pycache__ and .pyc files" .gitignore`
- [ ] Verify: `git status --porcelain README.md .gitignore` returns empty (both committed)
- [ ] Verify: `git log --oneline -2` shows the new commit(s) with `chore:` or `docs:` prefix

## 3. Bead state sync (Wave 3 — sequential)

### 3.1 Flush bead state

```yaml
depends_on: ["2.1"]
parallel: false
conflicts_with: []
files: [".beads/issues.jsonl", ".beads/.br_history/"]
estimated_minutes: 2
```

- [ ] Run `br sync --flush-only` to flush any pending bead state to JSONL files
- [ ] Check for new untracked bead state files: `git status --porcelain .beads/`
- [ ] If new untracked files appeared (e.g., new `.br_history/*.jsonl` snapshots), stage and commit them: `git add .beads/ && git commit -m "Update issues"`
- [ ] If no new files appeared, proceed to Wave 4
- [ ] Verify: `br sync --flush-only` exits 0
- [ ] Verify: `git status --porcelain .beads/` shows no untracked bead state files (or they've been committed)

## 4. Push to origin (Wave 4 — sequential)

### 4.1 Push main to origin

```yaml
depends_on: ["3.1"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 5
```

- [ ] Check current branch: `git branch --show-current`
- [ ] If on `feat/br-omp-backbone-skill-1da-fix-convention-consistency` (the branch the PRD commit landed on), switch to main: `git switch main`
- [ ] Merge the feature branch into main to bring the PRD commit and any hygiene commits onto main: `git merge feat/br-omp-backbone-skill-1da-fix-convention-consistency`
- [ ] If already on main, skip the merge step
- [ ] Push to origin: `git push origin main`
- [ ] If push is rejected (e.g., behind origin), pull first: `git pull --rebase origin main` then retry push
- [ ] Verify: `git status --short --branch` shows `## main...origin/main` with no ahead/behind indicator

## 5. Full verification (Wave 5 — sequential)

### 5.1 Full verification

```yaml
depends_on: ["4.1"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 5
```

- [ ] Verify Observable Truth 1: `git status --porcelain` returns empty (or only `?? .omp/commands/npm-release.md` which is out of scope)
- [ ] Verify Observable Truth 2: `git status --short --branch` shows `## main...origin/main` with no ahead/behind
- [ ] Verify Observable Truth 3: `git log --oneline -- '.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md'` returns a commit
- [ ] Verify Observable Truth 4: `test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"` returns PASS
- [ ] Verify Observable Truth 5: `grep '__pycache__' .gitignore` returns a match
- [ ] Verify Observable Truth 6: `git status --porcelain README.md` returns empty
- [ ] Verify Observable Truth 7: `br sync --flush-only` exits 0
- [ ] Verify Observable Truth 8: `test -f .omp/RULES.md && echo "PASS" || echo "FAIL"` returns PASS; `git diff .omp/RULES.md` is empty
- [ ] Verify Observable Truth 9: `git diff .omp/commands/init.md` is empty
- [ ] Verify Observable Truth 10: `git status --porcelain .omp/commands/npm-release.md` shows `?? .omp/commands/npm-release.md` (still untracked, out of scope)
- [ ] Verify no dependency cycles: `br dep cycles --json` returns `{"cycles":[],"count":0,...}`

## 6. Post-verification

### 6.1 Record completion evidence

```yaml
depends_on: ["5.1"]
parallel: false
conflicts_with: []
files: [".beads/artifacts/br-omp-backbone-skill-fi9/completion-evidence.json"]
estimated_minutes: 5
```

- [ ] Capture the output of all verification commands from Task 5.1
- [ ] Write the results to `.beads/artifacts/br-omp-backbone-skill-fi9/completion-evidence.json` with each observable truth, the command run, and the result
- [ ] Verify: `test -f .beads/artifacts/br-omp-backbone-skill-fi9/completion-evidence.json` passes
- [ ] Verify: the JSON is valid: `python3 -c "import json; json.load(open('.beads/artifacts/br-omp-backbone-skill-fi9/completion-evidence.json'))"` exits 0
