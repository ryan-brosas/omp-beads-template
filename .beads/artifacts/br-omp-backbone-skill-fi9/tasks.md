<!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin — tasks lack detail, verification steps are vague, dependencies undefined. Every task needs a yaml block, concrete verification steps, and enough detail for parallel execution without reading the PRD or plan. -->
# Tasks: br-omp-backbone-skill-fi9

## 1. Pre-merge cleanup (Wave 1 — parallel)

### 1.1 Flush bead state

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".beads/issues.jsonl", ".beads/.br_history/"]
estimated_minutes: 1
```

- [ ] Run `br sync --flush-only` to flush any pending bead state to JSONL files before the merge
- [ ] Check for new untracked bead state files: `git status --porcelain .beads/`
- [ ] If new untracked files appeared, stage and commit them: `git add .beads/ && git commit -m "Update issues"`
- [ ] If no new files appeared, proceed to Wave 2
- [ ] Verify: `br sync --flush-only` exits 0
- [ ] Verify: `git status --porcelain .beads/` shows no untracked bead state files (or they've been committed)

### 1.2 Delete dead Python bytecode cache (parallel with 1.1, 1.3)

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/scripts/__pycache__/hydrate-memory.cpython-311.pyc", ".omp/scripts/"]
estimated_minutes: 2
```

- [ ] Confirm the `.omp/scripts/` directory contains only the `__pycache__/` subdirectory: `ls -la .omp/scripts/`
- [ ] Delete the `__pycache__/` directory: `rm -rf .omp/scripts/__pycache__`
- [ ] Remove the now-empty `.omp/scripts/` directory: `rmdir .omp/scripts` (only if empty — if other files exist, keep the directory and skip this step)
- [ ] Verify: `test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"` — Expected: PASS
- [ ] Verify: `test ! -d .omp/scripts && echo "PASS" || echo "FAIL"` — Expected: PASS (directory removed if it was empty)

### 1.3 Add `__pycache__/` to .gitignore (parallel with 1.1, 1.2)

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".gitignore"]
estimated_minutes: 2
```

- [ ] Read the current `.gitignore` file (14 lines) to understand the existing structure and comment style
- [ ] Insert a new section after the "Beads runtime state" block (after line 11, the blank line after `.beads/issues.jsonl`), before the "# Local Honcho/OMP environment overrides" comment
- [ ] The added lines should be exactly:
  ```
  # Python bytecode
  __pycache__/
  *.pyc
  ```
- [ ] The resulting .gitignore should have 17 lines total with the new section between the Beads runtime state and Local Honcho sections
- [ ] Verify: `grep '__pycache__' .gitignore` returns a match
- [ ] Verify: `grep '\*.pyc' .gitignore` returns a match
- [ ] Verify: `grep -c '' .gitignore` returns 17 (17 lines total)

## 2. Initiate merge (Wave 2 — sequential)

### 2.1 Initiate merge of main into feature branch

```yaml
depends_on: ["1.1", "1.2", "1.3"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 1
```

- [ ] Confirm current branch is `feat/br-omp-backbone-skill-1da-fix-convention-consistency`: `git branch --show-current`
- [ ] Run the merge: `git merge main`
- [ ] Observe the 5 expected conflicts:
  - `CONFLICT (content): Merge conflict in .omp/memory/project/conventions.md`
  - `CONFLICT (content): Merge conflict in .omp/memory/project/project.md`
  - `CONFLICT (content): Merge conflict in .omp/memory/project/tech-stack.md`
  - `CONFLICT (add/add): Merge conflict in .omp/skills/design-system/DESIGN.md`
  - `CONFLICT (add/add): Merge conflict in .omp/skills/design-system/SKILL.md`
- [ ] Verify: `git diff --name-only --diff-filter=U` returns exactly these 5 files
- [ ] Verify: `git status` shows "You have unmerged paths" and "fix conflicts and then commit the result"

## 3. Resolve conflicts (Wave 3 — parallel where no file overlap)

### 3.1 Resolve conventions.md (favor feature side)

```yaml
depends_on: ["2.1"]
parallel: true
conflicts_with: ["3.2"]  # project.md is in the same directory but different file — no real conflict
files: [".omp/memory/project/conventions.md"]
estimated_minutes: 2
```

**Context:** We are ON the feature branch, merging main INTO feature. `--ours` = feature (HEAD) = the m6y-trimmed version with 1-line UI Design pointer. `--theirs` = main = the s2s version with full UI Design content (138 lines). We want the feature side.

- [ ] Take the feature-side version: `git checkout --ours .omp/memory/project/conventions.md`
- [ ] Stage the resolved file: `git add .omp/memory/project/conventions.md`
- [ ] Verify: `grep -c 'load.*design-system/SKILL.md' .omp/memory/project/conventions.md` returns ≥1 (1-line pointer present)
- [ ] Verify: `wc -l .omp/memory/project/conventions.md` returns ~100 lines (not 138 from main)
- [ ] Verify: `grep -c '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/conventions.md` returns 0 (no conflict markers)

### 3.2 Resolve project.md (favor feature side + add Success Criterion #4, parallel with 3.1)

```yaml
depends_on: ["2.1"]
parallel: true
conflicts_with: ["3.1"]
files: [".omp/memory/project/project.md"]
estimated_minutes: 5
```

**Context:** The feature side has status=`stable`, milestone=`close-memory-audit`, and `--exclude=project.md` grep fix. The main side has status=`active`, milestone=`s2s`, and Success Criterion #4. We want the feature side PLUS Success Criterion #4 from main.

- [ ] Take the feature-side version: `git checkout --ours .omp/memory/project/project.md`
- [ ] Read the file to find the Success Criteria section
- [ ] Manually add Success Criterion #4 after Criterion #3. The exact text to add:
  ```
  4. **Zero broken file references in memory files** — `grep -oP '\.omp/[\w/.-]+\.\w+' .omp/memory/project/*.md | while read f; do test -f "$f" || echo "$f"; done` returns no output
  ```
- [ ] Ensure the "Keep to 3-5 criteria" line remains (4 is within 3-5)
- [ ] Stage the resolved file: `git add .omp/memory/project/project.md`
- [ ] Verify: `grep 'stable' .omp/memory/project/project.md` returns a match
- [ ] Verify: `grep 'close-memory-audit' .omp/memory/project/project.md` returns a match
- [ ] Verify: `grep 'Zero broken file references' .omp/memory/project/project.md` returns a match
- [ ] Verify: `grep -- '--exclude=project.md' .omp/memory/project/project.md` returns a match (grep self-matching fix)
- [ ] Verify: `grep -c '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/project.md` returns 0

### 3.3 Resolve tech-stack.md (favor feature side, parallel with 3.1, 3.2)

```yaml
depends_on: ["2.1"]
parallel: true
conflicts_with: []
files: [".omp/memory/project/tech-stack.md"]
estimated_minutes: 1
```

**Context:** Both sides removed the Design Assets and Craft References tables. The feature side replaced `N/A` bash placeholders with valid `true  # <description>` commands. The main side left `N/A` placeholders (invalid shell). We want the feature side.

- [ ] Take the feature-side version: `git checkout --ours .omp/memory/project/tech-stack.md`
- [ ] Stage the resolved file: `git add .omp/memory/project/tech-stack.md`
- [ ] Verify: `grep -c 'true  #' .omp/memory/project/tech-stack.md` returns ≥5 (valid bash blocks)
- [ ] Verify: `grep -c 'N/A' .omp/memory/project/tech-stack.md` returns 0 (no invalid placeholders)
- [ ] Verify: `grep -c 'Design Assets\|Craft References' .omp/memory/project/tech-stack.md` returns 0 (stale tables removed)
- [ ] Verify: `grep -c '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/tech-stack.md` returns 0

### 3.4 Resolve DESIGN.md (favor feature side, parallel with 3.1, 3.2, 3.3)

```yaml
depends_on: ["2.1"]
parallel: true
conflicts_with: []
files: [".omp/skills/design-system/DESIGN.md"]
estimated_minutes: 1
```

**Context:** Main created DESIGN.md as a [FILL] template (183 lines, 95 placeholders). Feature side has concrete Open Design content (102 lines, no placeholders). Per user decision, we want the feature side (concrete content).

- [ ] Take the feature-side version: `git checkout --ours .omp/skills/design-system/DESIGN.md`
- [ ] Stage the resolved file: `git add .omp/skills/design-system/DESIGN.md`
- [ ] Verify: `grep -c '\[FILL\]' .omp/skills/design-system/DESIGN.md` returns 0 (no template placeholders)
- [ ] Verify: `wc -l .omp/skills/design-system/DESIGN.md` returns ~102 lines
- [ ] Verify: `grep -c '<<<<<<<\|=======\|>>>>>>>' .omp/skills/design-system/DESIGN.md` returns 0

### 3.5 Resolve SKILL.md (favor feature side, parallel with 3.1, 3.2, 3.3, 3.4)

```yaml
depends_on: ["2.1"]
parallel: true
conflicts_with: []
files: [".omp/skills/design-system/SKILL.md"]
estimated_minutes: 1
```

**Context:** Main created SKILL.md as a 95-line template-oriented skill. Feature side has a 127-line concrete version. Per user decision, we want the feature side (concrete content).

- [ ] Take the feature-side version: `git checkout --ours .omp/skills/design-system/SKILL.md`
- [ ] Stage the resolved file: `git add .omp/skills/design-system/SKILL.md`
- [ ] Verify: `wc -l .omp/skills/design-system/SKILL.md` returns ~127 lines
- [ ] Verify: `grep -c '<<<<<<<\|=======\|>>>>>>>' .omp/skills/design-system/SKILL.md` returns 0

## 4. Commit changes (Wave 4 — sequential)

### 4.1 Commit README.md and .gitignore changes

```yaml
depends_on: ["3.1", "3.2", "3.3", "3.4", "3.5"]
parallel: false
conflicts_with: []
files: ["README.md", ".gitignore"]
estimated_minutes: 2
```

**Context:** The merge is in progress (MERGE_HEAD exists). We can stage and commit additional changes before completing the merge commit. README.md has an existing +2/-1 modification (adds npm-release row). .gitignore has the new `__pycache__/` and `*.pyc` entries from Task 1.3.

- [ ] Stage the README.md change: `git add README.md`
- [ ] Stage the .gitignore change: `git add .gitignore`
- [ ] Commit with a combined message: `git commit -m "chore: add npm-release to README, gitignore Python bytecode"`
- [ ] Verify: `git status --porcelain README.md .gitignore` returns empty (both committed)

### 4.2 Complete the merge commit

```yaml
depends_on: ["4.1"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 1
```

**Context:** All 5 conflicts are resolved and staged (Wave 3). README.md and .gitignore are committed (Task 4.1). Now complete the merge commit.

- [ ] Verify all conflicts are resolved: `git diff --name-only --diff-filter=U` returns empty
- [ ] Verify no conflict markers remain: `grep -rn '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/ .omp/skills/design-system/` returns no matches
- [ ] Complete the merge commit: `git commit -m "Merge main into feat/br-omp-backbone-skill-1da-fix-convention-consistency — resolve 5 conflicts favoring feature side (vui/m6y/close-memory-audit work supersedes s2s content)"`
- [ ] Verify: `git log --oneline --merges -1` returns a merge commit
- [ ] Verify: `git diff --name-only --diff-filter=U` returns empty (no unresolved conflicts)
- [ ] Verify: `git status` shows "All conflicts fixed but you are still merging" → then after commit, clean state

## 5. Sync, reset main, push (Wave 5 — sequential)

### 5.1 Flush bead state, reset main, push to origin

```yaml
depends_on: ["4.2"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 5
```

**Context:** The merge is complete on the feature branch. Now we need to update main to point to the merged result and push to origin. The `git reset --hard` is safe because the feature branch (after merge) contains all of main's commits plus the feature-side work.

- [ ] Run `br sync --flush-only` to flush any remaining bead state
- [ ] Check for new untracked bead state files: `git status --porcelain .beads/`
- [ ] If new untracked files appeared, stage and commit them: `git add .beads/ && git commit -m "Update issues"`
- [ ] Switch to main: `git switch main`
- [ ] Reset main to the merged feature branch: `git reset --hard feat/br-omp-backbone-skill-1da-fix-convention-consistency`
- [ ] Verify the push will be clean (no force needed): `git push --dry-run origin main`
- [ ] Push to origin: `git push origin main`
- [ ] If push is rejected (e.g., behind origin), pull first: `git pull --rebase origin main` then retry push
- [ ] Verify: `git status --short --branch` shows `## main...origin/main` with no ahead/behind indicator

## 6. Full verification (Wave 6 — sequential)

### 6.1 Full verification

```yaml
depends_on: ["5.1"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 5
```

- [ ] Verify Observable Truth 1: `git log --oneline --merges -1` returns a merge commit
- [ ] Verify Observable Truth 2: `git diff --name-only --diff-filter=U` returns empty
- [ ] Verify Observable Truth 3: `grep -rn '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/ .omp/skills/design-system/` returns no matches
- [ ] Verify Observable Truth 4: `grep -c 'load.*design-system/SKILL.md' .omp/memory/project/conventions.md` returns ≥1
- [ ] Verify Observable Truth 5: `grep 'stable' .omp/memory/project/project.md` returns a match
- [ ] Verify Observable Truth 6: `grep 'close-memory-audit' .omp/memory/project/project.md` returns a match
- [ ] Verify Observable Truth 7: `grep 'Zero broken file references' .omp/memory/project/project.md` returns a match
- [ ] Verify Observable Truth 8: `grep -c 'true  #' .omp/memory/project/tech-stack.md` returns ≥5
- [ ] Verify Observable Truth 9: `grep -c 'N/A' .omp/memory/project/tech-stack.md` returns 0
- [ ] Verify Observable Truth 10: `grep -c '\[FILL\]' .omp/skills/design-system/DESIGN.md` returns 0
- [ ] Verify Observable Truth 11: `test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"` returns PASS
- [ ] Verify Observable Truth 12: `grep '__pycache__' .gitignore` returns a match
- [ ] Verify Observable Truth 13: `git status --porcelain README.md` returns empty
- [ ] Verify Observable Truth 14: `git status --short --branch` shows `## main...origin/main` with no ahead/behind
- [ ] Verify Observable Truth 15: `br sync --flush-only` exits 0
- [ ] Verify Observable Truth 16: `test -f .omp/RULES.md && echo "PASS" || echo "FAIL"` returns PASS; `git diff .omp/RULES.md` is empty
- [ ] Verify Observable Truth 17: `git diff .omp/commands/init.md` is empty
- [ ] Verify Observable Truth 18: `git status --porcelain .omp/commands/npm-release.md` shows `?? .omp/commands/npm-release.md`
- [ ] Verify no dependency cycles: `br dep cycles --json` returns `{"cycles":[],"count":0,...}`

## 7. Post-verification

### 7.1 Record completion evidence

```yaml
depends_on: ["6.1"]
parallel: false
conflicts_with: []
files: [".beads/artifacts/br-omp-backbone-skill-fi9/completion-evidence.json"]
estimated_minutes: 5
```

- [ ] Capture the output of all verification commands from Task 6.1
- [ ] Write the results to `.beads/artifacts/br-omp-backbone-skill-fi9/completion-evidence.json` with each observable truth, the command run, and the result
- [ ] Verify: `test -f .beads/artifacts/br-omp-backbone-skill-fi9/completion-evidence.json` passes
- [ ] Verify: the JSON is valid: `python3 -c "import json; json.load(open('.beads/artifacts/br-omp-backbone-skill-fi9/completion-evidence.json'))"` exits 0
