---
name: desk-research
description: 自律的なデスクリサーチ。プロジェクト配下のリサーチや_shared_researchのRQに基づいて情報収集し、ドキュメントに追記する。
user-invocable: true
---

# デスクリサーチ

プロジェクト配下のリサーチや_shared_researchのRQに基づいて、自律的に情報収集し、ドキュメントに追記する。

## デスクリサーチ or クロスポリネーションの切り替え

毎時の実行時、`date +%s` の末尾1桁で判定する：
- **偶数** → 通常のデスクリサーチ（以下の手順）
- **奇数** → クロスポリネーション（`.claude/skills/cross-pollination/SKILL.md` の手順に従う）

## 手順（デスクリサーチ）

1. `projects/_shared_research/_questions.md` を読み、活動中のRQ一覧を確認
2. 各RQドキュメント（`projects/_shared_research/` および `projects/*/research/`）を読み、「未解決の問い」「調査すべきテーマ」を確認
3. `projects/*/status.md` の「Claudeが自律的にできること」にリサーチ系のタスクがあれば優先的に選ぶ。なければ最も情報が不足しているRQを1つ選ぶ
4. WebSearchで関連する情報を検索
5. 見つかった情報をRQドキュメントに追記（日付付き、事実と解釈を分けて）
6. 新しい問いが出てきたら「未解決の問い」に追加
7. 他のRQやプロジェクトファイルとの接続が見えたら[[wikilink]]で繋ぐ
8. リモートリポジトリと同期している場合は変更をgit push（ローカル完結の場合はスキップ）

## 原則

- **1回の実行で1つのRQに集中する**
- **事実と解釈を分ける**
- **出典を必ず明記する**（著者/出典, 年, URL）
- **量より質**
