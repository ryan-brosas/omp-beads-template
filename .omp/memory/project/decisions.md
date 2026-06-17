# Decisions

- Use `.omp/` as the native project root; do not keep parallel `.pi/` project config.
- Keep command names bare (`/create`, `/plan`, `/ship`) — no namespace prefix needed since OMP resolves commands by directory.
- Keep workflow files under `.beads/artifacts/<bead-id>/`.
- Prefer OMP built-ins over custom delegate or orchestration code.
- Start lean: br, bv, commands, skills, agents, and one workflow gate extension.
