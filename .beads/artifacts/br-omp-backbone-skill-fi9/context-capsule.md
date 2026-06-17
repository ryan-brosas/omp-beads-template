# Context Capsule: br-omp-backbone-skill-fi9

## Objective

Reconcile a diverged repository state. The `feat/br-omp-backbone-skill-1da-fix-convention-consistency` branch and `main` diverged from merge-base `b32e245` 13 commits ago. Both branches independently modified the same 5 files (conventions.md, project.md, tech-stack.md, DESIGN.md, SKILL.md) with different intent. The feature branch has 15 commits of later bead work (vui, m6y, close-memory-audit, fi9 PRD+plan); main has 2 commits (s2s design-system creation, 1da close). A dry-run merge produces 5 content conflicts. This bead merges main into the feature branch, resolves all conflicts favoring the feature side (per user decision), cleans dead artifacts (pycache, gitignore), commits the README.md change, and pushes the reconciled result to origin/main.

## Key Patterns

- **Conventional commits** — The repo uses `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, and `close:` prefixes. Reference: git log (e.g., `8f73a9c close: br-omp-backbone-skill-close-memory-audit-tkt`, `60ef1dd fix: post-review cleanup`). For this bead: use `chore:` for hygiene commits, a descriptive merge commit message.
- **Bead sync before commit** — RULE #4: `br sync --flush-only` before `git add .beads/ && git commit`. Reference: `.omp/RULES.md` line 17. This ensures pending bead state is flushed to JSONL before committing.
- **Gitignore patterns** — Runtime/generated artifacts are gitignored with comment headers. Reference: `.gitignore` (`.bv/`, `.beads/beads.db`, `.env`, `.worktree/`). Follow this pattern for `__pycache__/`.
- **Sticky rules are harness-loaded** — `.omp/RULES.md` is loaded as an always-apply rule by the native OMP discovery provider, injected into the system prompt's `<generic-rules>` block. Reference: `omp://context-files.md`. Do NOT delete it — it is NOT a duplicate of AGENTS.md.
- **Inlined hydration logic** — The `/init` command's memory hydration logic lives as a Python heredoc inside `.omp/commands/init.md` (lines 36-456), not as a standalone script. The standalone `.omp/scripts/hydrate-memory.py` was deleted but its `.pyc` leaked. Reference: `.omp/commands/init.md`.
- **Merge conflict resolution with `--ours`/`--theirs`** — When merging main INTO the feature branch, `--ours` = feature (HEAD), `--theirs` = main (the branch being merged in). We want the feature side for all 5 conflicts. Reference: git merge documentation.
- **conventions.md trimming pattern** — The m6y bead (br-omp-backbone-skill-m6y) established the pattern of trimming conventions.md to reduce always-loaded context. UI Design rules live in the design-system skill (on-demand), not inlined in conventions.md. The s2s bead on main added full UI Design content that m6y later removed. Reference: commit 60ef1dd.
- **tech-stack.md bash validity pattern** — The m6y bead replaced `N/A` placeholders in bash verification blocks with `true  # <description>` — valid shell that passes `/verify`. Main's s2s left `N/A` placeholders (invalid shell). Reference: commit 60ef1dd.

## Constraints

1. MUST merge main into the feature branch (not rebase, not cherry-pick) — preserves full history of both branches
2. MUST resolve all 5 conflicts favoring the feature side (per user decision for design-system files; per investigation for memory files)
3. MUST add Success Criterion #4 to project.md (preserved from main's s2s, not present on feature side)
4. MUST delete `.omp/scripts/__pycache__/` — it is dead bytecode from a deleted script
5. MUST add `__pycache__/` and `*.pyc` to `.gitignore` to prevent future bytecode leaks
6. MUST commit the existing README.md change (npm-release row) — leaving it dirty compounds drift
7. MUST push the reconciled branch to origin/main
8. MUST NOT delete `.omp/RULES.md` — it is a harness-loaded sticky rule (always-apply), not a duplicate of AGENTS.md
9. MUST NOT modify `.omp/commands/init.md` — the inlined heredoc is the current source of truth
10. MUST NOT modify `.omp/commands/npm-release.md` — grounding it (package.json, workflow) is a separate bead
11. MUST NOT modify any closed bead's existing artifacts — only resolve conflicts in the 5 files
12. MUST NOT rebase or rewrite existing commits — merge is additive, preserves history
13. MUST NOT touch `.beads/beads.db` or any SQLite runtime state
14. MUST NOT create a worktree — reconciliation happens in the current directory on the current branch
15. MUST NOT force-push to origin — origin/main (94807b4) is an ancestor of the merged result, so a regular push should work

## File Ownership

| Task | Allowed | Forbidden |
|------|---------|-----------|
| 1.1 (flush bead state) | `.beads/issues.jsonl`, `.beads/.br_history/` (sync only — no manual edits) | All other files |
| 1.2 (delete pycache) | `.omp/scripts/__pycache__/`, `.omp/scripts/` (if empty) | All other files |
| 1.3 (edit gitignore) | `.gitignore` | All other files |
| 2.1 (initiate merge) | None (git merge only — no file changes) | All files |
| 3.1 (resolve conventions.md) | `.omp/memory/project/conventions.md` (checkout --ours + add) | All other files |
| 3.2 (resolve project.md) | `.omp/memory/project/project.md` (checkout --ours + manual edit + add) | All other files |
| 3.3 (resolve tech-stack.md) | `.omp/memory/project/tech-stack.md` (checkout --ours + add) | All other files |
| 3.4 (resolve DESIGN.md) | `.omp/skills/design-system/DESIGN.md` (checkout --ours + add) | All other files |
| 3.5 (resolve SKILL.md) | `.omp/skills/design-system/SKILL.md` (checkout --ours + add) | All other files |
| 4.1 (commit README + gitignore) | `README.md`, `.gitignore` (staging only — no content changes beyond 1.3) | All other files |
| 4.2 (complete merge commit) | None (git commit only — no file changes) | All files |
| 5.1 (sync, reset main, push) | None (git operations only — no file changes) | All files |
| 6.1 (verification) | None (read-only verification) | All files |

## Graph Context

- **Blast radius:** 8 files (5 conflict resolutions, 1 delete, 1 edit, 1 push)
  - 5 conflict files: `.omp/memory/project/conventions.md`, `.omp/memory/project/project.md`, `.omp/memory/project/tech-stack.md`, `.omp/skills/design-system/DESIGN.md`, `.omp/skills/design-system/SKILL.md`
  - 1 delete: `.omp/scripts/__pycache__/`
  - 1 edit: `.gitignore`
  - 1 edit (already modified): `README.md`
  - 1 push: `origin/main`
- **Related beads:** 4 closed beads whose work is being reconciled:
  - `br-omp-backbone-skill-s2s` (main side) — created design-system skill, updated memory files
  - `br-omp-backbone-skill-vui` (feature side) — migrated design system to .omp/skills/, synced density gates
  - `br-omp-backbone-skill-m6y` (feature side) — trimmed conventions.md, hardened success criteria, completed tree
  - `br-omp-backbone-skill-close-memory-audit-tkt` (feature side) — added memory audit phase to /close
- **File history:**
  - `.omp/memory/project/conventions.md`: 2 bead touches (s2s on main added UI Design content, m6y on feature trimmed it to 1-line pointer). Conflict: both modified the same section with opposite intent.
  - `.omp/memory/project/project.md`: 2 bead touches (s2s on main set milestone to s2s + added criterion #4, m6y+close-memory-audit on feature set milestone to close-memory-audit + added grep fix). Conflict: both updated status/milestone/criteria differently.
  - `.omp/memory/project/tech-stack.md`: 2 bead touches (s2s on main removed design tables but left N/A, m6y on feature removed design tables and made bash valid). Conflict: both removed tables but feature side has valid bash.
  - `.omp/skills/design-system/DESIGN.md`: 2 bead touches (s2s on main created [FILL] template, vui on feature created concrete content). Conflict: add/add — both branches created the file independently.
  - `.omp/skills/design-system/SKILL.md`: 2 bead touches (s2s on main created template version, vui on feature created concrete version). Conflict: add/add — both branches created the file independently.
- **Hotspots touched:** None — no file in this bead's blast radius has >3 bead history. The highest is 2 touches (all 5 conflict files).
- **Branch state:**
  - Current branch: `feat/br-omp-backbone-skill-1da-fix-convention-consistency`
  - Merge-base with main: `b32e245` (13 commits ago)
  - Feature branch: 15 commits ahead of merge-base
  - Main: 2 commits ahead of merge-base
  - origin/main: at 94807b4 (1 commit behind local main — s2s commit 665479d never pushed)
  - Divergence: both branches modified the same 5 files independently
  - After merge: feature branch contains all commits from both branches, with 5 conflicts resolved favoring feature side
  - After reset + push: main points to merged result, origin/main matches
- **Dependency edges:** None. Bead is depth 0, no parent, no children. Graph has 15 nodes, 0 edges (14 closed + this 1 open).
