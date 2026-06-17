# Review Report: br-omp-backbone-skill-nvf

**Reviewer:** makora1 (automated)
**Date:** 2026-06-17
**Verdict:** ✅ APPROVED — All checks pass, ready for PR

## Summary

Fix `/init` hydration: project name precedence fixed to git-remote-first, project goal now always a human TODO marker, and Frontend/Scripts conventions use package dependency evidence gates instead of backend-language inference.

## Review Checks

### Acceptance Criteria Verification

| AC | Description | Result |
|----|-------------|--------|
| AC1 | Project name fallback: git_remote_name() → package_name → first_heading_from_readme() → root.name → "Untitled Project" | ✅ PASS |
| AC2 | project_desc always "<!-- TODO: fill in your project goal -->", no README auto-fill | ✅ PASS |
| AC3 | Frontend row only hydrates when framework deps (react/svelte/vue/next/nuxt/astro/angular/solid) detected; TODO markers when absent | ✅ PASS |
| AC4 | Scripts TypeScript only when tsx/ts-node deps detected; Bash fallback with TODO notes otherwise | ✅ PASS |
| AC5 | TODO markers when evidence absent (Frontend language+notes, Scripts notes) | ✅ PASS |
| AC6 | Existing hydration unchanged (backend_notes, verification dicts, security_audit) | ✅ PASS |
| AC7 | Idempotency preserved (replace_exact calls unchanged) | ✅ PASS |

### Code Quality

| Check | Result |
|-------|--------|
| Syntax (Python block compilation) | ✅ PYTHON_BLOCK_SYNTAX_OK |
| No new imports | ✅ Only original imports present |
| Old inference removed | ✅ Language-based frontend/scripts inference fully replaced |
| has_package_dependency helper | ✅ Clean, checks dependencies/devDependencies/peerDependencies |
| Diff scope | ✅ Only Phase 2.5 regions changed; no template/memory/design changes from this bead |

### br/bv Health

| Check | Result |
|-------|--------|
| br lint | ✅ 0 issues |
| Cycle detection | ✅ 0 cycles |
| bv alerts | ✅ 0 alerts |

## Diff Summary

```diff
.omp/commands/init.md | 32 +++++++++++++++++++-------------
1 file changed, 19 insertions(+), 13 deletions(-)
```

Changes:
1. **+has_package_dependency()** helper (new)
2. **project_name** reordered: git_remote_name() first
3. **project_desc** simplified to static TODO marker
4. **Frontend** replaced language inference with framework evidence gate
5. **Scripts** replaced language dict with tsx/ts-node evidence gate with Bash fallback

## Risks

- **Low risk:** Changes are contained within the Phase 2.5 Python block. No template changes, no new dependencies, no new imports.
- **Backward compatible:** The replace_exact idempotency mechanism is unchanged. Existing memory files will not be overwritten.
- **No behavioral regression:** `first_paragraph_from_readme()` function definition remains (unused by Phase 2.5), preserving it for any other potential callers.

## Recommendation

Approve. This is a clean, boring fix that addresses all three review findings from br-omp-backbone-skill-9tl. Ready for PR.
