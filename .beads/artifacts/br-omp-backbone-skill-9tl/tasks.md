# Tasks: Teach /init to hydrate memory/project files from repo state

## 1. Detection Primitives {parallel}

### 1.1 Define project name detection snippet

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 10
```

- [ ] Write the shell snippet that extracts PROJECT_NAME from README.md h1 → git remote origin → directory basename, with fallback to "Untitled Project"
- [ ] Handle markdown link syntax in h1 (`[text](url)` → text via sed)
- [ ] Handle empty/whitespace-only results with the final fallback
- [ ] Test snippet manually against current repo: expect `PROJECT_NAME="OMP Beads Template"`
- [ ] Test snippet in a temp dir without README: expect directory basename
- [ ] Verify: snippet is self-contained (no dependencies on prior init phases), uses only bash builtins, grep, sed, git, basename

### 1.2 Define project description extraction snippet

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 10
```

- [ ] Write the awk snippet that extracts first non-heading, non-badge paragraph after README h1
- [ ] Skip badge/image lines (`[!`, `[<`) and heading lines (`#`)
- [ ] Fall back to `<!-- Replace with your project description -->` if no paragraph found or no README
- [ ] Test snippet against current repo: expect description containing "OMP-native project template with br and bv"
- [ ] Test snippet against a README with only headings and no prose: expect fallback comment
- [ ] Verify: snippet produces exactly one line (no trailing newlines leaking into sed later)

### 1.3 Define language/runtime detection snippet

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 15
```

- [ ] Write the if/elif chain checking lockfile/config presence: package.json+tsconfig.json → TypeScript, package.json alone → TypeScript/Node.js, go.mod → Go, pyproject.toml/requirements.txt → Python, Cargo.toml → Rust, else → placeholder comments
- [ ] Set PRIMARY_LANG, RUNTIME, PKG_MANAGER for each branch with version placeholders as `<!-- run ... -->` comments
- [ ] Test: create temp dir with only package.json → PRIMARY_LANG="TypeScript/Node.js"
- [ ] Test: create temp dir with package.json + tsconfig.json → PRIMARY_LANG="TypeScript"
- [ ] Test: create temp dir with only go.mod → PRIMARY_LANG="Go"
- [ ] Test: create temp dir with only Cargo.toml → PRIMARY_LANG="Rust"
- [ ] Test: empty dir with no lockfiles → all three vars contain `<!-- ... -->` comments
- [ ] Verify: snippet does not invoke node, go, python3, rustc, or any package manager

## 2. Hydration Commands {parallel}

### 2.1 Write project.md hydration block

```yaml
depends_on: ["1.1", "1.2"]
parallel: true
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 15
```

- [ ] Write the guarded sed block that hydrates project.md: heading (PROJECT_NAME), description (PROJECT_DESC), phase status ("active"), milestone text, next deliverable text
- [ ] Escape `/` and `&` in PROJECT_NAME and PROJECT_DESC before sed substitution (use `|` as delimiter, escape `&` with `\&`)
- [ ] Include idempotency guard: `grep -q '<[a-z]' .omp/memory/project/project.md` before sed
- [ ] Increment HYDRATED counter on write, SKIPPED counter on skip
- [ ] Echo status line: "✓ project.md" or "- project.md (user content — skipped)"
- [ ] Test: copy template project.md to temp dir, run snippet with PROJECT_NAME="Test & Co" and PROJECT_DESC="A test/project", verify heading is "# Project: Test & Co" and description is "A test/project"
- [ ] Test: run snippet on already-hydrated file (no `<[a-z]` patterns) → verify skipped
- [ ] Verify: success criteria placeholders (`<Criterion 1>`, `<Criterion 2>`) remain untouched

### 2.2 Write conventions.md hydration block

```yaml
depends_on: ["1.1", "1.3"]
parallel: true
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 15

- [ ] Write the guarded sed block that hydrates conventions.md: heading (PROJECT_NAME), backend language row from PRIMARY_LANG, frontend row (TypeScript if PRIMARY_LANG contains TypeScript, else comment), scripts row ("Bash"), constraint/framework comments
- [ ] Include idempotency guard and counter increments
- [ ] Handle the case where PRIMARY_LANG is a comment (no language detected): leave all table rows as `<!-- ... -->` comments
- [ ] Test with PRIMARY_LANG="TypeScript": backend=TypeScript, frontend=TypeScript, scripts=Bash
- [ ] Test with PRIMARY_LANG="Go": backend=Go, frontend=`<!-- TypeScript | JavaScript -->`, scripts=Bash
- [ ] Test with PRIMARY_LANG unset/comment: all rows left as comment placeholders
- [ ] Verify: no raw `<TypeScript | Go | Rust | Python>` patterns remain in language table rows

### 2.3 Write decisions.md hydration block

```yaml
depends_on: ["1.1"]
parallel: true
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 10
```

- [ ] Write the guarded sed block that hydrates decisions.md: heading (PROJECT_NAME), all `<YYYY-MM>` placeholders → `2026-06`
- [ ] Include idempotency guard and counter increments
- [ ] Test with PROJECT_NAME="My Project": verify heading is "# Decisions: My Project"
- [ ] Test with PROJECT_NAME containing special characters (slashes, ampersands): verify sed handles them
- [ ] Verify: 5 template decisions remain in the table (count decision rows: `grep -c '^| [0-9]' .omp/memory/project/decisions.md` → 6 after hydration: header row + 5 decisions)

### 2.4 Write tech-stack.md hydration block

```yaml
depends_on: ["1.1", "1.3"]
parallel: true
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 15
```

- [ ] Write the guarded sed block that hydrates tech-stack.md: heading (PROJECT_NAME), Language row (PRIMARY_LANG), Runtime row (RUNTIME with inline version comment), Package manager row (PKG_MANAGER with inline version comment), constraint/framework comments
- [ ] Include idempotency guard and counter increments
- [ ] Handle the `\|` alternation in sed patterns (shell escaping of `|` in `<TypeScript \| Python \| Go \| Rust>`)
- [ ] Leave all verification command placeholders untouched (out of scope per PRD)
- [ ] Test with PRIMARY_LANG="Go", RUNTIME="Go `<!-- run go version -->`", PKG_MANAGER="go mod `<!-- run go version -->`"
- [ ] Test with PRIMARY_LANG unset: language/runtime/pkg-mgr rows left as comment placeholders
- [ ] Verify: `<tsc --noEmit | mypy | cargo check | go vet>` and other verification command placeholders remain in the file

### 2.5 Write gotchas.md hydration block

```yaml
depends_on: ["1.1"]
parallel: true
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 10
```

- [ ] Write the guarded sed block that hydrates gotchas.md: heading (PROJECT_NAME), insert "inherited from omp-template" comment above "Template Bootstrap Gotchas" section
- [ ] Include idempotency guard and counter increments
- [ ] The "Active Warnings" table (with `<YYYY-MM>` placeholder row) remains untouched
- [ ] Test: verify heading change and comment insertion
- [ ] Test: run snippet twice → second run skips (comment insertion would duplicate without proper guard; use a marker to prevent double-insertion)
- [ ] Verify: Template Bootstrap Gotchas table (12 rows of gotchas) is fully preserved

## 3. Integration

### 3.1 Replace Phase 5 in init.md

```yaml
depends_on: ["2.1", "2.2", "2.3", "2.4", "2.5"]
parallel: false
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 20
```

- [ ] Read current `.omp/commands/init.md` to locate exact lines of Phase 5 block (lines ~95-101: "Check Agent Files" with the file list)
- [ ] Remove the old Phase 5 block entirely
- [ ] Insert new Phase 5: "Hydrate Memory Files" with subsections 5.1 (detection), 5.2-5.6 (one per memory file)
- [ ] Initialize HYDRATED=0 and SKIPPED=0 at top of Phase 5
- [ ] Insert new Phase 5a: "Post-Hydration Scan" with placeholder scan and warning logic
- [ ] Renumber old Phase 6 to stay as Phase 6 (Phase 5a is a sub-phase, not a renumber)
- [ ] Ensure all code blocks use proper markdown backtick fencing and are syntactically valid shell
- [ ] Verify: `grep -n '^## Phase' .omp/commands/init.md` shows Phase 1-6 in order, Phase 5 is "Hydrate Memory Files", old "Check Agent Files" is gone
- [ ] Verify: `wc -l .omp/commands/init.md` is between 180-220

### 3.2 Add post-hydration scan (Phase 5a)

```yaml
depends_on: ["3.1"]
parallel: false
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 10
```

- [ ] Write the post-hydration scan shell block that greps for remaining `<[a-z]` patterns in memory files
- [ ] Critical check: if `<project-name>` or `<what are we building>` still present, print WARNING with line numbers (indicates a detection/hydration bug)
- [ ] Report: "Hydrated: N | Skipped: M | Files with remaining placeholders: P"
- [ ] If P > 0, print guidance: "Review tech-stack.md and fill in version verification commands"
- [ ] Test mental trace: after full hydration, P should be 0 for project identity fields, non-zero for intentional placeholders (verification commands) — scan logic should distinguish
- [ ] Verify: scan does not error if HYDRATED/SKIPPED variables are unset (first-run scenario where no files were hydrated)

### 3.3 Update Phase 6 Report

```yaml
depends_on: ["3.1", "3.2"]
parallel: false
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 5
```

- [ ] Add "Memory:" line to Phase 6 report output showing HYDRATED, SKIPPED, and remaining placeholder count
- [ ] Ensure HYDRATED and SKIPPED variables initialized before Phase 5 are accessible in Phase 6 (same shell context, sequential phases)
- [ ] Verify: report line is present and correctly references the shell variables

### 3.4 Verify workflow gate exemption

```yaml
depends_on: ["3.1"]
parallel: false
conflicts_with: []
files: [".omp/extensions/workflow-gate.ts"]
estimated_minutes: 5
```

- [ ] Read `.omp/extensions/workflow-gate.ts` (already read — gates exempt `.omp/` and `.beads/` paths)
- [ ] Confirm that `.omp/memory/project/project.md` starts with `.omp/` and therefore passes the gate exemption check: `path.startsWith(".omp/")` is true
- [ ] If the gate path check is prefix-based (it is: `path.startsWith(".omp/")`), no code change needed
- [ ] If the gate path check is exact-match (`path === ".omp"`), add `|| path.startsWith(".omp/")` — but the source shows `path.startsWith(".omp/")` already exists
- [ ] Verify: no gate changes needed; document this in completion evidence

## 4. Verification

### 4.1 Structural verification

```yaml
depends_on: ["3.1", "3.2", "3.3"]
parallel: false
files: [".omp/commands/init.md"]
estimated_minutes: 10
```

- [ ] `grep -n '^## Phase' .omp/commands/init.md` — verify Phase 5 is "Hydrate Memory Files", Phase 5a is "Post-Hydration Scan", Phase 6 is "Report"
- [ ] `grep -c "grep -q '<\[a-z\]'" .omp/commands/init.md` — returns 5 (one idempotency guard per memory file)
- [ ] `grep -c 'PROJECT_NAME=' .omp/commands/init.md` — returns >= 1 (detection variable set)
- [ ] `grep -c 'HYDRATED=' .omp/commands/init.md` — returns >= 1 (counter initialized)
- [ ] `sed -n '/^## Phase 5:/,/^## Phase 6:/p' .omp/commands/init.md | grep -E '\b(python3?|npm |pip |cargo |node |go version|rustc)\b' | grep -v '<!--' | grep -v '^#' | grep -v 'echo'` — returns 0 (no tool invocations in Phase 5, only comments)
- [ ] `wc -l .omp/commands/init.md` — between 180 and 220

### 4.2 Mental trace verification (dry run against current repo)

```yaml
depends_on: ["4.1"]
parallel: false
files: []
estimated_minutes: 10
```

- [ ] Trace Phase 5 detection against omp-template repo: PROJECT_NAME should be "OMP Beads Template" (from README h1), PROJECT_DESC should start with "OMP-native project template", PRIMARY_LANG should be "TypeScript/Node.js" (package.json exists, no tsconfig.json)
- [ ] Trace Phase 5 hydration for each file: what sed commands fire? What placeholders remain?
- [ ] After hydration trace: project.md heading should be "# Project: OMP Beads Template", description filled, success criteria placeholders remain
- [ ] After hydration trace: conventions.md backend row should say "TypeScript/Node.js"
- [ ] After hydration trace: tech-stack.md language row should say "TypeScript/Node.js"
- [ ] After hydration trace: gotchas.md should have demarcation comment
- [ ] Phase 5a trace: critical placeholders count = 0, remaining placeholders = 3-5 (verification commands, version comments)

### 4.3 Full end-to-end verification (on fresh clone or restored templates)

```yaml
depends_on: ["4.2"]
parallel: false
files: []
estimated_minutes: 15
```

- [ ] Backup current memory files: `cp -r .omp/memory/project .omp/memory/project.bak`
- [ ] Restore template placeholders to memory files (or use a fresh clone)
- [ ] Run `/init` and capture Phase 5-5a-6 output
- [ ] Verify: `grep -r '<project-name>' .omp/memory/project/` returns zero matches
- [ ] Verify: `grep -r '<what are we building>' .omp/memory/project/` returns zero matches
- [ ] Verify: `head -3 .omp/memory/project/project.md` shows concrete project name
- [ ] Verify: `grep 'Language' .omp/memory/project/tech-stack.md` does not match `<TypeScript | Python | Go | Rust>`
- [ ] Verify Phase 6 report shows "Memory:" line with correct counts
- [ ] Test idempotency: manually edit project.md heading, run `/init` again, verify edit survives
- [ ] Restore original memory files from backup: `rm -rf .omp/memory/project && mv .omp/memory/project.bak .omp/memory/project`
- [ ] Record all findings in completion-evidence.json

### 4.4 Sync and finalize

```yaml
depends_on: ["4.3"]
parallel: false
files: []
estimated_minutes: 5
```

- [ ] `br sync --flush-only`
- [ ] Confirm all artifacts present in `.beads/artifacts/br-omp-backbone-skill-9tl/`
- [ ] List artifacts: `ls -la .beads/artifacts/br-omp-backbone-skill-9tl/`
- [ ] STOP — do NOT implement, do NOT close bead, do NOT git commit
