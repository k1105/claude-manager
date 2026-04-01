# PC起動時にセッションを自動起動する

Mac起動時にClaude Codeセッションをバックグラウンドで自動起動する方法。

## 概要

PCを再起動してもClaude Codeが自動で立ち上がり、Discordでの対話が復旧する仕組み。

## 方法1: launchd（macOS推奨）

1. plistファイルを `~/Library/LaunchAgents/` に作成
2. `claude --channels plugin:discord@claude-plugins-official` を起動するよう設定
3. `launchctl load` で登録

## 方法2: screenコマンド

1. `.zshrc` や `.bash_profile` にscreen起動コマンドを追加
2. `screen -dmS claude claude --channels plugin:discord@claude-plugins-official`

## 注意

- 認証トークンの期限切れに注意
- セッションが異常終了した場合の再起動ロジックも検討する
