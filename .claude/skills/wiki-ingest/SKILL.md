---
name: wiki-ingest
description: URLまたはテキストをwikiに取り込む。raw保存→要約ページ作成→entity/concept更新→index/log更新。
user-invocable: true
---

# Wiki Ingest

URLまたはテキストをwikiに取り込む。

## トリガー

**明示的：**
- ユーザーが「wikiに入れて」「ingestして」と言ったとき
- `/wiki-ingest <URL or text>` で呼ばれたとき

**自律的（`.claude/rules/wiki-integration.md` 参照）：**
- Discordで記事URL・gist・技術ブログ等が共有されたとき
- desk-researchで良質なソースを見つけたとき

## フロー

### 1. ソースの取得と保存

**URLの場合：**
1. WebFetchでページ内容を取得
2. `raw/articles/YYYY-MM-DD-title.md` に保存（frontmatter付き）

**セッションの学びの場合：**
1. ユーザーの説明またはコンテキストからキーポイントを抽出
2. `raw/sessions/YYYY-MM-DD-title.md` に保存

**テキスト/メモの場合：**
1. `raw/notes/YYYY-MM-DD-title.md` に保存

### 2. 要約ページの作成

`wiki/sources/YYYY-MM-DD-title.md` を作成。フォーマットは `wiki/SCHEMA.md` に従う。

内容：
- 要約（3-5文）
- キーポイント（箇条書き）
- 関連する既存wikiページへの `[[wikilink]]`

### 3. entity/conceptページの更新・作成

- 関連するentity/conceptページがあれば情報を追記
- 新しいentity/conceptが必要なら作成（テンプレートは `wiki/SCHEMA.md` 参照）
- 矛盾する情報がある場合: 両論併記し `> ⚠️ 矛盾` で明示。自動では解決しない

### 4. インデックスとログの更新

- `wiki/index.md` の該当セクションにページを追加
- `wiki/log.md` に操作を記録

### 5. 報告

Discord経由の場合、同じチャンネルに結果を報告：
```
📥 Wiki取り込み: {タイトル}
- 新規: {ページリスト}
- 更新: {ページリスト}
```

## 注意

- rawソースは絶対に変更しない（イミュータブル）
- 1回のingestで複数ページを更新してOK
- 大量の更新がある場合は要約して報告
