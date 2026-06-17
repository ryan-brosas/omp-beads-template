# Review Report

## Summary
Reviewed the `/init` hydration implementation in `.omp/commands/init.md` against the PRD and the recorded `/verify` evidence for bead `br-omp-backbone-skill-9tl`.

The new Phase 2.5 hydration flow is real, clearly separated, and appears operational: it hydrates all five memory files, removes the major template placeholders, preserves gotchas/decisions content, and is safe to rerun.

However, the implementation still does not fully satisfy the PRD. The main gaps are:
- project name precedence does not match the required git-remote-first behavior
- the project goal is auto-filled from README content even though the PRD marks that field as human-only
- conventions inference is more aggressive than the PRD example, especially for Frontend and Scripts rows

## Reviewed Artifacts
- `.omp/commands/init.md`
- `.beads/artifacts/br-omp-backbone-skill-9tl/prd.md`
- `.beads/artifacts/br-omp-backbone-skill-9tl/completion-evidence.json`
- `git diff -- .omp/commands/init.md`

## What Matches the PRD
- A distinct `Phase 2.5: Hydrate Memory Files` section was added in the right place, between `br init` and Honcho configuration.
- Hydration is implemented inline in `init.md` as an embedded Python block, matching the PRD constraint to avoid standalone scripts.
- The flow updates all five files under `.omp/memory/project/`.
- The implementation is idempotent at the placeholder level: it replaces exact template strings and leaves already-edited fields alone.
- Gotchas and decisions content is preserved apart from project-name heading replacement.
- Phase 5 now verifies hydration results rather than only checking file presence.

## Findings

### 1. Project name precedence does not match the PRD
**Severity:** Major

The PRD specifies project name detection from git remote URL with directory-name fallback. The implementation instead prefers:
1. README H1
2. `package.json` name
3. git remote name
4. directory name

Evidence:
- `init.md` lines 169-173 build `project_name` from `first_heading_from_readme() or package_name or git_remote_name() or root.name`
- `completion-evidence.json` requirement 1 is marked `partial`
- Verification scenario `remote + package.json and no README` hydrated `# Project: pkg-name-ignored` instead of using the remote-derived name

Impact:
- Hydrated project identity can diverge from the repository identity required by the PRD.
- Honcho workspace naming now inherits this altered precedence via Phase 3.

### 2. Human-only goal field is incorrectly auto-filled from README
**Severity:** Major

The PRD explicitly says the goal, success criteria, and milestones should remain TODO markers for human judgment. The implementation fills the project goal from the first README paragraph when available.

Evidence:
- `init.md` line 176 sets `project_desc = first_paragraph_from_readme() or "<!-- TODO: fill in your project goal -->"`
- `completion-evidence.json` requirement 9 is marked `fail`
- Verification scenario `scenario_readme_goal_autofill` shows `project.md` goal content became README prose instead of a TODO marker

Impact:
- The command writes inferred prose into a field the PRD reserves for explicit human judgment.
- This weakens the intended signal that project goals must be consciously set by the user.

### 3. Conventions inference exceeds the PRD example
**Severity:** Moderate

The PRD example expects uncertain conventions rows to remain TODO, especially Frontend, and expects Scripts to default to Bash in the TypeScript-only example. The implementation infers more than the PRD describes.

Evidence:
- `init.md` sets `frontend_language = "TypeScript"` when the detected language is TypeScript
- `init.md` sets `scripts_language = "TypeScript"` for TypeScript and JavaScript repos
- `completion-evidence.json` requirement 5 is `pass_with_deviation`
- Verification evidence shows rows became:
  - `| Frontend | TypeScript | reuse existing frontend framework conventions |`
  - `| Scripts | TypeScript | package scripts and repo automation |`

Impact:
- The hydrated conventions file can imply frontend and scripts conventions that were not actually detected.
- This is directionally useful, but it does not align with the more conservative PRD behavior.

## Risks Checked
- **Idempotency:** Verified by `/verify` evidence; rerun preserved a manually edited project goal and reported `hydrated=0 already_populated=5`.
- **Placeholder cleanup:** `/verify` reports zero remaining `<project-name>` placeholders across the five files in the TypeScript/pnpm scenario.
- **Template preservation:** Gotchas row count remained 12 and decision example row count remained 5 after hydration.
- **Workflow placement:** Phase 2.5 is correctly placed before Honcho workspace derivation, and Phase 3 now reads the hydrated project heading.

## Verdict
**Changes requested.**

The hydration mechanism is present and mostly sound, but the implementation is not yet fully compliant with the PRD. Before this bead should pass review, I recommend:
- changing project-name precedence to `git remote -> directory name` per PRD
- removing README-based auto-fill for the project goal so human-only fields stay as TODO markers
- making conventions hydration more conservative for Frontend and Scripts rows where the repo state does not directly prove those choices
