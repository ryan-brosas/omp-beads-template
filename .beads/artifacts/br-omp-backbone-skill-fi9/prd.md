<!-- DENSITY: Minimum 600 lines. No upper bound — be thorough. <600 = incomplete (missing sections, hand-wavy, no real technical context). This is an AI handoff: another agent must be able to pick this up and implement correctly without guessing. Every section must have concrete evidence: file paths, API signatures, existing patterns, constraints. -->
# PRD: Reconcile repo state — commit s2s closeout artifacts, excise dead pycache, push unpushed work

**Bead:** br-omp-backbone-skill-fi9 | **Type:** chore | **Priority:** P2
**Created:** 2026-06-17 | **Estimate:** 30

## Problem

WHEN the `br-omp-backbone-skill-s2s` bead was closed via `br close` in the beads database (status=closed, closed_at=2026-06-17T17:53:59Z) THEN the close command's Phase 4 git commit step was never executed, leaving the bead's `review-report.md` and 6 `.br_history/*.jsonl` files untracked in the working tree BECAUSE the `/close` command's `git add .beads/ && git commit` step was skipped or interrupted before completion, creating a state integrity mismatch where the bead is closed in DB but its closeout artifacts are not committed in git.

This affects every future agent that opens the repository. A bead marked `closed` in `br` should have a corresponding `close:` commit in git history — that is the invariant the `/close` command's Phase 4 is designed to enforce. The mismatch means the bead graph and the git history disagree, which breaks the "inspect-before-mutate" trust model: an agent running `br show` sees a closed bead, but `git log -- .beads/artifacts/br-omp-backbone-skill-s2s/` shows only the original `feat:` commit (665479d), with no closeout. Additionally, the working tree carries accumulated drift: a stale Python bytecode cache from a deleted script, and an unpushed commit on `main`. If we don't fix this now, the drift compounds — the next bead session inherits a dirty tree and the s2s closeout gap becomes harder to attribute.

## Scope

### In Scope
- Commit `.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md` with a proper `close:` commit message, reconciling the bead/git state mismatch
- Commit the 6 untracked `.beads/.br_history/*.jsonl` files from the s2s session (3 pairs: issues.20260617_174018_*, issues.20260617_174020_*, issues.20260617_175359_*) as part of the same bead-sync closeout commit, OR confirm they are already tracked and only need staging
- Delete `.omp/scripts/__pycache__/hydrate-memory.cpython-311.pyc` — dead bytecode, source script deleted, logic inlined into `.omp/commands/init.md` heredoc
- Add `__pycache__/` to `.gitignore` to prevent future bytecode leaks
- Push `main` to `origin/main` — currently ahead by 1 unpushed commit (5d7f242: feat: add memory audit phase to /close command)
- Commit the uncommitted `README.md` change (adds `/npm-release` row to command table) — this belongs with the npm-release command work and should be committed alongside the closeout

### Out of Scope
- **Do NOT delete `.omp/RULES.md`** — it is a harness-loaded sticky rule (always-apply), injected into every agent's system prompt `<generic-rules>` block. Verified via OMP docs (`omp://context-files.md`): `.omp/RULES.md` is loaded as an always-apply rule at the native project location. Deleting it would strip the 6 workflow rules from every session. It is NOT a duplicate of AGENTS.md — AGENTS.md's Guardrails section is different, softer content.
- Do NOT modify the `npm-release.md` command itself — grounding it (package.json, workflow, trusted publishing) is a separate bead, a design decision
- Do NOT modify any closed bead's existing artifacts (prd.md, plan.md, etc.) — only commit the missing s2s review-report.md
- Do NOT rebase or rewrite any existing commits
- Do NOT touch `.beads/beads.db` or any SQLite runtime state
- Do NOT modify `.omp/commands/init.md` — the inlined heredoc is the current source of truth for hydration logic
- Do NOT create a worktree — this is a mechanical hygiene task in the current directory

## Requirements

| # | Requirement | Priority | Acceptance Criteria |
|---|------------|----------|---------------------|
| 1 | The s2s bead's closeout artifacts must be committed to git, reconciling the bead-is-closed-in-DB-but-uncommitted-in-git mismatch | MUST | `git log --oneline -- '.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md'` returns a commit with `close:` prefix; `git status --porcelain` shows no untracked s2s files |
| 2 | Dead Python bytecode cache must be removed and prevented from recurring | MUST | `.omp/scripts/__pycache/` directory does not exist on disk; `grep '__pycache__' .gitignore` returns a match; `git status --porcelain` shows no pycache files |
| 3 | The unpushed commit on main must be pushed to origin | MUST | `git status --short --branch` shows "up to date with 'origin/main'" with no ahead/behind indicator |
| 4 | The README.md change (npm-release row) must be committed, not left dirty | MUST | `git status --porcelain README.md` returns empty (clean); the change is in a commit |
| 5 | The closeout commit(s) must follow the repo's conventional commit style | SHOULD | Commit message matches pattern `close: br-omp-backbone-skill-s2s` or `chore:` for the hygiene items, per the conventions.md Git section |
| 6 | All bead sync state (.br_history, issues.jsonl) must be flushed and committed | SHOULD | `br sync --flush-only` exits 0; `git status --porcelain .beads/` shows no untracked bead state files after commit |

## Technical Context

**Key files:**
- `.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md` — NEW (commit to git, 333 lines, already exists on disk untracked) — the s2s bead's review report that was written during `/review` but never committed during `/close`
- `.beads/.br_history/issues.20260617_174018_122102993.jsonl` + `.meta.json` — NEW (commit) — br history snapshot from s2s session
- `.beads/.br_history/issues.20260617_174020_885765031.jsonl` + `.meta.json` — NEW (commit) — br history snapshot from s2s session
- `.beads/.br_history/issues.20260617_175359_699847635.jsonl` + `.meta.json` — NEW (commit) — br history snapshot from s2s session
- `.omp/scripts/__pycache__/hydrate-memory.cpython-311.pyc` — DELETE (20.8KB, dead bytecode, source absent)
- `.gitignore` — EDIT (add `__pycache__/` entry, ~5 lines context)
- `README.md` — EDIT (already modified, +2/-1, stages the existing change: adds `/npm-release` row to command table)

**APIs / systems touched:**
- `br` CLI — `br sync --flush-only` to flush any pending bead state to JSONL before committing
- `git` — staging, committing, pushing; conventional commit format per conventions.md
- OMP context-file discovery — `.omp/RULES.md` is a sticky rule (always-apply), loaded by the native discovery provider; deleting it would break agent context injection. This is explicitly out of scope.

**Existing code to NOT modify:**
- `.omp/RULES.md` — harness-loaded sticky rule, always-apply, NOT a duplicate of AGENTS.md. See Out of Scope.
- `.omp/commands/init.md` — contains the inlined 551-line Python heredoc for memory hydration; the standalone `.omp/scripts/hydrate-memory.py` was deleted but its `.pyc` leaked. Do not touch init.md.
- `.omp/commands/npm-release.md` — untracked new command (100 lines), grounds the npm release workflow. Grounding it (package.json, .github/workflows/) is a separate bead.
- `.omp/commands/close.md` — the Phase 4 sync/commit logic is correct; the s2s close simply didn't complete Phase 4. No code change needed.
- All closed bead artifact directories under `.beads/artifacts/` — do not modify existing prd.md, plan.md, completion-evidence.json, etc. Only commit the missing s2s review-report.md.

## Approach

This is a mechanical reconciliation task with no architectural decisions. The approach is a strict sequence of git operations and one file deletion, following the `/close` command's Phase 4-5 pattern that was skipped for s2s.

**Step 1 — Flush bead state.** Run `br sync --flush-only` to ensure any pending bead state is written to `.beads/issues.jsonl` and `.br_history/`. This is the precondition for a clean commit per RULE #4.

**Step 2 — Delete dead bytecode.** Remove the `.omp/scripts/__pycache__/` directory. The source script `hydrate-memory.py` no longer exists (confirmed via `find . -name 'hydrate-memory.py'` returning empty). The `/init` command inlined the hydration logic as a Python heredoc directly in `.omp/commands/init.md` (confirmed: the heredoc spans lines 36-456, with `python3 - <<'PY'` invocation). The `.pyc` is a compilation artifact from a prior run of the standalone script, left behind when the script was deleted. After deletion, the `.omp/scripts/` directory will be empty and can also be removed.

**Step 3 — Update .gitignore.** Add `__pycache__/` to `.gitignore` to prevent any future Python bytecode from leaking into the tree. Place it in the appropriate section (after the existing `.beads/` runtime state entries, under a new "Python bytecode" comment). This follows the existing pattern where runtime/generated artifacts are gitignored (`.bv/`, `.beads/beads.db`, `.env`, `.worktree/`).

**Step 4 — Commit README.md change.** The existing uncommitted `README.md` change (adds `/npm-release` to the command table: "Nine slash commands" → "Ten slash commands plus npm releases") belongs with the npm-release command work. Since the npm-release command itself is untracked and will be committed in a separate bead, stage and commit README.md as part of this hygiene pass — it's already modified and leaving it dirty compounds drift. Use a `docs:` commit prefix.

**Step 5 — Commit s2s closeout artifacts.** Stage and commit `.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md` and the 6 `.br_history/*.jsonl` files. Use the `close:` commit prefix matching the pattern in git history (e.g., `8f73a9c close: br-omp-backbone-skill-close-memory-audit-tkt`, `f4816fa close: br-omp-backbone-skill-vui`). Commit message: `close: br-omp-backbone-skill-s2s`. This reconciles the bead/git state: the bead is closed in DB, now the closeout is committed in git.

**Step 6 — Sync and push.** Run `br sync --flush-only` one final time, then `git push origin main`. This pushes both the pre-existing unpushed commit (5d7f242) and the new hygiene commits. Verify `git status` shows "up to date with 'origin/main'".

The sequence is ordered: flush → delete → gitignore → commit README → commit closeout → flush → push. Each step is independently verifiable. The riskiest step is the push, but it only pushes commits that are already locally verified.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Pushing to origin/main triggers unexpected CI or hooks | Low | Medium | This repo has no `.github/workflows/` directory (confirmed), so no CI runs. Push is safe. |
| Deleting `.omp/scripts/` breaks a reference to the deleted script | Low | Low | Verified: `grep -rn 'scripts\|hydrate' .omp/commands/init.md` shows init.md uses an inline heredoc, not an external script reference. No other file references `.omp/scripts/`. |
| Committing `.br_history` files that should remain local-only | Low | Medium | Verified: `.br_history/*.jsonl` files ARE tracked in git (confirmed via `git ls-files .beads/.br_history/` returning 72 tracked files). The 6 untracked files follow the same pattern and belong in the repo. |
| README.md commit references npm-release command that is untracked | Medium | Low | The README change is a 1-row table addition that is already modified and uncommitted. Committing it resolves drift; the npm-release command grounding is a separate bead. The README accurately describes the command's existence. |
| Accidentally deleting `.omp/RULES.md` | Low | High | Explicitly out of scope. RULES.md is a harness-loaded sticky rule. The PRD and plan must not touch it. Verified via OMP context-files documentation. |

## Acceptance Criteria

- [ ] s2s closeout artifacts committed to git
    - Verify: `git log --oneline -- '.beads/artifacts/br-omp-backbone-skill-s2s/review-report.md'` returns a `close:` commit
- [ ] No untracked s2s files remain
    - Verify: `git status --porcelain | grep s2s` returns empty
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
