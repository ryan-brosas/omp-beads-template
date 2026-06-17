# OMP Beads Template

An OMP-native project template with br as the task tracking backbone and bv for graph-informed planning. Every phase queries the graph before acting. Clean, boring, mechanical.

@memory/project/project.md
@memory/project/conventions.md

## The Workflow

Every piece of work flows through br beads. bv's robot commands drive decisions at every phase. Commands + skills only — no scripts, no machinery.

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

## bv Capabilities

| Category | Commands | Use When |
|----------|----------|----------|
| **Triage & Planning** | triage, next, plan, priority | Entering any phase — what needs attention? |
| **Graph Analysis** | insights, alerts, suggest, forecast | Before /plan — graph metrics, cycles, staleness |
| **Labels** | label-health, label-flow, label-attention | During /brainstorm — where's the friction? |
| **History & Change** | history, diff | During /review — how did this file evolve? |
| **Sprint & Files** | burndown, file-hotspots, file-beads, file-relations | During /ship and /review — what else touches these files? |
| **Graph Export** | graph (json, dot, mermaid, html) | Visualizing dependencies or embedding in docs |

Always `--robot-*` for machine-readable output. Always `--format json` for parseable results. Prefer `--robot-triage` as the single entry point.

### Per-Phase Quick Reference

| Phase | Smallest Useful Query |
|-------|----------------------|
| `/brainstorm` | `bv --robot-triage --format json` |
| `/plan` | `bv --robot-plan --format json` |
| `/ship` | `bv --robot-file-beads <path> --format json` |
| `/review` | `bv --robot-file-hotspots --format json` + `bv --robot-file-relations --format json` |
| `/verify` | `bv --robot-alerts --format json` |
| `/close` | `bv --robot-suggest --format json` |


## br Conventions

- **Prefix:** `br-omp` (beads are `br-omp-<purpose>-<short-id>`, e.g. `br-omp-backbone-skill-1da`)
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

### Tier 1 — Always In Context

`@memory/project/project.md` and `@memory/project/conventions.md` are inlined into this file via OMP `@` imports before injection. They are always present in the agent's context — no separate load needed.

Keep each focused and concise. Target ≤1KB for project.md (vision + current phase), ≤4KB for conventions.md (workflow + naming + rules), and ≤2KB for other Tier 1 files. Prune stale entries before adding new ones.

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

## Honcho Memory

Honcho is the persistent memory layer. Full protocol in `conventions.md` → Honcho Memory section. Summary: `honcho_search` for prior context, `honcho_chat` for synthesis, `honcho_remember` for durable facts. Never store secrets or scratch state.

## Skills Map

| Skill | Load When |
|-------|-----------|
| `br` | Before any br mutation or bead state query |
| `bv` | Before any bv query or graph analysis |
| `honcho-memory` | When using Honcho search/chat/remember or designing Honcho-backed memory |
| `backbone` | First load — workflow reference card |
| `orchestrator` | User intent unclear or workflow stalls |
| `verification-before-completion` | Before /verify, /review, /pr, /close |
| `code-simplification` | Refactoring or complexity reduction |
| `root-cause-tracing` | Debugging — symptom → source |
| `defense-in-depth` | Adding validation layers |
| `incremental-implementation` | During /ship — slice strategy |
| `test-driven-development` | Writing tests before implementation |
| `testing-anti-patterns` | Reviewing or writing tests |
| `api-and-interface-design` | Designing contracts, endpoints, or types |
| `reflection-checkpoints` | During /ship — scope drift detection |
| `security-and-hardening` | Auditing for vulnerabilities, handling secrets |
| `deprecation-and-migration` | Removing old APIs or migrating data |
| `condition-based-waiting` | Tests with race conditions or timing dependencies |
| `design-system` | When generating UI, choosing colors/fonts/spacing, implementing components, or reviewing visual output |

Skills are decision trees, not reference manuals. They tell the agent *what to do* and *in what order*, not *everything about the topic*.
```
omp-template/
├── AGENTS.md                          # Delegates to .omp/AGENTS.md
├── .beads/                            # br workspace (SQLite + JSONL)
│   ├── beads.db                       # SQLite database
│   ├── beads.jsonl                    # Append-only journal
│   └── artifacts/                     # Per-bead artifact directories
│       └── <bead-id>/                 # e.g. br-omp-backbone-skill-1da
│           ├── prd.md                 # Problem, outcome, acceptance criteria
│           ├── prd.json               # Machine-readable requirements mirror
│           ├── plan.md                # Scope, blast radius, steps, risks, verification
│           ├── tasks.md               # Ordered task list with dependencies
│           ├── decisions.md           # Architecture and design decisions
│           ├── context-capsule.md     # Handoff for the next agent
│           ├── progress.txt           # Phase checklist and change log
│           ├── completion-evidence.json  # Verification commands and results
│           └── review-report.md       # Parallel review findings and verdict
├── .omp/                              # OMP harness configuration
│   ├── AGENTS.md                      # Canonical project context (loaded by OMP)
│   ├── commands/                      # Slash commands (9)
│   │   ├── brainstorm.md
│   │   ├── create.md
│   │   ├── plan.md
│   │   ├── ship.md
│   │   ├── verify.md
│   │   ├── review.md
│   │   ├── pr.md
│   │   ├── close.md
│   │   └── init.md
│   ├── skills/                        # Agent skills (17)
│   │   ├── br/SKILL.md
│   │   ├── bv/SKILL.md
│   │   ├── backbone/SKILL.md
│   │   ├── orchestrator/SKILL.md
│   │   ├── design-system/
│   │   │   ├── SKILL.md               # Brand contract + craft rules
│   │   │   └── DESIGN.md              # 9-section visual language spec
│   │   └── <cognitive-tool>/SKILL.md   # decision-tree pattern
│   ├── extensions/                    # OMP tool extensions
│   │   └── workflow-gate.ts           # edit/write gating based on bead state
│   ├── scripts/                       # Standalone utility scripts
│   │   └── hydrate-memory.py          # /init memory file hydration
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md
│   │   ├── prd.json
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── context-capsule.md
│   │   ├── progress.txt
│   │   ├── completion-evidence.json
│   │   ├── review-report.md
│   │   └── decisions.md
│   └── memory/project/                # Durable project knowledge
│       ├── project.md                 # Vision, goals, current phase
│       ├── conventions.md             # Naming, workflow, agent rules
│       ├── decisions.md               # Architecture decision records
│       ├── gotchas.md                 # Known pitfalls and mitigations
│       └── tech-stack.md              # Versions, verification commands, constraints
├── .gitignore
└── README.md

## Philosophy

- **YAGNI** — if it doesn't solve a real problem today, it doesn't exist. No speculative abstractions.
- **Prune over pad** — more context is not better. Fill the window with just the right information.
- **Graph-informed** — every phase queries bv before acting. The graph knows more than you do about the codebase.
- **Commands + skills only** — no scripts, no machinery. Every gap solvable through better prompts and skill knowledge.
- **Cognitive tools** — skills are decision trees that tell the agent *what to do next*, not reference manuals that describe *everything about a topic*.
- **Progressive disclosure** — lean core + references for deep content. AGENTS.md is the map; skills are the territory.
- **br is the backbone** — all work is tracked, all state is in beads, all evidence is in artifacts.
- **bv is the brain** — robot commands for graph analysis. Query before you act.
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
