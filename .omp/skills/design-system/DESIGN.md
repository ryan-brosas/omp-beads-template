# Brand Contract Template

> This file is a **template**. Every value is `[FILL]` — replace these with your project's actual brand choices. HTML comments show realistic examples of what a filled value looks like. The 9 sections together form a complete visual language spec. Fill them once and every agent that loads the design-system skill will produce consistent, brand-aligned UI.

---

## 1. Brand Identity

> The foundational layer: what is the product called, what does it promise, and what tone does it use? Everything else (colors, fonts, spacing, animation) derives from this.

| Token | Value | Description |
|-------|-------|-------------|
| `--brand-name` | `[FILL]` <!-- e.g., `Acme` --> | Product or company name |
| `--brand-tagline` | `[FILL]` <!-- e.g., `Build faster, ship smarter` --> | One-line promise or positioning statement |
| `--brand-voice` | `[FILL]` <!-- e.g., `Professional, clear, approachable` --> | Tone-of-voice keywords (3-5) |

---

## 2. Color Palette

> Colors carry emotional weight. Choose a primary that reflects the brand identity, a secondary that complements without competing, and semantic colors (success, warning, error) that are universally understood. Every color must meet WCAG 2.2 AA contrast against its intended background.

| Token | Value | Description |
|-------|-------|-------------|
| `--color-primary` | `[FILL]` <!-- e.g., `#3B82F6` --> | Primary brand color (buttons, links, focus rings) |
| `--color-primary-hover` | `[FILL]` <!-- e.g., `#2563EB` --> | Primary hover/active state |
| `--color-primary-soft` | `[FILL]` <!-- e.g., `#EFF6FF` --> | Primary tint for backgrounds, badges |
| `--color-secondary` | `[FILL]` <!-- e.g., `#8B5CF6` --> | Secondary accent (highlights, secondary CTAs) |
| `--color-secondary-soft` | `[FILL]` <!-- e.g., `#F5F3FF` --> | Secondary tint |
| `--color-neutral-50` | `[FILL]` <!-- e.g., `#FAFAFA` --> | Lightest neutral (page background) |
| `--color-neutral-100` | `[FILL]` <!-- e.g., `#F5F5F5` --> | Light neutral (card backgrounds) |
| `--color-neutral-200` | `[FILL]` <!-- e.g., `#E5E5E5` --> | Border light |
| `--color-neutral-300` | `[FILL]` <!-- e.g., `#D4D4D4` --> | Border default |
| `--color-neutral-400` | `[FILL]` <!-- e.g., `#A3A3A3` --> | Disabled text / placeholder |
| `--color-neutral-500` | `[FILL]` <!-- e.g., `#737373` --> | Secondary text |
| `--color-neutral-600` | `[FILL]` <!-- e.g., `#525252` --> | Body text on light backgrounds |
| `--color-neutral-700` | `[FILL]` <!-- e.g., `#404040` --> | Heading text |
| `--color-neutral-800` | `[FILL]` <!-- e.g., `#262626` --> | High-emphasis text |
| `--color-neutral-900` | `[FILL]` <!-- e.g., `#171717` --> | Highest emphasis |
| `--color-success` | `[FILL]` <!-- e.g., `#22C55E` --> | Success states (confirmations, toasts) |
| `--color-success-soft` | `[FILL]` <!-- e.g., `#F0FDF4` --> | Success tint |
| `--color-warning` | `[FILL]` <!-- e.g., `#F59E0B` --> | Warning states |
| `--color-warning-soft` | `[FILL]` <!-- e.g., `#FFFBEB` --> | Warning tint |
| `--color-error` | `[FILL]` <!-- e.g., `#EF4444` --> | Error/destructive states |
| `--color-error-soft` | `[FILL]` <!-- e.g., `#FEF2F2` --> | Error tint |
| `--color-info` | `[FILL]` <!-- e.g., `#06B6D4` --> | Informational states |
| `--color-info-soft` | `[FILL]` <!-- e.g., `#ECFEFF` --> | Info tint |

---

## 3. Typography

> Fonts define the voice of the interface. Choose a heading font that commands attention, a body font optimized for readability at 14-16px, and a monospace font for code and data. Pair fonts that share similar x-heights to avoid visual jarring.

| Token | Value | Description |
|-------|-------|-------------|
| `--font-heading` | `[FILL]` <!-- e.g., `"Inter", system-ui, sans-serif` --> | Font stack for h1–h6 |
| `--font-body` | `[FILL]` <!-- e.g., `"Inter", system-ui, sans-serif` --> | Font stack for body text, paragraphs, labels |
| `--font-mono` | `[FILL]` <!-- e.g., `"JetBrains Mono", ui-monospace, monospace` --> | Font stack for code, pre, data tables |
| `--text-xs` | `[FILL]` <!-- e.g., `0.75rem` (12px) --> | Extra small (captions, badges) |
| `--text-sm` | `[FILL]` <!-- e.g., `0.875rem` (14px) --> | Small (secondary text, labels) |
| `--text-base` | `[FILL]` <!-- e.g., `1rem` (16px) --> | Base (body text, inputs) |
| `--text-lg` | `[FILL]` <!-- e.g., `1.125rem` (18px) --> | Large (lead paragraphs) |
| `--text-xl` | `[FILL]` <!-- e.g., `1.25rem` (20px) --> | Extra large (h4) |
| `--text-2xl` | `[FILL]` <!-- e.g., `1.5rem` (24px) --> | 2x large (h3) |
| `--text-3xl` | `[FILL]` <!-- e.g., `1.875rem` (30px) --> | 3x large (h2) |
| `--text-4xl` | `[FILL]` <!-- e.g., `2.25rem` (36px) --> | 4x large (h1) |
| `--font-weight-normal` | `[FILL]` <!-- e.g., `400` --> | Body text weight |
| `--font-weight-medium` | `[FILL]` <!-- e.g., `500` --> | Medium emphasis (labels, buttons) |
| `--font-weight-semibold` | `[FILL]` <!-- e.g., `600` --> | Semibold (subheadings) |
| `--font-weight-bold` | `[FILL]` <!-- e.g., `700` --> | Bold (headings) |
| `--line-height-tight` | `[FILL]` <!-- e.g., `1.25` --> | Headings |
| `--line-height-normal` | `[FILL]` <!-- e.g., `1.5` --> | Body text |
| `--line-height-relaxed` | `[FILL]` <!-- e.g., `1.75` --> | Long-form reading |
| `--letter-spacing-tight` | `[FILL]` <!-- e.g., `-0.02em` --> | Large headings |
| `--letter-spacing-normal` | `[FILL]` <!-- e.g., `0` --> | Body text |
| `--letter-spacing-wide` | `[FILL]` <!-- e.g., `0.05em` --> | Uppercase labels, badges |

---

## 4. Spacing & Layout

> Consistent spacing creates visual rhythm. Use a 4px base scale — every spacing value should be a multiple of 4. This constraint eliminates arbitrary "close enough" values and makes the UI feel intentional.

| Token | Value | Description |
|-------|-------|-------------|
| `--space-1` | `[FILL]` <!-- e.g., `0.25rem` (4px) --> | Tightest spacing (icon-to-label gap) |
| `--space-2` | `[FILL]` <!-- e.g., `0.5rem` (8px) --> | Extra tight (inline gaps) |
| `--space-3` | `[FILL]` <!-- e.g., `0.75rem` (12px) --> | Tight (related elements) |
| `--space-4` | `[FILL]` <!-- e.g., `1rem` (16px) --> | Default (card padding, section gaps) |
| `--space-6` | `[FILL]` <!-- e.g., `1.5rem` (24px) --> | Medium (section spacing) |
| `--space-8` | `[FILL]` <!-- e.g., `2rem` (32px) --> | Large (major section breaks) |
| `--space-12` | `[FILL]` <!-- e.g., `3rem` (48px) --> | Extra large (page-level padding) |
| `--space-16` | `[FILL]` <!-- e.g., `4rem` (64px) --> | 2x large (hero spacing) |
| `--space-24` | `[FILL]` <!-- e.g., `6rem` (96px) --> | Maximum (full-page sections) |
| `--content-max-width` | `[FILL]` <!-- e.g., `72rem` (1152px) --> | Maximum content width for readability |
| `--content-narrow` | `[FILL]` <!-- e.g., `40rem` (640px) --> | Narrow content (forms, focused reading) |

---

## 5. Component Tokens

> These tokens define the "3D feel" of the interface — how elements sit on the page, how they respond to interaction, and how their state is communicated. Consistent application of these tokens is what separates polished UI from generic UI.

| Token | Value | Description |
|-------|-------|-------------|
| `--radius-sm` | `[FILL]` <!-- e.g., `4px` --> | Small radius (checkboxes, tags, badges) |
| `--radius-md` | `[FILL]` <!-- e.g., `6px` --> | Default radius (buttons, inputs, cards) |
| `--radius-lg` | `[FILL]` <!-- e.g., `8px` --> | Large radius (modals, panels) |
| `--radius-xl` | `[FILL]` <!-- e.g., `12px` --> | Extra large (large cards, drawers) |
| `--radius-full` | `[FILL]` <!-- e.g., `9999px` --> | Pill/fully rounded (chips, badges) |
| `--shadow-sm` | `[FILL]` <!-- e.g., `0 1px 3px rgba(0,0,0,0.06)` --> | Subtle elevation (cards on white) |
| `--shadow-md` | `[FILL]` <!-- e.g., `0 4px 12px rgba(0,0,0,0.08)` --> | Default elevation (dropdowns, tooltips) |
| `--shadow-lg` | `[FILL]` <!-- e.g., `0 8px 24px rgba(0,0,0,0.12)` --> | High elevation (modals, drawers) |
| `--shadow-xl` | `[FILL]` <!-- e.g., `0 16px 48px rgba(0,0,0,0.16)` --> | Maximum elevation |
| `--border-width` | `[FILL]` <!-- e.g., `1.5px` --> | Default border width |
| `--border-width-strong` | `[FILL]` <!-- e.g., `2px` --> | Strong border (focus rings, active states) |
| `--opacity-disabled` | `[FILL]` <!-- e.g., `0.5` --> | Disabled element opacity |
| `--opacity-hover` | `[FILL]` <!-- e.g., `0.8` --> | Hover overlay opacity |

---

## 6. Animation

> Motion communicates state change, hierarchy, and causality. Use it sparingly — every animation must have a purpose (entrance, exit, feedback, or attention). Prefer short durations that feel responsive, not sluggish.

| Token | Value | Description |
|-------|-------|-------------|
| `--dur-instant` | `[FILL]` <!-- e.g., `80ms` --> | Instant feedback (hover on/off, checkbox toggle) |
| `--dur-quick` | `[FILL]` <!-- e.g., `120ms` --> | Quick micro-feedback (button press, focus ring) |
| `--dur-normal` | `[FILL]` <!-- e.g., `200ms` --> | Default enter transition (elements appearing) |
| `--dur-exit` | `[FILL]` <!-- e.g., `140ms` --> | Default exit transition (elements dismissing) |
| `--dur-slow` | `[FILL]` <!-- e.g., `300ms` --> | Deliberate transition (page changes, panel slides) |
| `--easing-canonical` | `[FILL]` <!-- e.g., `cubic-bezier(0.23, 1, 0.32, 1)` --> | The one easing curve for all UI transitions |
| `--reduced-motion` | `[FILL]` <!-- e.g., `prefers-reduced-motion: reduce` --> | Policy: respect OS preference; set durations to 0ms |

---

## 7. Iconography

> Icons are visual shorthand. A consistent icon library, consistent sizing, and consistent color inheritance (`currentColor`) make the UI feel cohesive. Never mix icon sets — pick one and commit.

| Token | Value | Description |
|-------|-------|-------------|
| `--icon-library` | `[FILL]` <!-- e.g., `lucide-react` (MIT) --> | Icon library name and package |
| `--icon-size-inline` | `[FILL]` <!-- e.g., `1em` (inherits from parent text) --> | Size when inline with text |
| `--icon-size-sm` | `[FILL]` <!-- e.g., `16px` --> | Small standalone icons |
| `--icon-size-md` | `[FILL]` <!-- e.g., `20px` --> | Default standalone icons (toolbars, nav) |
| `--icon-size-lg` | `[FILL]` <!-- e.g., `24px` --> | Large icons (hero sections, empty states) |
| `--icon-stroke-width` | `[FILL]` <!-- e.g., `1.75px` --> | Stroke width for outline icons |
| `--icon-color` | `currentColor` | Icon color (inherits from parent text color) |

---

## 8. Imagery

> Photography and illustration style define the emotional character of the product. Consistent treatment — aspect ratios, border radii, overlays — makes imagery feel curated rather than slapped on.

| Token | Value | Description |
|-------|-------|-------------|
| `--image-aspect-portrait` | `[FILL]` <!-- e.g., `3 / 4` --> | Portrait aspect ratio (avatars, team photos) |
| `--image-aspect-landscape` | `[FILL]` <!-- e.g., `16 / 9` --> | Landscape aspect ratio (hero images, blog) |
| `--image-aspect-square` | `[FILL]` <!-- e.g., `1 / 1` --> | Square aspect ratio (thumbnails, logos) |
| `--image-radius` | `[FILL]` <!-- e.g., `var(--radius-md)` --> | Default image border radius |
| `--image-fit` | `[FILL]` <!-- e.g., `cover` --> | Default object-fit for images |
| `--image-treatment` | `[FILL]` <!-- e.g., `No filter` or `saturate(0.9) contrast(1.05)` --> | CSS filter for consistent photo look |

---

## 9. Theme

> A theme strategy defines how the UI shifts between light and dark. Every color token defined in Section 2 should have a dark-mode counterpart. The mode should respect system preference by default, with an explicit override for user choice.

| Token | Value | Description |
|-------|-------|-------------|
| `--theme-default` | `[FILL]` <!-- e.g., `light` --> | Default theme (light or system) |
| `--theme-dark-trigger` | `[FILL]` <!-- e.g., `prefers-color-scheme: dark` OR `[data-theme="dark"]` --> | How dark mode is activated |
| `--theme-transition` | `[FILL]` <!-- e.g., `background-color 300ms, color 200ms` --> | Theme switch transition properties |
| `--theme-toggle` | `[FILL]` <!-- e.g., `Manual toggle button + system auto-detect` --> | User-facing mode switching mechanism |

---

> **Attribution:** Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
