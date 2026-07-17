---
name: x-insight-cards
description: Find, verify, rank, deduplicate, translate, render, and quality-check recent X posts as English-Chinese insight cards with concise Chinese captions. Use for daily creator curation about wealth, life, goals, habits, attention, freedom, or long-term thinking when outputs must be source-auditable, typography-aware, ready for human review, and never auto-published or credential-backed.
---

# X Insight Cards

Turn public X posts into a small, source-auditable set of bilingual cards and copy-ready captions. Optimize for insight quality, faithful attribution, natural Chinese typography, and human review—not volume.

## Workflow

1. Read [references/workflow.md](references/workflow.md) before running a daily curation job.
2. Check the user's history file and existing output folders. Deduplicate by canonical URL and normalized English-text SHA-256.
3. Discover posts from the last 24 hours. Expand to 72 hours only when necessary; then use unused evergreen posts.
4. Verify each candidate's URL, author, handle, exact English text, publication date, and views when views are material to selection.
5. Reject politics, stock tips, medical advice, course sales, unattributed reposts, pure motivational filler, and unverifiable content.
6. Score candidates using [references/scoring.md](references/scoring.md). Select no more than five, sorted by score. Never pad below 75/100.
7. Translate faithfully. Preserve paragraphs, quotation marks, dashes, parentheses, and tone.
8. Render one card per selected post. Prefer a real post screenshot when the environment can capture it cleanly. Otherwise use `scripts/render_card.py` and label the record `rearranged-render`.
9. Write one concise Chinese caption per card: normally one sentence, at most two, followed by 3–5 relevant hashtags. Do not copy the translation.
10. Run the checks in [references/qa-checklist.md](references/qa-checklist.md). Stop at review-ready; do not upload or publish.

## Rendering

Install Pillow, then run:

```bash
python scripts/render_card.py \
  --input assets/demo-post.json \
  --output ./output/demo-card.png
```

The English post style is the fixed reference. Match Chinese to the English text's visual size, stroke darkness, line height, and color. On macOS, prefer PingFang SC Regular for Chinese regular text. Read [references/typography.md](references/typography.md) whenever typography or punctuation is in scope.

## Ranking and deduplication

After assigning evidence-based score components, run:

```bash
python scripts/score_candidates.py \
  --input candidates.json \
  --history history.jsonl \
  --output ranked.json
```

Read [references/candidate-schema.md](references/candidate-schema.md) when preparing input data or consuming the output.

## Output contract

Default deliverables:

- One PNG per selected post.
- One copy-ready caption per post in the response or a user-requested structured file.
- A private/auditable history record outside the public deliverable folder.

Do not add poster backgrounds, ratings, Chinese titles, commentary, decorative AI art, platform watermarks, or captions inside the card.

## Safety and rights

- Use public, read-only sources. Never read, export, or store cookies, passwords, or access tokens.
- Do not bypass login challenges, rate limits, CAPTCHAs, or platform restrictions.
- Do not imply endorsement by X or any quoted author.
- Keep source links and attribution. Do not redistribute third-party media unless the user has the necessary rights.
- Never publish automatically. A separate, explicit user request and platform-specific workflow is required for any upload.
