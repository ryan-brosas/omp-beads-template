# Tasks: Add OMP backbone skill

## T1: Create skill directory

- **Action**: Create `.omp/skills/backbone/` directory.
- **Verification**: `ls -d .omp/skills/backbone/` succeeds.
- **Depends on**: nothing.

## T2: Write backbone SKILL.md

- **Action**: Write `.omp/skills/backbone/SKILL.md` with the following sections:
  1. YAML frontmatter (`name: backbone`, `description: ...`)
  2. Backbone concept (br owns state, bv informs, OMP executes)
  3. Phase routing table (8 phases × columns: command, tools, artifacts, pre-flight)
  4. Artifact layout (canonical directory structure)
  5. Tool decision rules (when br, when bv, when OMP)
  6. Related skills (references with one-line purposes)
  7. Minimum checks (pre-flight checklist)
- **Constraints**: ≤150 lines. Reference other skills; do not duplicate.
- **Depends on**: T1.

## T3: Verify skill discovery

- **Action**: Confirm OMP discovers the new skill.
- **Verification**: `skill://backbone/SKILL.md` is readable. No load errors in `/extensions` output.
- **Depends on**: T2.

## T4: Verify no conflicts

- **Action**: Confirm existing skills (`br`, `bv`, `omp`, `orchestrator`, `verification-before-completion`) still load correctly.
- **Verification**: Each skill is readable via `skill://<name>/SKILL.md`. No warnings in `/extensions`.
- **Depends on**: T2.
