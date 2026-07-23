from __future__ import annotations

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
    / "wechat_main_window_delivery.swift"
)


class WeChatDeliveryTests(unittest.TestCase):
    def test_destination_is_fixed_and_fail_closed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8")
        self.assertIn('targetConversation = "文件传输助手"', text)
        self.assertIn("STOPPED_WITHOUT_UNVERIFIED_SEND", text)
        self.assertIn("DELIVERED_FOR_REVIEW", text)
        self.assertNotIn("--target", text)
        self.assertNotIn(".terminate()", text)

    def test_uses_capture_and_ocr_verification(self) -> None:
        text = SOURCE.read_text(encoding="utf-8")
        self.assertIn("AVCaptureScreenInput", text)
        self.assertIn("VNRecognizeTextRequest", text)
        self.assertIn("headerIsVerified", text)
        self.assertIn("messageInputContainsImage", text)

    def test_wrong_chat_safety_is_fail_closed(self) -> None:
        text = SOURCE.read_text(encoding="utf-8")
        self.assertIn("minimumOCRConfidence: Float = 0.80", text)
        self.assertIn("regionOfInterest: chatHeaderRegion", text)
        self.assertIn("listTargets.count == 1", text)
        self.assertIn("targetRowIsSelected", text)
        self.assertIn("stableVerificationSamples = 2", text)
        self.assertIn("requireSameFrontmostWeChatWindow", text)
        self.assertIn("requireNoPhysicalInput", text)
        self.assertIn("CGEventSource(stateID: .privateState)", text)
        self.assertIn("ProcessLock", text)
        self.assertIn("sendReturnAfterStableTarget", text)
        self.assertIn("pasteAfterStableTarget", text)
        self.assertEqual(text.count("postKey(36)"), 1)
        self.assertEqual(text.count("commandKey(9)"), 1)
        self.assertNotIn("clearMessageInput(window:", text)

    @unittest.skipUnless(
        sys.platform == "darwin" and shutil.which("swiftc"),
        "Swift macOS frameworks are only available on macOS",
    )
    def test_helper_compiles_on_macos(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "wechat-main-window-delivery"
            subprocess.run(
                [
                    "swiftc",
                    "-parse-as-library",
                    str(SOURCE),
                    "-o",
                    str(binary),
                    "-framework",
                    "AppKit",
                    "-framework",
                    "AVFoundation",
                    "-framework",
                    "CoreImage",
                    "-framework",
                    "CoreMedia",
                    "-framework",
                    "Vision",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(binary.exists())


if __name__ == "__main__":
    unittest.main()
