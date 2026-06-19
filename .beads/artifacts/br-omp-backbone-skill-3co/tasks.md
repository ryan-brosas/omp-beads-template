# Tasks: br-omp-backbone-skill-3co

## 1. Confirm inventory
- [x] Run `git ls-files '.omp/commands/*.md'`.
- [x] Confirm there are 10 tracked command files.
- [x] Confirm `git-clean.md` is tracked.
- [x] Confirm `.omp/commands` is clean via `git status --short .omp/commands`.

## 2. Inspect canonical documentation
- [x] Read `.omp/AGENTS.md` Command Reference and confirm `/git-clean` is already documented there.
- [x] Read the repository tree block and confirm it was stale: count said 9 and listing omitted `git-clean.md`.
- [x] Keep the lifecycle prose unchanged.

## 3. Apply the minimal production fix
- [x] Change the tree comment to `Slash commands (10)`.
- [x] Change the wrapped command-file listing to `init.md, git-clean.md`.
- [x] Avoid unrelated edits to command implementations, extensions, or README.

## 4. Verify and hand off
- [x] Re-read `.omp/AGENTS.md` and confirm the tree now matches tracked files.
- [x] Record accurate completion evidence for `git-clean`, not `npm-release`.
- [x] Record the pre-existing README drift separately so later agents are not misled.
- [x] Run `br lint br-omp-backbone-skill-3co --json`.
- [x] Run `br dep cycles --json`.
