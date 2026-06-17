<!-- DENSITY: Target ≥600 lines. This plan covers 5 files (2 new, 3 modify), 4 waves, full architecture, test strategy, migration plan, rollback plan, and timeline. -->
# Plan: br-omp-backbone-skill-s2s

**Goal:** Eliminate all broken file references, empty headers, and stale milestone data from memory files; create the missing design-system skill with a 9-section brand contract template so agents loading this project encounter zero dead links and zero empty sections.

## Graph Context

- **Blast radius:** 5 files (2 new, 3 edits, 0 deletes)
- **Unblocks:** None — this is a cleanup bead with no downstream dependents
- **Blocked by:** None — all upstream dependencies (br, bv, git, filesystem) are satisfied
- **Critical path:** No — no other bead depends on this work
- **Forecast:** 25 minutes (confidence 0.92)
- **Hotspots touched:** None — no files have >3 bead history; all prior beads are closed and immutable

## Observable Truths

Each of these statements is falsifiable — a `grep`, `test -f`, or `read` can confirm or refute it before and after implementation.

1. `.omp/skills/design-system/` does not exist on disk — `ls .omp/skills/design-system/` returns "No such file or directory"
2. `tech-stack.md` contains 12 references to `.omp/design/` or `.omp/design/craft/` across lines 65–89 (Design Assets table + Craft References table + attribution line)
3. `conventions.md` has two headers with zero content: `### CSS Ownership` (line 112) followed immediately by `### Component Variants` (line 113), and `### Craft Rules` (line 118) followed immediately by `### Theme` (line 119)
4. `conventions.md` UI Design section (lines 97–131) has no annotation clarifying it is downstream template content
5. `project.md` line 23 references closed bead `br-omp-backbone-skill-1da` as the active milestone
6. `project.md` Success Criteria section has exactly 3 entries — no criterion for broken file references
7. `AGENTS.md` line 188 already lists `design-system` as a loadable skill with trigger conditions
8. `AGENTS.md` lines 224–226 reference `.omp/skills/design-system/SKILL.md` and `DESIGN.md` in the tree diagram — these paths don't exist yet
9. The `design/` directory at repo root contains CSS files (`tokens.css`, `base.css`, `primitives.css`) and craft docs — these are downstream project artifacts, not template infrastructure, and are OUT OF SCOPE for this bead
10. 17 skill directories exist under `.omp/skills/` excluding design-system — this bead creates the 18th
11. Attribution for Open Design (Apache 2.0) and refero_skill (MIT) currently lives only in `tech-stack.md` line 89 — must be preserved in the new design-system skill
12. The bv graph shows this bead as the sole in-progress item with score 0.209 and no blockers — no contention risk
13. `tech-stack.md` section markers: `## Design Assets` (line 65) through attribution line (line 89) inclusive — exactly 25 lines to remove

## Architecture

### System Context

The omp-template repository is a workflow infrastructure template. It has no application runtime, no backend, no frontend. Its sole purpose is to provide agent instructions (skills, commands, conventions) and project scaffolding (memory files, templates, extensions) for downstream projects.

The design-system skill bridges a specific gap: when a downstream project bootstraps from this template and an agent is asked to generate UI, it needs a *contract* for what to ask the user about their brand. Without this contract, agents either guess (producing inconsistent output) or ask unstructured questions (wasting user time).

### Component Relationship Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Context Load                    │
│                                                         │
│  AGENTS.md (always loaded)                               │
│  ├── Lists design-system as skill (line 188)             │
│  ├── Tree diagram shows design-system/ dir (lines 224-6)│
│  └── Skills Map says "load when generating UI..."        │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────┐        │
│  │     design-system skill (NEW — this bead)    │        │
│  │                                              │        │
│  │  SKILL.md         DESIGN.md                  │        │
│  │  ┌──────────┐     ┌──────────────────┐       │        │
│  │  │ Decision  │────▶│ 9-section brand  │       │        │
│  │  │ tree      │     │ contract format  │       │        │
│  │  │           │     │                  │       │        │
│  │  │ When to   │     │ 1. Brand Identity│       │        │
│  │  │ use       │     │ 2. Color Palette │       │        │
│  │  │ When NOT  │     │ 3. Typography    │       │        │
│  │  │ to use    │     │ 4. Spacing       │       │        │
│  │  │ Process   │     │ 5. Components    │       │        │
│  │  └──────────┘     │ 6. Animation     │       │        │
│  │                    │ 7. Iconography   │       │        │
│  │                    │ 8. Imagery       │       │        │
│  │                    │ 9. Theme         │       │        │
│  │                    └──────────────────┘       │        │
│  └─────────────────────────────────────────────┘        │
│                                                         │
│  Memory files (Tier 1 always, Tier 2 on-demand)         │
│  ├── conventions.md                                      │
│  │   ├── UI Design section (annotated as downstream)     │
│  │   ├── CSS Ownership (filled — boundary statement)     │
│  │   └── Craft Rules (filled — upstream reference)       │
│  ├── project.md                                          │
│  │   ├── Current Phase → s2s milestone                   │
│  │   └── Success Criteria → +zero broken refs            │
│  └── tech-stack.md                                       │
│      ├── Design Assets table → REMOVED                   │
│      ├── Craft References table → REMOVED                │
│      └── Attribution line → MOVED to DESIGN.md           │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

```
DESIGN.md (template) ──load──▶ Agent in downstream project
                                    │
                            Reads 9 [FILL] sections
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              Section filled   Section unfilled  Bootstrap mode
              → Use value      → Apply default    → Prompt user
                                 (WCAG AA safe)     to fill contract
```

### File Ownership and Boundaries

| File | Owner | Contents | Lifetime |
|------|-------|----------|----------|
| `.omp/skills/design-system/SKILL.md` | This bead (CREATE) | Decision tree for design-system skill | Permanent — template infrastructure |
| `.omp/skills/design-system/DESIGN.md` | This bead (CREATE) | 9-section brand contract template with `[FILL]` placeholders | Permanent — downstream projects edit their copy |
| `.omp/memory/project/tech-stack.md` | This bead (MODIFY) | Remove Design Assets + Craft References tables | Change is permanent — no future bead should re-add |
| `.omp/memory/project/conventions.md` | This bead (MODIFY) | Fill CSS Ownership + Craft Rules; annotate UI Design | Change is permanent — empty headers eliminated |
| `.omp/memory/project/project.md` | This bead (MODIFY) | Update milestone reference + add success criterion | Updated per milestone — next bead will overwrite milestone again |

## Component Breakdown

### Component 1: design-system SKILL.md

**Purpose:** Decision tree that tells an agent *what to do* when generating UI in a project bootstrapped from this template.

**Structure:**

```
Frontmatter (YAML)
  ├── name: design-system
  └── description: When to use, when not to use, process steps

# design-system

## Purpose
  └── States: this is a brand contract TEMPLATE, not a completed design system.
      Explains the relationship between SKILL.md (decision flow) and
      DESIGN.md (brand values).

## When to Use
  └── List of trigger conditions matching AGENTS.md:188:
      - Generating UI components or pages
      - Choosing colors, fonts, or spacing values
      - Implementing component variants
      - Reviewing visual output for brand consistency
      - Setting up a new project's design tokens

## When NOT to Use
  └── Anti-patterns:
      - Don't load for backend-only changes
      - Don't load for documentation or config edits
      - Don't load for infrastructure/CLI work
      - Don't load if a full design system already exists in the project

## Decision Tree
  └── ASCII decision tree (per PRD Section 7.2):
      Agent loaded design-system skill
      ├─ Is this a template repo (no application code)?
      │  └─ YES → DESIGN.md is a template. Guide the downstream project to fill it.
      │            Do NOT make design decisions for the template itself.
      ├─ Does DESIGN.md exist?
      │  ├─ YES → Read it. Use the 9 sections as source of truth.
      │  │         Forward to downstream project for unfilled [FILL] slots.
      │  └─ NO → Bootstrap mode. Offer to create DESIGN.md from 9-section format.
      │           If declined → apply generic accessible defaults (WCAG 2.2 AA).
      └─ Is the downstream project requesting a design decision?
         ├─ Color → Check Section 2. If [FILL] → ask. Default: system colors.
         ├─ Typography → Check Section 3. If [FILL] → ask. Default: system font stack.
         ├─ Spacing → Check Section 4. Use 4px base scale.
         │             If [FILL] → defaults: 4, 8, 12, 16, 24, 32, 48, 64, 96.
         ├─ Animation → Check Section 6.
         │               If [FILL] → 200ms enter, 140ms exit, canonical easing.
         ├─ Components → Check Section 5.
         │                If [FILL] → geometric progression defaults.
         └─ Theme → Check Section 9.
                     If [FILL] → light default with system media query for dark.

## Process
  └── Step-by-step agent instructions:
      1. Check if DESIGN.md exists and has filled values
      2. Read the relevant section for the current decision
      3. Apply filled values if present; use defaults if [FILL]
      4. Record any new design decisions in DESIGN.md
      5. Verify output against WCAG 2.2 AA minimums

## Defaults (Fallback When DESIGN.md is Unfilled)
  └── Safe defaults for each section:
      - Color: System color scheme (CanvasText, Canvas, LinkText, etc.)
      - Typography: System font stack (-apple-system, BlinkMacSystemFont, etc.)
      - Spacing: 4px base scale (4, 8, 12, 16, 24, 32, 48, 64, 96)
      - Animation: 200ms enter, 140ms exit, cubic-bezier(0.23,1,0.32,1)
      - Components: 6px border-radius, 0 2px 8px shadow, 1.5px border
      - Theme: Light default, dark via prefers-color-scheme

## Attribution
  └── Open Design craft/ directory (Apache 2.0)
      refero_skill (MIT)
      Link format matching existing template conventions

## Related Skills
  └── Cross-references to other skills the agent might also need
```

**Input contract:** Agent loads this skill → receives decision tree + fallback defaults.

**Output contract:** Agent makes a design decision (either from DESIGN.md values, fallback defaults, or by asking the user).

**Error states:**
- DESIGN.md doesn't exist → Bootstrap mode (offer to create)
- DESIGN.md exists but section missing → Treat as [FILL], apply default
- DESIGN.md has conflicting values → Surface to user for resolution
- Agent is in template repo itself → Guide, don't enforce

### Component 2: design-system DESIGN.md

**Purpose:** The 9-section brand contract template. This is what downstream projects fill in with their actual brand values.

**Structure (exactly 9 sections):**

```
## 1. Brand Identity
   > Captures the brand name, tagline, and voice/tone keywords that shape all visual and textual output.
   
   | Property | Value | Notes |
   |----------|-------|-------|
   | `brand-name` | `[FILL]` <!-- e.g., "Acme Corp" --> | Used in page titles, headers, and meta |
   | `tagline` | `[FILL]` <!-- e.g., "Build faster" --> | Optional — appears in hero/header areas |
   | `voice` | `[FILL]` <!-- e.g., "Professional, warm, direct" --> | 3-5 keywords guiding copy tone |
   | `target-audience` | `[FILL]` <!-- e.g., "Enterprise developers" --> | Informs information density and complexity |

## 2. Color Palette
   > Defines the core color system. All colors must meet WCAG 2.2 AA contrast minimums against their intended backgrounds.

   | Token | Value | Description |
   |-------|-------|-------------|
   | `--color-primary` | `[FILL]` <!-- e.g., `#3B82F6` --> | Primary brand color — CTAs, links, active states |
   | `--color-primary-hover` | `[FILL]` <!-- e.g., `#2563EB` --> | 10-15% darker than primary |
   | `--color-secondary` | `[FILL]` <!-- e.g., `#8B5CF6` --> | Secondary brand color — accents, highlights |
   | `--color-accent` | `[FILL]` <!-- e.g., `#F97316` --> | High-attention elements — notifications, badges |
   | `--color-neutral-50` | `[FILL]` <!-- e.g., `#FAFAFA` --> | Lightest — page backgrounds |
   | `--color-neutral-100` | `[FILL]` <!-- e.g., `#F5F5F5` --> | Surface backgrounds |
   | `--color-neutral-200` | `[FILL]` <!-- e.g., `#E5E5E5` --> | Borders, dividers |
   | `--color-neutral-300...900` | `[FILL]` | Scale to darkest text/background |
   | `--color-success` | `[FILL]` <!-- e.g., `#22C55E` --> | Success states, confirmations |
   | `--color-warning` | `[FILL]` <!-- e.g., `#F59E0B` --> | Warnings, cautions |
   | `--color-error` | `[FILL]` <!-- e.g., `#EF4444` --> | Errors, destructive actions |
   | `--color-info` | `[FILL]` <!-- e.g., `#3B82F6` --> | Informational elements |

   > Every token must have a dark-mode counterpart. Use perceptual equivalence — not the same hex value darkened.

## 3. Typography
   > Font families, type scale, and weight assignments. Prefer system fonts as fallbacks to avoid FOUT.

   | Token | Value | Description |
   |-------|-------|-------------|
   | `--font-heading` | `[FILL]` <!-- e.g., `'Inter', system-ui, sans-serif` --> | h1–h4, card titles, nav labels |
   | `--font-body` | `[FILL]` <!-- e.g., `'Inter', system-ui, sans-serif` --> | Body text, inputs, labels |
   | `--font-mono` | `[FILL]` <!-- e.g., `'JetBrains Mono', monospace` --> | Code blocks, inline code, data tables |
   | `--text-xs` | `[FILL]` <!-- e.g., `0.75rem` (12px) --> | Captions, legal, metadata |
   | `--text-sm` | `[FILL]` <!-- e.g., `0.875rem` (14px) --> | Secondary text, labels, help text |
   | `--text-base` | `[FILL]` <!-- e.g., `1rem` (16px) --> | Body text — the default |
   | `--text-lg` | `[FILL]` <!-- e.g., `1.125rem` (18px) --> | Lead paragraphs, emphasized body |
   | `--text-xl` | `[FILL]` <!-- e.g., `1.25rem` (20px) --> | h4, card titles |
   | `--text-2xl` | `[FILL]` <!-- e.g., `1.5rem` (24px) --> | h3 |
   | `--text-3xl` | `[FILL]` <!-- e.g., `1.875rem` (30px) --> | h2 |
   | `--text-4xl` | `[FILL]` <!-- e.g., `2.25rem` (36px) --> | h1, hero headings |
   | `--font-weight-normal` | `[FILL]` <!-- e.g., `400` --> | Body, labels |
   | `--font-weight-medium` | `[FILL]` <!-- e.g., `500` --> | Emphasized body, button text |
   | `--font-weight-semibold` | `[FILL]` <!-- e.g., `600` --> | h3–h4, strong emphasis |
   | `--font-weight-bold` | `[FILL]` <!-- e.g., `700` --> | h1–h2 |
   | `--line-height-tight` | `[FILL]` <!-- e.g., `1.25` --> | Headings |
   | `--line-height-normal` | `[FILL]` <!-- e.g., `1.5` --> | Body text |
   | `--line-height-relaxed` | `[FILL]` <!-- e.g., `1.75` --> | Long-form reading |

## 4. Spacing & Layout
   > 4px base spacing scale. All padding, margin, gap, and layout values derive from this scale.

   | Token | Value | Description |
   |-------|-------|-------------|
   | `--space-1` | `[FILL]` <!-- e.g., `0.25rem` (4px) --> | Minimum spacing — inline gaps |
   | `--space-2` | `[FILL]` <!-- e.g., `0.5rem` (8px) --> | Tight padding, icon-text gaps |
   | `--space-3` | `[FILL]` <!-- e.g., `0.75rem` (12px) --> | Compact section padding |
   | `--space-4` | `[FILL]` <!-- e.g., `1rem` (16px) --> | Default padding/gap |
   | `--space-6` | `[FILL]` <!-- e.g., `1.5rem` (24px) --> | Section padding |
   | `--space-8` | `[FILL]` <!-- e.g., `2rem` (32px) --> | Large section spacing |
   | `--space-12` | `[FILL]` <!-- e.g., `3rem` (48px) --> | Page-level spacing |
   | `--space-16` | `[FILL]` <!-- e.g., `4rem` (64px) --> | Hero/landing spacing |
   | `--content-max-width` | `[FILL]` <!-- e.g., `72rem` (1152px) --> | Max content width for readability |
   | `--content-narrow` | `[FILL]` <!-- e.g., `40rem` (640px) --> | Reading-optimized column width |
   | `--grid-columns` | `[FILL]` <!-- e.g., `12` --> | Grid column count |
   | `--grid-gap` | `[FILL]` <!-- e.g., `var(--space-6)` --> | Default grid gap |

## 5. Component Tokens
   > Shared visual properties that apply across components. These are the "atoms" that components compose.

   | Token | Value | Description |
   |-------|-------|-------------|
   | `--radius-sm` | `[FILL]` <!-- e.g., `0.25rem` (4px) --> | Checkboxes, badges, tags |
   | `--radius-md` | `[FILL]` <!-- e.g., `0.375rem` (6px) --> | Buttons, inputs, cards (default) |
   | `--radius-lg` | `[FILL]` <!-- e.g., `0.5rem` (8px) --> | Modals, drawers, large cards |
   | `--radius-full` | `[FILL]` <!-- e.g., `9999px` --> | Pills, avatars, round buttons |
   | `--shadow-sm` | `[FILL]` <!-- e.g., `0 1px 2px rgba(0,0,0,0.05)` --> | Subtle elevation — cards on white |
   | `--shadow-md` | `[FILL]` <!-- e.g., `0 4px 6px rgba(0,0,0,0.07)` --> | Dropdowns, tooltips |
   | `--shadow-lg` | `[FILL]` <!-- e.g., `0 10px 25px rgba(0,0,0,0.1)` --> | Modals, drawers |
   | `--border-width` | `[FILL]` <!-- e.g., `1px` --> | Default border width |
   | `--border-width-focus` | `[FILL]` <!-- e.g., `2px` --> | Focus ring width |
   | `--opacity-disabled` | `[FILL]` <!-- e.g., `0.5` --> | Disabled state opacity |
   | `--opacity-hover` | `[FILL]` <!-- e.g., `0.08` --> | Hover overlay opacity (on dark) |

## 6. Animation
   > Duration tokens, easing curves, and reduced-motion policy. All transitions must respect `prefers-reduced-motion`.

   | Token | Value | Description |
   |-------|-------|-------------|
   | `--dur-instant` | `[FILL]` <!-- e.g., `80ms` --> | Checkbox toggle, ripple start |
   | `--dur-quick` | `[FILL]` <!-- e.g., `120ms` --> | Hover/focus transitions, micro-feedback |
   | `--dur-normal` | `[FILL]` <!-- e.g., `200ms` --> | UI element enter (default) |
   | `--dur-exit` | `[FILL]` <!-- e.g., `140ms` --> | UI element exit — shorter than enter |
   | `--dur-slow` | `[FILL]` <!-- e.g., `300ms` --> | Page transitions, complex animations |
   | `--easing-standard` | `[FILL]` <!-- e.g., `cubic-bezier(0.23,1,0.32,1)` --> | The single canonical curve for UI transitions |
   | `--easing-decelerate` | `[FILL]` <!-- e.g., `cubic-bezier(0,0,0.2,1)` --> | Enter animations — decelerate to rest |
   | `--easing-accelerate` | `[FILL]` <!-- e.g., `cubic-bezier(0.4,0,1,1)` --> | Exit animations — accelerate away |
   | `--reduced-motion` | `prefers-reduced-motion: reduce` | Respect OS setting — disable all non-essential animation |

## 7. Iconography
   > Icon library, sizing conventions, and accessibility rules.

   | Token | Value | Description |
   |-------|-------|-------------|
   | `--icon-library` | `[FILL]` <!-- e.g., `lucide`, `heroicons`, `phosphor` --> | Single consistent icon set |
   | `--icon-size-sm` | `[FILL]` <!-- e.g., `16px` --> | Inline with body text |
   | `--icon-size-md` | `[FILL]` <!-- e.g., `20px` --> | Toolbar buttons, nav items |
   | `--icon-size-lg` | `[FILL]` <!-- e.g., `24px` --> | Large controls, hero icons |
   | `--icon-stroke` | `[FILL]` <!-- e.g., `1.5px` --> | Preferred stroke width |
   | `--icon-color` | `currentColor` | Icons inherit text color by default |

   > **Accessibility rules:** Icon-only buttons MUST have `aria-label`. SVGs repeating adjacent text MUST use `aria-hidden="true" focusable="false"`. Never use emoji as UI icons.

## 8. Imagery
   > Illustration style, photo treatment, and aspect ratios. Defines the visual character of non-icon graphics.

   | Token | Value | Description |
   |-------|-------|-------------|
   | `--illustration-style` | `[FILL]` <!-- e.g., "Flat vector, 2-color duotone, rounded corners" --> | Style for empty states, onboarding, hero art |
   | `--photo-treatment` | `[FILL]` <!-- e.g., "Natural lighting, no heavy filters, slight warm tint" --> | Photo editing style |
   | `--avatar-shape` | `[FILL]` <!-- e.g., `circle` or `rounded` --> | User avatar shape |
   | `--image-aspect-hero` | `[FILL]` <!-- e.g., `16/9` --> | Hero/banner image aspect ratio |
   | `--image-aspect-card` | `[FILL]` <!-- e.g., `4/3` or `3/2` --> | Card thumbnail aspect ratio |
   | `--image-radius` | `[FILL]` <!-- e.g., `var(--radius-md)` --> | Default image border-radius |

## 9. Theme
   > Light/dark/system mode strategy and token naming convention.

   | Token | Value | Description |
   |-------|-------|-------------|
   | `--theme-default` | `[FILL]` <!-- e.g., `light` --> | Default mode on first visit |
   | `--theme-strategy` | `[FILL]` <!-- e.g., `system` --> | How mode is detected: `system`, `manual`, or `both` |
   | `--theme-attribute` | `[FILL]` <!-- e.g., `data-theme` --> | HTML attribute for explicit theme toggle |
   | `--theme-selector` | `[FILL]` <!-- e.g., `[data-theme="dark"]` --> | CSS selector for dark mode overrides |
   | `--theme-media` | `@media (prefers-color-scheme: dark)` | System preference media query |

   > **Token naming convention:** All design tokens use `--<category>-<name>` pattern. Semantic names over presentational names. Dark-mode counterparts use the same token name but different values under the theme selector.

---
> **Attribution:** Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT). The 9-section structure is this template's own organizational format; the design principles within each section draw from Open Design's craft rules.
```

**Input contract:** Downstream agent reads this file → receives a fill-in form with exactly 9 sections, each containing `[FILL]` placeholders with HTML comment examples.

**Output contract:** Agent fills in values or applies defaults. The file becomes the downstream project's single source of truth for visual language.

**Error states:**
- `[FILL]` placeholder encountered → Agent applies fallback default from SKILL.md or asks user
- Section missing entirely → Agent treats all tokens in that category as unfilled
- Conflicting values across sections → Agent surfaces conflict for human resolution
- File is empty/missing → Agent enters bootstrap mode per SKILL.md decision tree

### Component 3: tech-stack.md Modification

**Purpose:** Remove all references to non-existent `.omp/design/` and `.omp/design/craft/` files while preserving the file's structural integrity for its remaining content.

**Current state (lines 65–89):**
- `## Design Assets` (line 65) — table with 4 entries referencing `.omp/design/` files
- `## Craft References` (line 74) — table with 8 entries referencing `.omp/design/craft/` files
- Attribution line (line 89) — credits Open Design and refero_skill

**Target state:**
- Lines 65–89 are removed entirely
- The `## Constraints` section (line 58) flows directly to the end of the file
- No orphan references remain — `grep -r "\.omp/design/" .omp/memory/project/tech-stack.md` returns zero matches
- Attribution is preserved in `.omp/skills/design-system/DESIGN.md` (see Component 2 footer)

**Edge cases:**
- File total line count drops from 90 lines to 65 lines — still substantive (Runtime, Dependencies, Verification Commands, Security, Constraints all remain)
- No other section references the removed content — the tables are self-contained
- The `## Security` section's code block (lines 50–56) and `## Constraints` section (lines 58–63) are untouched

### Component 4: conventions.md Modification

**Purpose:** Fill two empty headers and add a contextual annotation to the UI Design section header.

**Change 1 — CSS Ownership (after line 112, before line 113):**

The header `### CSS Ownership` on line 112 has zero content before `### Component Variants` on line 113.

Fill with boundary statement:
```
### CSS Ownership

CSS is a downstream project concern. The design-system skill (`.omp/skills/design-system/`) defines the brand contract format; downstream projects provide their own CSS implementation. Template memory files do not own or define CSS rules. The animation philosophy, component variants, theme, and icon guidelines in this section are template content — when a project is bootstrapped, the agent uses these as defaults that the project team customizes.
```

This statement:
- Clarifies that CSS is not owned by the template
- Points to the design-system skill for the contract format
- Acknowledges that the UI Design section is template content, not template rules

**Change 2 — Craft Rules (after line 118, before line 119):**

The header `### Craft Rules` on line 118 has zero content before `### Theme` on line 119.

Fill with reference statement:
```
### Craft Rules

Craft rules are brand-agnostic design principles originally from Open Design's `craft/` directory (Apache 2.0). These rules cover typography, color, anti-AI-slop, animation discipline, state coverage, accessibility baseline, form validation, and typography hierarchy. Downstream projects may integrate these rules; the template itself does not enforce them. See `.omp/skills/design-system/DESIGN.md` for the brand contract format that anchors craft rules to a project's specific visual language. The upstream craft rules are available at the Open Design repository for projects that want the full reference.
```

This statement:
- Credits the upstream source (Open Design)
- Lists the craft rule categories (typography, color, anti-AI-slop, etc.)
- Clarifies the template doesn't enforce these rules
- Points to DESIGN.md for the contract format

**Change 3 — UI Design Section Annotation (before line 97):**

Insert immediately after `## UI Design` on line 97:
```
> **Note:** This section is template content for downstream projects, not rules that apply to the omp-template repository itself. The template has no application runtime or UI code. When a project is bootstrapped from this template, the design-system skill (`.omp/skills/design-system/`) guides the agent in filling in these sections with project-specific values.
```

This annotation:
- Prevents confusion about whether UI rules apply to the template
- Guides agents to the design-system skill for downstream use
- Keeps conventions.md complete as a template (not stripping useful content)
- Maintains conventions.md's role as a reference for downstream projects

**Edge cases:**
- Line numbers in conventions.md shift after each edit — all edits use content-based insertion, not line numbers
- If conventions.md has been modified since this PRD was written, content matching still works as long as the `### CSS Ownership` and `### Craft Rules` headers exist
- The annotation is additive only — if it already exists, don't double-insert (check before inserting)

### Component 5: project.md Modification

**Purpose:** Update stale milestone reference and add verifiable success criterion.

**Change 1 — Current Phase section (lines 22–24):**

Replace:
```
- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md fix
```

With:
```
- **Status:** active
- **Milestone:** Design asset audit and memory file cleanup (br-omp-backbone-skill-s2s)
- **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md and tech-stack.md cleanup
```

**Change 2 — Success Criteria section (after line 17):**

Add as entry 4:
```
4. **Zero broken file references in memory files** — `grep -oP '\.omp/[\w/.-]+\.\w+' .omp/memory/project/*.md | while read f; do test -f "$f" || echo "$f"; done` returns no output
```

**Edge cases:**
- If project.md milestone has already been updated (e.g., by a concurrent bead), the content match will fail. In that case, read the file fresh and update whatever text is present.
- The "Next" field text change is cosmetic — it adds "and tech-stack.md" to reflect what this bead actually cleans up.

## Data Models

There are no data models in this bead. All artifacts are plain Markdown files. The only "data" is:

| Entity | Format | Fields | Validation |
|--------|--------|--------|------------|
| SKILL.md | Markdown + YAML frontmatter | name, description, When to Use, When NOT to Use, Process, Decision Tree, Defaults, Attribution | Required sections present; decision tree is valid ASCII art; attribution includes both licenses |
| DESIGN.md | Markdown tables | 9 numbered sections, each with Token/Value/Description columns | Exactly 9 `## N.` headers; every table has `[FILL]` in Value column with HTML comment example; attribution footer present |
| tech-stack.md | Markdown tables | Runtime, Dependencies, Verification Commands, Security, Constraints | No `## Design Assets` or `## Craft References` headers; no `.omp/design/` string anywhere in file |
| conventions.md | Markdown prose + lists | Naming, Languages, Skill Structure, Command Structure, Git, Workflow, Agent Conventions, Honcho Memory, Memory File Maintenance, UI Design | No header immediately followed by another header of same/higher level with no content between; UI Design section has annotation blockquote |
| project.md | Markdown prose + lists | Goal, Success Criteria, Current Phase | Success Criteria has ≥4 entries including the new broken-refs criterion; Current Phase milestone = s2s |

## API Contracts

There are no APIs in this bead. The template has no application code. The only "contracts" are:

### Skill Load Contract

**Provider:** `.omp/skills/design-system/SKILL.md`
**Consumer:** OMP agent context loader (resolves skill names to file paths)
**Contract:**
1. File exists at `.omp/skills/design-system/SKILL.md`
2. File has valid YAML frontmatter with `name: design-system`
3. File has `## When to use` and `## When NOT to use` sections
4. File has a `## Process` section with numbered steps

**Breaking changes:** None — this is a new file, no consumers exist yet.

### Brand Contract Template Contract

**Provider:** `.omp/skills/design-system/DESIGN.md`
**Consumer:** Any agent generating UI in a downstream project
**Contract:**
1. File has exactly 9 numbered sections (`## 1.` through `## 9.`)
2. Each section has a table with at minimum Token, Value, Description columns
3. All Value cells contain `[FILL]` or `currentColor` (for icon-color)
4. All `[FILL]` placeholders have adjacent HTML comment examples

**Breaking changes:** None — this is a new file. Downstream projects may modify or replace it.

### Memory File Integrity Contract

**Provider:** All files in `.omp/memory/project/*.md`
**Consumer:** OMP agent context loader (injects Tier 1 files, loads Tier 2 on-demand)
**Contract:**
1. Every file path referenced within a memory file resolves to an existing file
2. No header is followed by zero content before the next header of same/higher level
3. project.md Current Phase section accurately reflects the active bead

**Breaking changes:** None — this bead restores compliance with an existing contract that was violated.

## Test Strategy

### Test Approach

This bead has no application code, so there are no unit tests, integration tests, or E2E tests in the traditional sense. Verification is entirely structural — file existence, content pattern matching, and graph health checks.

### Test Categories

| Category | What It Tests | How | Blocking? |
|----------|--------------|-----|-----------|
| File existence | Created files exist on disk | `test -f <path>` | Yes — if SKILL.md or DESIGN.md don't exist, nothing else matters |
| Section count | DESIGN.md has exactly 9 sections | `grep -c '^## [0-9]\.'` returns 9 | Yes — the contract format requires exactly 9 sections |
| Placeholder presence | Every DESIGN.md section uses `[FILL]` | `grep -c '\[FILL\]'` returns ≥9 (at least one per section) | Yes — no downstream project values in the template |
| Required sections | SKILL.md has When to Use, When NOT to Use, Process | `grep -c` for each section header returns ≥1 | Yes — these are the skill pattern requirements |
| Stale references gone | No `.omp/design/` string in tech-stack.md or any memory file | `grep -r '\.omp/design/' .omp/memory/project/` returns zero matches | Yes — this is the primary goal |
| Empty headers gone | No header in conventions.md has zero content | Visual inspection: read file, verify content exists after each `###` before next header | Yes — this is a stated requirement |
| UI Design annotated | conventions.md UI Design section has clarifying annotation | `grep 'template content for downstream projects' .omp/memory/project/conventions.md` returns a match | Yes — this is a stated requirement |
| Milestone current | project.md references s2s, not 1da | `grep 'br-omp-backbone-skill-1da'` returns no match; `grep 'br-omp-backbone-skill-s2s'` returns a match | Yes — stale milestone is a stated problem |
| Success criterion added | project.md has broken-refs criterion | `grep 'Zero broken file references' .omp/memory/project/project.md` returns a match | Yes — stated in requirements |
| Attribution preserved | DESIGN.md credits Open Design and refero_skill | `grep 'Apache 2.0' .omp/skills/design-system/DESIGN.md` and `grep 'refero_skill' .omp/skills/design-system/DESIGN.md` both return matches | Yes — license compliance |
| No skill regression | Existing 17 skill directories are untouched | `ls -d .omp/skills/*/ | wc -l` returns 18 (17 existing + 1 new design-system) | Yes — stated non-goal |
| Graph health | bv triage reports no new issues | `bv --robot-triage --format json` shows no new alerts or blocked beads | Soft — informational, not blocking |
| tech-stack.md structure | File ends after Constraints; no orphan sections | Visual inspection: `## Constraints` is the last section; no `## Design Assets` or `## Craft References` headers remain | Yes — structural integrity |
| Markdown validity | All files end with newline, no broken tables | `tail -c1` check for trailing newline; visual table inspection | Soft — cosmetic but good practice |

### Test Execution Order

1. **Pre-flight:** Record initial state (file counts, grep results)
2. **Wave 1 verification:** SKILL.md + DESIGN.md existence and structure
3. **Wave 2 verification:** tech-stack.md stale reference removal
4. **Wave 3 verification:** conventions.md empty header fix and annotation
5. **Wave 4 verification:** project.md milestone and success criterion update
6. **Full verification:** Run all checks end-to-end; record results in `completion-evidence.json`

### Test Environment

- Working directory: `/home/ryan/repos/omp-template`
- No external services required
- No test fixtures or mocks needed
- All tests are shell commands on the filesystem

## Migration Plan

### Pre-Migration State

```
.omp/skills/design-system/     → DOES NOT EXIST
.omp/design/                   → DOES NOT EXIST  
.omp/design/craft/             → DOES NOT EXIST
tech-stack.md                  → HAS 12 broken references (lines 65-89)
conventions.md                 → HAS 2 empty headers (lines 112, 118)
project.md                     → HAS stale milestone (line 23)
AGENTS.md                      → HAS correct design-system entry (line 188) — no change needed
```

### Migration Steps

| Step | Action | Rollback | Validation |
|------|--------|----------|------------|
| M1 | Create `.omp/skills/design-system/` directory | `rm -rf .omp/skills/design-system/` | `test -d .omp/skills/design-system/` |
| M2 | Write SKILL.md to new directory | `rm .omp/skills/design-system/SKILL.md` | `test -f` + section check |
| M3 | Write DESIGN.md to new directory | `rm .omp/skills/design-system/DESIGN.md` | `test -f` + 9-section check |
| M4 | Remove lines 65–89 from tech-stack.md | `git checkout -- .omp/memory/project/tech-stack.md` | `grep -r '\.omp/design/'` returns 0 |
| M5 | Fill CSS Ownership in conventions.md | `git checkout -- .omp/memory/project/conventions.md` | Content exists after header |
| M6 | Fill Craft Rules in conventions.md | Revert same file | Content exists after header |
| M7 | Add UI Design annotation in conventions.md | Revert same file | Annotation present |
| M8 | Update project.md milestone | `git checkout -- .omp/memory/project/project.md` | s2s reference present, 1da absent |
| M9 | Add success criterion to project.md | Revert same file | Criterion present |

### Migration Order Constraints

- M1 must precede M2 and M3 (need directory before files)
- M2 and M3 are independent of each other (can be parallel)
- M4 is independent of M1–M3 (different file)
- M5–M7 are on the same file (conventions.md) — must be sequential
- M8–M9 are on the same file (project.md) — must be sequential
- M4 and M5–M7 and M8–M9 are all on different files — can be parallel

### No Data Migration

No data is being migrated. No existing content is being transformed or moved. All changes are:
- **Create:** New files with no prior state
- **Delete:** Stale content removed from existing files
- **Add:** New content inserted into existing files

There are no user-visible features to transition, no database schemas to migrate, no API versions to deprecate. This is a documentation cleanup bead.

## Rollback Plan

### Rollback Trigger Conditions

Rollback is warranted if:
1. Any verification check in the "Full Verification" section fails and cannot be fixed within 2 attempts
2. A skill file is accidentally written with downstream project values (real hex codes, real font names)
3. tech-stack.md loses structural integrity (sections after removal don't flow correctly)
4. conventions.md develops new structural issues (broken headers, missing sections)
5. bv triage reports a regression (new blocked beads, new alerts)

### Rollback Procedure

```
# Full rollback to pre-bead state
git checkout -- .omp/memory/project/tech-stack.md
git checkout -- .omp/memory/project/conventions.md
git checkout -- .omp/memory/project/project.md
rm -rf .omp/skills/design-system/

# Verify rollback
test ! -d .omp/skills/design-system/ && echo "design-system dir removed"
test ! -f .omp/skills/design-system/SKILL.md && echo "SKILL.md removed"
test ! -f .omp/skills/design-system/DESIGN.md && echo "DESIGN.md removed"
grep '## Design Assets' .omp/memory/project/tech-stack.md && echo "tech-stack restored"
grep 'br-omp-backbone-skill-1da' .omp/memory/project/project.md && echo "project.md restored"
```

### Partial Rollback

| Failure | Rollback Scope | Command |
|---------|---------------|---------|
| SKILL.md has wrong content | Just SKILL.md | `rm .omp/skills/design-system/SKILL.md` then rewrite |
| DESIGN.md has wrong section count | Just DESIGN.md | `rm .omp/skills/design-system/DESIGN.md` then rewrite |
| tech-stack.md removal went wrong | Just tech-stack.md | `git checkout -- .omp/memory/project/tech-stack.md` then redo |
| conventions.md edits broke formatting | Just conventions.md | `git checkout -- .omp/memory/project/conventions.md` then redo |
| project.md milestone update failed | Just project.md | `git checkout -- .omp/memory/project/project.md` then redo |

### Rollback Safety

All changes are to memory files and skill files — no application code, no database, no external services. Rollback is a filesystem operation. No state is lost on rollback because the pre-change state is committed to git.

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | 1.1, 1.2 | Yes (different files) | design-system/ directory created | Both files exist; SKILL.md has required sections; DESIGN.md has 9 sections; all `[FILL]` placeholders present |
| 2 | 2.1 | No (single file edit) | Wave 1 complete | `grep -r '\.omp/design/' .omp/memory/project/tech-stack.md` returns zero matches; `## Design Assets` and `## Craft References` headers removed |
| 3 | 3.1, 3.2, 3.3 | No (same file — sequential edits) | Wave 1 complete | No empty headers in conventions.md; UI Design section annotated |
| 4 | 4.1, 4.2 | No (same file — sequential edits) | None (independent) | Milestone references s2s not 1da; success criterion #4 present |

**Parallelism note:** Waves 2, 3, and 4 touch different files (tech-stack.md, conventions.md, project.md) — they could run in parallel with three sub-agents. Wave 1 must precede Wave 3 (conventions.md references design-system path), but Wave 2 and Wave 4 are fully independent.

**Recommended execution order** for single-agent execution: Wave 1 → Wave 2 → Wave 3 → Wave 4. This respects the dependency (Wave 3 needs Wave 1's design-system path to exist) while keeping edits sequential and avoiding merge conflicts.

## Tasks

### Wave 1: Create design-system Skill

**Pre-flight:**
```bash
mkdir -p .omp/skills/design-system/
```

**Task 1.1: Write SKILL.md**

Create `.omp/skills/design-system/SKILL.md` following the established skill pattern (YAML frontmatter, Purpose, When to Use, When NOT to Use, Decision Tree, Process, Defaults, Attribution, Related Skills).

The decision tree is the critical intellectual content — it must correctly route agents through:
1. Template vs. downstream project detection
2. DESIGN.md existence check (bootstrap mode)
3. Per-category design decision routing (color, typography, spacing, animation, components, theme)
4. Fallback defaults for each unfilled category

Code outline:
```
---
name: design-system
description: Use when generating UI, choosing colors/fonts/spacing, implementing components, or reviewing visual output — provides brand contract format and fallback defaults.
---

# design-system

## Purpose

[States this is a brand contract template, not a completed design system.
 Explains SKILL.md = decision flow, DESIGN.md = brand values.]

## When to Use

[List of 5 trigger conditions from PRD + AGENTS.md:188]

## When NOT to Use

[List of 4 anti-pattern conditions]

## Decision Tree

[ASCII decision tree per PRD Section 7.2]

## Process

[5-step process: check DESIGN.md, read relevant section, apply filled/defaults, record decisions, verify WCAG AA]

## Defaults

[Fallback values for each DESIGN.md section when [FILL] is encountered]

## Attribution

[Open Design craft/ (Apache 2.0) + refero_skill (MIT) with link format matching template conventions]

## Related Skills

[Cross-references to other relevant skills]
```

**Verification:**
```bash
test -f .omp/skills/design-system/SKILL.md && echo "PASS: SKILL.md exists" || echo "FAIL"
grep -q '## When to use' .omp/skills/design-system/SKILL.md && echo "PASS: When to use" || echo "FAIL"
grep -q '## When NOT to use' .omp/skills/design-system/SKILL.md && echo "PASS: When NOT to use" || echo "FAIL"
grep -q '## Process' .omp/skills/design-system/SKILL.md && echo "PASS: Process" || echo "FAIL"
grep -q 'Apache 2.0' .omp/skills/design-system/SKILL.md && echo "PASS: attribution" || echo "FAIL"
```

**Task 1.2: Write DESIGN.md**

Create `.omp/skills/design-system/DESIGN.md` with exactly 9 numbered sections, each following the pattern:

```
## N. Section Name

> Brief explanation of what this section defines and why it matters for UI consistency.

| Token | Value | Description |
|-------|-------|-------------|
| `--[category]-[name]` | `[FILL]` <!-- e.g., `...` --> | What this token controls |
```

The 9 sections are: Brand Identity, Color Palette, Typography, Spacing & Layout, Component Tokens, Animation, Iconography, Imagery, Theme.

Every Value cell must contain `[FILL]` with an HTML comment example showing a realistic downstream value. The single exception is `--icon-color` = `currentColor` (this is a technical constant, not a brand choice).

Include attribution footer after section 9:
```
> **Attribution:** Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
```

**Verification:**
```bash
test -f .omp/skills/design-system/DESIGN.md && echo "PASS: DESIGN.md exists" || echo "FAIL"
SECTIONS=$(grep -c '^## [0-9]\.' .omp/skills/design-system/DESIGN.md)
test "$SECTIONS" -eq 9 && echo "PASS: 9 sections ($SECTIONS)" || echo "FAIL: $SECTIONS sections (expected 9)"
FILLS=$(grep -c '\[FILL\]' .omp/skills/design-system/DESIGN.md)
test "$FILLS" -ge 9 && echo "PASS: $FILLS FILL placeholders" || echo "FAIL: only $FILLS FILL placeholders"
grep -q 'Apache 2.0' .omp/skills/design-system/DESIGN.md && echo "PASS: attribution" || echo "FAIL"
grep -q 'refero_skill' .omp/skills/design-system/DESIGN.md && echo "PASS: refero_skill credit" || echo "FAIL"
```

### Wave 2: Clean tech-stack.md

**Task 2.1: Remove Design Assets and Craft References tables**

Remove lines 65–89 from `.omp/memory/project/tech-stack.md`:
- `## Design Assets` header and its 4-row table (lines 65–72)
- `## Craft References` header and its 8-row table (lines 74–88)
- Attribution line (line 89)

The file structure after removal:
```
## Constraints      (line 58)
...                 (lines 59-63 — unchanged)
                    (end of file)
```

The `## Security` section (lines 48–56) immediately precedes `## Constraints`. After removal, the file flows Security → Constraints → EOF with no design sections.

Code outline:
```
Read tech-stack.md
Delete all lines from "## Design Assets" through the attribution line
Verify no orphan content left
```

**Verification:**
```bash
grep -q '## Design Assets' .omp/memory/project/tech-stack.md && echo "FAIL: Design Assets still present" || echo "PASS: Design Assets removed"
grep -q '## Craft References' .omp/memory/project/tech-stack.md && echo "FAIL: Craft References still present" || echo "PASS: Craft References removed"
grep -r '\.omp/design/' .omp/memory/project/tech-stack.md && echo "FAIL: stale refs remain" || echo "PASS: no stale refs"
```

### Wave 3: Fix conventions.md

**Task 3.1: Fill CSS Ownership header**

Insert content after `### CSS Ownership` (line 112), before `### Component Variants` (line 113):

The content is the boundary statement from PRD Section 7.5 — clarifying that CSS is a downstream concern, the template doesn't own CSS rules, and the UI Design section is template content for downstream use.

**Verification:**
```bash
# Check that content exists between CSS Ownership and Component Variants headers
grep -A5 '### CSS Ownership' .omp/memory/project/conventions.md | grep -q 'downstream project concern' && echo "PASS" || echo "FAIL"
```

**Task 3.2: Fill Craft Rules header**

Insert content after `### Craft Rules` (line 118), before `### Theme` (line 119):

The content is the reference statement from PRD Section 7.5 — crediting Open Design, listing craft rule categories, clarifying the template doesn't enforce them, and pointing to DESIGN.md.

**Verification:**
```bash
grep -A5 '### Craft Rules' .omp/memory/project/conventions.md | grep -q 'Open Design' && echo "PASS" || echo "FAIL"
```

**Task 3.3: Add UI Design section annotation**

Insert immediately after `## UI Design` (line 97), before the existing `### Design System` (line 99):

```
> **Note:** This section is template content for downstream projects...
```

**Verification:**
```bash
grep -q 'template content for downstream projects' .omp/memory/project/conventions.md && echo "PASS" || echo "FAIL"
```

### Wave 4: Update project.md

**Task 4.1: Update Current Phase milestone**

Replace the stale milestone reference. Content matching — find "br-omp-backbone-skill-1da" and replace with "br-omp-backbone-skill-s2s". Also update the milestone description text and the Next field.

**Verification:**
```bash
grep -q 'br-omp-backbone-skill-1da' .omp/memory/project/project.md && echo "FAIL: stale ref" || echo "PASS: stale ref removed"
grep -q 'br-omp-backbone-skill-s2s' .omp/memory/project/project.md && echo "PASS: current milestone" || echo "FAIL: missing"
```

**Task 4.2: Add success criterion for broken references**

Add entry 4 to the Success Criteria list (after entry 3, before the "Keep to 3-5 criteria" line).

**Verification:**
```bash
grep -q 'Zero broken file references' .omp/memory/project/project.md && echo "PASS: criterion added" || echo "FAIL"
```

## Full Verification

```bash
echo "=== V1: File Existence ==="
test -f .omp/skills/design-system/SKILL.md && echo "PASS: SKILL.md" || echo "FAIL: SKILL.md missing"
test -f .omp/skills/design-system/DESIGN.md && echo "PASS: DESIGN.md" || echo "FAIL: DESIGN.md missing"

echo ""
echo "=== V2: SKILL.md Structure ==="
grep -q '## When to use' .omp/skills/design-system/SKILL.md && echo "PASS: When to use" || echo "FAIL: When to use"
grep -q '## When NOT to use' .omp/skills/design-system/SKILL.md && echo "PASS: When NOT to use" || echo "FAIL: When NOT to use"
grep -q '## Process' .omp/skills/design-system/SKILL.md && echo "PASS: Process" || echo "FAIL: Process"
grep -q 'Apache 2.0' .omp/skills/design-system/SKILL.md && echo "PASS: SKILL.md attribution" || echo "FAIL: SKILL.md attribution"

echo ""
echo "=== V3: DESIGN.md Structure ==="
SECTIONS=$(grep -c '^## [0-9]\.' .omp/skills/design-system/DESIGN.md)
test "$SECTIONS" -eq 9 && echo "PASS: 9 sections ($SECTIONS)" || echo "FAIL: $SECTIONS sections"
FILLS=$(grep -c '\[FILL\]' .omp/skills/design-system/DESIGN.md)
test "$FILLS" -ge 9 && echo "PASS: $FILLS [FILL] placeholders" || echo "FAIL: $FILLS [FILL]"
grep -q 'Apache 2.0' .omp/skills/design-system/DESIGN.md && echo "PASS: DESIGN.md attribution" || echo "FAIL: DESIGN.md attribution"
grep -q 'refero_skill' .omp/skills/design-system/DESIGN.md && echo "PASS: refero_skill credit" || echo "FAIL: refero_skill credit"

echo ""
echo "=== V4: Stale References ==="
grep -r '\.omp/design/' .omp/memory/project/ 2>/dev/null && echo "FAIL: stale .omp/design/ refs" || echo "PASS: no stale refs"

echo ""
echo "=== V5: tech-stack.md Clean ==="
grep -q '## Design Assets' .omp/memory/project/tech-stack.md && echo "FAIL: Design Assets still present" || echo "PASS: Design Assets removed"
grep -q '## Craft References' .omp/memory/project/tech-stack.md && echo "FAIL: Craft References still present" || echo "PASS: Craft References removed"

echo ""
echo "=== V6: conventions.md Empty Headers ==="
grep -A1 '### CSS Ownership' .omp/memory/project/conventions.md | tail -1 | grep -qv '^###' && echo "PASS: CSS Ownership has content" || echo "FAIL: CSS Ownership empty"
grep -A1 '### Craft Rules' .omp/memory/project/conventions.md | tail -1 | grep -qv '^###' && echo "PASS: Craft Rules has content" || echo "FAIL: Craft Rules empty"
grep -q 'template content for downstream projects' .omp/memory/project/conventions.md && echo "PASS: UI Design annotated" || echo "FAIL: UI Design not annotated"

echo ""
echo "=== V7: project.md Current ==="
grep -q 'br-omp-backbone-skill-1da' .omp/memory/project/project.md && echo "FAIL: stale 1da ref" || echo "PASS: no stale 1da"
grep -q 'br-omp-backbone-skill-s2s' .omp/memory/project/project.md && echo "PASS: s2s milestone" || echo "FAIL: s2s missing"
grep -q 'Zero broken file references' .omp/memory/project/project.md && echo "PASS: criterion added" || echo "FAIL: criterion missing"

echo ""
echo "=== V8: Graph Health ==="
bv --robot-triage --format json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('PASS: triage OK' if d.get('triage') else 'FAIL: triage failed')" 2>/dev/null || echo "WARN: bv triage check skipped"
br list --status open --status in_progress --json 2>/dev/null | python3 -c "import json,sys; beads=json.load(sys.stdin); print(f'Open beads: {len(beads)}')" 2>/dev/null || echo "WARN: br list skipped"

echo ""
echo "=== V9: Skill Directory Count ==="
SKILL_COUNT=$(ls -d .omp/skills/*/ 2>/dev/null | wc -l)
test "$SKILL_COUNT" -eq 18 && echo "PASS: 18 skill dirs" || echo "INFO: $SKILL_COUNT skill dirs (expected 18)"

echo ""
echo "=== V10: Markdown Integrity ==="
for f in .omp/memory/project/*.md .omp/skills/design-system/*.md; do
  test -f "$f" || continue
  test "$(tail -c1 "$f" | wc -l)" -gt 0 && echo "WARN: $f missing trailing newline" || echo "OK: $f"
done
```

## Risks and Mitigations

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|------------|--------|------------|
| R1 | DESIGN.md [FILL] placeholders accidentally contain real brand values from the review process | Low | Low | All values are explicitly `[FILL]` with HTML comment examples. Review gate catches filled values. |
| R2 | Removing 25 lines from tech-stack.md makes it feel too short | Low | Low | File retains Runtime, Dependencies, Verification Commands, Security, Constraints — all substantive sections. Post-removal ~65 lines, well above the "too thin" threshold. |
| R3 | conventions.md line numbers shift during sequential edits, causing wrong insertion points | Medium | Medium | All edits use content-based insertion (find header text, insert after), not absolute line numbers. The edit tool's `INS.POST N:` uses the line number from the latest read snapshot. |
| R4 | Another bead modifies the same files concurrently | Low | Low | This bead is the only in_progress item. br single-claim model prevents concurrent mutation. |
| R5 | DESIGN.md 9-section format is too prescriptive for some downstream projects | Low | Low | Every value is `[FILL]` — downstream projects can freely restructure. The 9 sections are an organizational guide, not an enforcement mechanism. |
| R6 | Attribution removal from tech-stack.md appears to lose license compliance | Low | Medium | Attribution is explicitly preserved in both SKILL.md and DESIGN.md. The content being removed (table entries with file paths) doesn't carry license weight — the attribution line does, and it's moved, not deleted. |

## Timeline

| Phase | Duration | Dependencies | Output |
|-------|----------|-------------|--------|
| Wave 1: Create design-system skill | 8 min | None | SKILL.md + DESIGN.md on disk |
| Wave 2: Clean tech-stack.md | 3 min | Wave 1 (soft — design-system path must exist before conventions.md refs it, but tech-stack.md itself doesn't depend) | tech-stack.md with design sections removed |
| Wave 3: Fix conventions.md | 5 min | Wave 1 (hard — conventions.md references design-system path) | conventions.md with filled headers and annotation |
| Wave 4: Update project.md | 3 min | None (independent) | project.md with current milestone and new criterion |
| Full Verification | 4 min | Waves 1-4 complete | completion-evidence.json with all passes |
| Commit + push | 2 min | Verification passes | Commit on feature branch |
| **Total** | **25 min** | | Bead ready for /verify → /review → /pr |

**Parallel opportunity:** Waves 2 and 4 can run in parallel since they touch different files (tech-stack.md vs project.md). Wave 3 can also run in parallel with Wave 2 and Wave 4 once Wave 1 completes. In a 3-agent parallel setup, total time drops to ~12 minutes.

## Acceptance Criteria Mapping

| # | Criterion | Verified By | Wave |
|---|-----------|-------------|------|
| AC1 | SKILL.md exists with When to Use, When NOT to Use, Process | V2 | 1 |
| AC2 | DESIGN.md exists with 9 sections, all `[FILL]` | V3 | 1 |
| AC3 | tech-stack.md has zero `.omp/design/` refs | V4, V5 | 2 |
| AC4 | conventions.md has zero empty headers | V6 | 3 |
| AC5 | conventions.md UI Design section annotated | V6 | 3 |
| AC6 | project.md references s2s, not 1da | V7 | 4 |
| AC7 | project.md includes broken-refs success criterion | V7 | 4 |
| AC8 | bv triage reports no new issues | V8 | Full |
| AC9 | Attribution preserved in design-system skill | V2, V3 | 1 |
| AC10 | No existing skill/command files modified | V9 | Full |

## Out of Scope (Reaffirmed)

- **NOT** creating `.omp/design/` or any files within it
- **NOT** creating `.omp/design/craft/` or any craft reference files
- **NOT** implementing any CSS, design tokens, or visual assets
- **NOT** modifying any skill files other than the new design-system skill
- **NOT** modifying AGENTS.md (it already correctly lists design-system)
- **NOT** modifying any of the 13 closed bead artifacts
- **NOT** adding new commands or extensions
- **NOT** changing the workflow gate or enforcement mechanisms
- **NOT** touching the `design/` directory at repo root (downstream artifacts)
- **NOT** changing conventions beyond the identified empty headers and annotation
- **NOT** relocating the UI Design section from conventions.md to the design-system skill