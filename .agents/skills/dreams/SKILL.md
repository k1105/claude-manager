---
name: dreams
description: Wikiに「夢を見させる」。頼まれずに wiki/ を彷徨い、繰り返すテーマ・隠れた矛盾・遠縁ページの意外な接続を1つだけ拾って synthesis ページの draft を書く。深夜cronまたは /dreams で起動。
user-invocable: true
---

# Dreams

`wiki-query` が「明示的な問いに答える」のに対し、`dreams` は**問いを与えられずに wiki を歩き、つながりを見つける**。Karpathy原典には無い、派生コミュニティの拡張パターン（ghelburlabs "synthesis pass"）。

## トリガー

- cron（深夜、JST 02:00 推奨。end-of-dayと朝briefingの間）
- `/dreams` 手動起動
- `/dreams keep <slug>` / `/dreams discard <slug>` で draft の昇格・破棄

## 原則

- **1回1夢**。ノイズになるので量を出さない
- **頼まれずに synthesis を書く**ことが本質。だが**24h は draft 状態で hold** する
- 自動修復はしない。lintとは役割を分ける（lintは健全性、dreamsは創発）

## フロー

### 1. 種を選ぶ

以下のいずれかから 5-10 ページを集める：

- 直近7日に updated されたページ（`wiki/log.md` を遡る）
- 直近 ingest した sources/
- 既存の synthesis/ で言及頻度の高いentity・concept

### 2. グラフを歩く

種ページから `[[wikilink]]` を 2-3 hop 辿り、**遠縁ページ集合**を作る。直接リンクされているだけのペアは「既に分かっている」ので除外、間接的に届くペアを優先する。

### 3. 1つだけ拾う

集合に対し以下のレンズで眺め、最も鋭いもの**1つ**を選ぶ：

- **繰り返すテーマ** — 別文脈で同じ構造が出ている（例: 異なるプロジェクトに共通する設計判断）
- **隠れた矛盾** — ある entity の方針と別の場所の決定がズレている
- **遠縁の接続** — 無関係に見えて同じ問題を別角度で扱っている2ページ

迷ったら**書かない**。鋭くないなら出さない方が良い。

### 4. dream-draft を書く

`wiki/synthesis/dream-YYYY-MM-DD-{slug}.md`：

```yaml
---
title: {夢のタイトル}
type: synthesis
status: dream-draft
born: YYYY-MM-DD HH:MM
sources: [wiki/path/a.md, wiki/path/b.md, ...]
tags: [dream]
---
```

本文：

- **見たもの**（1-2文で何を発見したか）
- **辿った道**（どのページからどう繋いだか — 後で検証可能に）
- **次の問い**（このつながりが本物なら何を調べるべきか）

### 5. 通知

- `wiki/log.md` に `[dream] {slug}` を追記
- 翌朝の briefing で「昨夜の dream: {タイトル} — keep / discard?」として提示（briefing側は `wiki/synthesis/` の `status: dream-draft` を拾う）

### 6. 昇格・破棄

- `/dreams keep <slug>` → frontmatter から `status` `born` を外し、index.md の Synthesis セクションに追加
- `/dreams discard <slug>` → `wiki/archive/dreams/` に移動
- 24h 経過しても判断がない draft → 翌 briefing で再掲。自動削除はしない

## 出力フォーマット（実行時）

```
🌙 Dream
種: {種に使ったページ数}件 / 歩いた範囲: {遠縁集合のページ数}件
発見: {1-2文}
保存: wiki/synthesis/dream-YYYY-MM-DD-{slug}.md (status: dream-draft)
```

鋭いものが見つからなかった場合：

```
🌙 Dream
今夜は何も見えなかった。
```

## やらないこと

- 既存ページの編集（lintとingestの仕事）
- 複数の dream を一晩で書く
- ユーザー承認なしの synthesis 正規化
