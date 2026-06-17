<!-- DENSITY: Target 500-700 lines. <300 = incomplete (missing sections, hand-wavy, no real technical context). No upper cap — be thorough. This is an AI handoff: another agent must be able to pick this up and implement correctly without guessing. Every section must have concrete evidence: file paths, API signatures, existing patterns, constraints. -->
# PRD: Teach /init to hydrate memory/project files from repo state instead of leaving placeholders

**Bead:** br-omp-backbone-skill-9tl | **Type:** feature | **Priority:** P1
**Created:** 2026-06-17 | **Estimate:** 90 minutes

## Problem

WHEN a user clones the omp-beads-template to bootstrap a new project and runs `/init`, THEN the five memory/project files (project.md, conventions.md, tech-stack.md, gotchas.md, decisions.md) are left with placeholder values like `<project-name>`, `<TypeScript | Python | Go | Rust>`, and `<version>`, BECAUSE the `/init` command only checks that these files exist (Phase 5: "Check Agent Files" at `.omp/commands/init.md:61-65`) but never detects the actual repo state to replace the placeholders.

Every agent session on this project will read ~1KB of placeholder template text that teaches nothing about the project. This violates the "prune over pad" philosophy and the memory protocol rule: "Stale memory is worse than no memory." The gotchas file itself warns about this exact problem ("Memory templates waste tokens if left as placeholders" — `.omp/memory/project/gotchas.md:30`), yet the `/init` command that should fix it does nothing about it.

**Who is affected:** Every user who clones this template. The project starts with a structural defect that persists until a human manually fills in all five files. Manual fill is error-prone, inconsistent, and often delayed indefinitely.

**Why now:** The template is approaching general usability. The `/init` command is the first thing every user runs. A first impression that leaves placeholder cruft in the agent's context forever is a poor first impression.

**What happens if we don't fix it:** Users clone the template, run `/init`, and agents read placeholder text in every session. Some users manually fix it (breaking conventions), others ignore it (agents work with wrong assumptions), and some abandon the template as "too much manual setup."

## Scope

### In Scope
- Detect project name from git remote URL or working directory name
- Detect programming language(s) from package manager config files (package.json, Cargo.toml, go.mod, pyproject.toml)
- Detect package manager from lockfiles (package-lock.json, pnpm-lock.yaml, yarn.lock, Cargo.lock, go.sum)
- Detect runtime from config files (tsconfig.json → Node.js/Bun/Deno, Cargo.toml → Rust, go.mod → Go)
- Replace `<project-name>` placeholders across all 5 memory files with detected project name
- Replace language/tooling placeholders in conventions.md with detected values; mark undetected rows with `<!-- TODO -->`
- Replace language/tooling/version placeholders in tech-stack.md with detected values; mark undetected with `<unknown>`
- Replace `<project-name>` in gotchas.md; preserve all template bootstrap gotchas (they are universally applicable)
- Replace `<project-name>` in decisions.md; preserve template decision records (they explain the template's own architecture)
- Leave human-only fields (project.md goal/success criteria, milestones) as explicit `<!-- TODO: fill in -->` markers
- Add a new "Phase 2.5: Hydrate Memory Files" to `.omp/commands/init.md` between Phase 2 (Initialize br) and Phase 3 (Configure Honcho)
- The hydration phase must be idempotent — safe to run `/init` multiple times without destroying user edits

### Out of Scope
- Auto-detecting project goal, success criteria, or current phase (requires human judgment)
- Auto-detecting gotcha entries for the user's specific codebase
- Auto-detecting architecture decisions for the user's project
- Creating a standalone script — the detection lives inline in the init.md command as bash+Python blocks
- Detecting frameworks (React, Svelte, etc.) — too many frameworks to enumerate reliably
- Detecting CI/CD configurations, linter configs, or test frameworks beyond what's in the verification commands section
- Modifying the template memory files themselves — hydration only runs on the user's clone
- Adding new memory file types or changing the file structure
- Installing or requiring new tools beyond what the template already assumes (bash, python3, git)

## Requirements

| # | Requirement | Priority | Acceptance Criteria |
|---|------------|----------|---------------------|
| 1 | `/init` detects project name from git remote or directory name | MUST | Run `/init` in a repo with `origin` remote; verify `project.md` title is replaced |
| 2 | `/init` detects language(s) from package manager config files | MUST | Run `/init` in a repo with `package.json`; verify `tech-stack.md` shows TypeScript/Node.js |
| 3 | `/init` detects package manager from lockfiles | MUST | Run `/init` in a repo with `pnpm-lock.yaml`; verify `tech-stack.md` shows pnpm |
| 4 | `/init` replaces all `<project-name>` placeholders across 5 memory files | MUST | `grep -r '<project-name>' .omp/memory/` returns empty after `/init` |
| 5 | `/init` replaces language/tooling placeholders in conventions.md | MUST | `grep '<TypeScript |' .omp/memory/project/conventions.md` returns empty after `/init` in a TS project |
| 6 | `/init` replaces language/tooling/version placeholders in tech-stack.md | MUST | `grep '<TypeScript |' .omp/memory/project/tech-stack.md` returns empty after `/init` in a TS project |
| 7 | Hydration is idempotent — re-running `/init` does not destroy filled-in fields | MUST | Fill goal in project.md manually, re-run `/init`, verify goal is preserved |
| 8 | Undetected fields are explicitly marked, not left as template placeholders | SHOULD | Undetected language rows show `<!-- TODO: fill in -->` or `<unknown>`, not `<TypeScript | Python | Go | Rust>` |
| 9 | Human-only fields (goal, success criteria, milestones, decisions) are left with TODO markers | MUST | `project.md` has `<!-- TODO: fill in your project goal -->` not `<One sentence...>` |
| 10 | Template bootstrap gotchas are preserved | MUST | All 12 gotcha rows in gotchas.md survive `/init` intact |
| 11 | Template architecture decisions are preserved | MUST | All 5 decision rows in decisions.md survive `/init` intact |
| 12 | The hydration phase in init.md is clearly separated and documented | MUST | init.md has a distinct Phase 2.5 section with explanation and bash/Python blocks |

## Technical Context

**Key files:**
- `.omp/commands/init.md` (62 lines) — EDIT — the main file to modify. Current structure: Phase 1 (Detect State), Phase 2 (Initialize br), Phase 3 (Configure Honcho), Phase 4 (Verify Backbone), Phase 5 (Check Agent Files), Phase 6 (Report). The hydration phase will be inserted as Phase 2.5 (runs after br init, before Honcho config, because project name is needed for Honcho config).
- `.omp/memory/project/project.md` (31 lines) — READ-ONLY for reference — contains `<project-name>`, `<One sentence...>`, `<Criterion 1-3>`, `<measurable outcome>`, `<active | maintenance | paused>`, `<what we're working toward right now>`, `<the next concrete deliverable>`. The hydration phase reads it, detects which placeholders are still present, and replaces only the auto-detectable ones.
- `.omp/memory/project/conventions.md` (101 lines) — READ-ONLY for reference — contains `<project-name>`, `<TypeScript | Go | Rust | Python>` (3 language rows), `<strict? Bun? Deno?>`, `<React? Svelte? plain?>`, `<Bash | Python | TypeScript>`. The hydration phase replaces language rows based on detection.
- `.omp/memory/project/tech-stack.md` (71 lines) — READ-ONLY for reference — contains `<project-name>`, `<TypeScript | Python | Go | Rust>`, 5 `<version>` placeholders, `<Node.js | Bun | Deno | Python 3.x | Go 1.x>`, `<npm | pnpm | yarn | pip | cargo | go mod>`. The hydration phase replaces detected tooling.
- `.omp/memory/project/gotchas.md` (63 lines) — READ-ONLY for reference — contains `<project-name>`, 12 template bootstrap gotchas. The hydration phase replaces `<project-name>` and preserves all gotcha rows.
- `.omp/memory/project/decisions.md` (46 lines) — READ-ONLY for reference — contains `<project-name>`, 5 template architecture decisions. The hydration phase replaces `<project-name>` and preserves all decision rows.
- `.omp/AGENTS.md` (136 lines) — DO NOT MODIFY — references memory files via `@memory/project/project.md` and `@memory/project/conventions.md`. These `@` imports are resolved by OMP's injection system. No change needed here.
- `.omp/templates/` (directory) — DO NOT MODIFY — templates are the upstream source for memory file defaults. Hydration operates on the instantiated files in `.omp/memory/project/`, not on templates.

**APIs / systems touched:**
- Git remote URL parsing (`git remote get-url origin`) — standard, no API
- Filesystem detection (`find`, `test -f`, `grep`) — standard POSIX
- Python 3 for robust JSON parsing (reading package.json, Cargo.toml) — `python3` is assumed available per the br skill
- `br where` for workspace path detection (already in Phase 1)
- Honcho config in `.env` (uses workspace name derived from project name — Phase 3 runs AFTER hydration, so it picks up the detected name)

**Existing code to NOT modify:**
- `.omp/AGENTS.md` — imports memory files via `@` syntax; hydration makes those imports more useful
- `.omp/RULES.md` — orthogonal to memory hydration
- `.omp/commands/` other than init.md — no other command touches memory files
- `.omp/skills/` — no skill touches memory file hydration
- `.omp/extensions/workflow-gate.ts` — no interaction with memory files
- `.omp/templates/` — templates are the upstream defaults; hydration operates on the instantiated copies
- `.beads/` — br database, no interaction with memory files
- `.gitignore` — no change needed
- `.env` — Honcho config uses workspace name; hydration provides a better default name, but Phase 3 already has the logic

**Existing patterns:**
- Commands use bash code blocks with ` ` `bash fences — the agent executes these as instructions (see init.md Phase 2-4)
- Python 3 is used for robust text processing (see init.md Phase 3 Honcho config)
- `grep`, `find`, `sed` are used for filesystem detection (see create.md Phase 3a)
- Placeholder replacement uses regex substitution (see init.md Phase 3 Honcho .env block)
- Idempotency: the Honcho `.env` block uses `re.sub` to replace a managed block; memory hydration should use a similar approach
- Template gotchas and decisions are deliberately marked as "Template Bootstrap" — they survive until replaced by project-specific entries

**Constraints:**
- No new dependencies — the template philosophy is "commands + skills only, no scripts"
- No standalone script files — all detection logic must be inline in init.md as bash/Python blocks the agent executes
- Python 3 must be available (already required by br skill and Phase 3 Honcho config)
- Must work on a fresh clone with zero pre-existing tooling (just git, bash, python3)
- Must not error out if no language is detected (e.g., pure documentation repos)
- Must preserve any user-edited content in memory files when re-run (idempotency)
- Token budget: each memory file under 2KB per conventions. Hydration doesn't add content — it replaces placeholders

## Approach

### Detection Strategy

The hydration phase runs as a single Python 3 script embedded in a bash block in init.md. A Python script (rather than pure bash) is chosen because:

1. **JSON parsing**: `package.json` requires structured parsing to extract `name`, `scripts.test`, `scripts.build`, `devDependencies.typescript`. Bash can't do this reliably.
2. **TOML parsing**: `Cargo.toml` and `pyproject.toml` require TOML parsing for `package.name`, `package.version`, `tool.poetry.dependencies.python`.
3. **Idempotent replacement**: The script needs to read each memory file, detect which placeholder patterns are still present (meaning the user hasn't filled them in), and only replace those. Simple `sed` would overwrite user edits.
4. **Already established pattern**: init.md Phase 3 already uses Python 3 with `python3 - <<'PY'` heredoc blocks. Phase 2.5 follows this exact pattern.

### Detection Heuristics (in priority order)

**Project name:**
1. `git remote get-url origin` → extract repo name from URL (e.g., `github.com/user/my-project.git` → `my-project`)
2. Fallback: `basename $(git rev-parse --show-toplevel 2>/dev/null || pwd)` → working directory name
3. Sanitize: lowercase, replace spaces/underscores with hyphens, strip non-alphanumeric

**Language detection (check for config files, highest-priority match wins):**
1. `package.json` exists → **TypeScript/JavaScript** (check `devDependencies.typescript` or `tsconfig.json` for TS vs JS)
2. `Cargo.toml` exists → **Rust**
3. `go.mod` exists → **Go**
4. `pyproject.toml` or `setup.py` or `requirements.txt` exists → **Python**
5. None found → **undetected** (mark as `<unknown>`, project may be docs-only or polyglot)

**Runtime detection:**
- `package.json` + `tsconfig.json` → **Node.js** (default), check for Bun (`bun.lockb`) or Deno (`deno.json`)
- `Cargo.toml` → **Rust** (no separate runtime)
- `go.mod` → **Go 1.x** (detect version from `go.mod` `go 1.21` line)
- `pyproject.toml` → **Python 3.x** (detect from `requires-python` or `tool.poetry.dependencies.python`)

**Package manager detection:**
- `pnpm-lock.yaml` → pnpm
- `yarn.lock` → yarn
- `bun.lockb` → bun
- `package-lock.json` → npm
- `Cargo.lock` → cargo
- `go.sum` → go mod
- `poetry.lock` / `Pipfile.lock` → poetry/pipenv (check which exists)
- `requirements.txt` without lock → pip

**Version detection:**
- TypeScript: parse `devDependencies.typescript` from `package.json`
- Node.js: check `.nvmrc` or `.node-version`, otherwise `<unknown>`
- Rust: `rustc --version` if available, otherwise parse `Cargo.toml` `package.edition`
- Go: parse `go.mod` `go` directive
- Python: parse `pyproject.toml` `requires-python` or `tool.poetry.dependencies.python`

### File-by-File Hydration Plan

**project.md** (`.omp/memory/project/project.md`):
- `# Project: <project-name>` → `# Project: {detected-name}`
- Everything else (Goal, Success Criteria, Current Phase) is human judgment → mark with `<!-- TODO: fill in your project goal -->` etc. Only replace if the placeholder pattern (e.g., `<One sentence...>`) is still present — if the user has written real text, preserve it.

**conventions.md** (`.omp/memory/project/conventions.md`):
- `# Conventions: <project-name>` → `# Conventions: {detected-name}`
- Language rows: For each of the 3 table rows (`Backend`, `Frontend`, `Scripts`), if the cell contains a choice pattern like `<TypeScript | Go | Rust | Python>`, replace with detected language. For rows that don't match the detected language, replace with `<!-- TODO: fill in -->` to indicate they need human attention.
- If no language is detected at all (docs-only repo), mark all language rows with `<!-- TODO: fill in -->`.

**tech-stack.md** (`.omp/memory/project/tech-stack.md`):
- `# Tech Stack: <project-name>` → `# Tech Stack: {detected-name}`
- Language row: replace `<TypeScript ...>` with detected language
- Runtime row: replace `<Node.js ...>` with detected runtime
- Package manager row: replace `<npm ...>` with detected package manager
- Version placeholders: fill in detected versions; leave undetected as `<unknown>`
- Verification commands: if a `package.json` has `scripts.test`, replace `<vitest run ...>` with the actual command. Apply same for `scripts.build`, `scripts.lint`. If running a command could detect the tool (e.g., `npx tsc --version` works), use that.
- Security audit commands: if `package.json` has `scripts.audit`, use it; otherwise keep generic `<npm audit ...>` placeholder but adapt to detected package manager.

**gotchas.md** (`.omp/memory/project/gotchas.md`):
- `# Gotchas: <project-name>` → `# Gotchas: {detected-name}`
- All 12 template bootstrap gotchas are preserved as-is — they describe the template itself and are always relevant
- The "Active Warnings" table header row's first entry `<YYYY-MM>` / `<area>` / `<what happens>` is the placeholder for project-specific gotchas — leave as-is (the human fills these in)

**decisions.md** (`.omp/memory/project/decisions.md`):
- `# Decisions: <project-name>` → `# Decisions: {detected-name}`
- All 5 template architecture decisions are preserved as-is — they document why this template works the way it does
- The "Decision Log" example row `#1` with `<YYYY-MM>` / `<what we decided>` is the placeholder for project-specific decisions — leave as-is

### Concrete Before/After Example

**tech-stack.md before hydration (TypeScript + npm project):**
```markdown
# Tech Stack: <project-name>

## Runtime
| Layer | Tool | Version | Notes |
|-------|------|---------|-------|
| Language | <TypeScript | Python | Go | Rust> | <version> | <strict mode? async? experimental flags?> |
| Runtime | <Node.js | Bun | Deno | Python 3.x | Go 1.x> | <version> | <LTS? latest?> |
| Package manager | <npm | pnpm | yarn | pip | cargo | go mod> | <version> | |
```

**tech-stack.md after hydration:**
```markdown
# Tech Stack: my-project

## Runtime
| Layer | Tool | Version | Notes |
|-------|------|---------|-------|
| Language | TypeScript | 5.3 | |
| Runtime | Node.js | <unknown> | LTS |
| Package manager | npm | <unknown> | |
```

**conventions.md before (Languages by Purpose table):**
```markdown
| Backend | <TypeScript | Go | Rust | Python> | <strict? Bun? Deno?> |
| Frontend | <TypeScript | JavaScript> | <React? Svelte? plain?> |
| Scripts | <Bash | Python | TypeScript> | <CI, dev tooling, one-offs> |
```

**conventions.md after hydration (TypeScript-only backend project):**
```markdown
| Backend | TypeScript | strict |
| Frontend | <!-- TODO: fill in --> | <!-- TODO: fill in --> |
| Scripts | Bash | CI, dev tooling, one-offs |
```

Note that `Frontend` is marked TODO because only a backend language was detected — the hydration script doesn't guess what the frontend stack is. `Scripts` defaults to Bash (always available) but leaves the notes column untouched.

### Python Script Structure (Pseudocode)

The hydration script follows this outline (actual implementation lives in init.md Phase 2.5):

```python
import json, re, os, sys
from pathlib import Path

ROOT = Path.cwd()
MEMORY = ROOT / ".omp" / "memory" / "project"

# --- Detection ---
def detect_project_name():
    # 1. Try git remote
    result = run("git remote get-url origin", capture=True)
    if result.ok:
        name = extract_repo_name(result.stdout)  # github.com/user/my-project.git → my-project
        return sanitize(name)
    # 2. Fallback: directory name
    return sanitize(ROOT.name)

def detect_language():
    configs = [
        ("package.json", "TypeScript"),
        ("Cargo.toml", "Rust"),
        ("go.mod", "Go"),
        ("pyproject.toml", "Python"),
        ("setup.py", "Python"),
        ("requirements.txt", "Python"),
    ]
    for filename, lang in configs:
        if (ROOT / filename).exists():
            return lang, filename
    return None, None

def detect_package_manager(lang):
    lockfiles = {
        "pnpm-lock.yaml": "pnpm", "yarn.lock": "yarn",
        "bun.lockb": "bun", "package-lock.json": "npm",
        "Cargo.lock": "cargo", "go.sum": "go mod",
        "poetry.lock": "poetry", "Pipfile.lock": "pipenv",
    }
    for lockfile, pm in lockfiles.items():
        if (ROOT / lockfile).exists():
            return pm
    # Fallbacks by language
    if lang == "TypeScript" and (ROOT / "package.json").exists():
        return "npm"
    if lang == "Python" and (ROOT / "requirements.txt").exists():
        return "pip"
    return None

def detect_version(lang, config_file):
    if lang == "TypeScript":
        pkg = json.loads((ROOT / "package.json").read_text())
        return pkg.get("devDependencies", {}).get("typescript", None)
    if lang == "Go":
        go_mod = (ROOT / "go.mod").read_text()
        m = re.search(r"^go (\d+\.\d+)", go_mod, re.MULTILINE)
        return m.group(1) if m else None
    # Rust: edition from Cargo.toml; Python: requires-python from pyproject.toml
    return None

# --- Hydration ---
def hydrate_file(filepath, replacements):
    content = filepath.read_text()
    modified = False
    for pattern, replacement in replacements.items():
        if pattern in content:  # Only replace if placeholder still present
            content = content.replace(pattern, replacement)
            modified = True
    if modified:
        filepath.write_text(content)
        print(f"  Hydrated: {filepath.name}")
    else:
        print(f"  Skipped (already hydrated): {filepath.name}")

def main():
    name = detect_project_name()
    lang, config = detect_language()
    pm = detect_package_manager(lang)
    ver = detect_version(lang, config) if lang else None

    # project.md replacements
    hydrate_file(MEMORY / "project.md", {
        "<project-name>": name,
        "<One sentence — what are we building and why?>": "<!-- TODO: fill in your project goal -->",
        "<Criterion 1>": "<!-- TODO: fill in -->",
        "<Criterion 2>": "<!-- TODO: fill in -->",
        "<Criterion 3>": "<!-- TODO: fill in -->",
        "<measurable outcome>": "<!-- TODO: fill in -->",
        "<active | maintenance | paused>": "active",
        "<what we're working toward right now>": "<!-- TODO: fill in -->",
        "<the next concrete deliverable>": "<!-- TODO: fill in -->",
    })

    # tech-stack.md replacements
    ts_replacements = {"<project-name>": name}
    if lang:
        ts_replacements["<TypeScript | Python | Go | Rust>"] = lang
    else:
        ts_replacements["<TypeScript | Python | Go | Rust>"] = "<unknown>"
    hydrate_file(MEMORY / "tech-stack.md", ts_replacements)

    # conventions.md, gotchas.md, decisions.md follow same pattern

if __name__ == "__main__":
    main()
```

### Edge Cases Handled

| Scenario | Behavior |
|----------|----------|
| No git remote (fresh init before first push) | Falls back to directory name |
| Multiple config files (monorepo with Rust + TypeScript) | First match wins (priority: package.json > Cargo.toml > go.mod > pyproject.toml). Human can edit after. |
| `package.json` in a subdirectory (workspace root has no config) | Check only repo root. Subdirectory configs are ignored — hydration targets the project root. |
| Corrupt config file (malformed JSON/TOML) | try/except wraps all parsing; skip that detection dimension, leave placeholder |
| User already edited some fields but not all | Idempotency: each placeholder checked individually; only unfilled ones replaced |
| Python 3 not available | Check `which python3` before running script; if missing, print warning and skip hydration (graceful degradation) |
| Directory name has special characters | Sanitize: lowercase, replace non-alphanumeric with hyphens, collapse consecutive hyphens |
| This template repo itself (omp-template) | Hydration detects "omp-beads-template" from remote URL. The template's own memory files are NOT modified during template development (they're the canonical source). The hydration script only runs in user clones, not during template dev. |

### Idempotency Strategy

The Python script reads each file's current content. For each placeholder pattern:
1. Check if the placeholder text (e.g., `<project-name>`) is still present in the file
2. If present → replace with detected value
3. If not present → the user has already replaced it, skip

This means:
- Running `/init` once: all auto-detectable placeholders get filled
- User then edits project.md to add their goal
- Running `/init` again: the goal is preserved (no placeholder pattern to match), project name is preserved (already replaced)
- The script is safe to run repeatedly

### init.md Structure Change

Insert Phase 2.5 between current Phase 2 (Initialize br) and Phase 3 (Configure Honcho):

```
## Phase 2.5: Hydrate Memory Files

Detect repo state and fill in auto-detectable fields across all five memory/project files.

[Detection here via Python script]

If this is a fresh clone, placeholders get real values. If the user has already edited files, only unfilled placeholders are replaced. The script is idempotent.
```

Phase 3 (Configure Honcho) runs after hydration because it derives `HONCHO_WORKSPACE_ID` from the project name. With hydration, the workspace name is now based on the detected project name rather than just the directory name.

Phase 4 (Verify Backbone) and Phase 5 (Check Agent Files) remain unchanged — the memory files now have real content instead of placeholders. Phase 6 (Report) should mention whether hydration filled in files or found them already populated.

### Why This Approach Over Alternatives

**Alternative A: Separate hydration script file**
- Rejected: violates "commands + skills only, no scripts" philosophy
- Also rejected because it would need to be maintained separately from the command

**Alternative B: Pure bash detection (grep/sed only)**
- Rejected: bash can't parse `package.json` or `Cargo.toml` reliably. JSON/TOML in bash requires fragile regex that breaks on whitespace or key ordering.
- Risk if re-introduced: incorrect values silently written to memory files, worse than placeholders

**Alternative C: OMP extension in TypeScript**
- Rejected: Over-engineering. An OMP extension adds the complexity of a TypeScript compilation step for something that a 50-line Python script handles. Also, extensions are for tool behavior modification (like the workflow gate), not for one-time initialization.
- Risk if re-introduced: maintenance burden, platform dependency, extension loading overhead

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Python script fails on malformed package.json or Cargo.toml | Medium | Low — hydration skips that file, leaves placeholder | Wrap all file parsing in try/except; log warning but don't abort init |
| Detection produces wrong language (e.g., test fixtures have package.json but project is Rust) | Low | Medium — wrong tech-stack.md content | Only check for config files in the repo root. Skip `node_modules/` and `vendor/`. Document that users can override by editing files manually. |
| Idempotency fails — script overwrites user edits | Medium | High — lost user work on conventions or decisions | Use regex patterns that match only the template placeholders, not user-written content. Test with pre-edited files before shipping. |
| Script breaks on repos with no git remote (fresh init before first push) | Low | Low — falls back to directory name | Graceful fallback to `basename $PWD`. Document in init.md that project name comes from directory if no remote exists. |
| Template gotchas or decisions accidentally modified | Low | High — lost institutional knowledge about template behavior | Hydration targets only `<project-name>` in gotchas.md and decisions.md. All table content is preserved untouched. Verify with grep after hydration. |
| Phase reordering breaks Honcho config | Low | Medium — wrong HONCHO_WORKSPACE_ID | Phase 2.5 runs before Phase 3 by design. Phase 3 already uses `re.sub` for idempotent replacement. Confirm the Python variable name used in Phase 2.5 matches what Phase 3 reads from the file. |

## Acceptance Criteria

- [ ] 1. Fresh clone: run `/init` on a repo with `package.json` (TypeScript, npm)
    - Verify: `grep -r '<project-name>' .omp/memory/project/` returns nothing
    - Verify: `.omp/memory/project/tech-stack.md` shows "TypeScript" as language, "Node.js" as runtime, "npm" as package manager
    - Verify: `.omp/memory/project/conventions.md` Backend row shows "TypeScript" not `<TypeScript | Go | Rust | Python>`
- [ ] 2. Fresh clone: run `/init` on a repo with `Cargo.toml`
    - Verify: `tech-stack.md` shows "Rust" as language, "cargo" as package manager
- [ ] 3. Fresh clone: run `/init` on a repo with `go.mod`
    - Verify: `tech-stack.md` shows "Go" as language, "go mod" as package manager
- [ ] 4. Fresh clone: run `/init` on a docs-only repo (no config files)
    - Verify: `tech-stack.md` language row shows `<unknown>` or `<!-- TODO -->`, not the old multi-choice placeholder
    - Verify: `/init` does not error out
- [ ] 5. Idempotency: run `/init`, manually edit `project.md` goal section, run `/init` again
    - Verify: Manual edit is preserved (no placeholder pattern matched, so no overwrite)
    - Verify: Project name is still correctly filled
- [ ] 6. Template preservation: after `/init`, verify all 12 gotcha rows in gotchas.md are unchanged
    - Verify: `grep -c '^|' .omp/memory/project/gotchas.md` returns the same count before and after
- [ ] 7. Template preservation: after `/init`, verify all 5 decision rows in decisions.md are unchanged
    - Verify: `grep -c '^| [0-9]' .omp/memory/project/decisions.md` returns 5 after `/init`
- [ ] 8. No regression: run `/init` on this template repo itself (omo-template)
    - Verify: br initialization succeeds, Honcho config is written, backbone is verified
    - Verify: The memory files used by THIS template are not damaged (they're the canonical copies)
