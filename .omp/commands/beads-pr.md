---
name: beads-pr
description: Prepare a pull-request summary from bead artifacts, verification evidence, and review findings.
---

Prepare the PR package for the active bead.

User input: $ARGUMENTS

Requirements:
- Read `prd.md`, `plan.md`, `completion-evidence.json`, and `review-report.md` when present.
- Summarize what changed, why it changed, how it was verified, and what remains risky.
- Produce concise reviewer-facing output.
- Do not invent checks or findings that were not recorded.
