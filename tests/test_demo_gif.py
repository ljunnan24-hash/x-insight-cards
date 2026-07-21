from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build-demo-gif.py"
SPEC = importlib.util.spec_from_file_location("build_demo_gif", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class DemoGifTests(unittest.TestCase):
    def test_builds_complete_workflow_animation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "demo.gif"
            MODULE.build_demo(ROOT / "examples" / "demo-card.png", output)

            self.assertTrue(output.exists())
            with Image.open(output) as image:
                self.assertEqual(image.size, (1280, 720))
                self.assertEqual(image.n_frames, 9)


if __name__ == "__main__":
    unittest.main()
