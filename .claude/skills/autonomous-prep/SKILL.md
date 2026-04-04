---
name: autonomous-prep
description: デッドライン駆動の自律準備。会議や提出物に向けて、論点整理・現状可視化・情報収集を行う。
user-invocable: true
---

# 自律準備（Autonomous Prep）

デッドラインから逆算し、会議や提出物に向けてClaude側でできる準備を自律的に実行する。

## トリガー

- project-scanで「デッドライン接近 + 準備不足」が検出された場合
- meeting-debriefで「次回に向けた準備」が発生した場合
- 手動で `/autonomous-prep {project-name}` で呼び出し

## 手順

1. 対象プロジェクトの `status.md` を読む
2. `projects/deadlines.md` から次のデッドラインを確認
3. 「ゴールとのギャップ」と「Claudeが自律的にできること」を確認
4. 以下のうち、該当するものを実行：

### A. 論点整理
- status.mdの「未解決の問い・課題」を構造化
- 「次の会議/議論で決めるべきこと」をリスト化
- `projects/{name}/drafts/YYYY-MM-DD_prep.md` に書き出す

### B. 現状の可視化
- status.mdの情報を整理し、「今どこにいて、何が足りないか」を簡潔にまとめる
- criteria.mdがあれば、各項目の達成状況を照合

### C. 情報収集
- 論点に必要な事例・データ・先行事例をWebSearchで調査
- 見つかった情報を `projects/{name}/research/` または `drafts/` に追記
- 出典を必ず明記

5. 準備した内容を `status.md` の「Claudeが自律的にできること」に反映（完了チェック）
6. Discord labチャンネル（`config/channels.json` から取得）に報告：「{project}の{deadline}に向けて、{何をした}。drafts/{file}に書いた」

## やらないこと

- アイデアを考える
- 叩き台の「内容」を作る（構成・フォーマットは整えるが、中身のアイデアはユーザーの仕事）
- 「こうすべき」という方針判断

**材料を揃える。判断はユーザーに委ねる。**

## 注意

- 1回の実行で1プロジェクトに集中する
- 準備した内容は必ずファイルに残す（会話だけで終わらせない）
- ユーザーがすぐディスカッションに入れる状態を作ることがゴール
