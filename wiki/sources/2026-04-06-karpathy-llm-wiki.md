---
title: "LLM Wiki - Andrej Karpathy"
type: source
tags: [llm, knowledge-management, wiki, obsidian, rag]
sources: [raw/articles/2026-04-06-karpathy-llm-wiki.md]
created: 2026-04-06
updated: 2026-04-06
---

# LLM Wiki - Andrej Karpathy

RAGの限界を超える個人ナレッジベース構築パターン。

## 要約

LLMがwikiを自動構築・維持するアーキテクチャ。RAG（毎回検索→回答）ではなく、ソース投入時にLLMが知識を構造化し、永続的なwikiとして蓄積する。知識が複利で増えていく。

## キーポイント

- **3層アーキテクチャ**: raw sources（イミュータブル）→ wiki（LLM管理）→ schema（運用ルール）
- **3つの操作**: ingest（取り込み）、query（質問）、lint（健全性チェック）
- **index.md + log.md**: 目次と時系列ログの2軸でナビゲーション
- **Obsidianとの相性**: graph view、Dataview、Marp等のプラグイン活用
- **人間の役割**: ソースのキュレーション、問いを立てる、意味を考える
- **LLMの役割**: 要約、クロスリファレンス、整理、メンテナンス全般

## 関連

- [[claude-code]] — このシステム自体がLLM Wikiパターンの実装
- [[obsidian]] — wikiの閲覧・可視化ツール
