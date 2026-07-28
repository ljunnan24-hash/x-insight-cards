#!/bin/zsh
set -eu

script_dir="${0:A:h}"
automation_root="${XIC_AUTOMATION_ROOT:-${CODEX_HOME:-$HOME/.codex}/automations/x-insight-cards}"
completion_root="$automation_root/completions"
stale_root="$automation_root/stale-locks"
lock_root="${XIC_LOCK_ROOT:-${TMPDIR:-/tmp}}"
lock_name="${XIC_LOCK_NAME:-codex-x-insight-cards-daily}"
stale_after_seconds="${XIC_STALE_LOCK_SECONDS:-21600}"
node_bin="${XIC_NODE_BIN:-$(command -v node)}"
action="${1:-status}"
run_date="${2:-$(TZ=Asia/Shanghai /bin/date +%F)}"

case "$run_date" in
  ????-??-??) ;;
  *)
    print -u2 -r -- "Invalid run date: $run_date"
    exit 2
    ;;
esac

case "$lock_name" in
  *[!A-Za-z0-9._-]*)
    print -u2 -r -- "XIC_LOCK_NAME contains unsupported characters"
    exit 2
    ;;
esac

lock_dir="$lock_root/$lock_name-$run_date.lock"
done_file="$completion_root/$run_date.done"

lock_modified_epoch() {
  /usr/bin/stat -f %m "$1" 2>/dev/null ||
    /usr/bin/stat -c %Y "$1" 2>/dev/null
}

acquire_lock() {
  if [ -f "$done_file" ]; then
    print -r -- "ALREADY_COMPLETE"
    return 0
  fi

  /bin/mkdir -p "$lock_root"
  if /bin/mkdir "$lock_dir" 2>/dev/null; then
    print -r -- "ACQUIRED"
    return 0
  fi

  now_epoch="$(/bin/date +%s)"
  lock_epoch="$(lock_modified_epoch "$lock_dir" || print -r -- "$now_epoch")"
  lock_age=$((now_epoch - lock_epoch))
  if [ "$lock_age" -lt "$stale_after_seconds" ]; then
    print -r -- "BUSY"
    return 0
  fi

  /bin/mkdir -p "$stale_root"
  stale_target="$stale_root/$run_date-$now_epoch.lock"
  if ! /bin/mv "$lock_dir" "$stale_target" 2>/dev/null; then
    print -r -- "BUSY"
    return 0
  fi
  if /bin/mkdir "$lock_dir" 2>/dev/null; then
    print -r -- "ACQUIRED_STALE_RECOVERY"
  else
    print -r -- "BUSY"
  fi
}

case "$action" in
  acquire)
    acquire_lock
    ;;
  mark-complete)
    if [ -z "${XIC_HISTORY_PATH:-}" ] || [ -z "${XIC_OUTPUT_ROOT:-}" ]; then
      print -u2 -r -- \
        "mark-complete requires XIC_HISTORY_PATH and XIC_OUTPUT_ROOT"
      exit 2
    fi
    proof="$(
      "$node_bin" "$script_dir/verify_daily_completion.mjs" \
        --date "$run_date" \
        --history "$XIC_HISTORY_PATH" \
        --output-root "$XIC_OUTPUT_ROOT"
    )"
    /bin/mkdir -p "$completion_root"
    temporary_file="$done_file.tmp.$$"
    print -r -- "$proof" > "$temporary_file"
    /bin/chmod 600 "$temporary_file"
    /bin/mv "$temporary_file" "$done_file"
    /bin/rmdir "$lock_dir" 2>/dev/null || true
    print -r -- "COMPLETED"
    ;;
  release)
    /bin/rmdir "$lock_dir" 2>/dev/null || true
    print -r -- "RELEASED"
    ;;
  status)
    if [ -f "$done_file" ]; then
      print -r -- "ALREADY_COMPLETE"
    elif [ -d "$lock_dir" ]; then
      print -r -- "BUSY"
    else
      print -r -- "AVAILABLE"
    fi
    ;;
  *)
    print -u2 -r -- \
      "Usage: daily_run_guard.sh {acquire|mark-complete|release|status} [YYYY-MM-DD]"
    exit 2
    ;;
esac
