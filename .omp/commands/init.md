---
description: "Initialize or inspect the beads workflow backbone for this repository."
argument-hint: "[optional: bead prefix]"
---

## Prerequisites

None. This command bootstraps the workflow itself.

Initialize the repository for the beads workflow.

## Phase 1: Detect State

```bash
br where 2>/dev/null && echo "INITIALIZED" || echo "NEEDS_INIT"
```

If already initialized, report current state and skip to Phase 4.

## Phase 2: Initialize br

```bash
br init ${ARGUMENTS:+--prefix "$ARGUMENTS"}
```

Uses a sensible prefix derived from the repo name. Pass a prefix as `$ARGUMENTS` to override.

## Phase 2.5: Hydrate Memory Files

Detect repo metadata and fill the instantiated memory files under `.omp/memory/project/`.

Run this phase after `br init` and before Honcho config so downstream tooling can reuse the detected project identity.
Hydration is idempotent: only known template placeholders are replaced. If a user has already edited a field, leave it alone.

```bash
python3 .omp/scripts/hydrate-memory.py
```

Fresh clones get real project identity, stack hints, and TODO markers for human judgment fields.
Re-running `/init` is safe because the script only replaces the exact template placeholders.

## Phase 3: Configure Honcho Memory (Optional)

If Honcho is available, configure a project-local `.env` block. If not, skip this phase.

```bash
which honcho 2>/dev/null && echo "HONCHO_AVAILABLE" || echo "NO_HONCHO"
```

If `NO_HONCHO`: skip to Phase 4. Honcho is an optional memory layer — the template works without it.

If `HONCHO_AVAILABLE`: create or refresh the `.env` Honcho block:

```bash
python3 - <<'PY'
from pathlib import Path
import os
import re

root = Path.cwd()
project_md = root / ".omp" / "memory" / "project" / "project.md"
workspace_source = root.name
if project_md.exists():
    for line in project_md.read_text().splitlines():
        if line.startswith("# Project: "):
            workspace_source = line.split(":", 1)[1].strip() or root.name
            break
workspace = re.sub(r"[^a-z0-9_-]+", "-", workspace_source.lower()).strip("-") or "omp-project"
user = os.environ.get("USER") or os.environ.get("LOGNAME") or "user"
env_path = root / ".env"

managed = f"""# BEGIN OMP HONCHO
# Project-scoped Honcho memory for OMP. API keys stay in ~/.honcho/config.json or the shell env.
HONCHO_ENABLED=true
HONCHO_URL=http://localhost:8000
HONCHO_WORKSPACE_ID={workspace}
HONCHO_AI_PEER=omp
HONCHO_PEER_NAME={user}
HONCHO_SESSION_STRATEGY=directory
HONCHO_CONTEXT_TOKENS=24000
HONCHO_MAX_MESSAGE_LENGTH=25000
HONCHO_SEARCH_LIMIT=20
HONCHO_TOOL_PREVIEW_LENGTH=2000
# END OMP HONCHO
"""

existing = env_path.read_text() if env_path.exists() else ""
pattern = re.compile(r"# BEGIN OMP HONCHO\n.*?# END OMP HONCHO\n?", re.S)
if pattern.search(existing):
    updated = pattern.sub(managed, existing)
elif existing.strip():
    updated = existing.rstrip() + "\n\n" + managed
else:
    updated = managed
env_path.write_text(updated)
PY
```

Ensure `.env` is gitignored. Do not write `HONCHO_API_KEY` into `.env`; use `~/.honcho/config.json`, the shell env, or a local secret manager.

## Phase 4: Verify Backbone

Check that these directories exist:
- `.omp/commands/`, `.omp/skills/`, `.omp/templates/`, `.omp/extensions/`
- `.beads/artifacts/` (create with `.gitkeep` if missing)

## Phase 5: Check Hydration Results

Verify the hydrated memory files are present and no project-identity placeholders remain.

```bash
grep -R "<project-name>" .omp/memory/project/ && echo "UNRESOLVED_PROJECT_NAME" || echo "PROJECT_NAME_OK"
grep -R "<TypeScript | Go | Rust | Python>\|<TypeScript \\| Python \\| Go \\| Rust>\|<Node.js \\| Bun \\| Deno \\| Python 3.x \\| Go 1.x>\|<npm \\| pnpm \\| yarn \\| pip \\| cargo \\| go mod>" .omp/memory/project/ && echo "STACK_PLACEHOLDERS_REMAIN" || echo "STACK_PLACEHOLDERS_OK"
```

If stack placeholders remain, review `.omp/memory/project/conventions.md` and `tech-stack.md` and fill in any repo-specific fields the detector could not infer.
Intentional TODO markers like `<!-- TODO: fill in -->` and `<unknown>` are acceptable.

## Phase 6: Report

```
Workspace: <path from br where>
br version: <br version>
Bead prefix: <prefix>
Beads: <N open, M closed>
Backbone: .omp/ <healthy/missing>
Memory: hydration summary from Phase 2.5 + whether project-identity placeholders remain
Honcho: <configured if available, "not installed" otherwise>
Next: /brainstorm
```
