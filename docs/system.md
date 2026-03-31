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

```
tasks/
  YYYY-MM-DD.md        # 今日のタスクリスト（ブリーフィング完了の証）
  timetable-YYYY-MM-DD.md  # その日のタイムライン（独立管理）
projects/
  _principles.md       # 指針・学び・経験から得た方針
  [project-name].md    # プロジェクトごとのドキュメント
plans/
  goals.md             # プロジェクト一覧インデックス
  weekly-YYYY-WNN.md   # 週次レビュー記録
config/
  cron_jobs.json       # 定期実行ジョブ定義
  channels.json        # Discordチャンネル設定
  daily_triggers.json  # その日の打ち合わせトリガー（ブリーフィング時に生成）
logs/
  YYYY-MM-DD.md        # 今日の会話・作業ログ
  screen/
    YYYY-MM-DD.json    # スクリーンキャプチャログ（オプション）
docs/
  profile.md           # ユーザーについて（性格・特性・コミュニケーション原則）
  system.md            # このファイル（システム運用ルール）
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
- **重要な決定・気づきが出たとき** → `logs/YYYY-MM-DD.md`に追記

## スクリーンキャプチャ監視（オプション）

- `scripts/screen_monitor.py` がバックグラウンドで常時動作（別途セットアップが必要）
- 60秒間隔でスクリーンショットを取得 → AIで画面内容を事実ベースで記述
- `logs/screen/YYYY-MM-DD.json` に追記（判断・評価なし、事実のみ）
- **離脱判定はClaude Code側のcronジョブで実施** — screen logとタスクを照合して判断
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

## 定期実行（外部スケジューラー）

定期実行は外部プロセス `scripts/scheduler.py` が担当する。

- ジョブ定義: `config/cron_jobs.json`
- 仕組み: cronスケジュールに従い、schedulerチャンネルに短いcue（`📋 {job_name}`）だけを投稿する
- Claude側の処理:
  1. schedulerチャンネルから `📋 {job_name}` を受け取る
  2. `config/cron_jobs.json` でジョブ名に対応する `skill` フィールドを確認
  3. `.claude/skills/{skill}/SKILL.md` を読んで手順に従い実行
  4. 完了後にそのメッセージに ✅ リアクションをつける
- 再送: Claudeが5分以内に ✅ をつけなければ、スケジューラーが最大3回まで再送する
- セッション内のCronCreateは使わない。すべて外部スケジューラー経由で実行する

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

`research/` ディレクトリに、調査・研究・思考の過程を記録する。

- **トピック単位でファイルを作る**（例：`research/topic-name.md`）
- 決定事項だけでなく、**中途の問い・ディスカッションの過程・仮説**も記録する
- 事実（調査結果）と内省（自分の考え・問い）を区別して書く
- Obsidianのwikilinkで他のファイル（プロジェクト、principles等）と接続する
- 定期的にアクセスして育てる。完成させるのではなく、継続的に深掘りする

## Obsidian連携

- 全てのmdファイルはObsidianで閲覧・編集可能
- ファイル間の参照には `[[wikilink]]` 形式を使う
- 積極的にリンクを張り、ナレッジグラフとしてネットワーク化する

## このシステムの設計思想

- ユーザーが「始める」必要があるのは起動だけ
- 記録・ログはすべて自動。人力ゼロを前提にする
- 使いながら改善していくシステム。気づいたことは随時このファイルに追記する
