---
name: news-share
description: ニュース共有。ユーザーが興味ありそうなニュースや話題をoff-topicチャンネルに投稿する。
user-invocable: false
---

# ニュース共有

## 時間帯の判別

cueのジョブ名から時間帯を判別する：
- `news-morning` → 朝
- `news-noon` → 昼
- `news-night` → 夜

## 手順

1. `research/news_shared.md` を読み、過去に共有済みのURLとトピックを確認する
2. WebSearchで最新ニュースを検索する
3. 共有済みと重複しないものから、ユーザーが興味ありそうなものを1〜2件選ぶ
4. `config/channels.json` からoff-topicチャンネルIDを取得し、短くまとめて共有する。リンク付きで
5. 共有した内容を `research/news_shared.md` に追記する（トピック・URL・日付）

## 対象ジャンル

`docs/profile.md` の興味・関心を参照して、ユーザーに合ったジャンルを選ぶ。例：
- AI/テック
- クリエイティブ
- ユーザーの専門分野に関連する話題
- 日頃のタスクに関連する話題
