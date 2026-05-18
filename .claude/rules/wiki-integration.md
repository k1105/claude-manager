# Wiki統合ルール

## 原則

wikiはこのシステムの「知識の永続化レイヤー」。プロジェクトのresearch/が「進行中の調査」なら、wikiは「確定した知識」。
ディレクトリ構造・フォーマットの正は `wiki/SCHEMA.md`。

## Discordメッセージからの自律トリガー

Discordでメッセージを受け取ったとき、以下の条件に該当すれば**明示的な指示なしで**wikiスキルを呼び出す。

### 自動ingest（wiki-ingest）

**ingestする:**
- 記事URL、技術ブログ、gist、公式ドキュメント、論文 — 内容が静的で再利用価値がある
- 添付ファイル（PDF、記事スクショ等）
- 会話中に出た体系的な知識（技術的解説、パターンの議論等）→ raw/sessions/ 経由

**ingestしない:**
- 動的ツールのリンク（Figma、Google Docs、Slack、GitHub PR等 — 内容が変わる）
- 一時的なリンク（ログURL、デプロイURL、CI結果）
- ミーム、雑談中のURL

**迷ったとき:** 「wikiに入れる？〜の文脈で再利用できそう」と理由付きで確認する。

### 自動query（wiki-query）

- 「〜って何だっけ」「前に調べた？」等の既存知識を問う質問 → wiki-queryで回答
- プロジェクト議論中に関連概念が出た → `wiki/index.md` を確認し、ヒットしたら提示

## desk-researchとの接続

1. RQに取り組む前に `wiki/index.md` で関連ページがないか確認
2. 既存の知識があればそれをベースに調査を深める（ゼロからやらない）
3. 調査で見つけた良質なソースは wiki-ingest で取り込む
4. RQドキュメントからwikiページへの `[[wikilink]]` を積極的に張る

## プロジェクトresearch/との棲み分け

| | projects/*/research/ | wiki/ |
|---|---|---|
| 性質 | プロジェクト固有、一時的 | 汎用的、永続的 |
| 例 | 「zuuumyのUI比較調査」 | 「UXデザインパターン」 |
| 管理 | プロジェクト終了で_archiveへ | 永続。wiki-lintで品質維持 |

## Obsidian連携

- `[[ページ名]]` wikilink形式（Obsidian互換）
- YAML frontmatter → Dataviewプラグインで活用可能
- graph viewでwikiの構造を可視化
