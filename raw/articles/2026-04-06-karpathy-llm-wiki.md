---
title: "LLM Wiki - Andrej Karpathy"
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
ingested: 2026-04-06
---

# LLM Wiki

A pattern for building personal knowledge bases using LLMs.

## Core Idea

Instead of just retrieving from raw documents at query time (RAG), the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files. When you add a new source, the LLM reads it, extracts key information, and integrates it into the existing wiki — updating entity pages, revising summaries, noting contradictions, strengthening the evolving synthesis.

The wiki is a persistent, compounding artifact. Cross-references are already there. Contradictions already flagged. Synthesis already reflects everything read.

## Architecture (3 layers)

1. **Raw sources** — curated collection of source documents. Immutable. LLM reads but never modifies.
2. **The wiki** — LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons. LLM owns this layer entirely.
3. **The schema** — a document (CLAUDE.md etc.) that tells the LLM how the wiki is structured, conventions, workflows.

## Operations

- **Ingest**: Drop source → LLM reads, discusses, writes summary, updates index, updates entity/concept pages, appends to log. Single source might touch 10-15 pages.
- **Query**: Ask questions → LLM searches index, reads relevant pages, synthesizes answer. Good answers filed back into wiki.
- **Lint**: Periodic health-check. Contradictions, stale claims, orphan pages, missing concepts, data gaps.

## Key Files

- **index.md**: Content-oriented catalog of everything. Organized by category. LLM reads this first for queries.
- **log.md**: Chronological append-only record. Parseable with unix tools.

## Tips

- Obsidian Web Clipper for converting articles to markdown
- Download images locally for LLM access
- Obsidian graph view for wiki shape visualization
- Marp for slide decks from wiki content
- Dataview plugin for querying YAML frontmatter
- Wiki is just a git repo — version history for free

## Why It Works

Humans abandon wikis because maintenance burden grows faster than value. LLMs don't get bored, don't forget cross-references, can touch 15 files in one pass. Maintenance cost is near zero.

Human's job: curate sources, direct analysis, ask good questions, think about meaning.
LLM's job: everything else.
