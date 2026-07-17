from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "x-insight-cards"
    / "scripts"
    / "score_candidates.py"
)
SPEC = importlib.util.spec_from_file_location("score_candidates", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def candidate(identifier: str, score: int, post: str | None = None) -> dict:
    detail = {
        "insight_gain": min(30, score),
        "clarity": min(20, max(0, score - 30)),
        "chinese_social_fit": min(20, max(0, score - 50)),
        "source_credibility": min(15, max(0, score - 70)),
        "freshness": min(10, max(0, score - 85)),
        "visual_readability": min(5, max(0, score - 95)),
    }
    return {
        "id": identifier,
        "url": f"https://x.com/example/status/{identifier}",
        "post": post or f"Synthetic post {identifier}",
        "score_detail": detail,
    }


class ScoringTests(unittest.TestCase):
    def test_selects_high_scores_in_order(self) -> None:
        result = MODULE.rank_candidates(
            [candidate("a", 82), candidate("b", 96), candidate("c", 74)],
            set(),
            set(),
            75,
            5,
        )
        self.assertEqual([item["id"] for item in result["selected"]], ["b", "a"])
        self.assertIn("score_below_75", result["rejected"][0]["reasons"])

    def test_rejects_duplicate_text(self) -> None:
        first = candidate("a", 90, "Same useful idea")
        second = candidate("b", 91, "  same   useful idea ")
        result = MODULE.rank_candidates([first, second], set(), set(), 75, 5)
        self.assertEqual(result["selection_count"], 1)
        self.assertIn("duplicate_text", result["rejected"][0]["reasons"])

    def test_rejects_disallowed_flag(self) -> None:
        item = candidate("a", 90)
        item["flags"] = ["stock_tip"]
        result = MODULE.rank_candidates([item], set(), set(), 75, 5)
        self.assertEqual(result["selection_count"], 0)
        self.assertIn("stock_tip", result["rejected"][0]["reasons"])


if __name__ == "__main__":
    unittest.main()
