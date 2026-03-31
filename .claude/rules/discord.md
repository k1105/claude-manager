# Discordチャンネル構成

チャンネルIDは `config/channels.json` で管理する。スキルやルールでチャンネルを参照するときは、`config/channels.json` を読んでIDを取得する。

| チャンネル | config key | 用途 |
|---|---|---|
| daily-briefing | `daily-briefing` | デイリーブリーフィング・ウィークリーレビュー |
| lab | `lab` | マネージャーシステムのディスカッション |
| alert | `alert` | 離脱検知アラート |
| task-report | `task-report` | タスク完了報告 → タスクファイルを更新 |
| off-topic | `off-topic` | 雑談・ニュース共有 |
| scheduler | `scheduler` | 外部スケジューラーからの定期実行指示 |
