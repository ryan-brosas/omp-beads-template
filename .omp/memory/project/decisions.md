# Decisions

- Use `.omp/` as the native project root; do not keep parallel `.pi/` project config.
- Keep command names namespaced as `beads-*` to avoid collisions with OMP built-ins.
- Keep workflow files under `.beads/artifacts/<bead-id>/`.
- Prefer OMP built-ins over custom delegate or orchestration code.
- Start lean: br, bv, commands, skills, agents, and one workflow gate extension.
