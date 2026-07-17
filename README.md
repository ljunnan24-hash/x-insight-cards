<p align="center">
  <img src="assets/hero.svg" alt="X Insight Cards" width="100%" />
</p>

<p align="center">
  <strong>Turn high-signal X posts into verified bilingual insight cards—without scraping credentials or auto-posting.</strong>
</p>

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

## The problem

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

## Creator-tested

This workflow grew out of a real Chinese knowledge-content account, not a synthetic growth demo.

One example post reached **9,545 views, 358 likes, and 42 saves** on Douyin. The creator reports that most recent posts receive strong reach. Public account ID: **51536643904**.

These numbers are evidence that the workflow has been used in practice—not a promise of future reach. Topic, account history, timing, and platform distribution still matter.

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
