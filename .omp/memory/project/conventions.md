---
purpose: How we build — naming, code style, workflow, agent conventions, memory system
updated: 2026-06-17
---

# Conventions: OMP Beads Template

## Naming

- **Files:** `kebab-case.md`, `kebab-case.json`, `kebab-case.ts`
- **Functions:** `camelCase` (TypeScript), `snake_case` (Python), `camelCase` (Go)
- **Classes/Components:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Bead slugs:** `kebab-case` (e.g. `feat-auth-login`, `fix-null-check`)
- **Bead prefix:** `br-omp`

## Languages by Purpose

| Purpose | Language | Notes |
|---------|----------|-------|
| Agent instructions | Markdown | Skills, commands, memory files |
| Configuration | JSON / YAML | settings, manifests |
| Backend | N/A | Template repo — no backend runtime |
| Frontend | N/A | Template repo — provides design system assets only |
| Scripts | Python | `/init` hydration script |

Fill in the actual languages for your project. Agents use this to pick the right tool for the job.

## Skill Structure

Every skill SKILL.md follows this pattern:
- **When to use** — trigger conditions the agent matches against
- **When NOT to use** — anti-patterns to avoid
- **Process** — step-by-step instructions, not prose

## Command Structure

- **Executable commands** (`/pr`): `allowed-tools` frontmatter, `!` backtick injection, single-turn execution
- **Descriptive commands** (`/plan`, `/ship`): multi-phase recipe with exact CLI commands, STOP conditions
- Every bead-ID-taking command starts with the same Bead ID Resolution block

## Git

- **Branch:** `<type>/<bead-id>-<slug>` (e.g. `feat/a1b2-add-login`)
- **Commit:** conventional commits — `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`
- **PR title:** `<bead-id>: <one-line summary>`
## Workflow

1. **Brainstorm** — `/brainstorm` explores codebase, identifies work
2. **Create** — `/create` produces PRD + decisions.md
3. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md
4. **Ship** — `/ship` implements per plan, no scope creep
5. **Verify** — `/verify` runs checks, records evidence
6. **Review** — `/review` runs 5 parallel agents, confidence filter ≥80
7. **PR** — `/pr` opens PR, single-turn execution
8. **Close** — `/close` after merge, suggests next bead

## Agent Conventions

- Evidence before claims — no assertion without observed output
- Read before edit — never guess file content
- Ask before destructive — confirm before deleting user code
- One bead per session — stay focused, don't multitask
- Never implement without a bead and plan — workflow gate enforces this structurally
- Scope changes to the active bead — don't "clean up while you're in here"
- Always `--json` with br/bv commands — parseable output, no screen scraping
- Resolve actor: `ACTOR="${BR_ACTOR:-assistant}"` on all br mutations


## Honcho Memory

- Use Honcho as persistent memory/reasoning, not as scratch state.
- Query Honcho only when prior user or project context can change the answer.
- `honcho_search` finds prior durable context; `honcho_chat` synthesizes preferences or decisions; `honcho_remember` stores one verified durable fact.
- Keep repository files, bead artifacts, and observed tool output authoritative.
- Never store secrets, credentials, command output, temporary todos, or speculation in Honcho.
- Use the smallest sufficient reasoning level: `minimal` for factual lookup, `low` by default, `medium`/`high` for multi-session synthesis, `max` rarely.

## Memory File Maintenance

Memory files are the project's durable context — equivalent to CLAUDE.md. They MUST stay current.

| File | What goes there | When to update |
|------|----------------|----------------|
| `project.md` | Vision, goals, current phase | After milestones, scope changes |
| `conventions.md` | Naming, workflow, agent rules | When conventions change |
| `decisions.md` | Architecture decisions | When a new decision is made |
| `gotchas.md` | Pitfalls, warnings, workarounds | When a gotcha is discovered |
| `tech-stack.md` | Versions, verification commands, constraints | When dependencies change |

**Update workflow:**
1. After a session that reveals missing context: write the target file, show the diff, get approval, apply.
2. Every `/close`: agent checks if any conventions/decisions/gotchas were discovered during the bead and proposes updates.
3. Audit periodically: are conventions current? Architecture clear? Gotchas captured?
4. Never let memory drift — stale memory is worse than no memory because it teaches wrong patterns.

## UI Design

### Design System

- **Brand contract:** `.omp/skills/design-system/DESIGN.md` — the 9-section source of truth for visual language.

### Animation Philosophy

- **Easing:** `cubic-bezier(0.23, 1, 0.32, 1)` is the single canonical curve for all UI transitions. Built-in `ease` is too weak; `ease-in` is forbidden for UI elements (feels sluggish).
- **Asymmetric durations:** enter ~200ms, exit ~140ms. Exit reads as decisive because the user has already chosen to dismiss.
- **Accordion expand/collapse:** `grid-template-rows: 0fr → 1fr` (modern auto-height pattern). Pair with opacity fade and the canonical easing. Reuse `.accordion-collapsible` + `.accordion-collapsible-inner`.
- **Scale floor:** Never animate from `transform: scale(0)`. Start from `scale(0.9)` or higher with `opacity: 0`.
- **Mount strategy:** Keep conditionally-visible elements mounted; toggle a CSS class. React unmounts skip the exit transition entirely.
- **Micro-feedback:** 120ms for hover/focus transitions (the `--dur-quick` token).

### CSS Ownership
### Component Variants

- **Buttons:** 5 variants — `default`, `primary`, `primary-ghost`, `ghost`, `subtle`. No new variants without a documented need.
- **Focus rings:** Use `--selected` (blue) + `--selected-soft` ring on inputs/selects. Use `--accent` (terracotta) for button focus-visible outlines. This separation lets a focused input and a primary CTA coexist without competing.

### Craft Rules
### Theme

- **Light default.** Dark via `[data-theme="dark"]` on `<html>`. System mode via `@media (prefers-color-scheme: dark)` when no explicit theme attribute.
- **Every token has a dark counterpart.** Never approximate dark values — each is chosen for perceptual equivalence.

### Icons

- **Icon set:** Use a single consistent icon library. Prefer 1.6–1.8px-stroke monoline SVG with `currentColor` so icons inherit text color.
- **Icon-only buttons:** Always include an `aria-label`. Pair with `.sr-only` text when the icon's meaning isn't universally obvious.
- **Never use emoji as UI icons.** Emoji render differently across platforms, lack `currentColor` inheritance, and read as unpolished. Reserve emoji for user-generated content only.
- **Icon sizing:** 16px for inline with body text, 20px for standalone UI (toolbar buttons, nav items), 24px for large controls.
- **Decorative icons:** `aria-hidden="true" focusable="false"` on SVGs that repeat adjacent text labels.
