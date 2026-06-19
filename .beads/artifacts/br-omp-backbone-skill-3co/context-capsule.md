# Context Capsule: br-omp-backbone-skill-3co

## Objective

Bring the `.omp/AGENTS.md` repository tree back in sync with the tracked command files by documenting all 10 shipped command files and listing `git-clean.md` in the tree block.

## What changed in production

- `.omp/AGENTS.md` tree comment changed from `Slash commands (9)` to `Slash commands (10)`.
- `.omp/AGENTS.md` command-file listing changed from `init.md` to `init.md, git-clean.md`.
- The Command Reference table already contained `/git-clean`; this bead does **not** add a new command row.

## Source of truth

Use tracked command files, not stale prose:

```bash
git ls-files '.omp/commands/*.md'
```

Observed tracked command files on this branch:
- `brainstorm.md`
- `close.md`
- `create.md`
- `git-clean.md`
- `init.md`
- `plan.md`
- `pr.md`
- `review.md`
- `ship.md`
- `verify.md`

## Constraints

1. Keep production scope to `.omp/AGENTS.md` only.
2. Do not modify `.omp/commands/*.md` implementations.
3. Do not modify `.omp/extensions/*.ts`.
4. Preserve the lifecycle chain `/brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close`.
5. Treat `/git-clean` as a housekeeping helper, not a lifecycle phase.

## Known pre-existing drift

`README.md` still documents `/npm-release` instead of `/git-clean`. That mismatch predates this PR and is not part of the production diff here. Record it as follow-up context, not as evidence for this bead.
