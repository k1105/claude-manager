# システム運用ルール

## 時間認識（重要）

- **すべての対話において現在時刻を正しく把握すること**
- **`date` コマンドの出力はUTC。JSTにするには +9時間する。**（GCP VMのタイムゾーンがUTCのため）
- Discordメッセージの `ts` フィールドもUTC。JSTにするには +9時間
- screen logのタイムスタンプはJST（ローカルMacで生成されるため）。そのまま使う
- 時間に基づく判断を誤ると信頼を損なう
- 時刻を発言する前に必ず `date` コマンドで確認し、タイムゾーン変換してから使う

> **注意:** VMのタイムゾーンがUTC以外の場合は `.claude/rules/timezone.md` を編集してください。

## 自分にできること・できないこと

できる：コード書く、ファイル編集、情報検索、タスク管理、ログ記録、Discordでの対話
できない：物理操作（端末操作、検証、印刷、移動）、実体のない「準備」

→ できないことを「やっておく」と言わない。「待機してる、聞かれたら答える」で十分。

## ファイル構造

各ディレクトリには明確な役割がある。迷ったらこのルールに従う。

### tasks/ — 日次タスクリスト（消費型）
毎日のブリーフィングで生成。その日限り。

```
tasks/
  YYYY-MM-DD.md             # その日のタスクリスト（ブリーフィング完了の証）
```

### projects/ — プロジェクト単位のドキュメント（蓄積型）
進行中・過去含むプロジェクトの記録。1プロジェクト = 1ディレクトリ。リサーチもプロジェクト配下で管理。

```
projects/
  deadlines.md               # プロジェクト横断のデッドライン一覧
  _shared_research/          # 複数プロジェクト横断のリサーチ
    _questions.md            #   RQインデックス
    cross-pollination.md     #   異業種クロスポリネーション
    [topic-name]/            #   横断的リサーチテーマ
  _archive/                  # 完了したプロジェクト
  [project-name]/            # プロジェクトディレクトリ
    README.md                #   概要・定義（変更頻度：低）
    status.md                #   現在地・TODO・決定事項ログ（変更頻度：高）
    criteria.md              #   クライテリア（あるもののみ）
    research/                #   プロジェクト固有のリサーチ
    drafts/                  #   会議向け叩き台・資料原稿
    topics/                  #   並行する議題・サブテーマ
```

### logs/ — 記録・ログ（時系列の事実記録）
日次ログ、システムログ。すべて「何が起きたか」の記録。

```
logs/
  daily/
    YYYY-MM-DD.md            # 日次の会話・作業ログ
  weekly/
    weekly-YYYY-WNN.md       # 週次レビュー記録
  system/
    *.log                    # システムプロセスログ
  screen/
    YYYY-MM-DD.json          # スクリーンキャプチャログ（オプション）
  action_items.md            # Claudeの自己管理用アクション項目
```

**配置ルール:** `logs/` に置くもの = 時系列の事実記録。判断や方針は含めない。

### config/ — 設定ファイル
スケジューラーやシステムの動作設定。

```
config/
  cron_jobs.json             # 定期実行ジョブ定義
  channels.json              # Discordチャンネル設定
  daily_triggers.json        # その日の打ち合わせトリガー（ブリーフィング時に生成）
```

### docs/ — システムドキュメント（永続型）
システムの設計・運用ルール、ユーザープロファイル。

```
docs/
  profile.md                 # ユーザーについて（性格・特性・コミュニケーション）
  system.md                  # このファイル（システム運用ルール）
  principles.md              # 指針・学び・経験から得た方針（横断的）
  criteria_archive.md        # クライテリアワークショップのメタ知見（横断的）
```

### タスクのフォーマット

```markdown
# YYYY-MM-DD のタスク

## 今日の優先順位

1. [ ] タスク名（締め切り・背景）[project-name]
2. [ ] タスク名
3. [ ] タスク名

## 持ち越し

- [ ] 前日からの未完了タスク

## 完了

- [x] 完了したタスク
```

### 自動記録のトリガー

- **新しいタスクが出てきたとき** → `tasks/YYYY-MM-DD.md`に即座に追記
- **タスクが完了したとき** → 該当タスクを`[x]`に更新
- **重要な決定・気づきが出たとき** → `logs/daily/YYYY-MM-DD.md`に追記
- **プロジェクトに関する決定・進捗** → `projects/{name}/status.md`に追記（realtime-record.mdルール参照）

## スクリーンキャプチャ監視（オプション）

- `scripts/screen_monitor.py` がバックグラウンドで常時動作（別途セットアップが必要）
- 60秒間隔でスクリーンショットを取得 → AIで画面内容を事実ベースで記述
- `logs/screen/YYYY-MM-DD.json` に追記（判断・評価なし、事実のみ）
- **離脱判定はClaude Code側のcheckinスキルで実施** — screen logとタスクを照合して判断
- 離脱アラートはDiscordのalertチャンネルに送信

## Discordチャンネル構成

チャンネルIDは `config/channels.json` で管理する。

| チャンネル | 用途 |
|---|---|
| daily-briefing | デイリーブリーフィング・ウィークリーレビュー |
| lab | マネージャーシステムのディスカッション |
| alert | 離脱検知アラート |
| task-report | タスク完了報告 → タスクファイルを更新 |
| off-topic | 雑談・ニュース共有 |
| scheduler | 外部スケジューラーからの定期実行指示 |

## 定期実行

定期実行には2つの方式がある。環境に応じて選択する。

### 方式A: セッション内CronCreate + タイムテーブル（ローカル推奨）

- `CronCreate` で `*/10 * * * *` の単一cronをセッション起動時に登録
- 10分ごとに `config/cron_jobs.json` を参照し、該当するジョブを実行
- **制約:**
  - セッション再起動時にcronの再登録が必要
  - 7日で自動期限切れ（recurring jobs）
  - PCスリープ中はcronが停止。復帰後、30分以上過ぎたタスクはスキップ
  - ただし `daily-briefing` 等スキップ不可のジョブは時間に関係なく実行する

### 方式B: 外部スケジューラー + 別botアカウント（常時稼働推奨）

- 外部プロセス `scripts/scheduler.py` が**別のDiscord botアカウント**でschedulerチャンネルにcue（`📋 {job_name}`）を投稿
- Claude Code側が反応して処理し、完了後に ✅ リアクション
- 5分以内に ✅ がなければ最大3回まで再送
- **重要: Discordプラグインはwebhook由来のメッセージとbot自身のメッセージをinboundイベントとして配信しない。スケジューラーにはClaude Codeとは別のbotアカウントが必要**

### 共通

- ジョブ定義: `config/cron_jobs.json`
- Claude側の処理:
  1. cueまたはcronトリガーを受け取る
  2. `config/cron_jobs.json` でジョブ名に対応する `skill` フィールドを確認
  3. `.claude/skills/{skill}/SKILL.md` を読んで手順に従い実行

## 打ち合わせトリガー（daily_triggers.json）

毎朝のブリーフィングでカレンダーを確認した後、その日の打ち合わせに連動するトリガーを `config/daily_triggers.json` に書き出す。

- **生成タイミング**: ブリーフィングでカレンダー確認後、Claudeが自動生成
- **処理**: `scripts/scheduler.py` がメインループで読み込み、`time_utc` と現在時刻を比較して±1分以内なら発動
- **発動時**: schedulerチャンネルにpromptを投稿（cronジョブと同じ仕組み）
- **二重実行防止**: `fired` リストに実行済みトリガーを記録
- **日付リセット**: `date` フィールドで判定し、日付が変わったらスキップ

### トリガーの種類

| type | 用途 |
|---|---|
| `meeting_start` | 打ち合わせ5分前に通知 |
| `meeting_end` | 打ち合わせ終了後に `/meeting-debrief` スキルを実行 |
| `task_reminder` | タスクに時間制約がある場合のリマインド |

### ファイル形式

```json
{
  "date": "YYYY-MM-DD",
  "triggers": [
    {
      "time_utc": "YYYY-MM-DDTHH:MM:SSZ",
      "type": "meeting_start",
      "meeting": "打ち合わせ名",
      "prompt": "通知メッセージ or スキル実行指示"
    }
  ],
  "fired": []
}
```

## リサーチドキュメント

リサーチは全てプロジェクト配下で管理する。

- **プロジェクト固有のリサーチ** → `projects/{name}/research/`
- **複数プロジェクト横断のリサーチ** → `projects/_shared_research/`
- RQインデックス → `projects/_shared_research/_questions.md`
- 決定事項だけでなく、**中途の問い・ディスカッションの過程・仮説**も記録する
- 事実（調査結果）と内省（自分の考え・問い）を区別して書く
- 出典（著者/出典, 年, URL）を必ず付ける

## Obsidian連携

- 全てのmdファイルはObsidianで閲覧・編集可能
- ファイル間の参照には `[[wikilink]]` 形式を使う
- 積極的にリンクを張り、ナレッジグラフとしてネットワーク化する

## このシステムの設計思想

- ユーザーが「始める」必要があるのは起動だけ
- 記録・ログはすべて自動。人力ゼロを前提にする
- 使いながら改善していくシステム。気づいたことは随時このファイルに追記する
