#!/usr/bin/env bash
# Install / remove macOS launchd auto-start for the live division dashboard.
#
#   install   — start the dashboard server at login (always on) + refresh the
#               data every 5 min. Serves http://127.0.0.1:8787
#   uninstall — stop and remove both agents
#   status    — show whether the agents are loaded + reachable
#
# Read-only: the server never writes the vault; the refresh job regenerates
# 00-Dashboard.md (gitignored) from current vault state.
set -euo pipefail

VAULT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"   # repo root = vault
PY="$VAULT/.venv/bin/python"
PORT="${BD_DASH_PORT:-8787}"
OWNER="${BD_DASH_OWNER:-Brian}"
DIVISION="${BD_DASH_DIVISION:-Hardware engineering & supply chain division}"
LA="$HOME/Library/LaunchAgents"
UID_NUM="$(id -u)"
SRV="com.bd-os.dashboard.server"
RFR="com.bd-os.dashboard.refresh"

plist_server() {
  cat <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$SRV</string>
  <key>ProgramArguments</key><array>
    <string>$PY</string>
    <string>$VAULT/docs/scripts/dashboard_server.py</string>
    <string>--vault</string><string>$VAULT</string>
    <string>--port</string><string>$PORT</string>
    <string>--owner</string><string>$OWNER</string>
    <string>--division</string><string>$DIVISION</string>
  </array>
  <key>WorkingDirectory</key><string>$VAULT</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>/tmp/bd-dashboard-server.log</string>
  <key>StandardErrorPath</key><string>/tmp/bd-dashboard-server.log</string>
</dict></plist>
EOF
}

plist_refresh() {
  cat <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$RFR</string>
  <key>ProgramArguments</key><array>
    <string>$PY</string>
    <string>$VAULT/docs/scripts/agent_dashboard.py</string>
    <string>--vault</string><string>$VAULT</string>
  </array>
  <key>WorkingDirectory</key><string>$VAULT</string>
  <key>RunAtLoad</key><true/>
  <key>StartInterval</key><integer>300</integer>
  <key>StandardOutPath</key><string>/tmp/bd-dashboard-refresh.log</string>
  <key>StandardErrorPath</key><string>/tmp/bd-dashboard-refresh.log</string>
</dict></plist>
EOF
}

load_one() {  # $1 = label, $2 = plist path
  launchctl bootout "gui/$UID_NUM/$1" 2>/dev/null || true
  launchctl bootstrap "gui/$UID_NUM" "$2"
  launchctl enable "gui/$UID_NUM/$1" 2>/dev/null || true
  launchctl kickstart -k "gui/$UID_NUM/$1" 2>/dev/null || true
}

case "${1:-}" in
  install)
    [ -x "$PY" ] || { echo "venv python not found at $PY — create the venv first." >&2; exit 1; }
    mkdir -p "$LA"
    pkill -f "dashboard_server.py" 2>/dev/null || true   # free the port from any manual run
    plist_server  > "$LA/$SRV.plist"
    plist_refresh > "$LA/$RFR.plist"
    load_one "$RFR" "$LA/$RFR.plist"
    sleep 2   # let the first refresh write 00-Dashboard.md
    load_one "$SRV" "$LA/$SRV.plist"
    sleep 1
    echo "Installed. Dashboard auto-starts at login."
    echo "  url      : http://127.0.0.1:$PORT"
    echo "  health   : $(curl -s "http://127.0.0.1:$PORT/health" 2>/dev/null || echo 'starting…')"
    echo "  logs     : /tmp/bd-dashboard-server.log  /tmp/bd-dashboard-refresh.log"
    echo "  uninstall: bash docs/scripts/dashboard-autostart.sh uninstall"
    ;;
  uninstall)
    launchctl bootout "gui/$UID_NUM/$SRV" 2>/dev/null || true
    launchctl bootout "gui/$UID_NUM/$RFR" 2>/dev/null || true
    rm -f "$LA/$SRV.plist" "$LA/$RFR.plist"
    pkill -f "dashboard_server.py" 2>/dev/null || true
    echo "Uninstalled. Auto-start removed."
    ;;
  status)
    echo "server : $(launchctl print "gui/$UID_NUM/$SRV" >/dev/null 2>&1 && echo loaded || echo 'not loaded')"
    echo "refresh: $(launchctl print "gui/$UID_NUM/$RFR" >/dev/null 2>&1 && echo loaded || echo 'not loaded')"
    echo "health : $(curl -s "http://127.0.0.1:$PORT/health" 2>/dev/null || echo unreachable)"
    ;;
  check)
    echo "server   : $(launchctl print "gui/$UID_NUM/$SRV" >/dev/null 2>&1 && echo loaded || echo 'not loaded')"
    echo "health   : $(curl -s "http://127.0.0.1:$PORT/health" 2>/dev/null || echo unreachable)"
    DASH="$VAULT/00-Dashboard.md"
    if [ -f "$DASH" ]; then
      echo "data     : $(( $(date +%s) - $(stat -f %m "$DASH") ))s old"
    else
      echo "data     : MISSING — run agent_dashboard.py"
    fi
    R=$(curl -s "http://127.0.0.1:$PORT/" 2>/dev/null | grep -c 'Good ' || true)
    [ "${R:-0}" -gt 0 ] && echo "render   : ok" || echo "render   : FAILED"
    ;;
  demo)
    # Demo mode runs on its OWN port so it NEVER disturbs the always-on read-only
    # server. The launchd agent on $PORT keeps running + auto-starting; closing the
    # demo (or a crash) can no longer break it. This was the root cause of past outages.
    COMPANY="${2:-${BD_DASH_COMPANY:-}}"
    DEMO_PORT="${BD_DASH_DEMO_PORT:-8788}"
    pkill -f "dashboard_server.py.*--port $DEMO_PORT" 2>/dev/null || true   # clear a prior demo only
    sleep 1
    "$PY" "$VAULT/docs/scripts/agent_dashboard.py" --vault "$VAULT" >/dev/null 2>&1 || true
    ( sleep 2; open -na "Google Chrome" --args --new-window --start-fullscreen "http://127.0.0.1:$DEMO_PORT/?present=1" >/dev/null 2>&1 \
        || open "http://127.0.0.1:$DEMO_PORT/?present=1" ) &
    echo "DEMO MODE on port $DEMO_PORT (live actions ON, present/kiosk)."
    echo "The always-on read-only dashboard on $PORT is untouched. Ctrl+C stops only this demo server."
    ARGS=(--vault "$VAULT" --port "$DEMO_PORT" --owner "$OWNER" --division "$DIVISION" --enable-actions)
    [ -n "$COMPANY" ] && ARGS+=(--company "$COMPANY")
    [ -n "${BD_DASH_LOGO:-}" ] && ARGS+=(--logo "$BD_DASH_LOGO")
    "$PY" "$VAULT/docs/scripts/dashboard_server.py" "${ARGS[@]}"
    ;;
  demo-embed)
    # Like `demo` but does NOT open a browser window — meant for the Obsidian embed
    # (00-Dashboard-Demo.md), which points its iframe at the demo port. Live actions ON.
    # The always-on read-only server on $PORT stays untouched. Ctrl+C stops only this server.
    COMPANY="${2:-${BD_DASH_COMPANY:-}}"
    DEMO_PORT="${BD_DASH_DEMO_PORT:-8788}"
    pkill -f "dashboard_server.py.*--port $DEMO_PORT" 2>/dev/null || true   # clear a prior demo only
    sleep 1
    "$PY" "$VAULT/docs/scripts/agent_dashboard.py" --vault "$VAULT" >/dev/null 2>&1 || true
    echo "DEMO-EMBED on port $DEMO_PORT (live actions ON). Open 00-Dashboard-Demo.md in Obsidian Reading view."
    echo "The always-on read-only dashboard on $PORT is untouched. Ctrl+C stops only this demo server."
    ARGS=(--vault "$VAULT" --port "$DEMO_PORT" --owner "$OWNER" --division "$DIVISION" --enable-actions)
    [ -n "$COMPANY" ] && ARGS+=(--company "$COMPANY")
    [ -n "${BD_DASH_LOGO:-}" ] && ARGS+=(--logo "$BD_DASH_LOGO")
    "$PY" "$VAULT/docs/scripts/dashboard_server.py" "${ARGS[@]}"
    ;;
  *)
    echo "usage: bash docs/scripts/dashboard-autostart.sh {install|uninstall|status|check|demo [\"Company Name\"]|demo-embed [\"Company Name\"]}" >&2
    exit 1
    ;;
esac
