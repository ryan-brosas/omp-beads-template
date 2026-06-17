---
name: design-system
description: Use when generating UI, choosing colors/fonts/spacing, implementing components, or reviewing visual output — provides brand contract format and fallback defaults.
---

# design-system

## Purpose

This skill provides a **brand contract template**, not a completed design system. In an omp-template project, `SKILL.md` defines the decision flow — when the agent encounters a design question, it routes through the decision tree below. `DESIGN.md` holds the project's actual brand values (colors, typography, spacing, etc.) in a 9-section format.

The template ships with `[FILL]` placeholders in every DESIGN.md value slot. Downstream projects replace these with their actual brand choices. Until then, this skill provides sensible, accessible defaults so the agent can still produce usable UI.

## When to Use

- Generating UI components or pages
- Choosing colors, fonts, or spacing values
- Implementing component variants (buttons, inputs, cards, etc.)
- Reviewing visual output for brand consistency
- Setting up a new project's design tokens
- Any decision that affects the visual appearance of the application

## When NOT to Use

- Backend-only changes (APIs, database, authentication, infrastructure)
- Documentation or configuration edits
- CLI or terminal tool work
- Graph operations, task tracking, or workflow management
- A full, production-grade design system already exists in the project (e.g., a comprehensive `tokens.json`, Figma integration, etc.)
- The project is a library, SDK, or CLI tool with no UI surface

## Decision Tree

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

## Process

1. **Check DESIGN.md existence and fill state**: Read `.omp/skills/design-system/DESIGN.md`. Determine if it exists and whether values are `[FILL]` placeholders or actual brand values.
2. **Read the relevant section**: For the current design decision, locate the corresponding numbered section in DESIGN.md. If the section is filled with real values, use them verbatim.
3. **Apply filled values or defaults**: If the relevant section contains `[FILL]`, either ask the downstream project for their preference OR apply the safe default from the Defaults section below. Always prefer asking for color and typography; defaults are acceptable for spacing, animation, and component tokens.
4. **Record new design decisions**: When the downstream project provides a design value, write it into DESIGN.md (replacing the `[FILL]` placeholder). This ensures future agents benefit from the decision.
5. **Verify output against WCAG 2.2 AA**: Every generated UI must meet at minimum: 4.5:1 contrast ratio for normal text, 3:1 for large text, visible focus indicators, and keyboard accessibility. Warnings on deviations.

## Defaults (Fallback When DESIGN.md is Unfilled)

| DESIGN.md Section | Default Value | Notes |
|---|---|---|
| **1. Brand Identity** | `[PROJECT_NAME]` / "Professional, clear, approachable" | Ask the project — brand identity is foundational |
| **2. Color Palette** | System color scheme (`CanvasText`, `Canvas`, `LinkText`, `Highlight`, etc.) | Use CSS system colors as safe, accessible defaults |
| **3. Typography** | System font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif` | Mono: `ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace` |
| **4. Spacing & Layout** | 4px base: 4, 8, 12, 16, 24, 32, 48, 64, 96 | Max content width: 72rem (1152px) |
| **5. Component Tokens** | border-radius: 6px; shadow: `0 2px 8px rgba(0,0,0,0.08)`; border: 1.5px; opacity-disabled: 0.5 | Use geometric progression for radii: 4, 6, 8, 12, 16, 24, 9999 |
| **6. Animation** | enter: 200ms, exit: 140ms, easing: `cubic-bezier(0.23, 1, 0.32, 1)` | Hover/feedback: 120ms (`--dur-quick`). Respect `prefers-reduced-motion` |
| **7. Iconography** | Lucide icons (MIT) or Heroicons (MIT); 1.6–1.8px stroke | 16px inline, 20px standalone, 24px large. `currentColor` for all. |
| **8. Imagery** | Neutral, professional photography; 16:9 and 1:1 aspect ratios | Use `object-fit: cover` with consistent treatment |
| **9. Theme** | Light default, dark via `prefers-color-scheme: dark` | `[data-theme="dark"]` for manual toggle. Every token has a dark counterpart. |

## Attribution

Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).

## Related Skills

- **backbone** — project bootstrapping and template initialization; load after design-system for new projects
- **br** — task tracking; use when creating beads for design work
- **verification-before-completion** — always verify visual output against WCAG AA before declaring done
