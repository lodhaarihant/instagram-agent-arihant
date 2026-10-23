#!/usr/bin/env bash
# Run autopost.py every INTERVAL seconds for up to LOOP_SECONDS, then return so
# the workflow can start the next run. State is committed after every pass, so
# a crash loses at most one pass. Run from thoughts4us/ (see the workflow).
set -u

LOOP_SECONDS=${LOOP_SECONDS:-18000}   # 5h, GitHub kills jobs at 6h
INTERVAL=${INTERVAL:-300}
REPLY_EVERY=${REPLY_EVERY:-3}         # replybot every 3rd pass (15 min)

save_state() {
  (
    cd ..
    git add thoughts4us/state
    git diff --cached --quiet && exit 0
    git config user.name "thoughts4us-bot"
    git config user.email "actions@users.noreply.github.com"
    git commit -q -m "autopost: update state [skip ci]"
    git push -q || { git pull --rebase -q && git push -q; }
  ) || echo "could not save state this pass" >&2
}

end=$((SECONDS + LOOP_SECONDS))
n=0
while :; do
  # Pick up new schedule, media and code pushed while this run was going.
  git -C .. pull --rebase --autostash -q || echo "pull failed, using local checkout" >&2

  python autopost.py || echo "autopost exited $?" >&2
  if [ $((n % REPLY_EVERY)) -eq 0 ]; then
    python replybot.py || echo "replybot exited $?" >&2
  fi
  save_state

  n=$((n + 1))
  [ $((SECONDS + INTERVAL)) -ge "$end" ] && break
  sleep "$INTERVAL"
done
