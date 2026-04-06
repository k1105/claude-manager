---
name: wiki-setup
description: "LLM Wiki（Karpathyパターン）の初期セットアップ。一度きりの実行。構造は wiki/SCHEMA.md を参照。"
user-invocable: true
---

# Wiki Setup（初回のみ）

LLM Wiki（Karpathyパターン）をハーネスに導入する一回きりのセットアップスキル。

## 前提

- Obsidian vaultが作成済み（このリポジトリがvaultに含まれる）

## フロー

### 1. ディレクトリ構造の作成

`wiki/SCHEMA.md` の「構造」セクションに従い、wiki/ と raw/ を作成する。

### 2. SCHEMA.md・index.md・log.md の初期化

- `wiki/SCHEMA.md` — ページフォーマット、種別テンプレート、操作、命名規則を定義
- `wiki/index.md` — 空のカテゴリ見出し（Entities / Concepts / Sources / Synthesis）
- `wiki/log.md` — 空のログファイル

### 3. 関連スキルの確認

以下が存在することを確認（なければ作成）：
- `wiki-ingest` — ソース取り込み
- `wiki-query` — 知識の検索・合成
- `wiki-lint` — 健全性チェック

### 4. ハーネスへの統合

- `CLAUDE.md` のファイル構造セクションに wiki/ と raw/ を追記
- `.claude/rules/wiki-integration.md` を作成（desk-research連携、Discord自律トリガー）
- `config/cron_jobs.json` に wiki-lint を追加
- `desk-research` スキルにwiki連携ステップを追加

### 5. 初回Ingest

Karpathyの元記事を `wiki-ingest` でingestし、動作確認する。

### 6. 完了チェック

- [ ] wiki/ と raw/ が存在
- [ ] SCHEMA.md / index.md / log.md が初期化済み
- [ ] wiki-ingest / wiki-query / wiki-lint スキルが存在
- [ ] CLAUDE.md に wiki/ raw/ の記載あり
- [ ] wiki-integration ルールが存在
- [ ] cron_jobs.json に wiki-lint あり
- [ ] Obsidianでgraph viewが表示される
