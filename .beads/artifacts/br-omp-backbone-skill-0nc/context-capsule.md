# Context Capsule: br-omp-backbone-skill-0nc

## Objective

Build the implementation for the OMP Beads Template hygiene bead: root `AGENTS.md` becomes a useful agents.md-compatible contract, `/init` Phase 2.5 hydrates that root file from existing detected metadata without clobbering user edits, README command inventory matches the ten shipped command files, and `.gitignore` keeps local runtime files ignored while allowing versioned bead sync JSONL.

## Key Patterns

- **Exact replacement hydration** — The current `/init` helper uses `replace_exact` and `write_text_if_changed`; extend that instead of fuzzy rewriting user prose. Reference: `.omp/commands/init.md:54-69 and .omp/commands/init.md:373-448` for safe idempotent hydration.
- **Detected metadata reuse** — The Phase 2.5 block already computes project name, package manager, language, runtime, and verification commands. Reference: `.omp/commands/init.md:179-371` for values to feed root AGENTS.md generation.
- **Root stub shape** — The current root file is only a heading and `.omp/AGENTS.md` pointer. Reference: `AGENTS.md:1-3` for known stub replacement target.
- **README inventory table** — The README workflow table is the human-visible command inventory. Reference: `README.md:37-49` for where `/npm-release` must be classified.
- **Runtime versus sync state** — `.beads/issues.jsonl` is br sync output; SQLite/WAL/lock/touch files are local runtime state. Reference: `.gitignore:4-10` for ignore rule split.
- **Command inventory source** — Actual shipped commands are `.omp/commands/*.md`, not README prose. Reference: `.omp/commands/` for inventory verification.
- **Workflow boundaries** — This bead excludes `.omp/AGENTS.md`, extensions, memory files, design assets, and command renames. Reference: `.beads/artifacts/br-omp-backbone-skill-0nc/prd.md:46-59` for scope enforcement.

## Constraints

1. MUST edit only `AGENTS.md`, `.omp/commands/init.md`, `README.md`, and `.gitignore` unless direct verification proves another file controls this bead.
2. MUST keep root `AGENTS.md` useful to generic agents that do not resolve OMP `@` imports.
3. MUST preserve a pointer from root `AGENTS.md` to `.omp/AGENTS.md` for OMP-specific bead workflow.
4. MUST implement root AGENTS hydration inside `/init` Phase 2.5; no standalone scripts.
5. MUST make `/init` idempotent for root `AGENTS.md`.
6. MUST not overwrite arbitrary user-maintained root `AGENTS.md` prose.
7. MUST not ignore `.beads/issues.jsonl`.
8. MUST keep `.beads/beads.db`, `.beads/beads.db-shm`, `.beads/beads.db-wal`, `.beads/.write.lock`, and `.beads/last-touched` ignored.
9. MUST add `__pycache__/` and `*.pyc` ignores.
10. MUST document `/npm-release` if `npm-release.md` remains shipped.
11. MUST not remove `/npm-release` to simplify README wording.
12. MUST not touch `.omp/AGENTS.md`.
13. MUST not touch `.omp/extensions/*`.
14. MUST not touch `design/` or `DESIGN.md`.
15. MUST not edit `.omp/memory/project/*` for this bead.
16. MUST not run `/verify`, `/review`, `/pr`, or `/close` during this `/plan`-only phase.
17. SHOULD use exact command/file evidence in every verification claim.
18. SHOULD keep generated root instructions concise and non-duplicative.
19. SHOULD classify `/npm-release` as release support, not a core lifecycle phase.
20. SHOULD run scratch hydration twice and prove byte-identical second run.

## File Ownership

| Task | Allowed | Forbidden |
|------|---------|-----------|
| 1.1 Re-read target contracts | `AGENTS.md`, `.omp/commands/init.md`, `README.md`, `.gitignore`, `.omp/commands/*.md` | No edits during grounding |
| 2.1 Replace root AGENTS.md stub | `AGENTS.md` | All other files |
| 2.2 Correct README command inventory | `README.md` | All other files |
| 2.3 Fix beads and Python ignore rules | `.gitignore` | All other files |
| 3.1 Extend init root AGENTS hydration | `.omp/commands/init.md` | `.omp/scripts/*`, `.omp/extensions/*`, `.omp/memory/project/*`, all other command files |
| 4.1 Run scoped verification gates | No source edits unless a gate identifies a direct defect in owned files | Workflow phase artifacts outside this bead, unrelated user changes |

## Graph Context

- **Blast radius:** 4 files (0 new, 4 edits, 0 deletes).
- **Related beads:** 0 blocking or blocked beads in dependency tree; graph has this bead as a depth-0 singleton.
- **File history:** `bv --robot-file-hotspots --format json` reports zero file links and no hotspots; PRD cites prior commits as historical motivation, not active blockers.
- **Hotspots touched:** None.
- **Execution tracks:** `bv --robot-plan --format json` returns one track, `track-A`, containing this bead.
- **Internal wave parallelism:** Wave 2 can run root AGENTS, README, and `.gitignore` edits in parallel because files are disjoint.
- **Sequential point:** `/init` hydration should follow root AGENTS shape decisions because generated content must match the intended root contract.
- **Forecast:** 52 minutes, confidence 0.5, one agent.
- **Critical path:** No downstream dependencies; still verify carefully because root AGENTS and `/init` affect future projects.

### Handoff checks for root AGENTS.md

- overview
- setup commands
- code style
- testing instructions
- OMP workflow pointer
- security note
- no OMP-only syntax dependency
- not a full copy of `.omp/AGENTS.md`

### Handoff checks for init hydration

- inside Phase 2.5
- uses existing metadata
- creates missing file
- replaces known stub
- replaces exact placeholders
- leaves user prose
- reports summary
- second run unchanged

### Handoff checks for README

- ten command files observed
- nine lifecycle commands preserved
- `/npm-release` documented
- release helper not lifecycle phase
- no stale count wording

### Handoff checks for gitignore

- runtime DB ignored
- WAL/SHM ignored
- lock/touch ignored
- issues.jsonl allowed
- Python bytecode ignored
- env ignored

