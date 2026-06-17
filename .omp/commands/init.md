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

## Phase 3: Configure Honcho Memory

Create or refresh a project-local `.env` Honcho block. This block is intentionally local and must remain gitignored; it sets repo-scoped memory without storing secrets.

```bash
python3 - <<'PY'
from pathlib import Path
import os
import re

root = Path.cwd()
workspace = re.sub(r"[^a-z0-9_-]+", "-", root.name.lower()).strip("-") or "omp-project"
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

# Hermes-compatible Honcho knobs. Ignored by the current OMP plugin if unsupported.
HONCHO_RECALL_MODE=hybrid
HONCHO_WRITE_FREQUENCY=turn
HONCHO_DIALECTIC_REASONING_LEVEL=max
HONCHO_DIALECTIC_DYNAMIC=true
HONCHO_MESSAGE_MAX_CHARS=25000
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

Ensure `.env` is ignored:

```bash
python3 - <<'PY'
from pathlib import Path

path = Path(".gitignore")
text = path.read_text() if path.exists() else ""
entry = ".env"
if entry not in {line.strip() for line in text.splitlines()}:
    suffix = "" if text.endswith("\n") or not text else "\n"
    path.write_text(text + suffix + "\n# Local Honcho/OMP environment overrides\n.env\n")
PY
```

Do not write `HONCHO_API_KEY` into `.env`; use `~/.honcho/config.json`, `HONCHO_API_KEY` in the shell, or a local secret manager.

## Phase 4: Verify Backbone

Check that these directories exist:
- `.omp/commands/`, `.omp/skills/`, `.omp/templates/`, `.omp/extensions/`
- `.beads/artifacts/` (create with `.gitkeep` if missing)

## Phase 5: Check Agent Files

Verify these are present and current:
- `.omp/AGENTS.md` — the main agent context file
- `.omp/RULES.md` — the 6 rules
- `.omp/memory/project/*.md` — project conventions, tech-stack, decisions, gotchas

## Phase 6: Report

```
Workspace: <path from br where>
br version: <br version>
Bead prefix: <prefix>
Beads: <N open, M closed>
Backbone: .omp/ <healthy/missing>
Honcho: workspace=<HONCHO_WORKSPACE_ID from .env>, session=directory, endpoint=<HONCHO_URL from .env>
Next: /brainstorm
```
