---
paths:
  - "logs/screen/**"
  - "scripts/screen_monitor.py"
---

# スクリーンキャプチャ監視（オプション）

- `scripts/screen_monitor.py` がバックグラウンドで常時動作
- 60秒間隔でスクリーンショットを取得 → AIで画面内容を事実ベースで記述
- `logs/screen/YYYY-MM-DD.json` に追記（判断・評価なし、事実のみ）
- 離脱判定はClaude Code側のcronジョブで実施 — screen logとタスクを照合して判断
- 離脱アラートはDiscordのalertチャンネルに送信

> **注意:** スクリーンキャプチャ監視はオプション機能です。screen_monitor.pyは別途セットアップが必要です。
