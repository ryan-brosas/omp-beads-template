# Decisions: br-omp-backbone-skill-3co

## Decision Log

| # | Decision | Rationale | Confidence |
|---|----------|-----------|------------|
| 1 | Fix `.omp/AGENTS.md` instead of command implementations. | Investigation showed `.omp/commands/npm-release.md` is tracked and README already documents it; the stale artifact is canonical OMP context. | High |
| 2 | Use tracked command files as the inventory source of truth. | `.omp/commands/verify.md` and `.omp/commands/review.md` explicitly require `git ls-files '.omp/commands/*.md'` for command inventory evidence. | High |
| 3 | Keep `/npm-release` outside the lifecycle arrow chain. | README calls it a release helper, and release publishing is not part of every bead lifecycle. | High |
| 4 | Treat README as read/verify unless post-edit comparison finds a direct conflict. | README already says nine lifecycle slash commands plus npm-release helper and includes the `/npm-release` row. | Medium |

## Rejected Alternatives

| # | Alternative | Why Rejected | Risk if Re-introduced |
|---|-------------|--------------|----------------------|
| 1 | Edit README only. | README is already aligned with tracked shipped commands; this would not fix the stale canonical context file. | Agents loading `.omp/AGENTS.md` would still miss `/npm-release`. |
| 2 | Remove `/npm-release` from README. | `.omp/commands/npm-release.md` is tracked and shipped, so hiding it would make public docs wrong. | Release helper becomes discoverable only by filesystem inspection. |
| 3 | Add `/npm-release` to the bead lifecycle arrow chain. | Release publishing is a separate helper, not a required bead phase. | Agents may attempt npm releases during ordinary close flow. |
| 4 | Generate `.omp/AGENTS.md` command inventory dynamically. | One stale Markdown table does not justify new machinery in a template that prefers commands and skills only. | More maintenance surface and a second source of truth. |

## Assumptions

| # | Assumption | Validation | Invalidation Impact |
|---|------------|------------|---------------------|
| 1 | `.omp/commands/npm-release.md` is shipped, not scratch. | `git ls-files '.omp/commands/*.md'` includes `.omp/commands/npm-release.md`; the command file has frontmatter and release procedure text. | If untracked, `.omp/AGENTS.md` should not document it as shipped. |
| 2 | README command inventory is already correct. | `README.md:10` says nine lifecycle commands plus npm-release helper, and `README.md:50` has the `/npm-release` row. | If README drifts after the `.omp/AGENTS.md` edit, `/ship` must include the minimal README correction. |
| 3 | `.omp/AGENTS.md` is the highest-priority stale context. | The project context states `.omp/AGENTS.md` is canonical and automatically loaded; observed stale rows are there. | If another always-loaded context duplicates the stale inventory, scope must expand to that exact file. |
| 4 | No behavior change is required. | The problem is a mismatch between documented inventory and tracked command files, not a failing command execution path. | If verification finds `/npm-release` command behavior broken, create a separate bead rather than expanding this one. |
