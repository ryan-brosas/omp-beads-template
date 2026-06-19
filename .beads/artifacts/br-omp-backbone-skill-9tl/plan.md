<!-- DENSITY: Target 500-700 lines. <300 = too thin (waves undefined, tasks lack code outlines, verification hand-wavy). Task outlines should show the shape of every file change — not full implementation, but enough that a different agent can execute without reading the PRD again. -->
# Plan: Teach /init to hydrate memory/project files from repo state

**Goal:** `/init` Phase 5 is replaced with a multi-step hydration phase that detects project identity from repo state (README.md, git remote, lockfiles/config files) and rewrites memory file placeholders with concrete, repo-derived content — making the template immediately useful after bootstrap without manual memory-file editing.

## Graph Context

- **Blast radius:** 1 file (0 new, 1 edit, 0 deletes) — `.omp/commands/init.md` is the sole implementation target. The 5 memory files under `.omp/memory/project/` are runtime hydration targets (written by `/init` at bootstrap time, not modified during implementation).
- **Unblocks:** None. This is a bootstrap-quality fix; no other beads depend on it.
- **Blocked by:** None. No upstream dependencies.
- **Critical path:** No. This is a self-contained quality improvement to the bootstrap experience.
- **Forecast:** 90 minutes (confidence 0.85). Detection primitives are shell one-liners on small files; hydration is sed on known template patterns. Primary risk is edge cases in README parsing (multi-line headings, no README, unusual README structure).
- **Hotspots touched:** None. `.omp/commands/init.md` has zero prior bead history.

## Observable Truths

1. After `/init` in a fresh clone, `grep -r '<project-name>' .omp/memory/project/` returns zero matches — no template placeholder survives in the heading position.
2. After `/init` in a repo with `# My Project` in README.md, `head -3 .omp/memory/project/project.md` contains `# Project: My Project`.
3. After `/init` in a project with `package.json`, `grep 'Language' .omp/memory/project/tech-stack.md` shows `TypeScript` or `TypeScript/Node.js` — not `<TypeScript | Python | Go | Rust>`.
4. After first `/init` hydrates files, manually editing `project.md` to say "Custom Project Name", then running `/init` again — the manual edit survives and `project.md` still says "Custom Project Name".
5. After `/init` in a repo with no README.md, `project.md` heading uses the directory name (e.g., `# Project: my-project`).
6. `.omp/commands/init.md` contains a `## Phase 5: Hydrate Memory Files` heading (not `## Phase 5: Check Agent Files`).
7. The Phase 5 body includes shell commands for repo state detection (grep, sed, git remote, ls) and file hydration (sed, echo) — no Python, no package manager invocation.
8. Phase 6 (Report) still works and the report output includes "Memory files hydrated: N" or equivalent.
9. `wc -l .omp/commands/init.md` is between 180 and 220 lines (up from ~120) — the added ~80 lines are detection and hydration logic, not fluff.
10. Post-hydration, `grep -c '<[a-z]' .omp/memory/project/*.md` returns a non-zero count for placeholder patterns that were intentionally left (e.g., verification commands, version placeholders with `<!-- run ... -->` comments), but zero for project identity placeholders (`<project-name>`, `<what are we building>`).

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| PRD | Problem statement, scope, requirements, technical context | `.beads/artifacts/br-omp-backbone-skill-9tl/prd.md` | Have |
| Decisions | Architecture decisions, rejected alternatives, assumptions | `.beads/artifacts/br-omp-backbone-skill-9tl/decisions.md` | Have |
| Plan | This file — wave structure, task outlines, verification | `.beads/artifacts/br-omp-backbone-skill-9tl/plan.md` | Need |
| Tasks | Ordered task checklist with dependencies | `.beads/artifacts/br-omp-backbone-skill-9tl/tasks.md` | Need |
| Context capsule | Agent handoff with file ownership and constraints | `.beads/artifacts/br-omp-backbone-skill-9tl/context-capsule.md` | Need |

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | 1.1, 1.2, 1.3 | Yes | Read current init.md and all 5 memory files to understand placeholder patterns | Each detection command returns expected output when tested manually against the current repo |
| 2 | 2.1, 2.2, 2.3, 2.4, 2.5 | Yes | Wave 1 complete — detection variables are defined and tested | Each hydration sed command correctly transforms a placeholder to detected value when tested on a copy of the memory file |
| 3 | 3.1, 3.2, 3.3, 3.4 | No (sequential integration steps) | Waves 1-2 complete — all detection and hydration snippets are verified independently | Full `/init` dry-run produces hydrated files with zero `<project-name>` placeholders; idempotency confirmed via double-run |

## Tasks

### Wave 1: Detection Primitives {parallel}

These three tasks define the shell commands that extract project identity from repo state. They are independent — project name detection, description extraction, and language detection touch different files and different commands. Each produces a shell variable (`PROJECT_NAME`, `PROJECT_DESC`, `PRIMARY_LANG`, `RUNTIME`, `PKG_MANAGER`) consumed by Wave 2 hydration commands.

**Task 1.1: Project name detection**

Extract the project name from README.md h1, fall back through git remote origin, then directory name. Priority order matches decision #5: README h1 is the canonical project name source.

This task defines the shell snippet that sets `PROJECT_NAME`. The snippet must handle:
- README.md exists with `# Some Project Name` → `PROJECT_NAME="Some Project Name"`
- README.md exists with `# Some Project Name — Subtitle` → `PROJECT_NAME="Some Project Name — Subtitle"`
- README.md exists but h1 has markdown links like `# [Project](url)` → strip markdown link syntax, keep text
- No README.md → try `git remote get-url origin 2>/dev/null`, extract repo name from URL (strip `.git`, strip path, take last segment)
- No git remote → use `basename "$(pwd)"` (directory name)
- Empty or whitespace-only result → `PROJECT_NAME="Untitled Project"`

```
# Shape of the detection snippet:
PROJECT_NAME=""
if [ -f "README.md" ]; then
  PROJECT_NAME=$(grep -m1 '^# ' README.md | sed 's/^# //' | sed 's/\[\([^]]*\)\]([^)]*)/\1/g' | xargs)
fi
if [ -z "$PROJECT_NAME" ]; then
  PROJECT_NAME=$(git remote get-url origin 2>/dev/null | sed 's|.*/||; s|\.git$||' | xargs)
fi
if [ -z "$PROJECT_NAME" ]; then
  PROJECT_NAME=$(basename "$(pwd)")
fi
if [ -z "$PROJECT_NAME" ]; then
  PROJECT_NAME="Untitled Project"
fi
```

**Verification:** Run the snippet in the current repo (omp-template). Expected: `PROJECT_NAME="OMP Beads Template"` (from README.md h1). Run in a temp dir without README: expected `PROJECT_NAME` matches directory basename.

**Task 1.2: Project description extraction**

Extract the first substantive paragraph from README.md after the h1 heading. Skip blank lines, skip badge/image lines (`[!`, `[<img`), skip subtitle lines that might be h2 (`## `), take the first non-empty, non-heading line that looks like prose.

This task defines the shell snippet that sets `PROJECT_DESC`. The snippet must handle:
- README.md exists with h1 then blank line then descriptive paragraph → capture that paragraph
- README.md exists but first paragraph is badges → skip badge lines, take next paragraph
- README.md exists but is only headings (unusual) → use fallback: `"<!-- Replace with your project description -->"`
- No README.md → same fallback

```
# Shape of the detection snippet:
PROJECT_DESC=""
if [ -f "README.md" ]; then
  # Skip from h1, then take first non-empty, non-heading, non-badge line
  PROJECT_DESC=$(awk '/^# / {found=1; next} found && NF && !/^#/ && !/^\[!/ && !/^\[</ {print; exit}' README.md | xargs)
fi
if [ -z "$PROJECT_DESC" ]; then
  PROJECT_DESC="<!-- Replace with your project description -->"
fi
```

**Verification:** Run the snippet in the current repo. Expected: `PROJECT_DESC` contains "OMP-native project template with br and bv as the backbone" (first paragraph of omp-template README after h1).

**Task 1.3: Language/runtime detection**

Detect primary language and runtime from lockfile/config file presence. Priority order per decision #4: TypeScript > Go > Python > Rust. Additional second-order signals refine within an ecosystem (e.g., `tsconfig.json` → TypeScript, not just Node.js).

This task defines the shell snippet that sets `PRIMARY_LANG`, `RUNTIME`, and `PKG_MANAGER`. Detection table:

| File present | PRIMARY_LANG | RUNTIME | PKG_MANAGER |
|-------------|-------------|---------|-------------|
| `package.json` + `tsconfig.json` | TypeScript | Node.js (`<!-- run node --version -->`) | npm (`<!-- run npm --version -->`) |
| `package.json` (no tsconfig) | TypeScript/Node.js | Node.js (`<!-- run node --version -->`) | npm (`<!-- run npm --version -->`) |
| `go.mod` | Go | Go (`<!-- run go version -->`) | go mod (`<!-- run go version -->`) |
| `pyproject.toml` or `requirements.txt` | Python | Python 3.x (`<!-- run python3 --version -->`) | pip/poetry (`<!-- check pyproject.toml -->`) |
| `Cargo.toml` | Rust | Rust (`<!-- run rustc --version -->`) | cargo (`<!-- run cargo --version -->`) |
| None of the above | `<!-- TypeScript | Python | Go | Rust -->` | `<!-- determine runtime -->` | `<!-- determine package manager -->` |

```
# Shape of the detection snippet:
PRIMARY_LANG=""; RUNTIME=""; PKG_MANAGER=""
if [ -f "package.json" ] && [ -f "tsconfig.json" ]; then
  PRIMARY_LANG="TypeScript"
  RUNTIME="Node.js \`<!-- run node --version -->\`"
  PKG_MANAGER="npm \`<!-- run npm --version -->\`"
elif [ -f "package.json" ]; then
  PRIMARY_LANG="TypeScript/Node.js"
  RUNTIME="Node.js \`<!-- run node --version -->\`"
  PKG_MANAGER="npm \`<!-- run npm --version -->\`"
elif [ -f "go.mod" ]; then
  PRIMARY_LANG="Go"
  RUNTIME="Go \`<!-- run go version -->\`"
  PKG_MANAGER="go mod \`<!-- run go version -->\`"
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
  PRIMARY_LANG="Python"
  RUNTIME="Python 3.x \`<!-- run python3 --version -->\`"
  PKG_MANAGER="pip/poetry \`<!-- check pyproject.toml -->\`"
elif [ -f "Cargo.toml" ]; then
  PRIMARY_LANG="Rust"
  RUNTIME="Rust \`<!-- run rustc --version -->\`"
  PKG_MANAGER="cargo \`<!-- run cargo --version -->\`"
else
  PRIMARY_LANG="<!-- TypeScript | Python | Go | Rust -->"
  RUNTIME="<!-- determine runtime -->"
  PKG_MANAGER="<!-- determine package manager -->"
fi
```

**Verification:** Run in a temp dir with only `package.json`: expected `PRIMARY_LANG="TypeScript/Node.js"`. Run with both `package.json` and `tsconfig.json`: expected `PRIMARY_LANG="TypeScript"`. Run with only `go.mod`: expected `PRIMARY_LANG="Go"`. Run with no lockfiles: expected all three variables contain `<!-- ... -->` placeholders.

### Wave 2: Hydration Commands {parallel}

These five tasks define the sed/awk/grep commands that hydrate each memory file. They consume the variables from Wave 1. All five tasks can be developed in parallel since they target different files. Each hydration command is guarded by an **idempotency check**: it only rewrites if angle-bracket placeholders (`<[a-z]`) exist in the file, preventing overwrite of user-authored content.

**Task 2.1: Hydrate project.md**

Rewrite `project.md` heading, goal description, and current phase status with detected values.

Patterns to replace:
- `# Project: <project-name>` → `# Project: $PROJECT_NAME`
- `<One sentence — what are we building and why?>` → `$PROJECT_DESC`
- `<Criterion 1>`, `<Criterion 2>`, `<Criterion 3>` — leave as-is (out of scope: success criteria require domain knowledge)
- `<active | maintenance | paused>` → `active` (fresh init = active project)
- `<what we're working toward right now>` → `"Complete project initialization and setup"`
- `<the next concrete deliverable>` → `"Run /brainstorm to identify first work item"`

```
# Shape of the hydration snippet (runs inside the init command):
if grep -q '<[a-z]' .omp/memory/project/project.md 2>/dev/null; then
  sed -i "s/# Project: <project-name>/# Project: $PROJECT_NAME/" .omp/memory/project/project.md
  sed -i "s/<One sentence — what are we building and why?>/$PROJECT_DESC/" .omp/memory/project/project.md
  sed -i 's/<active | maintenance | paused>/active/' .omp/memory/project/project.md
  sed -i 's/<what we.re working toward right now>/Complete project initialization and setup/' .omp/memory/project/project.md
  sed -i 's/<the next concrete deliverable>/Run \/brainstorm to identify first work item/' .omp/memory/project/project.md
  echo "  ✓ project.md hydrated"
else
  echo "  - project.md (user content detected — skipped)"
fi
```

Edge case: `$PROJECT_NAME` or `$PROJECT_DESC` may contain `/` or `&` characters that break sed. Mitigation: use a different delimiter in sed (e.g., `sed "s|pattern|$VAR|"`) and escape `&` in the variable: `ESCAPED_DESC=$(echo "$PROJECT_DESC" | sed 's/&/\\&/g')`.

**Verification:** On a copy of the template project.md with placeholders, run the snippet with `PROJECT_NAME="My Test Project"` and `PROJECT_DESC="A test project for verification"`. Verify heading is `# Project: My Test Project` and description is filled. Verify criterion placeholders remain untouched.

**Task 2.2: Hydrate conventions.md**

Rewrite `conventions.md` heading and language-by-purpose table rows with detected values.

Patterns to replace:
- `# Conventions: <project-name>` → `# Conventions: $PROJECT_NAME`
- The "Languages by Purpose" table has three placeholder rows:
  - Backend row: `<TypeScript | Go | Rust | Python>` → detected `$PRIMARY_LANG`; `<strict? Bun? Deno?>` → `<!-- specify constraints -->`
  - Frontend row: `<TypeScript | JavaScript>` → if TypeScript detected → `TypeScript`, else `<!-- TypeScript | JavaScript -->`; `<React? Svelte? plain?>` → `<!-- specify framework -->`
  - Scripts row: `<Bash | Python | TypeScript>` → `Bash` (scripts are always Bash for this template); `<CI, dev tooling, one-offs>` → `<!-- CI, dev tooling, one-offs -->`

```
# Shape of the hydration snippet:
if grep -q '<[a-z]' .omp/memory/project/conventions.md 2>/dev/null; then
  sed -i "s|# Conventions: <project-name>|# Conventions: $PROJECT_NAME|" .omp/memory/project/conventions.md

  # Backend row
  if [ -n "$PRIMARY_LANG" ] && ! echo "$PRIMARY_LANG" | grep -q '<!--'; then
    sed -i "s|<TypeScript | Go | Rust | Python>|$PRIMARY_LANG|" .omp/memory/project/conventions.md
  else
    sed -i 's|<TypeScript | Go | Rust | Python>|<!-- TypeScript | Go | Rust | Python -->|' .omp/memory/project/conventions.md
  fi
  sed -i 's|<strict? Bun? Deno?>|<!-- specify constraints -->|' .omp/memory/project/conventions.md

  # Frontend row
  if echo "$PRIMARY_LANG" | grep -q "TypeScript"; then
    sed -i 's|<TypeScript | JavaScript>|TypeScript|' .omp/memory/project/conventions.md
  else
    sed -i 's|<TypeScript | JavaScript>|<!-- TypeScript | JavaScript -->|' .omp/memory/project/conventions.md
  fi
  sed -i 's|<React? Svelte? plain?>|<!-- specify framework -->|' .omp/memory/project/conventions.md

  # Scripts row — kept as Bash (template convention)
  sed -i 's|<Bash | Python | TypeScript>|Bash|' .omp/memory/project/conventions.md
  sed -i 's|<CI, dev tooling, one-offs>|<!-- CI, dev tooling, one-offs -->|' .omp/memory/project/conventions.md

  echo "  ✓ conventions.md hydrated"
else
  echo "  - conventions.md (user content detected — skipped)"
fi
```

**Verification:** Run with `PRIMARY_LANG="TypeScript"`. Verify backend row says `TypeScript` (not placeholder), frontend says `TypeScript` (matched), scripts says `Bash`. Run with `PRIMARY_LANG="Go"`. Verify backend says `Go`, frontend stays as `<!-- TypeScript | JavaScript -->` comment placeholder (not overwritten with wrong language).

**Task 2.3: Hydrate decisions.md**

Rewrite `decisions.md` heading only. All five template decisions (br/bv, commands+skills, bare names, .omp/ root, separate tooling) are preserved — they ARE the project's first architectural decisions per decision #6.

Patterns to replace:
- `# Decisions: <project-name>` → `# Decisions: $PROJECT_NAME`
- `<YYYY-MM>` date placeholders in the template decision rows → actual dates. Template decisions 1-5 were made in `2026-06`. Leave these as `2026-06` (the actual template creation date) — update the placeholder `<YYYY-MM>` to `2026-06`.

```
# Shape of the hydration snippet:
if grep -q '<[a-z]' .omp/memory/project/decisions.md 2>/dev/null; then
  sed -i "s|# Decisions: <project-name>|# Decisions: $PROJECT_NAME|" .omp/memory/project/decisions.md
  sed -i 's|<YYYY-MM>|2026-06|g' .omp/memory/project/decisions.md
  echo "  ✓ decisions.md hydrated"
else
  echo "  - decisions.md (user content detected — skipped)"
fi
```

**Verification:** Run with `PROJECT_NAME="My Project"`. Verify heading is `# Decisions: My Project` and all `<YYYY-MM>` placeholders changed to `2026-06`. The 5 template decisions remain in the table.

**Task 2.4: Hydrate tech-stack.md**

Rewrite `tech-stack.md` heading, language/runtime/package-manager rows with detected values. Leave verification commands, key dependencies table, and version columns as directed placeholders (per decision #8: we don't run tools to detect versions).

Patterns to replace:
- `# Tech Stack: <project-name>` → `# Tech Stack: $PROJECT_NAME`
- Language row: `<TypeScript | Python | Go | Rust>` → `$PRIMARY_LANG`; `<version>` → `<!-- run ... -->` comment; `<strict mode? async? experimental flags?>` → `<!-- specify -->`
- Runtime row: `<Node.js | Bun | Deno | Python 3.x | Go 1.x>` → `$RUNTIME`; `<version>` → already handled by `$RUNTIME` inline comment; `<LTS? latest?>` → `<!-- specify -->`
- Package manager row: `<npm | pnpm | yarn | pip | cargo | go mod>` → `$PKG_MANAGER`; `<version>` → already handled by `$PKG_MANAGER` inline comment

```
# Shape of the hydration snippet:
if grep -q '<[a-z]' .omp/memory/project/tech-stack.md 2>/dev/null; then
  sed -i "s|# Tech Stack: <project-name>|# Tech Stack: $PROJECT_NAME|" .omp/memory/project/tech-stack.md

  # Language row
  if [ -n "$PRIMARY_LANG" ] && ! echo "$PRIMARY_LANG" | grep -q '<!--'; then
    sed -i "s|<TypeScript \\\\| Python \\\\| Go \\\\| Rust>|$PRIMARY_LANG|" .omp/memory/project/tech-stack.md
  fi
  sed -i 's|<version>|<!-- run appropriate version command -->|' .omp/memory/project/tech-stack.md
  sed -i 's|<strict mode? async? experimental flags?>|<!-- specify -->|' .omp/memory/project/tech-stack.md

  # Runtime row
  if [ -n "$RUNTIME" ] && ! echo "$RUNTIME" | grep -q '<!--'; then
    sed -i "s|<Node.js \\\\| Bun \\\\| Deno \\\\| Python 3.x \\\\| Go 1.x>|$RUNTIME|" .omp/memory/project/tech-stack.md
  fi
  # Version column for runtime row — handled by RUNTIME variable's inline `<!-- run ... -->`
  sed -i 's|<LTS? latest?>|<!-- specify -->|' .omp/memory/project/tech-stack.md

  # Package manager row
  if [ -n "$PKG_MANAGER" ] && ! echo "$PKG_MANAGER" | grep -q '<!--'; then
    sed -i "s|<npm \\\\| pnpm \\\\| yarn \\\\| pip \\\\| cargo \\\\| go mod>|$PKG_MANAGER|" .omp/memory/project/tech-stack.md
  fi
  # Version column for pkg mgr — handled by PKG_MANAGER variable's inline comment

  # Verification commands — leave all placeholders, add guidance comment
  # (Out of scope per PRD: requires knowing test framework, build tool, conventions)

  echo "  ✓ tech-stack.md hydrated"
else
  echo "  - tech-stack.md (user content detected — skipped)"
fi
```

**Verification:** Run with `PRIMARY_LANG="Go"`, `RUNTIME="Go <!-- run go version -->"`, `PKG_MANAGER="go mod <!-- run go version -->"`. Verify tech-stack.md language row says `Go`, runtime row says `Go <!-- run go version -->`, package manager says `go mod <!-- run go version -->`. Verify verification command placeholders (`<tsc --noEmit | ...>`) remain unchanged.

**Task 2.5: Hydrate gotchas.md**

Rewrite `gotchas.md` heading. Preserve the "Template Bootstrap Gotchas" table (they are real gotchas per decision #7). Add a comment above the table demarcating it as template-inherited.

Patterns to replace:
- `# Gotchas: <project-name>` → `# Gotchas: $PROJECT_NAME`
- Add a note above the Template Bootstrap Gotchas table: `<!-- The gotchas below are inherited from the omp-template. Replace with project-specific gotchas as you discover them. -->`
- The "Active Warnings" table heading stays — it's the table for project-specific gotchas (currently has only a placeholder row with `<YYYY-MM>`)

```
# Shape of the hydration snippet:
if grep -q '<[a-z]' .omp/memory/project/gotchas.md 2>/dev/null; then
  sed -i "s|# Gotchas: <project-name>|# Gotchas: $PROJECT_NAME|" .omp/memory/project/gotchas.md

  # Add demarcation above Template Bootstrap Gotchas table (between Active Warnings and Template Bootstrap)
  # The pattern: insert comment before "## Template Bootstrap Gotchas" heading
  sed -i '/^## Template Bootstrap Gotchas$/i\
\
<!-- The gotchas below are inherited from the omp-template. Replace with project-specific gotchas as you discover them. -->' .omp/memory/project/gotchas.md

  echo "  ✓ gotchas.md hydrated"
else
  echo "  - gotchas.md (user content detected — skipped)"
fi
```

**Verification:** Run with `PROJECT_NAME="Test"`. Verify heading is `# Gotchas: Test`. Verify the Template Bootstrap Gotchas section has a `<!-- inherited from omp-template -->` comment above it. Verify the Active Warnings table (with `<YYYY-MM>` placeholder row) remains untouched for user to fill in.

### Wave 3: Integration and Verification {sequential}

These tasks integrate the Wave 1-2 snippets into the init.md command file, add post-hydration scanning, and verify end-to-end correctness. They are sequential because each builds on the previous.

**Task 3.1: Replace Phase 5 in init.md with hydration phase**

Replace the current `## Phase 5: Check Agent Files` block (lines ~95-101 in init.md: "Verify these are present and current" with the file list) with two new phases:

- **Phase 5: Hydrate Memory Files** — runs the detection primitives (Wave 1), then runs the hydration commands (Wave 2) for each of the 5 memory files. Includes idempotency guards.
- **Phase 5a: Post-Hydration Scan** — greps for remaining angle-bracket placeholders and reports them. Warns if project identity placeholders remain (indicates a bug). Notes if intentional placeholders remain (verification commands, versions).

The existing Phase 6 (Report) stays unchanged except for an additional line: `Memory files: <N hydrated, M skipped, K placeholders remaining>`.

```
# Shape of the new Phase 5 block in init.md:

## Phase 5: Hydrate Memory Files

Hydrate template placeholders in memory files with repo-derived content.
Files with user-authored content (no angle-bracket placeholders) are skipped.

### 5.1: Detect Project Identity

\`\`\`bash
# --- Project name ---
PROJECT_NAME=""
if [ -f "README.md" ]; then
  PROJECT_NAME=$(grep -m1 '^# ' README.md | sed 's/^# //' | sed 's/\[\([^]]*\)\]([^)]*)/\1/g' | xargs)
fi
if [ -z "$PROJECT_NAME" ]; then
  PROJECT_NAME=$(git remote get-url origin 2>/dev/null | sed 's|.*/||; s|\.git$||' | xargs)
fi
if [ -z "$PROJECT_NAME" ]; then
  PROJECT_NAME=$(basename "$(pwd)")
fi
[ -z "$PROJECT_NAME" ] && PROJECT_NAME="Untitled Project"

# --- Project description ---
PROJECT_DESC=""
if [ -f "README.md" ]; then
  PROJECT_DESC=$(awk '/^# / {found=1; next} found && NF && !/^#/ && !/^\[!/ && !/^\[</ {print; exit}' README.md | xargs)
fi
[ -z "$PROJECT_DESC" ] && PROJECT_DESC="<!-- Replace with your project description -->"

# --- Language/runtime detection ---
PRIMARY_LANG=""; RUNTIME=""; PKG_MANAGER=""
if [ -f "package.json" ] && [ -f "tsconfig.json" ]; then
  PRIMARY_LANG="TypeScript"
  RUNTIME="Node.js \`<!-- run node --version -->\`"
  PKG_MANAGER="npm \`<!-- run npm --version -->\`"
elif [ -f "package.json" ]; then
  PRIMARY_LANG="TypeScript/Node.js"
  RUNTIME="Node.js \`<!-- run node --version -->\`"
  PKG_MANAGER="npm \`<!-- run npm --version -->\`"
elif [ -f "go.mod" ]; then
  PRIMARY_LANG="Go"
  RUNTIME="Go \`<!-- run go version -->\`"
  PKG_MANAGER="go mod \`<!-- run go version -->\`"
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
  PRIMARY_LANG="Python"
  RUNTIME="Python 3.x \`<!-- run python3 --version -->\`"
  PKG_MANAGER="pip/poetry \`<!-- check pyproject.toml -->\`"
elif [ -f "Cargo.toml" ]; then
  PRIMARY_LANG="Rust"
  RUNTIME="Rust \`<!-- run rustc --version -->\`"
  PKG_MANAGER="cargo \`<!-- run cargo --version -->\`"
fi
\`\`\`

### 5.2: Hydrate project.md

\`\`\`bash
if grep -q '<[a-z]' .omp/memory/project/project.md 2>/dev/null; then
  ESCAPED_NAME=$(echo "$PROJECT_NAME" | sed 's/[\/&]/\\&/g')
  ESCAPED_DESC=$(echo "$PROJECT_DESC" | sed 's/[\/&]/\\&/g')
  sed -i "s|# Project: <project-name>|# Project: $ESCAPED_NAME|" .omp/memory/project/project.md
  sed -i "s|<One sentence — what are we building and why?>|$ESCAPED_DESC|" .omp/memory/project/project.md
  sed -i 's|<active | maintenance | paused>|active|' .omp/memory/project/project.md
  sed -i 's|<what we.re working toward right now>|Complete project initialization and setup|' .omp/memory/project/project.md
  sed -i 's|<the next concrete deliverable>|Run /brainstorm to identify first work item|' .omp/memory/project/project.md
  HYDRATED=$((HYDRATED + 1))
  echo "  ✓ project.md"
else
  SKIPPED=$((SKIPPED + 1))
  echo "  - project.md (user content — skipped)"
fi
\`\`\`

### 5.3: Hydrate conventions.md

[... similar guarded sed blocks for conventions.md, decisions.md, tech-stack.md, gotchas.md ...]
```

**Verification:** After editing init.md, `grep -c 'Phase 5: Hydrate Memory Files' .omp/commands/init.md` returns 1. `grep -c 'Phase 5: Check Agent Files' .omp/commands/init.md` returns 0. The file has all 5 memory-file hydration blocks.

**Task 3.2: Add post-hydration scan**

Add Phase 5a that scans for remaining placeholders and reports them. This addresses requirement #5 from the PRD: "detects and reports unresolved placeholders that remain after hydration."

```
# Shape of Phase 5a:

## Phase 5a: Post-Hydration Scan

\`\`\`bash
echo ""
echo "Scanning for remaining placeholders..."
REMAINING=$(grep -rl '<[a-z]' .omp/memory/project/ 2>/dev/null | wc -l)
CRITICAL=$(grep -l '<project-name>\|<what are we building>' .omp/memory/project/*.md 2>/dev/null | wc -l)

if [ "$CRITICAL" -gt 0 ]; then
  echo "  ⚠ WARNING: $CRITICAL file(s) still contain identity placeholders"
  grep -n '<project-name>\|<what are we building>' .omp/memory/project/*.md 2>/dev/null
fi

echo "  Hydrated: $HYDRATED | Skipped: $SKIPPED | Files with remaining placeholders: $REMAINING"
if [ "$REMAINING" -gt 0 ]; then
  echo "  (Remaining placeholders are intentional: verification commands, version numbers, etc.)"
  echo "  Review .omp/memory/project/tech-stack.md and fill in version verification commands."
fi
\`\`\`
```

**Verification:** After Hydrate phase runs, the scan reports `Hydrated: 5` (fresh clone) or `Hydrated: 0, Skipped: 5` (already hydrated). Critical placeholder count is 0.

**Task 3.3: Verify idempotency**

Test that running hydration twice does not overwrite user content. This is a manual verification step, not code to add to init.md.

```
# Test procedure:
# 1. Run /init on a fresh clone → all 5 files hydrated
# 2. Manually edit project.md heading to "My Custom Project"
# 3. Run /init again → observe "project.md (user content — skipped)"
# 4. Verify heading still says "My Custom Project"
```

Verify that the grep guard `grep -q '<[a-z]' .omp/memory/project/project.md` correctly returns false after first hydration (no angle-bracket placeholders remain in project identity fields), preventing the second run from executing sed.

Edge case: If any angle-bracket placeholder remains (e.g., `<version>` in tech-stack.md is replaced with `<!-- run ... -->` comment but the `<Criterion 1>` placeholder in project.md stays), the guard will still trigger on the second run. This is acceptable — it re-hydrates the same placeholders with the same values (idempotent). The guard's purpose is to skip files where a user has removed ALL angle-bracket patterns (fully customized), not to track individual field-level hydration status.

**Verification:** The double-run test above confirms idempotency. The grep guard is tested manually.

**Task 3.4: Update Phase 6 Report**

Add hydration statistics to the Phase 6 report output. This provides user-facing feedback about what happened.

The current Phase 6 report template shows:
```
Workspace: <path>
br version: <version>
Bead prefix: <prefix>
Beads: <N open, M closed>
Backbone: .omp/ <healthy/missing>
Honcho: <configured/not installed>
Next: /brainstorm
```

Add a line after "Backbone:":
```
Memory: <HYDRATED> file(s) hydrated, <SKIPPED> skipped, <REMAINING> placeholders remaining
```

If `HYDRATED` and `SKIPPED` are shell variables scoped to Phase 5, they need to be initialized before the hydration block and accessible in Phase 6. Since `/init` phases run sequentially in the same shell context, this works naturally — initialize `HYDRATED=0; SKIPPED=0` at the top of Phase 5 and reference in Phase 6.

**Verification:** After full `/init` run, the report includes the memory line with correct counts.

## Full Verification

```bash
# 1. Structural: init.md has the right phases
grep -n '^## Phase' .omp/commands/init.md
# Expected: Phase 1-6 lines, Phase 5 is "Hydrate Memory Files", Phase 5a is "Post-Hydration Scan"

# 2. Size: init.md is within expected range
wc -l .omp/commands/init.md
# Expected: 180-220 lines (was ~120)

# 3. No stray template patterns in Phase 5
grep -n 'Check Agent Files' .omp/commands/init.md
# Expected: No matches (old Phase 5 is gone)

# 4. All 5 memory files have hydration blocks
grep -c '### 5\.' .omp/commands/init.md
# Expected: 5 or more (one per memory file + detection + scan)

# 5. Idempotency guard present in every hydration block
grep -c "grep -q '<\[a-z\]'" .omp/commands/init.md
# Expected: 5 (one per memory file)

# 6. Detection variables are set before use
grep -c 'PROJECT_NAME=' .omp/commands/init.md
# Expected: >= 1

# 7. No Python, no npm, no pip, no cargo in Phase 5
sed -n '/^## Phase 5:/,/^## Phase 6:/p' .omp/commands/init.md | grep -E 'python|npm |pip |cargo |node '
# Expected: No matches (except in comments/placeholders like `<!-- run npm --version -->`)

# 8. br sync after artifact writes
# (Run manually or trust the command)

# 9. Dry-run mental trace: trace through Phase 5 logic with current repo state
# Expected: PROJECT_NAME="OMP Beads Template" (from README h1)
# Expected: PRIMARY_LANG="TypeScript/Node.js" (package.json exists, no tsconfig.json)
# Expected: 5 files hydrated

# 10. No writes to files outside .omp/ and .beads/
# Verified by reviewing init.md — all writes target .omp/memory/project/*.md
```
