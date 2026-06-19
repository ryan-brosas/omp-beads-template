# Context Capsule: br-omp-backbone-skill-3co

## Objective

Update the canonical `.omp/AGENTS.md` command inventory so it matches the ten tracked shipped command files, including `.omp/commands/npm-release.md`, while preserving the normal eight-command bead lifecycle loop and keeping `/npm-release` documented as a release helper rather than a required bead phase.

## Key Patterns

- **Tracked inventory source of truth** — Use tracked `.omp/commands/*.md` files as the shipped command set, not incidental working-tree files. Reference: `.omp/commands/verify.md` lines 54-67 and `.omp/commands/review.md` lines 67-79.
- **Lifecycle versus helper commands** — Keep `/brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close` as the recurring bead loop. Reference: `.omp/AGENTS.md` workflow section.
- **README wording model** — README already says nine lifecycle slash commands plus npm-release release helper and includes the `/npm-release` row. Reference: `README.md` workflow table.
- **Release command semantics** — `/npm-release` cuts npm releases through GitHub Releases and trusted publishing. Reference: `.omp/commands/npm-release.md` purpose section.
- **Narrow documentation correction** — The defect is stale canonical context, not missing release implementation. Reference: PRD problem and scope.

## Constraints

1. MUST edit `.omp/AGENTS.md` only for production documentation unless verification proves a direct adjacent documentation contradiction.
2. MUST include `/npm-release` exactly once in the `.omp/AGENTS.md` Command Reference table.
3. MUST update the `.omp/AGENTS.md` repository tree block from nine to ten command files and include `npm-release.md`.
4. MUST keep the lifecycle arrow chain unchanged and free of `/npm-release`.
5. MUST keep `/init` as bootstrap, not a recurring bead phase.
6. MUST use `git ls-files .omp/commands/*.md` as inventory proof during ship and verify.
7. MUST NOT modify `.omp/commands/*.md` implementations for this bead.
8. MUST NOT modify `.omp/extensions/workflow-gate.ts`.
9. MUST NOT modify root `AGENTS.md` agents.md compliance work.
10. MUST NOT close or mutate broader bead `br-omp-backbone-skill-0nc`.
11. SHOULD leave README unchanged because it is already aligned unless a final comparison proves otherwise.
12. SHOULD fail verification if command rows contain missing, extra, or duplicate command names.

## File Ownership

| Task | Allowed | Forbidden |
|------|---------|-----------|
| 1.1 Capture tracked command inventory | `.omp/commands/*.md` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |
| 1.2 Extract canonical command rows | `.omp/AGENTS.md` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |
| 1.3 Extract README command rows | `README.md` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |
| 1.4 Locate stale tree block | `.omp/AGENTS.md` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |
| 2.1 Add npm-release table row | `.omp/AGENTS.md` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |
| 2.2 Update command tree count | `.omp/AGENTS.md` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |
| 2.3 Preserve lifecycle semantics | `.omp/AGENTS.md` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |
| 3.1 Verify AGENTS inventory equality | `.omp/AGENTS.md`, `.omp/commands/*.md` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |
| 3.2 Verify README agreement | `README.md`, `.omp/AGENTS.md` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |
| 3.3 Verify scope guard | `.omp/AGENTS.md` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |
| 3.4 Verify tree and lifecycle text | `.omp/AGENTS.md` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |
| 4.1 Record implementation evidence | `.beads/artifacts/br-omp-backbone-skill-3co/completion-evidence.json` | All other files; especially `.omp/commands/*.md`, `.omp/extensions/*.ts`, design files, memory files, and unrelated bead artifacts unless explicitly read-only. |

## Graph Context

- **Blast radius:** 1 production documentation edit, `.omp/AGENTS.md`; no production creates or deletes.
- **Planning artifacts:** `plan.md`, `tasks.md`, and `context-capsule.md` under this bead directory.
- **Related beads:** `br-omp-backbone-skill-0nc` appears as a separate in-progress track and must remain out of scope.
- **Dependency tree:** single root node for `br-omp-backbone-skill-3co`; no parent blocker reported.
- **Forecast:** 52 minutes at confidence 0.5 from bv robot forecast.
- **Graph metrics:** insights status reported computed for PageRank, Betweenness, Eigenvector, HITS, Critical, Cycles, KCore, Articulation, and Slack.
- **Cycles:** insight output reported null cycles; final verify still runs `br dep cycles --json`.
- **Hotspots touched:** no file with more than three bead-history links; listed hotspots had one bead each and did not make `.omp/AGENTS.md` a high-risk hotspot.
- **Tracked command inventory:** brainstorm, close, create, init, npm-release, plan, pr, review, ship, verify.
- **Command status:** `git status --short .omp/commands` produced no output during planning.
