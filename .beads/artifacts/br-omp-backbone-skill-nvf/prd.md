# PRD: Fix /init hydration: project name precedence, goal auto-fill, conventions over-inference

## Summary

- Bead: br-omp-backbone-skill-nvf
- Owner: makora1
- Status: in_progress
- Parent: br-omp-backbone-skill-9tl (Teach /init to hydrate memory/project files from repo state)

## Problem

The `/init` command's Phase 2.5 hydration script (`.omp/commands/init.md`, Python embedded block) has three review findings that deviate from the original PRD intent:

### 1. Project name precedence is wrong

**Current behavior:** Line 169-175 — the `project_name` fallback chain is `README heading → package.json name → git remote name → directory name`. README takes highest priority.

**Expected behavior (per PRD):** The git remote name should be the primary source. The PRD's stated intent was "hydrate from repo state" — the git remote is the canonical identifier of what the repo *is*, while README headings are prose that may not match the actual project identity. Order should be: `git remote name → package.json name → README heading → directory name`.

### 2. Goal field should not be auto-filled from README

**Current behavior:** Line 176 — `project_desc` is auto-filled from the first paragraph of the README, and line 367 writes this into the "One sentence — what are we building and why?" slot.

**Expected behavior (per PRD):** The goal field is a human-authored slot. Auto-filling it from README prose (which often contains installation instructions, badges, or marketing text in the first paragraph) produces noise, not a clear goal statement. It should remain as `<!-- TODO: fill in your project goal -->` — a deliberate TODO marker that prompts the human to write a precise goal, rather than presuming the README's first paragraph is suitable.

### 3. Conventions hydration over-infers for Frontend and Scripts rows

**Current behavior:** Lines 307-320 — Frontend language/notes and Scripts language/notes are aggressively inferred from the detected backend language. For example, if `language == "TypeScript"`, the Frontend row gets `TypeScript | reuse existing frontend framework conventions` and Scripts gets `TypeScript | package scripts and repo automation`.

**Expected behavior (per PRD):** These are conventions, not tech-stack. Over-inferring from a single detected language creates false precision. The Frontend row should only be populated when there is *actual evidence* of a frontend framework (e.g., React, Svelte, Vue deps in package.json). Scripts language should be conservative — only infer TypeScript for scripts if tsx/ts-node is a dependency; otherwise default to Bash. When evidence is absent, leave placeholders.

## Scope

### In Scope
- `.omp/commands/init.md` — Phase 2.5 Python block (lines ~169-176, ~307-320): fix project name precedence, goal auto-fill, and conventions over-inference
- `br-omp-backbone-skill-nvf` bead artifacts only

### Out of Scope
- Other init.md phases (Phase 1, 2, 3, 4) — no changes
- Memory file templates (`.omp/templates/`) — no changes
- br/bv commands, workflow gate, extensions — no changes
- New dependencies — none introduced

## Technical Context

**Key files:**
- `.omp/commands/init.md` — EDIT (~539 lines, Phase 2.5 Python block at lines 36-539)
- `.beads/artifacts/br-omp-backbone-skill-nvf/prd.md` — READ (this file)

**APIs / systems touched:**
- `/init` command hydration script (embedded Python in init.md)
- Memory file template substitution for `project.md` and `conventions.md`

**Existing code to NOT modify:**
- Phases 1, 2, 3, 4 of init.md
- Memory file templates (`.omp/templates/`)
- Backend/tech-stack/gotchas/decisions hydration logic (lines ~290-540)

## Approach

**Change 1 — Project name precedence (line 169-175):** Reorder the fallback chain so `git_remote_name()` is tried first, then `package_name`, then `first_heading_from_readme()`, then `root.name`, then `"Untitled Project"`. This is a simple reordering of the `or` chain — no new functions needed.

**Change 2 — Goal/description auto-fill (line 176):** Replace `first_paragraph_from_readme() or "<!-- TODO: fill in your project goal -->"` with just `"<!-- TODO: fill in your project goal -->"` — always the TODO marker, never auto-filled. This is a one-line change.

**Change 3 — Conservative conventions hydration (lines 307-320):** Replace the current language-based heuristic with evidence-based detection:
- `frontend_language`: check `package.json` deps for react, svelte, vue, next, nuxt, astro, angular, solid. Map each to the correct language (e.g., react→TypeScript/JavaScript based on tsconfig). If none detected, use `<!-- TODO: fill in -->`.
- `frontend_notes`: only populated when frontend_language is not a TODO marker.
- `scripts_language`: check for `tsx` or `ts-node` in package.json deps → TypeScript. Otherwise default to Bash.
- `scripts_notes`: populated when scripts_language is TypeScript ("package scripts and repo automation"). Otherwise default to "repo automation and one-offs" for Bash.

## Outcome

The `/init` hydration script is corrected so that:
1. Project name derivation uses git-remote-first precedence.
2. The goal/description field is a human-only TODO marker, never auto-filled.
3. Conventions Frontend/Scripts rows are only populated when concrete evidence exists; otherwise they remain placeholder-marked for human review.

## Acceptance Criteria

- [ ] In `init.md` Phase 2.5 Python block: `project_name` fallback chain is `git_remote_name() → package_json.name → first_heading_from_readme() → root.name → "Untitled Project"`
- [ ] In `init.md` Phase 2.5 Python block: `project_desc` always resolves to `<!-- TODO: fill in your project goal -->` (no README auto-fill)
- [ ] In `init.md` Phase 2.5 Python block: Frontend row only hydrates when frontend framework deps are detected in `package.json` (react, svelte, vue, next, nuxt, astro, angular, solid)
- [ ] In `init.md` Phase 2.5 Python block: Scripts language infers TypeScript only when `tsx` or `ts-node` is a dependency; otherwise defaults to Bash
- [ ] Conventions rows for Frontend/Scripts leave `<!-- TODO: fill in -->` when evidence is absent
- [ ] Existing correct hydration (Backend, tech-stack, gotchas, decisions) is unchanged
- [ ] The script remains idempotent — re-running `/init` on an already-hydrated repo does not overwrite user edits

## Constraints

- Changes are scoped to the Python embedded block in `.omp/commands/init.md`, Phase 2.5
- No changes to the init command structure, other phases, or memory file templates
- Must preserve idempotency: only replace exact template placeholders, never overwrite user-populated fields
- Must not introduce new dependencies

## Risks

- **Low**: Changing project name precedence could change the heading on already-initialized repos if `/init` is re-run. Mitigation: the existing already-populated guard means previously hydrated files are left alone.
- **Low**: Conservative conventions hydration means more TODO markers for humans to fill. Mitigation: this is intentional — false precision is worse than a TODO marker.
