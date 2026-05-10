# 出力フォーマット（Markdown / HTML 使い分け）

成果物の性質によって Markdown / HTML / ハイブリッドを使い分ける。三層で考える。

## 三層ルール

### ① 純Markdown（永続・ナビゲート対象）

**対象:**
- `wiki/` 全体（entities / concepts / sources / synthesis / index / log）
- `projects/*/status.md` `projects/*/README.md`
- `logs/daily/` `logs/weekly/` `logs/system/`
- `tasks/YYYY-MM-DD.md`
- `docs/` 配下
- メモリ（`~/.claude/projects/.../memory/`）

**理由:** Obsidianのgraph view・wikilink・backlink・全文検索・dataview・frontmatterクエリが全部markdown前提。HTML化すると恩恵を全部失う。長期に編集される＆diffレビュー対象なのも理由。

### ② Markdown内にHTML埋め込み（図表が主役の.md）

**対象:**
- `wiki/synthesis/` で比較表・関係図・タイムラインが主役のページ
- `projects/*/research/` で図解が要るリサーチドキュメント
- 一部の長文 spec で構造化が効く箇所

**使えるタグ:** `<table>` `<svg>` `<details>` `<summary>` `<div>` `<span>` `<img>` など。`<script>` は不可。

**理由:** markdownのリンク・frontmatter・graph統合は維持しつつ、リッチな構造を入れたい場面。

### ③ 単体HTML（一回読み・他人に渡す・インタラクティブ）

**対象:**
- `projects/*/drafts/*.html` — 見積、提案、モックアップ、PR explainer
- 他人（PO・取引先・チーム）に渡すレポート
- インタラクティブなプロトタイプ・カスタムエディタ・playground
- 週次レビューや横断スキャンの可視化ダッシュボード

**置き方:** `projects/{project}/drafts/` か `projects/{project}/reports/`。Obsidianからは「リンクで開くだけのリソース」として `.md` 側に `[link](./file.html)` の相対リンクを張る（クリックでブラウザが開く）。

**理由:** Thariqの議論（情報密度・視覚明瞭性・共有しやすさ・双方向性）が刺さる領域。一回読み or 他人に渡す前提なのでdiffノイズも問題にならない。

## 判定フロー

迷ったら以下の順で判定：

1. **wikilinkで辿られるか？** → Yes なら ①
2. **長期に編集・diffレビューされるか？** → Yes なら ①
3. **図表・比較が主役か？** → Yes なら ②（mdに埋め込み）
4. **他人に渡す or 一回読みのレポート/モック/プロトタイプか？** → Yes なら ③（単体html）
5. それ以外 → ① がデフォルト

## 補足

- Obsidian は `.html` ファイルを「ノート」として扱わない（graph/backlink/search対象外）。単体HTMLは「添付リソース」と理解する
- HTML生成はMarkdownの2-4倍時間がかかる。一発もの・他人に渡すもの以外では割に合わないこともある
- 既存の前例: `projects/zuuumy/drafts/metabase-estimate.html` は③パターンの典型
