#!/usr/bin/env python3
"""Render a clean bilingual X-style card from verified local JSON data."""

from __future__ import annotations

import argparse
import glob
import json
import os
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageOps


INK = "#111418"
MUTED = "#536471"
BORDER = "#D8DDE3"
CLOSING_PUNCTUATION = frozenset("，。；：！？、）》」』】”’）］｝")
OPENING_PUNCTUATION = frozenset("（《「『【“‘［｛")


def existing_font(candidates: Iterable[tuple[str, int]]) -> tuple[str, int]:
    for path, index in candidates:
        if path and Path(path).exists():
            return path, index
    raise FileNotFoundError(
        "No suitable font found. Set XIC_LATIN_FONT and XIC_CJK_FONT to local font files."
    )


def find_fonts() -> tuple[tuple[str, int], tuple[str, int], tuple[str, int]]:
    pingfang = sorted(
        glob.glob(
            "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/"
            "*.asset/AssetData/PingFang.ttc"
        )
    )
    latin_regular = existing_font(
        [
            (os.environ.get("XIC_LATIN_FONT", ""), int(os.environ.get("XIC_LATIN_INDEX", "0"))),
            ("/System/Library/Fonts/Supplemental/Arial.ttf", 0),
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 0),
            (r"C:\Windows\Fonts\arial.ttf", 0),
        ]
    )
    latin_bold = existing_font(
        [
            (os.environ.get("XIC_LATIN_BOLD_FONT", ""), int(os.environ.get("XIC_LATIN_BOLD_INDEX", "0"))),
            ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0),
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 0),
            (r"C:\Windows\Fonts\arialbd.ttf", 0),
            latin_regular,
        ]
    )
    cjk_candidates: list[tuple[str, int]] = []
    if os.environ.get("XIC_CJK_FONT"):
        cjk_candidates.append(
            (os.environ["XIC_CJK_FONT"], int(os.environ.get("XIC_CJK_INDEX", "0")))
        )
    cjk_candidates.extend((path, 3) for path in pingfang)  # PingFang SC Regular
    cjk_candidates.extend(
        [
            ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 2),
            ("/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf", 0),
            (r"C:\Windows\Fonts\msyh.ttc", 0),
            ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),
        ]
    )
    return latin_regular, latin_bold, existing_font(cjk_candidates)


def load_font(spec: tuple[str, int], size: int) -> ImageFont.FreeTypeFont:
    path, index = spec
    return ImageFont.truetype(path, size, index=index)


def measure(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> float:
    return float(draw.textlength(text, font=font))


def wrap_words(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if measure(draw, candidate, font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def rebalance_cjk(lines: list[str]) -> list[str]:
    if len(lines) > 1 and len(lines[-1]) <= 2 and len(lines[-2]) >= 7:
        count = 3 - len(lines[-1])
        lines[-1] = lines[-2][-count:] + lines[-1]
        lines[-2] = lines[-2][:-count]
    for index in range(1, len(lines)):
        while lines[index] and lines[index][0] in CLOSING_PUNCTUATION:
            lines[index - 1] += lines[index][0]
            lines[index] = lines[index][1:]
        if lines[index - 1] and lines[index - 1][-1] in OPENING_PUNCTUATION:
            lines[index] = lines[index - 1][-1] + lines[index]
            lines[index - 1] = lines[index - 1][:-1]
    return [line for line in lines if line]


def wrap_cjk(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if not current or measure(draw, candidate, font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = char
    if current:
        lines.append(current)
    return rebalance_cjk(lines)


def layout_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
    cjk: bool,
) -> list[str | None]:
    output: list[str | None] = []
    paragraphs = text.split("\n")
    for index, paragraph in enumerate(paragraphs):
        if paragraph:
            output.extend(
                wrap_cjk(draw, paragraph, font, max_width)
                if cjk
                else wrap_words(draw, paragraph, font, max_width)
            )
        elif 0 < index < len(paragraphs) - 1:
            output.append(None)
    return output


def initials(name: str) -> str:
    parts = [part for part in name.split() if part]
    return "".join(part[0].upper() for part in parts[:2]) or "X"


def avatar_image(
    avatar_path: str | None,
    name: str,
    size: int,
    bold_font: tuple[str, int],
) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    if avatar_path:
        source = Image.open(avatar_path).convert("RGB")
        source = ImageOps.fit(source, (size, size), method=Image.Resampling.LANCZOS)
    else:
        source = Image.new("RGB", (size, size), "#1D9BF0")
        draw = ImageDraw.Draw(source)
        label_font = load_font(bold_font, max(22, size // 3))
        label = initials(name)
        box = draw.textbbox((0, 0), label, font=label_font)
        draw.text(
            ((size - (box[2] - box[0])) / 2, (size - (box[3] - box[1])) / 2 - box[1]),
            label,
            font=label_font,
            fill="white",
        )
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(source, (0, 0), mask)
    return output


def render_card(data: dict, output_path: Path) -> dict:
    required = ("author", "handle", "post", "translation")
    missing = [key for key in required if not str(data.get(key, "")).strip()]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    latin_regular_spec, latin_bold_spec, cjk_spec = find_fonts()
    width = 1200
    margin_x = 58
    max_width = width - margin_x * 2
    body_size = int(data.get("body_size", 46))
    body_font = load_font(latin_regular_spec, body_size)
    translation_font = load_font(cjk_spec, body_size)
    scratch = ImageDraw.Draw(Image.new("RGB", (width, 1600), "white"))
    source_lines = layout_text(scratch, str(data["post"]), body_font, max_width, False)
    translation_lines = layout_text(
        scratch, str(data["translation"]), translation_font, max_width, True
    )

    body_y = 174
    line_height = int(data.get("line_height", 62))
    paragraph_gap = 26
    source_height = sum(paragraph_gap if line is None else line_height for line in source_lines)
    label_y = body_y + source_height + 20
    translation_y = label_y + 42
    translation_height = sum(
        paragraph_gap if line is None else line_height for line in translation_lines
    )
    footer_y = translation_y + translation_height + 24
    height = footer_y + 62

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((3, 3, width - 4, height - 4), radius=28, outline=BORDER, width=3)

    avatar = avatar_image(data.get("avatar"), str(data["author"]), 84, latin_bold_spec)
    image.paste(avatar, (58, 36), avatar)
    draw.text((166, 38), str(data["author"]), font=load_font(latin_bold_spec, 35), fill=INK)
    draw.text((166, 82), str(data["handle"]), font=load_font(latin_regular_spec, 27), fill=MUTED)
    draw.text((1080, 40), "X", font=load_font(latin_bold_spec, 40), fill=INK)

    y = body_y
    for line in source_lines:
        if line is None:
            y += paragraph_gap
        else:
            draw.text((margin_x, y), line, font=body_font, fill=INK)
            y += line_height

    draw.text((margin_x, label_y), "翻译自英语", font=load_font(cjk_spec, 22), fill=MUTED)
    y = translation_y
    for line in translation_lines:
        if line is None:
            y += paragraph_gap
        else:
            draw.text((margin_x, y), line, font=translation_font, fill=INK)
            y += line_height

    footer_parts = [str(data.get("date_display", "")).strip(), str(data.get("views_display", "")).strip()]
    footer = "  ·  ".join(part for part in footer_parts if part)
    if footer:
        draw.text((margin_x, footer_y), footer, font=load_font(cjk_spec, 26), fill=MUTED)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG", optimize=True)
    return {
        "output": str(output_path),
        "width": width,
        "height": height,
        "render_method": "rearranged-render",
        "latin_font": latin_regular_spec[0],
        "cjk_font": cjk_spec[0],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Verified post JSON")
    parser.add_argument("--output", required=True, type=Path, help="Output PNG")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(render_card(data, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
