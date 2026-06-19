# Plan: br-omp-backbone-skill-3co

## Goal

Correct the `.omp/AGENTS.md` repository tree so it reflects the 10 tracked command files, including `git-clean.md`, without changing command semantics.

## Observed truths

1. The production diff for this bead changes only `.omp/AGENTS.md`.
2. The live Command Reference table already includes `/git-clean`.
3. The stale part was the repository tree block, which still said `Slash commands (9)` and listed only `init.md` on the final wrapped line.
4. `git ls-files '.omp/commands/*.md'` returns 10 tracked command files, including `git-clean.md`.
5. `git status --short .omp/commands` returns no output.
6. `README.md` still documents `/npm-release`; that is pre-existing repo drift and outside this bead's production scope.

## Intended production edit

Update exactly two tree-block facts in `.omp/AGENTS.md`:
- `Slash commands (9)` → `Slash commands (10)`
- `init.md` → `init.md, git-clean.md`

## Non-goals

- No edits to `.omp/commands/*.md`
- No edits to `.omp/extensions/*.ts`
- No edits to `README.md` in this bead
- No lifecycle changes

## Verification commands

```bash
git ls-files '.omp/commands/*.md'
git status --short .omp/commands
git diff main...HEAD -- .omp/AGENTS.md
br lint br-omp-backbone-skill-3co --json
br dep cycles --json
```

## Expected verification outcome

- Tracked inventory includes `git-clean.md`
- `.omp/AGENTS.md` tree says 10 commands and lists `git-clean.md`
- No command implementation files changed
- br lint stays clean
- Dependency cycles remain empty
