#!/usr/bin/env bash
# SessionEnd hook for Claude Code.
#
# Reads the JSON event from stdin, locates the session transcript jsonl,
# and saves both the raw jsonl and a markdown digest under
#   raw/transcripts/YYYY-MM/YYYY-MM-DD-HHMM-<shortid>.{jsonl,md}
#
# Designed to be cheap and silent: failures are logged to a side file and
# never block session shutdown.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$PROJECT_ROOT/raw/transcripts"
ERR_LOG="$PROJECT_ROOT/logs/system/session-log.err"
mkdir -p "$LOG_DIR" "$(dirname "$ERR_LOG")"

# Read stdin event JSON (Claude Code SessionEnd payload).
event_json="$(cat || true)"
if [[ -z "$event_json" ]]; then
  echo "[$(date -Iseconds)] no event json on stdin" >> "$ERR_LOG"
  exit 0
fi

transcript_path="$(printf '%s' "$event_json" | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin); print(d.get("transcript_path") or "")
except Exception: print("")')"
session_id="$(printf '%s' "$event_json" | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin); print(d.get("session_id") or "")
except Exception: print("")')"

# Fallbacks: if the hook payload omits transcript_path, locate the freshest
# jsonl by session_id under ~/.claude/projects/.
if [[ -z "$transcript_path" && -n "$session_id" ]]; then
  hit="$(find "$HOME/.claude/projects" -maxdepth 2 -name "${session_id}.jsonl" -print -quit 2>/dev/null || true)"
  [[ -n "$hit" ]] && transcript_path="$hit"
fi

if [[ -z "$transcript_path" || ! -f "$transcript_path" ]]; then
  echo "[$(date -Iseconds)] transcript not found (session=$session_id)" >> "$ERR_LOG"
  exit 0
fi

date_dir="$(date +%Y-%m)"
ts="$(date +%Y-%m-%d-%H%M)"
short_id="${session_id:0:8}"
[[ -z "$short_id" ]] && short_id="$(basename "$transcript_path" .jsonl | cut -c1-8)"

mkdir -p "$LOG_DIR/$date_dir"
out_jsonl="$LOG_DIR/$date_dir/${ts}-${short_id}.jsonl"
out_md="$LOG_DIR/$date_dir/${ts}-${short_id}.md"

cp -f "$transcript_path" "$out_jsonl" 2>>"$ERR_LOG" || {
  echo "[$(date -Iseconds)] cp failed: $transcript_path" >> "$ERR_LOG"
  exit 0
}

python3 "$PROJECT_ROOT/scripts/transcript-to-md.py" "$out_jsonl" "$out_md" \
  2>>"$ERR_LOG" || echo "[$(date -Iseconds)] md conversion failed for $out_jsonl" >> "$ERR_LOG"

exit 0
