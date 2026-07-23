from __future__ import annotations

import importlib.util
import json
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
                self.assertEqual(image.n_frames, 8)
                durations = []
                for frame_index in range(image.n_frames):
                    image.seek(frame_index)
                    durations.append(image.info["duration"])
                self.assertEqual(sum(durations), 13000)

    def test_requires_a_public_x_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory) / "demo.json"
            data.write_text('{"source_url": ""}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "public X source_url"):
                MODULE.build_demo(
                    ROOT / "examples" / "demo-card.png",
                    Path(directory) / "demo.gif",
                    data,
                )

    def test_demo_score_is_auditable(self) -> None:
        data = json.loads((ROOT / "examples" / "demo-post.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(data["score_detail"].values()), 86)
        self.assertEqual(data["source_url"], "https://x.com/JamesClear/status/2045205241885323635")

    def test_final_scene_uses_the_phone_triggered_robot_route(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("发今日素材", text)
        self.assertIn("素材审核机器人", text)
        self.assertIn("收件人已固定", text)
        self.assertNotIn("文件传输助手", text)

    def test_bilingual_readmes_include_complete_listener_onboarding(self) -> None:
        for name in ("README.md", "README.zh-CN.md"):
            with self.subTest(name=name):
                text = (ROOT / name).read_text(encoding="utf-8")
                self.assertIn("weclaw login", text)
                self.assertIn("绑定素材助手", text)
                self.assertIn("wechat_ilink_listener_service.sh", text)
                self.assertIn("--history \"$HOME/Documents/x-insight-cards/history.jsonl\"", text)
                self.assertIn("发今日素材", text)


if __name__ == "__main__":
    unittest.main()
