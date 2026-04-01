# セットアップ未完了の自動検知

セッション起動時、以下の条件を満たす場合は **セットアップが途中である**。
ユーザーの最初のメッセージに応答する前に状態を確認し、`/setup-discord` スキルを実行すること。

## 判定条件

1. `~/.claude/channels/discord/.env` の `DISCORD_BOT_TOKEN` が設定済み
2. かつ、以下のいずれか：
   - `~/.claude/channels/discord/access.json` の `allowFrom` が空 → ペアリング未完了
   - `config/channels.json` の全キーが空文字 → チャンネル未設定（仮設定含む）

上記に該当する場合、ユーザーに「セットアップの続きですね」と伝えて `/setup-discord` を実行する。
