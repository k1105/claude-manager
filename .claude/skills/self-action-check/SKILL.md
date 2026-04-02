---
name: self-action-check
description: 自分（Claude）が「あとでやる」と言ったことの実施チェック。
user-invocable: false
---

# 自己アクションチェック

## 手順

1. 直近の会話で「あとでやる」「後回し」「今週のどこかで」等と言ったが、まだ実行していないことがないか確認する
2. `logs/action_items.md` に未処理のアクション項目がないか確認する
3. 実行可能なものがあれば、最も優先度が高い1件に取り組む
4. 取り組んだ結果を `config/channels.json` のlabチャンネルに報告する
5. 何もなければ何もしない（返答も不要）
