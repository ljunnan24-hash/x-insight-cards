from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "x-insight-cards" / "scripts" / "render_card.py"
SPEC = importlib.util.spec_from_file_location("render_card", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class RendererTests(unittest.TestCase):
    def test_renders_demo_png(self) -> None:
        data = json.loads((ROOT / "examples" / "demo-post.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            avatar = Path(directory) / "avatar.png"
            Image.new("RGB", (200, 200), "#2463EB").save(avatar)
            data["avatar"] = str(avatar)
            data.pop("avatar_url", None)
            output = Path(directory) / "card.png"
            metadata = MODULE.render_card(data, output)
            self.assertTrue(output.exists())
            with Image.open(output) as image:
                self.assertEqual(image.width, 1200)
                self.assertGreater(image.height, 600)
            self.assertEqual(metadata["render_method"], "rearranged-render")
            self.assertEqual(metadata["content_mode"], "bilingual")
            self.assertTrue(metadata["source_text_visible"])
            self.assertLessEqual(metadata["bilingual_height_estimate"], 1200)

    def test_requires_verified_core_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                MODULE.render_card({"author": "A"}, Path(directory) / "card.png")

    def test_rejects_missing_real_avatar(self) -> None:
        data = {
            "author": "Example Author",
            "handle": "@example",
            "post": "A useful idea.",
            "translation": "一个有用的观点。",
        }
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "Real author avatar is required"):
                MODULE.render_card(data, Path(directory) / "card.png")

    def test_rejects_untrusted_avatar_url(self) -> None:
        data = {
            "author": "Example Author",
            "handle": "@example",
            "avatar_url": "https://example.com/avatar.jpg",
            "post": "A useful idea.",
            "translation": "一个有用的观点。",
        }
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "Untrusted avatar URL"):
                MODULE.render_card(data, Path(directory) / "card.png")

    def test_auto_switches_long_posts_to_translation_only(self) -> None:
        data = {
            "author": "Example Author",
            "handle": "@example",
            "post": " ".join(["A long verified English source sentence."] * 90),
            "translation": "这是一段忠实而简洁的中文译文。\n\n它保留原帖的核心结构。",
            "date_display": "2026年8月28日",
            "views_display": "1万 次查看",
        }
        with tempfile.TemporaryDirectory() as directory:
            avatar = Path(directory) / "avatar.png"
            Image.new("RGB", (200, 200), "#2463EB").save(avatar)
            data["avatar"] = str(avatar)
            output = Path(directory) / "card.png"
            metadata = MODULE.render_card(data, output)
            self.assertEqual(metadata["content_mode"], "translation-only")
            self.assertFalse(metadata["source_text_visible"])
            self.assertGreater(metadata["bilingual_height_estimate"], 1200)
            self.assertLess(metadata["height"], metadata["bilingual_height_estimate"])

    def test_rejects_unknown_render_mode(self) -> None:
        data = {
            "author": "Example Author",
            "handle": "@example",
            "post": "A useful idea.",
            "translation": "一个有用的观点。",
            "render_mode": "compact",
        }
        with tempfile.TemporaryDirectory() as directory:
            avatar = Path(directory) / "avatar.png"
            Image.new("RGB", (200, 200), "#2463EB").save(avatar)
            data["avatar"] = str(avatar)
            with self.assertRaisesRegex(ValueError, "render_mode must be"):
                MODULE.render_card(data, Path(directory) / "card.png")


if __name__ == "__main__":
    unittest.main()
