import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs/promises";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const script = fileURLToPath(new URL("./wechat_ilink_delivery.mjs", import.meta.url));
const recipient = "fixed-review-user@im.wechat";
const botId = "fixed-review-bot@im.bot";
const pngBytes = Buffer.from(
  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
  "base64",
);

async function runCli(args) {
  return await new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [script, ...args], {
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", reject);
    child.on("close", (code) => resolve({ code, stdout, stderr }));
  });
}

async function startFakeIlink({ preflightRet = 0, captionFailures = 0 } = {}) {
  const requests = [];
  const messages = [];
  let remainingCaptionFailures = captionFailures;
  const server = http.createServer(async (request, response) => {
    const chunks = [];
    for await (const chunk of request) chunks.push(chunk);
    const body = Buffer.concat(chunks);
    requests.push({
      url: request.url,
      headers: request.headers,
      body,
    });

    if (request.url === "/ilink/bot/getupdates") {
      response.setHeader("Content-Type", "application/json");
      response.end(JSON.stringify({
        ret: 0,
        msgs: [{
          message_id: 101,
          from_user_id: recipient,
          context_token: "test-fresh-context-token",
          item_list: [{ type: 1, text_item: { text: "private content is ignored" } }],
        }],
        get_updates_buf: "next-cursor",
      }));
      return;
    }

    if (request.url === "/ilink/bot/getconfig") {
      response.setHeader("Content-Type", "application/json");
      response.end(JSON.stringify(preflightRet === 0
        ? { ret: 0, typing_ticket: "ticket" }
        : { ret: preflightRet, errmsg: "context expired" }));
      return;
    }

    if (request.url === "/ilink/bot/getuploadurl") {
      response.setHeader("Content-Type", "application/json");
      response.end(JSON.stringify({
        ret: 0,
        upload_full_url: `${origin}/cdn-upload`,
      }));
      return;
    }

    if (request.url === "/cdn-upload") {
      response.setHeader("x-encrypted-param", "download-param");
      response.end();
      return;
    }

    if (request.url === "/ilink/bot/sendmessage") {
      const parsed = JSON.parse(body.toString("utf8"));
      messages.push(parsed.msg);
      const itemType = parsed.msg.item_list[0].type;
      response.setHeader("Content-Type", "application/json");
      if (itemType === 1 && remainingCaptionFailures > 0) {
        remainingCaptionFailures -= 1;
        response.end(JSON.stringify({ ret: -3, errmsg: "caption rejected" }));
      } else {
        response.end(JSON.stringify({ ret: 0 }));
      }
      return;
    }

    response.statusCode = 404;
    response.end();
  });

  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  const origin = `http://127.0.0.1:${address.port}`;
  return {
    origin,
    messages,
    requests,
    close: async () => await new Promise((resolve) => server.close(resolve)),
  };
}

async function makeFixture(origin) {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), "xic-ilink-test-"));
  const credentials = path.join(directory, "credentials.json");
  const sync = path.join(directory, "sync.json");
  const config = path.join(directory, "delivery.json");
  const image = path.join(directory, "card.png");
  const manifest = path.join(directory, "manifest.json");
  await fs.writeFile(credentials, JSON.stringify({
    bot_token: "test-token",
    ilink_bot_id: botId,
    baseurl: origin,
  }), { mode: 0o600 });
  await fs.writeFile(sync, JSON.stringify({ get_updates_buf: "cursor" }), { mode: 0o600 });
  await fs.writeFile(image, pngBytes);
  await fs.writeFile(manifest, JSON.stringify({
    run_id: "test-run",
    pairs: [{
      image,
      caption: "测试配文。\n\n#测试 #安全",
      sha256: crypto.createHash("sha256").update(pngBytes).digest("hex"),
    }],
  }));
  const configured = await runCli([
    "configure",
    "--credentials", credentials,
    "--sync", sync,
    "--recipient", recipient,
    "--config", config,
    "--inter-message-delay-ms", "0",
  ]);
  assert.equal(configured.code, 0, configured.stderr);
  const captured = await runCli(["capture-context", "--config", config]);
  assert.equal(captured.code, 0, captured.stderr);
  return { directory, config, manifest };
}

test("sends image then caption to the pinned recipient and resumes idempotently", async (t) => {
  const fake = await startFakeIlink();
  t.after(fake.close);
  const fixture = await makeFixture(fake.origin);
  t.after(async () => await fs.rm(fixture.directory, { recursive: true, force: true }));

  const first = await runCli(["deliver", "--config", fixture.config, "--manifest", fixture.manifest]);
  assert.equal(first.code, 0, first.stderr);
  assert.equal(JSON.parse(first.stdout).status, "TRANSPORT_ACCEPTED");
  assert.deepEqual(fake.messages.map((message) => message.item_list[0].type), [2, 1]);
  for (const message of fake.messages) {
    assert.equal(message.to_user_id, recipient);
    assert.equal(message.from_user_id, "");
    assert.equal(message.context_token, "test-fresh-context-token");
    assert.equal(message.run_id, "test-run");
  }
  const apiRequest = fake.requests.find((request) => request.url === "/ilink/bot/getconfig");
  assert.equal(apiRequest.headers["ilink-app-id"], "bot");
  assert.equal(apiRequest.headers["ilink-app-clientversion"], "132102");

  const second = await runCli(["deliver", "--config", fixture.config, "--manifest", fixture.manifest]);
  assert.equal(second.code, 0, second.stderr);
  assert.equal(fake.messages.length, 2, "completed state must not resend messages");
});

test("fails preflight before sending any material when context is rejected", async (t) => {
  const fake = await startFakeIlink({ preflightRet: -2 });
  t.after(fake.close);
  const fixture = await makeFixture(fake.origin);
  t.after(async () => await fs.rm(fixture.directory, { recursive: true, force: true }));

  const result = await runCli(["deliver", "--config", fixture.config, "--manifest", fixture.manifest]);
  assert.equal(result.code, 23);
  assert.equal(JSON.parse(result.stderr).code, "CONTEXT_REFRESH_REQUIRED");
  assert.equal(fake.messages.length, 0);
  assert.equal(fake.requests.filter((request) => request.url === "/ilink/bot/getuploadurl").length, 0);
});

test("resumes at the caption checkpoint without duplicating the image", async (t) => {
  const fake = await startFakeIlink({ captionFailures: 1 });
  t.after(fake.close);
  const fixture = await makeFixture(fake.origin);
  t.after(async () => await fs.rm(fixture.directory, { recursive: true, force: true }));

  const first = await runCli(["deliver", "--config", fixture.config, "--manifest", fixture.manifest]);
  assert.equal(first.code, 1);
  assert.deepEqual(fake.messages.map((message) => message.item_list[0].type), [2, 1]);

  const second = await runCli(["deliver", "--config", fixture.config, "--manifest", fixture.manifest]);
  assert.equal(second.code, 0, second.stderr);
  assert.deepEqual(fake.messages.map((message) => message.item_list[0].type), [2, 1, 1]);
  assert.equal(fake.messages[1].client_id, fake.messages[2].client_id);
});
