#!/usr/bin/env python3
"""Hydrate .omp/memory/project/ files with detected repo metadata.

Idempotent: only replaces known template placeholders. Already-edited fields
are left alone. Run after `br init` and before Honcho config.

Usage: python3 .omp/scripts/hydrate-memory.py
"""
from __future__ import annotations

from pathlib import Path
import json
import os
import re
import subprocess

root = Path.cwd()
memory_dir = root / ".omp" / "memory" / "project"
summary = {"hydrated": 0, "already_populated": 0, "missing": 0, "files": []}


def read_text(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def write_text_if_changed(path: Path, before: str, after: str) -> None:
    if not path.exists():
        summary["missing"] += 1
        summary["files"].append(f"- {path.name}: missing")
        return
    if after != before:
        path.write_text(after)
        summary["hydrated"] += 1
        summary["files"].append(f"✓ {path.name}: hydrated")
    else:
        summary["already_populated"] += 1
        summary["files"].append(f"- {path.name}: already populated")


def replace_exact(text: str, old: str, new: str) -> str:
    return text.replace(old, new) if old in text else text


def first_heading_from_readme() -> str | None:
    for name in ("README.md", "Readme.md", "README.MD"):
        path = root / name
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            if line.startswith("# "):
                heading = line[2:].strip()
                heading = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", heading)
                return heading or None
    return None


def first_paragraph_from_readme() -> str | None:
    for name in ("README.md", "Readme.md", "README.MD"):
        path = root / name
        if not path.exists():
            continue
        after_h1 = False
        paragraph: list[str] = []
        for raw in path.read_text().splitlines():
            line = raw.strip()
            if not after_h1:
                if line.startswith("# "):
                    after_h1 = True
                continue
            if not line:
                if paragraph:
                    break
                continue
            if line.startswith("#"):
                if paragraph:
                    break
                continue
            if line.startswith("[!") or line.startswith("<img") or line.startswith("!["):
                if paragraph:
                    break
                continue
            paragraph.append(line)
        if paragraph:
            return " ".join(paragraph)
    return None


def parse_package_json() -> dict:
    path = root / "package.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def parse_simple_toml_value(path: Path, keys: list[tuple[str, ...]]) -> str | None:
    if not path.exists():
        return None
    text = path.read_text()
    current_section: tuple[str, ...] = ()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        section = re.match(r"\[(.+)\]", line)
        if section:
            current_section = tuple(part.strip() for part in section.group(1).split("."))
            continue
        match = re.match(r'([A-Za-z0-9_-]+)\s*=\s*["\']([^"\']+)["\']', line)
        if not match:
            continue
        key, value = match.groups()
        for target in keys:
            if current_section == target[:-1] and key == target[-1]:
                return value.strip()
    return None


def git_remote_name() -> str | None:
    try:
        remote = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            cwd=root,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return None
    remote = remote.rstrip("/")
    remote = remote[:-4] if remote.endswith(".git") else remote
    if ":" in remote and "/" not in remote.split(":", 1)[0]:
        remote = remote.split(":", 1)[1]
    name = remote.rsplit("/", 1)[-1].strip()
    return name or None


package_json = parse_package_json()
package_name = package_json.get("name") if isinstance(package_json.get("name"), str) else None


def has_package_dependency(name: str) -> bool:
    for section in ("dependencies", "devDependencies", "peerDependencies"):
        deps = package_json.get(section)
        if isinstance(deps, dict) and name in deps:
            return True
    return False


project_name = (
    git_remote_name()
    or package_name
    or first_heading_from_readme()
    or root.name
    or "Untitled Project"
)
project_desc = first_paragraph_from_readme() or "<!-- TODO: fill in your project goal -->"

has_package = (root / "package.json").exists()
has_tsconfig = (root / "tsconfig.json").exists()
has_cargo = (root / "Cargo.toml").exists()
has_go = (root / "go.mod").exists()
has_pyproject = (root / "pyproject.toml").exists()
has_setup_py = (root / "setup.py").exists()
has_requirements = (root / "requirements.txt").exists()
has_deno = (root / "deno.json").exists() or (root / "deno.jsonc").exists()
has_bun = (root / "bun.lockb").exists() or (root / "bun.lock").exists()

package_manager = "<unknown>"
if (root / "pnpm-lock.yaml").exists():
    package_manager = "pnpm"
elif (root / "yarn.lock").exists():
    package_manager = "yarn"
elif has_bun:
    package_manager = "bun"
elif (root / "package-lock.json").exists():
    package_manager = "npm"
elif (root / "Cargo.lock").exists() or has_cargo:
    package_manager = "cargo"
elif (root / "go.sum").exists() or has_go:
    package_manager = "go mod"
elif (root / "poetry.lock").exists():
    package_manager = "poetry"
elif (root / "Pipfile.lock").exists():
    package_manager = "pipenv"
elif has_pyproject or has_requirements or has_setup_py:
    package_manager = "pip"

language = "<unknown>"
if has_package:
    ts_version = None
    for section in ("devDependencies", "dependencies", "peerDependencies"):
        deps = package_json.get(section)
        if isinstance(deps, dict) and isinstance(deps.get("typescript"), str):
            ts_version = deps["typescript"]
            break
    if has_tsconfig or ts_version:
        language = "TypeScript"
    else:
        language = "JavaScript"
elif has_cargo:
    language = "Rust"
elif has_go:
    language = "Go"
elif has_pyproject or has_requirements or has_setup_py:
    language = "Python"

runtime = "<unknown>"
if has_package:
    if has_bun:
        runtime = "Bun"
    elif has_deno:
        runtime = "Deno"
    else:
        runtime = "Node.js"
elif has_cargo:
    runtime = "Rust"
elif has_go:
    runtime = "Go"
elif has_pyproject or has_requirements or has_setup_py:
    runtime = "Python 3.x"

language_version = "<unknown>"
if language == "TypeScript":
    for section in ("devDependencies", "dependencies", "peerDependencies"):
        deps = package_json.get(section)
        if isinstance(deps, dict) and isinstance(deps.get("typescript"), str):
            language_version = deps["typescript"]
            break
elif language == "JavaScript":
    language_version = "ES202x"
elif language == "Go":
    if has_go:
        match = re.search(r"^go\s+([0-9.]+)", (root / "go.mod").read_text(), re.M)
        if match:
            language_version = match.group(1)
elif language == "Python":
    language_version = (
        parse_simple_toml_value(root / "pyproject.toml", [("project", "requires-python"), ("tool", "poetry", "dependencies", "python")])
        or "3.x"
    )
elif language == "Rust":
    language_version = parse_simple_toml_value(root / "Cargo.toml", [("package", "edition")]) or "<unknown>"

runtime_version = "<unknown>"
if runtime in {"Node.js", "Bun", "Deno"}:
    for candidate in (".nvmrc", ".node-version"):
        path = root / candidate
        if path.exists():
            runtime_version = path.read_text().strip() or "<unknown>"
            break
elif runtime == "Go" and has_go:
    match = re.search(r"^go\s+([0-9.]+)", (root / "go.mod").read_text(), re.M)
    if match:
        runtime_version = match.group(1)
elif runtime == "Python 3.x":
    runtime_version = language_version
elif runtime == "Rust":
    runtime_version = parse_simple_toml_value(root / "Cargo.toml", [("package", "edition")]) or "<unknown>"

package_manager_version = "<unknown>"

scripts = package_json.get("scripts") if isinstance(package_json.get("scripts"), dict) else {}
pm_runner = {
    "npm": "npm run",
    "pnpm": "pnpm",
    "yarn": "yarn",
    "bun": "bun run",
}.get(package_manager, "npm run")


def package_script(name: str, fallback: str) -> str:
    if name in scripts:
        return f"{pm_runner} {name}" if pm_runner != "yarn" else f"yarn {name}"
    return fallback


def line_or_todo(value: str) -> str:
    return value if value and value != "<unknown>" else "<!-- TODO: fill in -->"

backend_notes = {
    "TypeScript": "strict mode if configured; capture tsconfig constraints",
    "JavaScript": "document runtime constraints and module format",
    "Python": "document typing, packaging, and virtualenv expectations",
    "Go": "document module boundaries and interface conventions",
    "Rust": "document edition, async runtime, and unsafe policy",
}.get(language, "<!-- TODO: fill in -->")
frontend_frameworks = ("react", "svelte", "vue", "next", "nuxt", "astro", "angular", "solid")
has_frontend_framework = any(has_package_dependency(name) for name in frontend_frameworks)
if has_frontend_framework:
    frontend_language = "TypeScript" if language == "TypeScript" else "JavaScript"
    frontend_notes = "detected frontend framework; document actual framework conventions"
else:
    frontend_language = "<!-- TODO: fill in -->"
    frontend_notes = "<!-- TODO: fill in -->"
has_typescript_script_runner = has_package_dependency("tsx") or has_package_dependency("ts-node")
if has_typescript_script_runner:
    scripts_language = "TypeScript"
    scripts_notes = "package scripts and repo automation"
else:
    scripts_language = "Bash"
    scripts_notes = "<!-- TODO: fill in -->"

verification_typecheck = {
    "TypeScript": package_script("typecheck", "npx tsc --noEmit"),
    "JavaScript": "<!-- TODO: fill in -->",
    "Python": package_script("typecheck", "python3 -m mypy ."),
    "Go": "go vet ./...",
    "Rust": "cargo check",
}.get(language, "<!-- TODO: fill in -->")
verification_lint = {
    "TypeScript": package_script("lint", f"{pm_runner} lint" if package_manager != "yarn" else "yarn lint"),
    "JavaScript": package_script("lint", f"{pm_runner} lint" if package_manager != "yarn" else "yarn lint"),
    "Python": package_script("lint", "python3 -m ruff check ."),
    "Go": "golangci-lint run",
    "Rust": "cargo clippy --all-targets --all-features -- -D warnings",
}.get(language, "<!-- TODO: fill in -->")
verification_test = {
    "TypeScript": package_script("test", f"{pm_runner} test" if package_manager != "yarn" else "yarn test"),
    "JavaScript": package_script("test", f"{pm_runner} test" if package_manager != "yarn" else "yarn test"),
    "Python": package_script("test", "pytest"),
    "Go": "go test ./...",
    "Rust": "cargo test",
}.get(language, "<!-- TODO: fill in -->")
verification_build = {
    "TypeScript": package_script("build", f"{pm_runner} build" if package_manager != "yarn" else "yarn build"),
    "JavaScript": package_script("build", f"{pm_runner} build" if package_manager != "yarn" else "yarn build"),
    "Python": package_script("build", "python3 -m pip install -e ."),
    "Go": "go build ./...",
    "Rust": "cargo build --release",
}.get(language, "<!-- TODO: fill in -->")
security_audit = {
    "pnpm": "pnpm audit",
    "yarn": "yarn audit",
    "bun": "bun audit",
    "npm": "npm audit",
    "pip": "python3 -m pip-audit",
    "poetry": "poetry run pip-audit",
    "pipenv": "pipenv run pip-audit",
    "cargo": "cargo audit",
    "go mod": "govulncheck ./...",
}.get(package_manager, "<!-- TODO: fill in -->")

# project.md
project_path = memory_dir / "project.md"
project_before = read_text(project_path)
project_after = project_before
project_after = replace_exact(project_after, "# Project: <project-name>", f"# Project: {project_name}")
project_after = replace_exact(project_after, "<One sentence — what are we building and why?>", project_desc)
project_after = replace_exact(project_after, "<Criterion 1>", "<!-- TODO: fill in criterion 1 -->")
project_after = replace_exact(project_after, "<Criterion 2>", "<!-- TODO: fill in criterion 2 -->")
project_after = replace_exact(project_after, "<Criterion 3>", "<!-- TODO: fill in criterion 3 -->")
project_after = replace_exact(project_after, "<measurable outcome>", "<!-- TODO: fill in measurable outcome -->")
project_after = replace_exact(project_after, "<active | maintenance | paused>", "active")
project_after = replace_exact(project_after, "<what we're working toward right now>", "<!-- TODO: fill in current milestone -->")
project_after = replace_exact(project_after, "<the next concrete deliverable>", "<!-- TODO: fill in next deliverable -->")
write_text_if_changed(project_path, project_before, project_after)

# conventions.md
conventions_path = memory_dir / "conventions.md"
conventions_before = read_text(conventions_path)
conventions_after = conventions_before
conventions_after = replace_exact(conventions_after, "# Conventions: <project-name>", f"# Conventions: {project_name}")
conventions_after = replace_exact(
    conventions_after,
    "| Backend | <TypeScript | Go | Rust | Python> | <strict? Bun? Deno?> |",
    f"| Backend | {line_or_todo(language)} | {backend_notes} |",
)
conventions_after = replace_exact(
    conventions_after,
    "| Frontend | <TypeScript | JavaScript> | <React? Svelte? plain?> |",
    f"| Frontend | {frontend_language} | {frontend_notes} |",
)
conventions_after = replace_exact(
    conventions_after,
    "| Scripts | <Bash | Python | TypeScript> | <CI, dev tooling, one-offs> |",
    f"| Scripts | {scripts_language} | {scripts_notes} |",
)
write_text_if_changed(conventions_path, conventions_before, conventions_after)

# tech-stack.md
tech_path = memory_dir / "tech-stack.md"
tech_before = read_text(tech_path)
tech_after = tech_before
tech_after = replace_exact(tech_after, "# Tech Stack: <project-name>", f"# Tech Stack: {project_name}")
tech_after = replace_exact(
    tech_after,
    "| Language | <TypeScript \\| Python \\| Go \\| Rust> | <version> | <strict mode? async? experimental flags?> |",
    f"| Language | {language} | {language_version} | {backend_notes if backend_notes != '<!-- TODO: fill in -->' else '<!-- TODO: fill in -->'} |",
)
tech_after = replace_exact(
    tech_after,
    "| Runtime | <Node.js \\| Bun \\| Deno \\| Python 3.x \\| Go 1.x> | <version> | <LTS? latest?> |",
    f"| Runtime | {runtime} | {runtime_version} | {'repo-managed runtime' if runtime != '<unknown>' else '<unknown>'} |",
)
tech_after = replace_exact(
    tech_after,
    "| Package manager | <npm \\| pnpm \\| yarn \\| pip \\| cargo \\| go mod> | <version> | |",
    f"| Package manager | {package_manager} | {package_manager_version} | |",
)
tech_after = replace_exact(tech_after, "<name>", "<!-- TODO: fill in -->")
tech_after = replace_exact(tech_after, "<what it does>", "<!-- TODO: fill in -->")
tech_after = replace_exact(tech_after, "<version>", "<unknown>")
tech_after = replace_exact(tech_after, "<tsc --noEmit | mypy | cargo check | go vet>", verification_typecheck)
tech_after = replace_exact(tech_after, "<eslint | ruff | clippy | golangci-lint>", verification_lint)
tech_after = replace_exact(tech_after, "<vitest run | pytest | cargo test | go test ./...>", verification_test)
tech_after = replace_exact(tech_after, "<tsup | pip install -e . | cargo build --release | go build>", verification_build)
tech_after = replace_exact(tech_after, "<npm audit | pip-audit | cargo audit | govulncheck>", security_audit)
tech_after = replace_exact(tech_after, "<gitleaks detect | trufflehog filesystem .>", "<!-- TODO: fill in -->")
write_text_if_changed(tech_path, tech_before, tech_after)

# gotchas.md
for name in ("gotchas.md", "decisions.md"):
    path = memory_dir / name
    before = read_text(path)
    after = before
    heading = "Gotchas" if name == "gotchas.md" else "Decisions"
    after = replace_exact(after, f"# {heading}: <project-name>", f"# {heading}: {project_name}")
    write_text_if_changed(path, before, after)

print("Memory hydration summary:")
for line in summary["files"]:
    print(f"  {line}")
print(
    f"Counts: hydrated={summary['hydrated']} already_populated={summary['already_populated']} missing={summary['missing']}"
)
