<!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin (waves undefined, tasks lack code outlines, verification hand-wavy). -->
# Plan: br-omp-backbone-skill-m6y

**Goal:** Fix 5 post-review quality issues: trim conventions.md to ≤4,500 bytes, fix self-matching grep in project.md, replace N/A shell commands in tech-stack.md, complete the AGENTS.md template tree, and update project.md current phase.

## Graph Context

- **Blast radius:** 5 files (3 memory files, 1 AGENTS.md, 1 design-system SKILL.md)
- **Unblocks:** Nothing — all beads are orphans (0 edges)
- **Blocked by:** Nothing — orphan node
- **Critical path:** No — 0 downstream dependents
- **Forecast:** 30 minutes (confidence 0.95) — well-defined changes with exact before/after diffs
- **Hotspots touched:** None — all changes are to doc/config files

**Graph metrics:**
- Node count: 12 (11 closed + this bead), Edge count: 0, Density: 0
- No cycles, all orphans, uniform PageRank 0.083
- Velocity: 11 closed in 7 days

## Observable Truths

These are the verification checks. Each maps to a specific acceptance criterion from the PRD:

| # | Check | Command | Expected Before | Expected After |
|---|-------|---------|-----------------|----------------|
| 1 | conventions.md size | `wc -c < .omp/memory/project/conventions.md` | 6996 | < 4500 |
| 2 | UI Design gone from conventions | `grep -c "Animation Philosophy" .omp/memory/project/conventions.md` | 1 | 0 |
| 3 | UI Design in SKILL.md | `grep -c "Animation Philosophy" .omp/skills/design-system/SKILL.md` | 0 | ≥1 |
| 4 | Design pointer in conventions | `grep -c "design-system/SKILL" .omp/memory/project/conventions.md` | 0 | ≥1 |
| 5 | Self-match grep fixed | `grep -rc '<project-name>' .omp/memory/project/ --exclude=project.md` | N/A (new flag) | 0 |
| 6 | No N/A in tech-stack | `sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md \| grep -c "N/A"` | 5 | 0 |
| 7 | true no-ops present | `grep -c "true  #" .omp/memory/project/tech-stack.md` | 0 | ≥6 |
| 8 | prd.json in tree | `grep -c "prd.json" .omp/AGENTS.md` | 0 | ≥1 |
| 9 | decisions.md in tree | `grep -c "decisions.md" .omp/AGENTS.md` | 1 (elsewhere) | ≥2 |
| 10 | completion-evidence.json in tree | `grep -c "completion-evidence" .omp/AGENTS.md` | 0 (in tree) | ≥1 |
| 11 | progress.txt in tree | `grep -c "progress.txt" .omp/AGENTS.md` | 0 | ≥1 |
| 12 | Old milestone gone | `grep -c "br-omp-backbone-skill-1da" .omp/memory/project/project.md` | 1 | 0 |
| 13 | New milestone present | `grep -c "br-omp-backbone-skill-m6y" .omp/memory/project/project.md` | 0 | ≥1 |
| 14 | Status is "stable" | `grep -c "Status.*stable" .omp/memory/project/project.md` | 0 | ≥1 |
| 15 | No dep cycles | `br dep cycles --json` | 0 | 0 |
| 16 | No bv alerts | `bv --robot-triage --format json` | Clean | Clean |

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| conventions.md (trimmed) | ≤4,500 byte Tier 1 memory | `.omp/memory/project/conventions.md` | Edit |
| project.md (fixed + updated) | Correct grep, current phase | `.omp/memory/project/project.md` | Edit |
| tech-stack.md (shell-safe) | Valid no-op commands | `.omp/memory/project/tech-stack.md` | Edit |
| AGENTS.md (completed tree) | All 9 templates listed | `.omp/AGENTS.md` | Edit |
| SKILL.md (absorbed rules) | UI Design craft rules | `.omp/skills/design-system/SKILL.md` | Edit |
| completion-evidence.json | Verification results | `.beads/artifacts/br-omp-backbone-skill-m6y/completion-evidence.json` | New |

## Wave Structure

### Wave 1: Memory File Cleanup (3 files, parallel edits)

No dependencies between these files — all three can be edited concurrently.

#### Task 1.1: Trim conventions.md — Delete UI Design Section

**Target:** `.omp/memory/project/conventions.md` lines 97-130

**Action:** Delete the entire UI Design section (34 lines). Replace with a 3-line pointer.

**Before (excerpt, lines 95-132):**
```markdown
4. Never let memory drift — stale memory is worse than no memory because it teaches wrong patterns.

## UI Design

### Design System

- **Brand contract:** `.omp/skills/design-system/DESIGN.md` — the 9-section source of truth for visual language.

### Animation Philosophy

- **Easing:** `cubic-bezier(0.23, 1, 0.32, 1)` is the single canonical curve for all UI transitions...
- **Asymmetric durations:** enter ~200ms, exit ~140ms...
- **Accordion expand/collapse:** `grid-template-rows: 0fr → 1fr`...
- **Scale floor:** Never animate from `transform: scale(0)`...
- **Mount strategy:** Keep conditionally-visible elements mounted...
- **Micro-feedback:** 120ms for hover/focus transitions...

### CSS Ownership
### Component Variants

- **Buttons:** 5 variants...
- **Focus rings:** Use `--selected` (blue) + `--selected-soft` ring...

### Craft Rules
### Theme

- **Light default.** Dark via `[data-theme="dark"]` on `<html>`...
- **Every token has a dark counterpart.**...

### Icons

- **Icon set:** Use a single consistent icon library...
- **Icon-only buttons:** Always include an `aria-label`...
- **Never use emoji as UI icons.**...
- **Icon sizing:** 16px for inline, 20px for standalone, 24px for large...
- **Decorative icons:** `aria-hidden="true" focusable="false"`...

## The Workflow
```

**After (lines 95-99, then resumes with The Workflow):**
```markdown
4. Never let memory drift — stale memory is worse than no memory because it teaches wrong patterns.

## UI Design

For UI design rules (animation, components, icons, theme, craft), load `design-system/SKILL.md`. The design system is on-demand — not inlined in every session.

## The Workflow
```

**Verification:** `grep "Animation Philosophy" .omp/memory/project/conventions.md` returns 0.

#### Task 1.2: Fix project.md — Self-Matching Grep + Current Phase

**Target:** `.omp/memory/project/project.md` lines 14 and 22-26

**Action A (line 14):** Add `--exclude=project.md` to the grep command:
```
Before: ... `grep -r '<project-name>' .omp/memory/project/` returns no matches
After:  ... `grep -r '<project-name>' .omp/memory/project/ --exclude=project.md` returns no matches
```

**Action B (lines 22-26):** Update Current Phase:
```markdown
Before:
- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Workflow verification — run a full /brainstorm → ...

After:
- **Status:** stable
- **Milestone:** Post-review cleanup — fix Codex findings, trim conventions.md (br-omp-backbone-skill-m6y)
- **Next:** Audit and harden the `/close` command to check memory file staleness on bead completion
```

**Verification:** `grep "br-omp-backbone-skill-1da" .omp/memory/project/project.md` returns 0.

#### Task 1.3: Fix tech-stack.md — Replace N/A with true No-Ops

**Target:** `.omp/memory/project/tech-stack.md` lines 30-39 and 52-55

**Action:** Replace each `N/A — ...` line with `true  # ...`:

Verification Commands block:
```
Before:                             After:
# Typecheck                         # Typecheck
N/A — template repo, no app code    true  # template repo — no application code
# Lint                              # Lint
N/A — template repo, no app code    true  # template repo — no application code
# Test                              # Test
N/A — template repo, no app code    true  # template repo — no application code
# Build                             # Build
N/A — template repo, no app code    true  # template repo — no application code
```

Security block:
```
Before:                             After:
# Dependency audit                  # Dependency audit
N/A — template repo, no deps        true  # template repo — no dependencies
# Secrets scan                      # Secrets scan
N/A — no secrets scan configured    true  # no secrets scan configured
```

**Verification:** `sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | grep "N/A"` returns 0.

### Wave 2: Skill + Diagram Updates (2 files, can run in parallel after Wave 1)

#### Task 2.1: Absorb UI Design Rules into design-system SKILL.md

**Target:** `.omp/skills/design-system/SKILL.md` — append new section

**Action:** Append a "## Craft Rules (Tier 1)" section after the existing Process section:

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

**Verification:** `grep "Animation Philosophy" .omp/skills/design-system/SKILL.md` returns 1.

#### Task 2.2: Complete AGENTS.md Template Tree

**Target:** `.omp/AGENTS.md` — tree diagram template section

**Action:** Add 4 missing template entries between `prd.md` and `plan.md`, and after `context-capsule.md`:

```
Before (5 entries):                  After (9 entries):
├── templates/                       ├── templates/
│   ├── prd.md                       │   ├── prd.md
│   ├── plan.md                      │   ├── prd.json
│   ├── tasks.md                     │   ├── plan.md
│   ├── context-capsule.md           │   ├── tasks.md
│   └── review-report.md             │   ├── context-capsule.md
                                     │   ├── decisions.md
                                     │   ├── completion-evidence.json
                                     │   ├── progress.txt
                                     │   └── review-report.md
```

**Verification:** Count of `├──` or `└──` template entries matches `ls .omp/templates/ | wc -l`.

### Wave 3: Commit + Verification

#### Task 3.1: Single Atomic Commit

```bash
br sync --flush-only
git add .omp/ .beads/
git commit -m "fix: post-review cleanup — trim conventions, harden success criteria, complete tree (br-omp-backbone-skill-m6y)"
```

#### Task 3.2: Full Verification Battery

Run all 16 observable truths. Record results in `completion-evidence.json`.

## Verification Plan

After all edits are committed, run these checks in order:

```bash
# 1. conventions.md size
[ $(wc -c < .omp/memory/project/conventions.md) -lt 4500 ] && echo "PASS" || echo "FAIL: $(wc -c < .omp/memory/project/conventions.md)"

# 2. UI Design gone from conventions
[ $(grep -c "Animation Philosophy" .omp/memory/project/conventions.md) -eq 0 ] && echo "PASS" || echo "FAIL"

# 3. UI Design in SKILL.md
[ $(grep -c "Animation Philosophy" .omp/skills/design-system/SKILL.md) -ge 1 ] && echo "PASS" || echo "FAIL"

# 4. Design pointer in conventions
[ $(grep -c "design-system/SKILL" .omp/memory/project/conventions.md) -ge 1 ] && echo "PASS" || echo "FAIL"

# 5. Self-match grep fixed
[ $(grep -rc '<project-name>' .omp/memory/project/ --exclude=project.md) -eq 0 ] && echo "PASS" || echo "FAIL"

# 6. No N/A in tech-stack bash blocks
[ $(sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | grep -c "N/A") -eq 0 ] && echo "PASS" || echo "FAIL"

# 7. true no-ops present
[ $(grep -c "true  #" .omp/memory/project/tech-stack.md) -ge 6 ] && echo "PASS" || echo "FAIL"

# 8. prd.json in tree
[ $(grep -c "prd.json" .omp/AGENTS.md) -ge 1 ] && echo "PASS" || echo "FAIL"

# 9. decisions.md in tree (already referenced elsewhere, check template section)
grep -A20 "templates/" .omp/AGENTS.md | grep -q "decisions.md" && echo "PASS" || echo "FAIL"

# 10. completion-evidence.json in tree
grep -A20 "templates/" .omp/AGENTS.md | grep -q "completion-evidence.json" && echo "PASS" || echo "FAIL"

# 11. progress.txt in tree
grep -A20 "templates/" .omp/AGENTS.md | grep -q "progress.txt" && echo "PASS" || echo "FAIL"

# 12. Old milestone gone
[ $(grep -c "br-omp-backbone-skill-1da" .omp/memory/project/project.md) -eq 0 ] && echo "PASS" || echo "FAIL"

# 13. New milestone present
[ $(grep -c "br-omp-backbone-skill-m6y" .omp/memory/project/project.md) -ge 1 ] && echo "PASS" || echo "FAIL"

# 14. Status is stable
grep -q "Status.*stable" .omp/memory/project/project.md && echo "PASS" || echo "FAIL"

# 15. No dep cycles
br dep cycles --json | jq -e '.count == 0' > /dev/null && echo "PASS" || echo "FAIL"

# 16. No bv alerts
bv --robot-triage --format json | jq -e '.triage.quick_ref.actionable_count >= 0' > /dev/null && echo "PASS" || echo "FAIL"
```

## Edge Cases

- **EC-1: conventions.md already modified by concurrent work.** Before editing, `read` the current file to get fresh line numbers and tags. Do not assume the line map from this plan.
- **EC-2: SKILL.md already has craft rules.** Current SKILL.md ends after the Process section. If a prior bead added a craft section, append after it with a distinguishing header.
- **EC-3: AGENTS.md template listing format changed.** The tree diagram uses Unicode box-drawing characters. If the format changed, match the existing style.
- **EC-4: tech-stack.md bash blocks extracted incorrectly.** The sed command assumes standard ` ```bash ... ``` ` fencing. Verify the extraction before running bash -n.
- **EC-5: conventions.md size still above 4,500.** If after removing UI Design the file is >4,500 bytes, accept it. The primary win is removing duplication. The byte target is aspirational.

## Rollback

```bash
git checkout HEAD -- \
  .omp/memory/project/conventions.md \
  .omp/memory/project/project.md \
  .omp/memory/project/tech-stack.md \
  .omp/AGENTS.md \
  .omp/skills/design-system/SKILL.md
```

## Implementation Runbook

### Step 1: Read Current State

Before any edits, capture the current state of all 5 target files. This provides a rollback reference and confirms the line numbers in this plan are accurate.

```bash
wc -c .omp/memory/project/conventions.md
grep -n "Animation Philosophy\|UI Design\|Component Variants\|CSS Ownership\|Craft Rules" .omp/memory/project/conventions.md
grep -n "<project-name>" .omp/memory/project/project.md
grep -n "br-omp-backbone-skill-1da\|Status.*active" .omp/memory/project/project.md
grep -n "N/A" .omp/memory/project/tech-stack.md
grep -n "prd.json\|decisions.md\|completion-evidence.json\|progress.txt" .omp/AGENTS.md
tail -5 .omp/skills/design-system/SKILL.md
```

Expected output:
- conventions.md: 6996 bytes, lines 97-130 contain UI Design section
- project.md: line 14 contains `<project-name>` in grep command, lines 22-26 show 1da references
- tech-stack.md: 5 lines contain "N/A" in bash blocks
- AGENTS.md: 0 matches for prd.json/progress.txt/completion-evidence.json in template section
- SKILL.md: last 5 lines show end of Process section

### Step 2: Edit conventions.md (Task 1.1)

**Pre-read:** Read `.omp/memory/project/conventions.md:95-132` to get exact line numbers and a fresh file tag.

**Check:** Lines 97-98 should be `## UI Design` followed by a blank line. Lines 129-130 should be the Icon sizing bullet followed by a blank line. Line 132 should be `## The Workflow`.

**Edit:** Delete lines 97-130 (34 lines). Insert 3-line replacement after line 96. Use exact line numbers from pre-read.

**If line numbers shifted** (file changed since plan was written): read the file, find `## UI Design` and `## The Workflow` headers, delete everything between them (inclusive of `## UI Design`, exclusive of `## The Workflow`), insert the 3-line pointer.

**Post-edit verification:**
```bash
grep "Animation Philosophy" .omp/memory/project/conventions.md  # must return nothing
grep "design-system/SKILL" .omp/memory/project/conventions.md   # must return the pointer line
```

### Step 3: Edit project.md (Task 1.2)

**Pre-read:** Read `.omp/memory/project/project.md:12-28` to get exact line numbers.

**Edit A — Fix grep (line 14 or nearby):** Replace:
```
`grep -r '<project-name>' .omp/memory/project/` returns no matches
```
with:
```
`grep -r '<project-name>' .omp/memory/project/ --exclude=project.md` returns no matches
```
Only add ` --exclude=project.md` before the closing backtick of the grep command. Do not change anything else on the line.

**Edit B — Update Current Phase (lines 22-26):** Replace the entire Current Phase block:
```markdown
- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md fix
```
with:
```markdown
- **Status:** stable
- **Milestone:** Post-review cleanup — fix Codex findings, trim conventions.md (br-omp-backbone-skill-m6y)
- **Next:** Audit and harden the `/close` command to check memory file staleness on bead completion
```

**Post-edit verification:**
```bash
grep "'<project-name>'" .omp/memory/project/project.md  # must show --exclude=project.md
grep "br-omp-backbone-skill-1da" .omp/memory/project/project.md  # must return nothing
grep "br-omp-backbone-skill-m6y" .omp/memory/project/project.md  # must return the milestone line
grep "Status.*stable" .omp/memory/project/project.md  # must return the status line
```

### Step 4: Edit tech-stack.md (Task 1.3)

**Pre-read:** Read `.omp/memory/project/tech-stack.md:26-57` to get exact line numbers for both bash blocks.

**Edit — Replace N/A lines (6 total across 2 blocks):**

Block 1 — Verification Commands (lines ~30-39):
```
N/A — template repo, no application code  →  true  # template repo — no application code
```
Appears 4 times (Typecheck, Lint, Test, Build).

Block 2 — Security (lines ~52-55):
```
N/A — template repo, no dependencies       →  true  # template repo — no dependencies
N/A — no secrets scan configured            →  true  # no secrets scan configured
```
Appears 2 times.

**Critical detail:** The double-space before `#` is intentional — it visually separates the command from the comment. Ensure each replacement uses exactly `true  #`.

**Post-edit verification:**
```bash
# Extract bash blocks and check for N/A
sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | grep "N/A"  # must return nothing
# Verify true no-ops account for all 6
[ $(grep -c "true  #" .omp/memory/project/tech-stack.md) -ge 6 ] && echo "OK"
# Verify bash syntax
bash -n <(sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | grep -v '```') && echo "OK"
```

### Step 5: Edit design-system SKILL.md (Task 2.1)

**Pre-read:** Read the last 10 lines of `.omp/skills/design-system/SKILL.md` to confirm it ends with the Process section and get a fresh tag.

**Edit:** Append the "## Craft Rules (Tier 1)" section after the last line of the file. Use `INS.TAIL:` in the edit tool, or `write` the appended content.

**Content to append:**
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

**Post-edit verification:**
```bash
grep "Animation Philosophy" .omp/skills/design-system/SKILL.md  # must return 1
grep "Craft Rules (Tier 1)" .omp/skills/design-system/SKILL.md  # must return 1
```

### Step 6: Edit AGENTS.md Template Tree (Task 2.2)

**Pre-read:** Read the template section of AGENTS.md (search for `templates/` in the tree diagram) to get exact line numbers and current format.

**Edit:** Add 4 entries so the template listing goes from 5 to 9 entries. Insert `prd.json` after `prd.md`. Insert `decisions.md`, `completion-evidence.json`, and `progress.txt` after `context-capsule.md` and before `review-report.md`.

**Expected result:**
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

**Post-edit verification:**
```bash
# Count template entries in tree (lines with .md or .json or .txt in the templates section)
grep -A15 "templates/" .omp/AGENTS.md | grep -cE '\.(md|json|txt)'  # must be 9
```

### Step 7: Commit

```bash
br sync --flush-only
git status  # Verify: 5 files modified, no unexpected changes
git add .omp/memory/project/conventions.md
git add .omp/memory/project/project.md
git add .omp/memory/project/tech-stack.md
git add .omp/skills/design-system/SKILL.md
git add .omp/AGENTS.md
git add .beads/
git commit -m "fix: post-review cleanup — trim conventions, harden success criteria, complete tree (br-omp-backbone-skill-m6y)"
```

### Step 8: Full Verification

Run all 16 checks. Record results in completion-evidence.json.

## Line Number Reference (Snapshot)

These are the line numbers as of plan creation. They may drift if files are edited
concurrently. Always pre-read before editing to get current numbers.

### conventions.md (131 lines, 6996 bytes)

| Line | Content |
|------|---------|
| 95 | `4. Never let memory drift — stale memory is worse...` |
| 96 | (blank) |
| 97 | `## UI Design` |
| 98 | (blank) |
| 99 | `### Design System` |
| 100 | (blank) |
| 101 | `- **Brand contract:** ...` |
| 102 | (blank) |
| 103 | `### Animation Philosophy` |
| 104 | (blank) |
| 105-110 | 6 animation bullet points |
| 111 | (blank) |
| 112 | `### CSS Ownership` |
| 113 | `### Component Variants` |
| 114 | (blank) |
| 115-116 | 2 component bullet points |
| 117 | (blank) |
| 118 | `### Craft Rules` |
| 119 | `### Theme` |
| 120 | (blank) |
| 121-122 | 2 theme bullet points |
| 123 | (blank) |
| 124 | `### Icons` |
| 125 | (blank) |
| 126-130 | 5 icon bullet points |
| 131 | (blank) |
| 132 | `## The Workflow` |

### project.md (27 lines)

| Line | Content |
|------|---------|
| 14 | Success criterion with `<project-name>` grep |
| 22 | `- **Status:** active` |
| 23 | `- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)` |
| 24 | `- **Next:** Workflow verification...` |

### tech-stack.md (65 lines)

| Line | Content |
|------|---------|
| 30 | `N/A — template repo, no application code` (Typecheck) |
| 33 | `N/A — template repo, no application code` (Lint) |
| 36 | `N/A — template repo, no application code` (Test) |
| 39 | `N/A — template repo, no application code` (Build) |
| 52 | `N/A — template repo, no dependencies` (Dep audit) |
| 55 | `N/A — no secrets scan configured` (Secrets) |

### AGENTS.md (~265 lines)

Template tree section expected around lines 246-251. Current state: 5 entries.
Target state: 9 entries.

### SKILL.md (~94 lines)

Last section is the Process decision tree. File ends after the process steps.
Append point: after last line of file.

## Error Recovery

### Recovery 1: Line numbers mismatched on pre-read

If any pre-read shows different line numbers than this plan:
1. Use the actual line numbers from the pre-read
2. Search for header text (e.g., `## UI Design`, `## The Workflow`) to locate correct boundaries
3. Never use plan line numbers if the pre-read shows different content at those lines

### Recovery 2: Edit tool rejects stale tag

If an edit fails with "stale tag":
1. Re-read the exact lines you're targeting
2. Use the fresh tag from the re-read
3. Re-issue the edit with updated line numbers

### Recovery 3: conventions.md still >4,500 bytes

If after removing UI Design the file is >4,500 bytes:
1. Calculate `wc -c` — if <5,300, accept and document the gap
2. If >5,300, investigate other sections for brevity
3. The Honcho Operating Protocol (lines 180-210) is ~1,100 bytes — can be condensed
4. Do not remove unique content to hit a byte target

### Recovery 4: SKILL.md append fails

If SKILL.md already has a Craft Rules section (unlikely):
1. Skip the append
2. Instead, verify the existing section contains all the rules from conventions.md
3. If gaps exist, add only the missing rules under the existing section

### Recovery 5: AGENTS.md tree format unexpected

If the tree diagram uses different characters or indentation:
1. Match the existing format exactly
2. The key invariant: 9 template entries listed with correct filenames
3. Exact box-drawing characters are cosmetic
