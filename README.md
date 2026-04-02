# Claude Manager - あなた専属のAIマネージャー

Claude Code上で動作する、対話を通じて自己改善していく専属AIマネージャーシステムです。

## クイックスタート

```bash
# 1. リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/claude-manager.git
cd claude-manager

# 2. Claude Codeを起動
claude

# 3. セットアップを開始
# Claude Codeの中で、次のように話しかけてください：
セットアップを始めたい
# または
/setup
```

セットアップスキルが環境チェック（bun・Discordプラグイン）、Bot作成、プロフィール収集を対話形式でガイドします。

## 何ができるか

- **デイリーブリーフィング** -- 毎朝、今日のタスクと優先順位を一緒に決める
- **チェックイン** -- 2-3時間おきに進捗を確認し、分岐点で声をかける
- **打ち合わせデブリーフ** -- 会議後にTODOと決定事項を回収・記録する
- **離脱アラート**（オプション） -- タスクと無関係な活動が続いたときに穏やかに通知する
- **自律リサーチ** -- 興味のあるテーマを自動的に調べてドキュメントに蓄積する
- **ニュース共有** -- 興味に合ったニュースを1日3回共有する
- **プロジェクト管理** -- プロジェクトファイルの作成・レビュー・更新を支援する
- **クライテリア・ワークショップ** -- 9つの問いで企画を構造的に整理する

## コミュニケーション設計

- **「今これをやろう、なぜならXだから」** -- 根拠のある提案をする
- **一度に1つ** -- 最優先の1つを明確にする
- **責めない** -- 事実を伝えて、次の一手を示す
- **記録は全自動** -- 人力ゼロを前提にする
- **対話を通じて改善** -- ユーザーのフィードバックを学習し、マネジメントスタイルを継続的に適応させる

## 必要なもの

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [bun](https://bun.sh/) — Discordプラグインの動作に必要
- Discordアカウントとサーバー（bot連携用）
- GCP VM等の常時稼働環境（推奨）

## ファイル構造

```
claude-manager/
  CLAUDE.md              # マネージャーの人格・コミュニケーション原則
  docs/
    profile.md           # ユーザープロフィール（セットアップで生成）
    system.md            # システム運用ルール
  .claude/
    rules/               # Claude Codeのルール（自動読み込み）
    skills/              # スキル定義（/コマンドで呼び出し可能）
  config/
    channels.json        # DiscordチャンネルID
    cron_jobs.json       # 定期実行ジョブ
    daily_triggers.json  # その日の打ち合わせトリガー
  tasks/                 # 日次タスクファイル
  logs/                  # 会話・作業ログ
  projects/              # プロジェクトドキュメント
  research/              # リサーチドキュメント
  plans/                 # 長期目標・週次レビュー
```

## スキル一覧

| スキル               | 説明                             | 手動呼び出し |
| -------------------- | -------------------------------- | ------------ |
| `/setup`             | 初回セットアップ                 | OK           |
| `/briefing`          | デイリーブリーフィング           | OK           |
| `/checkin`           | タスク進捗チェックイン           | OK           |
| `/end-of-day`        | 1日のサマリー・引き継ぎ          | OK           |
| `/meeting-debrief`   | 打ち合わせ後のTODO回収           | OK           |
| `/project-create`    | プロジェクトファイル作成         | OK           |
| `/project-review`    | プロジェクトレビュー             | OK           |
| `/research-note`     | リサーチノート作成               | OK           |
| `/criteria-workshop` | クライテリア・ワークショップ     | OK           |
| `/desk-research`     | 自律デスクリサーチ               | OK           |
| `screen-log-check`   | 離脱チェック（自動）             | -            |
| `health-check`       | screen monitor監視（自動）       | -            |
| `self-action-check`  | Claude自身のTODOチェック（自動） | -            |
| `news-share`         | ニュース共有（自動）             | -            |
| `cross-pollination`  | 異業種インスピレーション（自動） | -            |

## 定期実行

定期実行には2つの方式があります：

### 方式A: セッション内CronCreate + タイムテーブル（ローカル推奨）

外部プロセスなしで動作。セッション起動時に `CronCreate` で10分間隔のcronを1つ登録し、`config/cron_jobs.json` に基づいてタスクを実行します。

- **メリット**: 追加セットアップ不要
- **制約**: セッション再起動時にcronの再登録が必要。7日で自動期限切れ。PCスリープ中は停止

### 方式B: 外部スケジューラー + 別botアカウント（常時稼働推奨）

`scripts/scheduler.py` が別のDiscord botアカウントでschedulerチャンネルにcueを投稿し、Claude Codeが反応して処理します。

- **メリット**: セッション再起動に依存しない
- **制約**: **Claude Codeのbot自身が投稿したメッセージやwebhookメッセージはDiscordプラグインに配信されない**ため、スケジューラー用に別のbotアカウントが必要

詳細は `docs/system.md` を参照してください。

## Obsidian連携

全てのmdファイルはObsidianで閲覧・編集可能です。`[[wikilink]]` 形式でファイル間を接続し、ナレッジグラフとして活用できます。

## カスタマイズ

- `CLAUDE.md` -- マネージャーの人格・トーンを調整
- `docs/profile.md` -- ユーザー情報を更新
- `.claude/rules/timezone.md` -- タイムゾーンの設定
- `config/cron_jobs.json` -- 定期実行のスケジュール調整
- `.claude/skills/*/SKILL.md` -- 各スキルの動作をカスタマイズ

## ライセンス

MIT License
