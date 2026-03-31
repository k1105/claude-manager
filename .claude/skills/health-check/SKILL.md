---
name: health-check
description: screen_monitorのヘルスチェック。ログ更新が止まっていればalertチャンネルに通知する。
user-invocable: false
---

# Screen Monitor ヘルスチェック

## 夜間スキップ

JST 0:00〜8:00 の間は何もしない（就寝中のため）。`date` でUTC確認 → +9時間してJSTが0〜8時なら即終了。

## 手順

0. まず `git pull` を実行して、ローカルPCからpushされた最新のscreen logを取得する。
1. `logs/screen/YYYY-MM-DD.json` の最終エントリのタイムスタンプを確認する
2. 現在時刻と比較して20分以上更新がなければ、ローカルPCのscreen_monitorが停止しているか、git pushが止まっている可能性がある
3. 20分以上更新がない場合：
   - `config/channels.json` からalertチャンネルIDを取得し、通知：「screen logが20分以上更新されていません」
4. 正常であれば何もしない（返答も不要）。
