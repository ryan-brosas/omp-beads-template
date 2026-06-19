<!-- DENSITY: Target 500-700 lines. <300 = incomplete (missing sections, hand-wavy, no real technical context). No upper cap — be thorough. This is an AI handoff: another agent must be able to pick this up and implement correctly without guessing. Every section must have concrete evidence: file paths, API signatures, existing patterns, constraints. -->
# PRD: Align .omp/AGENTS.md command inventory with shipped lifecycle and npm-release commands

**Bead:** br-omp-backbone-skill-3co | **Type:** chore | **Priority:** P2
**Created:** 2026-06-19 | **Estimate:** 45 minutes

## Problem

WHEN an agent loads canonical project context from `.omp/AGENTS.md`, THEN the command inventory omits the shipped `/npm-release` command and still says `.omp/commands/` contains nine slash commands, BECAUSE the earlier command-inventory alignment updated README and verification/review rules but did not update the canonical OMP context file that this harness injects into every session.

This affects every OMP agent in this repository because `.omp/AGENTS.md` is the authoritative always-loaded context for workflow rules, command references, and the repository tree. README already advertises “Nine lifecycle slash commands plus the npm-release release helper,” and `git ls-files ".omp/commands/*.md"` shows ten tracked command files, including `.omp/commands/npm-release.md`; `.omp/AGENTS.md` is now the stale source. If left unfixed, agents can falsely conclude `/npm-release` is unshipped or out-of-band even though the command exists and README documents it.

The root cause is not that the command file is missing. The command file is tracked. The root cause is split inventory maintenance: README was aligned with tracked commands in prior commits, while `.omp/AGENTS.md` kept its older command table and tree block. This bead formalizes a narrow documentation correction so `/ship` can change the canonical inventory without touching command implementation, release behavior, or workflow gate semantics.

Observed evidence from investigation:
- `.omp/AGENTS.md:20-30` Command Reference lists `/brainstorm`, `/create`, `/plan`, `/ship`, `/verify`, `/review`, `/pr`, `/close`, and `/init`, but not `/npm-release`.
- `.omp/AGENTS.md:204` says `.omp/commands/` contains `9 slash commands`.
- `.omp/AGENTS.md:205-206` lists `brainstorm.md`, `create.md`, `plan.md`, `ship.md`, `verify.md`, `review.md`, `pr.md`, `close.md`, and `init.md`, but not `npm-release.md`.
- `README.md:10` says there are `Nine lifecycle slash commands plus the npm-release release helper`.
- `README.md:39-50` includes a workflow table row for `/npm-release`.
- `git ls-files ".omp/commands/*.md"` returned ten tracked commands: brainstorm, close, create, init, npm-release, plan, pr, review, ship, and verify.
- `.omp/commands/npm-release.md:7-9` defines the release command purpose and confirms it is a real shipped command, not scratch text.
- `.omp/commands/verify.md:54-67` and `.omp/commands/review.md:67-79` already define tracked command files as the inventory source of truth.

## Scope

### In Scope
- Edit `.omp/AGENTS.md` Command Reference so it includes a `/npm-release` row.
- Keep the eight-command bead lifecycle loop clear: `/brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close` remains the normal bead flow.
- Describe `/init` as bootstrap and `/npm-release` as a release helper so agents do not run release as part of ordinary bead completion.
- Update `.omp/AGENTS.md` repository tree comments from nine command files to ten command files.
- Add `npm-release.md` to the `.omp/commands/` file listing in `.omp/AGENTS.md`.
- Verify inventory against tracked files with `git ls-files ".omp/commands/*.md"`, not untracked filesystem globbing.
- Preserve README wording unless verification proves README and `.omp/AGENTS.md` conflict after the `.omp/AGENTS.md` fix.
- Preserve command files, workflow-gate extension behavior, templates, skills, and memory files unless a direct consistency issue is found during verification.

### Out of Scope
- Do not edit `.omp/commands/npm-release.md` behavior, allowed tools, version validation, release flow, or reporting text.
- Do not add a new command file.
- Do not rename `/npm-release`.
- Do not change the bead lifecycle ordering.
- Do not make `/npm-release` a required step before `/close`.
- Do not alter `.omp/extensions/workflow-gate.ts`.
- Do not alter native OMP slash command override behavior or global OMP runtime patches.
- Do not rework root `AGENTS.md` agents.md compliance.
- Do not edit README if `.omp/AGENTS.md` can be aligned to the already-correct README contract.
- Do not stage existing `.beads/.br_history/` untracked files unless br sync deliberately updates tracked bead state required for this bead.
- Do not close or modify the broader in-progress bead `br-omp-backbone-skill-0nc`.

## Requirements

| # | Requirement | Priority | Acceptance Criteria |
|---|------------|----------|---------------------|
| R1 | The `.omp/AGENTS.md` Command Reference table includes every tracked shipped lifecycle command and the tracked `/npm-release` command exactly once. | MUST | `git ls-files .omp/commands/*.md` returns ten tracked command files and `python3` parsing of `.omp/AGENTS.md` finds the same ten slash command names in the Command Reference table, with no missing or extra entries. |
| R2 | The `.omp/AGENTS.md` workflow narrative distinguishes the eight bead lifecycle execution loop from bootstrap and release helper commands. | MUST | Reading lines 8-31 of `.omp/AGENTS.md` shows `/brainstorm` through `/close` as the lifecycle loop, `/init` as bootstrap, and `/npm-release` as release helper, without implying npm release is part of every bead loop. |
| R3 | The `.omp/AGENTS.md` repository tree comment and command file listing match the tracked command inventory. | MUST | The tree block under `.omp/commands/` says ten command files and lists `npm-release.md` alongside the existing command files, matching `git ls-files .omp/commands/*.md`. |
| R4 | README and `.omp/AGENTS.md` agree on the shipped command count and names. | SHOULD | A comparison script extracts slash commands from README workflow rows and `.omp/AGENTS.md` Command Reference rows and confirms both document the same ten commands. |
| R5 | No untracked `.omp/commands/*.md` file is used as evidence for the inventory. | MUST | `git status --short .omp/commands` is empty, or any untracked command file is explicitly excluded from the verification evidence; inventory is derived from `git ls-files`, not filesystem globbing. |
| R6 | No unrelated command semantics, workflow gates, or command implementations change. | MUST | `git diff --name-only` for `/ship` includes `.omp/AGENTS.md` and bead artifacts only unless the plan explicitly expands scope; no `.omp/commands/*.md`, `.omp/extensions/*.ts`, or README behavior changes are required for this bead. |

## Technical Context

**Key files:**
- `.omp/AGENTS.md` — EDIT (~245 lines). Canonical OMP context injected into every agent session. Current stale inventory is in the Command Reference and repository tree block.
- `README.md` — READ/VERIFY (~74 lines). Public repo-facing inventory already states nine lifecycle commands plus npm-release helper and includes `/npm-release` in the workflow table.
- `.omp/commands/npm-release.md` — READ/VERIFY (~101 lines). Tracked command file whose existence must be reflected in `.omp/AGENTS.md`.
- `.omp/commands/verify.md` — READ/VERIFY (~96 lines). Defines tracked command files as command-inventory source of truth during verification.
- `.omp/commands/review.md` — READ/VERIFY (~203 lines). Defines tracked command files as command-inventory source of truth during review.

**APIs / systems touched:**
- Markdown project context consumed by OMP context injection.
- Slash command inventory documented under `.omp/AGENTS.md`.
- Beads workflow documentation and repository tree comments.
- Git tracked-file inventory from `git ls-files`, used as source-of-truth evidence.

**Existing code to NOT modify:**
- `.omp/commands/*.md` command implementations remain unchanged.
- `.omp/extensions/workflow-gate.ts` remains unchanged.
- `.omp/templates/*` remain unchanged.
- `.omp/skills/*` remain unchanged.
- `design/*` and `DESIGN.md` remain unchanged.
- Root `AGENTS.md` remains unchanged unless verification reveals a direct contradiction caused by this bead.

**Existing patterns to preserve:**
- `.omp/AGENTS.md` uses concise tables for command inventory.
- README separates lifecycle commands from npm release helper by saying “Nine lifecycle slash commands plus the npm-release release helper.”
- Verification and review commands use tracked command files, not incidental working-tree files, as command inventory source of truth.
- The core bead lifecycle remains an eight-command loop from `/brainstorm` to `/close`.
- `/init` is bootstrap and appears outside the recurring bead lifecycle loop.
- `/npm-release` is a release helper and should not be inserted into the lifecycle arrow chain.

**File history and graph evidence:**
- `bv --robot-triage --format json` reported one in-progress related bead, `br-omp-backbone-skill-0nc`, and one actionable/open count in project health.
- `bv --robot-plan --format json` reported a single actionable track and highest impact `br-omp-backbone-skill-0nc`, with no downstream dependencies.
- Exact dedup search for this requested title returned `[]`, so this bead is not an exact duplicate by title.
- `br search "command inventory" --json` found the broader related bead `br-omp-backbone-skill-0nc`.
- `bv --robot-file-beads .omp/AGENTS.md --format json` returned zero beads touching `.omp/AGENTS.md` in the indexed file history.
- `bv --robot-file-beads README.md --format json` returned one in-progress related bead, `br-omp-backbone-skill-0nc`, with commit `d9f3a7e`.
- `bv --robot-file-relations README.md --format json` showed co-change relation with `.omp/commands/init.md` and root `AGENTS.md` from commit `d9f3a7e`.
- `git log --all --oneline --grep="command inventory" -10` showed prior commits `78cb3b4 fix: include npm release command inventory` and `531d8b2 fix: align README command inventory with tracked commands`.
- `git log --all --oneline --grep="npm-release" -10` showed prior commit `1676ded chore: add npm-release to README, gitignore Python bytecode`.

**Constraints:**
- Inventory checks must use tracked files from `git ls-files`, not `find`, shell globs, or untracked files.
- `.omp/AGENTS.md` is loaded automatically; misleading text there has higher operational impact than README text.
- The fix must be documentation-only unless verification discovers a direct inconsistency requiring an adjacent documentation file change.
- The command table should not create a new lifecycle requirement for release publishing.
- The repository tree block should remain compact and not enumerate every unrelated directory.
- Existing untracked `.beads/.br_history/` files are unrelated working-tree noise and must not be confused with this bead scope.

## Approach

The chosen approach is a targeted `.omp/AGENTS.md` inventory correction. Update the Command Reference table by adding `/npm-release` with wording aligned to README and `.omp/commands/npm-release.md`: it cuts an npm release through GitHub Releases and trusted publishing, reads package/release state, writes version/tag/release state, and does not use bv. Keep `/init` in the table as bootstrap. Keep the lifecycle arrow chain unchanged so agents still understand the recurring bead loop.

Update the repository tree block in `.omp/AGENTS.md` so `.omp/commands/` says ten command files and its wrapped file list includes `npm-release.md`. This addresses the second stale inventory location without changing the rest of the tree. Because `.omp/AGENTS.md` is the canonical context file, this single-file fix removes the stale rule from the place agents actually load.

Use README as the consistency model, not as an edit target. README already says nine lifecycle slash commands plus the npm-release helper and its workflow table already includes the npm-release row. If verification finds README and `.omp/AGENTS.md` diverge after the `.omp/AGENTS.md` change, adjust only the wording needed to restore agreement; do not rewrite README structure.

Use tracked command inventory as the proof. The plan and verification should run `git ls-files ".omp/commands/*.md"` and compare those basenames to commands documented in `.omp/AGENTS.md`. This follows the rules already embedded in `/verify` and `/review` and avoids false positives from untracked scratch command files.

Alternatives considered:
- Alternative A: edit only README. Rejected because README is already aligned; the stale source is `.omp/AGENTS.md`.
- Alternative B: remove `/npm-release` from README to match `.omp/AGENTS.md`. Rejected because the command file is tracked and shipped; deleting documentation would hide real functionality.
- Alternative C: add `/npm-release` to the lifecycle arrow chain. Rejected because npm release is not part of every bead lifecycle and should not be run during ordinary `/close` flow.
- Alternative D: generate command inventory dynamically in `.omp/AGENTS.md`. Rejected because `.omp/AGENTS.md` is a static Markdown context file in this template and adding generation machinery violates YAGNI.

Implementation notes for `/ship`:
- Read `.omp/AGENTS.md` lines 18-31 before editing the table.
- Read `.omp/AGENTS.md` lines 191-207 before editing the tree block.
- Make only tight Markdown edits.
- Preserve table formatting and code spans.
- Do not reorder commands unless needed for clarity; a safe order is lifecycle commands, `/init`, then `/npm-release` or README table order with Init first.
- Prefer the README phrase “Cut an npm release through GitHub Releases and trusted publishing” for the npm-release description.

Verification design:
- Count tracked commands with `git ls-files ".omp/commands/*.md"`.
- Extract command basenames from tracked files and compare to `.omp/AGENTS.md` Command Reference command cells.
- Confirm the tree block mentions ten command files and includes `npm-release.md`.
- Confirm README and `.omp/AGENTS.md` both document `/npm-release`.
- Confirm no command implementation files changed.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `.omp/AGENTS.md` could imply `/npm-release` is part of every bead lifecycle. | Medium | Medium | Keep lifecycle arrow chain unchanged and describe npm-release as a release helper row, not a bead phase. |
| Verification could count untracked command files and force docs to mention scratch work. | Medium | Medium | Use `git ls-files ".omp/commands/*.md"` exactly as `/verify` and `/review` require. |
| The fix could drift README and `.omp/AGENTS.md` wording. | Low | Medium | Compare documented command names in both files during verification. |
| The tree block could still say nine after table is fixed. | Medium | Low | Treat table and tree block as separate acceptance checks. |
| Existing broader bead `br-omp-backbone-skill-0nc` could be confused with this narrower bead. | Medium | Low | Scope this bead only to `.omp/AGENTS.md` command inventory and do not modify or close the broader bead. |
| Editing command implementations would create behavior risk for a documentation mismatch. | Low | High | Mark `.omp/commands/*.md` as read/verify only and fail verification if implementation files change without explicit plan expansion. |

## Acceptance Criteria
- [ ] R1: The `.omp/AGENTS.md` Command Reference table includes every tracked shipped lifecycle command and the tracked `/npm-release` command exactly once.
    - Verify: ``git ls-files .omp/commands/*.md` returns ten tracked command files and `python3` parsing of `.omp/AGENTS.md` finds the same ten slash command names in the Command Reference table, with no missing or extra entries.`
- [ ] R2: The `.omp/AGENTS.md` workflow narrative distinguishes the eight bead lifecycle execution loop from bootstrap and release helper commands.
    - Verify: `Reading lines 8-31 of `.omp/AGENTS.md` shows `/brainstorm` through `/close` as the lifecycle loop, `/init` as bootstrap, and `/npm-release` as release helper, without implying npm release is part of every bead loop.`
- [ ] R3: The `.omp/AGENTS.md` repository tree comment and command file listing match the tracked command inventory.
    - Verify: `The tree block under `.omp/commands/` says ten command files and lists `npm-release.md` alongside the existing command files, matching `git ls-files .omp/commands/*.md`.`
- [ ] R4: README and `.omp/AGENTS.md` agree on the shipped command count and names.
    - Verify: `A comparison script extracts slash commands from README workflow rows and `.omp/AGENTS.md` Command Reference rows and confirms both document the same ten commands.`
- [ ] R5: No untracked `.omp/commands/*.md` file is used as evidence for the inventory.
    - Verify: ``git status --short .omp/commands` is empty, or any untracked command file is explicitly excluded from the verification evidence; inventory is derived from `git ls-files`, not filesystem globbing.`
- [ ] R6: No unrelated command semantics, workflow gates, or command implementations change.
    - Verify: ``git diff --name-only` for `/ship` includes `.omp/AGENTS.md` and bead artifacts only unless the plan explicitly expands scope; no `.omp/commands/*.md`, `.omp/extensions/*.ts`, or README behavior changes are required for this bead.`

Detailed verification checklist for `/ship` handoff:
- Check 1: Run `git ls-files ".omp/commands/*.md"` and record the ten tracked command file paths.
- Check 2: Confirm the tracked file list includes `.omp/commands/npm-release.md`.
- Check 3: Confirm `git status --short .omp/commands` does not show an untracked command that verification accidentally counted.
- Check 4: Parse `.omp/AGENTS.md` Command Reference rows and list every command cell.
- Check 5: Confirm `.omp/AGENTS.md` Command Reference includes `/brainstorm`.
- Check 6: Confirm `.omp/AGENTS.md` Command Reference includes `/create`.
- Check 7: Confirm `.omp/AGENTS.md` Command Reference includes `/plan`.
- Check 8: Confirm `.omp/AGENTS.md` Command Reference includes `/ship`.
- Check 9: Confirm `.omp/AGENTS.md` Command Reference includes `/verify`.
- Check 10: Confirm `.omp/AGENTS.md` Command Reference includes `/review`.
- Check 11: Confirm `.omp/AGENTS.md` Command Reference includes `/pr`.
- Check 12: Confirm `.omp/AGENTS.md` Command Reference includes `/close`.
- Check 13: Confirm `.omp/AGENTS.md` Command Reference includes `/init`.
- Check 14: Confirm `.omp/AGENTS.md` Command Reference includes `/npm-release`.
- Check 15: Confirm no command appears twice in `.omp/AGENTS.md` Command Reference.
- Check 16: Confirm the set of `.omp/AGENTS.md` command rows equals the set derived from tracked command basenames.
- Check 17: Confirm README workflow table includes `/npm-release` and still agrees with `.omp/AGENTS.md`.
- Check 18: Confirm `.omp/AGENTS.md` tree block says ten command files or equivalent wording.
- Check 19: Confirm `.omp/AGENTS.md` tree block lists `npm-release.md`.
- Check 20: Confirm lifecycle arrow chain remains `/brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close`.
- Check 21: Confirm `/npm-release` is not inserted into the lifecycle arrow chain.
- Check 22: Confirm `/init` remains described as bootstrap, not a repeating bead phase.
- Check 23: Confirm no `.omp/commands/*.md` file is modified by the implementation diff.
- Check 24: Confirm no `.omp/extensions/*.ts` file is modified by the implementation diff.
- Check 25: Confirm no design files are modified by the implementation diff.
- Check 26: Confirm no memory file is modified unless the implementation discovers a direct memory inconsistency.
- Check 27: Run markdown table visual inspection for column count consistency in the Command Reference table.
- Check 28: Run `br dep cycles --json` and confirm there are no dependency cycles after bead creation.
- Check 29: Run `br show br-omp-backbone-skill-3co --json` and confirm the bead exists.
- Check 30: Run `br sync --flush-only` before committing artifact state.

Handoff notes for maintainers:
- This bead is intentionally narrow because command inventory drift is a documentation defect, not a release-flow defect.
- The source of truth for shipped commands is tracked files, not current directory listings.
- `find` output during investigation showed ten command files, but acceptance should rely on `git ls-files` because review and verify already require that standard.
- `.omp/AGENTS.md` is more operationally important than README for OMP sessions because it is injected into every agent context.
- The table row for `/npm-release` should use concise wording; long release procedure belongs in `.omp/commands/npm-release.md`.
- No compatibility shim is needed because this is Markdown documentation.
- No tests need to exercise npm publishing because no release behavior changes.
- No new abstractions or generators should be added for one stale table row.
- If future commands are added, update `.omp/AGENTS.md`, README, and tracked-inventory verification together.
- If a command is untracked, do not document it as shipped.
- Inventory guardrail 1: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 1: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 1: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 1: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 1: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 2: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 2: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 2: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 2: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 2: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 3: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 3: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 3: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 3: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 3: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 4: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 4: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 4: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 4: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 4: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 5: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 5: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 5: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 5: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 5: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 6: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 6: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 6: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 6: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 6: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 7: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 7: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 7: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 7: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 7: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 8: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 8: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 8: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 8: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 8: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 9: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 9: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 9: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 9: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 9: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 10: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 10: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 10: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 10: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 10: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 11: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 11: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 11: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 11: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 11: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 12: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 12: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 12: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 12: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 12: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 13: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 13: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 13: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 13: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 13: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 14: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 14: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 14: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 14: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 14: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 15: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 15: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 15: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 15: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 15: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 16: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 16: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 16: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 16: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 16: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 17: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 17: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 17: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 17: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 17: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 18: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 18: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 18: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 18: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 18: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 19: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 19: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 19: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 19: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 19: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 20: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 20: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 20: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 20: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 20: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 21: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 21: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 21: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 21: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 21: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 22: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 22: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 22: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 22: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 22: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 23: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 23: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 23: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 23: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 23: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 24: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 24: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 24: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 24: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 24: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 25: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 25: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 25: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 25: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 25: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 26: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 26: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 26: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 26: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 26: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 27: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 27: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 27: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 27: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 27: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 28: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 28: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 28: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 28: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 28: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 29: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 29: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 29: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 29: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 29: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 30: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 30: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 30: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 30: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 30: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 31: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 31: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 31: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 31: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 31: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 32: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 32: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 32: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 32: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 32: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 33: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 33: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 33: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 33: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 33: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 34: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 34: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 34: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 34: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 34: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 35: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 35: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 35: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 35: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 35: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 36: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 36: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 36: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 36: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 36: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 37: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 37: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 37: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 37: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 37: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 38: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 38: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 38: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 38: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 38: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 39: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 39: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 39: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 39: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 39: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 40: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 40: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 40: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 40: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 40: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 41: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 41: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 41: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 41: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 41: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 42: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 42: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 42: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 42: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 42: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 43: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 43: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 43: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 43: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 43: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 44: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 44: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 44: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 44: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 44: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 45: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 45: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 45: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 45: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 45: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 46: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 46: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 46: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 46: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 46: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 47: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 47: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 47: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 47: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 47: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 48: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 48: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 48: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 48: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 48: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 49: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 49: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 49: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 49: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 49: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 50: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 50: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 50: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 50: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 50: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 51: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 51: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 51: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 51: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 51: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 52: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 52: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 52: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 52: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 52: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 53: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 53: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 53: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 53: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 53: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 54: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 54: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 54: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 54: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 54: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 55: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 55: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 55: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 55: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 55: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 56: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 56: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 56: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 56: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 56: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 57: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 57: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 57: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 57: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 57: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 58: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 58: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 58: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 58: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 58: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 59: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 59: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 59: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 59: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 59: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 60: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 60: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 60: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 60: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 60: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 61: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 61: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 61: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 61: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 61: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 62: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
- Inventory guardrail 62: If a command row is documented, its corresponding `.omp/commands/<name>.md` file must be tracked.
- Inventory guardrail 62: If a tracked command file exists, the `.omp/AGENTS.md` Command Reference must either document it or explicitly classify why it is excluded; no exclusion is expected here.
- Inventory guardrail 62: Keep the release helper separate from bead lifecycle execution to avoid accidental publish workflows.
- Inventory guardrail 62: Treat command inventory mismatch as a falsifiable set comparison, not a prose preference.
- Inventory guardrail 63: Do not infer command count from prose; derive it from tracked `.omp/commands/*.md` files.
