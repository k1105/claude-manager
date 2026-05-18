#!/usr/bin/env python3
"""Add path-based YAML tags to Obsidian vault md files lacking them.

Usage:
    tag-vault.py <vault_root> [--dry-run]

Rule of thumb: tags are derived from the file's path relative to the vault.
If a file already has `tags:` in frontmatter, it's skipped. Otherwise we
inject a tags block (or wrap the file in a fresh frontmatter section).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def tags_for(rel_path: Path) -> list[str]:
    parts = rel_path.parts
    if not parts:
        return []
    top = parts[0]
    name = rel_path.name

    # transcripts already tagged by transcript-to-md.py — leave alone
    if top == "raw" and len(parts) >= 2 and parts[1] == "transcripts":
        return []

    if top == "wiki":
        if len(parts) == 2:
            return ["wiki", "wiki/meta"]
        sub = parts[1]
        sub_map = {
            "entities": "wiki/entity",
            "concepts": "wiki/concept",
            "sources": "wiki/source",
            "synthesis": "wiki/synthesis",
        }
        return ["wiki", sub_map.get(sub, f"wiki/{sub}")]

    if top == "docs":
        return ["docs"]

    if top == "tasks":
        if name == "index.md":
            return ["task", "task/meta"]
        m = re.match(r"^(\d{4})-(\d{2})-\d{2}\.md$", name)
        if m:
            return ["task", f"task/{m.group(1)}-{m.group(2)}"]
        return ["task"]

    if top == "logs":
        if len(parts) >= 2 and parts[1] == "daily":
            return ["log", "log/daily"]
        if len(parts) >= 2 and parts[1] == "weekly":
            return ["log", "log/weekly"]
        if len(parts) >= 2 and parts[1] == "system":
            return ["log", "log/system"]
        if len(parts) >= 2 and parts[1] == "screen":
            return ["log", "log/screen"]
        return ["log"]

    if top == "projects":
        if len(parts) >= 2 and parts[1] == "_shared_research":
            return ["research", "research/shared"]
        if len(parts) >= 2 and parts[1] == "_archive":
            if len(parts) >= 3:
                return ["project", "project/archive", f"project/{parts[2]}"]
            return ["project", "project/archive"]
        if len(parts) >= 2 and parts[1].endswith(".md"):
            # projects/index.md, projects/deadlines.md
            return ["project", "project/meta"]
        if len(parts) >= 2:
            project = parts[1]
            tags = ["project", f"project/{project}"]
            if len(parts) >= 3 and not parts[2].endswith(".md"):
                # projects/<name>/<subdir>/...
                sub = parts[2]
                tags.append(f"project/{project}/{sub}")
            return tags
        return ["project"]

    if top == "raw":
        if len(parts) >= 2:
            sub = parts[1]
            if sub.endswith(".md"):
                return ["raw"]
            sub_map = {
                "articles": "raw/article",
                "sessions": "raw/session",
                "notes": "raw/note",
                "discord-reads": "raw/discord-read",
            }
            return ["raw", sub_map.get(sub, f"raw/{sub}")]
        return ["raw"]

    # Root-level oddballs (Welcome.md etc.)
    if len(parts) == 1:
        return ["meta"]

    return []


FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def process_file(path: Path, vault_root: Path, dry_run: bool) -> str:
    rel = path.relative_to(vault_root)
    tags = tags_for(rel)
    if not tags:
        return "skip-no-tags"

    text = path.read_text(encoding="utf-8")

    # already has tags? skip
    m = FRONT_RE.match(text)
    if m:
        fm_body = m.group(1)
        if re.search(r"^tags\s*:", fm_body, re.MULTILINE):
            return "skip-has-tags"
        # inject tags into existing frontmatter
        tag_block = "tags:\n" + "\n".join(f"  - {t}" for t in tags)
        new_fm = tag_block + "\n" + fm_body
        new_text = f"---\n{new_fm}\n---\n" + text[m.end():]
    else:
        # prepend new frontmatter
        tag_block = "tags:\n" + "\n".join(f"  - {t}" for t in tags)
        new_text = f"---\n{tag_block}\n---\n\n" + text

    if dry_run:
        return f"would-tag: {tags}"
    path.write_text(new_text, encoding="utf-8")
    return f"tagged: {tags}"


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    vault_root = Path(sys.argv[1]).resolve()
    dry_run = "--dry-run" in sys.argv[2:]
    if not vault_root.exists():
        print(f"vault not found: {vault_root}", file=sys.stderr)
        return 1

    counts: dict[str, int] = {}
    for path in vault_root.rglob("*.md"):
        if any(p.startswith(".") for p in path.relative_to(vault_root).parts):
            continue
        result = process_file(path, vault_root, dry_run)
        key = result.split(":", 1)[0]
        counts[key] = counts.get(key, 0) + 1

    print("summary:")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
