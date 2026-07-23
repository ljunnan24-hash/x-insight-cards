from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "skills"
    / "x-insight-cards"
    / "scripts"
    / "wechat_ilink_listener_service.sh"
)


class WeChatListenerServiceTests(unittest.TestCase):
    def test_shell_syntax_and_fixed_service_label(self) -> None:
        subprocess.run(["bash", "-n", str(SOURCE)], check=True)
        text = SOURCE.read_text(encoding="utf-8")
        self.assertIn('LABEL="com.x-insight-cards.wechat-listener"', text)
        self.assertIn("<key>KeepAlive</key>", text)
        self.assertIn("<key>RunAtLoad</key>", text)
        self.assertNotIn("--recipient", text)
        self.assertNotIn("bot_token", text)

    @unittest.skipUnless(
        sys.platform == "darwin" and shutil.which("node"),
        "launchd dry-run validation requires macOS and Node.js",
    )
    def test_dry_run_renders_private_fixed_arguments_without_installing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            config = home / ".weclaw" / "x-insight-cards-delivery.json"
            history = home / "review" / "history.jsonl"
            config.parent.mkdir(parents=True, mode=0o700)
            history.parent.mkdir(parents=True)
            config.write_text("{}\n", encoding="utf-8")
            history.write_text("{}\n", encoding="utf-8")
            config.chmod(0o600)
            environment = dict(os.environ)
            environment["HOME"] = str(home)
            result = subprocess.run(
                [
                    str(SOURCE),
                    "install",
                    "--dry-run",
                    "--config",
                    str(config),
                    "--history",
                    str(history),
                ],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )

            self.assertIn("com.x-insight-cards.wechat-listener", result.stdout)
            self.assertIn(str(config), result.stdout)
            self.assertIn(str(history), result.stdout)
            self.assertIn("wechat_ilink_listener.mjs", result.stdout)
            self.assertFalse((home / "Library" / "LaunchAgents").exists())


if __name__ == "__main__":
    unittest.main()
