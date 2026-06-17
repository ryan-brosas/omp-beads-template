---
name: beads-review
description: Review the active bead after verification using bv context plus direct file inspection.
---

Review the active bead.

User input: $ARGUMENTS

Requirements:
- Require verification evidence before final review.
- Use bv for related work, file history, hotspots, or impact context.
- Read the changed files directly; do not rely only on summaries.
- Write `.beads/artifacts/<bead-id>/review-report.md` using `.omp/templates/review-report.md` as the shape.
- Call out findings, residual risks, and whether the bead is ready for PR or close.
