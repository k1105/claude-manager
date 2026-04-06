# Wiki Schema

## 構造

```
wiki/
  index.md          — 全ページの目次（カテゴリ別）
  log.md            — 操作ログ（時系列）
  SCHEMA.md         — このファイル（運用ルール）
  entities/         — 人物・組織・技術・ツール
  concepts/         — 概念・パターン・設計思想
  sources/          — ソースごとの要約ページ
  synthesis/        — 横断分析・比較・テーマ別まとめ
raw/
  articles/         — Web記事のmarkdown（イミュータブル）
  notes/            — 手動メモ
  sessions/         — セッションからの学び
```

## ページフォーマット

すべてのwikiページにYAML frontmatterをつける：

```yaml
---
title: ページタイトル
type: entity | concept | source | synthesis
tags: [tag1, tag2]
sources: [raw/articles/xxx.md]  # 参照元
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## ページ種別テンプレート

### entity（人物・組織・技術・ツール）
- 概要（1-2文）
- 主な特徴・機能（箇条書き）
- 関連する `[[concept]]` や `[[entity]]` へのリンク
- ソースからの引用・事実（出典付き）

### concept（概念・パターン・設計思想）
- 定義（1-2文）
- 仕組み・構造の説明
- 具体例やユースケース
- 関連 `[[concept]]` `[[entity]]` へのリンク

### source（ソース要約）
- 要約（3-5文）
- キーポイント（箇条書き）
- 関連wikiページへの `[[wikilink]]`

### synthesis（横断分析）
- 問いまたはテーマ
- 関連ページからの情報統合
- 比較・対照・結論

## ページ内のルール

- 他のwikiページへのリンクは `[[ページ名]]` 形式（Obsidian互換）
- ソースへの参照は `[^source-name]` で脚注形式
- 矛盾する情報: `> ⚠️ 矛盾` ブロックで両論併記。自動解決しない
- 1ページ1トピック。長くなったら分割

## 操作

詳細な手順は各スキルを参照：

| 操作 | スキル | 概要 |
|---|---|---|
| Ingest | `wiki-ingest` | rawソース保存 → 要約 → entity/concept更新 → index/log更新 |
| Query | `wiki-query` | index → 関連ページ読み → 回答合成 → synthesis保存判定 |
| Lint | `wiki-lint` | 孤立ページ・壊れたリンク・frontmatter・矛盾・鮮度チェック |

## 命名規則

- ファイル名: kebab-case（例: `domain-driven-design.md`）
- rawソース: `YYYY-MM-DD-title.md`（例: `2026-04-06-karpathy-llm-wiki.md`）
