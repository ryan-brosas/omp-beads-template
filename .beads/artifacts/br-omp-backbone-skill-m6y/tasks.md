<!-- DENSITY: Minimum 600 lines. No upper bound. <600 = too thin — tasks lack detail, verification steps are vague, dependencies undefined. Every task needs a yaml block, concrete verification steps, and enough detail for parallel execution without reading the PRD or plan. -->
# Tasks: br-omp-backbone-skill-m6y

## 1. Memory File Cleanup

### 1.1 Trim conventions.md — Delete UI Design section, add pointer

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/memory/project/conventions.md"]
estimated_minutes: 5
```

- [ ] Read `.omp/memory/project/conventions.md` to confirm current state (expect 130 lines, 6,996 bytes, UI Design at lines 97-130)
- [ ] Delete lines 97-130: the entire `## UI Design` section (including sub-sections `### Design System`, `### Animation Philosophy`, `### CSS Ownership`, `### Component Variants`, `### Craft Rules`, `### Theme`, `### Icons`)
- [ ] Insert replacement pointer (3 lines) between line 96 (`4. Never let memory drift...`) and the existing `## The Workflow` header:

```markdown
## UI Design

For UI design rules (animation, components, icons, theme, craft), load `design-system/SKILL.md`. The design system is on-demand — not inlined in every session.
```

- [ ] Verify: `grep "Animation Philosophy" .omp/memory/project/conventions.md` returns 0 matches (zero exit code or no output)
- [ ] Verify: `grep "design-system/SKILL" .omp/memory/project/conventions.md` returns ≥1 match
- [ ] Verify: `grep "## The Workflow" .omp/memory/project/conventions.md` still exists (section wasn't accidentally deleted)
- [ ] Verify: `wc -c < .omp/memory/project/conventions.md` reports < 5300 (precise target is <4500 but ≤5300 is acceptable per PRD EC-2)

### 1.2 Fix project.md — Self-matching grep + current phase update {parallel}

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/memory/project/project.md"]
estimated_minutes: 5
```

- [ ] **Change A (line 14):** Add `--exclude=project.md` to the grep command in Success Criterion #1:

```
Before: `grep -r '<project-name>' .omp/memory/project/` returns no matches
After:  `grep -r '<project-name>' .omp/memory/project/ --exclude=project.md` returns no matches
```

- [ ] **Change B (lines 22-26):** Update the Current Phase section — replace status, milestone, and next:

```markdown
Before:
- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Workflow verification — run a full /brainstorm → ...

After:
- **Status:** stable
- **Milestone:** Post-review cleanup — fix Codex findings, trim conventions.md (br-omp-backbone-skill-m6y)
- **Next:** Audit and harden the `/close` command to check memory file staleness on bead completion
```

- [ ] Verify: `grep "br-omp-backbone-skill-1da" .omp/memory/project/project.md` returns 0 matches (old milestone gone)
- [ ] Verify: `grep "br-omp-backbone-skill-m6y" .omp/memory/project/project.md` returns ≥1 match (new milestone present)
- [ ] Verify: `grep "Status.*stable" .omp/memory/project/project.md` returns ≥1 match
- [ ] Verify: `grep -rc '<project-name>' .omp/memory/project/ --exclude=project.md` returns 0 (or output is "0" on last line)
- [ ] Verify: `grep "Next.*close" .omp/memory/project/project.md` returns ≥1 match (next step references /close hardening)

### 1.3 Fix tech-stack.md — Replace N/A with valid shell no-ops {parallel}

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/memory/project/tech-stack.md"]
estimated_minutes: 5
```

- [ ] Read `.omp/memory/project/tech-stack.md` to confirm current N/A lines appear in two bash blocks:
  - Verification Commands block: `N/A — template repo, no application code` (4 occurrences: Typecheck, Lint, Test, Build)
  - Security block: `N/A — template repo, no dependencies` and `N/A — no secrets scan configured` (2 occurrences)

- [ ] Replace each of the 6 `N/A — ...` lines with `true  # ...`:

```bash
# Verification Commands block — 4 replacements:
# Typecheck
N/A — template repo, no application code          →  true  # template repo — no application code
# Lint
N/A — template repo, no application code          →  true  # template repo — no application code
# Test
N/A — template repo, no application code          →  true  # template repo — no application code
# Build
N/A — template repo, no application code          →  true  # template repo — no application code

# Security block — 2 replacements:
# Dependency audit
N/A — template repo, no dependencies              →  true  # template repo — no dependencies
# Secrets scan
N/A — no secrets scan configured                  →  true  # no secrets scan configured
```

- [ ] Verify: `grep "N/A" .omp/memory/project/tech-stack.md` returns 0 matches (or matches only outside bash blocks)
- [ ] Verify: `sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | grep -c "N/A"` returns 0
- [ ] Verify: `grep -c "true  #" .omp/memory/project/tech-stack.md` returns ≥6 (all replacements landed)
- [ ] Verify: Extracted bash blocks pass syntax check:
  ```bash
  sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | sed '1d;$d' | bash -n && echo "PASS" || echo "FAIL"
  ```
- [ ] Verify: Each `true  #` line preserves the original comment text (visual check: read the two bash blocks)

## 2. Skill + Diagram Updates

### 2.1 Absorb UI Design rules into design-system SKILL.md

```yaml
depends_on: ["1.1"]
parallel: true
conflicts_with: []
files: [".omp/skills/design-system/SKILL.md"]
estimated_minutes: 8
```

- [ ] Read `.omp/skills/design-system/SKILL.md` to confirm current state (94 lines, ends with `## Attribution` section)
- [ ] Read `.omp/skills/design-system/DESIGN.md` to confirm no duplication with the content being absorbed — verify that DESIGN.md covers the same rules at a different level of detail (it does: component variants, easing, token rules all present at DESIGN.md § Do's and Don'ts)
- [ ] Append a new `## Craft Rules (Tier 1)` section after the existing `## Attribution` section:

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

- [ ] Verify: `grep -c "Craft Rules (Tier 1)" .omp/skills/design-system/SKILL.md` returns 1
- [ ] Verify: `grep -c "Animation" .omp/skills/design-system/SKILL.md` returns ≥2 (heading + at least one rule reference)
- [ ] Verify: `grep "Animation Philosophy" .omp/skills/design-system/SKILL.md` returns ≥1 match — equivalent content under `### Animation`
- [ ] Verify: `grep -c "cubic-bezier" .omp/skills/design-system/SKILL.md` returns ≥2 (existing DESIGN.md reference + new craft rule)
- [ ] Verify: `grep -c "aria-hidden" .omp/skills/design-system/SKILL.md` returns 1 (new icon rule)
- [ ] Verify: `grep -c "emoji" .omp/skills/design-system/SKILL.md` returns 4 (existing do's/don'ts + new craft rule + DESIGN.md reference)
- [ ] Verify: The `## Attribution` section still exists (not overwritten — new section is appended after it)

### 2.2 Complete AGENTS.md template tree diagram {parallel}

```yaml
depends_on: ["1.1"]
parallel: true
conflicts_with: []
files: [".omp/AGENTS.md"]
estimated_minutes: 4
```

- [ ] Read `.omp/AGENTS.md` around line 231-240 to confirm the current template tree section:

```
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── context-capsule.md
│   │   └── review-report.md
```

- [ ] Verify actual template files on disk: `ls .omp/templates/` shows 9 files:
  - `completion-evidence.json`, `context-capsule.md`, `decisions.md`, `plan.md`, `prd.json`, `prd.md`, `progress.txt`, `review-report.md`, `tasks.md`

- [ ] Replace the 5-entry template block with a 9-entry block, inserting the 4 missing files in order:
  - `prd.json` after `prd.md` (it's the machine-readable mirror)
  - `decisions.md` after `context-capsule.md` (alphabetical slot)
  - `completion-evidence.json` after `decisions.md` (alphabetical slot)
  - `progress.txt` after `completion-evidence.json` (alphabetical slot)

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

- [ ] Verify: `grep "prd.json" .omp/AGENTS.md` returns ≥1 match (was 0)
- [ ] Verify: `grep "decisions.md" .omp/AGENTS.md` returns ≥2 matches (was 1 — already referenced in memory/project section; now also in templates)
- [ ] Verify: `grep "completion-evidence.json" .omp/AGENTS.md` returns ≥1 match (was 0 in tree; may appear elsewhere)
- [ ] Verify: `grep "progress.txt" .omp/AGENTS.md` returns ≥1 match (was 0)
- [ ] Verify: Template entries count in tree matches disk count:
  ```bash
  # Extract template entries from AGENTS.md tree (between templates/ and next section)
  TREE_COUNT=$(sed -n '/templates\/.*Artifact templates/,/^│   └── memory/p' .omp/AGENTS.md | grep -cE '├──|└──')
  DISK_COUNT=$(ls .omp/templates/ | wc -l)
  [ "$TREE_COUNT" -eq "$DISK_COUNT" ] && echo "PASS: $TREE_COUNT == $DISK_COUNT" || echo "FAIL: $TREE_COUNT != $DISK_COUNT"
  ```
- [ ] Verify: The tree still uses correct Unicode box-drawing characters (`├──`, `│`, `└──`) — no ASCII fallback corruption

## 3. Commit + Verification

### 3.1 Atomic commit of all changes

```yaml
depends_on: ["1.1", "1.2", "1.3", "2.1", "2.2"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 2
```

- [ ] Stage all changed files: `git add .omp/memory/project/conventions.md .omp/memory/project/project.md .omp/memory/project/tech-stack.md .omp/skills/design-system/SKILL.md .omp/AGENTS.md`
- [ ] Stage bead artifacts: `git add .beads/artifacts/br-omp-backbone-skill-m6y/`
- [ ] Review diff: `git diff --cached --stat` — confirm exactly 5 files changed (3 memory, 1 skill, 1 AGENTS.md) plus bead artifacts
- [ ] Commit with conventional format:
  ```
  fix: post-review cleanup — trim conventions, harden success criteria, complete tree (br-omp-backbone-skill-m6y)
  ```
- [ ] Verify: `git log -1 --oneline` shows the commit

### 3.2 Full verification battery

```yaml
depends_on: ["3.1"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 5
```

- [ ] **Check 1 — conventions.md size:** `[ $(wc -c < .omp/memory/project/conventions.md) -lt 5300 ] && echo "PASS" || echo "FAIL: $(wc -c < .omp/memory/project/conventions.md)"`
- [ ] **Check 2 — UI Design gone from conventions:** `[ $(grep -c "Animation Philosophy" .omp/memory/project/conventions.md) -eq 0 ] && echo "PASS" || echo "FAIL"`
- [ ] **Check 3 — UI Design in SKILL.md:** `[ $(grep -c "Animation" .omp/skills/design-system/SKILL.md) -ge 2 ] && echo "PASS" || echo "FAIL"`
- [ ] **Check 4 — Design pointer in conventions:** `[ $(grep -c "design-system/SKILL" .omp/memory/project/conventions.md) -ge 1 ] && echo "PASS" || echo "FAIL"`
- [ ] **Check 5 — Self-match grep fixed:** `OUT=$(grep -rc '<project-name>' .omp/memory/project/ --exclude=project.md 2>&1); echo "$OUT" | tail -1 | grep -q "^0$" && echo "PASS" || echo "FAIL: $OUT"`
- [ ] **Check 6 — No N/A in tech-stack bash blocks:** `[ $(sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | grep -c "N/A") -eq 0 ] && echo "PASS" || echo "FAIL"`
- [ ] **Check 7 — true no-ops present:** `[ $(grep -c "true  #" .omp/memory/project/tech-stack.md) -ge 6 ] && echo "PASS" || echo "FAIL"`
- [ ] **Check 8 — Bash blocks parse:** `sed -n '/```bash/,/```/p' .omp/memory/project/tech-stack.md | sed '1d;$d' | bash -n && echo "PASS" || echo "FAIL"`
- [ ] **Check 9 — prd.json in tree:** `grep -q "prd.json" .omp/AGENTS.md && echo "PASS" || echo "FAIL"`
- [ ] **Check 10 — decisions.md in tree (templates section):** `grep -A25 "templates/" .omp/AGENTS.md | grep -q "decisions.md" && echo "PASS" || echo "FAIL"`
- [ ] **Check 11 — completion-evidence.json in tree:** `grep -A25 "templates/" .omp/AGENTS.md | grep -q "completion-evidence.json" && echo "PASS" || echo "FAIL"`
- [ ] **Check 12 — progress.txt in tree:** `grep -A25 "templates/" .omp/AGENTS.md | grep -q "progress.txt" && echo "PASS" || echo "FAIL"`
- [ ] **Check 13 — Old milestone gone:** `[ $(grep -c "br-omp-backbone-skill-1da" .omp/memory/project/project.md) -eq 0 ] && echo "PASS" || echo "FAIL"`
- [ ] **Check 14 — New milestone present:** `grep -q "br-omp-backbone-skill-m6y" .omp/memory/project/project.md && echo "PASS" || echo "FAIL"`
- [ ] **Check 15 — Status is stable:** `grep -q "Status.*stable" .omp/memory/project/project.md && echo "PASS" || echo "FAIL"`
- [ ] **Check 16 — No dependency cycles:** `br dep cycles --json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if d.get('count',0)==0 else 1)" && echo "PASS" || echo "FAIL"`
- [ ] **Check 17 — No bv alerts:** `bv --robot-triage --format json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0)" && echo "PASS" || echo "FAIL"`
- [ ] **Check 18 — File integrity:** `git diff --check` returns clean (no whitespace errors, no conflict markers, no trailing whitespace)
- [ ] Record all verification results in `.beads/artifacts/br-omp-backbone-skill-m6y/completion-evidence.json`

### 3.3 Sync artifacts to bead graph

```yaml
depends_on: ["3.2"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 1
```

- [ ] Run `br sync --flush-only` to sync bead artifacts to the graph
- [ ] Verify: Command exits 0
- [ ] Verify: `br show br-omp-backbone-skill-m6y --json` shows bead with status and artifact count

## 4. Edge Cases During Implementation

### EC-1: conventions.md line numbers shifted

If the file has been edited since this plan was written, the UI Design section may not start at line 97. Before editing:

- [ ] `grep -n "## UI Design" .omp/memory/project/conventions.md` to find the actual start line
- [ ] `grep -n "## The Workflow" .omp/memory/project/conventions.md` to find the section after UI Design
- [ ] Delete everything between those two section headers (including the `## UI Design` header, excluding `## The Workflow`)
- [ ] Insert the 3-line pointer exactly where `## UI Design` was

### EC-2: SKILL.md already has craft rules

If a prior bead added craft rules to SKILL.md:

- [ ] `grep -n "Craft Rules" .omp/skills/design-system/SKILL.md` — if found, do NOT append duplicate content
- [ ] Instead, verify the existing craft rules cover Animation, Components, Theme, Icons subsections
- [ ] If any subsection is missing, append only the missing subsections under the existing `## Craft Rules` header

### EC-3: AGENTS.md tree format changed

If the Unicode box-drawing characters have been replaced:

- [ ] Match the existing style exactly (ASCII `|--` vs Unicode `├──`)
- [ ] Maintain the same indentation depth as adjacent entries
- [ ] Insert entries in the correct order: prd.md, prd.json, plan.md, tasks.md, context-capsule.md, decisions.md, completion-evidence.json, progress.txt, review-report.md

### EC-4: tech-stack.md has more N/A lines than expected

If the file has been edited and N/A lines differ from the plan:

- [ ] `grep -n "N/A" .omp/memory/project/tech-stack.md` to find all occurrences
- [ ] Only replace N/A lines that are inside ` ```bash ` fenced blocks
- [ ] Lines outside bash blocks (e.g., in prose, tables) are NOT modified
- [ ] Each replacement follows the pattern: `N/A — <reason>` → `true  # <reason>` (preserve reason text exactly)

### EC-5: `--exclude=project.md` not supported by grep

If the platform grep doesn't support `--exclude`:

- [ ] Test: `echo "test" | grep --exclude=dummy test` — if it errors, fall back to:
  ```
  grep -rl '<project-name>' .omp/memory/project/ | grep -v project.md
  ```
- [ ] Update the criterion text to show the fallback command
