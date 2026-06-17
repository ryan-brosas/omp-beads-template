# Context Capsule: br-omp-backbone-skill-fi9

## Objective

Reconcile the omp-template working tree so bead-git state is consistent, dead artifacts are removed, and main is pushed to origin. The `br-omp-backbone-skill-s2s` bead was closed in the br database (status=closed, closed_at=2026-06-17T17:53:59Z) but its closeout artifacts (review-report.md + 6 .br_history files) were never committed to git during /close Phase 4. Additionally, a dead Python bytecode cache (`.omp/scripts/__pycache__/hydrate-memory.cpython-311.pyc`) from a deleted script lingers, and an unpushed commit (5d7f242) sits on main. This bead cleans all three issues and pushes, leaving a clean baseline for the next session.

## Key Patterns

- **Conventional commits** — The repo uses `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, and `close:` prefixes. Reference: git log (e.g., `8f73a9c close: br-omp-backbone-skill-close-memory-audit-tkt`, `60ef1dd fix: post-review cleanup`). For this bead: use `close:` for s2s closeout, `chore:` for gitignore, `docs:` for README.
- **Bead sync before commit** — RULE #4: `br sync --flush-only` before `git add .beads/ && git commit`. Reference: `.omp/RULES.md` line 17. This ensures pending bead state is flushed to JSONL before committing.
- **Gitignore patterns** — Runtime/generated artifacts are gitignored with comment headers. Reference: `.gitignore` (`.bv/`, `.beads/beads.db`, `.env`, `.worktree/`). Follow this pattern for `__pycache__/`.
- **Sticky rules are harness-loaded** — `.omp/RULES.md` is loaded as an always-apply rule by the native OMP discovery provider, injected into the system prompt's `<generic-rules>` block. Reference: `omp://context-files.md`. Do NOT delete it — it is NOT a duplicate of AGENTS.md.
- **Inlined hydration logic** — The `/init` command's memory hydration logic lives as a Python heredoc inside `.omp/commands/init.md` (lines 36-456), not as a standalone script. The standalone `.omp/scripts/hydrate-memory.py` was deleted but its `.pyc` leaked. Reference: `.omp/commands/init.md`.

## Constraints

1. MUST commit the s2s review-report.md with a `close:` commit prefix to match the existing pattern for closed beads
2. MUST delete `.omp/scripts/__pycache__/` — it is dead bytecode from a deleted script
3. MUST add `__pycache__/` to `.gitignore` to prevent future bytecode leaks
4. MUST push main to origin so it is up to date
5. MUST commit the existing README.md change (npm-release row) — leaving it dirty compounds drift
6. MUST NOT delete `.omp/RULES.md` — it is a harness-loaded sticky rule (always-apply), not a duplicate of AGENTS.md
7. MUST NOT modify `.omp/commands/init.md` — the inlined heredoc is the current source of truth
8. MUST NOT modify `.omp/commands/npm-release.md` — grounding it (package.json, workflow) is a separate bead
9. MUST NOT modify any closed bead's existing artifacts — only commit the missing s2s review-report.md
10. MUST NOT rebase or rewrite existing commits — additive commits only
11. MUST NOT create a worktree — mechanical hygiene in the current directory
12. MUST NOT touch `.beads/beads.db` or any SQLite runtime state

## File Ownership

| Task | Allowed | Forbidden |
|------|---------|-----------|
| 1.1 (delete pycache) | `.omp/scripts/__pycache__/`, `.omp/scripts/` (if empty) | All other files |
| 1.2 (edit gitignore) | `.gitignore` | All other files |
| 2.1 (commit README + gitignore) | `README.md`, `.gitignore` (staging only — no content changes beyond 1.2) | All other files |
| 3.1 (flush bead state) | `.beads/issues.jsonl`, `.beads/.br_history/` (sync only — no manual edits) | All other files |
| 4.1 (push to origin) | None (git push only — no file changes) | All files |
| 5.1 (verification) | None (read-only verification) | All files |

## Graph Context

- **Blast radius:** 5 files (1 new commit-only [s2s review-report.md — already committed in PRD commit], 2 edits [.gitignore, README.md], 1 delete [.omp/scripts/__pycache__/], 1 push [origin/main])
- **Related beads:** 1 (`br-omp-backbone-skill-s2s` — the bead whose closeout we are reconciling; it is closed in DB but its review-report.md was uncommitted until the PRD commit acdcedb)
- **File history:** `.gitignore` has 0 bead history (confirmed via `bv --robot-file-beads`). `README.md` has no bead links. No hotspot contention.
- **Hotspots touched:** None — no file in this bead's blast radius has >3 bead history. The s2s artifacts directory is low-churn.
- **Branch state:** The PRD commit (acdcedb) landed on `feat/br-omp-backbone-skill-1da-fix-convention-consistency`, not `main`. The plan's Wave 4 handles merging this back to main before pushing. The feature branch contains only the PRD commit and pre-existing unpushed commits — no conflicting work.
- **Dependency edges:** None. Bead is depth 0, no parent, no children. Graph has 15 nodes, 0 edges (14 closed + this 1 open).
