# LINE チャンネル運用

LINE は Discord と並ぶ双方向通信チャネル。外出先から LINE でマネージャーと会話できる。

## アーキテクチャ

```
LINE App → LINE Platform → Cloudflare Tunnel (persistent, 独立プロセス)
         → localhost:8787 → MCP server (Claude Code セッション内 subprocess)
```

- Cloudflare Tunnel は **Claude セッションと独立したバックグラウンドプロセス**
  - PID: `~/.claude/channels/line/tunnel.pid`
  - ログ: `~/.claude/channels/line/tunnel.log`
- MCP server は `.mcp.json` 経由で Claude Code セッションと同じ寿命
  - Claude セッションが生きている間のみ LINE メッセージを受信できる
  - セッション停止中に LINE からメッセージが来ても届かない（LINE 側は retry しない）

## 起動/再起動

**Tunnel が落ちている場合（Mac再起動後など）:**
```sh
cd ~/.claude/channels/line
nohup cloudflared tunnel --url http://localhost:8787 > tunnel.log 2>&1 &
echo $! > tunnel.pid; disown
```

URL が **変わる**ので、変わった場合は LINE Developers Console で Webhook URL を更新する。
（`grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' ~/.claude/channels/line/tunnel.log | head -1` で取得）

**Claude セッション起動時の channels フラグ:**
```sh
claude --dangerously-load-development-channels server:line
```

（プラグイン化すれば `--channels line` で使えるようになる — 将来課題）

## チャンネル ID

- **自分の userId**: `~/.claude/channels/line/access.json` の `allowFrom[0]`
- LINE は Discord のように「用途別チャンネル」を持てない（個人LINEは1対1）
  - 用途分けしたい場合: LINE グループを作って bot を招待、`access.json` の `groups` に登録

## MCP ツール

- `reply(chat_id, text, reply_to?)` — reply_to は inbound message_id。1分以内なら Reply API（無料）、過ぎたら Push API（月200通枠消費）
- `push(to, text)` — 明示的 Push
- `fetch_messages(chat_id, limit?)` — ローカル log から（LINE は履歴API非対応）
- `download_attachment(chat_id, message_id)` — 画像/動画/音声/ファイル

## 注意点

- **送信添付ファイルは未対応**（LINE は公開URLが必要）。将来対応
- **Reply token は1回・1分のみ**。長時間処理中は push に切り替わる
- **LINE Push 無料枠: 月200通**。超えると課金
- **reactions / message edit は LINE API 非対応**
