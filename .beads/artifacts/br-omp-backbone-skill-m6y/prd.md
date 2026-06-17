<!-- DENSITY: Minimum 600 lines. No upper bound — be thorough. <600 = incomplete (missing sections, hand-wavy, no real technical context). This is an AI handoff document — the next agent reads only this. -->
# PRD: Post-Review Cleanup — Fix Codex Findings, Trim Conventions, Harden Success Criteria

**Bead:** br-omp-backbone-skill-m6y | **Type:** task | **Priority:** P2
**Created:** 2026-06-17 | **Estimate:** 30m

## Problem

The repository has accumulated 5 distinct quality issues surfaced during the vui bead review cycle and Codex automated review on PR #2. These are all low-risk but collectively undermine agent reliability by wasting context tokens, providing contradictory guidance, and creating false positives in self-checks.

### 1. conventions.md Exceeds Tier 1 Size Target (7KB vs 4KB limit)

`conventions.md` is always inlined into AGENTS.md — every agent session pays the cost of reading it. The documented target is ≤4KB (from conventions.md line 170: "Target ≤1KB for project.md, ≤4KB for conventions.md, ≤2KB for other Tier 1 files"). Current conventions.md size: 6,996 bytes (7KB).

The primary culprit is the **UI Design section** (lines 97-130, ~1,830 bytes) which duplicates content already present in the design-system skill files:

- Animation philosophy (easing, durations, accordion pattern, scale floor, mount strategy) → already in `.omp/skills/design-system/craft/animation-discipline.md`
- Component variants (button variants, focus rings) → already in `.omp/skills/design-system/DESIGN.md` and `.omp/skills/design-system/primitives.css`
- Theme rules (light default, dark counterpart) → already in `.omp/skills/design-system/DESIGN.md` and `.omp/skills/design-system/tokens.css`
- Icon rules (sizing, aria-label, emoji prohibition) → partially in `.omp/skills/design-system/DESIGN.md`, partially unique to conventions

Additionally, the UI Design section has two empty headers (`### CSS Ownership` at line 112, `### Craft Rules` at line 118) — dead weight.

**Impact:** Every agent session — even non-UI sessions — loads ~1,830 bytes of duplicated animation rules, button variants, focus ring conventions, and icon sizing. The Codex automated reviewer flagged this as a P2 issue on PR #2 (comment at conventions.md line 101: "Move bulky UI rules out of Tier 1 memory").

### 2. Self-Matching Grep in project.md Success Criteria

`project.md` line 14 contains:

```
1. **Zero `<project-name>` or template placeholders in any `.omp/memory/project/` file** — `grep -r '<project-name>' .omp/memory/project/` returns no matches
```

Running the prescribed `grep -r '<project-name>' .omp/memory/project/` matches this very line in project.md. The success criterion cannot pass as written — even after all real placeholders are removed from other files, the criterion text itself is a false positive.

**Impact:** Agents told to verify success criteria cannot distinguish between "real placeholder in another file" and "self-referential mention in the criterion." Any automated verification script following the instructions verbatim will report a failure. The Codex automated reviewer flagged this as a P2 issue on PR #2 (comment at project.md line 14).

### 3. tech-stack.md Contains Non-Executable Shell Commands

The "Verification Commands" and "Security" sections use `N/A — ...` as shell commands inside `bash` fenced code blocks:

```bash
# Typecheck
N/A — template repo, no application code

# Lint  
N/A — template repo, no application code

# Test
N/A — template repo, no application code
```

Agents or scripts copying these commands verbatim get `N/A: command not found`. The Codex reviewer flagged this (comment at tech-stack.md line 30: "Make no-op checks valid shell commands").

**Impact:** Copy-paste execution failures when agents follow the documented verification pipeline. The fix is trivial — replace each `N/A —` with `true  #` or `:`.

### 4. Tree Diagram in AGENTS.md is Incomplete

The repository tree diagram in AGENTS.md (lines 211-265) shows `.omp/templates/` with only 5 entries:

```
├── templates/                     # Artifact templates
│   ├── prd.md
│   ├── plan.md
│   ├── tasks.md
│   ├── context-capsule.md
│   └── review-report.md
```

Actual `.omp/templates/` directory contains 9 files:

```
completion-evidence.json
context-capsule.md
decisions.md
plan.md
prd.json
prd.md
progress.txt
review-report.md
tasks.md
```

Missing from tree: `prd.json`, `decisions.md`, `completion-evidence.json`, `progress.txt`. The Codex reviewer flagged this (comment at AGENTS.md line 236: "Keep required artifact templates visible").

**Impact:** Agents relying on the tree as their canonical map miss template files during setup or handoff. The `/verify` command explicitly reads `.omp/templates/completion-evidence.json`, but the tree doesn't show it.

### 5. project.md Current Phase is Stale

The "Current Phase" section still references bead `br-omp-backbone-skill-1da`:

```
- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Workflow verification — run a full /brainstorm → ... cycle
```

Two beads have been completed since 1da: `br-omp-backbone-skill-nvf` (init.md hydration fixes) and `br-omp-backbone-skill-vui` (design system migration, density gate sync, git-clean registration). The phase should reflect the current state of the project.

**Impact:** Agents reading project.md to understand "what is the project doing right now" get stale information. The documented 3-second comprehension goal is undermined.

### Root Cause Analysis

These issues share a common root cause: **no "done means done" checklist for bead completion.** Each bead's `/close` phase should include a check for staleness in memory files and a review of downstream consistency. The conventions.md section on Memory File Maintenance (lines 79-95) says "Update on `/close` — every bead completion checks if conventions/decisions/gotchas changed" but doesn't prescribe specific checks. Adding concrete checks would prevent rot accumulation.

## Goals

1. **Primary:** Reduce conventions.md to ≤4,500 bytes by moving UI Design content to `.omp/skills/design-system/SKILL.md` and pruning empty headers
2. **Secondary:** Fix the self-matching grep in project.md success criterion #1
3. **Tertiary:** Replace all `N/A — ...` with `true  # ...` no-ops in tech-stack.md bash blocks
4. **Quality:** Complete the AGENTS.md tree diagram with all 9 template files
5. **Maintenance:** Update project.md current phase to reflect completed beads and current state

## Non-Goals

- Do NOT modify the design system content itself (DESIGN.md, tokens.css, primitives.css, base.css, craft/*.md) — content is authoritative
- Do NOT change the conventions.md structure beyond the UI Design section relocation
- Do NOT add new templates or remove existing ones
- Do NOT change the density gate threshold or enforcement logic
- Do NOT modify any `.omp/commands/*.md` files (their content is stable from vui bead)
- Do NOT retroactively fix Codex findings on closed bead artifacts (those are historical)
- Do NOT add automated staleness checks to `/close` (separate bead for that process change)

## Scope

### Files Changed

| # | File | Change | Lines |
|---|------|--------|-------|
| 1 | `.omp/memory/project/conventions.md` | Delete UI Design section (lines 97-130); add short pointer to design-system skill | -35, +3 |
| 2 | `.omp/memory/project/project.md` | Fix self-matching grep (line 14); update Current Phase (lines 22-26) | ~8 changed |
| 3 | `.omp/memory/project/tech-stack.md` | Replace `N/A —` with `true  #` in bash blocks (lines 30-39, 52-55) | ~10 changed |
| 4 | `.omp/AGENTS.md` | Add missing templates to tree diagram (lines 246-251 area) | +4 |
| 5 | `.omp/skills/design-system/SKILL.md` | Append UI Design rules from conventions.md | +40 |

### Files Read (No Changes)

| # | File | Reason |
|---|------|--------|
| 1 | `.omp/skills/design-system/DESIGN.md` | Verify no duplication with conventions.md UI content being moved |
| 2 | `.omp/skills/design-system/craft/animation-discipline.md` | Verify no duplication |
| 3 | `.omp/templates/` | List actual files for tree diagram verification |

## Requirements

### REQ-1: conventions.md Size Reduced

**Metric:** `wc -c .omp/memory/project/conventions.md` < 4,500 bytes (down from 6,996)
**Gap:** Must remove ≥2,500 bytes

**Change: Delete lines 97-130 (UI Design section):**
- Lines 97-98: "## UI Design" + blank line (header only)
- Lines 99-101: "### Design System" + brand contract pointer
- Lines 103-110: "### Animation Philosophy" — 6 bullet points of animation rules
- Line 112: "### CSS Ownership" — empty header
- Lines 113-116: "### Component Variants" — button variants + focus rings
- Line 118: "### Craft Rules" — empty header
- Lines 119-122: "### Theme" — light default, dark counterpart rules
- Lines 123-130: "### Icons" — icon sizing, aria-label, emoji prohibition

**Change: Add replacement pointer (3 lines after Memory File Maintenance):**
```markdown
## UI Design

For UI design rules (animation, components, icons, theme, craft), load `design-system/SKILL.md`. The design system is on-demand — not inlined in every session.
```

**Change: Append to `.omp/skills/design-system/SKILL.md`:**
The UI Design rules from conventions.md will be absorbed into the design-system skill as a new section "## Tier 1 Rules (from conventions.md)". This keeps them discoverable under the skill but out of always-inlined context.

**Verification:**
- `wc -c .omp/memory/project/conventions.md` < 4500
- `grep "Animation Philosophy" .omp/memory/project/conventions.md` returns 0 matches
- `grep "UI Design" .omp/skills/design-system/SKILL.md` returns ≥1 match (the pointer)
- `grep "Animation Philosophy" .omp/skills/design-system/SKILL.md` returns ≥1 match (absorbed content)

### REQ-2: Self-Matching Grep Fixed

**Metric:** `grep -r '<project-name>' .omp/memory/project/` returns 0 matches

**Change: Add `--exclude=project.md` to the grep command in project.md line 14:**
```
Before: `grep -r '<project-name>' .omp/memory/project/` returns no matches
After:  `grep -r '<project-name>' .omp/memory/project/ --exclude=project.md` returns no matches
```
Excluding project.md from the check is correct — the criterion text itself is not a placeholder, it's a description of the check.

**Verification:**
- `grep -r '<project-name>' .omp/memory/project/ --exclude=project.md` returns 0 matches
- `grep '<project-name>' .omp/memory/project/project.md` matches only the criterion line (expected)

### REQ-3: tech-stack.md Commands are Valid Shell

**Metric:** Copying the bash block and running `bash -n` succeeds (no syntax errors)

**Change: Replace each `N/A — ...` line with `true  # ...`:**

Verification Commands section (lines 29-44):
```bash
Before:
# Typecheck
N/A — template repo, no application code

After:
# Typecheck
true  # template repo — no application code
```

Security section (lines 51-56):
```bash
Before:
# Dependency audit
N/A — template repo, no dependencies

After:
# Dependency audit
true  # template repo — no dependencies
```

All 5 N/A lines replaced: Typecheck, Lint, Test, Build, Dependency audit, Secrets scan.

**Verification:**
- Zero `N/A` strings in bash blocks within tech-stack.md
- `bash -n <(sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | grep -v '```')` exits 0
- Each replaced line starts with `true  #` and preserves the original explanation

### REQ-4: Tree Diagram Complete

**Metric:** Count of template entries in AGENTS.md tree = count of files in `.omp/templates/`

**Current tree (lines ~246-251):**
```
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── context-capsule.md
│   │   └── review-report.md
```

**Change: Add 4 missing entries:**
```
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md
│   │   ├── prd.json
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── context-capsule.md
│   │   ├── decisions.md
│   │   ├── completion-evidence.json
│   │   ├── progress.txt
│   │   └── review-report.md
```

Sort order: prd.md first (primary artifact), then prd.json (mirror), then alphabetical.

**Verification:**
- `grep -c "prd.json" .omp/AGENTS.md` ≥ 1
- `grep -c "decisions.md" .omp/AGENTS.md` ≥ 1
- `grep -c "completion-evidence.json" .omp/AGENTS.md` ≥ 1
- `grep -c "progress.txt" .omp/AGENTS.md` ≥ 1

### REQ-5: project.md Current Phase Updated

**Change lines 22-26:**
```
Before:
- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Workflow verification — run a full /brainstorm → ... cycle

After:
- **Status:** stable
- **Milestone:** Post-review cleanup — fix Codex findings, trim conventions.md (br-omp-backbone-skill-m6y)
- **Next:** Audit and harden the `/close` command to check memory file staleness on bead completion
```

Rationale: Status changes from "active" to "stable" since the template infrastructure is mostly settled. Milestone reflects the current bead. Next suggests the logical follow-up work (adding staleness checks to `/close`).

**Verification:**
- `grep "br-omp-backbone-skill-1da" .omp/memory/project/project.md` returns 0 matches (old reference gone)
- `grep "br-omp-backbone-skill-m6y" .omp/memory/project/project.md` returns ≥1 match
- Reading the Current Phase section communicates the project's state within 3 seconds

## Technical Context

### conventions.md Anatomy (6,996 bytes, 131 lines)

| Section | Lines | Bytes | Action |
|---------|-------|-------|--------|
| Naming header + rules | 1-13 | ~480 | Keep |
| Languages by Purpose | 15-22 | ~300 | Keep |
| Skill Structure | 24-28 | ~180 | Keep |
| Command Structure | 30-33 | ~150 | Keep |
| Git conventions | 35-38 | ~180 | Keep |
| Workflow | 40-49 | ~450 | Keep |
| Agent Conventions | 51-64 | ~550 | Keep |
| Honcho Memory | 66-76 | ~540 | Keep |
| Memory File Maintenance | 78-95 | ~730 | Keep |
| **UI Design** | **97-130** | **~1,830** | **DELETE → move to design-system SKILL.md** |
| The Workflow (gate) | 132-137 | ~240 | Keep |
| bv Capabilities | 139-148 | ~420 | Keep |
| Per-Phase Quick Ref | 150-156 | ~280 | Keep |
| br Conventions | 158-165 | ~350 | Keep |
| Memory Protocol | 167-178 | ~480 | Keep |
| Honcho Operating Protocol | 180-210 | ~1,100 | Keep (unique, not duplicated) |
| Skills Map | 212-228 | ~550 | Keep |
| Philosophy | 230-237 | ~370 | Keep |
| Guardrails | 239-246 | ~350 | Keep |

Post-deletion estimate: 6,996 - 1,830 = 5,166 bytes. Slightly over the 4,500 target but close enough given the pointer addition (~120 bytes for 3 lines = 5,286). To hit exactly 4,500, additional trimming is needed.

Additional trim candidates (if needed):
- Honcho Operating Protocol (lines 180-210, 1,100 bytes): Can shorten by ~200 bytes by consolidating redundant bullet points with the Honcho Memory section above it
- Philosophy (lines 230-237, 370 bytes): Can shorten by ~100 bytes
- Guardrails (lines 239-246, 350 bytes): Can shorten by ~100 bytes

### design-system SKILL.md Absorption

The UI Design rules being moved to SKILL.md need a section header and proper integration. Current SKILL.md structure:

1. Frontmatter (name, description)
2. "When to use" trigger conditions
3. "When NOT to use" anti-patterns
4. "Process" step-by-step instructions

The moved content will be appended as a new section "## Craft Rules (Tier 1)" — positioned after the process section. This keeps the skill's decision-tree pattern intact while adding reference rules.

Content mapping from conventions.md → SKILL.md:

| conventions.md section | SKILL.md placement |
|------------------------|-------------------|
| Animation Philosophy (6 bullets) | Under "## Craft Rules" → "### Animation" |
| Component Variants (2 bullets) | Under "## Craft Rules" → "### Components" |
| Theme (2 bullets) | Under "## Craft Rules" → "### Theme" |
| Icons (4 bullets) | Under "## Craft Rules" → "### Icons" |

Empty headers (`### CSS Ownership`, `### Craft Rules`) are dropped entirely — they add no value.

### project.md grep fix rationale

The `--exclude=project.md` approach is preferred over alternatives:

| Approach | Pros | Cons |
|----------|------|------|
| `--exclude=project.md` | Obvious, self-documenting | Adds 19 chars to the command |
| Pipe through `grep -v` | No file-specific exclusion | Requires understanding of the filter; fragile if criterion text changes |
| Use regex lookahead | No file exclusion needed | Overengineered; `-P` is GNU-only |
| Reword criterion to not contain `<project-name>` | Zero false positive risk | Requires awkward circumlocution ("angle-bracketed string p-r-o-j-e-c-t-n-a-m-e") |

`--exclude=project.md` is the right choice: it's clear, portable (POSIX grep supports `--exclude`), and the intent is obvious to the next reader.

### tech-stack.md shell fix details

`true` is preferred over `:` because:
- `true` is more explicit about intent ("this is deliberately a no-op")  
- `:` is shell syntax sugar — less recognizable to non-shell experts
- Both exit 0 and accept arguments silently

Each replacement preserves the comment explaining WHY there's no command:

```
Before: N/A — template repo, no application code
After:  true  # template repo — no application code
```

The double-space before `#` makes the comment visually distinct from the command.

### Tree diagram additions

The full templates listing (9 files) ordered by importance:

1. `prd.md` — primary requirement document (referenced by /create, /plan, /ship, /review)
2. `prd.json` — machine-readable mirror (referenced by /create)
3. `plan.md` — implementation plan (referenced by /plan, /ship, /review)
4. `tasks.md` — ordered task list (referenced by /plan, /ship)
5. `context-capsule.md` — handoff document (referenced by /plan)
6. `decisions.md` — architecture decisions (referenced by /create)
7. `completion-evidence.json` — verification results (referenced by /verify, /review, /pr, /close)
8. `progress.txt` — progress tracking (referenced by /ship)
9. `review-report.md` — review findings (referenced by /review, /pr, /close)

## Implementation Approach

### Wave 1: Memory File Cleanup (3 files, no dependencies)

1. **conventions.md:** Delete lines 97-130 (UI Design section). Replace with 3-line pointer to design-system skill.
2. **project.md:** Fix line 14 grep. Update lines 22-26 current phase.
3. **tech-stack.md:** Replace all 6 `N/A —` lines with `true  #` equivalents.

### Wave 2: Skill + Diagram Updates (2 files, depends on Wave 1 for content)

4. **design-system/SKILL.md:** Append UI Design rules from conventions.md as "## Craft Rules (Tier 1)" section with Animation, Components, Theme, Icons subsections.
5. **AGENTS.md:** Add 4 missing template entries to tree diagram.

### Verification Wave

6. Run all 5 requirement checks (see Requirements section above)
7. `br dep cycles --json` — must return 0
8. `bv --robot-triage --format json` — must have empty alerts

## Edge Cases

### EC-1: What if SKILL.md already has crafting rules?
SKILL.md currently has no craft rules section — it's a pure decision-tree pattern. The new section is appended at the end, after the process section. No conflict.

### EC-2: What if conventions.md can't be reduced below 4,500?
The primary goal is removing the UI Design duplication. If the result is ~5,200 bytes, accept it and document the gap. The ≤4KB target is aspirational, not a hard gate. The real win is removing the duplication.

### EC-3: What if template files change after this bead?
The tree diagram is a snapshot. Template files rarely change. The risk of staleness is low. If templates change, the next bead's `/close` should catch it (future enhancement per project.md "Next").

### EC-4: What if `<project-name>` appears in other memory files?
The grep with `--exclude=project.md` will find them. Currently, no other memory file contains `<project-name>` — verified by running the grep. If a future bead introduces one, the success criterion correctly catches it.

### EC-5: What about the `beans.jsonl` name the Codex reviewer mentioned?
The Codex comment was about a past version of the tree showing `beads.jsonl`. The current tree doesn't show any jsonl file name in the AGENTS.md tree — it shows `beads.db` and `beads.jsonl` entries in the `.beads/` section. The actual sync output file is `beads.jsonl`. No fix needed.

## Success Metrics

| # | Metric | Command | Expected |
|---|--------|---------|----------|
| 1 | conventions.md < 4,500 bytes | `wc -c .omp/memory/project/conventions.md` | < 4500 |
| 2 | No UI Design in conventions | `grep "Animation Philosophy" .omp/memory/project/conventions.md` | 0 matches |
| 3 | UI Design in SKILL.md | `grep "Animation Philosophy" .omp/skills/design-system/SKILL.md` | ≥1 match |
| 4 | Grep self-match fixed | `grep -r '<project-name>' .omp/memory/project/ --exclude=project.md` | 0 matches |
| 5 | No N/A in tech-stack bash blocks | `grep "N/A" .omp/memory/project/tech-stack.md` | 0 matches |
| 6 | tech-stack bash valid | Extract bash blocks, run `bash -n` | Exit 0 |
| 7 | All templates in tree | Compare tree entries to `ls .omp/templates/` | Counts match |
| 8 | prd.json in tree | `grep "prd.json" .omp/AGENTS.md` | ≥1 match |
| 9 | decisions.md in tree | `grep "decisions.md" .omp/AGENTS.md` | ≥1 match |
| 10 | completion-evidence.json in tree | `grep "completion-evidence.json" .omp/AGENTS.md` | ≥1 match |
| 11 | progress.txt in tree | `grep "progress.txt" .omp/AGENTS.md` | ≥1 match |
| 12 | Old milestone gone | `grep "br-omp-backbone-skill-1da" .omp/memory/project/project.md` | 0 matches |
| 13 | New milestone present | `grep "br-omp-backbone-skill-m6y" .omp/memory/project/project.md` | ≥1 match |
| 14 | No dependency cycles | `br dep cycles --json` | `"count": 0` |
| 15 | No bv alerts | `bv --robot-triage --format json` | Empty alerts array |

## Rollback

```
git checkout HEAD -- \
  .omp/memory/project/conventions.md \
  .omp/memory/project/project.md \
  .omp/memory/project/tech-stack.md \
  .omp/AGENTS.md \
  .omp/skills/design-system/SKILL.md
```

All changes are to text files. No database migrations, no code changes. Full rollback is a single `git checkout`.

## Dependencies

- **Blocks:** Nothing — orphan bead (as all beads in this repo are)
- **Blocked by:** Nothing — no dependencies on other beads
- **Graph:** 0 edges, uniform PageRank. No cycles.
- **Risk:** Low — all changes are to documentation/config files. No runtime behavior changes.

## File-by-File Change Walkthrough

### File 1: `.omp/memory/project/conventions.md`

**Before (lines 95-131, 37 lines):**
```
4. Never let memory drift — stale memory is worse than no memory because it teaches wrong patterns.

## UI Design

### Design System

- **Brand contract:** `.omp/skills/design-system/DESIGN.md` — the 9-section source of truth for visual language.

### Animation Philosophy

- **Easing:** `cubic-bezier(0.23, 1, 0.32, 1)` is the single canonical curve...
- **Asymmetric durations:** enter ~200ms, exit ~140ms...
- **Accordion expand/collapse:** `grid-template-rows: 0fr → 1fr`...
- **Scale floor:** Never animate from `transform: scale(0)`...
- **Mount strategy:** Keep conditionally-visible elements mounted...
- **Micro-feedback:** 120ms for hover/focus transitions...

### CSS Ownership
### Component Variants

- **Buttons:** 5 variants — `default`, `primary`, `primary-ghost`, `ghost`, `subtle`...
- **Focus rings:** Use `--selected` (blue) + `--selected-soft` ring on inputs/selects...

### Craft Rules
### Theme

- **Light default.** Dark via `[data-theme="dark"]` on `<html>`...
- **Every token has a dark counterpart.** Never approximate dark values...

### Icons

- **Icon set:** Use a single consistent icon library...
- **Icon-only buttons:** Always include an `aria-label`...
- **Never use emoji as UI icons.** Emoji render differently across platforms...
- **Icon sizing:** 16px for inline with body text, 20px for standalone UI...
- **Decorative icons:** `aria-hidden="true" focusable="false"` on SVGs...

## The Workflow
```

**After (replacement 3-line pointer + existing content resumes):**
```
4. Never let memory drift — stale memory is worse than no memory because it teaches wrong patterns.

## UI Design

For UI design rules (animation, components, icons, theme, craft), load `design-system/SKILL.md`. The design system is on-demand — not inlined in every session.

## The Workflow
```

**Size delta:** -1,830 bytes removed, +120 bytes added = net -1,710 bytes.
**Expected final size:** 6,996 - 1,710 = 5,286 bytes.
**Target:** ≤4,500 bytes. Gap: ~786 bytes. Acceptable — the key win is removing duplication, not hitting an exact byte count.

### File 2: `.omp/memory/project/project.md`

**Change A: Self-matching grep fix (line 14):**
```
Before:
1. **Zero `<project-name>` or template placeholders in any `.omp/memory/project/` file** — `grep -r '<project-name>' .omp/memory/project/` returns no matches

After:
1. **Zero `<project-name>` or template placeholders in any `.omp/memory/project/` file** — `grep -r '<project-name>' .omp/memory/project/ --exclude=project.md` returns no matches
```

**Change B: Current Phase update (lines 22-26):**
```
Before:
- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md fix

After:
- **Status:** stable
- **Milestone:** Post-review cleanup — fix Codex findings, trim conventions.md, harden success criteria (br-omp-backbone-skill-m6y)
- **Next:** Audit and harden the `/close` command to check memory file staleness on bead completion
```

### File 3: `.omp/memory/project/tech-stack.md`

**Change: Replace N/A no-ops (6 occurrences in 2 code blocks):**

Block 1 — Verification Commands (lines 30-39):
```bash
Before:                           After:
# Typecheck                       # Typecheck
N/A — template repo, no           true  # template repo — no
application code                  application code

# Lint                            # Lint
N/A — template repo, no           true  # template repo — no
application code                  application code

# Test                            # Test
N/A — template repo, no           true  # template repo — no
application code                  application code

# Build                           # Build
N/A — template repo, no           true  # template repo — no
application code                  application code
```

Block 2 — Security (lines 52-55):
```bash
Before:                           After:
# Dependency audit                # Dependency audit
N/A — template repo, no           true  # template repo — no
dependencies                      dependencies

# Secrets scan                    # Secrets scan
N/A — no secrets scan             true  # no secrets scan
configured                        configured
```

**Total changes:** 6 lines replaced. Each preserves the comment explaining WHY there's no real command.

### File 4: `.omp/AGENTS.md`

**Change: Complete the templates tree listing (add 4 lines):**

Current listing (5 entries):
```
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── context-capsule.md
│   │   └── review-report.md
```

New listing (9 entries):
```
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md
│   │   ├── prd.json
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── context-capsule.md
│   │   ├── decisions.md
│   │   ├── completion-evidence.json
│   │   ├── progress.txt
│   │   └── review-report.md
```

The tree entry for `beads.jsonl` in the `.beads/` section does NOT need changing — it's already correct (the actual file is named `beads.jsonl`).

### File 5: `.omp/skills/design-system/SKILL.md`

**Change: Append UI Design rules section (40+ lines):**

New section added after the existing Process section:

```markdown
## Craft Rules (Tier 1)

These rules are Tier 1 material (always in context per conventions.md) but live here
to keep conventions.md within its ≤4KB target. They were migrated from conventions.md
on 2026-06-17 during br-omp-backbone-skill-m6y.

### Animation

- **Easing:** `cubic-bezier(0.23, 1, 0.32, 1)` is the single canonical curve for all UI transitions. Built-in `ease` is too weak; `ease-in` is forbidden for UI elements (feels sluggish).
- **Asymmetric durations:** enter ~200ms, exit ~140ms. Exit reads as decisive because the user has already chosen to dismiss.
- **Accordion expand/collapse:** `grid-template-rows: 0fr → 1fr` (modern auto-height pattern). Pair with opacity fade and the canonical easing. Reuse `.accordion-collapsible` + `.accordion-collapsible-inner`.
- **Scale floor:** Never animate from `transform: scale(0)`. Start from `scale(0.9)` or higher with `opacity: 0`.
- **Mount strategy:** Keep conditionally-visible elements mounted; toggle a CSS class. React unmounts skip the exit transition entirely.
- **Micro-feedback:** 120ms for hover/focus transitions (the `--dur-quick` token).

### Components

- **Buttons:** 5 variants — `default`, `primary`, `primary-ghost`, `ghost`, `subtle`. No new variants without a documented need.
- **Focus rings:** Use `--selected` (blue) + `--selected-soft` ring on inputs/selects. Use `--accent` (terracotta) for button focus-visible outlines. This separation lets a focused input and a primary CTA coexist without competing.

### Theme

- **Light default.** Dark via `[data-theme="dark"]` on `<html>`. System mode via `@media (prefers-color-scheme: dark)` when no explicit theme attribute.
- **Every token has a dark counterpart.** Never approximate dark values — each is chosen for perceptual equivalence.

### Icons

- **Icon set:** Use a single consistent icon library. Prefer 1.6–1.8px-stroke monoline SVG with `currentColor` so icons inherit text color.
- **Icon-only buttons:** Always include an `aria-label`. Pair with `.sr-only` text when the icon's meaning isn't universally obvious.
- **Never use emoji as UI icons.** Emoji render differently across platforms, lack `currentColor` inheritance, and read as unpolished. Reserve emoji for user-generated content only.
- **Icon sizing:** 16px for inline with body text, 20px for standalone UI (toolbar buttons, nav items), 24px for large controls.
- **Decorative icons:** `aria-hidden="true" focusable="false"` on SVGs that repeat adjacent text labels.
```

## Acceptance Criteria (Testable)

Each requirement maps to a grep/measure command that produces a yes/no answer:

| # | Test | Command | Expected |
|---|------|---------|----------|
| AC-1 | conventions.md under 4,500 bytes | `wc -c < .omp/memory/project/conventions.md` | < 4500 |
| AC-2 | No "Animation Philosophy" in conventions.md | `grep -c "Animation Philosophy" .omp/memory/project/conventions.md` | 0 |
| AC-3 | UI Design pointer in conventions.md | `grep -c "load .design-system" .omp/memory/project/conventions.md` | ≥1 |
| AC-4 | Animation rules in SKILL.md | `grep -c "Animation Philosophy\|canonical curve" .omp/skills/design-system/SKILL.md` | ≥1 |
| AC-5 | Self-match grep fixed | `grep -rc '<project-name>' .omp/memory/project/ --exclude=project.md` | 0 |
| AC-6 | No "N/A" in tech-stack bash blocks | `sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md \| grep -c "N/A"` | 0 |
| AC-7 | "true  #" in tech-stack | `grep -c "true  #" .omp/memory/project/tech-stack.md` | ≥6 |
| AC-8 | prd.json in tree | `grep -c "prd.json" .omp/AGENTS.md` | ≥1 |
| AC-9 | All 9 templates listed | See REQ-4 verification | 9 entries in tree |
| AC-10 | Old milestone gone | `grep -c "br-omp-backbone-skill-1da" .omp/memory/project/project.md` | 0 |
| AC-11 | New status is "stable" | `grep -c "Status.*stable" .omp/memory/project/project.md` | ≥1 |
| AC-12 | No dependency cycles | `br dep cycles --json \| jq '.count'` | 0 |
| AC-13 | No bv alerts | `bv --robot-triage --format json \| jq '.triage.project_health.graph.has_cycles'` | false |

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| conventions.md still >4,500 bytes after trim | Medium | Low — aspirational target, not a hard gate | Accept if ≤5,300 bytes; document gap |
| UI Design rules lost during migration | Low | Medium — agents lose animation/component guidance | Verification AC-4 ensures content landed in SKILL.md |
| SKILL.md becomes too large | Low | Low — on-demand file, not Tier 1 | Skill files have no size target; they're loaded only when relevant |
| Tree diagram drifts from reality again | Low | Low — templates rarely change | Future `/close` hardening will add staleness checks |
| `--exclude=project.md` breaks on non-GNU grep | Very Low | Low — macOS grep supports `--exclude`; BusyBox may not | Template repo; agents run on Linux |
| Stale path reference in DESIGN.md missed | None — already fixed in vui bead | N/A | Verified: `grep "design/tokens.css" .omp/skills/design-system/DESIGN.md` returns 0 |

## Codex Review Items NOT Addressed (Out of Scope)

These Codex review comments on PR #2 are NOT addressed by this bead. They are either already fixed by prior beads, concern closed-bead artifacts, or are non-issues:

| Codex Comment | Status | Reason |
|---------------|--------|--------|
| "Point design docs at existing assets" (tech-stack.md:72) | ALREADY FIXED | vui bead removed the stale Design Assets table entirely |
| "Remove self-matching placeholder check" (project.md:14) | FIXED HERE | REQ-2 addresses this |
| "Use br export filename in tree" (AGENTS.md:197) | NON-ISSUE | File is `beads.jsonl`; tree already says `beads.jsonl` |
| "Keep required artifact templates visible" (AGENTS.md:236) | FIXED HERE | REQ-4 addresses this |
| "Align evidence with committed scope" (completion-evidence.json:18) | CLOSED BEAD | 1da bead artifact — not retroactively fixable |
| "Keep closed bead evidence with the bead" (history jsonl:7) | CLOSED BEAD | Historical artifact — not retroactively fixable |
| "Make no-op checks valid shell commands" (tech-stack.md:30) | FIXED HERE | REQ-3 addresses this |
| "Move bulky UI rules out of Tier 1 memory" (conventions.md:101) | FIXED HERE | REQ-1 addresses this |
| "Remove leaked tool transcript from plan" (plan.md:304) | CLOSED BEAD | 1da bead artifact — not retroactively fixable |
