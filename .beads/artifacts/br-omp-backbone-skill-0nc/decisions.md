# Decisions: br-omp-backbone-skill-0nc

## Decision Log

| # | Decision | Rationale | Confidence |
|---|----------|-----------|------------|
| 1 | Use root AGENTS.md as a generic agents.md-compatible file | The current root stub is not enough for non-OMP agents; agents.md guidance says root AGENTS.md should hold setup, testing, style, and extra instructions. | High |
| 2 | Extend `.omp/commands/init.md` Phase 2.5 instead of adding a script | Existing hydration already detects project metadata and updates template files idempotently; project conventions say commands + skills only, no scripts. | High |
| 3 | Document `/npm-release` in README rather than removing it | The command file exists and user named README command inventory; removing shipped functionality is scope creep. | High |
| 4 | Stop ignoring `.beads/issues.jsonl` while keeping runtime DB ignores | br sync exports JSONL for git; SQLite/WAL/lock/touch files are runtime state. | High |
| 5 | Limit this session to /create artifacts | User explicitly requested only /create and forbade /plan, /ship, /verify, /review, /pr, and /close. | High |

## Rejected Alternatives

| # | Alternative | Why Rejected | Risk if Re-introduced |
|---|-------------|--------------|----------------------|
| 1 | Keep root AGENTS.md as only `See @.omp/AGENTS.md` | It remains OMP-specific and weak for generic agents that consume agents.md. | Fresh projects still give generic agents no setup/test/style contract. |
| 2 | Create `.omp/scripts/hydrate-agents.py` | The template intentionally avoids scripts; the inline init helper already owns hydration. | Adds hidden machinery and another maintenance surface. |
| 3 | Copy all `.omp/AGENTS.md` content into root AGENTS.md | Root file should be concise generic agent guidance; `.omp/AGENTS.md` is dense OMP harness context. | Bloating root instructions makes them harder for generic agents to follow and easier to stale. |
| 4 | Ignore README mismatch because `/npm-release` is not lifecycle | The README says command count, and the command exists. It needs classification, not silence. | Humans and agents keep seeing conflicting command inventories. |
| 5 | Leave `.beads/issues.jsonl` ignored | This contradicts br sync workflow and prevents bead state from becoming versioned handoff state. | Future commits omit issue updates even after `br sync --flush-only`. |

## Assumptions

| # | Assumption | Validation | Invalidation Impact |
|---|------------|------------|---------------------|
| 1 | Root AGENTS.md is intended for generic agents, while `.omp/AGENTS.md` remains OMP-specific. | Current root file points to `.omp/AGENTS.md`; agents.md docs describe root AGENTS.md as a README for agents. | If root should remain OMP-only, R1/R2 need redesign and README-only/gitignore work should split out. |
| 2 | `npm-release.md` is intentionally shipped. | `.omp/commands/` listing shows `npm-release.md`; prior git history includes a commit adding npm-release to README. | If the command is accidental, README should not document it and a separate removal bead is needed. |
| 3 | `.beads/issues.jsonl` should be committed. | br skill and project conventions require `br sync --flush-only` then `git add .beads/`; sync exports JSONL. | If the repository chooses DB-only tracking, br workflow docs and commit policy need broader changes. |
| 4 | Inline Python remains acceptable inside command Markdown. | Existing `/init` Phase 2.5 uses inline Python for memory hydration. | If inline Python is banned later, all hydration needs redesign, not just AGENTS.md. |
| 5 | No matching open/in-progress bead already owns this work. | `br search` for the full description and related keywords returned empty arrays; bv reported zero open/in-progress beads. | If a hidden duplicate exists, merge or close one bead before planning. |
