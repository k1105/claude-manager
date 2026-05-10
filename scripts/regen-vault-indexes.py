#!/usr/bin/env python3
"""Regenerate `<!-- wiki-relink:start -->` blocks in vault index.md files
so every md file gets at least one inbound [[wikilink]] from a hub page.

Walks the vault, finds <dir>/index.md files, and rewrites the relink block
to enumerate every .md file under that directory (excluding the index itself
and other index.md files in subdirs which act as their own hubs).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

START = "<!-- wiki-relink:start -->"
END = "<!-- wiki-relink:end -->"

# Index files we manage. Each maps to the dir it indexes.
INDEX_FILES = ["raw", "tasks", "logs", "docs", "projects"]


def first_h1(md: str) -> str:
    m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    if not m:
        return ""
    title = m.group(1).strip()
    if len(title) > 60:
        title = title[:60].rstrip() + "…"
    return title


def gather(root: Path, vault: Path) -> dict[str, list[tuple[str, str, str]]]:
    """Return {section_label: [(vault_rel_link, display_stem, title), ...]}.

    vault_rel_link is the path relative to the vault, without `.md`, used
    inside `[[ ]]` for unambiguous linking. display_stem is the bare filename
    used as the visible label when the wikilink uses pipe-aliasing.
    Skips child index.md files (each subdir's index handles itself).
    """
    sections: dict[str, list[tuple[str, str, str]]] = {}
    for path in sorted(root.rglob("*.md")):
        if path.name == "index.md":
            continue
        rel = path.relative_to(root)
        parts = rel.parts
        if len(parts) == 1:
            label = "(直下)"
        else:
            label = "/".join(parts[:-1]) + "/"
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        title = first_h1(text) or path.stem
        vault_rel = str(path.relative_to(vault).with_suffix(""))
        sections.setdefault(label, []).append((vault_rel, path.stem, title))
    return sections


def render_block(sections: dict[str, list[tuple[str, str, str]]]) -> str:
    out: list[str] = [START]
    keys = sorted(sections.keys(), key=lambda k: (k != "(直下)", k))
    for k in keys:
        out.append("")
        out.append(f"## {k}")
        for vault_rel, stem, title in sections[k]:
            # `[[full/path|alias]]` — full path resolves unambiguously,
            # alias keeps the rendered text short.
            link = f"[[{vault_rel}|{stem}]]"
            display = title if title and title != stem else ""
            if display:
                out.append(f"- {link} — {display}")
            else:
                out.append(f"- {link}")
    out.append("")
    out.append(END)
    return "\n".join(out)


def update_index(index_path: Path, root: Path, vault: Path) -> str:
    if not index_path.exists():
        return "missing-index"
    text = index_path.read_text(encoding="utf-8")
    sections = gather(root, vault)
    new_block = render_block(sections)

    if START in text and END in text:
        s = text.index(START)
        e = text.index(END) + len(END)
        new_text = text[:s] + new_block + text[e:]
    else:
        # No marker — append before EOF
        new_text = text.rstrip() + "\n\n" + new_block + "\n"

    if new_text == text:
        return "unchanged"
    index_path.write_text(new_text, encoding="utf-8")
    n_links = sum(len(v) for v in sections.values())
    return f"updated ({n_links} links)"


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    vault = Path(sys.argv[1]).resolve()
    if not vault.exists():
        print(f"vault not found: {vault}", file=sys.stderr)
        return 1
    for name in INDEX_FILES:
        root = vault / name
        index = root / "index.md"
        if not root.is_dir():
            print(f"  {name}/: skip (no dir)")
            continue
        result = update_index(index, root, vault)
        print(f"  {name}/index.md: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
