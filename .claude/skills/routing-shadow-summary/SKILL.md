---
name: routing-shadow-summary
description: STT 振り分け shadow ログの日次サマリ。 routing_shadow_analyze.py で当日分を集計し、 結果を alert チャンネルに通知＆ stt-log に保存する。 毎日 23:01 JST（cron 表記は UTC 14:01）に cron から実行。
---

# routing-shadow-summary

タナカ部門の shadow 計測ログ（`~/.claude/stt-log/routing-shadow-YYYY-MM-DD.jsonl`）を
1 日分集計し、 件数 / hold 率 / diff 率（誤振り分け代理指標）/ confidence 分布 / 拮抗ケース上位を
出力する。 新ハイブリッドルータへの切替判断に使う観測データ。

## 仕様

- 対象: 実行日（JST）の `routing-shadow-YYYY-MM-DD.jsonl`
- 集計ツール: `/Users/htk/work-manager/tools/say-menubar/routing_shadow_analyze.py`
- 保存先: `~/.claude/stt-log/routing-shadow-summary-YYYY-MM-DD.txt`
- 通知先: Discord `alert` チャンネル（`config/channels.json` の `alert`）
- 集計対象が 0 件のときは alert に 1 行（「shadow log 0 件」）だけ流す

## 実行手順

1. `date` で当日（JST）を取得。 UTC 表記なら +9h 補正してから ISO 日付を組む。
2. shadow ログを集計（`--by-session` 付き）:

   ```sh
   /Users/htk/work-manager/tools/say-menubar/.venv/bin/python \
     /Users/htk/work-manager/tools/say-menubar/routing_shadow_analyze.py \
     --date <YYYY-MM-DD> --by-session > ~/.claude/stt-log/routing-shadow-summary-<YYYY-MM-DD>.txt
   ```

   - `.venv/bin/python` が無ければ `python3` に fallback
   - 標準出力をそのまま `routing-shadow-summary-YYYY-MM-DD.txt` に保存

3. Discord `alert` チャンネルに、 保存ファイルの中身を整形して通知:

   ```
   📊 routing shadow summary YYYY-MM-DD
   <件数行 + hold 率 + diff 率>
   <セッション別上位 3 件>
   詳細: ~/.claude/stt-log/routing-shadow-summary-YYYY-MM-DD.txt
   ```

   - Discord はコードブロック内に貼ると長くて見にくいので、 拮抗ケースとセッション別は上位 3 件に絞る
   - 通知本文は 1800 字以内（Discord 上限 2000 字に余裕を残す）
   - `config/channels.json` の `alert` チャンネル ID を読み込み、 plugin:discord 経由で投稿

4. 完了後、 scheduler メッセージに ✅ リアクションを付ける（方式 B のとき）。

## 失敗時

- 集計スクリプトが返り値 != 0 → alert に「routing-shadow-summary 失敗: <stderr 抜粋>」
- jsonl が 0 件 → 「shadow log 0 件（recorder 側で未稼働の可能性）」を 1 行通知
- 通知自体が失敗 → ローカル `routing-shadow-summary-YYYY-MM-DD.txt` は保存できているので静かに継続

## 触る正本

- 集計スクリプト: `/Users/htk/work-manager/tools/say-menubar/routing_shadow_analyze.py`
- ログ source: `~/.claude/stt-log/routing-shadow-YYYY-MM-DD.jsonl`
- サマリ保存: `~/.claude/stt-log/routing-shadow-summary-YYYY-MM-DD.txt`
- Discord チャンネル: `config/channels.json` の `alert`
- voice-recognition 部門の status: [[projects/voice-recognition/status]]
