# Tasks: br-omp-backbone-skill-nvf

## 1. Source anchoring

### 1.1 Read Phase 2.5 edit ranges

```yaml
depends_on: []
parallel: false
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 5
```

- [ ] Read `.omp/commands/init.md:149-176` and record the current `git_remote_name`, `package_json`, `package_name`, `project_name`, and `project_desc` lines.
- [ ] Read `.omp/commands/init.md:282-320` and record the current `scripts`, `package_script`, `line_or_todo`, `backend_notes`, `frontend_language`, `frontend_notes`, `scripts_language`, and `scripts_notes` lines.
- [ ] Read `.omp/commands/init.md:362-397` and confirm the `project.md` and `conventions.md` `replace_exact` calls are unchanged before editing.
- [ ] Verify: the shipping agent has fresh line numbers and a current file tag before any edit.

### 1.2 Snapshot non-target invariants

```yaml
depends_on: ["1.1"]
parallel: false
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 5
```

- [ ] Identify imports in the embedded Python block and confirm the change needs no new import.
- [ ] Identify `parse_package_json()` and confirm dependency evidence can reuse its result.
- [ ] Identify backend, verification, security, gotchas, and decisions hydration blocks as non-target areas.
- [ ] Verify: write down the non-target anchor names before editing: `backend_notes`, `verification_typecheck`, `verification_lint`, `verification_test`, `verification_build`, `security_audit`, `replace_exact`.

## 2. Project identity and goal

### 2.1 Reorder project_name fallback chain

```yaml
depends_on: ["1.1", "1.2"]
parallel: false
conflicts_with: ["2.2", "3.1", "3.2", "3.3"]
files: [".omp/commands/init.md"]
estimated_minutes: 5
```

- [ ] Edit only the `project_name = (` expression.
- [ ] Move `git_remote_name()` to the first fallback position inside the expression.
- [ ] Keep `package_name` as the second fallback.
- [ ] Keep `first_heading_from_readme()` as the third fallback.
- [ ] Keep `root.name` as the fourth fallback.
- [ ] Keep `"Untitled Project"` as the final fallback.
- [ ] Do not change `git_remote_name()` implementation.
- [ ] Do not change `first_heading_from_readme()` implementation.
- [ ] Do not add normalization, slugifying, or validation.
- [ ] Verify: static inspection shows `git_remote_name()` before `package_name` before `first_heading_from_readme()` in `project_name`.

### 2.2 Make project_desc static TODO marker

```yaml
depends_on: ["2.1"]
parallel: false
conflicts_with: ["3.1", "3.2", "3.3"]
files: [".omp/commands/init.md"]
estimated_minutes: 5
```

- [ ] Edit only the `project_desc` assignment.
- [ ] Replace the README paragraph fallback expression with the exact string `"<!-- TODO: fill in your project goal -->"`.
- [ ] Do not change the `replace_exact` call for `<One sentence — what are we building and why?>`.
- [ ] Do not change success criteria TODO replacements.
- [ ] Do not change current phase TODO replacements.
- [ ] Do not delete `first_paragraph_from_readme()` unless you separately prove no references remain and the diff stays inside Phase 2.5.
- [ ] Verify: `project_desc` has one assignment and the assignment line has no `first_paragraph_from_readme` token.

## 3. Conventions evidence gates

### 3.1 Add package dependency evidence helper

```yaml
depends_on: ["2.2"]
parallel: false
conflicts_with: ["3.2", "3.3"]
files: [".omp/commands/init.md"]
estimated_minutes: 10
```

- [ ] Place a helper near package-derived values, after `package_json` and `package_name` or before Frontend/Scripts assignments.
- [ ] Use signature shape `def has_package_dependency(name: str) -> bool:` or `def has_dep(name: str) -> bool:`.
- [ ] Loop over `dependencies`, `devDependencies`, and `peerDependencies`.
- [ ] For each section, read `deps = package_json.get(section)`.
- [ ] Return `True` only when `deps` is a dict and `name in deps`.
- [ ] Return `False` after the loop.
- [ ] Do not read `package.json` again.
- [ ] Do not allocate a merged dependency dictionary.
- [ ] Do not add imports.
- [ ] Verify: helper returns a boolean and uses only existing `package_json` data.

### 3.2 Gate Frontend language and notes

```yaml
depends_on: ["3.1"]
parallel: false
conflicts_with: ["3.3"]
files: [".omp/commands/init.md"]
estimated_minutes: 15
```

- [ ] Remove the current one-line `frontend_language` inference from backend `language`.
- [ ] Remove the current `frontend_notes` inference from `frontend_language` alone.
- [ ] Define framework evidence using the exact package names `react`, `svelte`, `vue`, `next`, `nuxt`, `astro`, `angular`, and `solid`.
- [ ] Compute `has_frontend_framework` from dependency helper calls.
- [ ] When framework evidence exists, set `frontend_language` to `TypeScript` if `language == "TypeScript"`, otherwise `JavaScript`.
- [ ] When framework evidence exists, set `frontend_notes` to an evidence-based note, not a hard-coded framework convention claim.
- [ ] When framework evidence is absent, set `frontend_language` to `<!-- TODO: fill in -->`.
- [ ] When framework evidence is absent, set `frontend_notes` to `<!-- TODO: fill in -->`.
- [ ] Do not change the Frontend `replace_exact` call in the conventions hydration section.
- [ ] Verify: no frontend framework dependency path leaves both Frontend variables as TODO markers.

### 3.3 Gate Scripts language and notes

```yaml
depends_on: ["3.2"]
parallel: false
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 10
```

- [ ] Remove the current `scripts_language` dictionary keyed by backend `language`.
- [ ] Remove the current `scripts_notes` dictionary keyed by backend `language`.
- [ ] Compute `has_typescript_script_runner` from `tsx` or `ts-node` dependency evidence.
- [ ] When script-runner evidence exists, set `scripts_language` to `TypeScript`.
- [ ] When script-runner evidence exists, set `scripts_notes` to `package scripts and repo automation`.
- [ ] When script-runner evidence is absent, set `scripts_language` to `Bash`.
- [ ] When script-runner evidence is absent, set `scripts_notes` to `<!-- TODO: fill in -->`.
- [ ] Do not infer Python, Go, or Rust scripts from backend language.
- [ ] Do not change `package_script()` or verification command inference dictionaries.
- [ ] Verify: no `tsx` and no `ts-node` path gives Bash language and TODO notes; either dependency gives TypeScript language.

## 4. Verification

### 4.1 Syntax-check embedded Python block

```yaml
depends_on: ["3.3"]
parallel: false
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 5
```

- [ ] Extract the Phase 2.5 Python block from `.omp/commands/init.md`.
- [ ] Compile the extracted string with Python `compile()` without executing hydration writes.
- [ ] Fail on SyntaxError or extraction failure.
- [ ] Verify: command prints `PYTHON_BLOCK_SYNTAX_OK`.

### 4.2 Run behavioral harness cases

```yaml
depends_on: ["4.1"]
parallel: false
conflicts_with: []
files: [".omp/commands/init.md"]
estimated_minutes: 15
```

- [ ] Create a temporary directory or isolated function harness; do not mutate `.omp/memory/project/` in the repo.
- [ ] Case: git remote, package name, README heading all present; project name chooses git remote.
- [ ] Case: no git remote; package name and README heading present; project name chooses package name.
- [ ] Case: no git remote and no package name; README heading present; project name chooses README heading.
- [ ] Case: README paragraph present; project_desc still equals TODO marker.
- [ ] Case: no frontend dependency; Frontend variables are TODO markers.
- [ ] Case: frontend dependency present; Frontend variables are populated from evidence.
- [ ] Case: no `tsx` and no `ts-node`; Scripts language Bash and notes TODO.
- [ ] Case: `tsx` present; Scripts language TypeScript.
- [ ] Case: `ts-node` present; Scripts language TypeScript.
- [ ] Verify: harness exits zero and prints all PASS lines.

### 4.3 Check diff scope and artifact readiness

```yaml
depends_on: ["4.2"]
parallel: false
conflicts_with: []
files: [".omp/commands/init.md", ".beads/artifacts/br-omp-backbone-skill-nvf/plan.md", ".beads/artifacts/br-omp-backbone-skill-nvf/tasks.md", ".beads/artifacts/br-omp-backbone-skill-nvf/context-capsule.md"]
estimated_minutes: 10
```

- [ ] Review `git diff -- .omp/commands/init.md` and confirm only planned Phase 2.5 regions changed.
- [ ] Confirm no `.omp/templates/` files changed.
- [ ] Confirm no `.omp/memory/project/` files changed unless a verification run intentionally executed hydration; if they changed unintentionally, inspect and revert those changes before reporting.
- [ ] Run `br lint br-omp-backbone-skill-nvf --json`.
- [ ] Run `br dep cycles --json` and require no cycles.
- [ ] Run `bv --robot-suggest --format json` and record any hygiene warnings relevant to this bead.
- [ ] Run line-count checks for plan, tasks, PRD, and bundle.
- [ ] Run `br sync --flush-only` after artifact writes.
- [ ] Verify: all required artifacts exist under `.beads/artifacts/br-omp-backbone-skill-nvf/`.

### 4.4 Acceptance checklist

```yaml
depends_on: ["4.3"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 3
```

- [ ] Verify: AC1 project_name order.
- [ ] Verify: AC2 static project_desc.
- [ ] Verify: AC3 frontend framework gate.
- [ ] Verify: AC4 tsx or ts-node scripts gate.
- [ ] Verify: AC5 absent-evidence TODO markers.
- [ ] Verify: AC6 unchanged existing hydration.
- [ ] Verify: AC7 idempotency via replace_exact.

### 4.5 Non-goals checklist

```yaml
depends_on: ["4.3"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 3
```

- [ ] Verify: no new dependency.
- [ ] Verify: no template edit.
- [ ] Verify: no command phase rewrite.
- [ ] Verify: no Honcho config edit.
- [ ] Verify: no design file edit.
- [ ] Verify: no br or bv behavior edit.
- [ ] Verify: no workflow gate edit.

### 4.6 Handoff checklist

```yaml
depends_on: ["4.3"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 3
```

- [ ] Verify: plan artifact present.
- [ ] Verify: tasks artifact present.
- [ ] Verify: context capsule present.
- [ ] Verify: verification commands copied from plan.
- [ ] Verify: file ownership understood.
- [ ] Verify: graph context understood.
- [ ] Verify: next command is /ship br-omp-backbone-skill-nvf.

- [ ] Verification detail 253: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 254: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 255: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 256: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 257: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 258: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 259: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 260: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 261: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 262: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 263: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 264: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 265: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 266: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 267: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 268: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 269: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 270: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 271: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 272: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 273: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 274: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 275: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 276: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 277: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 278: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 279: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 280: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 281: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 282: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 283: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 284: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 285: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 286: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 287: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 288: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 289: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 290: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 291: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 292: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 293: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 294: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 295: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 296: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 297: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 298: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 299: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 300: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 301: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 302: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 303: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 304: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 305: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 306: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 307: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 308: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 309: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 310: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 311: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 312: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 313: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 314: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 315: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 316: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 317: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 318: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 319: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 320: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 321: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 322: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 323: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 324: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 325: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 326: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 327: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 328: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 329: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 330: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 331: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 332: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 333: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 334: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 335: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 336: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 337: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 338: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
- [ ] Verification detail 339: if this check cannot be proven from source inspection or the harness, do not mark the bead ready for `/verify`.
