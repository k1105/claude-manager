#!/usr/bin/env bash
# One-shot backfill: copy every existing claude-manager transcript jsonl
# into raw/transcripts/YYYY-MM/ and generate a markdown digest.
#
# Date bucket comes from the jsonl mtime. Filename: {date}-{shortid}.{jsonl,md}
# Idempotent — skips files whose target already exists.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$HOME/.claude/projects/-Users-htk-dev-claude-manager"
LOG_DIR="$PROJECT_ROOT/raw/transcripts"
mkdir -p "$LOG_DIR"

count=0
skipped=0
failed=0

shopt -s nullglob
for f in "$SRC_DIR"/*.jsonl; do
  base="$(basename "$f" .jsonl)"
  short_id="${base:0:8}"
  # mtime → YYYY-MM-DD-HHMM
  ts="$(date -r "$f" +%Y-%m-%d-%H%M)"
  ym="${ts:0:7}"
  out_dir="$LOG_DIR/$ym"
  mkdir -p "$out_dir"
  out_jsonl="$out_dir/${ts}-${short_id}.jsonl"
  out_md="$out_dir/${ts}-${short_id}.md"

  if [[ -f "$out_jsonl" && -f "$out_md" ]]; then
    skipped=$((skipped+1))
    continue
  fi

  cp -f "$f" "$out_jsonl"
  if python3 "$PROJECT_ROOT/scripts/transcript-to-md.py" "$out_jsonl" "$out_md" 2>/dev/null; then
    count=$((count+1))
  else
    failed=$((failed+1))
    echo "[fail] $f"
  fi
done

echo "backfill done: imported=$count, skipped=$skipped, failed=$failed"
echo "output: $LOG_DIR"
