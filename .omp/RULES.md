# Rules

## RULE #1

Do not implement without a plan. No edits, no writes, no code changes during brainstorm or explore phases. Implementation happens during `/ship` — after PRD and plan exist.

## RULE #2

Always use `br --json`. Never run `br` without `--json` — you will get colored terminal output that cannot be parsed. Always resolve actor: `ACTOR="${BR_ACTOR:-assistant}"` and pass `--actor "$ACTOR"` on all mutating commands.

## RULE #3

Never run bare `bv`. Always use `bv --robot-*` flags. Bare `bv` launches an interactive TUI that blocks the session. The primary entry points are `bv --robot-triage --format json` for triage and `bv --robot-plan --format json` for planning.

## RULE #4

Sync is explicit. br never runs git commands. After bead state changes, you must: `br sync --flush-only` → `git add .beads/ && git commit`. Before ending a session: `git pull --rebase` → `br sync --flush-only` → `git add .beads/ && git commit -m "Update issues"` → `git push` → `git status`.
