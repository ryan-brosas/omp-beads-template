# Context Capsule: br-omp-backbone-skill-9tl

## Objective

Replace `/init` Phase 5 ("Check Agent Files") with a multi-step hydration phase that detects project identity from repo state (README.md, git remote, lockfiles) and rewrites placeholder text in the 5 memory files under `.omp/memory/project/` with concrete, repo-derived content. This eliminates the ~1KB of template placeholder text that agents read every session and makes the template immediately useful after bootstrap.

## Key Patterns

- **Shell-only detection** — No Python, no package manager invocation. All detection uses bash builtins + grep + sed + awk + git + ls. This keeps `/init` portable and fast (<1 second). Reference: `.omp/commands/init.md` for existing Phase 1-4 patterns (bash-detectable phases with `## Phase N:` headings and fenced code blocks).
- **Idempotency via grep guard** — Before hydrating any file, check `grep -q '<[a-z]' <file>`. If no angle-bracket patterns remain, the file is treated as user-authored and skipped. This prevents `/init` from overwriting user edits on re-run. Reference: `.omp/memory/project/project.md` for placeholder patterns (`<project-name>`, `<what are we building>`, `<active | maintenance | paused>`, `<Criterion 1>`).
- **Three-tier fallback for project name** — README.md h1 (strip markdown link syntax) → git remote origin URL (extract repo name, strip `.git`) → directory basename → "Untitled Project". Reference: `README.md` line 1 (`# OMP Beads Template`).
- **Language detection priority chain** — TypeScript (package.json + tsconfig.json) > TypeScript/Node.js (package.json alone) > Go (go.mod) > Python (pyproject.toml or requirements.txt) > Rust (Cargo.toml) > placeholder comments. Second-order refinement: `tsconfig.json` presence upgrades "TypeScript/Node.js" to "TypeScript". Reference: current repo has `package.json` but no `tsconfig.json` → would detect "TypeScript/Node.js".
- **Sed escaping discipline** — Use `|` as delimiter instead of `/` when substituting file paths or URLs. Escape `&` in variables with `\&` before sed. Test with project names containing `/` and `&`. Reference: existing sed usage in init.md Phase 3 (Honcho `.env` block uses Python, not sed — our hydration uses sed, not Python).
- **Phase structure convention** — Each phase has a `## Phase N: Name` heading. Sub-phases use `### N.M: Name`. Code blocks use triple-backtick \`\`\`bash. Phases run sequentially in the same shell context (variables persist). Reference: existing init.md Phase 1-6 structure.
- **Workflow gate exemption** — The gate (`.omp/extensions/workflow-gate.ts`) already exempts paths starting with `.omp/` via `path.startsWith(".omp/")`. Memory files at `.omp/memory/project/*.md` are automatically exempt. No gate changes needed. Reference: workflow-gate.ts lines checking `path.startsWith(".omp/")`.

## Constraints

1. **Do NOT modify any file except `.omp/commands/init.md`.** The memory files are runtime hydration targets — they ship with placeholders and get hydrated when `/init` runs. Do not edit them during implementation.
2. **Do NOT modify `.omp/templates/`.** Those are bead artifact templates (prd.md, plan.md, tasks.md, etc.) — unrelated to init hydration.
3. **Do NOT invoke package managers or runtimes.** No `node --version`, `npm --version`, `go version`, `python3 --version`, `cargo --version`, or `rustc --version`. Version columns get `<!-- run ... -->` comments pointing the user to run these manually.
4. **Do NOT create new commands or skills.** Hydration lives entirely within `/init`. No `/hydrate-memory` command. No new skill files.
5. **Do NOT change Phases 1-4 or Phase 6 structure.** Only Phase 5 is replaced. Phase 6 (Report) gets one new line for memory statistics.
6. **Do NOT delete template decisions or gotchas.** The 5 template decisions (br/bv, commands+skills, bare names, .omp/ root, separate tooling) and the 12 template bootstrap gotchas are preserved. They are real architectural context, not placeholders.
7. **Do NOT implement anything outside the bead scope.** No "while you're in here" cleanups. No touching README.md, .omp/AGENTS.md, .omp/RULES.md, or any other file.
8. **Keep init.md under 220 lines.** The current file is ~120 lines. The hydration logic adds ~80 lines (detection: ~30, hydration blocks: ~40, scan + report: ~10).

## File Ownership

| Task | Allowed | Forbidden |
|------|---------|-----------|
| 1.1-1.3 (detection) | `.omp/commands/init.md` (write detection snippets) | All other files |
| 2.1-2.5 (hydration blocks) | `.omp/commands/init.md` (write hydration blocks) | All other files |
| 3.1-3.3 (integration) | `.omp/commands/init.md` (replace Phase 5, add Phase 5a, update Phase 6) | All other files |
| 3.4 (gate check) | `.omp/extensions/workflow-gate.ts` (read-only verification) | Do not edit |
| 4.1-4.4 (verification) | `.omp/memory/project/*.md` (read-only, or backup/restore for testing) | Do not permanently edit |

## Graph Context

- **Blast radius:** 1 file (0 new, 1 edit, 0 deletes). Only `.omp/commands/init.md` is modified.
- **Related beads:** None. This bead has no dependencies and nothing depends on it.
- **File history:** `.omp/commands/init.md` has zero prior bead history (fresh template file). No merge conflicts, no hotspots.
- **Hotspots touched:** None.

## Implementation Notes

### The 5 memory files and what gets hydrated in each

| File | What changes | What stays |
|------|-------------|------------|
| `project.md` | Heading (project name), description, phase status (→ "active"), milestone text, next deliverable text | Success criteria placeholders (`<Criterion 1>`, etc.) — require domain knowledge |
| `conventions.md` | Heading, backend language row, frontend language row (if TypeScript), scripts row (→ "Bash"), constraint comments | All other convention text (naming rules, workflow steps, git conventions, Honcho protocol) |
| `decisions.md` | Heading, `<YYYY-MM>` date placeholders (→ "2026-06") | All 5 template decision rows (br/bv, commands+skills, bare names, .omp/ root, separate tooling) |
| `tech-stack.md` | Heading, Language row, Runtime row, Package manager row, constraint comments | Verification command placeholders, Key Dependencies table, Security section, Constraints section |
| `gotchas.md` | Heading, demarcation comment above template gotchas section | Template Bootstrap Gotchas table (12 rows), Active Warnings table, "How to Add a Gotcha" section |

### Edge cases the implementation must handle

1. **README.md h1 has markdown links:** `# [Project Name](https://example.com)` → strip link syntax, keep "Project Name"
2. **README.md exists but has no paragraph after h1** (only headings, badges, links) → fallback description comment
3. **PROJECT_NAME or PROJECT_DESC contains `/`:** Use `|` as sed delimiter, not `/`
4. **PROJECT_NAME or PROJECT_DESC contains `&`:** Escape `&` → `\&` before sed (unescaped `&` in sed replacement means "the matched text")
5. **No lockfiles at all:** All language/runtime/pkg-mgr rows get `<!-- ... -->` comment placeholders
6. **Multiple lockfiles (monorepo):** Deterministic priority: TypeScript > Go > Python > Rust. The first match wins. The report notes ambiguity (out of scope for this bead to handle multi-language detection).
7. **gotchas.md comment double-insertion:** Running hydration twice on gotchas.md could insert the demarcation comment twice. Use a marker (e.g., check if comment already exists before inserting) or rely on the idempotency guard (which skips the whole file if no `<[a-z]` patterns remain — but gotchas.md has `<YYYY-MM>` in Active Warnings, so the guard may not protect against double-insertion). **Solution:** Check for the demarcation comment before inserting: `grep -q 'inherited from the omp-template' .omp/memory/project/gotchas.md || sed -i '...'`
8. **sed pattern escaping for `\|` in alternation:** The tech-stack.md table has patterns like `<TypeScript \| Python \| Go \| Rust>`. In shell, `\|` in a sed pattern means literal `|` when using basic regex. These need careful escaping — test that the exact sed commands work against the actual template file.

### Files to read before implementing

1. `.omp/commands/init.md` — current state (~120 lines), locate exact Phase 5 block to replace
2. `.omp/memory/project/project.md` — confirm placeholder patterns for sed matching
3. `.omp/memory/project/conventions.md` — confirm table structure for language row sed
4. `.omp/memory/project/decisions.md` — confirm `<YYYY-MM>` patterns and decision row count
5. `.omp/memory/project/tech-stack.md` — confirm `\|` escaping needs in table rows
6. `.omp/memory/project/gotchas.md` — confirm heading structure for demarcation comment insertion point
7. `.omp/extensions/workflow-gate.ts` — confirm `.omp/` path exemption (read-only, no edits planned)
8. `.beads/artifacts/br-omp-backbone-skill-9tl/decisions.md` — design decisions and rejected alternatives
9. `.beads/artifacts/br-omp-backbone-skill-9tl/plan.md` — full wave structure and code outlines
10. `.beads/artifacts/br-omp-backbone-skill-9tl/tasks.md` — step-by-step implementation checklist

### Verification checklist (run these before declaring done)

- [ ] `grep -n '^## Phase' .omp/commands/init.md` shows Phase 5 as "Hydrate Memory Files", Phase 5a as "Post-Hydration Scan"
- [ ] `grep "Check Agent Files" .omp/commands/init.md` returns nothing (old Phase 5 removed)
- [ ] `grep -c "grep -q '<\[a-z\]'" .omp/commands/init.md` returns 5 (one per memory file)
- [ ] `sed -n '/^## Phase 5:/,/^## Phase 6:/p' .omp/commands/init.md | grep -E '\b(python3?|npm |pip |cargo |node |go version|rustc)\b' | grep -v '<!--' | grep -v 'echo'` returns 0 (no tool invocations)
- [ ] `wc -l .omp/commands/init.md` between 180-220
- [ ] After mental trace or dry-run of Phase 5 with current repo values: PROJECT_NAME="OMP Beads Template", PRIMARY_LANG="TypeScript/Node.js"
- [ ] All 5 memory files would receive heading + content hydration per the table above
