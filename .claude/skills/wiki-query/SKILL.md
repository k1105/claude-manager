---
name: wiki-query
description: Wikiに蓄積された知識を検索・合成して質問に答える。有用な回答はsynthesis/に保存する。
user-invocable: true
---

# Wiki Query

wikiに蓄積された知識から質問に答える。

## トリガー

**明示的：**
- `/wiki-query <質問>` で呼ばれたとき
- 「wikiで調べて」「wikiに何かある？」と言われたとき

**自律的（`.claude/rules/wiki-integration.md` 参照）：**
- 「〜って何だっけ」等、既存知識を問う質問がDiscordで来たとき
- desk-research開始時の既存知識確認

## フロー

### 1. インデックスを読む

`wiki/index.md` を読み、質問に関連するページを特定する。

### 2. 関連ページを読む

特定したページを読み、回答に必要な情報を集める。

### 3. 回答を合成する

- 複数ソースからの情報は出典を明記
- 矛盾がある場合は両方の見解を提示
- wikiに情報がない場合は「wikiには該当情報なし」と明示

### 4. synthesis/への保存判定

以下のいずれかに該当する場合、`wiki/synthesis/` に保存する：
- 3ページ以上を横断した分析
- RQに紐づく問いへの回答
- ユーザーが「これ保存して」と言った場合

保存時は `wiki/SCHEMA.md` のsynthesisテンプレートに従い、index.md・log.mdを更新する。

### 5. 知識ギャップの報告

回答の過程で見つかった不足を報告し、ingest候補として提案する。
