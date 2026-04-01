#!/bin/bash
# セットアップ状態をチェックし、未完了なら指示を出力する
# SessionStartフックから呼ばれ、stdout がLLMコンテクストに注入される

ENV_FILE="$HOME/.claude/channels/discord/.env"
ACCESS_FILE="$HOME/.claude/channels/discord/access.json"
CHANNELS_FILE="$(dirname "$0")/../config/channels.json"

# トークンが設定されているか
TOKEN=""
if [ -f "$ENV_FILE" ]; then
  TOKEN=$(grep -o 'DISCORD_BOT_TOKEN=.\+' "$ENV_FILE" | cut -d= -f2)
fi

if [ -z "$TOKEN" ]; then
  # Phase 1未完了（トークン未設定）
  exit 0
fi

# allowFromが空か
ALLOW_FROM_EMPTY=true
if [ -f "$ACCESS_FILE" ]; then
  ALLOW_COUNT=$(python3 -c "import json; d=json.load(open('$ACCESS_FILE')); print(len(d.get('allowFrom',[])))" 2>/dev/null)
  if [ "$ALLOW_COUNT" != "0" ] && [ -n "$ALLOW_COUNT" ]; then
    ALLOW_FROM_EMPTY=false
  fi
fi

# channels.jsonの全キーが空か
CHANNELS_EMPTY=true
if [ -f "$CHANNELS_FILE" ]; then
  NON_EMPTY=$(python3 -c "import json; d=json.load(open('$CHANNELS_FILE')); print(sum(1 for v in d.values() if v))" 2>/dev/null)
  if [ "$NON_EMPTY" != "0" ] && [ -n "$NON_EMPTY" ]; then
    CHANNELS_EMPTY=false
  fi
fi

# groupsが空か
GROUPS_EMPTY=true
if [ -f "$ACCESS_FILE" ]; then
  GROUPS_COUNT=$(python3 -c "import json; d=json.load(open('$ACCESS_FILE')); print(len(d.get('groups',{})))" 2>/dev/null)
  if [ "$GROUPS_COUNT" != "0" ] && [ -n "$GROUPS_COUNT" ]; then
    GROUPS_EMPTY=false
  fi
fi

# 状態判定
if $ALLOW_FROM_EMPTY; then
  echo "【セットアップ未完了】Phase 2: ペアリングから開始。/setup-discord スキルを実行してください。"
elif $GROUPS_EMPTY || $CHANNELS_EMPTY; then
  echo "【セットアップ未完了】Phase 2: チャンネル設定から開始。/setup-discord スキルを実行してください。"
fi
