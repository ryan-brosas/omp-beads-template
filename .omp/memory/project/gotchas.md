# Gotchas

- The workflow gate only understands the active bead if `br list --status open --status in_progress --json` works.
- The gate intentionally blocks `edit` and `write`; shell-based mutation can still bypass it if you choose to.
- Commands are prompt templates, not compiled code. Keep them explicit and deterministic.
- OMP loads project-native capabilities from `.omp/`; moving files back under `.pi/` will stop native discovery.
