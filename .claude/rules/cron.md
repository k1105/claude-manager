# 定期実行（外部スケジューラー）

schedulerチャンネルから `📋 {job_name}` というcueが来たら：

1. `config/cron_jobs.json` でジョブ名に対応する `skill` フィールドを確認
2. `.claude/skills/{skill}/SKILL.md` を読んで手順に従い実行
3. 完了したらメッセージに ✅ リアクション

ジョブ名とスキルの対応は `config/cron_jobs.json` を参照。
セッション内のCronCreateは使わない。すべて外部スケジューラー経由で実行する。
