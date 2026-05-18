# 別Mac への移植手順

このリポジトリと付随する `~/.claude/` を、別の Mac でも動かすための手順。

## 全体像

3層に分けて持っていく。

1. **repo 本体** — `git clone` で済む
2. **Dropbox vault** — Dropbox.app を入れて sync すれば自動で揃う（`projects/`, `wiki/`, `logs/`, `raw/`, `tasks/`, `docs/`, `handoff/` の中身）
3. **`~/.claude/`** — Dropbox にも git にも入っていない。**旧Mac から rsync する必要がある**

トークン・アプリ・launchd は手作業。

## クイックスタート

### 旧Mac でやること

1. Discord/LINE bot を**そのまま共有しない**場合は事前に新規 bot を作る（後述）
2. `~/.claude/` を新Macへ転送する（下の rsync コマンド参照）

### 新Mac でやること

```sh
# 1. 依存を入れる
brew install gh jq tmux cloudflared rsync
curl -fsSL https://bun.sh/install | bash
# Claude Code 本体: https://docs.claude.com/claude-code

# 2. Dropbox.app を起動し、CloudOptionDJteam team を sync 完了まで待つ
#    確認: ~/Library/CloudStorage/Dropbox-CloudOptionDJteam/ですはた/HTK/HTK が見えること

# 3. repo を clone
mkdir -p ~/dev && cd ~/dev
git clone https://github.com/k1105/claude-manager.git
cd claude-manager

# 4. Dropbox dir への symlink を張る
./scripts/bootstrap-new-mac.sh

# 5. 現状を診断
./scripts/check-new-mac.sh
```

`check-new-mac.sh` の出力で `NG` が残った箇所を、以降の節に従って埋める。

## `~/.claude/` の rsync

旧Mac で実行する。`NEW_MAC` は新Mac の hostname か IP（ssh で届くこと）。

```sh
# 安全な範囲（メモリ・スキル・hooks・bin・avatar・設定）
rsync -avh --progress \
  --exclude '_archive/' \
  --exclude 'backups/' \
  --exclude 'cache/' \
  --exclude 'image-cache/' \
  --exclude 'paste-cache/' \
  --exclude 'downloads/' \
  --exclude 'file-history/' \
  --exclude 'history.jsonl' \
  --exclude 'menubar.log' \
  --exclude 'say-daemon.log' \
  --exclude 'sessions/' \
  --exclude 'projects/*/conversations/' \
  ~/.claude/ NEW_MAC:.claude/
```

過去の会話 jsonl を持っていきたければ `sessions/` と `projects/*/conversations/` の除外を外す。容量が膨れることに注意。

**memory はこの rsync に含まれる**（`~/.claude/projects/-Users-htk-dev-claude-manager/memory/`）。

## トークン・秘密情報

`.env` は `.gitignore` 対象で repo に入らない。**個別にコピーするか新規発行する**。

### Discord bot

選択肢2つ。

- **共有する**: 旧Mac の `~/.claude/channels/discord/.env` を新Mac にコピー。ただし **両Macで同時に Claude を起動するとメッセージは早い方にしか届かない**。メイン機を移行するならこれで OK。
- **新規発行**: Claude Code 上で `/setup` を実行すると Discord Developer Portal の手順を案内される。新Mac 用に別 bot を作る。並走するならこちら。

### LINE bot

`~/.claude/channels/line/.env` をコピー。`cloudflared tunnel` は **両機で同時に動かさない**（webhook URL がどちらか一方にしか向かない）。

### gh auth

```sh
gh auth login
```

## アプリ・常駐

### AivisSpeech（TTS）

公式から DMG を落として `/Applications/` に入れる。speaker_id 等の設定は `~/.claude/say-config.json` で揃う（rsync 済み）。

### SayMenubar.app（メニューバーアバター）

`utsushi` リポジトリにビルドソースがある。

```sh
git clone <utsushi の repo URL> ~/dev/utsushi
cd ~/dev/utsushi
# README に従ってビルド → SayMenubar.app を生成
```

launchd 登録:

```sh
cp ~/Library/LaunchAgents/com.hata.say-menubar.plist /tmp/  # 旧Mac から持ってきた plist
# plist 内のパスを新Mac 用に書き換え（旧Mac の /Users/htk/dev/utsushi/... が一致するなら不要）
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.hata.say-menubar.plist
launchctl kickstart -k gui/$(id -u)/com.hata.say-menubar
```

### tmux personas

```sh
~/.claude/bin/tmux-claude-up
```

## utsushi / avatar-frontend など外部 repo

`avatar-frontend` は `~/dev/utsushi/avatar-frontend/` 配下（memory 参照）。utsushi repo に同梱されている前提。

## 並走 vs 置き換えの判断

| | メイン置き換え | サブで並走 |
|---|---|---|
| Discord/LINE bot | 旧トークン使い回し可。旧Macで Claude を止める | 新規 bot 推奨。同時受信は不可 |
| Dropbox | 自動 sync で同期 | 同上 |
| `~/.claude/` | 1回 rsync すれば良い | 定期 rsync が必要（memory が両機で書き換わる） |
| AivisSpeech 課金/設定 | 移すだけ | 個別 |

サブ並走は memory の整合性が崩れやすい。可能ならメイン置き換えの方が運用は楽。

## 検証

新Mac で:

```sh
cd ~/dev/claude-manager
claude    # Claude Code 起動
# session 内で:
/setup     # （新規bot ルートを取った場合のみ）
# Discord で "おはよう" を投げ、返答が来ること
```

`./scripts/check-new-mac.sh` を最後にもう一度走らせて、すべて OK か WARN になっていれば完了。
