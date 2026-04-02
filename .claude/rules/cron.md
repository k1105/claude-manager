# 定期実行

## 方式A: セッション内CronCreate（ローカル環境）

セッション開始時に `CronCreate` で `*/10 * * * *` を1つ登録する。
10分ごとに `config/cron_jobs.json` を参照し、現在時刻に該当するジョブのスキルを実行する。

- cron_jobs.jsonの時刻表記に注意: UTC表記の場合はJST変換が必要
- PCスリープ等で30分以上過ぎたジョブはスキップ（ただし `daily-briefing` はスキップ不可）
- セッション再起動時はcronの再登録を忘れない

## 方式B: 外部スケジューラー（常時稼働環境）

schedulerチャンネルから `📋 {job_name}` というcueが来たら：

1. `config/cron_jobs.json` でジョブ名に対応する `skill` フィールドを確認
2. `.claude/skills/{skill}/SKILL.md` を読んで手順に従い実行
3. 完了したらメッセージに ✅ リアクション

ジョブ名とスキルの対応は `config/cron_jobs.json` を参照。
