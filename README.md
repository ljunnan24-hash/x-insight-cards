<p align="center">
  <img src="assets/hero.svg" alt="X Insight Cards" width="100%" />
</p>

<p align="center">
  <strong>Automatically turn high-quality X posts into image-and-caption content packs for Douyin and Xiaohongshu.</strong><br />
  <strong>自动筛选 X 上的优质内容，生成适合抖音、小红书的双语图片与配文素材。</strong>
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="#creator-tested">Real-world results</a> ·
  <a href="#how-it-works">How it works</a>
</p>

<p align="center">
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827" />
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
  <img alt="Privacy first" src="https://img.shields.io/badge/privacy-no%20cookies-16A34A" />
  <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-blue" />
</p>

## What it does

**X Insight Cards automates the work before publishing: it finds strong X posts, verifies and ranks them, removes duplicates, translates them, and produces bilingual images plus concise Chinese captions for Douyin and Xiaohongshu.**

**X Insight Cards 自动完成发布前的素材准备：寻找优质 X 原帖、核验来源、评分去重、翻译排版，最终生成适合抖音和小红书的双语图片与极简配文。**

`discover → verify → rank → deduplicate → translate → typeset → review`

Each run gives you:

- Automated discovery and ranking of recent high-quality source posts.
- Up to five Douyin/Xiaohongshu content packs—never filler added to reach a quota.
- One source-attributed bilingual PNG and one copy-ready Chinese caption per post.
- A private history record for duplicate prevention and auditability.

<a id="creator-tested"></a>

## Creator-tested on Douyin and Xiaohongshu

The workflow has already been used to make posts for real creator accounts. Results visible in the creator-provided screenshots include:

| Platform | Documented results |
| --- | --- |
| **Douyin** | One post reached **9,545 plays, 358 likes, and 42 saves**, plus a platform notice for **5,990 bonus views** |
| **Xiaohongshu** | Five visible posts reached **6,536, 4,271, 1,775, 1,584, and 665 views**; visible likes include **153, 131, and 105** |
| **Xiaohongshu account** | **1,511 total likes and saves** |

Public Douyin ID: `51536643904`.

**中文说明：**由本工作流生成素材的抖音单条作品获得 **9,545 播放、358 赞、42 收藏**，并收到 **5,990 额外浏览量奖励**；小红书多条作品获得数百至数千浏览，账号累计 **1,511 获赞与收藏**。

These figures demonstrate real-world use, not guaranteed future reach. Topic choice, account history, timing, and platform distribution still matter.

## Quick start

```bash
git clone https://github.com/ljunnan24-hash/x-insight-cards.git
cd x-insight-cards
./scripts/install-skill.sh
```

Then ask Codex:

```text
Use $x-insight-cards to find today's best posts about attention, habits,
freedom, and long-term thinking. Create up to five verified bilingual
image-and-caption content packs for Douyin and Xiaohongshu review.
```

That is the whole setup. The Skill contains the workflow, quality rubric, typography rules, renderer, and safety boundaries.

## Why creators use it

| The usual problem | What this Skill does |
| --- | --- |
| Finding good material every day takes time | Automatically discovers recent X posts and scores them for insight and creator fit |
| Screenshots lose context | Keeps the author, handle, source URL, date, and exact English text |
| Literal Chinese feels translated | Preserves meaning and tone, then applies native Simplified Chinese typography |
| Daily curation repeats the same posts | Deduplicates by canonical URL and normalized text hash |
| Automation creates account risk | Uses public read-only sources and stops at human review |

<a id="how-it-works"></a>

## How it works

1. Search the last 24 hours; expand to 72 hours only when needed.
2. Verify the URL, author, handle, exact text, date, and material view counts.
3. Reject politics, stock tips, medical advice, course sales, reposts, and empty motivation.
4. Score every candidate out of 100 and reject anything below 75.
5. Remove previously used URLs and semantically duplicated text.
6. Translate faithfully and match the Chinese typography to the English source style.
7. Render the card, write a one- or two-sentence caption, run QA, and stop for review.

If only three posts pass the bar, the output is three. Quality wins over quota.

## Quality bar

| Dimension | Points |
| --- | ---: |
| Insight gain | 30 |
| One-idea clarity | 20 |
| Chinese social fit | 20 |
| Source credibility | 15 |
| Freshness | 10 |
| Visual readability | 5 |

## Chinese typography is part of the product

The English source remains the visual reference. Chinese matches its perceived size, stroke weight, line height, and color without changing the source style.

- Mainland Simplified Chinese punctuation uses native full-width metrics.
- Commas, stops, semicolons, colons, question marks, and exclamation marks keep their native lower placement.
- Dashes and ellipses remain centered; paired marks keep their paired forms.
- On macOS, the renderer prefers **PingFang SC Regular** for regular Chinese text.

Override fonts with `XIC_LATIN_FONT`, `XIC_CJK_FONT`, and their optional index variables.

## Use the renderer without Codex

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

## Safety by default

- No cookies, passwords, tokens, or session exports.
- No CAPTCHA, login-wall, rate-limit, or platform-control bypasses.
- No automatic draft creation, upload, or publishing.
- No bundled X posts, author avatars, platform screenshots, or system fonts.
- Rearranged cards are identified as rearranged renders, never native screenshots.

Publishing is always a separate, explicit human decision.

## Repository layout

```text
skills/x-insight-cards/
├── SKILL.md
├── agents/openai.yaml
├── scripts/
│   ├── render_card.py
│   └── score_candidates.py
├── references/
└── assets/demo-post.json
```

Only `skills/x-insight-cards/` is installed into the Codex skills directory.

## Contributing

Issues and pull requests are welcome—especially for Linux/Windows CJK fonts, line breaking, accessibility, and better scoring evidence. See [CONTRIBUTING.md](CONTRIBUTING.md).

If this saves you from rebuilding the same creator workflow, a Star helps other creators find it.

## License

MIT for the code and original documentation. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
