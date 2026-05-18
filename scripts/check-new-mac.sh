#!/usr/bin/env bash
# check-new-mac.sh — claude-manager 移植先 Mac の状態を診断する
# 何も書き換えない。読むだけ。SETUP_NEW_MAC.md と併せて使う。
set -uo pipefail

OK="OK  "
NG="NG  "
WARN="WARN"

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
echo "claude-manager: $repo_root"
echo

# ---------- 1. dependencies ----------
echo "[1/6] dependencies"
check_bin() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "  $OK $1   ($(command -v "$1"))"
  else
    echo "  $NG $1   → $2"
  fi
}
check_bin git        "xcode-select --install"
check_bin gh         "brew install gh"
check_bin jq         "brew install jq"
check_bin bun        "curl -fsSL https://bun.sh/install | bash"
check_bin python3    "comes with macOS"
check_bin tmux       "brew install tmux"
check_bin rsync      "comes with macOS"
check_bin cloudflared "brew install cloudflared  (LINE を使うなら)"

# Claude Code: PATH or Applications どちらか
if command -v claude >/dev/null 2>&1; then
  echo "  $OK claude   ($(command -v claude))"
elif [ -e "/Applications/Claude Code URL Handler.app" ]; then
  echo "  $OK claude   (Claude Code URL Handler.app)"
else
  echo "  $NG claude   → https://docs.claude.com/claude-code"
fi
echo

# ---------- 2. Dropbox vault & symlinks ----------
echo "[2/6] Dropbox vault & symlinks"
vault="$HOME/Library/CloudStorage/Dropbox-CloudOptionDJteam/ですはた/HTK/HTK"
if [ -d "$vault" ]; then
  echo "  $OK vault: $vault"
else
  echo "  $NG vault が無い: $vault"
  echo "      Dropbox app を入れ、CloudOptionDJteam team を sync する"
fi
for d in projects wiki logs raw tasks docs handoff; do
  p="$repo_root/$d"
  if [ -L "$p" ]; then
    if [ -e "$p" ]; then
      echo "  $OK $d → $(readlink "$p")"
    else
      echo "  $NG $d (symlink の先が無い)"
    fi
  elif [ -d "$p" ]; then
    echo "  $WARN $d は通常dir (本来は symlink)"
  else
    echo "  $NG $d 無し  → bootstrap-new-mac.sh で symlink 作成"
  fi
done
echo

# ---------- 3. ~/.claude tree ----------
echo "[3/6] ~/.claude tree"
for p in CLAUDE.md hooks bin channels plugins say-config.json pronunciation.json; do
  if [ -e "$HOME/.claude/$p" ]; then
    echo "  $OK ~/.claude/$p"
  else
    echo "  $NG ~/.claude/$p 無し  → 旧Mac から rsync"
  fi
done
mem="$HOME/.claude/projects/-Users-htk-dev-claude-manager/memory"
if [ -d "$mem" ]; then
  cnt=$(ls -1 "$mem" 2>/dev/null | wc -l | tr -d ' ')
  echo "  $OK memory ($cnt files)"
else
  echo "  $NG memory dir 無し  → 旧Mac から rsync"
fi
echo

# ---------- 4. secrets ----------
echo "[4/6] secrets"
disc_env="$HOME/.claude/channels/discord/.env"
if [ -f "$disc_env" ] && grep -q "^DISCORD_BOT_TOKEN=." "$disc_env" 2>/dev/null; then
  echo "  $OK Discord bot token"
else
  echo "  $NG Discord bot token 無し  → /setup スキル or 旧Mac からコピー"
fi
line_env="$HOME/.claude/channels/line/.env"
if [ -f "$line_env" ]; then
  echo "  $OK LINE .env"
else
  echo "  $WARN LINE .env 無し  (LINE を使うなら必要)"
fi
gh_status=$(gh auth status 2>&1 || true)
if echo "$gh_status" | grep -q "Logged in to github.com"; then
  echo "  $OK gh auth"
else
  echo "  $NG gh auth 未  → gh auth login"
fi
echo

# ---------- 5. avatar / TTS ----------
echo "[5/6] avatar / TTS"
if [ -d "$HOME/.claude/avatar" ]; then
  echo "  $OK ~/.claude/avatar"
else
  echo "  $WARN ~/.claude/avatar 無し"
fi
if [ -e "$HOME/dev/utsushi/SayMenubar.app" ] || [ -e "/Applications/SayMenubar.app" ]; then
  echo "  $OK SayMenubar.app"
else
  echo "  $WARN SayMenubar.app 無し  → utsushi repo から build"
fi
if [ -e "/Applications/AivisSpeech.app" ] || pgrep -x "AivisSpeech" >/dev/null 2>&1; then
  echo "  $OK AivisSpeech"
else
  echo "  $WARN AivisSpeech 未インストール  (TTS を使うなら)"
fi
echo

# ---------- 6. launchd agents ----------
echo "[6/6] launchd agents"
uid=$(id -u)
for agent in com.hata.say-menubar; do
  if launchctl print "gui/$uid/$agent" >/dev/null 2>&1; then
    state=$(launchctl print "gui/$uid/$agent" 2>/dev/null | awk '/state =/ {print $3; exit}')
    echo "  $OK $agent  (state=$state)"
  else
    echo "  $WARN $agent 未登録"
  fi
done
echo

echo "詳細手順は SETUP_NEW_MAC.md を読むこと。"
