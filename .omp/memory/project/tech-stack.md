---
purpose: Tech stack, versions, verification commands, and constraints
updated: 2026-06-17
---

# Tech Stack: OMP Beads Template

## Runtime

| Layer | Tool | Version | Notes |
|-------|------|---------|-------|
| Language | N/A | — | Template repo — no application language |
| Runtime | N/A | — | Template repo — no application runtime |
| Package manager | N/A | — | Template repo — no dependencies |
| Task tracking | br (beads_rust) | latest | `which br` — CLI task tracker |
| Graph intelligence | bv (beads_viewer) | latest | `which bv` — robot commands for graph analysis |

## Key Dependencies

| Dependency | Purpose | Version |
|------------|---------|---------|
| N/A | Template repo — no dependencies | — |

Keep to the dependencies that shape architecture decisions. Don't list every transitive dep.

## Verification Commands

```bash
# Typecheck
printf '%s\n' 'N/A — template repo, no application code'

# Lint
printf '%s\n' 'N/A — template repo, no application code'

# Test
printf '%s\n' 'N/A — template repo, no application code'

# Build
printf '%s\n' 'N/A — template repo, no application code'

# Graph state (always available)
bv --robot-triage
br list --status open --status in_progress --json
```

Replace placeholders with your project's actual commands. These are what `/verify` runs.

## Security

```bash
# Dependency audit
printf '%s\n' 'N/A — template repo, no dependencies'

# Secrets scan (if configured)
printf '%s\n' 'N/A — no secrets scan configured'
```

## Constraints

- **Dependencies:** No new dependency without discussion. Audit before adding.
- **Token budget:** Keep each memory file under 2KB. Total memory context under 8KB.
- **No new tooling categories:** Skills = Markdown, commands = Markdown, extensions = TypeScript. If it doesn't fit, discuss first.
- **Verification gate:** Every bead must pass its verification commands before `/review` or `/pr`.

## Design Assets

| Asset | Path | Purpose |
|-------|------|---------|
| Brand contract | `DESIGN.md` | 9-section visual language spec |
| Design tokens | `design/tokens.css` | CSS custom properties (light + dark + system) |
| CSS base | `design/base.css` | Minimal reset + body defaults |
| CSS primitives | `design/primitives.css` | Base element styles (buttons, inputs, selects, tooltips) |

## Craft References

Brand-agnostic universal design rules that apply on top of `DESIGN.md`:

| File | Purpose |
|------|---------|
| `design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
| `design/craft/color.md` | Palette structure, accent discipline, contrast minimums, dark themes, semantic naming |
| `design/craft/anti-ai-slop.md` | Seven cardinal sins, soft tells, polish tells, soul-injection rules |
| `design/craft/animation-discipline.md` | When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits |

Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
