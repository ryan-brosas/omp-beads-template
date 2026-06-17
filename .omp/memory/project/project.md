---
purpose: Project vision, goals, success criteria, and current phase
updated: 2026-06-17
---

# Project: OMP Beads Template

## The Goal

An OMP-native project template that provides br/bv-powered workflow infrastructure for AI-agent-driven software development — task tracking, graph-informed planning, artifact generation, and quality gating.

## Success Criteria

1. **Zero `<project-name>` or template placeholders in any `.omp/memory/project/` file** — `grep -r '<project-name>' .omp/memory/project/` returns no matches
2. **Every memory file is valid markdown with filled tables** — read each file; no orphan rows, consistent column counts
3. **An agent loading this context can answer "what is this project" within 3 seconds** — `project.md` heading + goal is self-contained and understandable

Keep to 3-5 criteria. Each must be verifiable — "good UX" is not verifiable. "Zero uncaught exceptions in prod for 30 days" is.

## Current Phase

- **Status:** active
- **Milestone:** Memory file hydration — project identity hardening
- **Next:** Audit command files for consistency with conventions.md

Update this section after every milestone. An agent reading this must understand, within 3 seconds, what the project is doing right now.
