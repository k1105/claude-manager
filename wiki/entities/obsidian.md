---
title: Obsidian
type: entity
tags: [tool, knowledge-management, markdown]
sources: [raw/articles/2026-04-06-karpathy-llm-wiki.md]
created: 2026-04-06
updated: 2026-04-06
---

# Obsidian

Markdownベースのナレッジベースツール。ローカルファイルで動作し、`[[wikilink]]` によるページ間リンクとgraph viewが特徴。

## LLM Wikiでの役割

Karpathyの表現: 「ObsidianはIDE、LLMはプログラマー、wikiはコードベース」

- **graph view**: wikiの構造を視覚化。ハブページ、孤立ページの発見
- **Web Clipper**: ブラウザ記事をmarkdownに変換してraw sourceに
- **Dataview**: YAML frontmatterへのクエリ。動的なテーブル/リスト生成
- **Marp**: markdownからスライドデッキ生成

## 関連

- [[llm-wiki-pattern]] — Obsidianを閲覧層として活用
