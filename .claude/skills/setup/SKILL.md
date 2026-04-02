---
name: setup
description: 初回セットアップ（Phase 1）。環境チェック・Bot作成・トークン設定まで。セッション再起動後は /setup-discord が自動で引き継ぐ。
user-invocable: true
---

# 初回セットアップ（Phase 1: ターミナル）

このシステムを初めて使うときに実行する。
**このスキルはターミナル上で完結する。** Discord上での対話確立は Phase 2（`/setup-discord`）で行う。

## 全体の流れ（3フェーズ）

1. **Phase 1（このスキル `/setup`）** — ターミナルで実施
   - 環境チェック（bun、Discordプラグイン）
   - 挨拶・名前の取得
   - Bot作成・トークン設定
   - → セッション再起動を案内
2. **Phase 2（`/setup-discord`）** — 再起動後、自動実行
   - DMペアリング
   - 「一般」チャンネルでの対話開始
   - プロフィール収集（Discord上で）
3. **Phase 3（`/setup-channels`）** — Discord上で実施
   - 用途別チャンネルの作成・ID登録

## フロー

### 1. 環境チェック（自動・無言で）

ユーザーに声をかける前に、以下を確認する：

1. **bunがインストールされているか**
   - `which bun` を実行
   - なければユーザーに伝える：「Discordプラグインの動作にbunが必要です。インストールしてよいですか？」
   - 許可を得たら `curl -fsSL https://bun.sh/install | bash` を実行
2. **Discordプラグインがインストールされているか**
   - `/mcp` でプラグイン一覧を確認
   - `plugin:discord:discord` がなければ：「Discordプラグインをインストールします」と伝え、`/plugin install discord@claude-plugins-official` を案内

環境が整ったらステップ2へ。

### 2. 挨拶と説明（短く）

```
はじめまして。あなた専用のAIマネージャーです。

- 毎朝のブリーフィングでタスクを整理
- 日中のチェックインで進捗確認
- 打ち合わせ後のTODO回収
- リサーチや情報収集の自律実行

まずDiscordで話せるようにします。お名前を教えてください（ニックネームでOK）。
```

名前を受け取ったら `docs/profile.md` の名前だけ埋めて、すぐステップ3へ。

### 3. Bot作成・トークン設定

一度に全手順を提示する（ステップごとに分割して待たない）：

```
以下の手順でDiscord botを作成してください：

1. Discordでサーバーを新規作成（既存サーバーでもOK）
2. Discord Developer Portal（https://discord.com/developers/applications）を開く
3. 「New Application」→ 名前をつけて作成
4. 左メニュー「Bot」→ 以下を設定：
   - 「Privileged Gateway Intents」で MESSAGE CONTENT INTENT、SERVER MEMBERS INTENT、PRESENCE INTENT を全てON
   - 「Reset Token」でトークンをコピー（一度しか表示されません）
5. 左メニュー「OAuth2」→「URL Generator」：
   - Scopesで「bot」を選択
   - Bot Permissionsで以下を選択：
     - View Channels
     - Send Messages
     - Send Messages in Threads
     - Read Message History
     - Attach Files
     - Add Reactions
   - 生成されたURLをブラウザで開き、サーバーに招待

💡 後でチャンネルIDを取得するために、Discordの開発者モードをONにしてください：
   「ユーザー設定」→「アプリの設定」→「詳細設定」→「開発者モード」をON
   （これがONでないとチャンネルIDをコピーできません）

全部できたらトークンを貼ってください。
```

### 4. トークン保存

トークンを受け取ったら `/discord:configure <token>` スキルで設定する。

### 5. セッション再起動の案内

```
トークンを保存しました。

Discordで対話するために、セッションを再起動する必要があります。
以下のコマンドで起動し直してください：

claude --channels plugin:discord@claude-plugins-official

起動したら、DiscordでbotにDMを送ってください。
ペアリングコードが返ってきたら、セットアップの続きが自動で始まります。
```

**ここでPhase 1は終了。**
Phase 2は再起動後のセッションで自動的に引き継がれる（`.claude/rules/setup-detect.md` がセットアップ未完了を検知し、`/setup-discord` を実行する）。

## トラブルシュート

### MCPサーバーがfailedになる場合

1. **Intentsの確認**: Developer Portal → Bot → Privileged Gateway Intentsで3つ全てONか
2. **トークンの確認**: Developer Portal → Bot → Reset Tokenで再生成
3. **起動フラグの確認**: `claude --channels plugin:discord@claude-plugins-official` で起動しているか
4. **エラーの確認**: `--debug` フラグをつけて起動し、discord関連のエラーを確認

## 注意

- 環境チェックは先に、静かに行う。ユーザーの手を煩わせない
- Bot権限に「Manage Channels」は不要（botはチャンネルを作成できない）
- このフェーズではプロフィールを詳しく聞かない。名前だけ
