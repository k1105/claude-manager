---
name: work-tracker-sync
description: work-tracker DBの稼働エントリをzuuumy業務時間記載シート（Google Sheets）に同期する。毎日夜にcronから実行。
---

# work-tracker-sync

`/Users/htk/dev/work-tracker/work-tracker.db` の当月エントリを
`【ZuMy × 畑さん】業務時間記載シート` (spreadsheetId: `1Fe8VwbEUJk83xbTzKIEeksa3SINY4Nmj61Vt8XK8PUo`) に転記する。

## 仕様

- 対象: 当月（JST）の `stopped_at IS NOT NULL` なエントリ
- 粒度: 1日1行（同一日の複数エントリは集約）
  - 開始時間 = 最早 `started_at` （JST）
  - 終了時間 = 最遅 `stopped_at` （JST, 翌日にまたぐ場合は24h超表記）
  - 休憩時間 = span − 稼働合計
  - 稼動内容 = `#<issue_number>` の集合 + note/title
  - 稼働時間 = シート側で `=D-C-E`
- 除外issue: `339`（別途見積もり済み）
- 月タブが無ければ 2025/08 をテンプレートに複製して新規作成

## 実行

```sh
cd /Users/htk/dev/work-tracker && bun run scripts/sync-to-sheet.ts
```

引数で `YYYY-MM` を指定すると過去月も同期可能（例: `... scripts/sync-to-sheet.ts 2026-03`）。

## cron完了後

完了したら scheduler メッセージに ✅ リアクションを付ける。
失敗時は alert チャンネルにエラーを共有する。
gws認証切れなら `gws auth login` の手順（スマホ完結の手順は [[projects/zuuumy/status.md]] 参照）をユーザーに促す。
