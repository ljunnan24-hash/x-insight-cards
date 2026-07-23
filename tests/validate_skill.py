#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> None:
    skill = Path(sys.argv[1] if len(sys.argv) > 1 else "skills/x-insight-cards")
    document = skill / "SKILL.md"
    text = document.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise SystemExit("SKILL.md is missing YAML frontmatter")
    frontmatter = match.group(1)
    if not re.search(r"^name: x-insight-cards$", frontmatter, re.MULTILINE):
        raise SystemExit("Invalid skill name")
    description = re.search(r"^description: (.+)$", frontmatter, re.MULTILINE)
    if not description or len(description.group(1)) < 80:
        raise SystemExit("Skill description is too short")
    if "TODO" in text:
        raise SystemExit("SKILL.md still contains TODO markers")
    required = [
        skill / "agents" / "openai.yaml",
        skill / "scripts" / "render_card.py",
        skill / "scripts" / "score_candidates.py",
        skill / "scripts" / "wechat_ilink_delivery.mjs",
        skill / "scripts" / "wechat_ilink_delivery.test.mjs",
        skill / "scripts" / "wechat_ilink_listener.mjs",
        skill / "scripts" / "wechat_ilink_listener.test.mjs",
        skill / "scripts" / "wechat_ilink_listener_service.sh",
        skill / "scripts" / "wechat_main_window_delivery.sh",
        skill / "scripts" / "wechat_main_window_delivery.swift",
        skill / "references" / "workflow.md",
        skill / "references" / "typography.md",
        skill / "references" / "private-delivery.md",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"Missing skill resources: {missing}")
    print(f"Validated {skill}")


if __name__ == "__main__":
    main()
