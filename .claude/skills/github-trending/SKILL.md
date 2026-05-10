# github-trending

GitHubトレンドを取得し、関西弁の女子っぽい口調で要約してDiscordのoff-topicチャンネルに投稿する。

## 手順

1. `WebFetch` で `https://github.com/trending` を取得し、トップ10リポジトリを抽出する
   - リポジトリ名（owner/name）、言語、説明、本日のスター数
2. 関西弁の女子っぽい口調で要約を作成する
   - 各リポジトリにGitHubリンク（`https://github.com/{owner/name}`）を付ける
   - 技術的な内容をカジュアルにわかりやすく説明する
   - 全体の傾向についてひとこと添える
3. `config/channels.json` の `off-topic` チャンネルIDを取得し、Discord reply で投稿する

## フォーマット例

```
🔥 **今日のGitHubトレンド** （{月/日}）

{冒頭の一言}

**1. owner/name** ⭐{stars}/日
{関西弁での説明}
https://github.com/owner/name

...

---
{全体の傾向コメント}
```

## 口調ガイド

- 関西弁の女子っぽく（「〜やねん」「〜やな」「〜やん〜」「えぐない？」「ほんま」等）
- 技術に詳しい感じ、でもカジュアル
- 絵文字は控えめ（🔥と🚀くらい）
- wは使ってOK
