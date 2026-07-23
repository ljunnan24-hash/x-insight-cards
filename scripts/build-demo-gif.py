#!/usr/bin/env python3
"""Build a four-scene demo of scheduled preparation and phone-triggered delivery."""

from __future__ import annotations

import argparse
import importlib.util
import json
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
BACKGROUND = "#07111F"
SURFACE = "#101D30"
SURFACE_LIGHT = "#172840"
INK = "#F8FAFC"
MUTED = "#9DB0C9"
ACCENT = "#37C4FF"
GREEN = "#4ADE80"
PENDING = "#344760"


def font(spec: tuple[str, int], size: int) -> ImageFont.FreeTypeFont:
    return RENDER_MODULE.load_font(spec, size)


def base_frame(
    scene: str,
    latin_regular: tuple[str, int],
    latin_bold: tuple[str, int],
    cjk: tuple[str, int],
) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.ellipse((-230, -310, 510, 430), fill="#0D2A45")
    draw.ellipse((1000, 500, 1470, 970), fill="#14233A")
    draw.rounded_rectangle((30, 24, WIDTH - 30, HEIGHT - 24), 28, outline="#213651", width=2)

    draw.rounded_rectangle((58, 48, 100, 90), 12, fill=ACCENT)
    draw.text((72, 55), "X", font=font(latin_bold, 23), fill=BACKGROUND)
    draw.text((116, 54), "X Insight Cards", font=font(latin_bold, 23), fill=INK)
    label = f"{scene}  ·  真实工作流演示"
    label_font = font(cjk, 20)
    label_width = draw.textlength(label, font=label_font)
    draw.text((WIDTH - 58 - label_width, 58), label, font=label_font, fill=MUTED)
    return image, draw


def pill(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    label: str,
    label_font: ImageFont.FreeTypeFont,
    fill: str,
    color: str,
) -> None:
    draw.rounded_rectangle(box, 14, fill=fill)
    text_box = draw.textbbox((0, 0), label, font=label_font)
    text_width = text_box[2] - text_box[0]
    text_height = text_box[3] - text_box[1]
    x = box[0] + (box[2] - box[0] - text_width) / 2
    y = box[1] + (box[3] - box[1] - text_height) / 2 - text_box[1]
    draw.text((x, y), label, font=label_font, fill=color)


def schedule_frame(
    latin_regular: tuple[str, int],
    latin_bold: tuple[str, int],
    cjk: tuple[str, int],
) -> Image.Image:
    image, draw = base_frame("1 / 4", latin_regular, latin_bold, cjk)
    draw.text((70, 126), "每天 12:00，自动开始", font=font(cjk, 45), fill=INK)
    draw.text((72, 184), "Codex 定时任务自动唤醒 $x-insight-cards。", font=font(cjk, 25), fill=MUTED)

    draw.rounded_rectangle((70, 250, 1210, 548), 22, fill=SURFACE, outline="#2B4566", width=2)
    draw.rounded_rectangle((104, 286, 318, 500), 24, fill="#F8FAFC")
    draw.rounded_rectangle((104, 286, 318, 350), 24, fill=ACCENT)
    draw.rectangle((104, 326, 318, 350), fill=ACCENT)
    draw.text((171, 300), "DAILY", font=font(latin_bold, 22), fill=BACKGROUND)
    draw.text((138, 369), "12:00", font=font(latin_bold, 49), fill="#101828")
    draw.text((151, 442), "北京时间", font=font(cjk, 19), fill="#536471")

    draw.text((370, 294), "每日 X 优质认知帖子 Top 5", font=font(cjk, 31), fill=INK)
    draw.text((370, 354), "自动发现、核验、评分、去重、翻译与排版", font=font(cjk, 23), fill=MUTED)
    draw.text((370, 404), "最近 24 小时优先 · 不足 75 分不凑数", font=font(cjk, 22), fill=MUTED)
    pill(draw, (370, 458, 514, 504), "已启用", font(cjk, 18), "#12392E", GREEN)
    draw.text((540, 468), "下一次运行：明天 12:00", font=font(cjk, 19), fill=ACCENT)

    pill(draw, (70, 592, 276, 640), "无需每天输入", font(cjk, 18), "#15304B", ACCENT)
    pill(draw, (290, 592, 488, 640), "历史自动去重", font(cjk, 18), "#12392E", GREEN)
    pill(draw, (502, 592, 742, 640), "完成后等待指令", font(cjk, 18), "#2A2E47", "#D8C8FF")
    return image


def processing_frame(
    completed: int,
    data: dict,
    latin_regular: tuple[str, int],
    latin_bold: tuple[str, int],
    cjk: tuple[str, int],
) -> Image.Image:
    image, draw = base_frame("2 / 4", latin_regular, latin_bold, cjk)
    draw.text((70, 118), "找到帖子，并留下核验证据", font=font(cjk, 42), fill=INK)
    draw.text((72, 172), "不是黑盒：来源、内容和筛选结果都能追溯。", font=font(cjk, 24), fill=MUTED)

    draw.rounded_rectangle((70, 230, 770, 622), 22, fill=SURFACE, outline="#2B4566", width=2)
    draw.text((100, 258), "发现 1 条高质量候选", font=font(cjk, 22), fill=ACCENT)
    draw.text((100, 306), str(data["author"]), font=font(latin_bold, 30), fill=INK)
    draw.text((292, 312), str(data["handle"]), font=font(latin_regular, 22), fill=MUTED)
    draw.text(
        (100, 360),
        "The wedding is an event, love is a practice.\n"
        "The graduation is an event, education is a practice.\n"
        "The race is an event, fitness is a practice.",
        font=font(latin_regular, 23),
        fill=INK,
        spacing=13,
    )
    draw.line((100, 500, 740, 500), fill="#2A3D58", width=2)
    draw.text((100, 522), "公开来源", font=font(cjk, 18), fill=MUTED)
    draw.text((100, 557), str(data["source_url"]), font=font(latin_regular, 17), fill=ACCENT)

    draw.rounded_rectangle((800, 230, 1210, 622), 22, fill=SURFACE, outline="#2B4566", width=2)
    draw.text((832, 258), "核验记录", font=font(cjk, 25), fill=INK)
    score = sum(int(value) for value in data["score_detail"].values())
    checks = [
        "公开来源已读取",
        "作者、账号与日期一致",
        "英文原文逐字核对完成",
        f"评分 {score}/100；历史未使用",
    ]
    for index, label in enumerate(checks):
        y = 322 + index * 67
        done = index < completed
        draw.ellipse((834, y, 862, y + 28), fill=GREEN if done else PENDING)
        if done:
            draw.text((840, y - 2), "✓", font=font(cjk, 20), fill=BACKGROUND)
        draw.text((880, y - 2), label, font=font(cjk, 21), fill=INK if done else MUTED)

    status = "正在读取公开来源…" if completed == 1 else "正在核验与筛选…"
    if completed == len(checks):
        status = "核验完成，开始生成素材包。"
    draw.text((832, 574), status, font=font(cjk, 18), fill=GREEN if completed == 4 else ACCENT)
    return image


def output_frame(
    card_path: Path,
    data: dict,
    latin_regular: tuple[str, int],
    latin_bold: tuple[str, int],
    cjk: tuple[str, int],
) -> Image.Image:
    image, draw = base_frame("3 / 4", latin_regular, latin_bold, cjk)
    draw.text((52, 112), "生成可审核素材包", font=font(cjk, 42), fill=INK)
    draw.text((54, 164), "双语卡片、中文配文和原帖链接已准备完成。", font=font(cjk, 23), fill=MUTED)

    source_card = Image.open(card_path).convert("RGB")
    max_width, max_height = 680, 462
    scale = min(max_width / source_card.width, max_height / source_card.height)
    card_size = (int(source_card.width * scale), int(source_card.height * scale))
    source_card = source_card.resize(card_size, Image.Resampling.LANCZOS)
    card_x = 52 + (680 - card_size[0]) // 2
    card_y = 212 + (462 - card_size[1]) // 2
    image.paste(source_card, (card_x, card_y))

    draw.rounded_rectangle((758, 212, 1228, 674), 22, fill=SURFACE, outline="#2B4566", width=2)
    draw.text((790, 244), "小红书配文", font=font(cjk, 23), fill=ACCENT)
    caption = str(data["caption"])
    caption_lines = caption.replace("，", "，\n")
    hashtags = "  ".join(f"#{tag}" for tag in data["hashtags"])
    draw.text(
        (790, 292),
        caption_lines,
        font=font(cjk, 26),
        fill=INK,
        spacing=16,
    )
    draw.text((790, 422), hashtags, font=font(cjk, 18), fill=MUTED)
    draw.line((790, 458, 1196, 458), fill="#2A3D58", width=2)
    draw.text((790, 480), "原帖来源", font=font(cjk, 17), fill=MUTED)
    draw.text((790, 513), "x.com/JamesClear/status/2045205…", font=font(latin_regular, 17), fill=ACCENT)

    pill(draw, (790, 558, 952, 602), "来源已核验", font(cjk, 17), "#12392E", GREEN)
    pill(draw, (966, 558, 1166, 602), "等待手机指令", font(cjk, 17), "#15304B", ACCENT)
    draw.rounded_rectangle((790, 620, 1196, 658), 12, fill="#18273D")
    draw.text((817, 626), "素材已就绪，等待“发今日素材”。", font=font(cjk, 18), fill=INK)
    return image


def delivery_frame(
    card_path: Path,
    data: dict,
    sent_count: int,
    latin_regular: tuple[str, int],
    latin_bold: tuple[str, int],
    cjk: tuple[str, int],
) -> Image.Image:
    image, draw = base_frame("4 / 4", latin_regular, latin_bold, cjk)
    complete = sent_count == 5
    title = "已送达专属微信机器人" if complete else "发送到专属微信机器人"
    draw.text((52, 112), title, font=font(cjk, 40), fill=INK)
    draw.text(
        (54, 164),
        "手机发送“发今日素材”，后台机器人即刻交付。",
        font=font(cjk, 23),
        fill=MUTED,
    )

    draw.rounded_rectangle((52, 218, 404, 646), 22, fill=SURFACE, outline="#2B4566", width=2)
    draw.text((82, 248), "今日 Top 5", font=font(cjk, 24), fill=INK)
    for index in range(5):
        y = 304 + index * 61
        delivered = index < sent_count
        draw.rounded_rectangle((82, y, 374, y + 46), 12, fill=SURFACE_LIGHT)
        draw.rounded_rectangle((94, y + 8, 126, y + 38), 7, fill=ACCENT if delivered else PENDING)
        draw.text((103, y + 9), str(index + 1), font=font(latin_bold, 16), fill=BACKGROUND if delivered else MUTED)
        draw.text((142, y + 10), "图片 + 配文", font=font(cjk, 18), fill=INK if delivered else MUTED)
        draw.text((329, y + 10), "✓" if delivered else "…", font=font(cjk, 18), fill=GREEN if delivered else MUTED)

    draw.line((430, 424, 486, 424), fill=ACCENT, width=5)
    draw.polygon(((486, 414), (506, 424), (486, 434)), fill=ACCENT)

    draw.rounded_rectangle((526, 218, 1228, 646), 22, fill="#EFF2F5", outline="#2B4566", width=2)
    draw.rounded_rectangle((526, 218, 1228, 282), 22, fill="#F8FAFC")
    draw.rectangle((526, 258, 1228, 282), fill="#F8FAFC")
    draw.ellipse((554, 234, 586, 266), fill="#20C05C")
    draw.text((597, 231), "素材审核机器人", font=font(cjk, 23), fill="#172033")
    pill(draw, (1002, 228, 1196, 268), "收件人已固定", font(cjk, 15), "#E1F5E8", "#168A45")

    source_card = Image.open(card_path).convert("RGB")
    thumb_width = 302
    thumb_height = int(source_card.height * thumb_width / source_card.width)
    source_card = source_card.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
    image.paste(source_card, (568, 310))
    draw.rounded_rectangle((974, 300, 1190, 346), 15, fill="#95EC69")
    draw.text((1005, 308), "发今日素材", font=font(cjk, 19), fill="#172033")
    draw.rounded_rectangle((888, 366, 1190, 480), 16, fill="#FFFFFF")
    draw.text((910, 386), "真正改变人生的，", font=font(cjk, 19), fill="#172033")
    draw.text((910, 418), "是日复一日的练习。", font=font(cjk, 19), fill="#172033")
    draw.text((910, 450), "#长期主义 #习惯养成", font=font(cjk, 15), fill="#536471")

    status_color = GREEN if complete else ACCENT
    status = "5 / 5 已发送到专属机器人" if complete else f"正在发送… {sent_count} / 5"
    draw.rounded_rectangle((568, 560, 1190, 610), 14, fill="#E4E9EE")
    draw.text((592, 571), status, font=font(cjk, 20), fill="#168A45" if complete else "#1684B4")
    draw.ellipse((1144, 573, 1168, 597), fill=status_color)
    if complete:
        draw.text((1149, 571), "✓", font=font(cjk, 17), fill=BACKGROUND)

    draw.text(
        (52, 670),
        "固定机器人私聊 · 小红书、抖音仍由你审核发布",
        font=font(cjk, 19),
        fill=MUTED,
    )
    return image


def build_demo(card_path: Path, output_path: Path, data_path: Path | None = None) -> None:
    latin_regular, latin_bold, cjk = RENDER_MODULE.find_fonts()
    data_path = data_path or ROOT / "examples" / "demo-post.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    if not str(data.get("source_url", "")).startswith("https://x.com/"):
        raise ValueError("Demo data must include a public X source_url")

    frames = [schedule_frame(latin_regular, latin_bold, cjk)]
    frames.extend(
        processing_frame(completed, data, latin_regular, latin_bold, cjk)
        for completed in range(1, 5)
    )
    frames.append(output_frame(card_path, data, latin_regular, latin_bold, cjk))
    frames.append(delivery_frame(card_path, data, 3, latin_regular, latin_bold, cjk))
    frames.append(delivery_frame(card_path, data, 5, latin_regular, latin_bold, cjk))
    durations = [2200, 900, 900, 900, 1200, 2200, 1500, 3200]

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
    parser.add_argument("--data", type=Path, default=ROOT / "examples" / "demo-post.json")
    parser.add_argument("--output", type=Path, default=ROOT / "assets" / "demo-workflow.gif")
    args = parser.parse_args()
    build_demo(args.card, args.output, args.data)
    print(args.output)


if __name__ == "__main__":
    main()
