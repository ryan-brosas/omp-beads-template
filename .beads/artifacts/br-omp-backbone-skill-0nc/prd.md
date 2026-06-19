<!-- DENSITY: Target 500-700 lines. Fewer than 300 lines means incomplete: missing sections, hand-wavy context, or no real technical context. This is an AI handoff: another agent must be able to pick this up and implement correctly without guessing. Every section has concrete evidence: file paths, API signatures, existing patterns, and constraints. -->
# PRD: Align root AGENTS.md, init hydration, README command inventory, and beads runtime ignores

**Bead:** br-omp-backbone-skill-0nc | **Type:** chore | **Priority:** P2
**Created:** 2026-06-19 | **Estimate:** 90 minutes

## Problem

WHEN an agent or a freshly cloned project relies on the repository root `AGENTS.md` THEN it receives only a pointer to `.omp/AGENTS.md` BECAUSE the template root file was kept as an OMP-only delegation stub instead of an agents.md-compatible instruction document.

1. Agents outside the OMP harness expect root `AGENTS.md` to be a readable Markdown contract with setup commands, testing guidance, code style, and project-specific notes.
2. The current root file is three lines: a title and `See @.omp/AGENTS.md`.
3. That pointer is useful inside OMP because the harness resolves `.omp/AGENTS.md`, but it is too sparse for generic agents that do not understand OMP imports.
4. The agents.md site describes AGENTS.md as a README for agents and lists common content: project overview, build and test commands, code style guidelines, testing instructions, security considerations, and extra instructions.
5. The `/init` command already performs repository metadata detection in Phase 2.5 for `.omp/memory/project/*`.
6. That detection includes README heading/paragraph extraction, package manager detection, language/runtime inference, and verification command inference.
7. Root AGENTS.md hydration belongs next to that existing logic so new projects start with a useful agent instruction file without adding a standalone script.
8. README.md currently says there are nine slash commands covering the lifecycle, while `.omp/commands/` currently contains ten command files including `npm-release.md`.
9. The README workflow table lists nine lifecycle commands and omits `/npm-release`.
10. The prior fi9 work added npm-release material, and this bead should make the inventory match the shipped commands rather than leaving a stale count.
11. `.gitignore` currently ignores `.beads/issues.jsonl`; that conflicts with the br workflow because `issues.jsonl` is the explicit sync artifact that should be committed after `br sync --flush-only`.
12. `.gitignore` currently ignores `.beads/beads.db`, `.beads/beads.db-shm`, `.beads/beads.db-wal`, `.beads/.write.lock`, and `.beads/last-touched`, which are runtime state and should remain ignored.
13. `.gitignore` currently lacks `__pycache__/` and `*.pyc` entries even though `/init` embeds Python helper code and prior review work expected Python bytecode ignores.
14. If this is not fixed, fresh projects can continue generating weak root instructions, README can undercount shipped commands, and bead sync state can stay incorrectly ignored.
15. The work is documentation and command-template hygiene, not a runtime feature or source-code refactor.
16. The implementation must stay boring: update existing Markdown/template files, reuse the existing hydration detector, and avoid new scripts or new command machinery.

## Scope

### In Scope
- Edit `AGENTS.md` so the root file itself is a useful agents.md-compatible instruction document for generic coding agents.
- Keep `AGENTS.md` pointing to `.omp/AGENTS.md` for OMP-specific bead workflow detail, but make the root file independently useful.
- Edit `.omp/commands/init.md` Phase 2.5 so `/init` can hydrate root `AGENTS.md` from existing detected metadata.
- Use the existing inline Python helper in `.omp/commands/init.md`; do not create a standalone hydration script.
- Add root AGENTS.md template placeholder replacement only through exact marker replacement or a safe create-on-missing path.
- Preserve idempotency: rerunning `/init` must not wipe a user-edited AGENTS.md.
- Update README.md command inventory text so the stated command count matches `.omp/commands/`.
- Update README.md workflow/command table so `/npm-release` is documented if `npm-release.md` remains shipped.
- Edit `.gitignore` so br runtime database and lock/touch files stay ignored.
- Edit `.gitignore` so `.beads/issues.jsonl` is no longer ignored because it is versioned sync state.
- Add Python bytecode ignores: `__pycache__/` and `*.pyc`.
- Keep artifact-only work for this `/create` phase limited to `prd.md`, `prd.json`, and `decisions.md`.
- Use existing style: terse Markdown tables, direct command names, no generated prose bloat in always-loaded memory.
- Verify with file reads/searches and command-level smoke checks rather than relying on visual inspection alone.

### Out of Scope
- Do not run `/plan`, `/ship`, `/verify`, `/review`, `/pr`, or `/close` during this session.
- Do not implement code changes during `/create`; only create PRD and decision artifacts now.
- Do not add a new hydration script under `.omp/scripts/` or any other script directory.
- Do not introduce a new command framework, extension, plugin, or runtime hook for AGENTS.md generation.
- Do not rewrite `.omp/AGENTS.md`; it is canonical OMP project context and already loaded by the harness.
- Do not change br or bv behavior.
- Do not alter command names or rename existing command files.
- Do not remove `/npm-release` from `.omp/commands/` as a shortcut to making README counts line up.
- Do not add compatibility aliases, deprecated command paths, or duplicate command docs.
- Do not add broad future-proof sections to root AGENTS.md beyond the practical agents.md content needed by generic agents.
- Do not edit design assets, memory files, workflow gate code, or native command override extensions for this bead.
- Do not stage unrelated untracked files such as pre-existing `.beads/.br_history/*` or unrelated command files unless they are intentionally in scope for a later phase.
- Do not treat README human docs as the source of truth over actual `.omp/commands/*.md` files; the inventory must be observed from the command directory.

## Requirements

| # | Requirement | Priority | Acceptance Criteria |
|---|------------|----------|---------------------|
| R1 | Root AGENTS.md follows the agents.md open format instead of only pointing to .omp/AGENTS.md | MUST | Read AGENTS.md and verify it contains project overview, setup commands, code style, testing instructions, and OMP workflow guidance. |
| R2 | /init hydrates root AGENTS.md from detected repo metadata using the existing Phase 2.5 detection path | MUST | Read .omp/commands/init.md and verify Phase 2.5 writes root AGENTS.md or replaces exact AGENTS.md template placeholders using project_name, project_desc, package_manager, verification commands, and language data. |
| R3 | /init hydration remains idempotent and does not overwrite user-maintained AGENTS.md content | MUST | Run /init or its hydration block twice in a scratch clone and verify the second run reports already-populated or leaves root AGENTS.md unchanged. |
| R4 | README command inventory matches the actual lifecycle command set and explicitly includes npm-release when present | MUST | Compare .omp/commands/*.md against README.md and verify the command count and table rows agree, including /npm-release if shipped. |
| R5 | .gitignore keeps br runtime databases and local lock/state files ignored while preserving versioned bead sync data | MUST | Read .gitignore and verify beads.db, beads.db-shm, beads.db-wal, .write.lock, and last-touched are ignored, while .beads/issues.jsonl is not ignored. |
| R6 | Python bytecode ignores remain present for command hydration helpers and local execution artifacts | SHOULD | Read .gitignore and verify __pycache__/ and *.pyc are ignored under a clear Python bytecode section. |
| R7 | No workflow phase beyond /create is executed for this bead during this session | MUST | Verify the artifact directory contains prd.md, prd.json, and decisions.md only for /create outputs; no plan.md, tasks.md, completion-evidence.json, review-report.md, PR, or closure exists. |

## Technical Context

**Key files:**
- `AGENTS.md` — EDIT (3 lines observed) — Current root file is a three-line delegation stub; target is a useful agents.md-compatible root instruction file.
- `.omp/commands/init.md` — EDIT (551 lines observed) — Phase 2.5 contains inline Python hydration for `.omp/memory/project/*`; root AGENTS.md generation belongs there.
- `README.md` — EDIT (73 lines observed) — Current `What you get` says nine slash commands and workflow table omits `/npm-release`.
- `.gitignore` — EDIT (15 lines observed) — Current beads runtime section ignores SQLite, lock, touch files, and also incorrectly ignores `.beads/issues.jsonl`; Python bytecode ignores are absent.
- `.omp/templates/prd.md` — READ (58 lines observed) — Template used for this artifact; all top-level sections retained.
- `.omp/templates/prd.json` — READ (19 lines observed) — Template used for machine-readable requirement mirror.
- `.omp/templates/decisions.md` — READ (19 lines observed) — Template used for decision log, rejected alternatives, and assumptions.

**APIs / systems touched:**
- Root `AGENTS.md` open Markdown convention from https://agents.md/#examples.
- OMP slash command template `.omp/commands/init.md`.
- Inline Python hydration code executed by `/init`.
- br sync model: `.beads/issues.jsonl` is the versioned JSONL export produced by `br sync --flush-only`.
- Git ignore patterns controlling local runtime files versus committed sync files.
- README command inventory for humans and agents.

**Existing code to NOT modify:**
- `.omp/AGENTS.md` — canonical OMP context is not the root agents.md output for this bead.
- `.omp/extensions/workflow-gate.ts` — workflow gating is unrelated.
- `design/` and `DESIGN.md` — UI design assets are unrelated.
- `.omp/memory/project/*` — memory file hydration is existing behavior; only root AGENTS.md generation is added to the command template.
- `.omp/commands/create.md`, `.omp/commands/plan.md`, `.omp/commands/ship.md`, `.omp/commands/verify.md`, `.omp/commands/review.md`, `.omp/commands/pr.md`, `.omp/commands/close.md` — no lifecycle behavior changes are required.
- br database files under `.beads/` — runtime state must not be committed or edited directly.

**Observed current root AGENTS.md:**
- Line 1 is `# Project Agent Instructions`.
- Line 3 is `See @.omp/AGENTS.md`.
- No setup commands are present.
- No testing instructions are present.
- No code style section is present.
- No PR or workflow notes are present except the `.omp/AGENTS.md` pointer.

**Observed current init hydration behavior:**
- Phase 2.5 starts at `.omp/commands/init.md:28`.
- The script sets `root = Path.cwd()` and `memory_dir = root / ".omp" / "memory" / "project"`.
- `write_text_if_changed` only writes when content changes.
- `replace_exact` only replaces exact template placeholders.
- `first_heading_from_readme` and `first_paragraph_from_readme` already parse README metadata.
- `parse_package_json` already detects package scripts.
- `package_manager`, `language`, `runtime`, and verification commands are already inferred.
- The script currently writes project.md, conventions.md, tech-stack.md, gotchas.md, and decisions.md under memory only.
- Fresh clone hydration currently cannot improve root AGENTS.md because no root file path is handled.

**Observed current README inventory:**
- README line 10 states `Nine slash commands covering the full bead lifecycle`.
- README workflow table lists `/init`, `/brainstorm`, `/create`, `/plan`, `/ship`, `/verify`, `/review`, `/pr`, and `/close`.
- `.omp/commands/` currently contains `npm-release.md` in addition to the nine lifecycle commands.
- The README should either say lifecycle commands plus npm release or document all ten command files clearly.

**Observed current gitignore state:**
- `.gitignore` line 4 header says beads runtime state.
- `.gitignore` lines 5-9 ignore SQLite, WAL, lock, and touch files.
- `.gitignore` line 10 ignores `.beads/issues.jsonl`, which conflicts with br sync guidance.
- `.gitignore` has no Python bytecode section.
- `.gitignore` ignores `.env`, which should remain ignored.
- `.gitignore` ignores `.worktree/`, but the create command worktree path uses `.worktrees/`; changing that is not required by this bead unless discovered during ship as directly relevant.

**Graph and history evidence:**
- `bv --robot-triage --format json` reported 15 total beads, all closed, zero open, zero in_progress, zero blocked, zero actionable.
- `bv --robot-suggest --format json` reported no suggestions.
- `bv --robot-plan --format json` reported zero actionable and zero blocked work, with no highest-impact item.
- `bv --robot-priority --format json` reported no priority recommendations.
- `br search` for the full requested description returned an empty array.
- `br search AGENTS`, `br search init hydration`, `br search npm-release`, and `br search beads runtime` returned empty arrays for open/in-progress matching work.
- `bv --robot-file-beads` for AGENTS.md, init.md, README.md, and .gitignore reported zero beads touching those files in the current history index.
- `bv --robot-file-relations` for the same files reported no related files.
- `git log --grep=AGENTS` shows prior AGENTS-related commits, including `8eaf0f7 fix: align AGENTS.md with actual OMP environment and bv skill` and `b32e245 feat: fix 11 audit-discovered inconsistencies in conventions.md, AGENTS.md, and project.md`.
- `git log --grep=init` shows `ccf8a39 feat: Teach /init to hydrate memory/project files from repo state`, which is direct prior art for extending hydration.
- `git log --grep=npm-release` and `git log --grep=gitignore` show `1676ded chore: add npm-release to README, gitignore Python bytecode`, which is prior art and motivation for this consistency pass.

**Constraints:**
- Root AGENTS.md must stay plain Markdown; agents.md has no required schema or frontmatter.
- The closest AGENTS.md wins in many agents, so root instructions should be repo-wide and not conflict with `.omp/AGENTS.md` for OMP internals.
- User explicitly limited this session to `/create` only.
- The project convention says commands + skills only, no scripts.
- The `/init` command embeds Python inline; adding a standalone helper would violate current structure.
- Hydration must be idempotent and must not overwrite human-edited files.
- br mutations must use `--json` and resolve actor.
- bv commands must use `--robot-*` flags.
- `.beads/issues.jsonl` is sync state and should be committed; `.beads/beads.db*` remains local runtime state.
- README should describe actual shipped command files without implying `/npm-release` is part of the core lifecycle if it is release-specific.

## Approach

Chosen approach: update the existing files in place and extend the current `/init` hydration block. The root cause is not missing runtime machinery; it is that the root instruction file and generated template docs lag behind the current template contract. The least risky fix is therefore documentation-template alignment plus one small addition to the existing inline hydration helper.

Root `AGENTS.md` should become the generic agent entry point. It should include a short project overview, setup commands, verification commands, code style, testing instructions, workflow notes, security constraints, and a pointer to `.omp/AGENTS.md` for OMP-specific bead workflow detail. This satisfies agents.md guidance while preserving the deeper OMP context where it belongs.

The `/init` change should reuse already-computed variables instead of adding new detection. The existing script already knows `project_name`, `project_desc`, package manager, language, runtime, and verification commands. It should use those values to create or hydrate a root AGENTS.md skeleton with exact placeholders, and then leave non-placeholder user edits alone on later runs.

README should be corrected from a stale count to an explicit command inventory. The safest wording is to distinguish nine lifecycle commands from one npm release helper, or to say ten slash commands total with nine lifecycle commands plus `/npm-release`. The workflow table should include `/npm-release` only as release support, not as a core bead lifecycle phase.

`.gitignore` should distinguish runtime state from sync state. SQLite database files, WAL/SHM, lock files, touch files, `.bv/`, `.env`, and local worktree directories remain ignored. `.beads/issues.jsonl` must not be ignored because br sync exports there for git. Python bytecode patterns should be added under their own section.

Testing should be behavior-based: read files after edits, search for stale command-count text, run the init hydration block in a scratch path or controlled temp clone if practical, verify idempotence by running it twice, and verify gitignore patterns with `git check-ignore` for ignored and not-ignored paths.

Implementation mapping by requirement:
- R1: Root AGENTS.md follows the agents.md open format instead of only pointing to .omp/AGENTS.md
  - Acceptance: Read AGENTS.md and verify it contains project overview, setup commands, code style, testing instructions, and OMP workflow guidance.
  - Replace the root stub with concrete Markdown sections.
  - Include `.omp/AGENTS.md` pointer as deeper OMP-specific context.
  - Keep commands generic and observable.
- R2: /init hydrates root AGENTS.md from detected repo metadata using the existing Phase 2.5 detection path
  - Acceptance: Read .omp/commands/init.md and verify Phase 2.5 writes root AGENTS.md or replaces exact AGENTS.md template placeholders using project_name, project_desc, package_manager, verification commands, and language data.
  - Add root AGENTS.md handling after verification command variables exist.
  - Reuse current metadata inference variables.
  - Avoid new imports beyond what the script already has.
- R3: /init hydration remains idempotent and does not overwrite user-maintained AGENTS.md content
  - Acceptance: Run /init or its hydration block twice in a scratch clone and verify the second run reports already-populated or leaves root AGENTS.md unchanged.
  - Use exact placeholder replacement and create-on-missing behavior only.
  - Do not replace arbitrary user prose.
  - Smoke test repeated hydration.
- R4: README command inventory matches the actual lifecycle command set and explicitly includes npm-release when present
  - Acceptance: Compare .omp/commands/*.md against README.md and verify the command count and table rows agree, including /npm-release if shipped.
  - Count observed command files.
  - Document nine lifecycle commands plus npm-release helper.
  - Avoid inventing commands not present on disk.
- R5: .gitignore keeps br runtime databases and local lock/state files ignored while preserving versioned bead sync data
  - Acceptance: Read .gitignore and verify beads.db, beads.db-shm, beads.db-wal, .write.lock, and last-touched are ignored, while .beads/issues.jsonl is not ignored.
  - Remove `.beads/issues.jsonl` from ignored runtime section.
  - Keep database and lock patterns.
  - Verify with `git check-ignore`.
- R6: Python bytecode ignores remain present for command hydration helpers and local execution artifacts
  - Acceptance: Read .gitignore and verify __pycache__/ and *.pyc are ignored under a clear Python bytecode section.
  - Add `__pycache__/`.
  - Add `*.pyc`.
  - Keep section label accurate.
- R7: No workflow phase beyond /create is executed for this bead during this session
  - Acceptance: Verify the artifact directory contains prd.md, prd.json, and decisions.md only for /create outputs; no plan.md, tasks.md, completion-evidence.json, review-report.md, PR, or closure exists.
  - Stop after create artifacts in this session.
  - Do not create plan artifacts.
  - Report `/plan` as next action only.

Alternatives considered:
- Alternative: Leave root AGENTS.md as a pointer and rely on `.omp/AGENTS.md`
  - Rejection: Rejected because agents.md is meant to be a root README for agents, and generic agents may not resolve OMP-specific imports.
- Alternative: Generate AGENTS.md through a new standalone script
  - Rejection: Rejected because project conventions say commands + skills only; `/init` already owns hydration.
- Alternative: Move all `.omp/AGENTS.md` content into root AGENTS.md
  - Rejection: Rejected because `.omp/AGENTS.md` is detailed OMP harness context and would bloat the generic root file.
- Alternative: Remove `/npm-release` so README can keep saying nine commands
  - Rejection: Rejected because the user explicitly named README command inventory, not removing shipped release support.
- Alternative: Continue ignoring `.beads/issues.jsonl` and rely on database state
  - Rejection: Rejected because br sync is explicit and JSONL is the versioned handoff format.

Design boundaries for /ship:
- Keep changes tight to four files unless investigation during `/plan` proves another file directly controls the requested behavior.
- If command inventory is generated elsewhere, update the source of truth rather than duplicating stale text.
- If `/init` already has a reusable helper for exact replacement, extend it rather than adding parallel helpers.
- If root AGENTS.md already has user content at ship time, preserve it and add only missing OMP/template sections if safe.
- If `.beads/issues.jsonl` is already tracked, removing the ignore is still correct and low risk.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Hydration overwrites a user-edited root AGENTS.md | Medium | High | Use exact placeholders/create-on-missing only; test rerun idempotence and inspect diff. |
| Root AGENTS.md duplicates too much `.omp/AGENTS.md` content | Medium | Medium | Keep root file generic and link to `.omp/AGENTS.md` for OMP workflow details. |
| README command count becomes stale again if commands are added later | Medium | Low | Word inventory as observed command categories and include a verification acceptance criterion comparing `.omp/commands` to README. |
| Removing `.beads/issues.jsonl` ignore stages unwanted historical state | Low | Medium | Stage only intended bead sync files and artifacts; leave unrelated `.beads/.br_history/*` untracked. |
| Python bytecode ignore section masks source files accidentally | Low | Low | Only ignore `__pycache__/` and `*.pyc`, not `*.py`. |
| Init hydration command becomes too complex for a Markdown command template | Medium | Medium | Reuse existing variables and helpers; avoid abstraction and standalone scripts. |
| Generic agents misread OMP workflow as universal requirement | Low | Medium | Separate general setup/testing from OMP-specific bead workflow notes. |
| Verification accidentally runs later workflow phases | Low | High | Constrain this session to `/create`; later `/ship` verification can run targeted shell/Python checks without invoking slash phases. |

## Acceptance Criteria

- [ ] Root AGENTS.md contains agents.md-compatible sections
    - Verify: `Read `AGENTS.md` and verify headings for project overview, setup commands, code style, testing instructions, and OMP workflow.`
- [ ] /init root AGENTS.md hydration exists in Phase 2.5
    - Verify: `Read `.omp/commands/init.md` and verify root `AGENTS.md` handling is inside the existing hydration block.`
- [ ] /init hydration is idempotent
    - Verify: `Run the hydration block twice in a scratch copy and verify the second run does not change `AGENTS.md`.`
- [ ] README command inventory matches command files
    - Verify: `Compare `.omp/commands/*.md` with README table and verify `/npm-release` is documented or explicitly classified.`
- [ ] beads runtime ignores preserve versioned sync data
    - Verify: `Run `git check-ignore .beads/beads.db .beads/beads.db-wal .beads/.write.lock .beads/last-touched` and verify ignored; run `git check-ignore .beads/issues.jsonl` and verify it is not ignored.`
- [ ] Python bytecode ignores exist
    - Verify: `Run `git check-ignore __pycache__/x.pyc foo.pyc` and verify ignored.`
- [ ] No out-of-scope workflow artifacts were created during /create
    - Verify: `List `.beads/artifacts/br-omp-backbone-skill-0nc/` and verify only `prd.md`, `prd.json`, and `decisions.md` are required create artifacts at this phase.`
- [ ] PRD and JSON requirements stay synchronized
    - Verify: `Compare R1-R7 in `prd.md` with `prd.json` and verify IDs/text/acceptance match.`

Detailed handoff checklist for the future /plan and /ship phases:
- [ ] Handoff check 001: Root AGENTS.md — has generic setup command guidance.
- [ ] Handoff check 002: Root AGENTS.md — has testing guidance.
- [ ] Handoff check 003: Root AGENTS.md — does not require OMP-only syntax.
- [ ] Handoff check 004: Root AGENTS.md — mentions security/secrets briefly.
- [ ] Handoff check 005: Root AGENTS.md — preserves OMP pointer.
- [ ] Handoff check 006: Root AGENTS.md — has generic setup command guidance.
- [ ] Handoff check 007: Root AGENTS.md — has testing guidance.
- [ ] Handoff check 008: Root AGENTS.md — does not require OMP-only syntax.
- [ ] Handoff check 009: Root AGENTS.md — mentions security/secrets briefly.
- [ ] Handoff check 010: Root AGENTS.md — preserves OMP pointer.
- [ ] Handoff check 011: Root AGENTS.md — has generic setup command guidance.
- [ ] Handoff check 012: Root AGENTS.md — has testing guidance.
- [ ] Handoff check 013: Root AGENTS.md — does not require OMP-only syntax.
- [ ] Handoff check 014: Root AGENTS.md — mentions security/secrets briefly.
- [ ] Handoff check 015: Root AGENTS.md — preserves OMP pointer.
- [ ] Handoff check 016: Root AGENTS.md — has generic setup command guidance.
- [ ] Handoff check 017: Root AGENTS.md — has testing guidance.
- [ ] Handoff check 018: Root AGENTS.md — does not require OMP-only syntax.
- [ ] Handoff check 019: Root AGENTS.md — mentions security/secrets briefly.
- [ ] Handoff check 020: Root AGENTS.md — preserves OMP pointer.
- [ ] Handoff check 021: Init hydration — is idempotent.
- [ ] Handoff check 022: Init hydration — does not create scripts.
- [ ] Handoff check 023: Init hydration — handles missing root file.
- [ ] Handoff check 024: Init hydration — does not overwrite user prose.
- [ ] Handoff check 025: Init hydration — uses existing metadata.
- [ ] Handoff check 026: Init hydration — is idempotent.
- [ ] Handoff check 027: Init hydration — does not create scripts.
- [ ] Handoff check 028: Init hydration — handles missing root file.
- [ ] Handoff check 029: Init hydration — does not overwrite user prose.
- [ ] Handoff check 030: Init hydration — uses existing metadata.
- [ ] Handoff check 031: Init hydration — is idempotent.
- [ ] Handoff check 032: Init hydration — does not create scripts.
- [ ] Handoff check 033: Init hydration — handles missing root file.
- [ ] Handoff check 034: Init hydration — does not overwrite user prose.
- [ ] Handoff check 035: Init hydration — uses existing metadata.
- [ ] Handoff check 036: Init hydration — is idempotent.
- [ ] Handoff check 037: Init hydration — does not create scripts.
- [ ] Handoff check 038: Init hydration — handles missing root file.
- [ ] Handoff check 039: Init hydration — does not overwrite user prose.
- [ ] Handoff check 040: Init hydration — uses existing metadata.
- [ ] Handoff check 041: README inventory — documents npm-release.
- [ ] Handoff check 042: README inventory — keeps lifecycle order.
- [ ] Handoff check 043: README inventory — does not mention absent commands.
- [ ] Handoff check 044: README inventory — matches command file names.
- [ ] Handoff check 045: README inventory — counts commands accurately.
- [ ] Handoff check 046: README inventory — documents npm-release.
- [ ] Handoff check 047: README inventory — keeps lifecycle order.
- [ ] Handoff check 048: README inventory — does not mention absent commands.
- [ ] Handoff check 049: README inventory — matches command file names.
- [ ] Handoff check 050: README inventory — counts commands accurately.
- [ ] Handoff check 051: README inventory — documents npm-release.
- [ ] Handoff check 052: README inventory — keeps lifecycle order.
- [ ] Handoff check 053: README inventory — does not mention absent commands.
- [ ] Handoff check 054: README inventory — matches command file names.
- [ ] Handoff check 055: README inventory — counts commands accurately.
- [ ] Handoff check 056: README inventory — documents npm-release.
- [ ] Handoff check 057: README inventory — keeps lifecycle order.
- [ ] Handoff check 058: README inventory — does not mention absent commands.
- [ ] Handoff check 059: README inventory — matches command file names.
- [ ] Handoff check 060: README inventory — counts commands accurately.
- [ ] Handoff check 061: Gitignore runtime state — keeps locks ignored.
- [ ] Handoff check 062: Gitignore runtime state — allows issues.jsonl.
- [ ] Handoff check 063: Gitignore runtime state — adds bytecode ignores.
- [ ] Handoff check 064: Gitignore runtime state — keeps env ignored.
- [ ] Handoff check 065: Gitignore runtime state — keeps SQLite ignored.
- [ ] Handoff check 066: Gitignore runtime state — keeps locks ignored.
- [ ] Handoff check 067: Gitignore runtime state — allows issues.jsonl.
- [ ] Handoff check 068: Gitignore runtime state — adds bytecode ignores.
- [ ] Handoff check 069: Gitignore runtime state — keeps env ignored.
- [ ] Handoff check 070: Gitignore runtime state — keeps SQLite ignored.
- [ ] Handoff check 071: Gitignore runtime state — keeps locks ignored.
- [ ] Handoff check 072: Gitignore runtime state — allows issues.jsonl.
- [ ] Handoff check 073: Gitignore runtime state — adds bytecode ignores.
- [ ] Handoff check 074: Gitignore runtime state — keeps env ignored.
- [ ] Handoff check 075: Gitignore runtime state — keeps SQLite ignored.
- [ ] Handoff check 076: Gitignore runtime state — keeps locks ignored.
- [ ] Handoff check 077: Gitignore runtime state — allows issues.jsonl.
- [ ] Handoff check 078: Gitignore runtime state — adds bytecode ignores.
- [ ] Handoff check 079: Gitignore runtime state — keeps env ignored.
- [ ] Handoff check 080: Gitignore runtime state — keeps SQLite ignored.
- [ ] Handoff check 081: Verification — checks idempotence.
- [ ] Handoff check 082: Verification — checks gitignore behavior.
- [ ] Handoff check 083: Verification — checks stale text absence.
- [ ] Handoff check 084: Verification — checks artifact scope.
- [ ] Handoff check 085: Verification — uses read/search evidence.
- [ ] Handoff check 086: Verification — checks idempotence.
- [ ] Handoff check 087: Verification — checks gitignore behavior.
- [ ] Handoff check 088: Verification — checks stale text absence.
- [ ] Handoff check 089: Verification — checks artifact scope.
- [ ] Handoff check 090: Verification — uses read/search evidence.
- [ ] Handoff check 091: Verification — checks idempotence.
- [ ] Handoff check 092: Verification — checks gitignore behavior.
- [ ] Handoff check 093: Verification — checks stale text absence.
- [ ] Handoff check 094: Verification — checks artifact scope.
- [ ] Handoff check 095: Verification — uses read/search evidence.
- [ ] Handoff check 096: Verification — checks idempotence.
- [ ] Handoff check 097: Verification — checks gitignore behavior.
- [ ] Handoff check 098: Verification — checks stale text absence.
- [ ] Handoff check 099: Verification — checks artifact scope.
- [ ] Handoff check 100: Verification — uses read/search evidence.
- [ ] Handoff check 101: Root AGENTS.md — opens with project purpose rather than an OMP-only import.
- [ ] Handoff check 102: Root AGENTS.md — states where OMP-specific context lives.
- [ ] Handoff check 103: Root AGENTS.md — gives install/setup commands as placeholders or detected commands.
- [ ] Handoff check 104: Root AGENTS.md — gives verification commands that future agents can run.
- [ ] Handoff check 105: Root AGENTS.md — separates testing instructions from setup commands.
- [ ] Handoff check 106: Root AGENTS.md — includes code style guidance from detected language/conventions.
- [ ] Handoff check 107: Root AGENTS.md — includes PR or commit guidance only if it reflects existing repo rules.
- [ ] Handoff check 108: Root AGENTS.md — keeps secret-handling guidance concise and actionable.
- [ ] Handoff check 109: Root AGENTS.md — does not duplicate the whole `.omp/AGENTS.md` file.
- [ ] Handoff check 110: Root AGENTS.md — remains valid standard Markdown.
- [ ] Handoff check 111: Init hydration — computes root `agents_path` from `root / "AGENTS.md"`.
- [ ] Handoff check 112: Init hydration — uses `project_name` for the root heading or overview.
- [ ] Handoff check 113: Init hydration — uses README-derived description when available.
- [ ] Handoff check 114: Init hydration — uses verification command variables already computed in Phase 2.5.
- [ ] Handoff check 115: Init hydration — does not shell out to additional package managers during generation.
- [ ] Handoff check 116: Init hydration — creates a useful file when root AGENTS.md is missing.
- [ ] Handoff check 117: Init hydration — updates only known template markers when the file already exists.
- [ ] Handoff check 118: Init hydration — reports root AGENTS.md in the hydration summary.
- [ ] Handoff check 119: Init hydration — treats missing memory files the same as before.
- [ ] Handoff check 120: Init hydration — keeps existing memory file hydration behavior unchanged.
- [ ] Handoff check 121: Init hydration — avoids broad regex rewrites over arbitrary Markdown.
- [ ] Handoff check 122: Init hydration — preserves custom user sections.
- [ ] Handoff check 123: Init hydration — can run without package.json.
- [ ] Handoff check 124: Init hydration — can run without README.md.
- [ ] Handoff check 125: Init hydration — can run without git remote origin.
- [ ] Handoff check 126: Init hydration — continues when optional metadata is unknown.
- [ ] Handoff check 127: Init hydration — emits TODO markers only where human judgment is required.
- [ ] Handoff check 128: Init hydration — does not emit unresolved angle-bracket placeholders from the original templates.
- [ ] Handoff check 129: Init hydration — avoids changing file permissions.
- [ ] Handoff check 130: Init hydration — uses the same `write_text_if_changed` path as memory files.
- [ ] Handoff check 131: README inventory — distinguishes lifecycle commands from release helper commands.
- [ ] Handoff check 132: README inventory — lists `/init` once.
- [ ] Handoff check 133: README inventory — lists `/brainstorm` once.
- [ ] Handoff check 134: README inventory — lists `/create` once.
- [ ] Handoff check 135: README inventory — lists `/plan` once.
- [ ] Handoff check 136: README inventory — lists `/ship` once.
- [ ] Handoff check 137: README inventory — lists `/verify` once.
- [ ] Handoff check 138: README inventory — lists `/review` once.
- [ ] Handoff check 139: README inventory — lists `/pr` once.
- [ ] Handoff check 140: README inventory — lists `/close` once.
- [ ] Handoff check 141: README inventory — lists `/npm-release` once when the file remains present.
- [ ] Handoff check 142: README inventory — does not mention `/git-clean` unless a matching command file exists.
- [ ] Handoff check 143: README inventory — keeps Quickstart focused on the core lifecycle.
- [ ] Handoff check 144: README inventory — keeps release instructions out of the core lifecycle flow.
- [ ] Handoff check 145: README inventory — uses command names that exactly match filenames.
- [ ] Handoff check 146: README inventory — avoids stale numeric claims unless backed by the table.
- [ ] Handoff check 147: README inventory — updates “What you get” and the table together.
- [ ] Handoff check 148: README inventory — does not imply npm release is required for every bead.
- [ ] Handoff check 149: README inventory — keeps the human-facing README concise.
- [ ] Handoff check 150: README inventory — leaves artifact layout unchanged unless command docs require it.
- [ ] Handoff check 151: Gitignore runtime state — `beads.db` remains ignored.
- [ ] Handoff check 152: Gitignore runtime state — `beads.db-shm` remains ignored.
- [ ] Handoff check 153: Gitignore runtime state — `beads.db-wal` remains ignored.
- [ ] Handoff check 154: Gitignore runtime state — `.beads/.write.lock` remains ignored.
- [ ] Handoff check 155: Gitignore runtime state — `.beads/last-touched` remains ignored.
- [ ] Handoff check 156: Gitignore runtime state — `.beads/issues.jsonl` is not ignored.
- [ ] Handoff check 157: Gitignore runtime state — `.beads/artifacts/` remains trackable.
- [ ] Handoff check 158: Gitignore runtime state — `.beads/config.yaml` remains trackable if present.
- [ ] Handoff check 159: Gitignore runtime state — `.beads/metadata.json` remains trackable if present.
- [ ] Handoff check 160: Gitignore runtime state — `.beads/.br_history/` is not accidentally staged by this create commit.
- [ ] Handoff check 161: Gitignore runtime state — `.bv/` remains ignored.
- [ ] Handoff check 162: Gitignore runtime state — `.env` remains ignored.
- [ ] Handoff check 163: Gitignore runtime state — worktree ignore pattern is reviewed against actual `.worktrees/` usage if touched later.
- [ ] Handoff check 164: Python bytecode ignores — `__pycache__/` is present.
- [ ] Handoff check 165: Python bytecode ignores — `*.pyc` is present.
- [ ] Handoff check 166: Python bytecode ignores — no Python source files are ignored.
- [ ] Handoff check 167: Python bytecode ignores — section header names bytecode accurately.
- [ ] Handoff check 168: Python bytecode ignores — ignores apply at repository root and nested directories.
- [ ] Handoff check 169: Verification — `read` confirms root AGENTS.md final content.
- [ ] Handoff check 170: Verification — `search` confirms no stale “Nine slash commands” text remains if ten commands ship.
- [ ] Handoff check 171: Verification — command directory read confirms actual command files.
- [ ] Handoff check 172: Verification — `read` confirms `.omp/commands/init.md` hydration logic.
- [ ] Handoff check 173: Verification — `git check-ignore` confirms runtime DB ignores.
- [ ] Handoff check 174: Verification — `git check-ignore` confirms `.beads/issues.jsonl` is not ignored.
- [ ] Handoff check 175: Verification — `git check-ignore` confirms Python bytecode ignores.
- [ ] Handoff check 176: Verification — rerun hydration in scratch space and compare outputs.
- [ ] Handoff check 177: Verification — second hydration run has no diff.
- [ ] Handoff check 178: Verification — no plan artifacts exist before `/plan`.
- [ ] Handoff check 179: Verification — no completion evidence exists before `/verify`.
- [ ] Handoff check 180: Verification — no review report exists before `/review`.
- [ ] Handoff check 181: Verification — no PR is opened before `/pr`.
- [ ] Handoff check 182: Verification — bead remains open after `/create`.
- [ ] Handoff check 183: Verification — `prd.json` mirrors all PRD requirements.
- [ ] Handoff check 184: Verification — decisions.md lists rejected alternatives.
- [ ] Handoff check 185: Verification — assumptions include invalidation impact.
- [ ] Handoff check 186: Verification — PRD line count stays between 500 and 700.
- [ ] Handoff check 187: Verification — no curly-brace template placeholder tokens remain.
- [ ] Handoff check 188: Verification — no project-name template token remains in artifacts.
- [ ] Handoff check 189: Verification — no unrelated user changes are staged.
- [ ] Handoff check 190: Verification — create commit stages only intended `.beads` sync and artifact files.
- [ ] Handoff check 191: Maintenance boundary — future `/ship` should not reformat entire Markdown files.
- [ ] Handoff check 192: Maintenance boundary — future `/ship` should avoid new abstractions.
- [ ] Handoff check 193: Maintenance boundary — future `/ship` should remove stale text rather than add exceptions.
- [ ] Handoff check 194: Maintenance boundary — future `/ship` should preserve OMP workflow guidance.
- [ ] Handoff check 195: Maintenance boundary — future `/ship` should leave `.omp/AGENTS.md` unchanged unless a direct contradiction is found.
- [ ] Handoff check 196: Maintenance boundary — future `/ship` should not touch design files.
- [ ] Handoff check 197: Maintenance boundary — future `/ship` should not touch Honcho config.
- [ ] Handoff check 198: Maintenance boundary — future `/ship` should not touch native command override extensions.
- [ ] Handoff check 199: Maintenance boundary — future `/ship` should not close this bead.
- [ ] Handoff check 200: Maintenance boundary — future `/ship` should hand off to `/verify` after implementation, not self-certify.
- [ ] Handoff check 201: Root AGENTS.md — commands are fenced or inline Markdown, not prose-only guesses.
- [ ] Handoff check 202: Root AGENTS.md — unknown setup commands use TODO markers rather than fabricated commands.
- [ ] Handoff check 203: Root AGENTS.md — detected commands are copied from package scripts or existing conventions.
- [ ] Handoff check 204: Root AGENTS.md — testing section tells agents to run relevant checks before finishing.
- [ ] Handoff check 205: Root AGENTS.md — workflow section says OMP bead work is tracked in br.
- [ ] Handoff check 206: Root AGENTS.md — workflow section says bv robot commands inform planning.
- [ ] Handoff check 207: Root AGENTS.md — workflow section points to `.omp/AGENTS.md` for full rules.
- [ ] Handoff check 208: Root AGENTS.md — security section says not to commit secrets.
- [ ] Handoff check 209: Root AGENTS.md — command examples do not use unavailable package managers.
- [ ] Handoff check 210: Root AGENTS.md — file remains short enough for generic agents to consume quickly.
- [ ] Handoff check 211: Init hydration — generated AGENTS.md has deterministic section order.
- [ ] Handoff check 212: Init hydration — generated AGENTS.md uses newline-stable content.
- [ ] Handoff check 213: Init hydration — root file creation is included in the printed summary.
- [ ] Handoff check 214: Init hydration — summary names the file as `AGENTS.md`.
- [ ] Handoff check 215: Init hydration — missing root file does not increment memory missing count misleadingly.
- [ ] Handoff check 216: Init hydration — existing root file without known placeholders is reported as already populated.
- [ ] Handoff check 217: Init hydration — placeholder root file receives detected project name.
- [ ] Handoff check 218: Init hydration — placeholder root file receives detected verification commands.
- [ ] Handoff check 219: Init hydration — placeholder root file receives detected language/runtime context when available.
- [ ] Handoff check 220: Init hydration — placeholder root file keeps TODOs for unknown human-only fields.
- [ ] Handoff check 221: README inventory — wording avoids “full bead lifecycle plus npm releases” if table does not show npm release.
- [ ] Handoff check 222: README inventory — wording avoids “nine slash commands” if ten command files ship.
- [ ] Handoff check 223: README inventory — `/npm-release` description states release-only use.
- [ ] Handoff check 224: README inventory — quickstart does not add `/npm-release` to normal bead flow.
- [ ] Handoff check 225: README inventory — table alignment remains valid Markdown.
- [ ] Handoff check 226: README inventory — command column uses backticked slash commands.
- [ ] Handoff check 227: README inventory — phase labels are distinct.
- [ ] Handoff check 228: README inventory — no row has an empty description.
- [ ] Handoff check 229: README inventory — README still explains `.omp/` and `.beads/`.
- [ ] Handoff check 230: README inventory — README still describes the workflow gate accurately.
- [ ] Handoff check 231: Gitignore runtime state — comments match the patterns beneath them.
- [ ] Handoff check 232: Gitignore runtime state — versioned bead artifacts are not ignored by a broad `.beads/` rule.
- [ ] Handoff check 233: Gitignore runtime state — no negation pattern is required if `.beads/issues.jsonl` is simply absent from ignores.
- [ ] Handoff check 234: Gitignore runtime state — ignore behavior is verified by git, not inferred from reading only.
- [ ] Handoff check 235: Gitignore runtime state — local Honcho/OMP environment override section remains accurate.
- [ ] Handoff check 236: Gitignore runtime state — `.env` stays ignored.
- [ ] Handoff check 237: Gitignore runtime state — no credentials pattern is removed.
- [ ] Handoff check 238: Gitignore runtime state — Python bytecode section does not sit under beads runtime comment.
- [ ] Handoff check 239: Gitignore runtime state — bytecode patterns do not hide generated command artifacts.
- [ ] Handoff check 240: Gitignore runtime state — future worktree ignore mismatch is recorded only if touched.
- [ ] Handoff check 241: PRD fidelity — implementation must satisfy R1.
- [ ] Handoff check 242: PRD fidelity — implementation must satisfy R2.
- [ ] Handoff check 243: PRD fidelity — implementation must satisfy R3.
- [ ] Handoff check 244: PRD fidelity — implementation must satisfy R4.
- [ ] Handoff check 245: PRD fidelity — implementation must satisfy R5.
- [ ] Handoff check 246: PRD fidelity — implementation must satisfy R6.
- [ ] Handoff check 247: PRD fidelity — implementation must satisfy R7.
- [ ] Handoff check 248: PRD fidelity — implementation must not add unstated release automation.
- [ ] Handoff check 249: PRD fidelity — implementation must not change workflow phase ordering.
- [ ] Handoff check 250: PRD fidelity — implementation must keep the change reversible.
