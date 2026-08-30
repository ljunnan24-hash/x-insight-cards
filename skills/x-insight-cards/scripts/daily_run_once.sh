#!/bin/zsh
set -eu

script_dir="${0:A:h}"
guard="$script_dir/daily_run_guard.sh"
run_date="${1:-$(TZ=Asia/Shanghai /bin/date +%F)}"
if [ "${2:-}" != "--" ] || [ "$#" -lt 3 ]; then
  print -u2 -r -- \
    "Usage: daily_run_once.sh [YYYY-MM-DD] -- command [args ...]"
  exit 2
fi
shift 2

# A catch-up service can set 740 to wait until 12:20 Shanghai time. The normal
# scheduled job leaves this at zero. Historical dates are always due.
not_before="${XIC_NOT_BEFORE_MINUTE_OF_DAY:-0}"
today="$(TZ=Asia/Shanghai /bin/date +%F)"
if [ "$run_date" = "$today" ] && [ "$not_before" -gt 0 ]; then
  hour="$(TZ=Asia/Shanghai /bin/date +%H)"
  minute="$(TZ=Asia/Shanghai /bin/date +%M)"
  minute_of_day=$((10#$hour * 60 + 10#$minute))
  if [ "$minute_of_day" -lt "$not_before" ]; then
    print -r -- "NOT_DUE"
    exit 0
  fi
fi

guard_result="$("$guard" acquire "$run_date")"
case "$guard_result" in
  ALREADY_COMPLETE|BUSY)
    print -r -- "$guard_result"
    exit 0
    ;;
  ACQUIRED|ACQUIRED_STALE_RECOVERY)
    ;;
  *)
    print -u2 -r -- "Unexpected guard result: $guard_result"
    exit 1
    ;;
esac

trap '"$guard" release "$run_date" >/dev/null 2>&1 || true' EXIT
X_GUARD_ALREADY_HELD_BY_WRAPPER=1 XIC_RUN_DATE="$run_date" "$@"
"$guard" mark-complete "$run_date"
trap - EXIT
