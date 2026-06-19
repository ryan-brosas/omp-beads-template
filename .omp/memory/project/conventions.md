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

## Languages by Purpose

| Purpose | Language | Notes |
|---------|----------|-------|
| Agent instructions | Markdown | Skills, commands, memory files |
| Configuration | JSON / YAML | settings, manifests |
| Backend | N/A | Template repo — no backend runtime |
| Frontend | N/A | Template repo — provides design system assets only |
| Scripts | Python | `/init` embeds the hydration helper inline; no standalone script file is shipped |

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

1. **Triage** — `bv --robot-triage` before any action
2. **Create** — `/create` produces PRD + plan + tasks
3. **Implement** — `/ship` follows plan, no scope creep
4. **Verify** — `/verify` runs checks, records evidence
5. **Review** — `/review` runs parallel agents, confidence filter
6. **PR** — `/pr` opens PR, single-turn execution
7. **Close** — `/close` after merge, suggests next bead

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

Keep `conventions.md` lean. Load the design docs only when a task actually touches UI work.

- **Brand contract:** `DESIGN.md`
- **Design assets:** `design/`
- **Craft references:** `design/craft/typography.md`, `design/craft/color.md`, `design/craft/anti-ai-slop.md`, `design/craft/animation-discipline.md`
- **Rule:** Link to detailed guidance from task-specific prompts instead of inlining it into always-loaded memory files.
