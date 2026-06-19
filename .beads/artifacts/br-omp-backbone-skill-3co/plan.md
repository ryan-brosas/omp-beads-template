<!-- DENSITY: Filled plan. Template sections are preserved; deeper subsections provide executable handoff detail. -->
# Plan: br-omp-backbone-skill-3co

**Goal:** Update `.omp/AGENTS.md` so its shipped-command inventory matches the ten tracked `.omp/commands/*.md` files, including `/npm-release`, while preserving the eight-command bead lifecycle loop.

## Graph Context

- **Blast radius:** 1 production documentation file for `/ship`: `.omp/AGENTS.md`.
- **Planning artifact blast radius:** 3 bead artifacts created by `/plan`: `plan.md`, `tasks.md`, and `context-capsule.md`.
- **Implementation change type:** 0 new production files, 1 production edit, 0 production deletes.
- **Read-only verification files:** `README.md`, `.omp/commands/npm-release.md`, `.omp/commands/verify.md`, `.omp/commands/review.md`, and tracked `.omp/commands/*.md` inventory.
- **Unblocks:** None reported for this bead.
- **Blocked by:** None. `br dep tree br-omp-backbone-skill-3co --json` returned only the root node.
- **Critical path:** No. `bv --robot-plan --format json` placed this bead in `track-B` as a single actionable item with no downstream unblocks.
- **Forecast:** 52 minutes, confidence 0.5, from `bv --robot-forecast br-omp-backbone-skill-3co --format json`.
- **Graph data hash:** `b28ef101b0539c10` for plan, insights, and forecast; `83e27f60221d` for file hotspots.
- **Insight status:** PageRank, Betweenness, Eigenvector, HITS, Critical, Cycles, KCore, Articulation, and Slack all reported `computed`.
- **Cycles:** Insights reported `Cycles: null`; final verification still runs `br dep cycles --json`.
- **Parallel tracks:** `track-A` is broader related bead `br-omp-backbone-skill-0nc`; `track-B` is this bead.
- **Hotspots touched:** None above the more-than-three-bead threshold. `bv --robot-file-hotspots` listed `.omp/commands/init.md`, `AGENTS.md`, and `README.md` at one bead each; `.omp/AGENTS.md` was not a multi-bead hotspot.
- **Related bead caution:** Do not close, mutate, or absorb `br-omp-backbone-skill-0nc`; this bead is narrower.
- **Tracked command inventory observed:** brainstorm, close, create, init, npm-release, plan, pr, review, ship, verify.
- **Command status observed:** `git status --short .omp/commands` produced no output during planning.

## Observable Truths

1. `.omp/AGENTS.md` Command Reference contains exactly ten command rows after implementation.
2. Every Command Reference row corresponds to one tracked `.omp/commands/<name>.md` file.
3. `/npm-release` appears exactly once in the Command Reference table.
4. `/npm-release` wording marks it as a release helper, not a bead lifecycle phase.
5. The lifecycle arrow chain remains `/brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close`.
6. `/init` remains bootstrap and stays outside the recurring bead loop.
7. The repository tree block says ten command files.
8. The repository tree block lists `npm-release.md`.
9. `README.md` and `.omp/AGENTS.md` document the same ten command names.
10. Inventory verification uses `git ls-files .omp/commands/*.md` as the source of truth.
11. `git status --short .omp/commands` is empty or unrelated untracked commands are explicitly excluded.
12. No `.omp/commands/*.md` file changes in the implementation diff.
13. No `.omp/extensions/*.ts` file changes in the implementation diff.
14. No design file changes in the implementation diff.
15. No memory file changes unless a direct contradiction is discovered and documented.
16. `br lint br-omp-backbone-skill-3co --json` reports zero lint failures before completion.
17. `br dep cycles --json` reports no dependency cycles before completion.
18. `completion-evidence.json` records exact output during `/verify`, not inferred results.

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| prd.md | Problem, scope, requirements, approach, risks, and acceptance criteria | `.beads/artifacts/br-omp-backbone-skill-3co/prd.md` | Have |
| prd.json | Machine-readable mirror of requirements and success criteria | `.beads/artifacts/br-omp-backbone-skill-3co/prd.json` | Have |
| plan.md | Graph-informed wave plan with task outlines and verification commands | `.beads/artifacts/br-omp-backbone-skill-3co/plan.md` | Have after `/plan` |
| tasks.md | Checkbox task decomposition with YAML metadata and verification checks | `.beads/artifacts/br-omp-backbone-skill-3co/tasks.md` | Have after `/plan` |
| context-capsule.md | Concise implementation handoff and file ownership map | `.beads/artifacts/br-omp-backbone-skill-3co/context-capsule.md` | Have after `/plan` |
| completion-evidence.json | Exact verification output after implementation | `.beads/artifacts/br-omp-backbone-skill-3co/completion-evidence.json` | Need during `/verify` |
| review-report.md | Parallel review findings and verdict after verification | `.beads/artifacts/br-omp-backbone-skill-3co/review-report.md` | Need during `/review` |

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | 1.1, 1.2, 1.3, 1.4 | Yes | PRD and PRD JSON exist with no placeholders | Tracked inventory, current AGENTS table, README rows, and tree block are captured before edits |
| 2 | 2.1, 2.2, 2.3 | No | Wave 1 evidence identifies exact stale table and tree locations | `.omp/AGENTS.md` has one release-helper row and tree count/list match tracked files |
| 3 | 3.1, 3.2, 3.3, 3.4 | Yes after Wave 2 | `.omp/AGENTS.md` edit is complete | Set equality, README agreement, scope guard, lifecycle text, and tree block checks pass |
| 4 | 4.1 | No | Wave 3 passes | `/verify` writes `completion-evidence.json`; `/review` can inspect concrete evidence |

## Tasks

### Wave 1: Read-only inventory evidence parallel

**Task 1.1: Capture tracked command inventory**

Run `git ls-files .omp/commands/*.md` and derive the ten tracked command basenames.

- **Files:** `.omp/commands/*.md`
- **Dependencies:** none
- **Parallel:** yes
- **Wave purpose:** read-only inventory evidence
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 1.1 Capture tracked command inventory
inputs:
  - .omp/commands/*.md
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - run git ls-files for .omp/commands/*.md
  - strip path and .md suffix
  - sort basenames
  - require ten names
  - require npm-release in the set
outputs:
  - observed evidence for task 1.1
```

**Verification:** Task 1.1 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

**Task 1.2: Extract `.omp/AGENTS.md` command rows**

Read the Command Reference table and derive documented slash-command names and duplicates.

- **Files:** `.omp/AGENTS.md`
- **Dependencies:** none
- **Parallel:** yes
- **Wave purpose:** read-only inventory evidence
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 1.2 Extract `.omp/AGENTS.md` command rows
inputs:
  - .omp/AGENTS.md
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - read .omp/AGENTS.md Command Reference
  - collect slash command cells
  - detect missing names
  - detect duplicate names
  - keep table columns unchanged
outputs:
  - observed evidence for task 1.2
```

**Verification:** Task 1.2 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

**Task 1.3: Extract README command rows**

Read README workflow table and confirm it already includes `/npm-release`.

- **Files:** `README.md`
- **Dependencies:** none
- **Parallel:** yes
- **Wave purpose:** read-only inventory evidence
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 1.3 Extract README command rows
inputs:
  - README.md
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - read README workflow table
  - collect slash command cells
  - confirm npm-release row exists
  - confirm README says lifecycle plus release helper
  - use README wording as model
outputs:
  - observed evidence for task 1.3
```

**Verification:** Task 1.3 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

**Task 1.4: Locate stale tree block**

Read `.omp/AGENTS.md` repository tree block and identify stale nine-count and missing `npm-release.md`.

- **Files:** `.omp/AGENTS.md`
- **Dependencies:** none
- **Parallel:** yes
- **Wave purpose:** read-only inventory evidence
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 1.4 Locate stale tree block
inputs:
  - .omp/AGENTS.md
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - read .omp/AGENTS.md tree block
  - locate commands directory comment
  - locate wrapped command filename rows
  - record nine-count stale text
  - record missing npm-release.md
outputs:
  - observed evidence for task 1.4
```

**Verification:** Task 1.4 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

### Wave 2: Canonical context edit

**Task 2.1: Add `/npm-release` table row**

Insert one `/npm-release` row with release-helper wording and no lifecycle implication.

- **Files:** `.omp/AGENTS.md`
- **Dependencies:** 1.1,1.2,1.3
- **Parallel:** no
- **Wave purpose:** canonical context edit
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 2.1 Add `/npm-release` table row
inputs:
  - .omp/AGENTS.md
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - insert one /npm-release table row
  - use concise release helper text
  - use em dash for bv commands
  - do not insert into arrow chain
  - do not modify npm-release command file
outputs:
  - observed evidence for task 2.1
```

**Verification:** Task 2.1 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

**Task 2.2: Update command tree count and list**

Change the tree comment to ten command files and include `npm-release.md`.

- **Files:** `.omp/AGENTS.md`
- **Dependencies:** 1.1,1.4
- **Parallel:** no
- **Wave purpose:** canonical context edit
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 2.2 Update command tree count and list
inputs:
  - .omp/AGENTS.md
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - change nine command files to ten command files
  - add npm-release.md to wrapped list
  - keep tree compact
  - do not enumerate unrelated files
  - leave skill and extension rows unchanged
outputs:
  - observed evidence for task 2.2
```

**Verification:** Task 2.2 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

**Task 2.3: Preserve lifecycle semantics**

Re-read the workflow prose and keep `/npm-release` outside the bead loop.

- **Files:** `.omp/AGENTS.md`
- **Dependencies:** 2.1,2.2
- **Parallel:** no
- **Wave purpose:** canonical context edit
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 2.3 Preserve lifecycle semantics
inputs:
  - .omp/AGENTS.md
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - re-read workflow paragraph
  - confirm arrow chain has eight bead commands
  - confirm npm-release absent from arrow chain
  - confirm init is bootstrap
  - tighten nearby prose only if ambiguous
outputs:
  - observed evidence for task 2.3
```

**Verification:** Task 2.3 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

### Wave 3: Verification gate parallel

**Task 3.1: Verify AGENTS inventory equality**

Compare tracked basenames with `.omp/AGENTS.md` command rows and require exact equality.

- **Files:** `.omp/AGENTS.md plus .omp/commands/*.md`
- **Dependencies:** 2.1,2.2,2.3
- **Parallel:** yes
- **Wave purpose:** verification gate
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 3.1 Verify AGENTS inventory equality
inputs:
  - .omp/AGENTS.md plus .omp/commands/*.md
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - run command-set comparison script
  - require missing list empty
  - require extra list empty
  - require duplicate list empty
  - require tracked count ten
outputs:
  - observed evidence for task 3.1
```

**Verification:** Task 3.1 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

**Task 3.2: Verify README agreement**

Compare README workflow commands with `.omp/AGENTS.md` command rows and require exact equality.

- **Files:** `README.md plus .omp/AGENTS.md`
- **Dependencies:** 2.1,2.2,2.3
- **Parallel:** yes
- **Wave purpose:** verification gate
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 3.2 Verify README agreement
inputs:
  - README.md plus .omp/AGENTS.md
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - run README comparison script
  - require both sets equal
  - require both contain npm-release
  - require both contain init
  - do not edit README unless proof requires it
outputs:
  - observed evidence for task 3.2
```

**Verification:** Task 3.2 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

**Task 3.3: Verify scope guard**

Inspect changed files and reject command implementation, extension, design, or memory drift.

- **Files:** `git diff metadata`
- **Dependencies:** 2.1,2.2,2.3
- **Parallel:** yes
- **Wave purpose:** verification gate
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 3.3 Verify scope guard
inputs:
  - git diff metadata
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - inspect git diff name list
  - allow .omp/AGENTS.md
  - allow this bead artifacts
  - reject .omp/commands changes
  - reject .omp/extensions changes
outputs:
  - observed evidence for task 3.3
```

**Verification:** Task 3.3 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

**Task 3.4: Verify tree and lifecycle text**

Read edited ranges and confirm ten command files, `npm-release.md`, and eight-command lifecycle.

- **Files:** `.omp/AGENTS.md`
- **Dependencies:** 2.1,2.2,2.3
- **Parallel:** yes
- **Wave purpose:** verification gate
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 3.4 Verify tree and lifecycle text
inputs:
  - .omp/AGENTS.md
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - read final command table
  - read final tree block
  - confirm ten command files text
  - confirm npm-release.md appears
  - confirm lifecycle excludes release helper
outputs:
  - observed evidence for task 3.4
```

**Verification:** Task 3.4 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

### Wave 4: Evidence handoff

**Task 4.1: Record verification evidence**

During `/verify`, write exact command output to completion-evidence.json after checks pass.

- **Files:** `completion-evidence.json`
- **Dependencies:** 3.1,3.2,3.3,3.4
- **Parallel:** no
- **Wave purpose:** evidence handoff
- **Requirement coverage:**
  - R1: Command Reference table includes every tracked shipped lifecycle command and `/npm-release` exactly once.
  - R2: Workflow narrative separates the eight bead lifecycle loop from bootstrap and release helper commands.
  - R3: Repository tree comment and command file listing match tracked command inventory.
  - R4: README and `.omp/AGENTS.md` agree on shipped command count and names.
  - R5: No untracked `.omp/commands/*.md` file is used as shipped inventory evidence.
  - R6: No unrelated command semantics, workflow gates, or command implementations change.

```text
task 4.1 Record verification evidence
inputs:
  - completion-evidence.json
steps:
  - read only the needed ranges before acting
  - preserve tracked inventory as the source of truth
  - keep release helper wording separate from lifecycle wording
  - avoid command implementation changes
  - record observable evidence
  - run /verify after implementation
  - record exact outputs
  - include br lint output
  - include br dep cycles output
  - include inventory comparison output
outputs:
  - observed evidence for task 4.1
```

**Verification:** Task 4.1 is complete when its evidence is observed and no covered requirement remains contradicted.

**Failure modes to avoid:**
- Counting untracked command files as shipped inventory.
- Treating `/npm-release` as a bead lifecycle phase.
- Editing command implementations for a documentation mismatch.
- Updating README only and leaving `.omp/AGENTS.md` stale.
- Expanding this bead into `br-omp-backbone-skill-0nc`.

## Full Verification

Run these after `/ship`. Expected output descriptions are structural because JSON timestamps and ordering can vary.

```bash
git ls-files .omp/commands/*.md
# Expected: ten tracked paths including .omp/commands/npm-release.md
git status --short .omp/commands
# Expected: no output or explicit unrelated untracked command evidence
python3 - <<'PY'
from pathlib import Path
import re, subprocess
tracked_paths = subprocess.check_output(['git','ls-files','.omp/commands/*.md'], text=True).splitlines()
tracked = sorted(Path(p).stem for p in tracked_paths)
text = Path('.omp/AGENTS.md').read_text()
section = text.split('## Command Reference',1)[1].split('## Workflow Enforcement',1)[0]
documented = sorted(re.findall(r'`/([^`]+)`', section))
duplicates = sorted(x for x in set(documented) if documented.count(x) > 1)
print('tracked', tracked)
print('documented', documented)
print('missing', sorted(set(tracked) - set(documented)))
print('extra', sorted(set(documented) - set(tracked)))
print('duplicates', duplicates)
assert len(tracked) == 10
assert tracked == documented
assert duplicates == []
PY
# Expected: missing empty, extra empty, duplicates empty, assertions succeed
python3 - <<'PY'
from pathlib import Path
text = Path('.omp/AGENTS.md').read_text()
workflow = text.split('## The Workflow',1)[1].split('## Command Reference',1)[0]
assert '/npm-release' not in workflow
assert '/brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close' in workflow
print('lifecycle preserved')
PY
# Expected: lifecycle preserved
python3 - <<'PY'
from pathlib import Path
text = Path('.omp/AGENTS.md').read_text()
tree = text.split('omp-template/',1)[1].split('## Philosophy',1)[0]
assert '10 slash commands' in tree or '10 command files' in tree
assert 'npm-release.md' in tree
print('tree inventory aligned')
PY
# Expected: tree inventory aligned
python3 - <<'PY'
from pathlib import Path
import re
def commands_from_agents():
    text = Path('.omp/AGENTS.md').read_text()
    section = text.split('## Command Reference',1)[1].split('## Workflow Enforcement',1)[0]
    return sorted(re.findall(r'`/([^`]+)`', section))
def commands_from_readme():
    text = Path('README.md').read_text()
    section = text.split('## Workflow',1)[1].split('## Escape hatch',1)[0]
    return sorted(re.findall(r'`/([^`]+)`', section))
print('agents', commands_from_agents())
print('readme', commands_from_readme())
assert commands_from_agents() == commands_from_readme()
PY
# Expected: same ten commands in both lists
python3 - <<'PY'
import subprocess
changed = subprocess.check_output(['git','diff','--name-only'], text=True).splitlines()
allowed_prefix = '.beads/artifacts/br-omp-backbone-skill-3co/'
for path in changed:
    allowed = path == '.omp/AGENTS.md' or path.startswith(allowed_prefix)
    print(path, 'allowed' if allowed else 'unexpected')
    assert allowed
PY
# Expected: only .omp/AGENTS.md and this bead artifacts
br lint br-omp-backbone-skill-3co --json
# Expected: JSON with zero lint errors
br dep cycles --json
# Expected: empty cycle list
br sync --flush-only
# Expected: successful JSONL flush before commit by the phase owner
```

Verification notes:
- R1: verified by the commands above and task gates in Waves 1 through 4.
- R2: verified by the commands above and task gates in Waves 1 through 4.
- R3: verified by the commands above and task gates in Waves 1 through 4.
- R4: verified by the commands above and task gates in Waves 1 through 4.
- R5: verified by the commands above and task gates in Waves 1 through 4.
- R6: verified by the commands above and task gates in Waves 1 through 4.
