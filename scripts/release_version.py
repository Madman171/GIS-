#!/usr/bin/env python3
"""Calculate and apply the next semantic version from Conventional Commits."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
PACKAGE_FILE = ROOT / "frontend" / "package.json"
BACKEND_FILE = ROOT / "backend" / "main.py"
CHANGELOG_FILE = ROOT / "CHANGELOG.md"
VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def parse_version(value: str) -> tuple[int, int, int]:
    match = VERSION_PATTERN.fullmatch(value.strip().lstrip("v"))
    if not match:
        raise ValueError(f"Invalid semantic version: {value}")
    return tuple(int(part) for part in match.groups())


def latest_tag() -> str | None:
    try:
        return subprocess.check_output(
            ("git", "describe", "--tags", "--match", "v*", "--abbrev=0"),
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return None


def commits_since(tag: str | None) -> list[str]:
    revision = f"{tag}..HEAD" if tag else "HEAD"
    output = run("git", "log", revision, "--pretty=%s")
    return [line for line in output.splitlines() if line.strip()]


def bump_kind(commits: list[str]) -> str | None:
    if any(
        "BREAKING CHANGE" in commit or re.match(r"^[a-z]+!\s*[:(]", commit)
        for commit in commits
    ):
        return "major"
    if any(re.match(r"^feat(?:\([^)]*\))?\s*:", commit) for commit in commits):
        return "minor"
    if any(
        re.match(r"^(?:fix|perf|revert)(?:\([^)]*\))?\s*:", commit)
        for commit in commits
    ):
        return "patch"
    return None


def next_version(current: tuple[int, int, int], kind: str) -> tuple[int, int, int]:
    major, minor, patch = current
    if kind == "major":
        return major + 1, 0, 0
    if kind == "minor":
        return major, minor + 1, 0
    return major, minor, patch + 1


def format_version(value: tuple[int, int, int]) -> str:
    return ".".join(str(part) for part in value)


def apply_version(version: str, commits: list[str]) -> None:
    VERSION_FILE.write_text(f"{version}\n", encoding="utf-8")

    package = json.loads(PACKAGE_FILE.read_text(encoding="utf-8"))
    package["version"] = version
    package["releaseVersion"] = f"v{version}"
    PACKAGE_FILE.write_text(
        json.dumps(package, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    backend = BACKEND_FILE.read_text(encoding="utf-8")
    backend, count = re.subn(
        r'(app = FastAPI\(\s*title=.*?\n\s*version=)["\'][^"\']+["\']',
        rf'\g<1>"{version}"',
        backend,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        raise RuntimeError("Could not update backend FastAPI version")
    BACKEND_FILE.write_text(backend, encoding="utf-8")

    existing = CHANGELOG_FILE.read_text(encoding="utf-8")
    grouped = "\n".join(f"- {commit}" for commit in reversed(commits))
    entry = f"## [{version}] - {date.today().isoformat()}\n\n{grouped}\n\n"
    marker = "## ["
    insertion = existing.find(marker)
    if insertion < 0:
        existing = existing.rstrip() + "\n\n" + entry
    else:
        existing = existing[:insertion] + entry + existing[insertion:]
    CHANGELOG_FILE.write_text(existing, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    current = parse_version(VERSION_FILE.read_text(encoding="utf-8"))
    tag = latest_tag()
    commits = commits_since(tag)
    kind = bump_kind(commits)
    if kind is None:
        print("NO_RELEASE")
        return 0
    version = format_version(next_version(current, kind))
    print(version)
    if args.apply:
        apply_version(version, commits)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
