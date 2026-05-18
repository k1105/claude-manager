#!/usr/bin/env python3
"""Read-only Discord message fetcher for an external server.

Uses `curl` for HTTPS to avoid Python's certifi-bundle setup on macOS.

Usage:
    discord-reader.py <channel_id> [--limit N] [--before MSG_ID] [--after MSG_ID]
                                   [--out PATH] [--format md|json]

Token is read from ~/.claude/channels/discord-reader/.env.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

ENV_PATH = Path.home() / ".claude" / "channels" / "discord-reader" / ".env"
API = "https://discord.com/api/v10"


def load_token() -> str:
    if not ENV_PATH.exists():
        sys.exit(f"missing token file: {ENV_PATH}")
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if line.startswith("DISCORD_BOT_TOKEN="):
            return line.split("=", 1)[1].strip()
    sys.exit("DISCORD_BOT_TOKEN not found in .env")


def request(path: str, token: str, params: dict | None = None) -> list | dict:
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    proc = subprocess.run(
        [
            "curl", "-sS", "--fail-with-body",
            "-H", f"Authorization: Bot {token}",
            "-H", "User-Agent: claude-manager-discord-reader/0.1",
            url,
        ],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        sys.exit(f"curl failed ({proc.returncode}) on {path}: {proc.stdout or proc.stderr}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        sys.exit(f"non-JSON response on {path}: {proc.stdout[:500]}")


def fetch_channel(channel_id: str, token: str) -> dict:
    return request(f"/channels/{channel_id}", token)


def fetch_messages(channel_id: str, token: str, limit: int,
                   before: str | None, after: str | None) -> list[dict]:
    out: list[dict] = []
    cursor_before = before
    remaining = limit
    while remaining > 0:
        page = min(100, remaining)
        params = {"limit": page}
        if cursor_before:
            params["before"] = cursor_before
        if after and not cursor_before:
            params["after"] = after
        batch = request(f"/channels/{channel_id}/messages", token, params)
        if not batch:
            break
        out.extend(batch)
        remaining -= len(batch)
        if len(batch) < page:
            break
        cursor_before = batch[-1]["id"]
    out.sort(key=lambda m: int(m["id"]))
    return out


def to_markdown(channel: dict, msgs: list[dict]) -> str:
    name = channel.get("name", channel.get("id"))
    lines = [
        f"# #{name}", "",
        f"channel_id: `{channel.get('id')}`  ",
        f"fetched: {datetime.now().isoformat(timespec='seconds')}  ",
        f"count: {len(msgs)}", "",
    ]
    for m in msgs:
        author = m.get("author", {})
        handle = author.get("global_name") or author.get("username") or author.get("id", "?")
        ts = m.get("timestamp", "")
        content = m.get("content", "") or ""
        lines.append(f"### {handle} — {ts}")
        if content:
            lines.append(content)
        for att in m.get("attachments", []) or []:
            lines.append(f"- attachment: [{att.get('filename')}]({att.get('url')})")
        for emb in m.get("embeds", []) or []:
            url = emb.get("url")
            title = emb.get("title") or ""
            if url:
                lines.append(f"- embed: [{title}]({url})")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("channel_id")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--before")
    ap.add_argument("--after")
    ap.add_argument("--out", help="output file path; default stdout")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    args = ap.parse_args()

    token = load_token()
    channel = fetch_channel(args.channel_id, token)
    msgs = fetch_messages(args.channel_id, token, args.limit, args.before, args.after)

    if args.format == "json":
        body = json.dumps({"channel": channel, "messages": msgs}, ensure_ascii=False, indent=2)
    else:
        body = to_markdown(channel, msgs)

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(body, encoding="utf-8")
        print(f"wrote {len(msgs)} messages to {args.out}")
    else:
        print(body)


if __name__ == "__main__":
    main()
