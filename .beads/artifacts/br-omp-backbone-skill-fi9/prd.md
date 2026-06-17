<!-- DENSITY: Minimum 600 lines. No upper bound — be thorough. <600 = incomplete (missing sections, hand-wavy, no real technical context). This is an AI handoff: another agent must be able to pick this up and implement correctly without guessing. Every section must have concrete evidence: file paths, API signatures, existing patterns, constraints. -->
# PRD: Reconcile repo state — commit s2s closeout artifacts, excise dead pycache, push unpushed work

**Bead:** br-omp-backbone-skill-fi9 | **Type:** chore | **Priority:** P2
**Created:** 2026-06-17 | **Estimate:** 45

## Problem

WHEN the `feat/br-omp-backbone-skill-1da-fix-convention-consistency` branch and `main` diverged from merge-base `b32e245` (13 commits ago) THEN 5 files developed conflicting content across the two branches BECAUSE bead work continued independently on both branches without synchronization — `main` received the s2s bead (665479d: design-system skill creation + memory file updates) and 1da close (94807b4), while the feature branch received vui (5253d81: design-system migration + density gates), vui review fix (7f78661), vui evidence (04281b5), vui close (f4816fa), m6y (3d4a54e, 60ef1dd, 4d60a0e, 194c79a: conventions trim, success criteria hardening, tree completion), close-memory-audit (a5d47d4, 8f73a9c, 5d7f242: /close memory audit phase), and fi9 PRD+plan (acdcedb, b95d2c8) — and no merge was performed between them, so both branches independently modified the same 5 files (conventions.md, project.md, tech-stack.md, DESIGN.md, SKILL.md) with different intent and different content.

This affects every future agent that opens the repository. The working tree is on a feature branch that has diverged from main by 15 commits, while main has diverged from the feature branch by 2 commits. A dry-run merge (`git merge --no-commit --no-ff main`) produces 5 content conflicts. Additionally, the working tree carries accumulated drift: a stale Python bytecode cache from a deleted script, an uncommitted README.md change, and an unpushed commit on main (665479d, the s2s bead, was never pushed to origin/main which sits at 94807b4). If we don't reconcile this now, the branches diverge further with each subsequent bead, the conflict surface grows, and the merge becomes harder to attribute and resolve.

The s2s bead closeout gap (review-report.md untracked) was partially resolved during the `/create` phase: the PRD commit (acdcedb) staged `.beads/` wholesale, which included the s2s review-report.md and 6 `.br_history` files. These are now tracked in git, but under a `docs:` commit rather than a `close:` commit. This is acceptable — the artifacts are committed, the state mismatch is resolved at the filesystem level, and the commit prefix is a SHOULD not MUST requirement.

## Scope

### In Scope
- Merge `main` into the feature branch `feat/br-omp-backbone-skill-1da-fix-convention-consistency`, resolving all 5 content conflicts
- Conflict resolution per file (determined by investigation — see Technical Context):
  - `.omp/memory/project/conventions.md` → favor feature side (m6y bead trimmed UI Design to 1-line pointer; main's s2s added full content that m6y explicitly removed)
  - `.omp/memory/project/project.md` → favor feature side (close-memory-audit is the latest milestone; main's s2s milestone is superseded)
  - `.omp/memory/project/tech-stack.md` → favor feature side (m6y made bash blocks valid with `true #` replacements; main has invalid `N/A` placeholders)
  - `.omp/skills/design-system/DESIGN.md` → favor feature side (concrete Open Design content per user decision; main has [FILL] template version)
  - `.omp/skills/design-system/SKILL.md` → favor feature side (concrete content per user decision; main has template version)
- Delete `.omp/scripts/__pycache__/hydrate-memory.cpython-311.pyc` — dead bytecode, source script deleted, logic inlined into `.omp/commands/init.md` heredoc
- Add `__pycache__/` and `*.pyc` to `.gitignore` to prevent future bytecode leaks
- Commit the uncommitted `README.md` change (adds `/npm-release` row to command table)
- Push the reconciled branch to `origin/main` so origin matches local state

### Out of Scope
- **Do NOT delete `.omp/RULES.md`** — it is a harness-loaded sticky rule (always-apply), injected into every agent's system prompt `<generic-rules>` block. Verified via OMP docs (`omp://context-files.md`): `.omp/RULES.md` is loaded as an always-apply rule at the native project location. Deleting it would strip the 6 workflow rules from every session. It is NOT a duplicate of AGENTS.md — AGENTS.md's Guardrails section is different, softer content.
- Do NOT modify the `npm-release.md` command itself — grounding it (package.json, workflow, trusted publishing) is a separate bead, a design decision
- Do NOT modify any closed bead's existing artifacts (prd.md, plan.md, etc.) — the s2s review-report.md is already committed in the PRD commit
- Do NOT rebase or rewrite existing commits — merge is additive, preserves history
- Do NOT touch `.beads/beads.db` or any SQLite runtime state
- Do NOT modify `.omp/commands/init.md` — the inlined heredoc is the current source of truth for hydration logic
- Do NOT create a worktree — reconciliation happens in the current directory on the current branch
- Do NOT cherry-pick individual commits — a single merge commit is cleaner and preserves the full history of both branches
- Do NOT force-push to origin — a regular push should suffice since origin/main (94807b4) is an ancestor of the merged result

## Requirements

| # | Requirement | Priority | Acceptance Criteria |
|---|------------|----------|---------------------|
| 1 | The branch divergence must be reconciled via a merge of main into the feature branch, with all 5 content conflicts resolved | MUST | `git log --oneline --merges -1` shows a merge commit; `git diff --name-only --diff-filter=U` returns empty (no unresolved conflicts) |
| 2 | Conflict resolution must favor the feature side for all 5 files, per the investigation findings and user decision | MUST | `git diff main..HEAD -- .omp/memory/project/conventions.md` shows feature content (100 lines, 1-line UI Design pointer); `git diff main..HEAD -- .omp/memory/project/project.md` shows feature content (status=stable, close-memory-audit milestone); `git diff main..HEAD -- .omp/memory/project/tech-stack.md` shows `true #` bash blocks; `git diff main..HEAD -- .omp/skills/design-system/DESIGN.md` shows concrete Open Design content (not [FILL] placeholders); `git diff main..HEAD -- .omp/skills/design-system/SKILL.md` shows 127-line concrete version |
| 3 | Dead Python bytecode cache must be removed and prevented from recurring | MUST | `.omp/scripts/__pycache__/` directory does not exist on disk; `grep '__pycache__' .gitignore` returns a match; `git status --porcelain` shows no pycache files |
| 4 | The README.md change (npm-release row) must be committed, not left dirty | MUST | `git status --porcelain README.md` returns empty (clean); the change is in a commit |
| 5 | The reconciled branch must be pushed to origin/main | MUST | `git status --short --branch` shows "up to date with 'origin/main'" with no ahead/behind indicator |
| 6 | All bead sync state (.br_history, issues.jsonl) must be flushed and committed | SHOULD | `br sync --flush-only` exits 0; `git status --porcelain .beads/` shows no untracked bead state files after commit |
| 7 | The merge commit message must be descriptive, naming both branches and the conflict resolution strategy | SHOULD | `git log -1 --format='%s'` references both main and feature branch or uses a clear merge message like `Merge main into feat/br-omp-backbone-skill-1da-fix-convention-consistency — resolve 5 conflicts favoring feature side` |

## Technical Context

### Branch Topology

The repository has diverged into two branches from a common merge-base:

```
          b32e245 (merge-base)
         /         \
       /             \
  main (665479d)    feature/...1da (b95d2c8)
  | 665479d: s2s    | 5253d81: vui migration
  | 94807b4: 1da    | 7f78661: vui review fix
  | close           | 04281b5: vui evidence
  |                 | f4816fa: vui close
  |                 | 3ee0269: Update issues
  |                 | 3d4a54e: m6y PRD+plan
  |                 | 60ef1dd: m6y cleanup
  |                 | 4d60a0e: m6y review
  |                 | 194c79a: m6y close
  |                 | a5d47d4: close-memory-audit PRD
  |                 | 8f73a9c: close-memory-audit close
  |                 | 5d7f242: /close memory audit phase
  |                 | acdcedb: fi9 PRD
  |                 | b95d2c8: fi9 plan
```

- **Merge-base:** `b32e245` (feat: fix 11 audit-discovered inconsistencies — br-omp-backbone-skill-1da)
- **main:** 2 commits ahead of merge-base (665479d s2s, 94807b4 1da close)
- **feature:** 15 commits ahead of merge-base (vui, m6y, close-memory-audit, fi9 PRD+plan)
- **origin/main:** at 94807b4 (1 commit behind local main — the s2s commit 665479d was never pushed)
- **Divergence:** both branches modified the same 5 files independently

### Conflict Analysis — 5 Files

A dry-run merge (`git merge --no-commit --no-ff main`) produced exactly 5 content conflicts. Each file was modified on both branches with different intent:

#### File 1: `.omp/memory/project/conventions.md`

**Main side (s2s, commit 665479d):** Added full UI Design section content — Design System pointer, Animation Philosophy (easing, durations, accordion, scale floor, mount strategy, micro-feedback), CSS Ownership boundary statement, Component Variants (buttons, focus rings), Craft Rules reference, Theme (light default, dark mode), Icons (library, aria-label, emoji prohibition, sizing, decorative). Total: 138 lines.

**Feature side (m6y, commit 60ef1dd):** Trimmed the entire UI Design section to a single 1-line pointer: `For UI design rules (animation, components, icons, theme, craft), load design-system/SKILL.md. The design system is on-demand — not inlined in every session.` Total: 100 lines.

**Resolution: FEATURE SIDE.** The m6y bead (br-omp-backbone-skill-m6y) explicitly trimmed conventions.md to reduce always-loaded context. The s2s bead added content that m6y later removed. The feature side represents the latest intent — conventions.md should be lean, with UI design rules loaded on-demand via the design-system skill, not inlined in an always-loaded context file.

**Before (merge-base b32e245):** conventions.md had empty UI Design headers (the original state before either bead touched it).

**After (feature side):** conventions.md has a 1-line UI Design pointer to the design-system skill. The full UI Design content (animation, components, theme, icons) lives in the design-system SKILL.md and DESIGN.md, loaded on-demand.

#### File 2: `.omp/memory/project/project.md`

**Main side (s2s, commit 665479d):** Status=`active`, Milestone=`Design asset audit and memory file cleanup (br-omp-backbone-skill-s2s)`, Next=`Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle`. Added Success Criterion #4 (zero broken file references). Has `--exclude=project.md` missing from grep in criterion #1.

**Feature side (m6y + close-memory-audit, commits 60ef1dd + 8f73a9c):** Status=`stable`, Milestone=`Memory audit phase integrated into /close (br-omp-backbone-skill-close-memory-audit-tkt)`, Next=`Brainstorm new beads — memory maintenance cycle complete`. Added `--exclude=project.md` to grep in criterion #1 (fixes self-matching grep bug). Does NOT have Success Criterion #4 (m6y did not add it; it was only on main's s2s).

**Resolution: FEATURE SIDE.** The close-memory-audit bead is the latest milestone in the project timeline. The feature side also fixes a grep self-matching bug (`--exclude=project.md`) that the main side doesn't have. However, Success Criterion #4 (zero broken file references) from s2s is valuable and should be preserved — it should be manually added to the feature-side version during conflict resolution.

**Conflict resolution detail:** Take the feature-side project.md as the base, then manually add Success Criterion #4 from the main side: `4. **Zero broken file references in memory files** — \`grep -oP '\.omp/[\w/.-]+\.\w+' .omp/memory/project/*.md | while read f; do test -f "$f" || echo "$f"; done\` returns no output`

#### File 3: `.omp/memory/project/tech-stack.md`

**Main side (s2s, commit 665479d):** Removed Design Assets and Craft References tables (correct — they were stale references to `.omp/design/` which no longer exists). But left `N/A` placeholders in bash verification blocks, which are invalid shell — `N/A` is not a valid command.

**Feature side (m6y, commit 60ef1dd):** Also removed Design Assets and Craft References tables (same change as main — both beads independently identified the same stale references). But replaced `N/A` bash placeholders with `true  # <description>` — valid shell that passes verification. Also added a trailing newline.

**Resolution: FEATURE SIDE.** The feature side has the same structural changes (removed stale design tables) plus valid bash blocks. The `true #` replacements are correct — `true` is a valid shell command that always exits 0, and the comment explains why. Main's `N/A` placeholders would fail `/verify` if any agent tried to run them as bash.

#### File 4: `.omp/skills/design-system/DESIGN.md`

**Main side (s2s, commit 665479d):** Created DESIGN.md as a [FILL] template — 183 lines, 9 sections (Brand Identity, Color Palette, Typography, Spacing & Layout, Component Tokens, Animation, Iconography, Imagery, Theme), every value cell contains `[FILL]` with HTML comment examples showing realistic downstream values. 95 total [FILL] placeholders. Attribution: Apache 2.0 + refero_skill.

**Feature side (vui, commits 5253d81 + 7f78661):** DESIGN.md has concrete Open Design content — 102 lines, actual color values, typography specs, spacing tokens, animation rules, icon guidelines. No [FILL] placeholders. Attribution: Apache 2.0 + Open Design. This is real, usable design guidance adapted from the Open Design project.

**Resolution: FEATURE SIDE (per user decision).** The user decided the template should ship concrete Open Design content, not [FILL] placeholders. The feature-side DESIGN.md provides actual, usable design guidance that downstream projects can customize, rather than a blank template they must fill from scratch.

#### File 5: `.omp/skills/design-system/SKILL.md`

**Main side (s2s, commit 665479d):** Created SKILL.md as a 95-line template-oriented skill — Purpose section explaining the brand contract template concept, When to Use (6 triggers), When NOT to Use (6 anti-patterns), Decision tree covering routing cases, Process section with 5 steps, Defaults table covering all 9 DESIGN.md sections with concrete fallbacks, Attribution, Related Skills.

**Feature side (vui, commits 5253d81 + 7f78661):** SKILL.md is a 127-line concrete version — Brand contract for generating UI, When to Use (6 triggers focused on real UI generation), When NOT to Use (3 anti-patterns), Process with detailed steps referencing actual tokens and rules, CSS ownership rules, component variants, theme, icons, craft rules. Attribution: Apache 2.0 + Open Design.

**Resolution: FEATURE SIDE (per user decision).** The user decided the feature-side concrete version should win. This version provides actual design rules and guidance, not template placeholders.

### Additional Untracked/Modified Files

**Key files:**
- `.omp/scripts/__pycache__/hydrate-memory.cpython-311.pyc` — DELETE (20.8KB, dead bytecode, source absent)
- `.gitignore` — EDIT (add `__pycache__/` and `*.pyc` entries)
- `README.md` — EDIT (already modified +2/-1, stages existing change: adds `/npm-release` row to command table; changes "Nine slash commands" → "Ten slash commands plus npm releases")

**Already committed in PRD commit (acdcedb):**
- `.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md` — the s2s bead's review report, committed under `docs:` prefix rather than `close:` prefix. Acceptable — file is tracked, state mismatch resolved.
- 6 `.beads/.br_history/*.jsonl` files from s2s session — committed in the same PRD commit.

### APIs / systems touched

- `br` CLI — `br sync --flush-only` to flush any pending bead state to JSONL before committing
- `git` — merge with conflict resolution, staging, committing, pushing; conventional commit format per conventions.md
- OMP context-file discovery — `.omp/RULES.md` is a sticky rule (always-apply), loaded by the native discovery provider; deleting it would break agent context injection. This is explicitly out of scope.

### Existing code to NOT modify

- `.omp/RULES.md` — harness-loaded sticky rule, always-apply, NOT a duplicate of AGENTS.md. See Out of Scope.
- `.omp/commands/init.md` — contains the inlined 551-line Python heredoc for memory hydration; the standalone `.omp/scripts/hydrate-memory.py` was deleted but its `.pyc` leaked. Do not touch init.md.
- `.omp/commands/npm-release.md` — untracked new command (100 lines), grounds the npm release workflow. Grounding it (package.json, .github/workflows/) is a separate bead.
- `.omp/commands/close.md` — the Phase 4 sync/commit logic is correct; the s2s close simply didn't complete Phase 4. No code change needed.
- All closed bead artifact directories under `.beads/artifacts/` — do not modify existing prd.md, plan.md, completion-evidence.json, etc.

## Approach

This is a branch reconciliation task with conflict resolution. The approach is a strict sequence of git operations: merge, resolve conflicts, clean dead files, commit, push.

### Step 1 — Flush bead state

Run `br sync --flush-only` to ensure any pending bead state is written to `.beads/issues.jsonl` and `.br_history/`. This is the precondition for a clean merge per RULE #4.

### Step 2 — Initiate merge

Run `git merge main` on the feature branch. This will produce 5 content conflicts (confirmed via dry-run). The merge will stop with conflict markers in the 5 files.

### Step 3 — Resolve conflicts per file

For each of the 5 conflicting files, resolve by favoring the feature side (our side, since we're merging main INTO feature):

- **conventions.md:** `git checkout --ours .omp/memory/project/conventions.md` — take the feature-side trimmed version (1-line pointer to design-system skill)
- **project.md:** `git checkout --ours .omp/memory/project/project.md` — take the feature-side version (stable status, close-memory-audit milestone). Then manually edit to add Success Criterion #4 from main: `4. **Zero broken file references in memory files** — \`grep -oP '\.omp/[\w/.-]+\.\w+' .omp/memory/project/*.md | while read f; do test -f "$f" || echo "$f"; done\` returns no output`
- **tech-stack.md:** `git checkout --ours .omp/memory/project/tech-stack.md` — take the feature-side version (valid `true #` bash blocks)
- **DESIGN.md:** `git checkout --ours .omp/skills/design-system/DESIGN.md` — take the feature-side concrete Open Design content
- **SKILL.md:** `git checkout --ours .omp/skills/design-system/SKILL.md` — take the feature-side concrete version

After resolving, run `git add` on all 5 files to mark conflicts as resolved.

### Step 4 — Delete dead bytecode

Remove the `.omp/scripts/__pycache__/` directory. The source script `hydrate-memory.py` no longer exists (confirmed via `find . -name 'hydrate-memory.py'` returning empty). The `/init` command inlined the hydration logic as a Python heredoc directly in `.omp/commands/init.md` (confirmed: the heredoc spans lines 36-456, with `python3 - <<'PY'` invocation). The `.pyc` is a compilation artifact from a prior run of the standalone script, left behind when the script was deleted. After deletion, the `.omp/scripts/` directory will be empty and can also be removed.

### Step 5 — Update .gitignore

Add `__pycache__/` and `*.pyc` to `.gitignore` to prevent any future Python bytecode from leaking into the tree. Place it in a new "Python bytecode" section after the existing "Beads runtime state" block. This follows the existing pattern where runtime/generated artifacts are gitignored (`.bv/`, `.beads/beads.db`, `.env`, `.worktree/`).

### Step 6 — Commit README.md and .gitignore changes

Stage and commit the README.md change (existing +2/-1 modification adding the npm-release row to the command table) and the .gitignore edit (adding `__pycache__/`). Use a `chore:` commit prefix for both.

### Step 7 — Complete the merge commit

After all conflicts are resolved and additional changes are staged, complete the merge commit. The merge commit message should be descriptive: `Merge main into feat/br-omp-backbone-skill-1da-fix-convention-consistency — resolve 5 conflicts favoring feature side (vui/m6y/close-memory-audit work supersedes s2s content)`.

### Step 8 — Sync and push

Run `br sync --flush-only` one final time. Then update local main to point to the merged result: `git switch main && git reset --hard feat/br-omp-backbone-skill-1da-fix-convention-consistency`. Then push: `git push origin main`. This pushes all commits (the pre-existing unpushed s2s commit, the merge commit, and all hygiene commits) to origin/main. Since origin/main (94807b4) is an ancestor of the merged result, a regular (non-force) push should work.

The sequence is ordered: flush → merge → resolve conflicts → delete pycache → edit gitignore → commit README+gitignore → complete merge commit → flush → reset main → push. Each step is independently verifiable. The riskiest step is the conflict resolution — if any conflict marker is left in a file, the merge is incomplete. Verification gates after each step catch this.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Merge conflict resolution leaves conflict markers in files | Medium | High | After resolving each file, run `grep -n '<<<<<<<\|=======\|>>>>>>>' <file>` to confirm no markers remain. Before completing the merge, run the same check across all 5 files. |
| `git checkout --ours` takes the wrong side (feature vs main) | Low | High | We are ON the feature branch, merging main INTO feature. `--ours` = feature (HEAD), `--theirs` = main (the branch being merged in). This is correct — we want the feature side. Verify by checking file content after checkout. |
| Pushing to origin/main is rejected (force-push required) | Low | Medium | origin/main (94807b4) is an ancestor of the merged result — all commits in origin/main are in the merged history. A regular push should work. If rejected, investigate with `git push --dry-run origin main` first. |
| Success Criterion #4 is lost when taking feature-side project.md | Medium | Low | Explicitly add Success Criterion #4 to the feature-side project.md during conflict resolution (Step 3, project.md sub-step). The criterion text is documented in Technical Context. |
| Deleting `.omp/scripts/` breaks a reference to the deleted script | Low | Low | Verified: `grep -rn 'scripts\|hydrate' .omp/commands/init.md` shows init.md uses an inline heredoc, not an external script reference. No other file references `.omp/scripts/`. |
| Committing `.br_history` files that should remain local-only | Low | Medium | Verified: `.br_history/*.jsonl` files ARE tracked in git (confirmed via `git ls-files .beads/.br_history/` returning 72 tracked files). The untracked files follow the same pattern and belong in the repo. |
| Accidentally deleting `.omp/RULES.md` | Low | High | Explicitly out of scope. RULES.md is a harness-loaded sticky rule. The PRD and plan must not touch it. Verified via OMP context-files documentation. |
| The merge brings in main's version of files we don't want | Low | Medium | The dry-run merge showed only 5 conflicts. All other files from main (s2s artifacts: brainstorm-notes.md, completion-evidence.json, plan.md, prd.md) are additive — they don't conflict with feature-side content and are welcome additions (they complete the s2s bead's artifact set). |

## Acceptance Criteria

- [ ] Merge completed with all conflicts resolved
    - Verify: `git log --oneline --merges -1` shows a merge commit
    - Verify: `git diff --name-only --diff-filter=U` returns empty
    - Verify: `grep -rn '<<<<<<<\|=======\|>>>>>>>' .omp/memory/project/ .omp/skills/design-system/` returns no matches
- [ ] conventions.md has feature-side content (1-line UI Design pointer)
    - Verify: `grep -c 'load.*design-system/SKILL.md' .omp/memory/project/conventions.md` returns ≥1
    - Verify: `wc -l .omp/memory/project/conventions.md` returns ~100 lines
- [ ] project.md has feature-side content + Success Criterion #4
    - Verify: `grep 'stable' .omp/memory/project/project.md` returns a match
    - Verify: `grep 'close-memory-audit' .omp/memory/project/project.md` returns a match
    - Verify: `grep 'Zero broken file references' .omp/memory/project/project.md` returns a match
- [ ] tech-stack.md has valid bash blocks
    - Verify: `grep -c 'true  #' .omp/memory/project/tech-stack.md` returns ≥5
    - Verify: `grep -c 'N/A' .omp/memory/project/tech-stack.md` returns 0
- [ ] DESIGN.md has concrete content (not [FILL] placeholders)
    - Verify: `grep -c '\[FILL\]' .omp/skills/design-system/DESIGN.md` returns 0
- [ ] SKILL.md has feature-side content (127 lines)
    - Verify: `wc -l .omp/skills/design-system/SKILL.md` returns ~127 lines
- [ ] Dead pycache deleted
    - Verify: `test ! -d .omp/scripts/__pycache__ && echo "PASS" || echo "FAIL"`
- [ ] `__pycache__/` gitignored
    - Verify: `grep '__pycache__' .gitignore` returns a match
- [ ] README.md is clean (committed)
    - Verify: `git status --porcelain README.md` returns empty
- [ ] main is up to date with origin
    - Verify: `git status --short --branch` shows no ahead/behind indicator
- [ ] Bead sync state flushed
    - Verify: `br sync --flush-only` exits 0 with no pending changes
- [ ] RULES.md untouched
    - Verify: `test -f .omp/RULES.md && echo "PASS" || echo "FAIL"` returns PASS
    - Verify: `git diff .omp/RULES.md` is empty
- [ ] init.md untouched
    - Verify: `git diff .omp/commands/init.md` is empty
