#!/usr/bin/env python3
"""Lint a Cowork business folder against the standard (standard/SPEC.md).

Usage:
    python tools/lint.py folders/core/business-os
    python tools/lint.py folders/**/            # lint everything (shell-expanded)
    python tools/lint.py --all                  # lint every folder under folders/

Exit code is non-zero if any folder fails. No dependencies beyond PyYAML.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = {"core", "finance", "growth", "operations", "people", "professional", "commerce"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")

REQUIRED_FILES = ["folder.yaml", "CLAUDE.md", "README.md", "setup.md", "connectors.md"]
REQUIRED_MEMORY = ["memory/profile.md", "memory/decisions.md", "memory/people.md"]


class Linter:
    def __init__(self, folder: Path):
        self.folder = folder
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def _exists(self, rel: str) -> bool:
        return (self.folder / rel).exists()

    def _nonempty(self, rel: str) -> bool:
        p = self.folder / rel
        return p.is_file() and p.stat().st_size > 0

    def run(self) -> bool:
        if not self.folder.is_dir():
            self.err(f"not a directory: {self.folder}")
            return False

        for rel in REQUIRED_FILES:
            if not self._exists(rel):
                self.err(f"missing required file: {rel}")
            elif not self._nonempty(rel):
                self.err(f"required file is empty: {rel}")

        manifest = self._load_manifest()
        if manifest is not None:
            self._check_manifest(manifest)

        self._check_claude_md()
        self._check_skills(manifest)
        self._check_schedules(manifest)
        self._check_memory()

        if not self._exists("reports"):
            self.err("missing required directory: reports/")

        return not self.errors

    def _load_manifest(self) -> dict | None:
        p = self.folder / "folder.yaml"
        if not p.is_file():
            return None
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            self.err(f"folder.yaml is not valid YAML: {e}")
            return None
        if not isinstance(data, dict):
            self.err("folder.yaml must be a mapping")
            return None
        return data

    def _check_manifest(self, m: dict) -> None:
        required = ["slug", "name", "category", "version", "summary",
                    "same_day_win", "connectors", "skills", "schedules"]
        for key in required:
            if key not in m:
                self.err(f"folder.yaml missing required key: {key}")

        slug = m.get("slug")
        if slug and not SLUG_RE.match(str(slug)):
            self.err(f"folder.yaml slug not kebab-case: {slug!r}")
        if slug and slug != self.folder.name:
            self.err(f"folder.yaml slug {slug!r} != directory name {self.folder.name!r}")

        cat = m.get("category")
        if cat and cat not in CATEGORIES:
            self.err(f"folder.yaml category {cat!r} not one of {sorted(CATEGORIES)}")

        ver = m.get("version")
        if ver and not SEMVER_RE.match(str(ver)):
            self.err(f"folder.yaml version {ver!r} is not semver (x.y.z)")

        for conn in m.get("connectors", []) or []:
            if not isinstance(conn, dict) or not {"name", "required", "why"} <= conn.keys():
                self.err(f"connector entry needs name/required/why: {conn!r}")

        skills = m.get("skills") or []
        if isinstance(skills, list) and len(skills) < 1:
            self.err("folder.yaml must declare at least one skill")
        schedules = m.get("schedules") or []
        if isinstance(schedules, list) and len(schedules) < 1:
            self.err("folder.yaml must declare at least one schedule")

    def _check_claude_md(self) -> None:
        p = self.folder / "CLAUDE.md"
        if not p.is_file():
            return
        text = p.read_text(encoding="utf-8").lower()
        if "hard rule" not in text:
            self.err("CLAUDE.md must contain a 'Hard rules' section")
        if "memory/" not in text and "memory" not in text:
            self.warn("CLAUDE.md should point to memory/ as the source of truth")

    def _check_skills(self, m: dict | None) -> None:
        skills_dir = self.folder / "skills"
        if not skills_dir.is_dir():
            self.err("missing required directory: skills/")
            return
        on_disk = {d.name for d in skills_dir.iterdir()
                   if d.is_dir() and (d / "SKILL.md").is_file()}
        if not on_disk:
            self.err("skills/ must contain at least one <slug>/SKILL.md")
        if m:
            for s in m.get("skills", []) or []:
                slug = s.get("slug") if isinstance(s, dict) else None
                if slug and slug not in on_disk:
                    self.err(f"skill {slug!r} in folder.yaml has no skills/{slug}/SKILL.md")

    def _check_schedules(self, m: dict | None) -> None:
        sched_dir = self.folder / "schedules"
        if not sched_dir.is_dir():
            self.err("missing required directory: schedules/")
            return
        on_disk = {p.stem for p in sched_dir.glob("*.md")}
        if not on_disk:
            self.err("schedules/ must contain at least one <slug>.md")
        if m:
            for s in m.get("schedules", []) or []:
                slug = s.get("slug") if isinstance(s, dict) else None
                if slug and slug not in on_disk:
                    self.err(f"schedule {slug!r} in folder.yaml has no schedules/{slug}.md")

    def _check_memory(self) -> None:
        for rel in REQUIRED_MEMORY:
            if not self._exists(rel):
                self.err(f"missing required memory stub: {rel}")
        if not (self.folder / "memory" / "logs").is_dir():
            self.err("missing required directory: memory/logs/")


def discover_folders(args: list[str]) -> list[Path]:
    if args == ["--all"]:
        base = REPO_ROOT / "folders"
        return sorted(p.parent for p in base.rglob("folder.yaml"))
    # Path.resolve() handles both relative (against cwd) and absolute paths.
    return [Path(a).resolve() for a in args]


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    folders = discover_folders(argv)
    if not folders:
        print("no folders to lint")
        return 2

    failed = 0
    for folder in folders:
        linter = Linter(folder)
        ok = linter.run()
        rel = folder.name
        if ok and not linter.warnings:
            print(f"✅ {rel}")
        elif ok:
            print(f"✅ {rel}  ({len(linter.warnings)} warning(s))")
            for w in linter.warnings:
                print(f"   ⚠️  {w}")
        else:
            failed += 1
            print(f"❌ {rel}")
            for e in linter.errors:
                print(f"   ✗ {e}")
            for w in linter.warnings:
                print(f"   ⚠️  {w}")

    print()
    total = len(folders)
    print(f"{total - failed}/{total} folder(s) passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
