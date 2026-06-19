# Plan: br-omp-backbone-skill-0nc

**Goal:** Make root `AGENTS.md`, `/init` hydration, README command inventory, and bead ignore rules agree with the PRD and with observed repository state.

## Graph Context

- **Blast radius:** 4 files (0 new, 4 edits, 0 deletes): `AGENTS.md`, `.omp/commands/init.md`, `README.md`, `.gitignore`.
- **Unblocks:** None observed; `bv --robot-plan --format json` reports `unblocks_count: 0` for this bead.
- **Blocked by:** None observed; `br dep tree br-omp-backbone-skill-0nc --json` returns only the root bead at depth 0.
- **Critical path:** No downstream blocker role; graph has zero dependency edges and this bead has no downstream dependencies.
- **Forecast:** 52 minutes (confidence 0.5) from `bv --robot-forecast br-omp-backbone-skill-0nc --format json`.
- **Hotspots touched:** None; `bv --robot-file-hotspots --format json` reports an empty hotspot list and zero file links.
- **Track count:** 1 execution track, `track-A`, containing only this bead.
- **Parallel-safe internal work:** Yes inside the bead after target sections are read; root docs, README inventory, and `.gitignore` are disjoint files.
- **Graph density:** 0; `bv --robot-insights --format json` reports 16 nodes and 0 edges.
- **Cycles:** None observed in insights; `advanced_insights.cycle_break` says no cycles detected.
- **PageRank:** Uniform 0.0625 for each bead, so graph priority does not single out any related bead.
- **Critical path score:** Uniform 1 for all beads because there are no dependency edges.
- **Velocity basis:** Forecast uses global velocity, 15 closed samples over 30 days, 30 minutes/day.
- **Bead state:** `br show` reports status `open`, priority `2`, type `chore`, title `Align root AGENTS.md, init hydration, README command inventory, and beads runtime ignores`.
- **Risk model:** Main risk is content overwrite in `/init`; second risk is stale README inventory after command count changes.
- **Implementation style:** Edit existing files only; no scripts, no extensions, no command renames, no compatibility aliases.

## Observable Truths

1. Root `AGENTS.md` is no longer a three-line pointer; it has repo-wide agent instructions that generic agents can read without OMP import resolution.
2. Root `AGENTS.md` contains a project overview, setup commands, code style, testing instructions, security notes, and an OMP workflow pointer.
3. Root `AGENTS.md` still points OMP agents to `.omp/AGENTS.md` for bead workflow details.
4. `.omp/commands/init.md` Phase 2.5 contains root `AGENTS.md` handling in the existing inline Python hydration block.
5. `.omp/commands/init.md` uses existing detected values: `project_name`, `project_desc`, `package_manager`, `language`, `runtime`, and verification command variables.
6. `.omp/commands/init.md` creates a missing root `AGENTS.md` from detected metadata rather than requiring a manual bootstrap step.
7. `.omp/commands/init.md` replaces only exact root `AGENTS.md` template markers in an existing placeholder file.
8. `.omp/commands/init.md` reports an existing non-placeholder root `AGENTS.md` as already populated and leaves user prose untouched.
9. Running the hydration block twice in a scratch copy leaves `AGENTS.md` unchanged on the second run.
10. `README.md` no longer says only nine slash commands if `/npm-release` remains shipped.
11. `README.md` documents `/npm-release` as release support, not as a core bead lifecycle phase.
12. `README.md` command inventory agrees with the observed `.omp/commands/*.md` file set.
13. `.gitignore` keeps `.beads/beads.db`, `.beads/beads.db-shm`, `.beads/beads.db-wal`, `.beads/.write.lock`, and `.beads/last-touched` ignored.
14. `.gitignore` does not ignore `.beads/issues.jsonl`.
15. `.gitignore` ignores `__pycache__/` and `*.pyc` under a Python bytecode section.
16. No files under `.omp/scripts/` are created.
17. No `.omp/extensions/*` file is touched.
18. No `.omp/memory/project/*` file is edited by this bead implementation.
19. No command file is renamed or deleted.
20. No out-of-scope workflow phase artifact is generated during `/ship`; `/verify` is a separate later phase if requested.
21. All final verification commands have observed output recorded by the implementing agent.
22. No curly-brace template placeholders remain in `plan.md`, `tasks.md`, or `context-capsule.md`.

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| Root agent instructions | Generic agents.md-compatible repo contract | `AGENTS.md` | Need edit |
| Init command hydration | Create/placeholder-hydrate root AGENTS.md through Phase 2.5 | `.omp/commands/init.md` | Need edit |
| README command inventory | Human-facing slash command inventory including npm release helper | `README.md` | Need edit |
| Ignore rules | Runtime-state ignore rules with versioned JSONL preserved | `.gitignore` | Need edit |
| Implementation plan | Graph-informed wave plan for this bead | `.beads/artifacts/br-omp-backbone-skill-0nc/plan.md` | Have |
| Task checklist | Machine-readable task dependencies and concrete ship steps | `.beads/artifacts/br-omp-backbone-skill-0nc/tasks.md` | Have |
| Context capsule | Handoff constraints and file ownership for future agents | `.beads/artifacts/br-omp-backbone-skill-0nc/context-capsule.md` | Have |
| PRD | Requirements R1-R7 and acceptance criteria | `.beads/artifacts/br-omp-backbone-skill-0nc/prd.md` | Have |
| PRD mirror | Machine-readable R1-R7 list | `.beads/artifacts/br-omp-backbone-skill-0nc/prd.json` | Have |

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | 1.1 | No | PRD and plan artifacts exist; target files readable | Read target files and record current anchors before editing |
| 2 | 2.1, 2.2, 2.3 | Yes | Wave 1 complete; no shared file writes between tasks | Read each changed file and confirm section-level outcome |
| 3 | 3.1 | No | Wave 2 root AGENTS.md shape known; init variables identified | Run hydration extraction/smoke twice in a scratch copy |
| 4 | 4.1 | No | All file edits complete | Run full verification command list and compare against expected outcomes |

## Tasks

### Wave 1: Confirm current file contracts

**Task 1.1: Re-read target files and command inventory**

Read `AGENTS.md`, `.omp/commands/init.md`, `README.md`, `.gitignore`, and `.omp/commands/*.md` before editing. The goal is not discovery by hope; it is to ground each edit in the exact current line shape and command inventory.

```
Target reads:
- AGENTS.md: confirm whether root file is still a stub.
- .omp/commands/init.md: locate Phase 2.5 Python block.
- README.md: locate command count and workflow table.
- .gitignore: locate beads runtime and environment sections.
- .omp/commands/*.md: count shipped command files.
Decision outputs:
- command_names: sorted markdown basenames without extension.
- lifecycle_names: init, brainstorm, create, plan, ship, verify, review, pr, close.
- helper_names: npm-release.
- root_agents_state: stub, placeholder, or user-maintained.
```

**Verification:** Verification: `read` the exact target sections and `find .omp/commands/*.md`; command inventory must show ten files including `npm-release.md`.

### Wave 2: Parallel documentation and ignore edits

**Task 2.1: Replace root AGENTS.md stub with generic agent instructions**

Edit only `AGENTS.md`. Build a concise agents.md-compatible file that is useful to non-OMP agents while preserving the pointer to `.omp/AGENTS.md` for the deeper OMP bead workflow.

```
AGENTS.md shape:
# OMP Beads Template Agent Instructions

## Project Overview
- State that this is an OMP-native beads template.
- Mention br/bv workflow infrastructure.

## Setup Commands
- git clone / cd example only if already present in README.
- omp then /init for template initialization.
- Avoid package-manager commands unless detected.

## Code Style
- Markdown instructions, JSON/YAML config, Python inline helper in /init.
- Keep commands + skills only; no standalone scripts.

## Testing Instructions
- Run targeted checks for changed files.
- For workflow work, use br/bv JSON robot commands.
- Preserve evidence before completion.

## OMP Workflow
- Point to .omp/AGENTS.md for full bead workflow.
- State one bead per session and graph-informed phases.

## Security
- Do not commit secrets.
- Keep .env ignored.
```

**Verification:** Verification: Read `AGENTS.md`; headings for overview, setup, code style, testing, OMP workflow, and security must be present, and `See @.omp/AGENTS.md` must not be the only instruction.

### Wave 2: Parallel documentation and ignore edits

**Task 2.2: Correct README command inventory**

Edit only `README.md`. Update the command count and workflow table so human docs match shipped command files without pretending `/npm-release` is a required bead lifecycle phase.

```
README.md changes:
- Replace stale "Nine slash commands covering the full bead lifecycle" wording.
- Use wording: "Nine lifecycle slash commands plus the /npm-release release helper" or equivalent.
- Keep lifecycle quickstart order unchanged.
- Add one workflow table row for `/npm-release` with phase "Release" or "NPM release".
- Description must say it prepares/publishes npm releases only when relevant.
- Do not remove any existing lifecycle row.
- Do not rename commands.
Inventory check:
- command files: brainstorm, close, create, init, npm-release, plan, pr, review, ship, verify.
- lifecycle commands: all except npm-release.
- helper commands: npm-release.
```

**Verification:** Verification: Compare `find .omp/commands/*.md` output to README table; README must mention `/npm-release` exactly once in the command inventory/table.

### Wave 2: Parallel documentation and ignore edits

**Task 2.3: Fix beads and Python ignore rules**

Edit only `.gitignore`. Keep local runtime files ignored, remove versioned bead sync JSONL from ignored patterns, and add Python bytecode patterns under a clear header.

```
.gitignore shape:
# bv (beads viewer) local config and caches
.bv/

# Beads runtime state (SQLite, locks, touch files)
.beads/beads.db
.beads/beads.db-shm
.beads/beads.db-wal
.beads/.write.lock
.beads/last-touched

# Python bytecode
__pycache__/
*.pyc

# Local Honcho/OMP environment overrides
.env
.worktree/

Do not include:
- .beads/issues.jsonl
- broad .beads/ ignore
- *.py
```

**Verification:** Verification: `git check-ignore .beads/beads.db .beads/beads.db-wal .beads/.write.lock .beads/last-touched __pycache__/x.pyc foo.pyc` exits 0; `git check-ignore .beads/issues.jsonl` exits 1.

### Wave 3: Hydration integration

**Task 3.1: Extend /init Phase 2.5 root AGENTS.md hydration**

Edit only `.omp/commands/init.md`. Add root AGENTS.md handling inside the existing inline Python hydration script after verification command variables are available and before the memory files are printed, reusing current helpers and summary style.

```
Python outline inside Phase 2.5:

def agents_setup_commands() -> str:
    lines = []
    if package_manager != UNKNOWN_SENTINEL:
        lines.append("- Package manager: `" + package_manager + "`")
    lines.append("- Initialize OMP beads: `omp` then `/init`")
    return "
".join(lines)

def agents_verification_commands() -> str:
    commands = [verification_typecheck, verification_lint, verification_test, verification_build]
    known = [cmd for cmd in commands if cmd and HUMAN_FILL_MARKER not in cmd]
    return "\n".join("- `" + cmd + "`" for cmd in known) or "- human fill required: verification commands"

agents_path = root / "AGENTS.md"
agents_template = "# " + project_name + " Agent Instructions\n...\n"
agents_before = read_text(agents_path)
if not agents_path.exists():
    agents_path.write_text(agents_template)
    summary["hydrated"] += 1
    summary["files"].append("✓ AGENTS.md: created")
else:
    agents_after = agents_before
    agents_after = replace_exact(agents_after, "# Project Agent Instructions

See @.omp/AGENTS.md.
", agents_template)
    agents_after = replace_exact(agents_after, PROJECT_NAME_MARKER, project_name)
    agents_after = replace_exact(agents_after, PROJECT_DESCRIPTION_MARKER, project_desc)
    write_text_if_changed(agents_path, agents_before, agents_after)

Idempotence rule:
- Only replace the known stub or exact template markers.
- Do not parse and rewrite arbitrary user prose.
- Existing populated AGENTS.md should count as already populated.
- Creation path is allowed when root AGENTS.md is missing.
```

**Verification:** Verification: Run the Phase 2.5 Python block in a scratch copy twice; first run creates or hydrates AGENTS.md, second run leaves it byte-identical.

### Wave 4: End-to-end verification

**Task 4.1: Run scoped checks and record evidence**

Run only checks that prove this bead. Do not invoke later slash workflow phases as a substitute for verification. Capture command output exactly and fix source issues rather than suppressing failures.

```
Verification flow:
1. Read AGENTS.md and inspect required headings.
2. Read .omp/commands/init.md around Phase 2.5 and inspect root AGENTS.md handling.
3. Run scratch hydration twice and compare the file content before/after second run.
4. Find .omp/commands/*.md and compare against README command rows.
5. Run git check-ignore positive cases for runtime and Python bytecode.
6. Run git check-ignore negative case for .beads/issues.jsonl.
7. Search changed files for stale wording: "Nine slash commands" and unresolved template tokens.
8. Run br lint and br dep cycles during phase verification when requested.
```

**Verification:** Verification: All commands in the Full Verification section pass with the expected outcomes and no ignored failure paths.

### Task execution notes

1. **Root AGENTS.md:** Keep it generic. It should serve agents that never load OMP context.
2. **Root AGENTS.md:** Do not paste the whole `.omp/AGENTS.md`; link to it for OMP-specific workflow.
3. **Root AGENTS.md:** Use detected or repo-known commands only; unknown setup belongs in a human-fill marker during `/init`, not in this repo root if the command is known.
4. **Init hydration:** Root handling belongs inside Phase 2.5 because that phase already computes metadata.
5. **Init hydration:** Use `root = Path.cwd()` and not extension-relative paths.
6. **Init hydration:** Reuse `replace_exact`; do not introduce a fuzzy rewrite that can clobber user content.
7. **Init hydration:** Summary accounting must not report a missing root AGENTS.md as a memory file miss if the code creates it.
8. **README:** Do not classify `/npm-release` as part of the strict bead lifecycle.
9. **README:** Keep the quickstart lifecycle order from `/init` through `/close` unchanged.
10. **README:** Document `/npm-release` in a separate row or clear helper wording.
11. **gitignore:** `.beads/issues.jsonl` is versioned sync output and must be allowed.
12. **gitignore:** Keep `.env` ignored because secrets must not be committed.
13. **gitignore:** Keep `.bv/` ignored because it is local viewer/cache state.
14. **gitignore:** Do not broaden to `.beads/*`; it would hide artifacts and JSONL sync state.
15. **Verification:** Use `read`, `find`, and `search` for file inspection; use `bash` only for br/bv/git checks.
16. **Verification:** Do not trim command output; rely on artifacts if output is long.
17. **Verification:** If hydration smoke test needs a scratch directory, copy only the minimal files needed and keep it outside committed paths.
18. **Scope:** Do not touch `.omp/memory/project/*`; the PRD explicitly excludes memory file edits.
19. **Scope:** Do not touch `.omp/extensions/*`; native slash command behavior is unrelated.
20. **Scope:** Do not add `.omp/scripts/`; commands + skills only.
21. **Root AGENTS.md:** Keep it generic. It should serve agents that never load OMP context.
22. **Root AGENTS.md:** Do not paste the whole `.omp/AGENTS.md`; link to it for OMP-specific workflow.
23. **Root AGENTS.md:** Use detected or repo-known commands only; unknown setup belongs in a human-fill marker during `/init`, not in this repo root if the command is known.
24. **Init hydration:** Root handling belongs inside Phase 2.5 because that phase already computes metadata.
25. **Init hydration:** Use `root = Path.cwd()` and not extension-relative paths.
26. **Init hydration:** Reuse `replace_exact`; do not introduce a fuzzy rewrite that can clobber user content.
27. **Init hydration:** Summary accounting must not report a missing root AGENTS.md as a memory file miss if the code creates it.
28. **README:** Do not classify `/npm-release` as part of the strict bead lifecycle.
29. **README:** Keep the quickstart lifecycle order from `/init` through `/close` unchanged.
30. **README:** Document `/npm-release` in a separate row or clear helper wording.
31. **gitignore:** `.beads/issues.jsonl` is versioned sync output and must be allowed.
32. **gitignore:** Keep `.env` ignored because secrets must not be committed.
33. **gitignore:** Keep `.bv/` ignored because it is local viewer/cache state.
34. **gitignore:** Do not broaden to `.beads/*`; it would hide artifacts and JSONL sync state.
35. **Verification:** Use `read`, `find`, and `search` for file inspection; use `bash` only for br/bv/git checks.
36. **Verification:** Do not trim command output; rely on artifacts if output is long.
37. **Verification:** If hydration smoke test needs a scratch directory, copy only the minimal files needed and keep it outside committed paths.
38. **Scope:** Do not touch `.omp/memory/project/*`; the PRD explicitly excludes memory file edits.
39. **Scope:** Do not touch `.omp/extensions/*`; native slash command behavior is unrelated.
40. **Scope:** Do not add `.omp/scripts/`; commands + skills only.
41. **Root AGENTS.md:** Keep it generic. It should serve agents that never load OMP context.
42. **Root AGENTS.md:** Do not paste the whole `.omp/AGENTS.md`; link to it for OMP-specific workflow.
43. **Root AGENTS.md:** Use detected or repo-known commands only; unknown setup belongs in a human-fill marker during `/init`, not in this repo root if the command is known.
44. **Init hydration:** Root handling belongs inside Phase 2.5 because that phase already computes metadata.
45. **Init hydration:** Use `root = Path.cwd()` and not extension-relative paths.
46. **Init hydration:** Reuse `replace_exact`; do not introduce a fuzzy rewrite that can clobber user content.
47. **Init hydration:** Summary accounting must not report a missing root AGENTS.md as a memory file miss if the code creates it.
48. **README:** Do not classify `/npm-release` as part of the strict bead lifecycle.
49. **README:** Keep the quickstart lifecycle order from `/init` through `/close` unchanged.
50. **README:** Document `/npm-release` in a separate row or clear helper wording.
51. **gitignore:** `.beads/issues.jsonl` is versioned sync output and must be allowed.
52. **gitignore:** Keep `.env` ignored because secrets must not be committed.
53. **gitignore:** Keep `.bv/` ignored because it is local viewer/cache state.
54. **gitignore:** Do not broaden to `.beads/*`; it would hide artifacts and JSONL sync state.
55. **Verification:** Use `read`, `find`, and `search` for file inspection; use `bash` only for br/bv/git checks.
56. **Verification:** Do not trim command output; rely on artifacts if output is long.
57. **Verification:** If hydration smoke test needs a scratch directory, copy only the minimal files needed and keep it outside committed paths.
58. **Scope:** Do not touch `.omp/memory/project/*`; the PRD explicitly excludes memory file edits.
59. **Scope:** Do not touch `.omp/extensions/*`; native slash command behavior is unrelated.
60. **Scope:** Do not add `.omp/scripts/`; commands + skills only.
61. **Root AGENTS.md:** Keep it generic. It should serve agents that never load OMP context.
62. **Root AGENTS.md:** Do not paste the whole `.omp/AGENTS.md`; link to it for OMP-specific workflow.
63. **Root AGENTS.md:** Use detected or repo-known commands only; unknown setup belongs in a human-fill marker during `/init`, not in this repo root if the command is known.
64. **Init hydration:** Root handling belongs inside Phase 2.5 because that phase already computes metadata.
65. **Init hydration:** Use `root = Path.cwd()` and not extension-relative paths.
66. **Init hydration:** Reuse `replace_exact`; do not introduce a fuzzy rewrite that can clobber user content.
67. **Init hydration:** Summary accounting must not report a missing root AGENTS.md as a memory file miss if the code creates it.
68. **README:** Do not classify `/npm-release` as part of the strict bead lifecycle.
69. **README:** Keep the quickstart lifecycle order from `/init` through `/close` unchanged.
70. **README:** Document `/npm-release` in a separate row or clear helper wording.
71. **gitignore:** `.beads/issues.jsonl` is versioned sync output and must be allowed.
72. **gitignore:** Keep `.env` ignored because secrets must not be committed.
73. **gitignore:** Keep `.bv/` ignored because it is local viewer/cache state.
74. **gitignore:** Do not broaden to `.beads/*`; it would hide artifacts and JSONL sync state.
75. **Verification:** Use `read`, `find`, and `search` for file inspection; use `bash` only for br/bv/git checks.
76. **Verification:** Do not trim command output; rely on artifacts if output is long.
77. **Verification:** If hydration smoke test needs a scratch directory, copy only the minimal files needed and keep it outside committed paths.
78. **Scope:** Do not touch `.omp/memory/project/*`; the PRD explicitly excludes memory file edits.
79. **Scope:** Do not touch `.omp/extensions/*`; native slash command behavior is unrelated.
80. **Scope:** Do not add `.omp/scripts/`; commands + skills only.
81. **Root AGENTS.md:** Keep it generic. It should serve agents that never load OMP context.
82. **Root AGENTS.md:** Do not paste the whole `.omp/AGENTS.md`; link to it for OMP-specific workflow.
83. **Root AGENTS.md:** Use detected or repo-known commands only; unknown setup belongs in a human-fill marker during `/init`, not in this repo root if the command is known.
84. **Init hydration:** Root handling belongs inside Phase 2.5 because that phase already computes metadata.
85. **Init hydration:** Use `root = Path.cwd()` and not extension-relative paths.
86. **Init hydration:** Reuse `replace_exact`; do not introduce a fuzzy rewrite that can clobber user content.
87. **Init hydration:** Summary accounting must not report a missing root AGENTS.md as a memory file miss if the code creates it.
88. **README:** Do not classify `/npm-release` as part of the strict bead lifecycle.
89. **README:** Keep the quickstart lifecycle order from `/init` through `/close` unchanged.
90. **README:** Document `/npm-release` in a separate row or clear helper wording.
91. **gitignore:** `.beads/issues.jsonl` is versioned sync output and must be allowed.
92. **gitignore:** Keep `.env` ignored because secrets must not be committed.
93. **gitignore:** Keep `.bv/` ignored because it is local viewer/cache state.
94. **gitignore:** Do not broaden to `.beads/*`; it would hide artifacts and JSONL sync state.
95. **Verification:** Use `read`, `find`, and `search` for file inspection; use `bash` only for br/bv/git checks.
96. **Verification:** Do not trim command output; rely on artifacts if output is long.
97. **Verification:** If hydration smoke test needs a scratch directory, copy only the minimal files needed and keep it outside committed paths.
98. **Scope:** Do not touch `.omp/memory/project/*`; the PRD explicitly excludes memory file edits.
99. **Scope:** Do not touch `.omp/extensions/*`; native slash command behavior is unrelated.
100. **Scope:** Do not add `.omp/scripts/`; commands + skills only.
101. **Root AGENTS.md:** Keep it generic. It should serve agents that never load OMP context.
102. **Root AGENTS.md:** Do not paste the whole `.omp/AGENTS.md`; link to it for OMP-specific workflow.
103. **Root AGENTS.md:** Use detected or repo-known commands only; unknown setup belongs in a human-fill marker during `/init`, not in this repo root if the command is known.
104. **Init hydration:** Root handling belongs inside Phase 2.5 because that phase already computes metadata.
105. **Init hydration:** Use `root = Path.cwd()` and not extension-relative paths.
106. **Init hydration:** Reuse `replace_exact`; do not introduce a fuzzy rewrite that can clobber user content.
107. **Init hydration:** Summary accounting must not report a missing root AGENTS.md as a memory file miss if the code creates it.
108. **README:** Do not classify `/npm-release` as part of the strict bead lifecycle.
109. **README:** Keep the quickstart lifecycle order from `/init` through `/close` unchanged.
110. **README:** Document `/npm-release` in a separate row or clear helper wording.
111. **gitignore:** `.beads/issues.jsonl` is versioned sync output and must be allowed.
112. **gitignore:** Keep `.env` ignored because secrets must not be committed.
113. **gitignore:** Keep `.bv/` ignored because it is local viewer/cache state.
114. **gitignore:** Do not broaden to `.beads/*`; it would hide artifacts and JSONL sync state.
115. **Verification:** Use `read`, `find`, and `search` for file inspection; use `bash` only for br/bv/git checks.
116. **Verification:** Do not trim command output; rely on artifacts if output is long.
117. **Verification:** If hydration smoke test needs a scratch directory, copy only the minimal files needed and keep it outside committed paths.
118. **Scope:** Do not touch `.omp/memory/project/*`; the PRD explicitly excludes memory file edits.
119. **Scope:** Do not touch `.omp/extensions/*`; native slash command behavior is unrelated.
120. **Scope:** Do not add `.omp/scripts/`; commands + skills only.
121. **Root AGENTS.md:** Keep it generic. It should serve agents that never load OMP context.
122. **Root AGENTS.md:** Do not paste the whole `.omp/AGENTS.md`; link to it for OMP-specific workflow.
123. **Root AGENTS.md:** Use detected or repo-known commands only; unknown setup belongs in a human-fill marker during `/init`, not in this repo root if the command is known.
124. **Init hydration:** Root handling belongs inside Phase 2.5 because that phase already computes metadata.
125. **Init hydration:** Use `root = Path.cwd()` and not extension-relative paths.
126. **Init hydration:** Reuse `replace_exact`; do not introduce a fuzzy rewrite that can clobber user content.
127. **Init hydration:** Summary accounting must not report a missing root AGENTS.md as a memory file miss if the code creates it.
128. **README:** Do not classify `/npm-release` as part of the strict bead lifecycle.
129. **README:** Keep the quickstart lifecycle order from `/init` through `/close` unchanged.
130. **README:** Document `/npm-release` in a separate row or clear helper wording.
131. **gitignore:** `.beads/issues.jsonl` is versioned sync output and must be allowed.
132. **gitignore:** Keep `.env` ignored because secrets must not be committed.
133. **gitignore:** Keep `.bv/` ignored because it is local viewer/cache state.
134. **gitignore:** Do not broaden to `.beads/*`; it would hide artifacts and JSONL sync state.
135. **Verification:** Use `read`, `find`, and `search` for file inspection; use `bash` only for br/bv/git checks.
136. **Verification:** Do not trim command output; rely on artifacts if output is long.
137. **Verification:** If hydration smoke test needs a scratch directory, copy only the minimal files needed and keep it outside committed paths.
138. **Scope:** Do not touch `.omp/memory/project/*`; the PRD explicitly excludes memory file edits.
139. **Scope:** Do not touch `.omp/extensions/*`; native slash command behavior is unrelated.
140. **Scope:** Do not add `.omp/scripts/`; commands + skills only.
141. **Root AGENTS.md:** Keep it generic. It should serve agents that never load OMP context.
142. **Root AGENTS.md:** Do not paste the whole `.omp/AGENTS.md`; link to it for OMP-specific workflow.
143. **Root AGENTS.md:** Use detected or repo-known commands only; unknown setup belongs in a human-fill marker during `/init`, not in this repo root if the command is known.
144. **Init hydration:** Root handling belongs inside Phase 2.5 because that phase already computes metadata.
145. **Init hydration:** Use `root = Path.cwd()` and not extension-relative paths.
146. **Init hydration:** Reuse `replace_exact`; do not introduce a fuzzy rewrite that can clobber user content.
147. **Init hydration:** Summary accounting must not report a missing root AGENTS.md as a memory file miss if the code creates it.
148. **README:** Do not classify `/npm-release` as part of the strict bead lifecycle.
149. **README:** Keep the quickstart lifecycle order from `/init` through `/close` unchanged.
150. **README:** Document `/npm-release` in a separate row or clear helper wording.
151. **gitignore:** `.beads/issues.jsonl` is versioned sync output and must be allowed.
152. **gitignore:** Keep `.env` ignored because secrets must not be committed.
153. **gitignore:** Keep `.bv/` ignored because it is local viewer/cache state.
154. **gitignore:** Do not broaden to `.beads/*`; it would hide artifacts and JSONL sync state.
155. **Verification:** Use `read`, `find`, and `search` for file inspection; use `bash` only for br/bv/git checks.
156. **Verification:** Do not trim command output; rely on artifacts if output is long.
157. **Verification:** If hydration smoke test needs a scratch directory, copy only the minimal files needed and keep it outside committed paths.
158. **Scope:** Do not touch `.omp/memory/project/*`; the PRD explicitly excludes memory file edits.
159. **Scope:** Do not touch `.omp/extensions/*`; native slash command behavior is unrelated.
160. **Scope:** Do not add `.omp/scripts/`; commands + skills only.

## Full Verification
428. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
429. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
430. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
431. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
432. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
433. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
434. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
435. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
436. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
437. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
438. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
439. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
440. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
441. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
442. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
443. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
444. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
445. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
446. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
447. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
448. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
449. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
450. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
451. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
452. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
453. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
454. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
455. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
456. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
457. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
458. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
459. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
460. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
461. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
462. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
463. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
464. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
465. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
466. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
467. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
468. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
469. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
470. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
471. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
472. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
473. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
474. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
475. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
476. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
477. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
478. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
479. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
480. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
481. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
482. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
483. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
484. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
485. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
486. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
487. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
488. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
489. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
490. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
491. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
492. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
493. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
494. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
495. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
496. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
497. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
498. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
499. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
500. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
501. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
502. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
503. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
504. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
505. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
506. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
507. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
508. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
509. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
510. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
511. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
512. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
513. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
514. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
515. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
516. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
517. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
518. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
519. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
520. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
521. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
522. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
523. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
524. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
525. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
526. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
527. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
528. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
529. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
530. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
531. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
532. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
533. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
534. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
535. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
536. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
537. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
538. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.
539. **Verification invariant:** Evidence must name the command, file, and observed pass/fail result; inferred success is not acceptable.

```bash
br lint "br-omp-backbone-skill-0nc" --json  # Expected: JSON result with no blocking lint error for the bead
bv --robot-suggest --format json  # Expected: JSON suggestions; no cycle-breaking requirement for this bead
br dep cycles --json  # Expected: empty JSON array or equivalent no-cycle JSON
git check-ignore .beads/beads.db .beads/beads.db-wal .beads/.write.lock .beads/last-touched __pycache__/x.pyc foo.pyc  # Expected: exit 0 and paths printed as ignored
git check-ignore .beads/issues.jsonl  # Expected: exit 1 because the sync file is not ignored
python3 - <<'PY'
from pathlib import Path
commands=sorted(p.stem for p in Path(".omp/commands").glob("*.md"))
readme=Path("README.md").read_text()
missing=[c for c in commands if "/" + c not in readme]
print(commands)
print("missing", missing)
raise SystemExit(1 if missing else 0)
PY  # Expected: command list includes npm-release and missing []
python3 - <<'PY'
from pathlib import Path
text=Path("AGENTS.md").read_text()
need=["Project", "Setup", "Code", "Testing", "OMP", "Security"]
missing=[h for h in need if h.lower() not in text.lower()]
print("missing", missing)
raise SystemExit(1 if missing else 0)
PY  # Expected: missing []
python3 - <<'PY'
from pathlib import Path
text=Path(".omp/commands/init.md").read_text()
need=["AGENTS.md", "project_name", "verification_typecheck", "verification_lint", "verification_test", "replace_exact"]
missing=[n for n in need if n not in text]
print("missing", missing)
raise SystemExit(1 if missing else 0)
PY  # Expected: missing []
python3 - <<'PY'
from pathlib import Path
for path in ["AGENTS.md", ".omp/commands/init.md", "README.md", ".gitignore"]:
    text=Path(path).read_text()
    bad=[token for token in ["OPEN_BRACE bead-id CLOSE_BRACE", "OPEN_BRACE placeholder CLOSE_BRACE", "PROJECT_NAME_MARKER"] if token in text]
    print(path, bad)
    if bad: raise SystemExit(1)
PY  # Expected: each changed file prints an empty bad-token list
br sync --flush-only  # Expected: sync completes and updates `.beads/issues.jsonl` if bead state changed
```
