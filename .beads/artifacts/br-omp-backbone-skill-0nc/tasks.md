# Tasks: br-omp-backbone-skill-0nc

## 1. Grounding

### 1.1 Re-read target contracts

```yaml
depends_on: []
parallel: false
conflicts_with: []
files: ["AGENTS.md", ".omp/commands/init.md", "README.md", ".gitignore", ".omp/commands/*.md"]
estimated_minutes: 8
```

- [ ] Read root `AGENTS.md` and confirm whether it is a stub, placeholder, or user-maintained instruction file.
- [ ] Read `.omp/commands/init.md` Phase 2.5 and identify the existing Python helpers and verification variables.
- [ ] Read `README.md` command inventory and workflow table.
- [ ] Read `.gitignore` beads/runtime sections.
- [ ] Find `.omp/commands/*.md` and record command basenames.
- [ ] Classify commands into nine lifecycle commands and one npm release helper.
- [ ] Record that bv file hotspots are empty, so no file has graph hotspot constraints.
- [ ] Verify: Observed file reads and command inventory show ten command files including `npm-release.md`.

## 2. Parallel file edits

### 2.1 Replace root AGENTS.md stub

```yaml
depends_on: ["1.1"]
parallel: true
conflicts_with: ["3.1"]
files: ["AGENTS.md"]
estimated_minutes: 12
```

- [ ] Replace the three-line root stub with a repo-wide Markdown instruction file.
- [ ] Add a project overview that identifies this repository as the OMP Beads Template.
- [ ] Add setup commands that mention opening `omp` and running `/init` for new projects.
- [ ] Add code style guidance for Markdown instructions, JSON/YAML config, and inline Python in `/init`.
- [ ] Add testing instructions that tell agents to run scoped verification before yielding.
- [ ] Add OMP workflow guidance that points to `.omp/AGENTS.md` for full bead rules.
- [ ] Add security guidance to keep secrets out and `.env` ignored.
- [ ] Do not paste all of `.omp/AGENTS.md` into the root file.
- [ ] Do not add OMP-only import syntax as the only useful content.
- [ ] Verify: Read `AGENTS.md`; it contains overview, setup, code style, testing, OMP workflow, and security sections.

### 2.2 Correct README command inventory

```yaml
depends_on: ["1.1"]
parallel: true
conflicts_with: []
files: ["README.md"]
estimated_minutes: 10
```

- [ ] Replace the stale “Nine slash commands” wording.
- [ ] Use wording that says there are nine lifecycle commands plus `/npm-release` release support, or equivalent explicit total inventory.
- [ ] Keep quickstart lifecycle commands in existing order from `/init` through `/close`.
- [ ] Add `/npm-release` to the command table as release-only support.
- [ ] Do not claim `/npm-release` is required for every bead lifecycle.
- [ ] Do not remove any existing lifecycle command row.
- [ ] Do not document commands that are not present in `.omp/commands/`.
- [ ] Verify: A command-file comparison script reports no command basenames missing from README command inventory.

### 2.3 Fix beads and Python ignore rules

```yaml
depends_on: ["1.1"]
parallel: true
conflicts_with: []
files: [".gitignore"]
estimated_minutes: 8
```

- [ ] Keep `.bv/` ignored as local viewer/cache state.
- [ ] Keep `.beads/beads.db` ignored.
- [ ] Keep `.beads/beads.db-shm` ignored.
- [ ] Keep `.beads/beads.db-wal` ignored.
- [ ] Keep `.beads/.write.lock` ignored.
- [ ] Keep `.beads/last-touched` ignored.
- [ ] Remove `.beads/issues.jsonl` from ignored patterns.
- [ ] Add a `# Python bytecode` section.
- [ ] Add `__pycache__/` under Python bytecode.
- [ ] Add `*.pyc` under Python bytecode.
- [ ] Keep `.env` ignored.
- [ ] Do not add broad `.beads/` or `*.py` patterns.
- [ ] Verify: `git check-ignore` accepts runtime and bytecode paths, and `git check-ignore .beads/issues.jsonl` exits non-zero.

## 3. Hydration integration

### 3.1 Extend init root AGENTS hydration

```yaml
depends_on: ["2.1"]
parallel: false
conflicts_with: ["2.1"]
files: [".omp/commands/init.md"]
estimated_minutes: 18
```

- [ ] Add root `AGENTS.md` handling inside the existing Phase 2.5 Python block.
- [ ] Place the logic after `verification_typecheck`, `verification_lint`, `verification_test`, and `verification_build` are computed.
- [ ] Reuse `root = Path.cwd()` to resolve `AGENTS.md`.
- [ ] Reuse `read_text`, `write_text_if_changed`, and `replace_exact` where they fit.
- [ ] Build the generated root content from `project_name` and `project_desc`.
- [ ] Include detected `package_manager`, `language`, and `runtime` in generated guidance when known.
- [ ] Include detected verification commands when known.
- [ ] Create root `AGENTS.md` when missing.
- [ ] Replace only the known current stub or exact template markers when the file already exists.
- [ ] Leave arbitrary user-maintained root content unchanged.
- [ ] Make summary output distinguish created, hydrated, and already-populated root AGENTS states.
- [ ] Do not count a created root `AGENTS.md` as a missing memory file.
- [ ] Do not add a standalone script or new command file.
- [ ] Do not change memory file hydration behavior except for shared helper reuse if unavoidable.
- [ ] Verify: Run the Phase 2.5 hydration block twice in a scratch copy and prove the second run leaves `AGENTS.md` byte-identical.

## 4. Verification

### 4.1 Run scoped verification gates

```yaml
depends_on: ["2.1", "2.2", "2.3", "3.1"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 14
```

- [ ] Run `br lint "br-omp-backbone-skill-0nc" --json` and inspect JSON output.
- [ ] Run `bv --robot-suggest --format json` and inspect suggestions.
- [ ] Run `br dep cycles --json` and confirm no cycles.
- [ ] Run positive `git check-ignore` checks for `.beads/beads.db`, `.beads/beads.db-wal`, `.beads/.write.lock`, `.beads/last-touched`, `__pycache__/x.pyc`, and `foo.pyc`.
- [ ] Run negative `git check-ignore .beads/issues.jsonl` and confirm it is not ignored.
- [ ] Run README command inventory script and confirm no command file is missing from README.
- [ ] Run root AGENTS heading script and confirm all required sections are present.
- [ ] Run init-hydration token script and confirm `AGENTS.md` root handling uses expected variables/helpers.
- [ ] Search changed files for stale “Nine slash commands” wording.
- [ ] Search changed files for unresolved curly-brace template placeholders.
- [ ] Run `br sync --flush-only` after any bead state mutation.
- [ ] Verify: All verification commands match expected output; no failures are suppressed or trimmed.

## 5. Root AGENTS.md acceptance details

- [ ] Confirm first heading names the project or template plainly.
- [ ] Confirm overview states this repository is a template, not an application runtime.
- [ ] Confirm setup commands do not fabricate package-manager installs absent from repo evidence.
- [ ] Confirm setup commands tell fresh agents to run `/init` inside `omp`.
- [ ] Confirm code style mentions Markdown, JSON/YAML, and inline Python command helpers.
- [ ] Confirm testing section says to run targeted checks for changed files.
- [ ] Confirm OMP workflow section names br and bv.
- [ ] Confirm OMP workflow section points to `.omp/AGENTS.md`.
- [ ] Confirm security section says not to commit secrets.
- [ ] Confirm `.env` remains ignored.

## 6. README acceptance details

- [ ] Confirm `/init` row remains present.
- [ ] Confirm `/brainstorm` row remains present.
- [ ] Confirm `/create` row remains present.
- [ ] Confirm `/plan` row remains present.
- [ ] Confirm `/ship` row remains present.
- [ ] Confirm `/verify` row remains present.
- [ ] Confirm `/review` row remains present.
- [ ] Confirm `/pr` row remains present.
- [ ] Confirm `/close` row remains present.
- [ ] Confirm `/npm-release` row is present and release-scoped.
- [ ] Confirm README does not say “Nine slash commands” without qualifying npm release support.

## 7. Init hydration acceptance details

- [ ] Confirm no `.omp/scripts/` directory is introduced.
- [ ] Confirm root AGENTS path is `root / "AGENTS.md"`.
- [ ] Confirm root creation path writes full usable Markdown.
- [ ] Confirm existing-stub path replaces the known three-line stub.
- [ ] Confirm placeholder path replaces exact markers only.
- [ ] Confirm arbitrary populated root content is left unchanged.
- [ ] Confirm verification command list omits unknown commands or marks them explicitly.
- [ ] Confirm generated content includes `.omp/AGENTS.md` pointer.
- [ ] Confirm generated content includes setup guidance.
- [ ] Confirm generated content includes testing guidance.
- [ ] Confirm generated content includes security guidance.
- [ ] Confirm second hydration run is byte-identical.

## 8. Gitignore acceptance details

- [ ] Confirm `.beads/issues.jsonl` is absent from `.gitignore`.
- [ ] Confirm `.beads/beads.db` is present.
- [ ] Confirm `.beads/beads.db-shm` is present.
- [ ] Confirm `.beads/beads.db-wal` is present.
- [ ] Confirm `.beads/.write.lock` is present.
- [ ] Confirm `.beads/last-touched` is present.
- [ ] Confirm `__pycache__/` is present.
- [ ] Confirm `*.pyc` is present.
- [ ] Confirm `.env` is present.
- [ ] Confirm no broad `.beads/` pattern is present.

- [ ] Verification evidence item 197: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 198: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 199: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 200: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 201: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 202: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 203: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 204: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 205: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 206: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 207: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 208: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 209: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 210: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 211: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 212: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 213: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 214: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 215: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 216: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 217: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 218: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 219: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 220: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 221: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 222: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 223: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 224: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 225: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 226: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 227: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 228: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 229: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 230: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 231: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 232: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 233: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 234: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 235: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 236: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 237: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 238: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 239: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 240: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 241: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 242: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 243: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 244: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 245: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 246: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 247: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 248: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 249: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 250: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 251: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 252: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 253: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 254: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 255: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 256: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 257: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 258: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 259: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 260: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 261: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 262: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 263: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 264: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 265: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 266: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 267: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 268: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 269: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 270: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 271: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 272: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 273: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 274: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 275: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 276: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 277: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 278: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 279: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 280: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 281: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 282: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 283: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 284: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 285: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 286: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 287: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 288: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 289: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 290: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 291: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 292: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 293: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 294: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 295: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 296: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 297: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 298: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 299: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 300: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 301: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 302: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 303: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 304: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 305: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 306: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 307: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 308: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 309: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 310: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 311: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 312: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 313: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 314: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 315: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 316: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 317: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 318: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 319: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 320: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 321: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 322: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 323: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 324: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 325: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 326: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 327: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 328: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
- [ ] Verification evidence item 329: record the exact command and observed result in the later `/verify` artifact if this check is run during verification.
