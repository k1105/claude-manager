#!/usr/bin/env bash
# bootstrap-new-mac.sh — 安全に自動化できる部分だけ実行する
# やること: Dropbox dir への symlink を repo 直下に作る
# やらないこと: 秘密情報のコピー、アプリのインストール、トークン発行
#
# 前提: Dropbox app が起動しており、CloudOptionDJteam が sync 完了している
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
vault="$HOME/Library/CloudStorage/Dropbox-CloudOptionDJteam/ですはた/HTK/HTK"

if [ ! -d "$vault" ]; then
  echo "ERROR: Dropbox vault が見つからない: $vault"
  echo "  Dropbox.app をインストールし、CloudOptionDJteam を sync してから再実行する"
  exit 1
fi

echo "vault: $vault"
echo "repo:  $repo_root"
echo

linked=0
skipped=0
for d in projects wiki logs raw tasks docs handoff; do
  src="$vault/$d"
  dst="$repo_root/$d"
  if [ ! -d "$src" ]; then
    echo "  skip  $d  (vault側に存在しない: $src)"
    skipped=$((skipped+1))
    continue
  fi
  if [ -L "$dst" ]; then
    cur=$(readlink "$dst")
    if [ "$cur" = "$src" ]; then
      echo "  ok    $d  (既に正しい symlink)"
      skipped=$((skipped+1))
      continue
    else
      echo "  warn  $d  symlink あり、別の先を指している: $cur"
      echo "        手動で確認してから ln -snf するか判断"
      skipped=$((skipped+1))
      continue
    fi
  fi
  if [ -e "$dst" ]; then
    echo "  warn  $d  通常 file/dir として既に存在。上書きしない"
    skipped=$((skipped+1))
    continue
  fi
  ln -s "$src" "$dst"
  echo "  link  $d → $src"
  linked=$((linked+1))
done

echo
echo "完了: link=$linked  skip=$skipped"
echo "次は: ./scripts/check-new-mac.sh で残りを確認する"
