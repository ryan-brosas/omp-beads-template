# OMP Beads Template Agent Instructions

## Project Overview

This repository is an OMP-native project template. It provides the bead workflow backbone for agent-driven software work: `br` owns task state, `bv` provides graph-aware planning signals, and `.omp/` contains the commands, skills, templates, and workflow gate.

## Setup Commands

- Start OMP in the project root: `omp`
- Initialize a fresh clone: `/init`
- Start new work through the bead workflow: `/brainstorm`, `/create`, `/plan`, then `/ship`
- Use `br --json` and `bv --robot-* --format json` for machine-readable workflow checks.

## Code Style

- Agent instructions and command recipes are Markdown.
- Configuration is JSON or YAML.
- `/init` keeps its hydration helper inline as Python; do not add standalone scripts.
- Keep the template boring: commands plus skills, exact file edits, no speculative machinery.

## Testing Instructions

- Run targeted verification for the files you change before yielding.
- For workflow changes, verify with `br`/`bv` JSON commands and file reads/searches.
- Record observed evidence; do not claim checks passed unless the command output was observed.

## OMP Workflow

- Read `.omp/AGENTS.md` for the full OMP-specific bead workflow and project memory contract.
- Work one bead per session.
- Query `bv` before acting, inspect `br` state before mutating, and keep implementation scoped to the active bead.

## Security

- Never commit secrets, credentials, tokens, or private keys.
- Keep local environment overrides such as `.env` ignored.
- Do not write secret values into bead artifacts, memory files, command docs, or Honcho memory.
