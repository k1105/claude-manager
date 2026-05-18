# 会話中の決定事項をファイルに即時記録する

## 原則

会話の中で決まったこと・新しい情報が出たら、**会話のまとまりができた段階で**関連ファイルに追記する。end-of-dayまで先送りしない。

「会話のまとまり」とは：話題が一区切りついたタイミング。次の話題に移る前、またはユーザーの承認・確認が得られた時点。

## 記録先の振り分け

| 情報の性質 | 記録先 |
|---|---|
| プロジェクトに紐付く決定事項・TODO・日程 | `projects/{project}/` の該当ファイル |
| タスクの追加・完了・変更 | `tasks/YYYY-MM-DD.md` |
| 中長期のデッドライン | `projects/deadlines.md` |
| 指針・方針レベルの決定 | `docs/principles.md` |
| システム改善に関する議論 | `projects/manager-system/` の該当ファイル（or 相当するプロジェクト） |
| 上記に該当しない会話ログ | `logs/daily/YYYY-MM-DD.md` |

## 記録のタイミング

- **何かが決まったとき** — 方針、日程、TODO、優先度の変更
- **話題が変わるとき** — 次の話題に移る前に、前の話題の結論を書く
- **未決事項が明らかになったとき** — 「決まっていないこと」も記録する（open questions）
- **中間成果物が出たとき** — 20案出して6案に絞った、のような過程も記録

## 禁止事項

- 「あとでまとめて書く」「end-of-dayで反映する」は禁止
- 会話の中で出た具体的な数字・日付・人名・方針は、記憶に頼らずファイルに書く

## wikilink を必ず張る（Obsidianグラフ駆動）

ファイルを書くとき、関連する他ファイル・プロジェクトには **`[[wikilink]]` 形式**で参照を入れる。プレーンなパス文字列（`projects/xxx/status.md`）だけだと Obsidian のグラフ・バックリンクに乗らない。

### 必須シーン

- **logs/daily/YYYY-MM-DD.md** を書くとき：その日触れた全プロジェクトに `[[projects/xxx/status]]` をファイル冒頭の「関連:」行で張る
- **projects/{A}/** から **projects/{B}/** に影響がある時：両方向で `[[projects/{B}/status]]` 等を張る（cross-link）
- **research/** や **drafts/** から元プロジェクトの status へリンクを張る
- **logs/daily 内で使う日付参照**は `[[2026-05-01]]` 形式で（裸の文字列にしない）
- **wiki/** 系（concepts / entities / sources / synthesis）は SCHEMA に従う

### 書き方の例

```markdown
---
tags:
  - log
  - log/daily
---

# 2026-05-06

関連: [[projects/money-plan/status]] / [[projects/polymarket-bot/status]] / [[projects/trading-bot/status]]

## kado MVP-0 ローカル起動
...
```

### NG パターン

- ❌ `詳細は projects/trading-bot/status.md の「次に再開〜」` （プレーンパス、リンクされない）
- ✅ `詳細は [[projects/trading-bot/status]] の「次に再開〜」`

### 効果

- グラフビューで projects 間の関係性が可視化される
- バックリンクで「このプロジェクトに触れた日付」を即座に追える
- 検索だけに頼らず構造でナビゲートできる
