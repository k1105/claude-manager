---
name: work-tracker-start
description: zuuumy作業時間トラッカー (Hono+Bun) を起動する。既に起動していればno-op。手動でユーザーから「work-tracker起動して」と頼まれたら呼ぶ。
---

# work-tracker-start

`/Users/htk/dev/work-tracker/` のサーバを起動する。
URL: http://127.0.0.1:3456/ （※ `localhost` は Chrome が IPv6 優先でコケるので IPv4 指定必須）

## 手順

1. **既存プロセスチェック**: `lsof -iTCP:3456 -sTCP:LISTEN`
   - すでに `bun` が listening ならそのまま「起動済み」と報告して終了。再起動はしない（アクティブセッションを潰すリスク）。
   - `curl -s http://127.0.0.1:3456/api/active` でアプリレベルでも応答することを確認する。

2. **起動**: 何も listening していなければ、以下を実行：
   ```sh
   cd /Users/htk/dev/work-tracker && nohup bun run src/index.ts > /tmp/work-tracker.log 2>&1 &
   disown
   ```
   - `&` でバックグラウンド + `disown` でセッション切断後も生存させる
   - ログは `/tmp/work-tracker.log`

3. **起動確認**:
   - 1〜2秒待ってから `curl -s -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:3456/`
   - HTTP 200 なら成功。違えば `/tmp/work-tracker.log` を読んで原因を特定する。

4. **報告**: Discord channels.json の `lab` か呼び出し元チャネルに「起動した（PID: xxx）」または「すでに起動中」と短く返す。

## 再起動が必要なケース

`src/index.ts` を編集した後など、コード変更を反映したいときだけ：

```sh
# 安全確認
curl -s http://127.0.0.1:3456/api/active   # null ならアクティブセッションなし
# 再起動
kill <PID> && sleep 1 && cd /Users/htk/dev/work-tracker && nohup bun run src/index.ts > /tmp/work-tracker.log 2>&1 & disown
```

アクティブセッションがあるときは必ず先にユーザーに確認する（タイマーを失わないため）。

## 関連

- 同期 cron: skill `work-tracker-sync`（毎晩23:00 JST、`config/cron_jobs.json`）
- DB: `/Users/htk/dev/work-tracker/work-tracker.db`
- Mac再起動後にこのスキルを毎回呼ぶ運用にしてもよい（cronに `@reboot` 相当を入れるなら別途検討）
