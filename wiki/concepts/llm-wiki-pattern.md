---
title: LLM Wikiパターン
type: concept
tags: [llm, knowledge-management, architecture]
sources: [raw/articles/2026-04-06-karpathy-llm-wiki.md]
created: 2026-04-06
updated: 2026-04-06
---

# LLM Wikiパターン

LLMが永続的なwikiを自動構築・維持するナレッジマネジメント手法。

## 概要

従来のRAG（Retrieval-Augmented Generation）は毎回ゼロから知識を検索・合成する。LLM Wikiパターンでは、ソース投入時にLLMが知識を構造化し、wikiページとして蓄積する。知識が複利的に増加し、クロスリファレンスが自動的に維持される。

## 3層アーキテクチャ

| 層 | 役割 | 管理者 |
|---|---|---|
| Raw Sources | 生データ（記事、メモ、議事録） | 人間が投入、イミュータブル |
| Wiki | 構造化された知識ページ | LLMが生成・更新 |
| Schema | 運用ルール・構造定義 | 人間とLLMが共同進化 |

## RAGとの違い

- RAG: 質問→検索→回答（毎回ゼロから）
- LLM Wiki: ソース→構造化→蓄積→質問→既存知識から回答（複利的）

## 参照

- [[2026-04-06-karpathy-llm-wiki]] — 原典（Karpathy gist）
