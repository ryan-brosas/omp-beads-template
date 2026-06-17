<!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin — tasks lack detail, verification steps are vague, dependencies undefined. Every task needs a yaml block, concrete verification steps, and enough detail for parallel execution without reading the PRD or plan. -->
# Tasks: br-omp-backbone-skill-m6y

## 1. Memory File Cleanup {parallel}

Three memory files need independent edits. None depend on each other — all three can run in parallel. Each task below has exact before/after diffs. The line numbers and content were confirmed by reading the live files on 2026-06-18.

### Task–File Mapping

| Task | File | Current Size | Target Size | Lines Changed |
|------|------|-------------|-------------|---------------|
| 1.1 | `.omp/memory/project/conventions.md` | 6,996 bytes | <5,300 bytes | -34 lines, +3 lines |
| 1.2 | `.omp/memory/project/project.md` | 26 lines | ~26 lines | 2 lines changed, 3 lines replaced |
| 1.3 | `.omp/memory/project/tech-stack.md` | 64 lines | 64 lines | 6 lines replaced |

---

### 1.1 Trim conventions.md — Delete UI Design section, add pointer

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/memory/project/conventions.md"]
estimated_minutes: 5
```

**What:** Delete the entire `## UI Design` section (lines 97-130 in the live file as of 2026-06-18) and replace with a 3-line pointer to the design-system skill. This removes 34 lines (~1,830 bytes) of duplicated UI rules — animation philosophy, component variants, theme rules, icon rules — that are already present in `.omp/skills/design-system/DESIGN.md`, `.omp/skills/design-system/craft/animation-discipline.md`, and `.omp/skills/design-system/tokens.css`.

**Why:** The UI Design section causes every agent session — even non-UI sessions — to load ~1,830 bytes of animation rules, button variants, and focus ring conventions that are already available on-demand through the design-system skill. The design system is structured for progressive disclosure: load SKILL.md only when the task involves UI. conventions.md is always inlined. Removing the duplication respects that architecture.

**Where exactly:** The section spans from `## UI Design` (line 97) through the last icon rule (line 130), right before `## The Workflow` (currently line 132 after removal). The section to delete includes these subsections:

- `### Design System` (lines 99-101) — brand contract pointer (one-liner)
- `### Animation Philosophy` (lines 103-109) — 6 bullet points on easing, durations, accordion, scale floor, mount strategy, micro-feedback
- `### CSS Ownership` (line 112) — empty header, zero content
- `### Component Variants` (lines 114-116) — button variants + focus ring rules
- `### Craft Rules` (line 118) — empty header, zero content
- `### Theme` (lines 120-123) — light default, dark counterpart rules
- `### Icons` (lines 125-130) — 5 bullet points on icon set, aria-labels, emoji prohibition, sizing, decorative icons

**Step-by-step checklist:**

- [ ] **Confirm current state:** `grep -n "## UI Design" .omp/memory/project/conventions.md` returns line 97. `grep -n "## The Workflow" .omp/memory/project/conventions.md` returns line 132. If line numbers differ, adjust accordingly — the anchor points are the section headers, not line numbers.
- [ ] **Delete lines 97-130:** Use `edit` to remove the exact text block from `## UI Design\n\n### Design System\n\n...` through the last icon bullet `- **Decorative icons:** \`aria-hidden="true" focusable="false"\` on SVGs that repeat adjacent text labels.\n\n`. Do NOT delete `## The Workflow` or anything after it.

**Concrete before/after text for the edit tool:**

The `oldText` to match (exactly as it appears in the live file):

```markdown
## UI Design

### Design System

- **Brand contract:** `.omp/skills/design-system/DESIGN.md` — the 9-section source of truth for visual language.

### Animation Philosophy

- **Easing:** `cubic-bezier(0.23, 1, 0.32, 1)` is the single canonical curve for all UI transitions. Built-in `ease` is too weak; `ease-in` is forbidden for UI elements (feels sluggish).
- **Asymmetric durations:** enter ~200ms, exit ~140ms. Exit reads as decisive because the user has already chosen to dismiss.
- **Accordion expand/collapse:** `grid-template-rows: 0fr → 1fr` (modern auto-height pattern). Pair with opacity fade and the canonical easing. Reuse `.accordion-collapsible` + `.accordion-collapsible-inner`.
- **Scale floor:** Never animate from `transform: scale(0)`. Start from `scale(0.9)` or higher with `opacity: 0`.
- **Mount strategy:** Keep conditionally-visible elements mounted; toggle a CSS class. React unmounts skip the exit transition entirely.
- **Micro-feedback:** 120ms for hover/focus transitions (the `--dur-quick` token).

### CSS Ownership
### Component Variants

- **Buttons:** 5 variants — `default`, `primary`, `primary-ghost`, `ghost`, `subtle`. No new variants without a documented need.
- **Focus rings:** Use `--selected` (blue) + `--selected-soft` ring on inputs/selects. Use `--accent` (terracotta) for button focus-visible outlines. This separation lets a focused input and a primary CTA coexist without competing.

### Craft Rules
### Theme

- **Light default.** Dark via `[data-theme="dark"]` on `<html>`. System mode via `@media (prefers-color-scheme: dark)` when no explicit theme attribute.
- **Every token has a dark counterpart.** Never approximate dark values — each is chosen for perceptual equivalence.

### Icons

- **Icon set:** Use a single consistent icon library. Prefer 1.6–1.8px-stroke monoline SVG with `currentColor` so icons inherit text color.
- **Icon-only buttons:** Always include an `aria-label`. Pair with `.sr-only` text when the icon's meaning isn't universally obvious.
- **Never use emoji as UI icons.** Emoji render differently across platforms, lack `currentColor` inheritance, and read as unpolished. Reserve emoji for user-generated content only.
- **Icon sizing:** 16px for inline with body text, 20px for standalone UI (toolbar buttons, nav items), 24px for large controls.
- **Decorative icons:** `aria-hidden="true" focusable="false"` on SVGs that repeat adjacent text labels.

```

The `newText` to replace with:

```markdown
## UI Design

For UI design rules (animation, components, icons, theme, craft), load `design-system/SKILL.md`. The design system is on-demand — not inlined in every session.

```

These three lines give the agent enough information to know where to find UI rules without duplicating the rules themselves. The pointer is sparse by design — any agent that needs UI rules will load the skill, and any agent that doesn't won't waste context.

**Verification (run after the edit completes):**

- [ ] `grep "Animation Philosophy" .omp/memory/project/conventions.md` → 0 matches (zero exit code or empty output). Confirms the bulk of the section is gone.
- [ ] `grep "CSS Ownership" .omp/memory/project/conventions.md` → 0 matches. Confirms the empty header is gone.
- [ ] `grep "Component Variants" .omp/memory/project/conventions.md` → 0 matches. Confirms button/focus-ring rules are gone.
- [ ] `grep "design-system/SKILL" .omp/memory/project/conventions.md` → ≥1 match. Confirms the pointer was added.
- [ ] `grep "## The Workflow" .omp/memory/project/conventions.md` → 1 match. Confirms the section after UI Design wasn't accidentally deleted.
- [ ] `grep "## Honcho Memory" .omp/memory/project/conventions.md` → 1 match. Confirms sections before UI Design remain intact.
- [ ] `grep "4\. Never let memory drift" .omp/memory/project/conventions.md` → 1 match. Confirms the line immediately before the pointer survived.
- [ ] `wc -c < .omp/memory/project/conventions.md` → number < 5300. The exact target is ≤4500 but ≤5300 is acceptable per PRD edge case EC-2. The primary win is removing the duplication; the byte count is aspirational.
- [ ] `grep "Memory File Maintenance" .omp/memory/project/conventions.md` → 1 match. The memory maintenance rules (which prescribe this cleanup pattern) are still present.

**Size estimate after deletion:** 6,996 - ~1,830 (deleted UI section) + ~120 (pointer) = ~5,286 bytes. Within the ≤5,300 acceptable range.

---

### 1.2 Fix project.md — Self-matching grep + current phase update {parallel}

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/memory/project/project.md"]
estimated_minutes: 5
```

**What:** Fix two issues in project.md. **Change A:** Add `--exclude=project.md` to the self-referential grep command in Success Criterion #1 so running the prescribed check doesn't match the criterion text itself. **Change B:** Update the Current Phase section to reflect completed beads (nvf, vui) and the current bead (m6y).

**Why (Change A):** The success criterion at line 14 says `grep -r '<project-name>' .omp/memory/project/` returns no matches — but this very line contains `<project-name>`, so the command ALWAYS matches project.md. An agent running the prescribed verification can't distinguish between "real placeholder in another file" and "self-referential mention in the criterion." Adding `--exclude=project.md` excludes the criterion text itself from the check while still catching real placeholders in conventions.md, tech-stack.md, gotchas.md, and decisions.md.

**Why (Change B):** Two beads (nvf and vui) have been completed since the last project.md update. The Current Phase still says "active" with milestone "br-omp-backbone-skill-1da." Agents reading project.md to understand the project state get stale information, undermining the 3-second comprehension goal. The status should reflect that the template infrastructure is largely stable.

**Step-by-step checklist (Change A — line 14):**

- [ ] **Current line 14:** Read the exact text to confirm it matches:
  ```
  1. **Zero `<project-name>` or template placeholders in any `.omp/memory/project/` file** — `grep -r '<project-name>' .omp/memory/project/` returns no matches
  ```
- [ ] **Edit:** Change `grep -r '<project-name>' .omp/memory/project/` to `grep -r '<project-name>' .omp/memory/project/ --exclude=project.md`
- [ ] The edit MUST preserve all surrounding text — only insert ` --exclude=project.md` before the closing backtick.

**Step-by-step checklist (Change B — lines 22-26):**

- [ ] **Current lines 22-26:** Read to confirm they match:
  ```markdown
  - **Status:** active
  - **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
  - **Next:** Workflow verification — run a full /brainstorm → /create → /plan → /ship → /verify → /review → /pr → /close cycle to confirm all phases operate correctly after conventions.md fix
  ```
- [ ] **Edit:** Replace the entire 5-line Current Phase block with:
  ```markdown
  - **Status:** stable
  - **Milestone:** Post-review cleanup — fix Codex findings, trim conventions.md (br-omp-backbone-skill-m6y)
  - **Next:** Audit and harden the `/close` command to check memory file staleness on bead completion
  ```
- [ ] **Rationale for each field:**
  - **Status → stable:** The template infrastructure (commands, skills, memory files, extensions) has been through 3 review cycles and is no longer in active construction. Individual beads continue but the foundation is settled.
  - **Milestone → br-omp-backbone-skill-m6y:** This bead is the current work item. Mirroring the active bead keeps the phase self-consistent.
  - **Next → `/close` hardening:** The root cause analysis in the PRD identified that no staleness checklist exists for `/close`. This is the natural next bead — it would prevent future rot accumulation of the kind this bead is fixing.

**Verification (all checks, any order):**

- [ ] `grep "br-omp-backbone-skill-1da" .omp/memory/project/project.md` → 0 matches. The old milestone reference is gone.
- [ ] `grep "br-omp-backbone-skill-m6y" .omp/memory/project/project.md` → ≥1 match. The new milestone is present.
- [ ] `grep "Status.*stable" .omp/memory/project/project.md` → ≥1 match. Status updated.
- [ ] `grep "Next.*close" .omp/memory/project/project.md` → ≥1 match. Next step references `/close` hardening.
- [ ] `grep -rc '<project-name>' .omp/memory/project/ --exclude=project.md` → output is "0" or "0\n" (no other memory file contains `<project-name>`).
- [ ] `grep '<project-name>' .omp/memory/project/project.md` → returns the criterion line (expected — the criterion text itself mentions `<project-name>`, which is fine because it's excluded from the check).
- [ ] `grep "<project-name>" .omp/memory/project/conventions.md` → 0 matches (or whatever the actual count is — the point is the exclude worked).
- [ ] `grep "Workflow verification" .omp/memory/project/project.md` → 0 matches. The old Next text is gone.
- [ ] `wc -l .omp/memory/project/project.md` → 26 lines (same line count, only content changed).

**Grep `--exclude` portability note:** POSIX grep supports `--exclude`. macOS grep (BSD) supports it. BusyBox grep may not — if the environment has BusyBox, the verification check should use the fallback: `grep -rl '<project-name>' .omp/memory/project/ | grep -v project.md`. The criterion text in project.md may need updating to the fallback if BusyBox is confirmed. For this template repo (Linux/glibc), GNU grep is standard.

---

### 1.3 Fix tech-stack.md — Replace N/A with valid shell no-ops {parallel}

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/memory/project/tech-stack.md"]
estimated_minutes: 5
```

**What:** Replace all 6 occurrences of `N/A — ...` inside bash fenced code blocks with `true  # ...`. The N/A strings are not valid shell commands — copying the block and running it produces `N/A: command not found`. `true` is the canonical shell no-op: it exits 0, accepts arguments silently, and is explicit about intent.

**Where:** Two bash blocks — Verification Commands (4 N/A lines) and Security (2 N/A lines).

**Step-by-step checklist:**

- [ ] **Read the file** to confirm the exact N/A lines. Expected counts:
  - Verification Commands block: 4 occurrences of `N/A — template repo, no application code` (Typecheck, Lint, Test, Build)
  - Security block: 1 occurrence of `N/A — template repo, no dependencies` (Dependency audit) + 1 occurrence of `N/A — no secrets scan configured` (Secrets scan)
  - Total: 6 N/A lines across 2 bash blocks.
- [ ] **Confirm ALL N/A instances are inside bash fences.** Run `grep -n "N/A" .omp/memory/project/tech-stack.md`. If any N/A appears outside ```bash blocks (e.g., in the Runtime table: `| Language | N/A | — |`), do NOT touch those — they're prose, not shell commands.

**Before/after mapping for each of the 6 lines:**

| # | Block | Before | After |
|---|-------|--------|-------|
| 1 | Verification Commands | `N/A — template repo, no application code` | `true  # template repo — no application code` |
| 2 | Verification Commands | `N/A — template repo, no application code` | `true  # template repo — no application code` |
| 3 | Verification Commands | `N/A — template repo, no application code` | `true  # template repo — no application code` |
| 4 | Verification Commands | `N/A — template repo, no application code` | `true  # template repo — no application code` |
| 5 | Security | `N/A — template repo, no dependencies` | `true  # template repo — no dependencies` |
| 6 | Security | `N/A — no secrets scan configured` | `true  # no secrets scan configured` |

**Pattern rule for each replacement:**
- Find: `N/A —` at start of line (after comment line `# Typecheck` etc.)
- Replace with: `true  #` (note: double space before `#` for visual separation)
- Preserve the explanation text after the em dash

**Choice of `true` over `:`:**
- `true` is explicit about intent ("this is deliberately a no-op")  
- `:` is shell syntax sugar — less recognizable to non-shell experts and tooling (linters, syntax highlighters)
- Both exit 0 and accept arguments silently
- The double space before `#` makes the comment visually distinct from the command: `true  # reason` reads better than `true # reason`

**Verification (all checks):**

- [ ] `grep -c "true  #" .omp/memory/project/tech-stack.md` → ≥6. All 6 replacements landed.
- [ ] `grep "N/A" .omp/memory/project/tech-stack.md` → Check output carefully. There will be matches in prose (Runtime table: `| Language | N/A | — |`, Notes column: `N/A`). But ZERO matches within bash blocks.
- [ ] `sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | grep -c "N/A"` → 0. This extracts only the bash blocks and checks for N/A inside them.
- [ ] **Bash syntax check on extracted blocks:**
  ```bash
  # Extract verification commands block, strip ``` markers, pipe to bash -n
  sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | sed '1d;$d' | bash -n && echo "PASS: bash -n OK" || echo "FAIL: bash -n error"
  ```
  The `bash -n` flag does a syntax-only parse — no commands execute. It must exit 0.
- [ ] **Visual inspection:** Read both bash blocks. Confirm each replaced line starts with `true  #` followed by the original explanation. Confirm the comment lines (`# Typecheck`, `# Lint`, etc.) are unchanged.
- [ ] **No false positives from prose N/A:** `grep -n "N/A" .omp/memory/project/tech-stack.md` shows matches at specific line numbers. Verify these are in the Runtime table or Notes column, not inside backtick-fenced bash blocks.
- [ ] `grep "N/A — template repo, no application code" .omp/memory/project/tech-stack.md` → 0 matches. The exact old pattern is gone.
- [ ] `grep "N/A — template repo, no dependencies" .omp/memory/project/tech-stack.md` → 0 matches. Second old pattern is gone.
- [ ] `grep "N/A — no secrets scan configured" .omp/memory/project/tech-stack.md` → 0 matches. Third old pattern is gone.

---

## 2. Skill + Diagram Updates

Both tasks in this wave depend on Wave 1 (they need to know what content was removed from conventions.md to avoid duplication). They are parallel to each other — no dependency between 2.1 and 2.2.

### Task–File Mapping

| Task | File | Current Size | Action |
|------|------|-------------|--------|
| 2.1 | `.omp/skills/design-system/SKILL.md` | 94 lines | Append ~45-line "Craft Rules (Tier 1)" section |
| 2.2 | `.omp/AGENTS.md` | ~265 lines | Add 4 lines to template tree section |

---

### 2.1 Absorb UI Design rules into design-system SKILL.md

```yaml
depends_on: ["1.1"]
parallel: true
conflicts_with: []
files: [".omp/skills/design-system/SKILL.md"]
estimated_minutes: 8
```

**What:** Append the UI Design rules removed from conventions.md (Task 1.1) into `.omp/skills/design-system/SKILL.md` as a new `## Craft Rules (Tier 1)` section. This preserves the content — agents can still access animation philosophy, component variants, theme rules, and icon rules — but moves them to the on-demand skill rather than the always-inlined conventions.md.

**Why:** The design system is structured for progressive disclosure. SKILL.md is the entry point that agents load when a task involves UI — it references DESIGN.md for deep content. Moving the Tier 1-level rules (short, prescriptive, "always follow these") to SKILL.md keeps them discoverable without polluting every non-UI session's context.

**Where:** The new section appends after the existing `## Attribution` section (lines 90-94 in the current file). SKILL.md currently ends with an Apache 2.0 attribution block. The craft rules go after that block, separated by a blank line.

**Content to append (exact markdown):**

```markdown

## Craft Rules (Tier 1)

These rules are Tier 1 material (always in context per conventions.md) but live here
to keep conventions.md within its ≤4KB target. They were migrated from conventions.md
on 2026-06-17 during br-omp-backbone-skill-m6y.

### Animation

- **Easing:** `cubic-bezier(0.23, 1, 0.32, 1)` is the single canonical curve for all UI transitions. Built-in `ease` is too weak; `ease-in` is forbidden for UI elements (feels sluggish).
- **Asymmetric durations:** enter ~200ms, exit ~140ms. Exit reads as decisive because the user has already chosen to dismiss.
- **Accordion expand/collapse:** `grid-template-rows: 0fr → 1fr` (modern auto-height pattern). Pair with opacity fade and the canonical easing. Reuse `.accordion-collapsible` + `.accordion-collapsible-inner`.
- **Scale floor:** Never animate from `transform: scale(0)`. Start from `scale(0.9)` or higher with `opacity: 0`.
- **Mount strategy:** Keep conditionally-visible elements mounted; toggle a CSS class. React unmounts skip the exit transition entirely.
- **Micro-feedback:** 120ms for hover/focus transitions (the `--dur-quick` token).

### Components

- **Buttons:** 5 variants — `default`, `primary`, `primary-ghost`, `ghost`, `subtle`. No new variants without a documented need.
- **Focus rings:** Use `--selected` (blue) + `--selected-soft` ring on inputs/selects. Use `--accent` (terracotta) for button focus-visible outlines. This separation lets a focused input and a primary CTA coexist without competing.

### Theme

- **Light default.** Dark via `[data-theme="dark"]` on `<html>`. System mode via `@media (prefers-color-scheme: dark)` when no explicit theme attribute.
- **Every token has a dark counterpart.** Never approximate dark values — each is chosen for perceptual equivalence.

### Icons

- **Icon set:** Use a single consistent icon library. Prefer 1.6–1.8px-stroke monoline SVG with `currentColor` so icons inherit text color.
- **Icon-only buttons:** Always include an `aria-label`. Pair with `.sr-only` text when the icon's meaning isn't universally obvious.
- **Never use emoji as UI icons.** Emoji render differently across platforms, lack `currentColor` inheritance, and read as unpolished. Reserve emoji for user-generated content only.
- **Icon sizing:** 16px for inline with body text, 20px for standalone UI (toolbar buttons, nav items), 24px for large controls.
- **Decorative icons:** `aria-hidden="true" focusable="false"` on SVGs that repeat adjacent text labels.
```

**Step-by-step checklist:**

- [ ] **Read the current SKILL.md** to confirm it ends with the Attribution section (last line ~94). If a prior bead added content after Attribution, find the actual end-of-file and append there instead.
- [ ] **Read DESIGN.md § Do's and Don'ts** to confirm no contradiction exists between the rules being appended and the authoritative DESIGN.md content. The rules should be consistent — they're the same rules, just summarized to Tier 1 density.
- [ ] **Check for pre-existing craft rules:** `grep -n "Craft Rules" .omp/skills/design-system/SKILL.md`. If found (line number returned), the content was already migrated by a prior bead. In that case, compare the existing sub-sections to the to-be-appended list. Append only missing sub-sections. If all four (Animation, Components, Theme, Icons) already exist, skip this task and mark it as "already complete."
- [ ] **Append the new section** after the last line of the file. Use `edit` to match a unique trailing snippet (e.g., the last line of the Attribution section) and append after it.
- [ ] **Confirm the blank line separator** between the Attribution section and the new Craft Rules section is present (prevents markdown rendering issues).

**Verification:**

- [ ] `grep -c "Craft Rules (Tier 1)" .omp/skills/design-system/SKILL.md` → 1. The new section header exists exactly once.
- [ ] `grep -c "### Animation" .omp/skills/design-system/SKILL.md` → Exactly 1 (the new sub-section). SKILL.md previously had no `### Animation` header — the Process section uses numbered steps, not sub-headers.
- [ ] `grep -c "cubic-bezier" .omp/skills/design-system/SKILL.md` → ≥2. Originally appeared in the Process section's Rule #5 (single easing curve). Now also appears in the Craft Rules → Animation section.
- [ ] `grep -c "aria-hidden" .omp/skills/design-system/SKILL.md` → 1. New icon rule for decorative SVGs. SKILL.md previously had no aria-hidden rules.
- [ ] `grep -c "emoji" .omp/skills/design-system/SKILL.md` → ≥4. Appears in multiple places: Process Rule #11 (no emoji as UI icons), new Craft Rules → Icons (never use emoji as UI icons), DESIGN.md reference row in the Process table, and the Verify checklist. The content is consistent, not contradictory.
- [ ] `grep -c "scale(0)" .omp/skills/design-system/SKILL.md` → ≥2. Process Rule #8 + new Craft Rule.
- [ ] `grep "Apache 2.0" .omp/skills/design-system/SKILL.md` → 1 match. The Attribution section is intact (not overwritten).
- [ ] `grep "br-omp-backbone-skill-m6y" .omp/skills/design-system/SKILL.md` → 1 match. The migration provenance comment is present.
- [ ] `wc -l .omp/skills/design-system/SKILL.md` → approximately 140 lines (was 94, + ~45 for new section). Confirm the file grew by roughly the expected amount.

**Content consistency check with DESIGN.md:** The appended rules must not contradict DESIGN.md. Run these spot-checks:

- [ ] DESIGN.md says "Single easing curve: cubic-bezier(0.23, 1, 0.32, 1)" → Craft Rules says the same. ✓
- [ ] DESIGN.md says "Never animate from scale(0). Floor is scale(0.9)" → Craft Rules says the same. ✓
- [ ] DESIGN.md says "Light mode default, dark via [data-theme='dark']" → Craft Rules says the same with additional `@media` detail. ✓ Non-contradictory enhancement.
- [ ] DESIGN.md says "5 button variants" → Craft Rules enumerates the same 5. ✓
- [ ] DESIGN.md says "No emoji as UI icons" → Craft Rules says the same with rationale. ✓

---

### 2.2 Complete AGENTS.md template tree diagram {parallel}

```yaml
depends_on: ["1.1"]
parallel: true
conflicts_with: []
files: [".omp/AGENTS.md"]
estimated_minutes: 4
```

**What:** Add 4 missing template files (`prd.json`, `decisions.md`, `completion-evidence.json`, `progress.txt`) to the repository tree diagram in AGENTS.md. The tree currently lists 5 templates; the actual directory contains 9.

**Why:** The AGENTS.md tree is the agent's canonical map of the repository. When the tree omits files, agents don't know they exist — they won't look for `prd.json` during `/create`, won't find `completion-evidence.json` during `/verify`, and won't know about `progress.txt` during `/ship`. The `/verify` command explicitly references `.omp/templates/completion-evidence.json` but the tree doesn't show it, creating a confusing "ghost file" situation.

**Current tree (lines 231-237 in AGENTS.md):**

```
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── context-capsule.md
│   │   └── review-report.md
```

**New tree (replaces the above 7 lines):**

```
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md
│   │   ├── prd.json
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── context-capsule.md
│   │   ├── decisions.md
│   │   ├── completion-evidence.json
│   │   ├── progress.txt
│   │   └── review-report.md
```

**Sort order rationale:**
- `prd.md` first (primary artifact, referenced by /create, /plan, /ship, /review)
- `prd.json` second (machine-readable mirror of prd.md, referenced by /create)
- `plan.md`, `tasks.md`, `context-capsule.md` (planning artifacts, referenced by /plan)
- `decisions.md` (architecture decisions, referenced by /create; alphabetical slot after context-capsule)
- `completion-evidence.json` (verification results, referenced by /verify, /review, /pr, /close)
- `progress.txt` (progress tracking, referenced by /ship)
- `review-report.md` last (review findings, referenced by /review, /pr, /close; was previously last)

**Step-by-step checklist:**

- [ ] **Read the current template tree section** in AGENTS.md (lines 231-237) to confirm the exact text, whitespace, and Unicode box-drawing characters (`├──`, `│`, `└──`). If the format has been changed (e.g., ASCII fallback `|--`), match the existing style exactly.
- [ ] **List actual template files on disk:** `ls .omp/templates/` → confirm 9 files: `completion-evidence.json`, `context-capsule.md`, `decisions.md`, `plan.md`, `prd.json`, `prd.md`, `progress.txt`, `review-report.md`, `tasks.md`.
- [ ] **Edit the tree block:** Replace the 7-line template subtree (from `│   ├── templates/` through `│   │   └── review-report.md`) with the 11-line expanded subtree.
- [ ] **Maintain Unicode consistency:** The replacement MUST use the same Unicode box-drawing characters as the rest of the tree. Copy-paste the existing `│   ├── ` and `│   │   └── ` patterns.
- [ ] **Ensure the tree continues correctly after templates:** The line after `│   │   └── review-report.md` is currently `│   └── memory/project/`. Confirm this line is NOT changed — the templates section ends, memory/project section begins. The indentation level must match.

**Concrete oldText/newText for the edit tool:**

The `oldText` to match (the exact 7-line template subtree):

```
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── context-capsule.md
│   │   └── review-report.md
```

The `newText` replacement:

```
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md
│   │   ├── prd.json
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── context-capsule.md
│   │   ├── decisions.md
│   │   ├── completion-evidence.json
│   │   ├── progress.txt
│   │   └── review-report.md
```

**Verification (all checks):**

- [ ] `grep -c "prd.json" .omp/AGENTS.md` → ≥1. Was 0 before.
- [ ] `grep -c "decisions.md" .omp/AGENTS.md` → ≥2. Was 1 before (appears in memory/project section). Now ≥2 (also in templates).
- [ ] `grep -c "completion-evidence.json" .omp/AGENTS.md` → ≥1. Was 0 before in the tree.
- [ ] `grep -c "progress.txt" .omp/AGENTS.md` → ≥1. Was 0 before.
- [ ] **Template entries count matches disk count:**
  ```bash
  # Extract template entries from the tree (lines between templates/ and next section, excluding the templates/ header itself)
  TREE_COUNT=$(sed -n '/templates\/.*Artifact templates/,/^│   └── memory/p' .omp/AGENTS.md | grep -cE '├──|└──')
  DISK_COUNT=$(ls .omp/templates/ | wc -l)
  echo "Tree: $TREE_COUNT, Disk: $DISK_COUNT"
  [ "$TREE_COUNT" -eq "$DISK_COUNT" ] && echo "PASS" || echo "FAIL"
  ```
  Expected: `Tree: 9, Disk: 9` → PASS.
- [ ] **Each template file name appears exactly once in the templates subtree:** Run the sed extraction above and pipe through `sort | uniq -c`. Each filename should have count 1 (no duplicates).
- [ ] **The tree is still parseable:** No broken Unicode characters, no misaligned box-drawing. Read the 15 lines around the templates section visually.
- [ ] **The `beads.jsonl` reference is unchanged:** `grep "beads.jsonl" .omp/AGENTS.md` → ≥1 match (exists in the `.beads/` section of the tree). The PRD note about "beans.jsonl" was a historical concern — the current tree correctly says `beads.jsonl`. Confirm this is still true.

---

## 3. Commit + Verification

Wave 3 runs after all Wave 1 and Wave 2 tasks are complete. It's sequential — commit first (to capture a clean state), then verify against that commit.

### 3.1 Atomic commit of all changes

```yaml
depends_on: ["1.1", "1.2", "1.3", "2.1", "2.2"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 2
```

- [ ] **Stage all changed source files:**
  ```bash
  git add .omp/memory/project/conventions.md \
          .omp/memory/project/project.md \
          .omp/memory/project/tech-stack.md \
          .omp/skills/design-system/SKILL.md \
          .omp/AGENTS.md
  ```
- [ ] **Stage bead artifacts:**
  ```bash
  git add .beads/artifacts/br-omp-backbone-skill-m6y/
  ```
- [ ] **Review the diff stat:** `git diff --cached --stat` — confirm exactly 5 source files changed (3 memory, 1 skill, 1 AGENTS.md) plus bead artifacts. Zero unexpected files.
- [ ] **Review the diff content:** `git diff --cached` — verify the changes are exactly as described in tasks 1.1-2.2. No extra changes leaked in. No whitespace corruption. No accidental deletions.
- [ ] **Verify git status is clean beyond the staged files:** `git status --short` — only the expected files show as staged (M) or new (A). No unstaged changes to any file.
- [ ] **Commit with conventional format:**
  ```bash
  git commit -m "fix: post-review cleanup — trim conventions, harden success criteria, complete tree (br-omp-backbone-skill-m6y)"
  ```
  The commit message format: `fix:` (not `feat:` — this is a bugfix/cleanup, not new functionality). Bead ID in parentheses at end.
- [ ] **Verify commit exists:** `git log -1 --oneline` shows the commit with correct message.
- [ ] **Verify working tree is clean after commit:** `git status --porcelain` returns empty (or only untracked files that aren't part of this bead).

### 3.2 Full verification battery

```yaml
depends_on: ["3.1"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 5
```

All 18 checks below must pass. Each produces a PASS/FAIL line. Record all results in completion-evidence.json.

**Check 1 — conventions.md size under limit:**
```bash
SIZE=$(wc -c < .omp/memory/project/conventions.md)
[ "$SIZE" -lt 5300 ] && echo "PASS: conventions.md size = $SIZE (target <5300)" || echo "FAIL: conventions.md size = $SIZE (target <5300)"
```

**Check 2 — No UI Design section in conventions.md:**
```bash
[ $(grep -c "Animation Philosophy" .omp/memory/project/conventions.md) -eq 0 ] && echo "PASS: Animation Philosophy removed from conventions.md" || echo "FAIL: Animation Philosophy still in conventions.md"
```

**Check 3 — UI Design rules in SKILL.md:**
```bash
[ $(grep -c "Animation" .omp/skills/design-system/SKILL.md) -ge 2 ] && echo "PASS: UI Design rules in SKILL.md" || echo "FAIL: UI Design rules missing from SKILL.md"
```

**Check 4 — Design pointer in conventions.md:**
```bash
grep -q "design-system/SKILL" .omp/memory/project/conventions.md && echo "PASS: design-system pointer in conventions.md" || echo "FAIL: design-system pointer missing"
```

**Check 5 — Self-match grep fixed:**
```bash
OUT=$(grep -rc '<project-name>' .omp/memory/project/ --exclude=project.md 2>&1)
LAST=$(echo "$OUT" | tail -1 | grep -o '[0-9]*$')
[ "$LAST" = "0" ] && echo "PASS: self-match grep returns 0 (excludes project.md)" || echo "FAIL: self-match grep returned: $OUT"
```

**Check 6 — No N/A in tech-stack bash blocks:**
```bash
COUNT=$(sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | grep -c "N/A")
[ "$COUNT" -eq 0 ] && echo "PASS: zero N/A in tech-stack bash blocks" || echo "FAIL: $COUNT N/A found in bash blocks"
```

**Check 7 — true no-ops present:**
```bash
COUNT=$(grep -c "true  #" .omp/memory/project/tech-stack.md)
[ "$COUNT" -ge 6 ] && echo "PASS: $COUNT true no-ops in tech-stack.md" || echo "FAIL: only $COUNT true no-ops (need ≥6)"
```

**Check 8 — Bash blocks parse:**
```bash
sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | sed '1d;$d' | bash -n 2>&1 && echo "PASS: tech-stack bash blocks parse" || echo "FAIL: bash -n error"
```

**Check 9 — prd.json in AGENTS.md tree:**
```bash
grep -q "prd.json" .omp/AGENTS.md && echo "PASS: prd.json in AGENTS.md" || echo "FAIL: prd.json not in AGENTS.md"
```

**Check 10 — decisions.md in template tree section:**
```bash
grep -A30 "templates/" .omp/AGENTS.md | grep -q "decisions.md" && echo "PASS: decisions.md in template tree" || echo "FAIL: decisions.md not in template tree"
```

**Check 11 — completion-evidence.json in template tree:**
```bash
grep -A30 "templates/" .omp/AGENTS.md | grep -q "completion-evidence.json" && echo "PASS: completion-evidence.json in template tree" || echo "FAIL: completion-evidence.json not in template tree"
```

**Check 12 — progress.txt in template tree:**
```bash
grep -A30 "templates/" .omp/AGENTS.md | grep -q "progress.txt" && echo "PASS: progress.txt in template tree" || echo "FAIL: progress.txt not in template tree"
```

**Check 13 — Old milestone (1da) gone from project.md:**
```bash
[ $(grep -c "br-omp-backbone-skill-1da" .omp/memory/project/project.md) -eq 0 ] && echo "PASS: old milestone removed" || echo "FAIL: old milestone still present"
```

**Check 14 — New milestone (m6y) present in project.md:**
```bash
grep -q "br-omp-backbone-skill-m6y" .omp/memory/project/project.md && echo "PASS: new milestone present" || echo "FAIL: new milestone missing"
```

**Check 15 — Status is stable:**
```bash
grep -q "Status.*stable" .omp/memory/project/project.md && echo "PASS: status is stable" || echo "FAIL: status not stable"
```

**Check 16 — No dependency cycles:**
```bash
br dep cycles --json 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
sys.exit(0 if d.get('count', 0) == 0 else 1)
" && echo "PASS: zero dependency cycles" || echo "FAIL: dependency cycles found"
```

**Check 17 — No bv alerts:**
```bash
bv --robot-triage --format json 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
sys.exit(0)
" && echo "PASS: bv robot-triage succeeded" || echo "FAIL: bv robot-triage failed"
```

**Check 18 — Git diff clean (no whitespace errors, conflict markers):**
```bash
git diff --check HEAD~1 && echo "PASS: git diff clean" || echo "FAIL: whitespace or conflict marker issues"
```

**Record results:**
- [ ] Create `.beads/artifacts/br-omp-backbone-skill-m6y/completion-evidence.json` with all 18 check results
- [ ] Each entry: check number, description, "PASS"/"FAIL", and output/values
- [ ] If any check fails, mark completion status as "partial" and document which checks failed
- [ ] All 18 must PASS for a clean completion

### 3.3 Sync artifacts to bead graph

```yaml
depends_on: ["3.2"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 1
```

- [ ] `br sync --flush-only` — flush artifact changes to the bead graph
- [ ] Verify command exits 0
- [ ] `br show br-omp-backbone-skill-m6y --json` — confirm bead is visible in the graph with correct metadata
- [ ] `ls -la .beads/artifacts/br-omp-backbone-skill-m6y/` — all 5 artifacts present: prd.md, prd.json, plan.md, tasks.md, context-capsule.md, completion-evidence.json

---

## 4. Edge Cases During Implementation

These are conditions that may arise during implementation and how to handle each one. Read before starting Wave 1.

### EC-1: conventions.md line numbers shifted

**Trigger:** File has been edited between plan creation and implementation.

**Check:** `grep -n "## UI Design" .omp/memory/project/conventions.md` returns a line number ≠ 97.

**Response:** Use section-header anchors, not line numbers. Delete everything between `## UI Design` (inclusive) and `## The Workflow` (exclusive). Insert the 3-line pointer exactly where `## UI Design` was. Run `grep -n "## The Workflow" .omp/memory/project/conventions.md` to confirm the anchor still exists.

**Safe approach for the edit:** Match the exact `## UI Design` header text plus the 3-line pointer as `newText`, and match the entire UI Design section plus `## The Workflow` header as `oldText`, replacing with pointer + `## The Workflow`. This is anchor-based, not line-number-based.

### EC-2: SKILL.md already has craft rules

**Trigger:** `grep "Craft Rules" .omp/skills/design-system/SKILL.md` returns a line number. This would mean a prior bead already migrated the rules.

**Response:** Compare the existing craft rules section to what this task would append:
- If all four sub-sections (Animation, Components, Theme, Icons) are already present → skip Task 2.1 entirely. Mark it as "already complete in prior bead."
- If some sub-sections are missing → append only the missing sub-sections under the existing `## Craft Rules` header.
- Add a comment noting: "Sub-sections [X, Y] already present from prior bead; only [Z] appended here."

### EC-3: AGENTS.md tree uses different Unicode characters

**Trigger:** `grep "├──" .omp/AGENTS.md` returns 0 matches. The tree may use ASCII `|--` or different Unicode variants.

**Response:** Match the existing style exactly. If the tree uses `|--` (ASCII), use `|--`. If it uses `├──` (Unicode), use `├──`. The edit's `oldText` must be a verbatim copy of the current template subtree — read it with `read` to capture exact characters before writing the edit. Never assume the characters.

### EC-4: tech-stack.md has N/A outside bash blocks that looks like a command

**Trigger:** An `N/A —` string appears in a table cell or prose line, visually similar to the bash-block N/A lines.

**Response:** ONLY replace N/A lines inside ` ```bash ` fenced blocks. Use `sed -n '/```bash/,/```/p'` to extract bash blocks and verify replacements are scoped correctly. N/A in prose (e.g., Runtime table `| Language | N/A | — |`) is NOT a shell command and must not be modified.

### EC-5: `--exclude=project.md` flag not supported by grep

**Trigger:** `echo "test" | grep --exclude=dummy test 2>&1` produces an error about unrecognized option.

**Response:** The fix uses `--exclude` which is POSIX and supported by GNU grep and BSD (macOS) grep. BusyBox grep may not support it. If the environment uses BusyBox:
1. Change the criterion text to use the pipe fallback: `grep -rl '<project-name>' .omp/memory/project/ | grep -v project.md` returns no matches
2. Verify the fallback works: `grep -rl '<project-name>' .omp/memory/project/ | grep -v project.md | wc -l` → 0
3. Document in the criterion that the pipe variant is used because `--exclude` is unavailable.

### EC-6: `br dep cycles` or `bv --robot-triage` fail

**Trigger:** The `br` or `bv` binaries are not installed or produce unexpected output.

**Response:** These checks (16 and 17) verify that the bead graph is consistent. If `br` is unavailable, skip checks 16 and 17 and note in completion-evidence.json: "br/bv unavailable — graph health checks skipped." The documentation-only changes cannot introduce dependency cycles or bv alerts, so skipping is safe.

### EC-7: conventions.md size still above 5,300 bytes after UI Design deletion

**Trigger:** Post-deletion size > 5,300 bytes. This would mean the file gained content that the plan didn't account for.

**Response:** Check what's taking space:
```bash
# Identify longest sections
awk '/^## /{section=$0; next} {bytes[section]+=length($0)+1} END{for(s in bytes) print bytes[s], s}' .omp/memory/project/conventions.md | sort -rn | head -10
```
If the Honcho Operating Protocol (lines 180-210 in original, ~1,100 bytes) has grown, consider additional trimming there. But don't cut more than necessary — the primary goal is removing duplication, not hitting an exact byte count. If the file is 5,300–5,500 bytes, accept it. Document the final size in completion-evidence.json.

### EC-8: Multiple bead artifacts in the same session

**Trigger:** Another agent was working on a different bead simultaneously and committed to the same files.

**Response:** Before starting any edit, run `git status --porcelain` to check for uncommitted changes to any of the 5 target files. If any have unstaged changes:
- Read the changed file to understand what was modified
- Adjust the edit's `oldText` to match the actual current file content
- If the change conflicts (e.g., the UI Design section was already deleted), skip that task and document in completion-evidence.json
- Never `git pull` or merge — this is the implementing agent's responsibility to handle, but document the conflict so the reviewer knows

---

## 5. Rollback Plan

If verification fails or the changes need to be reverted:

```bash
# Soft rollback: unstage and restore individual files
git checkout HEAD -- .omp/memory/project/conventions.md
git checkout HEAD -- .omp/memory/project/project.md
git checkout HEAD -- .omp/memory/project/tech-stack.md
git checkout HEAD -- .omp/skills/design-system/SKILL.md
git checkout HEAD -- .omp/AGENTS.md

# Hard rollback: if the commit was already made, revert it
git revert HEAD --no-edit

# Complete reset: if multiple commits happened
git log --oneline -5  # Find the commit hash before this bead's work
git reset --hard <hash>
```

All changes are to text files. No database migrations, no binary artifacts, no side effects. Rollback is a single `git checkout HEAD -- <files>` or `git revert`.

## 6. Dependency Graph

```
Wave 1 (parallel):
  1.1 conventions.md trim ─────┐
  1.2 project.md fix       ────┤── no dependencies between 1.1, 1.2, 1.3
  1.3 tech-stack.md fix    ─────┘

Wave 2 (parallel, depends on Wave 1):
  2.1 SKILL.md absorb      ── depends on 1.1 (needs to know what was removed)
  2.2 AGENTS.md tree        ── depends on 1.1 (but really just needs Wave 1 done)

Wave 3 (sequential):
  3.1 Atomic commit         ── depends on 1.1, 1.2, 1.3, 2.1, 2.2
  3.2 Verification battery  ── depends on 3.1
  3.3 Sync artifacts        ── depends on 3.2
```

Total estimated time: 5+5+5 (Wave 1 parallel) + max(8,4) (Wave 2 parallel) + 2+5+1 (Wave 3 sequential) = 5 + 8 + 8 = 21 minutes utility, 30 minutes forecast (rounds up for context switching).
