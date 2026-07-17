#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".txt", ".sh", ""}
FORBIDDEN_PATH_PARTS = {"__pycache__", ".venv", "private", "runs", "daily"}
PATTERNS = {
    "personal absolute path": re.compile(r"/Users/(?!example(?:/|$))[A-Za-z0-9._-]+/"),
    "credential assignment": re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]+"),
    "cookie file": re.compile(r"(?i)cookies?\.json|\.cookie\b"),
}


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    findings: list[str] = []
    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_dir():
            continue
        relative = path.relative_to(root)
        if any(part in FORBIDDEN_PATH_PARTS for part in relative.parts):
            continue
        if relative.as_posix() in {".gitignore", "tests/privacy_check.py"}:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}: {relative}")
    if findings:
        raise SystemExit("Privacy check failed:\n- " + "\n- ".join(sorted(set(findings))))
    print(f"Privacy check passed for {root}")


if __name__ == "__main__":
    main()
