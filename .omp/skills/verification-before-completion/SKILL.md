---
name: verification-before-completion
description: Require concrete verification and recorded evidence before review, PR, or bead closure.
---

# verification before completion

## Principle

A bead is not done because the diff looks plausible. It is done when the changed behavior is checked and the evidence is recorded.

## Required outputs

- Targeted verification commands or scenarios.
- A concise result for each check.
- `.beads/artifacts/<bead-id>/completion-evidence.json` updated with those checks.

## Checklist

1. Re-read the plan's verification section.
2. Run only the checks that prove the changed behavior.
3. Record failures honestly.
4. If verification is partial, say exactly what remains.
5. Do not close the bead without evidence.
