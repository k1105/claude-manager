#!/usr/bin/env python3
"""Convert a Claude Code session transcript (jsonl) to a readable markdown digest.

Usage:
    transcript-to-md.py <transcript.jsonl> <out.md>

Strategy:
- Iterate jsonl events in order.
- Emit user prompts and assistant text content blocks.
- Collapse tool_use / tool_result into one-line summaries (path/cmd preview).
- Skip system/attachment/permission-mode/file-history-snapshot/ai-title noise.
- Truncate tool inputs/outputs to keep the file scannable in Obsidian.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

PREVIEW_CHARS = 200
MAX_TOOL_INPUT_CHARS = 400


def short(s: str, n: int = PREVIEW_CHARS) -> str:
    s = s.replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def escape_obsidian(s: str) -> str:
    """Escape `[[` / `]]` so Obsidian doesn't render them as wikilinks.

    Raw transcripts often contain Rails bind values like `[["id", 1]]`,
    which Obsidian misinterprets as broken wikilinks otherwise.
    """
    return s.replace("[[", r"\[\[").replace("]]", r"\]\]")


def render_content(content) -> list[str]:
    """Return a list of markdown lines for an assistant/user content list."""
    out: list[str] = []
    if isinstance(content, str):
        out.append(escape_obsidian(content))
        return out
    if not isinstance(content, list):
        return out
    for block in content:
        if not isinstance(block, dict):
            continue
        btype = block.get("type")
        if btype == "text":
            out.append(escape_obsidian(block.get("text", "")))
        elif btype == "thinking":
            txt = block.get("thinking", "")
            if txt:
                out.append(f"<details><summary>thinking</summary>\n\n{escape_obsidian(txt)}\n\n</details>")
        elif btype == "tool_use":
            name = block.get("name", "?")
            inp = block.get("input", {})
            try:
                inp_s = json.dumps(inp, ensure_ascii=False)
            except Exception:
                inp_s = str(inp)
            # backticks already prevent wikilink parsing inside inline code
            out.append(f"- 🔧 **{name}**: `{short(inp_s, MAX_TOOL_INPUT_CHARS)}`")
        elif btype == "tool_result":
            content_inner = block.get("content")
            text_parts: list[str] = []
            if isinstance(content_inner, list):
                for c in content_inner:
                    if isinstance(c, dict) and c.get("type") == "text":
                        text_parts.append(c.get("text", ""))
            elif isinstance(content_inner, str):
                text_parts.append(content_inner)
            preview = short(" ".join(text_parts), PREVIEW_CHARS)
            err = " (error)" if block.get("is_error") else ""
            out.append(f"  ↳ result{err}: {escape_obsidian(preview)}")
        elif btype == "image":
            out.append("- 🖼 (image attached)")
    return out


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])

    if not src.exists():
        print(f"transcript not found: {src}", file=sys.stderr)
        return 1

    dst.parent.mkdir(parents=True, exist_ok=True)

    title = src.stem
    started = ""
    cwd = ""
    lines: list[str] = []
    last_role: str | None = None  # aggregate consecutive same-role events into one section

    with src.open() as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                ev = json.loads(raw)
            except json.JSONDecodeError:
                continue
            t = ev.get("type")
            ts = ev.get("timestamp") or ev.get("created_at") or ""
            if not started and ts:
                started = ts
            if not cwd:
                cwd = ev.get("cwd") or ev.get("working_directory") or ""

            if t == "ai-title":
                title = ev.get("title", title)
                continue
            if t in {"system", "permission-mode", "file-history-snapshot", "attachment", "last-prompt"}:
                continue

            if t == "user":
                msg = ev.get("message", {}) or {}
                content = msg.get("content") if isinstance(msg, dict) else ev.get("content")
                rendered = render_content(content)
                if not rendered:
                    continue
                body = "\n".join(b for b in rendered if b)
                if not body.strip():
                    continue
                # Skip tool_result-only user turns (already shown under prior assistant)
                if all(line.startswith("  ↳ result") for line in rendered if line):
                    continue
                if last_role != "user":
                    lines.append(f"### 👤 user — {short(ts)}")
                    lines.append("")
                    last_role = "user"
                lines.append(body)
                lines.append("")
            elif t == "assistant":
                msg = ev.get("message", {}) or {}
                content = msg.get("content") if isinstance(msg, dict) else ev.get("content")
                rendered = render_content(content)
                if not rendered:
                    continue
                body = "\n".join(rendered)
                if not body.strip():
                    continue
                if last_role != "assistant":
                    lines.append(f"### 🤖 assistant — {short(ts)}")
                    lines.append("")
                    last_role = "assistant"
                lines.append(body)
                lines.append("")

    # Build tag list so transcripts aren't orphans in Obsidian graph view.
    # - `transcript` groups all transcripts.
    # - `transcript/YYYY-MM` lets you slice by month.
    # - `cwd/<basename>` clusters by project (cwd of the session).
    tags = ["transcript"]
    # YYYY-MM from filename prefix (e.g. 2026-05-03-1817-7c88a61c → 2026-05)
    stem = src.stem
    if len(stem) >= 7 and stem[4] == "-":
        tags.append(f"transcript/{stem[:7]}")
    if cwd:
        cwd_slug = Path(cwd).name
        if cwd_slug:
            tags.append(f"cwd/{cwd_slug}")

    frontmatter = ["---", "tags:"]
    for t in tags:
        frontmatter.append(f"  - {t}")
    frontmatter.append(f"session: {src.name}")
    if started:
        frontmatter.append(f"started: {started}")
    if cwd:
        frontmatter.append(f"cwd: {cwd}")
    frontmatter.append(f"generated: {datetime.now().isoformat(timespec='seconds')}")
    frontmatter.append("---")
    frontmatter.append("")

    header = [
        f"# {title}",
        "",
        "---",
        "",
    ]
    dst.write_text("\n".join(frontmatter + header + lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
