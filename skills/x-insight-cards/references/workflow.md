# Daily curation workflow

## Discovery ladder

1. Search the last 24 hours.
2. If fewer than five verified candidates score at least 75, expand to 72 hours.
3. If still short, use unused evergreen posts.
4. Return fewer than five rather than lowering the quality bar.

Recommended topics: wealth, money, life, dreams, goals, systems, habits, attention, freedom, purpose, and long-term thinking.

## Source verification

For every candidate, record:

- Canonical post URL.
- Author display name and handle.
- Exact English text and paragraph structure.
- Published date/time and source timezone when available.
- View count only when it affects ranking or is shown on the card.
- Capture method: `native-screenshot` or `rearranged-render`.

Use the native X page when available. Public oEmbed or another public read-only representation is an acceptable fallback. Never present a reconstructed card as a native screenshot.

## Exclusions

Reject:

- Political controversy or rage bait.
- Financial/stock recommendations.
- Medical or therapeutic advice.
- Course sales, funnels, or disguised promotion.
- Reposts without a traceable original source.
- Pure emotional encouragement with no transferable idea.
- Content already present in history by URL or text hash.

## Translation

- Preserve meaning, stance, paragraph breaks, quotation marks, dashes, parentheses, and rhetorical tone.
- Prefer natural Simplified Chinese over literal word order.
- Keep author names and product names accurate.
- Do not add interpretation inside the translation.

## Caption

- Prefer one sentence; allow two only when needed.
- Restate the insight more simply or add one tightly related angle.
- Do not copy or line-by-line summarize the card translation.
- Add 3–5 useful hashtags on a new line.
- Avoid promises of reach, income, or guaranteed outcomes.

## State model

Use this monotonic state model when logging a run:

`DISCOVERED → VERIFIED → SCORED → CAPTURED → TRANSLATED → READY_FOR_REVIEW [→ DELIVERED_FOR_REVIEW]`

Send unusable candidates to `REJECTED`; rendering failures go to `FAILED` with a reason.
`DELIVERED_FOR_REVIEW` is optional and means the review pack reached a verified private self-chat. It never means uploaded, drafted, or published on a content platform.
