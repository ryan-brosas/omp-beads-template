# Tasks: br-omp-backbone-skill-3co

## 1. Inventory discovery

### 1.1 Capture tracked command inventory parallel

```yaml
depends_on: []
parallel: true
conflicts_with: []
files:
  - ".omp/commands/*.md"
estimated_minutes: 6
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] Use tracked files to derive shipped command basenames.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Run `git ls-files .omp/commands/*.md` during implementation verification.
- [ ] Expect exactly ten tracked command files.
- [ ] Expect `.omp/commands/npm-release.md` in the tracked inventory.
- [ ] Strip `.md` suffixes for comparison.
- [ ] Sort basenames before comparing.
- [ ] Treat dirty or untracked command files as separate evidence.
- [ ] Verify: Task 1.1 evidence is observed and no covered requirement remains unverified.

### 1.2 Extract canonical command rows parallel

```yaml
depends_on: []
parallel: true
conflicts_with: []
files:
  - ".omp/AGENTS.md"
estimated_minutes: 6
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] Parse the Command Reference table and identify missing, extra, or duplicate slash commands.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Read `.omp/AGENTS.md` Command Reference table.
- [ ] Extract only backtick slash-command cells.
- [ ] Expect `/npm-release` missing before the fix.
- [ ] Identify duplicate rows if any.
- [ ] Keep table headers and column count unchanged.
- [ ] Prepare the smallest insertion point.
- [ ] Verify: Task 1.2 evidence is observed and no covered requirement remains unverified.

### 1.3 Extract README command rows parallel

```yaml
depends_on: []
parallel: true
conflicts_with: []
files:
  - "README.md"
estimated_minutes: 5
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] Parse README workflow rows and confirm README already documents `/npm-release`.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Read README workflow table.
- [ ] Confirm README includes `/npm-release`.
- [ ] Confirm README says lifecycle plus release helper.
- [ ] Use README release-helper wording as the wording model.
- [ ] Do not rewrite README structure.
- [ ] Use README as consistency evidence, not the primary edit target.
- [ ] Verify: Task 1.3 evidence is observed and no covered requirement remains unverified.

### 1.4 Locate stale tree block parallel

```yaml
depends_on: []
parallel: true
conflicts_with: []
files:
  - ".omp/AGENTS.md"
estimated_minutes: 5
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] Find the repository tree block count and command filename list that need correction.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Read `.omp/AGENTS.md` repository tree block.
- [ ] Confirm current stale text says nine slash commands.
- [ ] Confirm current list omits `npm-release.md`.
- [ ] Prepare the smallest tree edit.
- [ ] Keep unrelated tree rows unchanged.
- [ ] Do not expand the tree into a full directory listing.
- [ ] Verify: Task 1.4 evidence is observed and no covered requirement remains unverified.

## 2. Canonical context edit

### 2.1 Add npm-release table row

```yaml
depends_on: ["1.1", "1.2", "1.3"]
parallel: false
conflicts_with: ["2.2", "2.3"]
files:
  - ".omp/AGENTS.md"
estimated_minutes: 8
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] Insert one `/npm-release` Command Reference row with release-helper wording.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Add exactly one `/npm-release` row.
- [ ] Use the description: Cut an npm release through GitHub Releases and trusted publishing.
- [ ] Set Reads to package and release state or concise equivalent.
- [ ] Set Writes to version, tag, and release state or concise equivalent.
- [ ] Set bv Commands to em dash because release publishing is not graph planning.
- [ ] Do not move `/npm-release` into the lifecycle prose.
- [ ] Verify: Task 2.1 evidence is observed and no covered requirement remains unverified.

### 2.2 Update command tree count

```yaml
depends_on: ["1.1", "1.4"]
parallel: false
conflicts_with: ["2.1", "2.3"]
files:
  - ".omp/AGENTS.md"
estimated_minutes: 7
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] Change the tree count to ten command files and add `npm-release.md`.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Change the commands comment from nine to ten command files.
- [ ] Add `npm-release.md` to the wrapped command filename list.
- [ ] Keep wrapping readable.
- [ ] Do not change skill, extension, template, or memory tree rows.
- [ ] Do not alter root README artifact layout.
- [ ] Ensure the count matches tracked inventory.
- [ ] Verify: Task 2.2 evidence is observed and no covered requirement remains unverified.

### 2.3 Preserve lifecycle semantics

```yaml
depends_on: ["2.1", "2.2"]
parallel: false
conflicts_with: ["2.1", "2.2"]
files:
  - ".omp/AGENTS.md"
estimated_minutes: 4
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] Confirm the lifecycle arrow chain remains the eight bead commands only.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Re-read workflow prose after editing.
- [ ] Confirm the arrow chain has exactly eight bead commands.
- [ ] Confirm `/npm-release` is absent from the arrow chain.
- [ ] Confirm `/init` remains outside the arrow chain.
- [ ] Confirm helper commands are distinguishable from lifecycle commands.
- [ ] Tighten only nearby prose if ambiguity remains.
- [ ] Verify: Task 2.3 evidence is observed and no covered requirement remains unverified.

## 3. Verification

### 3.1 Verify AGENTS inventory equality parallel

```yaml
depends_on: ["2.1", "2.2", "2.3"]
parallel: true
conflicts_with: []
files:
  - ".omp/AGENTS.md"
  - ".omp/commands/*.md"
estimated_minutes: 8
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] Compare tracked command basenames with `.omp/AGENTS.md` command rows.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Run the command-set comparison script from `plan.md`.
- [ ] Require missing list empty.
- [ ] Require extra list empty.
- [ ] Require duplicates list empty.
- [ ] Require tracked command count ten.
- [ ] Do not pass from visual inspection alone.
- [ ] Verify: Task 3.1 evidence is observed and no covered requirement remains unverified.

### 3.2 Verify README agreement parallel

```yaml
depends_on: ["2.1", "2.2", "2.3"]
parallel: true
conflicts_with: []
files:
  - "README.md"
  - ".omp/AGENTS.md"
estimated_minutes: 7
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] Compare README command rows with `.omp/AGENTS.md` command rows.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Run the README agreement script from `plan.md`.
- [ ] Require both outputs to contain `npm-release`.
- [ ] Require both outputs to contain `init`.
- [ ] Require both outputs to contain all eight bead lifecycle commands.
- [ ] If README differs, decide against tracked inventory.
- [ ] Do not edit README unless the proof requires it.
- [ ] Verify: Task 3.2 evidence is observed and no covered requirement remains unverified.

### 3.3 Verify scope guard parallel

```yaml
depends_on: ["2.1", "2.2", "2.3"]
parallel: true
conflicts_with: []
files:
  - ".omp/AGENTS.md"
estimated_minutes: 5
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] Inspect changed paths and reject unrelated command, extension, design, or memory edits.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Inspect `git diff --name-only`.
- [ ] Allow `.omp/AGENTS.md` as the production documentation edit.
- [ ] Allow only this bead artifact files under `.beads/artifacts/br-omp-backbone-skill-3co/`.
- [ ] Fail if `.omp/commands/*.md` changed.
- [ ] Fail if `.omp/extensions/*.ts` changed.
- [ ] Fail if design or memory files changed without scope expansion.
- [ ] Verify: Task 3.3 evidence is observed and no covered requirement remains unverified.

### 3.4 Verify tree and lifecycle text parallel

```yaml
depends_on: ["2.1", "2.2", "2.3"]
parallel: true
conflicts_with: []
files:
  - ".omp/AGENTS.md"
estimated_minutes: 6
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] Read final `.omp/AGENTS.md` ranges and confirm tree and lifecycle invariants.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Read final command table.
- [ ] Read final tree block.
- [ ] Confirm tree text says ten command files or ten slash commands.
- [ ] Confirm tree text lists `npm-release.md`.
- [ ] Confirm lifecycle text excludes release helper.
- [ ] Confirm table columns remain visually consistent.
- [ ] Verify: Task 3.4 evidence is observed and no covered requirement remains unverified.

## 4. Evidence handoff

### 4.1 Record implementation evidence

```yaml
depends_on: ["3.1", "3.2", "3.3", "3.4"]
parallel: false
conflicts_with: []
files:
  - ".beads/artifacts/br-omp-backbone-skill-3co/completion-evidence.json"
estimated_minutes: 6
```

- [ ] Read the listed files or ranges before acting.
- [ ] Keep the work scoped to `br-omp-backbone-skill-3co`.
- [ ] During `/verify`, record exact command output after implementation passes.
- [ ] Use tracked command inventory as the shipped-command source of truth.
- [ ] Do not count untracked command files as shipped inventory.
- [ ] Keep `/npm-release` separate from the eight-command bead lifecycle loop.
- [ ] Keep `/init` documented as bootstrap.
- [ ] Do not modify `.omp/commands/*.md` implementations.
- [ ] Do not modify `.omp/extensions/workflow-gate.ts`.
- [ ] Do not modify design assets.
- [ ] Do not modify memory files unless a direct contradiction is found and explicitly recorded.
- [ ] Do not close, update, or absorb `br-omp-backbone-skill-0nc`.
- [ ] Record concrete evidence for the task.
- [ ] Stop if evidence contradicts the PRD scope.
- [ ] Create `completion-evidence.json` during `/verify`, not during `/plan`.
- [ ] Record actual command outputs and return codes.
- [ ] Include `br lint` output.
- [ ] Include `br dep cycles` output.
- [ ] Include inventory comparison output.
- [ ] Include README agreement and scope diff output.
- [ ] Verify: Task 4.1 evidence is observed and no covered requirement remains unverified.

- [ ] Cross-check 1: Task 1.1 keeps `.omp/commands/*.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 2: Task 1.2 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 3: Task 1.3 keeps `README.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 4: Task 1.4 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 5: Task 2.1 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 6: Task 2.2 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 7: Task 2.3 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 8: Task 3.1 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 9: Task 3.2 keeps `README.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 10: Task 3.3 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 11: Task 3.4 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 12: Task 4.1 keeps `.beads/artifacts/br-omp-backbone-skill-3co/completion-evidence.json` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 13: Task 1.1 keeps `.omp/commands/*.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 14: Task 1.2 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 15: Task 1.3 keeps `README.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 16: Task 1.4 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 17: Task 2.1 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 18: Task 2.2 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 19: Task 2.3 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 20: Task 3.1 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 21: Task 3.2 keeps `README.md` inside ownership and avoids unrelated cleanup.
- [ ] Cross-check 22: Task 3.3 keeps `.omp/AGENTS.md` inside ownership and avoids unrelated cleanup.
