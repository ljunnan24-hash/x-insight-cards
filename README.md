<p align="center">
  <img src="assets/hero.svg" alt="X Insight Cards" width="100%" />
</p>

<p align="center">
  <strong>Turn high-signal X posts into verified bilingual insight cards—without scraping credentials or auto-posting.</strong><br />
  <strong>把 X 上真正有价值的内容，变成来源可核验、中文排版准确的双语创作素材。</strong>
</p>

<p align="center">
  <strong>Creator-tested result · 创作者实测</strong>
</p>

| **9,545 plays · 播放** | **358 likes · 点赞** | **42 saves · 收藏** | **+5,990 bonus views · 额外浏览奖励** |
| ---: | ---: | ---: | ---: |

<p align="center">
  One Douyin video made with this workflow · 一条使用本工作流制作的抖音视频<br />
  Public Douyin ID · 抖音号：<strong>51536643904</strong><br />
  <sub>Observed result, not a reach guarantee · 真实使用结果，不构成流量承诺</sub>
</p>

### More documented creator results · 更多创作者实测数据

| Platform · 平台 | Screenshot-verified evidence · 截图可核验数据 |
| --- | --- |
| **Douyin · 抖音** | **9,545 plays**, **358 likes**, **42 saves**, plus **5,990 bonus views** · **9,545 播放、358 赞、42 收藏、5,990 额外浏览奖励** |
| **Xiaohongshu · 小红书** | Five visible post examples: **6,536 · 4,271 · 1,775 · 1,584 · 665 views** · 五条可见作品案例：**6,536 · 4,271 · 1,775 · 1,584 · 665 浏览** |
| **Xiaohongshu · 小红书** | Visible post likes include **153, 131 and 105**; the account shows **1,511 total likes & saves** · 可见作品含 **153、131、105 赞**；账号累计 **1,511 获赞与收藏** |

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="#why-this-is-different">Why it is different</a> ·
  <a href="#creator-tested">Creator-tested</a>
</p>

<p align="center">
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827" />
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
  <img alt="Privacy first" src="https://img.shields.io/badge/privacy-no%20cookies-16A34A" />
  <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-blue" />
</p>

## 一句话介绍 · One-line introduction

**X Insight Cards is a creator-tested Codex Skill that finds high-signal X posts, verifies and scores them, then produces faithful English-Chinese cards and concise captions ready for human review.**

**X Insight Cards 是一个经过真实创作者验证的 Codex Skill：从 X 筛选高认知内容，完成来源核验、评分、去重、翻译和中文排版，最终生成可审核的双语卡片与极简配文。**

---

## The problem · 为什么做它

Finding useful posts is easy. Building a repeatable creator workflow is not:

- Viral posts are not always insightful.
- Screenshots lose context and attribution.
- Literal Chinese translations read poorly.
- Mixed Latin/CJK fonts often produce visibly wrong weight and punctuation.
- Most “automation” projects jump straight to risky credential scraping and auto-publishing.

**X Insight Cards** turns that mess into an auditable pipeline:

`discover → verify → deduplicate → score → translate → render → review`

## What you get

- A reusable **Codex Skill** for daily X curation.
- A deterministic Python card renderer with cross-platform font discovery.
- A 100-point quality rubric and a hard 75-point floor—never pad the list.
- URL + normalized text-hash deduplication.
- Simplified Chinese typography rules, including native punctuation placement.
- One- or two-sentence captions that do not copy the translation.
- A review-first safety boundary: no cookies, no CAPTCHA bypass, no automatic publishing.

## Quick start

### Install as a Codex Skill

```bash
git clone https://github.com/ljunnan24-hash/x-insight-cards.git
cd x-insight-cards
./scripts/install-skill.sh
```

Then ask Codex:

```text
Use $x-insight-cards to find and create today's top five verified bilingual
insight cards about attention, habits, freedom, and long-term thinking.
```

### Render a synthetic demo card

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python skills/x-insight-cards/scripts/render_card.py \
  --input examples/demo-post.json \
  --output examples/demo-card.png
```

![Synthetic bilingual card example](examples/demo-card.png)

The demo author and post are fictional. No third-party avatar or post is bundled.

## Why this is different

| Typical content automation | X Insight Cards |
| --- | --- |
| Optimize for volume | Optimize for transferable insight |
| Rank by views | Score insight, clarity, fit, credibility, freshness, readability |
| Copy popular posts | Verify and retain attribution |
| Literal translation | Preserve meaning, structure, tone, and native Chinese typography |
| Generate a fixed quota | Return fewer than five when quality is insufficient |
| Scrape sessions or auto-post | Public read-only discovery and human review by default |
| Opaque selection | Component scores, source links, hashes, and state history |

<a id="creator-tested"></a>

## Creator-tested · 创作者实测

This workflow grew out of a real Chinese knowledge-content account, not a synthetic growth demo. One Douyin video made with it reached **9,545 plays, 358 likes, and 42 saves**, and received a platform notice for **5,990 bonus views**. Xiaohongshu screenshots also document five visible posts with **6,536, 4,271, 1,775, 1,584, and 665 views**; visible likes include **153, 131, and 105**, while the account shows **1,511 total likes and saves**.

这套工作流来自真实的中文知识内容账号，而不是虚构的增长案例。其中一条用本工作流制作的抖音视频获得 **9,545 播放、358 赞、42 收藏**，并收到平台的 **5,990 额外浏览量奖励**。小红书截图还记录了五条可见作品的 **6,536、4,271、1,775、1,584、665 浏览**；可见点赞案例包括 **153、131、105 赞**，账号累计 **1,511 获赞与收藏**。公开抖音号：**51536643904**。

These numbers prove real-world use, not guaranteed future reach. Topic, account history, timing, and platform distribution still matter.

这些数据用于证明工作流经过真实使用，不代表未来作品一定获得相同流量；选题、账号基础、发布时间和平台分发仍然会影响结果。

## Quality model

| Dimension | Points |
| --- | ---: |
| Insight gain | 30 |
| One-idea clarity | 20 |
| Chinese social fit | 20 |
| Source credibility | 15 |
| Freshness | 10 |
| Visual readability | 5 |

Candidates below **75/100** are rejected. If only three posts clear the bar, the output is three.

## Typography that respects Chinese

The English post remains the fixed visual reference. Chinese is calibrated to match its perceived size, stroke darkness, line height, and color.

For Mainland Simplified Chinese horizontal text:

- `、，；：。？！` use native full-width forms toward the lower-left of their character frame.
- Quotation marks, parentheses, and book-title marks keep their paired native forms.
- Dashes and ellipses remain centered.
- No code pushes every punctuation mark into the same corner.

On macOS, the renderer prefers **PingFang SC Regular** for regular Chinese text. Override fonts with `XIC_LATIN_FONT`, `XIC_CJK_FONT`, and their optional index variables.

## Repository layout

```text
.
├── README.md
├── README.zh-CN.md
├── examples/
│   ├── demo-post.json
│   └── demo-card.png
├── skills/x-insight-cards/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── scripts/
│   │   ├── render_card.py
│   │   └── score_candidates.py
│   ├── references/
│   └── assets/demo-post.json
└── tests/
```

Only `skills/x-insight-cards/` is copied into the Codex skills directory.

## Boundaries

- This project does not ship X posts, author avatars, platform screenshots, cookies, or system fonts.
- It is not affiliated with X, Douyin, Xiaohongshu, or any quoted author.
- Keep source links and follow applicable platform rules and copyright law.
- Reconstructed cards must be identified as rearranged renders, not native screenshots.
- Publishing remains a separate, explicit human decision.

## Contributing

Issues and pull requests are welcome—especially for Linux/Windows CJK font support, better line breaking, new scoring evidence, and accessibility. See [CONTRIBUTING.md](CONTRIBUTING.md).

If this saves you from rebuilding the same workflow, consider starring the repository. It helps more creators find a safer, higher-signal alternative to blind content automation.

## License

MIT for the code and original documentation. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
