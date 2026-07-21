#!/usr/bin/env python3
"""Build the README workflow demo GIF from the repository's real demo card."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "skills" / "x-insight-cards" / "scripts" / "render_card.py"
SPEC = importlib.util.spec_from_file_location("xic_render_card", RENDERER)
RENDER_MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(RENDER_MODULE)

WIDTH = 1280
HEIGHT = 720
BACKGROUND = "#09111F"
SURFACE = "#111C2E"
SURFACE_LIGHT = "#18263C"
INK = "#F8FAFC"
MUTED = "#9FB0C8"
ACCENT = "#35C2FF"
ACCENT_GREEN = "#4ADE80"


def font(spec: tuple[str, int], size: int) -> ImageFont.FreeTypeFont:
    return RENDER_MODULE.load_font(spec, size)


def base_frame() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.ellipse((-190, -260, 500, 430), fill="#102B45")
    draw.ellipse((930, 430, 1510, 1010), fill="#17243B")
    draw.rounded_rectangle((34, 28, WIDTH - 34, HEIGHT - 28), 30, outline="#21324A", width=2)
    return image, draw


def header(
    draw: ImageDraw.ImageDraw,
    regular: ImageFont.FreeTypeFont,
    bold: ImageFont.FreeTypeFont,
) -> None:
    draw.rounded_rectangle((60, 50, 100, 90), 12, fill=ACCENT)
    draw.text((74, 58), "X", font=bold, fill=BACKGROUND)
    draw.text((116, 55), "X Insight Cards", font=bold, fill=INK)
    label = "v1.0.0 workflow demo"
    box = draw.textbbox((0, 0), label, font=regular)
    draw.text((WIDTH - 62 - (box[2] - box[0]), 60), label, font=regular, fill=MUTED)


def intro_frame(
    latin_regular: tuple[str, int],
    latin_bold: tuple[str, int],
    cjk: tuple[str, int],
) -> Image.Image:
    image, draw = base_frame()
    header(draw, font(latin_regular, 22), font(latin_bold, 22))
    draw.text((80, 142), "One prompt. A complete creator pack.", font=font(latin_bold, 52), fill=INK)
    draw.text((82, 210), "一句指令，完成选题、核验、翻译、排版与质检。", font=font(cjk, 29), fill=MUTED)

    draw.rounded_rectangle((80, 300, WIDTH - 80, 512), 24, fill=SURFACE, outline="#29415F", width=2)
    draw.text((112, 330), "$x-insight-cards", font=font(latin_bold, 28), fill=ACCENT)
    draw.text(
        (112, 386),
        "Find today's best X posts and create up to five\nreview-ready packs for Douyin and Xiaohongshu.",
        font=font(latin_regular, 31),
        fill=INK,
        spacing=13,
    )

    draw.text(
        (80, 588),
        "No API key  ·  No cookies  ·  Source attributed  ·  Stops before publishing",
        font=font(latin_regular, 24),
        fill=ACCENT_GREEN,
    )
    return image


def workflow_frame(
    active_index: int,
    latin_regular: tuple[str, int],
    latin_bold: tuple[str, int],
) -> Image.Image:
    image, draw = base_frame()
    regular_22 = font(latin_regular, 22)
    bold_22 = font(latin_bold, 22)
    header(draw, regular_22, bold_22)
    draw.text((80, 135), "Source-verified workflow", font=font(latin_bold, 48), fill=INK)
    draw.text(
        (82, 196),
        "Every stage leaves evidence. Quality wins over quota.",
        font=font(latin_regular, 27),
        fill=MUTED,
    )

    steps = ["discover", "verify", "rank", "deduplicate", "translate", "typeset", "QA"]
    gap = 12
    card_width = 150
    start_x = (WIDTH - (len(steps) * card_width + (len(steps) - 1) * gap)) // 2
    for index, step in enumerate(steps):
        x = start_x + index * (card_width + gap)
        active = index == active_index
        draw.rounded_rectangle(
            (x, 286, x + card_width, 364),
            18,
            fill=ACCENT if active else SURFACE_LIGHT,
            outline=ACCENT if active else "#2A3A52",
            width=2,
        )
        label_font = font(latin_bold if active else latin_regular, 19)
        box = draw.textbbox((0, 0), step, font=label_font)
        draw.text(
            (x + (card_width - (box[2] - box[0])) / 2, 314),
            step,
            font=label_font,
            fill=BACKGROUND if active else INK,
        )

    evidence = [
        "Source fields checked: URL · author · handle · exact text · date",
        "Quality gate applied: only candidates scoring 75/100 or higher",
        "History checked: canonical URL and normalized text hash",
    ]
    for index, line in enumerate(evidence):
        y = 430 + index * 58
        draw.ellipse((84, y + 7, 102, y + 25), fill=ACCENT_GREEN)
        draw.text((122, y), line, font=font(latin_regular, 24), fill=INK)

    progress = f"{active_index + 1} / {len(steps)}"
    draw.text((82, 630), progress, font=regular_22, fill=MUTED)
    draw.rounded_rectangle((160, 640, WIDTH - 80, 650), 5, fill="#253650")
    progress_width = int((WIDTH - 240) * (active_index + 1) / len(steps))
    draw.rounded_rectangle((160, 640, 160 + progress_width, 650), 5, fill=ACCENT)
    return image


def output_frame(
    card_path: Path,
    latin_regular: tuple[str, int],
    latin_bold: tuple[str, int],
    cjk: tuple[str, int],
) -> Image.Image:
    image, draw = base_frame()
    header(draw, font(latin_regular, 22), font(latin_bold, 22))
    draw.text((60, 120), "Review-ready output", font=font(latin_bold, 44), fill=INK)
    draw.text((62, 174), "One attributed card + one copy-ready caption", font=font(latin_regular, 25), fill=MUTED)

    source_card = Image.open(card_path).convert("RGB")
    target_width = 720
    target_height = int(source_card.height * target_width / source_card.width)
    source_card = source_card.resize((target_width, target_height), Image.Resampling.LANCZOS)
    image.paste(source_card, (60, 230))

    panel = (820, 230, 1220, 632)
    draw.rounded_rectangle(panel, 22, fill=SURFACE, outline="#2A3A52", width=2)
    draw.text((852, 262), "Caption", font=font(latin_bold, 25), fill=ACCENT)
    draw.text(
        (852, 315),
        "注意力从来不是时间管理问题，\n而是选择问题。你反复答应什么，\n生活就会向什么方向复利。",
        font=font(cjk, 28),
        fill=INK,
        spacing=15,
    )
    draw.text((852, 480), "#长期主义  #注意力管理  #认知成长", font=font(cjk, 20), fill=MUTED)

    draw.rounded_rectangle((852, 540, 1034, 584), 14, fill="#153C31")
    draw.text((874, 551), "SOURCE VERIFIED", font=font(latin_bold, 15), fill=ACCENT_GREEN)
    draw.rounded_rectangle((1048, 540, 1188, 584), 14, fill="#20334C")
    draw.text((1070, 551), "HUMAN REVIEW", font=font(latin_bold, 15), fill=ACCENT)
    return image


def build_demo(card_path: Path, output_path: Path) -> None:
    latin_regular, latin_bold, cjk = RENDER_MODULE.find_fonts()
    frames = [intro_frame(latin_regular, latin_bold, cjk)]
    frames.extend(
        workflow_frame(index, latin_regular, latin_bold)
        for index in range(7)
    )
    frames.append(output_frame(card_path, latin_regular, latin_bold, cjk))
    durations = [1500] + [420] * 7 + [2600]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--card", type=Path, default=ROOT / "examples" / "demo-card.png")
    parser.add_argument("--output", type=Path, default=ROOT / "assets" / "demo-workflow.gif")
    args = parser.parse_args()
    build_demo(args.card, args.output)
    print(args.output)


if __name__ == "__main__":
    main()
