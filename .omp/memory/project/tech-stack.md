---
purpose: Tech stack, versions, verification commands, and constraints
updated: 2026-06-17
---

# Tech Stack: <project-name>

## Runtime

| Layer | Tool | Version | Notes |
|-------|------|---------|-------|
| Language | <TypeScript \| Python \| Go \| Rust> | <version> | <strict mode? async? experimental flags?> |
| Runtime | <Node.js \| Bun \| Deno \| Python 3.x \| Go 1.x> | <version> | <LTS? latest?> |
| Package manager | <npm \| pnpm \| yarn \| pip \| cargo \| go mod> | <version> | |
| Task tracking | br (beads_rust) | latest | `which br` — CLI task tracker |
| Graph intelligence | bv (beads_viewer) | latest | `which bv` — robot commands for graph analysis |

## Key Dependencies

| Dependency | Purpose | Version |
|------------|---------|---------|
| <name> | <what it does> | <version> |

Keep to the dependencies that shape architecture decisions. Don't list every transitive dep.

## Verification Commands

```bash
# Typecheck
<tsc --noEmit | mypy | cargo check | go vet>

# Lint
<eslint | ruff | clippy | golangci-lint>

# Test
<vitest run | pytest | cargo test | go test ./...>

# Build
<tsup | pip install -e . | cargo build --release | go build>

# Graph state (always available)
bv --robot-triage
br list --status open --status in_progress --json
```

Replace placeholders with your project's actual commands. These are what `/verify` runs.

## Security

```bash
# Dependency audit
<npm audit | pip-audit | cargo audit | govulncheck>

# Secrets scan (if configured)
<gitleaks detect | trufflehog filesystem .>
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

Brand-agnostic universal design rules that apply on top of any `DESIGN.md`:

| File | Purpose |
|------|---------|
| `design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
| `design/craft/color.md` | Palette structure, accent discipline, contrast minimums, dark themes, semantic naming |
| `design/craft/anti-ai-slop.md` | Seven cardinal sins, soft tells, polish tells, soul-injection rules |
| `design/craft/animation-discipline.md` | When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits |

Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
