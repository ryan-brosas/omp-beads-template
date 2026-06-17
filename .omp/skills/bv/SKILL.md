---
name: bv
description: Use bv before action to get graph-informed triage, impact analysis, and review context.
---

# bv

## When to use

- You are about to brainstorm, plan, ship, verify, or review.
- You need file hotspots, related work, blast radius, or blockers.
- You need a graph-informed view before choosing the next bead.

## When not to use

- You already have the exact file, symbol, or callsite. Use OMP discovery tools directly.
- You want to skip inspection and jump to editing. Run bv first when the phase depends on context.

## Recommended command families

- Triage: `bv --robot-triage`, `bv --robot-next`, `bv --robot-alerts`
- Planning: `bv --robot-plan`, `bv --robot-priority`, `bv --robot-forecast`
- Impact: `bv --robot-impact`, `bv --robot-impact-network`, `bv --robot-blocker-chain`
- Files: `bv --robot-file-hotspots`, `bv --robot-file-beads`, `bv --robot-file-relations`
- Review hygiene: `bv --robot-related`, `bv --robot-suggest`

## Process

1. Start each phase with the smallest bv query that answers the decision in front of you.
2. Capture the concrete result that changes the plan: files, risks, dependencies, or missing work.
3. Use that result to scope edits, checks, or review.
4. Re-run bv when the phase changes or the blast radius grows.

## Anti-patterns

- Running the whole robot suite every time.
- Treating bv output as proof without checking the underlying files.
- Using bv as a substitute for verification after implementation.
