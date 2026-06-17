# PRD: br-omp-backbone-skill-s2s — Audit and Fix Missing Design Assets, Stale References, and Empty Conventions Sections

**Bead ID:** `br-omp-backbone-skill-s2s`
**Status:** In Progress (assigned to makora1)
**Created:** 2026-06-18
**Phase:** /create

---

## 1. Problem Statement

After closing 13 prior beads on the omp-template repository, a quality audit revealed systemic documentation drift. The template's memory files and agent instructions reference infrastructure that does not exist on disk. Specifically:

1. **12 missing design asset files** — `tech-stack.md` (lines 65-88) documents a "Design Assets" table and "Craft References" table referencing 12 files under `.omp/design/` and `.omp/design/craft/`. None of these files or directories exist on disk.

2. **Missing design-system skill directory** — `conventions.md:101`, `tech-stack.md:69`, and `AGENTS.md:224-226` all reference `.omp/skills/design-system/DESIGN.md` (and the `SKILL.md` for the design-system skill). The directory `.omp/skills/design-system/` does not exist. The skill table in AGENTS.md line 188 lists `design-system` as a loadable skill with trigger conditions, but the skill itself is absent.

3. **Empty headers in conventions.md** — Lines 112 (`### CSS Ownership`) and 118 (`### Craft Rules`) are followed by no content, immediately transitioning to the next section. These are structural noise.

4. **Stale project.md milestone** — `project.md:23` still references `br-omp-backbone-skill-1da` as the active milestone despite that bead being closed. The "Next" field on line 24 references "Workflow verification" which was never executed.

5. **Template identity confusion** — `conventions.md` contains a full "UI Design" section (lines 97-131) with detailed animation philosophy, component variant rules, theme specifications, and icon guidelines. This is inconsistent with a workflow template that explicitly states "Template repo — no backend runtime" and "Template repo — no application runtime" in `tech-stack.md`. These UI design sections were adapted from Open Design's craft directory and refero_skill (Apache 2.0 / MIT), originally intended for downstream projects that use this template — but they live in the template's own memory files, creating a structural contradiction.

### Impact

- **Agents that load the design-system skill** (triggered by "generating UI, choosing colors/fonts/spacing, implementing components, or reviewing visual output" per AGENTS.md:188) will find nothing to load — a silent failure that wastes context and degrades output quality.
- **Agents following conventions.md** encounter dead sections that waste token budget and create confusion about what rules actually exist.
- **Downstream projects that clone this template** inherit broken references. The template's own doc tree serves as the bootstrapping reference, so every clone starts with broken links.
- **The project.md milestone tracker** is stale, making it impossible to determine the project's actual current phase from memory files alone.

---

## 2. Goals

| # | Goal | Success Measure |
|---|------|----------------|
| G1 | Create the `design-system` skill with a proper `SKILL.md` and `DESIGN.md` that serves as the single source of truth for visual language in downstream projects | `.omp/skills/design-system/SKILL.md` and `DESIGN.md` exist on disk; `grep -r "design-system" .omp/` resolves to existing paths |
| G2 | Remove all references to non-existent `.omp/design/` and `.omp/design/craft/` files from `tech-stack.md` and any other memory files | `grep -r "\.omp/design/" .omp/memory/` returns zero matches |
| G3 | Fill or remove the empty headers in `conventions.md` (CSS Ownership and Craft Rules) | No header in `conventions.md` is followed by zero content before the next header |
| G4 | Update `project.md` to reflect current state — remove stale milestone reference, update status to reflect this bead | `project.md:23` no longer references closed bead br-omp-backbone-skill-1da |
| G5 | Clarify the template's relationship to UI design: the design-system skill provides a *brand contract template* for downstream projects, not UI implementation rules for the template itself | `conventions.md` UI Design section either moved to design-system skill or annotated as downstream template content |
| G6 | Zero broken references across all memory files — every referenced file path in `.omp/memory/project/*.md` resolves to an existing file | Manual audit: for each path reference in memory files, `test -f <path>` succeeds |

---

## 3. Non-Goals

| # | Non-Goal | Rationale |
|---|----------|-----------|
| NG1 | Creating actual `.omp/design/tokens.css`, `base.css`, or any `.omp/design/craft/*.md` files | These are downstream project artifacts, not template infrastructure. They document project-specific design tokens and brand choices that vary per project. Including them would require maintenance and constrain downstream design freedom. |
| NG2 | Implementing any UI components or visual assets | Template repo has no application code. The design-system skill defines *what to document*, not *what to build*. |
| NG3 | Creating a full design token system | The template's role is to specify the *contract format* (DESIGN.md's 9 sections) that downstream projects fill in. It does not own the tokens themselves. |
| NG4 | Auditing or modifying any files outside `.omp/memory/project/` and `.omp/skills/design-system/` | Scope is limited to the identified issues. Other template infrastructure (commands, extensions, other skills) is out of scope unless they contain broken references discovered during implementation. |
| NG5 | Updating tech-stack.md's "Design Assets" table to point to new locations | The table is being removed entirely, not relocated. |
| NG6 | Changing the 13 closed beads or their artifacts | Immutable. Only current-state memory files are in scope. |
| NG7 | Adding new conventions, rules, or workflow changes | This is a cleanup bead. Feature additions belong in separate beads. |

---

## 4. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Broken file references in memory files | 0 | `grep -oP '\.omp/[a-zA-Z0-9_/.-]+\.(md|css|json|ts)' .omp/memory/project/*.md \| while read f; do test -f "$f" \|\| echo "MISSING: $f"; done` returns no output |
| Empty sections in conventions.md | 0 | Parse headers: no H3/H4 header has zero content before next header of same or higher level |
| Design-system skill loads successfully | N/A | Agent can read `.omp/skills/design-system/SKILL.md` and `.omp/skills/design-system/DESIGN.md`; DESIGN.md has all 9 required sections |
| Stale milestone references in project.md | 0 | project.md Current Phase section references only currently active beads |
| Template identity clarity | N/A | After changes, an agent reading conventions.md can distinguish "rules for the template" from "template content for downstream projects" |
| No regression in existing skills | N/A | All 18 existing skill directories (17 named + backbone) remain untouched; `bv --robot-triage` reports no new issues |

---

## 5. Detailed Requirements

### R1: Create design-system Skill Directory

**Files to create:**
- `.omp/skills/design-system/SKILL.md`
- `.omp/skills/design-system/DESIGN.md`

#### R1.1: SKILL.md Structure

Follow the established skill pattern (per conventions.md "Skill Structure" section):

```markdown
---
name: design-system
description: When to use, when not to use, process steps
---

# design-system

## When to use
- [Trigger conditions matching AGENTS.md:188]

## When NOT to use
- [Anti-patterns]

## Process
### Step 1: ...
### Step 2: ...
```

The SKILL.md must:
- Document that this skill is a *brand contract template*, not a completed design system
- Instruct agents to check if DESIGN.md exists and is filled before generating UI
- Provide fallback guidance when a downstream project hasn't filled in the brand contract
- Reference Open Design craft rules (Apache 2.0) and refero_skill (MIT) as upstream sources that downstream projects can integrate
- NOT contain any tool-specific directives that would be invalid for projects not using this template's exact toolchain

#### R1.2: DESIGN.md Structure

Must contain exactly 9 sections as specified by the brand contract format:

| # | Section | Description |
|---|---------|-------------|
| 1 | **Brand Identity** | Brand name, tagline, voice/tone keywords |
| 2 | **Color Palette** | Primary, secondary, accent, neutral, semantic colors with hex values |
| 3 | **Typography** | Font families (heading, body, mono), type scale, weight assignments |
| 4 | **Spacing & Layout** | Spacing scale (4px base), max content width, grid system |
| 5 | **Component Tokens** | Border radius, shadow levels, border widths, opacity states |
| 6 | **Animation** | Duration tokens, easing curves, reduced-motion policy |
| 7 | **Iconography** | Icon library, sizing conventions, accessibility rules |
| 8 | **Imagery** | Illustration style, photo treatment, aspect ratios |
| 9 | **Theme** | Light/dark/system mode strategy, token naming convention |

Each section must:
- Start with a brief explanation of what the section captures
- Use `[FILL]` placeholders for values downstream projects must replace
- Include a concrete example value in a comment so the downstream project understands the expected format
- NOT contain specific brand values (no actual hex codes, font names, etc. — those are downstream choices)

#### R1.3: Attribution

Both SKILL.md and DESIGN.md must include attribution:
- Open Design craft/ rules (Apache 2.0 license) — the source of craft-level design rules
- refero_skill (MIT license) — the refero design methodology
- Link format must follow the existing template convention

### R2: Remove Stale Design Asset References from tech-stack.md

**Target file:** `.omp/memory/project/tech-stack.md`

#### R2.1: Remove "Design Assets" Table

The entire "Design Assets" table (current lines 65-72) must be removed. This table references:
- `.omp/skills/design-system/DESIGN.md` (will exist after R1 — still remove from this table since it belongs in AGENTS.md skill map, not tech-stack)
- `.omp/design/tokens.css` (does not exist, will not be created — downstream concern)
- `.omp/design/base.css` (does not exist, will not be created)
- `.omp/design/primitives.css` (does not exist, will not be created)

#### R2.2: Remove "Craft References" Table

The "Craft References" table (current lines 74-88) must be removed. All 8 referenced craft files are downstream concerns that:
- Do not exist on disk
- Will not be created in this template
- Are upstream content from Open Design (Apache 2.0) that downstream projects may choose to integrate

#### R2.3: Preserve Attribution

The attribution line "Adapted from Open Design's `craft/` directory (Apache 2.0) and refero_skill (MIT)" must be moved to the design-system skill's DESIGN.md as attribution, then removed from tech-stack.md.

#### R2.4: Verify No Orphan References

After removal, verify that no other tech-stack.md section references removed content. The file must remain internally consistent and complete for its stated purpose: "Tech stack, versions, verification commands, and constraints."

### R3: Fix Empty Headers in conventions.md

**Target file:** `.omp/memory/project/conventions.md`

#### R3.1: CSS Ownership (current line 112)

The `### CSS Ownership` header on line 112 is followed immediately by `### Component Variants` on line 113 with no content.

**Decision required:** This section should be filled with a concise statement about CSS ownership in the template context. Options:

- **Option A (Fill):** "CSS is a downstream project concern. The design-system skill (`.omp/skills/design-system/`) defines the brand contract format; downstream projects provide their own CSS implementation. Template memory files do not own CSS rules."
- **Option B (Remove):** Delete the empty header entirely.

**Recommendation: Option A** — the header exists in the UI Design section which is being retained as downstream template content. A brief ownership statement clarifies boundaries.

#### R3.2: Craft Rules (current line 118)

The `### Craft Rules` header on line 118 is followed immediately by `### Theme` on line 119 with no content.

**Decision required:** Same as above.

- **Option A (Fill):** "Craft rules are brand-agnostic design principles originally from Open Design's craft/ directory (Apache 2.0). Downstream projects may integrate these rules; the template itself does not enforce them. See `.omp/skills/design-system/DESIGN.md` for the brand contract format."
- **Option B (Remove):** Delete the empty header.

**Recommendation: Option A** — provides a pointer to where downstream projects can learn about craft rules.

### R4: Update project.md Stale Milestone

**Target file:** `.omp/memory/project/project.md`

#### R4.1: Fix Current Phase

Current lines 22-24:
```
- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md fix
```

Must be updated to:
```
- **Status:** active
- **Milestone:** Design asset audit and memory file cleanup (br-omp-backbone-skill-s2s)
- **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md and tech-stack.md cleanup
```

#### R4.2: Add Success Criteria Entry

Add to the Success Criteria section:
```
4. **Zero broken file references in memory files** — `grep -oP '\.omp/[\w/.-]+\.\w+' .omp/memory/project/*.md | while read f; do test -f "$f" || echo "$f"; done` returns no output
```

### R5: Clarify Template Identity in conventions.md

**Target file:** `.omp/memory/project/conventions.md`

#### R5.1: Add Section Header Annotation

The "UI Design" section header on line 97 (`## UI Design`) should be annotated to clarify its purpose. Add a brief intro sentence:

```
## UI Design

> **Note:** This section is template content for downstream projects, not rules that apply to the omp-template repository itself. The template has no application runtime or UI code. When a project is bootstrapped from this template, the design-system skill (`.omp/skills/design-system/`) guides the agent in filling in these sections with project-specific values.
```

This annotation:
- Prevents confusion about whether these rules apply to the template
- Guides agents to the design-system skill for downstream use
- Keeps conventions.md complete as a template (not stripping useful content)
- Maintains conventions.md's role as a reference for downstream projects

---

## 6. User Stories

### US1: Agent Loads design-system Skill

**As** an AI agent working in a project bootstrapped from omp-template
**When** I load the `design-system` skill (triggered by UI generation, color/font choices, component implementation, or visual review per AGENTS.md:188)
**I want** a SKILL.md with clear decision-tree guidance and a DESIGN.md with the 9-section brand contract format
**So that** I can generate consistent, brand-aligned UI even when the project hasn't filled in its brand values yet

**Acceptance Criteria:**
- `.omp/skills/design-system/SKILL.md` exists and follows the skill pattern
- `.omp/skills/design-system/DESIGN.md` exists with all 9 sections
- Each DESIGN.md section uses `[FILL]` placeholders with commented examples
- SKILL.md includes fallback guidance for unfilled brand contracts

### US2: Agent Reads conventions.md Without Confusion

**As** an AI agent working in the omp-template repository itself
**When** I read `conventions.md` as part of my context injection
**I want** no empty sections and clear distinction between template rules and downstream template content
**So that** I don't waste tokens on dead sections or mistakenly apply UI rules to a template that has no UI

**Acceptance Criteria:**
- No header in conventions.md has zero content before the next header
- CSS Ownership section contains a boundary statement
- Craft Rules section contains a reference to upstream sources
- UI Design section has an annotation clarifying it's downstream template content

### US3: Agent Reads tech-stack.md Without Broken References

**As** an AI agent assessing the project's tech stack
**When** I read `tech-stack.md` to understand dependencies, verification commands, and constraints
**I want** every file reference to resolve to an existing file
**So that** I don't follow broken links or assume infrastructure exists that doesn't

**Acceptance Criteria:**
- No reference to `.omp/design/` or `.omp/design/craft/` in tech-stack.md
- All remaining file references in tech-stack.md resolve to existing files
- Attribution for Open Design and refero_skill is preserved in the design-system skill

### US4: Agent Reads project.md for Orientation

**As** an AI agent being injected with project context
**When** I read `project.md` to understand the project's current phase
**I want** the milestone to reflect the actual active bead, not a stale closed one
**So that** I can correctly orient myself and contribute to current work

**Acceptance Criteria:**
- project.md Current Phase section references br-omp-backbone-skill-s2s (this bead)
- No reference to closed bead br-omp-backbone-skill-1da remains in project.md
- The "Next" field remains accurate

---

## 7. Technical Design

### 7.1 Affected Files

| File | Action | Impact |
|------|--------|--------|
| `.omp/skills/design-system/SKILL.md` | CREATE | New skill file |
| `.omp/skills/design-system/DESIGN.md` | CREATE | New brand contract template |
| `.omp/memory/project/tech-stack.md` | MODIFY | Remove 2 tables, 1 attribution line |
| `.omp/memory/project/conventions.md` | MODIFY | Fill 2 empty headers, add annotation to UI Design section |
| `.omp/memory/project/project.md` | MODIFY | Update milestone reference, add success criterion |

**Zero files deleted.** All changes are additive (create new) or subtractive within existing files (remove stale sections). No git rm operations.

### 7.2 SKILL.md Decision Tree

```
Agent loaded design-system skill
│
├─ Is this a template repo (no application code)?
│  └─ YES → DESIGN.md is a template. Guide the downstream project to fill it in.
│            Do NOT make design decisions for the template itself.
│
├─ Does DESIGN.md exist?
│  ├─ YES → Read it. Use the 9 sections as the source of truth for all visual decisions.
│  │         Forward to downstream project for value decisions on unfilled [FILL] slots.
│  │
│  └─ NO → Bootstrap mode. Prompt: "This project doesn't have a brand contract yet.
│           Would you like me to create one using the omp-template design-system format?"
│           If yes → Create DESIGN.md from template using 9-section format.
│           If no → Apply generic accessible defaults (WCAG 2.2 AA minimum).
│
└─ Is the downstream project requesting a design decision?
   ├─ Color → Check DESIGN.md Section 2 (Color Palette). Use defined tokens.
   │           If [FILL] → ask. Default: system colors.
   ├─ Typography → Check DESIGN.md Section 3 (Typography).
   │                If [FILL] → ask. Default: system font stack.
   ├─ Spacing → Check DESIGN.md Section 4. Use the 4px base scale.
   │             If [FILL] → use defaults: 4, 8, 12, 16, 24, 32, 48, 64, 96.
   ├─ Animation → Check DESIGN.md Section 6.
   │               If [FILL] → use sensible defaults (200ms enter, 140ms exit, canonical easing).
   ├─ Components → Check DESIGN.md Section 5.
   │                If [FILL] → use geometric progression defaults.
   └─ Theme → Check DESIGN.md Section 9.
               If [FILL] → light default with system media query for dark.
```

### 7.3 DESIGN.md 9-Section Template Structure

Each section follows this pattern:

```markdown
## N. Section Name

> Brief explanation of what this section defines and why it matters for UI consistency.

| Token | Value | Description |
|-------|-------|-------------|
| `--[category]-[name]` | `[FILL]` <!-- e.g., `#3B82F6` --> | What this token controls |
```

The `[FILL]` placeholder with HTML comment example is the key pattern — it makes the template immediately usable as a fill-in form while providing concrete guidance.

### 7.4 tech-stack.md Transformation

**Before (lines 65-89):**
```
## Design Assets

| Asset | Path | Purpose |
|-------|------|---------|
| Brand contract | `.omp/skills/design-system/DESIGN.md` | 9-section visual language spec |
| Design tokens | `.omp/design/tokens.css` | CSS custom properties (light + dark + system) |
| CSS base | `.omp/design/base.css` | Minimal reset + body defaults |
| CSS primitives | `.omp/design/primitives.css` | Base element styles (buttons, inputs, selects, tooltips) |

## Craft References

Brand-agnostic universal design rules that apply on top of any `.omp/skills/design-system/DESIGN.md`:

| File | Purpose |
|------|---------|
| `.omp/design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
| `.omp/design/craft/color.md` | Palette structure, accent discipline, contrast minimums, dark themes, semantic naming |
| `.omp/design/craft/anti-ai-slop.md` | Seven cardinal sins, soft tells, polish tells, soul-injection rules |
| `.omp/design/craft/animation-discipline.md` | When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits |
| `.omp/design/craft/state-coverage.md` | Loading, empty, error, edge-case states; which states must exist and what they must contain |
| `.omp/design/craft/accessibility-baseline.md` | WCAG 2.2 AA floor, contrast, touch targets, focus, labels, keyboard, ARIA discipline |
| `.omp/design/craft/form-validation.md` | Input state machine, validation timing, Constraint Validation API, error wiring, submit hygiene |
| `.omp/design/craft/typography-hierarchy.md` | Entry points, hierarchy vectors, rhythm failure modes, controlled violations |

Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
```

**After:**
```
(These sections are removed entirely. The Constraints section continues directly after the Security section.)
```

The file ends after the Constraints section. No design-related content remains in tech-stack.md.

### 7.5 conventions.md Empty Header Fix

**CSS Ownership (insert after `### CSS Ownership`, before `### Component Variants`):**

```
### CSS Ownership

CSS is a downstream project concern. The design-system skill (`.omp/skills/design-system/`) defines the brand contract format; downstream projects provide their own CSS implementation. Template memory files do not own or define CSS rules. The animation philosophy, component variants, theme, and icon guidelines in this section are template content — when a project is bootstrapped, the agent uses these as defaults that the project team customizes.
```

**Craft Rules (insert after `### Craft Rules`, before `### Theme`):**

```
### Craft Rules

Craft rules are brand-agnostic design principles originally from Open Design's `craft/` directory (Apache 2.0). These rules cover typography, color, anti-AI-slop, animation discipline, state coverage, accessibility baseline, form validation, and typography hierarchy. Downstream projects may integrate these rules; the template itself does not enforce them. See `.omp/skills/design-system/DESIGN.md` for the brand contract format that anchors craft rules to a project's specific visual language. The upstream craft rules are available at the Open Design repository for projects that want the full reference.
```

---

## 8. Edge Cases

| # | Edge Case | Handling |
|---|-----------|----------|
| EC1 | Another bead modifies the same files concurrently | br single-claim model prevents concurrent mutation. This bead is already claimed by makora1. |
| EC2 | DESIGN.md [FILL] placeholders are accidentally committed with real values | SKILL.md and DESIGN.md must contain ONLY [FILL] placeholders with comment examples. Review gate catches filled values. |
| EC3 | Downstream project has its own design system and ignores the template | DESIGN.md is a contract format, not an implementation. Downstream projects can replace or remove it entirely. The template doesn't enforce its use. |
| EC4 | tech-stack.md becomes too short after removing Design Assets + Craft References | The file will still cover Runtime, Dependencies, Verification Commands, Security, and Constraints — all substantive sections. Min length target: lines remain after removal. If it drops below 50 lines, consider consolidating but that's a separate bead. |
| EC5 | conventions.md UI Design section is still confusing after annotation | The annotation explicitly states it's template content for downstream use. If confusion persists, a future bead can relocate this section entirely to the design-system skill. |
| EC6 | Attribution removal from tech-stack.md loses license compliance | Attribution is preserved in the design-system skill's DESIGN.md. License compliance is maintained since the content being removed (design asset table entries) is being moved, not deleted without attribution. |
| EC7 | v2.2/design-system SKILL.md might already exist in a future version | This bead runs against the current repo state where it does not exist. If it appears mid-execution, the bead must detect and handle the conflict. |
| EC8 | conventions.md line numbers shift during editing | All edits use content-based matching (find-and-replace by section content), not line numbers. Line numbers in this PRD are for reference only. |

---

## 9. Dependencies

### Upstream Dependencies

| Dependency | Status | Impact if Unavailable |
|------------|--------|-----------------------|
| br CLI | Installed, operational | Cannot verify bead state after changes |
| bv CLI | Installed, operational | Cannot run triage to verify no regressions |
| git | Installed, operational | Cannot commit changes |
| File system (write access to .omp/) | Granted | Cannot create new files or modify existing ones |

All dependencies are satisfied. No external services required.

### Downstream Dependencies

| Dependent | How It's Affected | Mitigation |
|-----------|-------------------|------------|
| design-system skill loaders (agents generating UI) | They now have a real skill to load instead of a missing file | SKILL.md is created in this bead |
| tech-stack.md readers (agents assessing deps) | They no longer see broken references to non-existent design files | References removed in this bead |
| conventions.md readers (all agents) | They no longer encounter empty sections | Empty headers filled in this bead |
| project.md readers (all agents) | They see the correct current milestone | Updated in this bead |

---

## 10. Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|------------|--------|------------|
| R1 | DESIGN.md template format is too opinionated for diverse downstream projects | Medium | Low | Use [FILL] placeholders throughout — no hardcoded values. Each section explains what to specify, not what to choose. Downstream projects can freely restructure. |
| R2 | Removing tech-stack.md design tables surprises agents that cached those references | Low | Low | tech-stack.md is a Tier 2 memory file (loaded on-demand). Agents re-read it when tasks touch tooling. No persistent cache to invalidate. |
| R3 | DESIGN.md 9-section format conflicts with Open Design upstream format if it changes | Low | Low | The 9-section format is adapted from Open Design, not directly coupled. Attribution acknowledges the source without promising format compatibility. |
| R4 | conventions.md UI Design annotation is misinterpreted as "ignore this section" | Low | Low | Annotation says "template content for downstream projects" — agents should still read it when working on downstream projects. |
| R5 | Filling CSS Ownership and Craft Rules sections adds maintenance burden | Low | Low | Both sections are concise boundary statements (~3-4 lines each). They reduce confusion, which reduces maintenance burden overall. |

---

## 11. Verification Plan

### V1: File Existence Check

```bash
# Verify created files exist
test -f .omp/skills/design-system/SKILL.md && echo "PASS: SKILL.md exists" || echo "FAIL: SKILL.md missing"
test -f .omp/skills/design-system/DESIGN.md && echo "PASS: DESIGN.md exists" || echo "FAIL: DESIGN.md missing"

# Verify no stale references remain
grep -r '\.omp/design/' .omp/memory/project/ && echo "FAIL: stale .omp/design/ refs found" || echo "PASS: no stale refs"
grep -r '\.omp/design/' .omp/AGENTS.md && echo "FAIL: stale .omp/design/ refs in AGENTS.md" || echo "PASS: no stale refs in AGENTS.md"
```

### V2: Content Validation

```bash
# DESIGN.md has 9 sections
grep -c '^## [0-9]\.' .omp/skills/design-system/DESIGN.md | xargs -I{} sh -c 'test {} -eq 9 && echo "PASS: 9 sections" || echo "FAIL: {} sections (expected 9)"'

# DESIGN.md uses [FILL] placeholders (at least one per section)
grep -c '\[FILL\]' .omp/skills/design-system/DESIGN.md

# SKILL.md has required sections
grep -c '## When to use' .omp/skills/design-system/SKILL.md
grep -c '## When NOT to use' .omp/skills/design-system/SKILL.md
grep -c '## Process' .omp/skills/design-system/SKILL.md

# conventions.md has no empty headers
# (manual check: read file, verify content exists after each ### header)
```

### V3: Structural Integrity

```bash
# All memory files are valid markdown (no obvious structural issues)
for f in .omp/memory/project/*.md; do
  echo "Checking $f..."
  # Verify file ends with newline
  test "$(tail -c1 "$f")" = "" || echo "WARN: $f missing trailing newline"
done

# project.md milestone is current
grep "br-omp-backbone-skill-1da" .omp/memory/project/project.md && echo "FAIL: stale milestone ref" || echo "PASS: no stale milestone"
grep "br-omp-backbone-skill-s2s" .omp/memory/project/project.md && echo "PASS: current milestone present" || echo "FAIL: current milestone missing"
```

### V4: Graph Health

```bash
# No regressions
bv --robot-triage --format json
bv --robot-alerts --format json
br list --status open --status in_progress --json
```

### V5: Agent Load Test (Manual)

1. Load the `backbone` skill — confirm it references design-system as an existing skill
2. Load the `bv` skill — confirm triage output includes no new issues
3. Read `tech-stack.md` — confirm no broken references
4. Read `conventions.md` — confirm no empty sections, clear UI Design annotation
5. Read `project.md` — confirm current milestone is correct

---

## 12. Decisions

| # | Decision | Rationale | Date |
|---|----------|-----------|------|
| D1 | Create design-system skill, NOT .omp/design/ files | The skill provides the contract format (SKILL.md + DESIGN.md). The .omp/design/ files are downstream project artifacts. Creating them in the template would be misleading — they'd contain fake token values that confuse agents. | 2026-06-18 |
| D2 | Remove Design Assets and Craft References tables from tech-stack.md entirely | These tables are the primary source of broken references. Moving them (vs. deleting them) would require creating the referenced files, which is a non-goal. Their content (attribution, purpose) is preserved in the design-system skill. | 2026-06-18 |
| D3 | Fill empty headers in conventions.md rather than deleting them | The headers are in the UI Design section which is retained as downstream template content. Deleting them would lose structural context. Filling them with boundary statements adds clarity. | 2026-06-18 |
| D4 | Keep conventions.md UI Design section with annotation | The section contains valuable default rules (animation philosophy, component variants, icon conventions) that downstream projects benefit from. Moving it to the design-system skill would be a larger refactor — tabled for a future bead if needed. | 2026-06-18 |
| D5 | Add success criterion for zero broken references to project.md | This makes the cleanup verifiable and sets a quality bar for future maintenance. Aligns with the existing 3 success criteria. | 2026-06-18 |

---

## 13. Implementation Approach

### Wave 1: Create design-system skill (R1)
- Write `.omp/skills/design-system/SKILL.md` with decision tree
- Write `.omp/skills/design-system/DESIGN.md` with 9-section template
- Verify both files exist with correct structure

### Wave 2: Clean tech-stack.md (R2)
- Remove Design Assets table
- Remove Craft References table
- Remove attribution line
- Verify no broken references remain

### Wave 3: Fix conventions.md (R3, R5)
- Fill CSS Ownership header
- Fill Craft Rules header
- Add UI Design section annotation
- Verify no empty headers

### Wave 4: Update project.md (R4)
- Update milestone reference
- Add success criterion
- Verify no stale references

Waves 1 and 2 can run in parallel (independent files). Waves 3 and 4 are independent but should follow Wave 1 (since conventions.md references design-system path).

---

## 14. Acceptance Criteria (Summary)

1. `.omp/skills/design-system/SKILL.md` exists with When-to-use, When-NOT-to-use, and Process sections
2. `.omp/skills/design-system/DESIGN.md` exists with exactly 9 sections, all using `[FILL]` placeholders
3. `tech-stack.md` contains zero references to `.omp/design/` or `.omp/design/craft/`
4. `conventions.md` has zero empty headers (content exists after every `###` before the next header)
5. `conventions.md` UI Design section has annotation clarifying it's downstream template content
6. `project.md` Current Phase section references `br-omp-backbone-skill-s2s`, not `br-omp-backbone-skill-1da`
7. `project.md` includes success criterion for zero broken file references
8. `bv --robot-triage` reports no new issues
9. Attribution for Open Design and refero_skill is preserved in the design-system skill
10. No existing skills or command files are modified

---

## 15. Out of Scope (Explicit)

- Creating `.omp/design/` directory or any files within it
- Creating `.omp/design/craft/` directory or any craft reference files
- Implementing any CSS, design tokens, or visual assets
- Modifying any skill files other than the new design-system skill
- Modifying AGENTS.md (it already correctly lists design-system as a skill)
- Modifying any of the 13 closed bead artifacts
- Adding new commands
- Adding new extensions
- Changing the workflow gate or any enforcement mechanism
- Changing conventions beyond the identified issues
- Running a full workflow verification cycle (that's the "Next" milestone)

---

## 16. Rollback Plan

If this bead introduces regressions:

1. **Delete created files:**
   ```bash
   rm -rf .omp/skills/design-system/
   ```

2. **Revert modified files via git:**
   ```bash
   git checkout -- .omp/memory/project/tech-stack.md
   git checkout -- .omp/memory/project/conventions.md
   git checkout -- .omp/memory/project/project.md
   ```

3. **Verify rollback:**
   ```bash
   bv --robot-triage --format json  # Should match pre-change state
   test -d .omp/skills/design-system && echo "FAIL: not fully rolled back" || echo "PASS: rolled back"
   ```

No database migrations, no API changes, no infrastructure changes — rollback is pure git + rm.

---

*PRD version: 1.0 | Created by: makora1 | Phase: /create*
