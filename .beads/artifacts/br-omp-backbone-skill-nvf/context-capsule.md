# Context Capsule: br-omp-backbone-skill-nvf

## Objective

Fix the `/init` Phase 2.5 memory hydration script in `.omp/commands/init.md` so it matches the PRD and review findings: project name detection must prefer the git remote over README prose, project goal hydration must remain a human-authored TODO marker, and Frontend/Scripts rows in `conventions.md` must be populated only from direct evidence instead of backend-language guesses. The shipping change is intentionally small: one source file edit inside the embedded Python block, with no template changes, no dependency changes, and no changes to Honcho, br, bv, design, or memory-file content outside what `/init` would generate in a temporary verification harness.

## Key Patterns

- **Exact-placeholder idempotency** — `replace_exact(text, old, new)` only replaces known template strings. Preserve every `replace_exact` call; change only the variable values feeding project and conventions replacements. Reference: ``.omp/commands/init.md:68-69` and `.omp/commands/init.md:362-397``.
- **Repo-state identity first** — `git_remote_name()` already parses origin URLs and returns the repository name. Use it before package name and README heading in `project_name`. Reference: ``.omp/commands/init.md:149-176``.
- **Human goal field** — `project_desc` should always be `<!-- TODO: fill in your project goal -->`. README paragraphs are not authoritative goals. Reference: ``.omp/commands/init.md:176``.
- **Evidence-gated conventions** — Frontend and Scripts rows describe conventions, not detected backend stack. Populate them only from direct package dependency evidence. Reference: ``.omp/commands/init.md:300-320``.
- **Backend untouched** — `backend_notes` and language detection are already correct for this bead. Do not refactor them while fixing Frontend/Scripts. Reference: ``.omp/commands/init.md:208-306``.
- **Verification dictionaries untouched** — `verification_typecheck`, `verification_lint`, `verification_test`, `verification_build`, and `security_audit` are not part of the review findings. Reference: ``.omp/commands/init.md:322-360``.

## Constraints

1. MUST edit only `.omp/commands/init.md` during `/ship` source implementation.
2. MUST keep source changes inside `## Phase 2.5: Hydrate Memory Files` unless a syntax extraction boundary needs a comment-free adjustment, which is not expected.
3. MUST preserve all `replace_exact` calls so already-populated memory files are not overwritten.
4. MUST keep project goal as the exact string `<!-- TODO: fill in your project goal -->`.
5. MUST use git remote, package name, README heading, root directory, then `"Untitled Project"` for project name precedence.
6. MUST require frontend framework package evidence before populating Frontend language or notes.
7. MUST recognize the PRD frontend package names: react, svelte, vue, next, nuxt, astro, angular, solid.
8. MUST require `tsx` or `ts-node` dependency evidence before Scripts language becomes TypeScript.
9. MUST use Bash as the conservative Scripts language fallback when TypeScript runner evidence is absent.
10. MUST keep Scripts notes as TODO when runner evidence is absent.
11. MUST NOT change `.omp/templates/` files.
12. MUST NOT change `.omp/memory/project/` files as part of implementation; use temporary directories for behavior checks.
13. MUST NOT add Python imports or package dependencies.
14. MUST NOT alter Phase 1, Phase 2 br init, Phase 3 Honcho config, Phase 4 verification text, Phase 5 hydration result checks, or Phase 6 report text unless the user separately asks.
15. MUST NOT infer Frontend from TypeScript backend alone.
16. MUST NOT infer Scripts from Python, Go, Rust, JavaScript, or TypeScript backend language alone.
17. SHOULD keep the diff boring and reviewable: one fallback reorder, one assignment simplification, one dependency helper, one Frontend gate, one Scripts gate.
18. SHOULD use a behavior harness instead of executing `/init` against this repository memory files.
19. SHOULD fail verification on any unintended `.omp/memory/project/` mutation.
20. SHOULD leave `first_paragraph_from_readme()` in place unless removing it is proven safe and kept within scope; the one-line assignment change is preferred.

## File Ownership

| Task | Allowed | Forbidden |
|------|---------|-----------|
| 1.1 | `.omp/commands/init.md` read-only ranges 149-176, 282-320, 362-397 | Edits to any file |
| 1.2 | `.omp/commands/init.md` read-only invariant anchors | Edits to any file |
| 2.1 | `.omp/commands/init.md` `project_name = (` expression only | `git_remote_name()`, README parser functions, package parser, other phases |
| 2.2 | `.omp/commands/init.md` `project_desc =` assignment only | `replace_exact` calls, success criteria placeholders, current phase placeholders |
| 3.1 | `.omp/commands/init.md` one dependency helper near package-derived values | New imports, new file reads, merged dependency caches, package files |
| 3.2 | `.omp/commands/init.md` Frontend variable computation only | Frontend `replace_exact` call, Backend block, templates |
| 3.3 | `.omp/commands/init.md` Scripts variable computation only | `package_script()`, verification dictionaries, Backend block, templates |
| 4.1 | No source edits; syntax-check command only | Executing hydration against repo memory files |
| 4.2 | Temporary harness files outside repo or in system temp only | Persistent repo memory-file mutations |
| 4.3 | Verification commands and bead artifacts only | Unrelated cleanup, design files, Honcho config, br/bv implementation |

## Graph Context

- **Blast radius:** 4 files in this phase bundle (0 new, 4 edits, 0 deletes): three bead artifacts now, one source file during `/ship`.
- **Implementation blast radius:** `.omp/commands/init.md` only. The changed regions are the Phase 2.5 Python assignments around current lines 169-176 and 307-320 plus one nearby helper.
- **Related beads:** 1 named in PRD context, `br-omp-backbone-skill-9tl`; current `br dep tree` for this bead has no dependency edges.
- **File history:** `bv --robot-file-hotspots --format json` returned no tracked hotspots, no file links, and no files with multiple beads. The PRD still identifies `.omp/commands/init.md` as sensitive because it is the init command.
- **Hotspots touched:** None reported by bv. Treat `.omp/commands/init.md` with care because command docs are executable recipes.
- **Parallel tracks:** `bv --robot-plan --format json` returned one track, `track-A`, containing only this bead. Inside the bead, tasks are serial because they touch the same file.
- **Forecast:** 98 minutes at confidence 0.4 from `bv --robot-forecast`; bead estimate is 60 minutes. Keep implementation direct; do not expand scope to close the forecast gap.
- **Cycles:** `bv --robot-insights` reported cycle analysis computed and no cycles; `br dep cycles --json` must still be run after artifact writes.
- **Critical path:** No downstream unblock effect. Completing this bead fixes review drift but does not unlock other graph work according to bv.
- **Shipping reminder 64** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 65** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 66** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 67** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 68** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 69** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 70** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 71** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 72** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 73** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 74** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 75** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 76** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 77** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 78** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 79** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 80** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 81** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 82** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 83** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 84** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 85** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 86** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 87** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 88** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 89** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 90** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 91** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 92** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 93** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 94** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 95** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 96** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 97** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 98** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 99** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 100** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 101** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 102** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 103** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 104** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 105** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 106** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 107** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 108** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 109** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 110** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 111** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 112** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 113** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 114** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 115** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 116** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 117** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 118** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 119** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 120** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 121** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 122** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 123** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 124** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 125** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 126** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 127** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 128** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 129** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 130** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 131** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 132** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 133** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 134** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 135** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 136** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 137** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 138** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 139** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 140** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 141** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 142** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 143** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 144** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 145** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 146** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 147** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 148** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 149** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 150** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 151** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 152** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 153** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 154** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 155** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 156** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 157** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 158** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 159** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 160** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 161** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 162** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 163** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 164** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 165** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 166** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 167** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 168** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
- **Shipping reminder 169** — If a proposed edit is not needed for project name precedence, static project goal, frontend evidence, scripts evidence, idempotency, or verification, leave it out.
