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
            output = Path(directory) / "card.png"
            metadata = MODULE.render_card(data, output)
            self.assertTrue(output.exists())
            with Image.open(output) as image:
                self.assertEqual(image.width, 1200)
                self.assertGreater(image.height, 600)
            self.assertEqual(metadata["render_method"], "rearranged-render")

    def test_requires_verified_core_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                MODULE.render_card({"author": "A"}, Path(directory) / "card.png")


if __name__ == "__main__":
    unittest.main()
