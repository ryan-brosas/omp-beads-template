# Review Report: br-omp-backbone-skill-0nc

## Verdict

`changes-requested` — README documents `/npm-release`, but the command file is untracked and absent from `HEAD`, so the reviewed commit would ship stale command inventory docs.

**Ready for close:** false

## Review Summary

- Agents run: 1 (`Review0nc`, consolidated spec/plan/bug/comment review)
- Total raw findings: 1
- High-confidence (≥80): 1
- False positives filtered: 0

## Findings

### #1: Ship the documented npm-release command (confidence: 95)

- **Agent:** Review0nc
- **Severity:** high
- **File:** `README.md`#50
- **Issue:** `README.md` now advertises `/npm-release`, but `.omp/commands/npm-release.md` is present only as an untracked working-tree file and is absent from the reviewed commit. Observed evidence: `git status --short .omp/commands/npm-release.md` reports `?? .omp/commands/npm-release.md`, and `git show HEAD:.omp/commands/npm-release.md` fails with `path '.omp/commands/npm-release.md' exists on disk, but not in 'HEAD'`.
- **Recommendation:** Either commit `.omp/commands/npm-release.md` as part of this bead or remove the `/npm-release` README inventory row/count wording. Do not close until README command inventory matches tracked shipped command files.

## Spec ↔ Code Adherence

- PRD requirement coverage: 6/7 requirements implemented for the tracked commit set. R1, R2, R3, R5, R6, and the create-phase R7 are satisfied by observed files/evidence; R4 is not satisfied because `/npm-release` is documented but not tracked in `HEAD`.
- Plan task coverage: 5/6 tasks completed for the tracked commit set. Tasks 1.1, 2.1, 2.3, 3.1, and 4.1 are satisfied; task 2.2 is incomplete until the command inventory references only tracked shipped command files or the command file is added.
- Drift from plan: README inventory verification used the working tree, not the committed artifact set. That let an untracked `.omp/commands/npm-release.md` satisfy the evidence check without being part of the reviewed diff.

## Residual Risks

- Hydration behavior was verified by the existing `completion-evidence.json` scratch run, but this review did not rerun full `/verify`; user requested `/review` only.
- `.omp/commands/npm-release.md` content was not reviewed as a shipped command because it is untracked and outside the committed diff.

## Summary

The root `AGENTS.md`, `/init` hydration block, and `.gitignore` changes match the PRD and plan at review depth. The README command inventory is not safe to merge because it documents a command file absent from `HEAD`. Fix the tracked command inventory mismatch, rerun `/verify`, then rerun `/review`.
