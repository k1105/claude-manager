---
name: wiki-lint
description: Wikiの健全性チェック。孤立ページ・壊れたリンク・frontmatter不備・矛盾フラグ・鮮度を検出し修復する。
user-invocable: true
---

# Wiki Lint

wikiの健全性を定期チェックし、品質を維持する。

## トリガー

- cron（週1回、土曜 07:30 JST — project-scanの30分後）
- `/wiki-lint` で手動実行

## チェック項目と対応

| チェック | 自動修復 | 手動判断 |
|---|---|---|
| index.mdに未掲載のページ | ✅ 追加 | |
| 他ページからリンクなし（孤立） | ✅ 関連ページにリンク追加 | |
| `[[wikilink]]` 先が存在しない | | 作成候補リスト |
| frontmatter必須フィールド不足 | ✅ 補完 | |
| `> ⚠️ 矛盾` フラグの一覧 | | ユーザーに報告 |
| `updated` が90日以上前 | | 要レビューリスト |
| raw/に対応するsourcesページなし | | ingest候補リスト |

## 出力

```
🔍 Wiki Lint Report
- 自動修復: N件
- 作成候補: {ページリスト}
- 矛盾フラグ: N件
- 鮮度警告: N件
- 未処理raw: N件
```

修復した内容は `wiki/log.md` に記録する。
