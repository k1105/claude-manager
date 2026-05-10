---
name: obsidian-link-fix
description: Obsidian風 `[[wikilink]]` の壊れたリンク・タイポを検出して修正する。case違い・slug差異の自動修正と、曖昧なものの候補提示。
user-invocable: true
---

# Obsidian Link Fix

`[[wikilink]]` 形式のリンクで「壊れてる」「ちょっとズレてる」ものを検出して直す。
wiki-lint の検出は弱い（候補提示まで）ので、本スキルが**実際の置換**まで実行する。

## トリガー

- `/obsidian-link-fix` で手動実行
- 引数で範囲を絞れる（例: `/obsidian-link-fix wiki/`、なしで `wiki/ projects/ docs/ raw/` 全体）

## 手順

### 1. インデックス構築

`wiki/` 配下の全 md ファイルからファイル名（拡張子なし）を集めて **正規 slug 集合** を作る。

```bash
find wiki -name "*.md" -type f | sed 's|.*/||; s|\.md$||' | sort -u
```

加えて、各ページの先頭 H1 を「**別名（alias）**」として記録（後述の matching に使う）。

### 2. リンク抽出

対象ディレクトリ（デフォルト `wiki/ projects/ docs/ raw/`）から `[[...]]` を全部抽出。
display alias 付き（`[[name|表示名]]`）と plain（`[[name]]`）両方拾う。

```bash
grep -rEn '\[\[[^]|#]+(\|[^]]+)?\]\]' --include='*.md' wiki/ projects/ docs/ raw/
```

heading anchor（`[[page#heading]]`）は heading 部分を分離して、ページ部分だけ resolve。

### 3. 解決と分類

各リンクのターゲット名を以下の順で判定：

| 段階 | 判定 | アクション |
|---|---|---|
| 1 | exact match in wiki slug 集合 | OK |
| 2 | case-fold match（`Zuuumy` → `zuuumy`） | **自動修正** |
| 3 | hyphen ↔ underscore ↔ space normalize match | **自動修正** |
| 4 | alias（H1 ヘッディング）一致 | **自動修正** または `[[slug\|alias]]` 形式に変換 |
| 5 | Levenshtein 距離 ≤ 2 の slug が **1つだけ** | 候補提示（自動修正は user 確認後） |
| 6 | 距離 ≤ 2 の slug が複数 / それ以上ズレ | **手動判断**として report |
| 7 | どこにも該当なし | **新規ページ作成候補** or **削除候補** として report |

### 4. 修正と報告

- **段階 2-4** はファイル直接編集（バックアップとして diff を `wiki/log.md` に記録）
- **段階 5-7** は report として出力、ユーザー確認後に修正

### 5. 出力フォーマット

```
🔗 Obsidian Link Fix Report (2026-05-03)

✅ 自動修正: N件
- {file}:{line}  [[Zuuumy]] → [[zuuumy]]  (case-fold)
- {file}:{line}  [[zuuumy_v2]] → [[zuuumy-v2]]  (normalize)

⚠️ 候補提示（要確認）: N件
- {file}:{line}  [[zuuum-v2]] → [[zuuumy-v2]] ?  (距離=1)

❌ 解決不能: N件
- {file}:{line}  [[unknown-page]]  → 新規作成 or 削除？
```

修正した内容は `wiki/log.md` に「YYYY-MM-DD obsidian-link-fix」セクションで追記。

## 注意

- **markdown style リンク `[text](path.md)` はスコープ外**（別 skill で扱う）
- `wiki/` 以外への wikilink（例: projects 内 `[[deadlines]]`）も解決対象に入れる。projects/ 配下の md も slug 集合に含めるオプションを持つ
- frontmatter 内の wikilink は触らない（人間が手で書いた fragile なもの）
- コードブロック内（```...```）の wikilink は触らない（例示の可能性）
- 大量修正になる場合は **dry-run 結果を最初に提示してから user 確認** を取る
