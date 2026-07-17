# Candidate data schema

`score_candidates.py` accepts either a JSON array or `{ "candidates": [...] }`.

Required fields:

```json
{
  "id": "candidate-01",
  "url": "https://x.com/example/status/123",
  "author": "Example Author",
  "handle": "@example",
  "post": "Exact English text",
  "translation": "忠实的中文翻译",
  "score_detail": {
    "insight_gain": 27,
    "clarity": 18,
    "chinese_social_fit": 18,
    "source_credibility": 13,
    "freshness": 9,
    "visual_readability": 5
  }
}
```

Optional fields:

- `published_at`: ISO 8601 timestamp.
- `date_display`: Human-readable date for the card.
- `views_display`: Human-readable view count.
- `avatar`: Local image path supplied by the user.
- `caption`: One or two Chinese sentences plus hashtags.
- `flags`: Array of exclusion flags.
- `render_method`: `native-screenshot` or `rearranged-render`.

History is JSONL. The scorer reads `url` or `source_url` and `text_sha256` or `source_text_sha256` for deduplication.
