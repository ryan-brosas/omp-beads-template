# OMP Beads Template

An OMP-native project template with br as the task tracking backbone and bv for graph-informed planning. Every phase queries the graph before acting. Clean, boring, mechanical.

@memory/project/project.md
@memory/project/conventions.md

## The Workflow

Every piece of work flows through br beads. bv's 22 robot commands drive decisions at every phase. Commands + skills only — no scripts, no machinery.

```
/brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close
```

Or load the **orchestrator** skill to chain phases automatically — the agent reads the graph and decides which phase to enter next.

## Command Reference

| Command | What It Does | Reads | Writes | bv Commands |
|---------|-------------|-------|--------|-------------|
| `/brainstorm` | Ideas from graph + codebase exploration | — | — | triage, suggest, priority, label-attention, plan, search, file-hotspots |
| `/create` | Formalize into bead + PRD | br state, affected code | `prd.md`, `decisions.md` | triage, suggest, plan, search, label-health |
| `/plan` | Wave-sequence with blast radius | `prd.md` | `plan.md`, `tasks.md`, `context-capsule.md` | plan, impact, impact-network, blocker-chain, forecast, capacity, file-hotspots, file-relations |
| `/ship` | Implement with file awareness | `prd.md`, `plan.md` | changed source files | triage, alerts, related, impact, file-beads, file-relations |
| `/verify` | Run checks, record evidence | plan verification section | `completion-evidence.json` | triage, alerts, impact, impact-network, blocker-chain |
| `/review` | 5-agent parallel review with confidence scoring | `completion-evidence.json`, git diff | `review-report.md` | impact, related, file-beads, file-relations, suggest |
| `/pr` | Create GitHub PR (single-turn executable) | `review-report.md`, `completion-evidence.json` | PR body | — |
| `/close` | Close bead, suggest next | all artifacts | — | suggest, next, capacity |
| `/init` | Bootstrap workspace + br init | — | `.beads/` | — |

## Workflow Enforcement

The workflow-gate extension (`.omp/extensions/workflow-gate.ts`) blocks `edit`/`write` tools until required artifacts exist.

**You MUST follow the workflow:**
1. `/brainstorm` → `/create` → `/plan` → `/ship` → `/verify` → `/review` → `/pr` → `/close`
2. Each command checks its prerequisites. If it says "run X first," do it.
3. Do not fight the gate. If blocked, run the prerequisite.

**What gets blocked:**

| Tool | Condition | Error |
|------|-----------|-------|
| edit | No PRD for active bead | "Run /create first" |
| edit | No plan for active bead | "Run /plan first" |
| write | Same as edit | Same |

**What always passes:**
- Reading files (read tool, read-only bash)
- Writing to `.beads/` and `.omp/` (workflow files)
- Running `bv`, `br`, `git status`, `git diff`

**Bypass:** `OMP_SKIP_BEADS_WORKFLOW=1` (emergencies only).

## bv Capabilities (22 robot commands)

| Category | Commands | Use When |
|----------|----------|----------|
| **Triage** | triage, next, alerts, triage-by-label, triage-by-track | Entering any phase — what needs attention? |
| **Planning** | plan, priority, recipes | Before /plan — what's the right sequence? |
| **Impact** | impact, impact-network, causality, blocker-chain | Before /ship — what breaks if I change this? |
| **Files** | file-hotspots, file-beads, file-relations | During /ship — what else touches these files? |
| **Related** | related, search | During /review — what beads are connected? |
| **History** | diff, history, drift | During /review — how did this file evolve? |
| **Forecast** | forecast, capacity | Before /close — what's the next bottleneck? |
| **Labels** | label-health, label-flow, label-attention | During /brainstorm — where's the friction? |
| **Hygiene** | suggest, orphans | During /brainstorm — what's stale? |
| **Schema** | capabilities, schema, docs, metrics, help | When exploring — what can bv do? |

Full reference in the `bv` skill. Always `--robot-*` for machine-readable output. Always `--format json` for parseable results.

## br Conventions

- **Prefix:** `omp` (beads are `omp-a1b2`, `omp-c3d4`, ...)
- **Artifacts:** `.beads/artifacts/<bead-id>/` — prd.md, plan.md, tasks.md, completion-evidence.json, review-report.md
- **Inspect before mutate:** `br show <id> --json` before any state change
- **Claim atomically:** `br update <id> --claim --json`
- **Sync safely:** `br sync --flush-only` after mutations
- **Resolve actor:** `ACTOR="${BR_ACTOR:-assistant}"` on all br mutations
- **One bead per session** — restart after `/close`
- **Priority:** P0=critical, P1=high, P2=medium, P3=low, P4=backlog (numbers, not words)
- **Notes survive compaction:** write COMPLETED / IN PROGRESS / NEXT / BLOCKERS in the notes field

Full reference in the `br` skill. Short ID resolution: suffix match via `br list` → Python filter → `br show`.

## Memory Protocol

### Tier 1 — Always Load (via @memory/ references above)

- `project.md` — What are we building? Current phase?
- `conventions.md` — How do we build? Naming, workflow, agent rules.

These load automatically every session. Keep them under 1KB each.

### Tier 2 — On-Demand (load when relevant)

| File | Load When |
|------|-----------|
| `tech-stack.md` | Task touches tooling, builds, dependencies, or verification |
| `gotchas.md` | Working near known hazards or debugging |
| `decisions.md` | Making architectural choices or reviewing past decisions |

### Rules

- **Write-before-compaction** — extract durable facts to memory files before context fills
- **Consolidate, don't append** — rewrite files periodically, merge duplicates, remove stale entries
- **Update on `/close`** — every bead completion checks if conventions/decisions/gotchas changed
- **No secrets** — never write credentials, API keys, or tokens to memory files
- **Stale memory is worse than no memory** — audit periodically, delete obsolete entries

## Skills Map

| Skill | Load When | Lines |
|-------|-----------|-------|
| `br` | Before any br mutation or bead state query | 433 |
| `bv` | Before any bv query or graph analysis | 228 |
| `backbone` | First load — workflow reference card | 74 |
| `orchestrator` | User intent unclear or workflow stalls | — |
| `verification-before-completion` | Before /verify, /review, /pr, /close | 228 |
| `code-simplification` | Refactoring or complexity reduction | 165 |
| `root-cause-tracing` | Debugging — symptom → source | 125 |
| `defense-in-depth` | Adding validation layers | 126 |
| `incremental-implementation` | During /ship — slice strategy | 179 |
| `test-driven-development` | Writing tests before implementation | 212 |
| `testing-anti-patterns` | Reviewing or writing tests | 210 |
| `api-and-interface-design` | Designing contracts, endpoints, or types | — |
| `reflection-checkpoints` | During /ship — scope drift detection | — |
| `security-and-hardening` | Auditing for vulnerabilities, handling secrets | 566 |
| `deprecation-and-migration` | Removing old APIs or migrating data | — |

Skills are decision trees, not reference manuals. They tell the agent *what to do* and *in what order*, not *everything about the topic*.

## Project Structure

```
omp-template/
├── AGENTS.md                          # Delegates to .omp/AGENTS.md
├── .beads/                            # br workspace (SQLite + JSONL)
│   └── artifacts/<bead-id>/           # Bead artifacts
│       ├── prd.md                     # Problem, outcome, acceptance criteria
│       ├── plan.md                    # Scope, blast radius, steps, risks, verification
│       ├── tasks.md                   # Ordered task list with dependencies
│       ├── decisions.md               # Architecture and design decisions
│       ├── context-capsule.md         # Handoff for the next agent
│       ├── progress.txt               # Phase checklist
│       ├── completion-evidence.json   # Verification commands and results
│       ├── review-report.md           # Parallel review findings and verdict
│       └── solve-ledger.md            # Wave-by-wave execution log
├── .omp/
│   ├── AGENTS.md                      # You are here — canonical project context
│   ├── commands/                      # 9 slash commands (912 lines)
│   │   ├── brainstorm.md, create.md, plan.md, ship.md
│   │   ├── verify.md, review.md, pr.md, close.md, init.md
│   ├── skills/                        # 16 skills (2896 lines)
│   │   ├── br/SKILL.md, bv/SKILL.md
│   │   ├── backbone/SKILL.md, orchestrator/SKILL.md
│   │   └── <cognitive-tool>/SKILL.md
│   ├── extensions/                    # Workflow gate
│   │   └── workflow-gate.ts
│   ├── templates/                     # Artifact templates
│   │   └── prd.md, plan.md, tasks.md, review-report.md, ...
│   └── memory/project/                # Durable project knowledge
│       ├── project.md                 # Vision, goals, current phase
│       ├── conventions.md             # Naming, workflow, agent rules
│       ├── decisions.md               # Architecture decision records
│       ├── gotchas.md                 # Known pitfalls and mitigations
│       └── tech-stack.md              # Versions, verification commands, constraints
├── .gitignore
└── README.md
```

## Philosophy

- **YAGNI** — if it doesn't solve a real problem today, it doesn't exist. No speculative abstractions.
- **Prune over pad** — more context is not better. Fill the window with just the right information.
- **Graph-informed** — every phase queries bv before acting. The graph knows more than you do about the codebase.
- **Commands + skills only** — no scripts, no machinery. Every gap solvable through better prompts and skill knowledge.
- **Cognitive tools** — skills are decision trees that tell the agent *what to do next*, not reference manuals that describe *everything about a topic*.
- **Progressive disclosure** — lean core + references for deep content. AGENTS.md is the map; skills are the territory.
- **br is the backbone** — all work is tracked, all state is in beads, all evidence is in artifacts.
- **bv is the brain** — 22 robot commands for graph analysis. Query before you act.
- **Agent-native** — designed for AI coding agents from day one. Every artifact is a complete handoff.

## Guardrails

- **Ask before destructive** — confirm before deleting user code, force-pushing, or dropping beads
- **Never fabricate output** — no claim without observed evidence. If you didn't run it, don't report it.
- **Never expose secrets** — no credentials, API keys, or tokens in any artifact or memory file
- **Max 3 fix cycles** — if a bug survives 3 attempts, escalate. Don't loop.
- **Evidence before close** — `completion-evidence.json` must exist before `/review`, `/pr`, or `/close`
- **One bead per session** — stay focused. Don't multitask across beads.
- **Read before edit** — never guess file content. `read` the exact lines before touching them.
- **Scope to the active bead** — no "while you're in here" cleanups. If it's not in the plan, it's a separate bead.
