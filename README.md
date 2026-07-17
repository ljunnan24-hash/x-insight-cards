<p align="center">
  <img src="assets/hero.svg" alt="X Insight Cards" width="100%" />
</p>

<p align="center">
  <strong>Find the X posts worth sharing. Turn them into bilingual cards ready for review.</strong><br />
  <strong>筛出真正值得分享的 X 内容，生成可直接审核的中英双语卡片。</strong>
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

**X Insight Cards is a Codex Skill for Chinese creators who want a repeatable way to turn high-value X posts into source-verified, well-typeset English-Chinese cards.**

**X Insight Cards 是为中文创作者设计的 Codex Skill：自动筛选高价值 X 原帖，核验来源、评分去重，并生成中英双语卡片与极简配文。**

`discover → verify → rank → deduplicate → translate → typeset → review`

Each run gives you:

- Up to five posts that clear the quality bar—never filler added to reach a quota.
- One source-attributed bilingual PNG per post.
- One concise Chinese caption per card, ready to copy.
- A private history record for duplicate prevention and auditability.

## Quick start

```bash
git clone https://github.com/ljunnan24-hash/x-insight-cards.git
cd x-insight-cards
./scripts/install-skill.sh
```

Then ask Codex:

```text
Use $x-insight-cards to find today's best posts about attention, habits,
freedom, and long-term thinking. Create up to five verified bilingual cards
with concise Chinese captions.
```

That is the whole setup. The Skill contains the workflow, quality rubric, typography rules, renderer, and safety boundaries.

## Why creators use it

| The usual problem | What this Skill does |
| --- | --- |
| Trending posts drown out useful ideas | Scores for insight, clarity, fit, credibility, freshness, and readability |
| Screenshots lose context | Keeps the author, handle, source URL, date, and exact English text |
| Literal Chinese feels translated | Preserves meaning and tone, then applies native Simplified Chinese typography |
| Daily curation repeats the same posts | Deduplicates by canonical URL and normalized text hash |
| Automation creates account risk | Uses public read-only sources and stops at human review |

<a id="creator-tested"></a>

## Built in a real creator workflow

This is not a mock growth project. It was extracted from a workflow used on real Chinese content accounts.

- **Douyin:** one video made with the workflow reached **9,545 plays, 358 likes, and 42 saves**, plus a platform notice for **5,990 bonus views**.
- **Xiaohongshu:** documented post examples reached **6,536, 4,271, 1,775, 1,584, and 665 views**. Visible likes include **153, 131, and 105**; the account shows **1,511 total likes and saves**.
- **Public Douyin ID:** `51536643904`.

The numbers show that the workflow has been used in practice. They are not a promise of future reach; topic choice, account history, timing, and distribution still matter.

<details>
<summary><strong>中文实测说明</strong></summary>

这不是为展示而虚构的增长项目，而是从真实中文内容账号的日常工作流中提炼出来的工具：抖音单条作品获得 **9,545 播放、358 赞、42 收藏**，并收到 **5,990 额外浏览量奖励**；小红书可见作品案例获得 **6,536、4,271、1,775、1,584、665 浏览**，可见点赞包括 **153、131、105 赞**，账号累计 **1,511 获赞与收藏**。这些数据只证明工具经过真实使用，不构成流量承诺。

</details>

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
