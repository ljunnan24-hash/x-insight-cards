# Private WeChat delivery

Use this step only for a private review destination explicitly configured by the user. It is not social publishing.

## Route selection

1. Prefer `scripts/wechat_ilink_delivery.mjs` when a dedicated iLink robot review chat is pinned. It is headless, never opens desktop WeChat, and cannot accept a runtime recipient override during delivery.
2. Use `scripts/wechat_main_window_delivery.sh` only when the user separately configured their File Transfer Assistant and the iLink route is unavailable.
3. Never switch routes during a failed batch. Stop, preserve the checkpoint, and report the exact reason.

## Dedicated iLink robot

The helper keeps its fixed recipient, credential path, context cache, and delivery checkpoints under `~/.weclaw`. The config and context files must be mode `0600`; their parent directory must be mode `0700`. The helper reads tokens internally and never prints them.

When `scripts/wechat_ilink_listener.mjs` is installed as a user `launchd` service, it long-polls without opening a window. It accepts only the exact text `发今日素材` from the pinned recipient. It ignores the same text from every other user. Other nonempty text from the pinned recipient is not treated as a delivery command; instead, the listener replies with the exact usage prompt. Before advancing the iLink sync cursor, it durably journals both delivery commands and guidance replies so a process crash cannot lose either action.

For the requested Shanghai calendar date, the listener selects the candidates immediately preceding the latest matching `run_completion` record in private history. It requires `READY_FOR_REVIEW`, the final absolute PNG path and SHA-256, a nonempty caption, completed manual 200% QA, and a matching selection count. It then builds a private manifest and uses the normal preflight and checkpointed delivery path.

If the pack is not ready, reply only that it is not ready and require a later command. If a private receipt already exists for the date, reply that it was already sent and do not resend. A transport error keeps the durable command pending with bounded exponential backoff.

Configure once:

```bash
node scripts/wechat_ilink_delivery.mjs configure \
  --credentials /absolute/path/to/account.json \
  --sync /absolute/path/to/account.sync.json \
  --recipient 'fixed-user-id@im.wechat'
```

Capture a context after the pinned user messages the dedicated robot:

```bash
node scripts/wechat_ilink_delivery.mjs capture-context
```

Run the required zero-message preflight:

```bash
node scripts/wechat_ilink_delivery.mjs preflight
```

If preflight exits with code `23`, ask the user to send one character to the dedicated robot, run `capture-context`, and repeat preflight. Do not start a batch with missing, empty, mismatched, or rejected context. Context refresh requires an inbound user message; never imitate one, use another recipient, or fall back to context-free sending.

Prepare a private manifest outside the public deliverable folder:

```json
{
  "run_id": "2026-07-23-top-5",
  "pairs": [
    {
      "image": "/absolute/path/to/final-card.png",
      "caption": "独立配文。\\n\\n#标签一 #标签二 #标签三",
      "sha256": "expected-final-png-sha256"
    }
  ]
}
```

Deliver:

```bash
node scripts/wechat_ilink_delivery.mjs deliver \
  --manifest /absolute/path/to/private-delivery-manifest.json
```

The helper validates 1–5 final PNGs and their hashes, preflights context before the first upload, sends image then caption, and checkpoints every accepted message. Stable client IDs make a resumed attempt reuse the same message identity; an accepted image is never intentionally resent when only its caption remains. Stop immediately on the first error. Never convert a rejected image, send a file attachment, or retry blindly.

`TRANSPORT_ACCEPTED` means iLink accepted every image and caption. Ask the user to confirm that the complete set is visible before recording `DELIVERED_FOR_REVIEW`.

The default macOS service label is `com.junnan.x-insight-cards-wechat-listener`. Inspect it without sending:

```bash
launchctl print "gui/$(id -u)/com.junnan.x-insight-cards-wechat-listener"
```

## File Transfer Assistant fallback

1. Confirm that WeChat is already signed in. Never quit, restart, log out, switch accounts, or choose `仅传输文件`.
2. Run `scripts/wechat_main_window_delivery.sh --dry-run`. Do not open a detached `文件传输助手` window.
3. The helper requires exactly one visible File Transfer Assistant row, a verified green selected state, high-confidence OCR of the cropped chat header, two consecutive matching frames, and the same frontmost WeChat window before every send. Physical mouse or keyboard input during verification aborts.
4. Obtain any required just-in-time computer-control confirmation.
5. Send each final PNG as an image, followed immediately by its matching plain-text caption. Never send a TXT file.
6. Stop without sending when any destination, header, preview, pasted text, foreground-window, or emptied-input check fails. Do not guess or use unverified coordinates.

Deliver one verified pair:

```bash
scripts/wechat_main_window_delivery.sh \
  --image /absolute/path/to/card.png \
  --caption-file /absolute/path/to/caption.txt
```

Never open a Xiaohongshu, Douyin, or other publishing page during private delivery.
