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

## 設計思想

**記録駆動型マネージャー。** 会話で決まったことは即座にファイルに書き、プロジェクトの穴をstatus.mdで構造的に可視化する。2つの大方針：

1. **ユーザーの脳を駆動する** -- プロジェクトの「穴」を見つけて突く。問いを投げて思考を引き出す
2. **自律実行を最大化する** -- 調査・整理・情報収集はClaudeが自律的に進める。アイデアを考えるのはユーザーの仕事

## 何ができるか

- **デイリーブリーフィング** -- 毎朝、今日のタスクと優先順位を一緒に決める
- **チェックイン** -- 2-3時間おきに進捗を確認し、分岐点で声をかける（離脱判定を統合）
- **打ち合わせデブリーフ** -- 会議後にTODOと決定事項を回収・記録する
- **離脱アラート**（オプション） -- タスクと無関係な活動が続いたときに穏やかに通知する
- **プロジェクトスキャン** -- 週1回、全プロジェクトの穴を見つけて報告する
- **自律準備** -- デッドライン駆動で論点整理・情報収集を自律実行する
- **自律リサーチ** -- 興味のあるテーマを自動的に調べてドキュメントに蓄積する
- **ニュース共有** -- 興味に合ったニュースを1日3回共有する
- **プロジェクト管理** -- プロジェクトファイルの作成・レビュー・更新を支援する
- **ゴール駆動ディスカッション** -- status.mdのゴールとギャップに照らして議論する

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
  logs/
    daily/               # 日次の会話・作業ログ
    weekly/              # 週次レビュー記録
    system/              # システムプロセスログ
    screen/              # スクリーンキャプチャログ（オプション）
  projects/
    deadlines.md         # 全プロジェクト横断のデッドライン一覧
    _shared_research/    # 横断リサーチ（RQ、クロスポリネーション）
    _archive/            # 完了したプロジェクト
    [project-name]/      # プロジェクト単位（status.md, research/, drafts/, topics/)
  docs/
    principles.md        # 指針・学び
    criteria_archive.md  # プロジェクト評価基準のメタ知見
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
| `/desk-research`     | 自律デスクリサーチ               | OK           |
| `/project-scan`      | 全プロジェクト横断スキャン       | OK           |
| `/autonomous-prep`   | デッドライン駆動の自律準備       | OK           |
| `/session-start`     | セッション開始セルフチェック     | OK           |
| `/weekly-review`     | 週次レビュー                     | OK           |
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
