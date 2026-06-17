# Plan: Implement Honcho Memory Operating Workflow

## Scope
Update the template's agent-facing documentation so future agents know how to use Honcho efficiently as a persistent memory/reasoning layer.

## Blast Radius
- Agent documentation only.
- No source runtime, no external service configuration, no credentials.

## Steps
1. Inspect existing documentation surfaces to choose the canonical location.
2. Add a compact Honcho operating protocol with:
   - memory boundaries
   - tool-selection rules
   - reasoning-level rules
   - per-task retrieval and persistence flow
   - SDK/MCP design defaults if later wired
3. Verify the rendered file contains all required headings and no secrets.
4. Record completion evidence.

## Risks
- Over-documenting duplicates Honcho docs; keep this repository-specific and operational.
- Treating Honcho as source of truth conflicts with repo artifacts; explicitly keep repo artifacts canonical.

## Verification
Run targeted text checks against the updated documentation for required headings and prohibited secret patterns.
