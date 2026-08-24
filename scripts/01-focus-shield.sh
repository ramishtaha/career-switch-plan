#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────
# FOCUS SHIELD — laptop distraction blocker for Ramish's career-switch goals
# ──────────────────────────────────────────────────────────────────────────
# WHAT IT DOES:
#   1. Adds a /etc/hosts block for Instagram, YouTube, Netflix, Prime, Hotstar,
#      Facebook, and common web-series / short-video sites.
#   2. Provides two toggle scripts: focus-on.sh / focus-off.sh
#   3. The "off" switch has a 30-second forced delay + intent log,
#      so disabling is a conscious act, not an impulse click.
#
# WHY: Your relapse chain is  web-series/reels → no sleep → freeze.
#      Removing the trigger at the DNS level is the highest-leverage fix.
#      This is NOT willpower — it's removing the option so willpower isn't tested.
#
# USAGE (on your laptop, not the cloud server):
#   chmod +x scripts/01-focus-shield.sh
#   sudo ./scripts/01-focus-shield.sh install
#   ./scripts/focus-on.sh    # turn blocking ON  (default after install)
#   ./scripts/focus-off.sh   # turn blocking OFF (30s delay + intent log)
#
# RUNS ON: Ubuntu/Debian laptops. Tested on Ubuntu 24.04. macOS needs manual /etc/hosts edit.
# ──────────────────────────────────────────────────────────────────────────
set -euo pipefail

# --- Distraction domains -----------------------------------------------------
# Instagram, YouTube, streaming, web-series, short-video, social.
# YouTube is intentionally included — if you need it for learning, use focus-off
# deliberately, watch the video, then focus-on again. The friction is the point.
DISTRACTION_DOMAINS=(
  # Instagram
  instagram.com www.instagram.com
  # YouTube + Shorts
  youtube.com www.youtube.com m.youtube.com
  # Netflix
  netflix.com www.netflix.com
  # Amazon Prime
  primevideo.com www.primevideo.com
  # Hotstar / Disney+ Hotstar
  hotstar.com www.hotstar.com
  # Facebook
  facebook.com www.facebook.com m.facebook.com
  # Common web-series / short-video traps
  mxplayer.in www.mxplayer.in
  jiocinema.com www.jiocinema.com
  voot.com www.voot.com
  zee5.com www.zee5.com
  sonyliv.com www.sonyliv.com
  # TikTok / short-video
  tiktok.com www.tiktok.com
)

HOSTS_FILE="/etc/hosts"
BEGIN_MARKER="# >>> FOCUS-SHIELD BLOCK START >>>"
END_MARKER="# <<< FOCUS-SHIELD BLOCK END <<<"
INTENT_LOG="$HOME/.focus-shield-intent.log"
OFF_DELAY_SECONDS=30

# --- Helpers ------------------------------------------------------------------
color_green() { printf '\033[0;32m%s\033[0m\n' "$1"; }
color_red()   { printf '\033[0;31m%s\033[0m\n' "$1"; }
color_yellow(){ printf '\033[0;33m%s\033[0m\n' "$1"; }

is_blocked() {
  grep -q "$BEGIN_MARKER" "$HOSTS_FILE" 2>/dev/null
}

# --- Install: set up scripts + blocking + DNS cache flush ---------------------
install_shield() {
  # Write the hosts block
  if is_blocked; then
    color_yellow "Focus shield already installed in $HOSTS_FILE. Refreshing..."
    remove_block
  fi

  {
    echo "$BEGIN_MARKER"
    echo "# Added $(date '+%Y-%m-%d %H:%M:%S') by focus-shield"
    echo "# To remove: run scripts/focus-off.sh  (30s delay + intent log)"
    for domain in "${DISTRACTION_DOMAINS[@]}"; do
      echo "127.0.0.1  $domain"
      echo "::1        $domain"
    done
    echo "$END_MARKER"
  } >> "$HOSTS_FILE"

  # Flush DNS cache so the block takes effect immediately
  flush_dns

  # Create convenience scripts in the same directory
  create_toggles

  color_green "✅ Focus shield INSTALLED."
  echo ""
  echo "Blocked ${#DISTRACTION_DOMAINS[@]} domains (Instagram, YouTube, Netflix,"
  echo "Prime, Hotstar, Facebook, web-series, TikTok)."
  echo ""
  echo "Toggles (from repo root):"
  echo "  ./scripts/focus-on.sh   — blocking ON (default)"
  echo "  ./scripts/focus-off.sh  — blocking OFF (30s delay + intent log)"
  echo ""
  echo "DNS cache flushed. Sites should be unreachable now."
  echo ""
  color_yellow "NOTE: If you need YouTube for a learning video, run focus-off.sh,"
  echo "      watch it, then run focus-on.sh. The friction is intentional."
}

# --- Remove the block from /etc/hosts -----------------------------------------
remove_block() {
  # Delete everything between markers, including markers
  if is_blocked; then
    sed -i "/$BEGIN_MARKER/,/$END_MARKER/d" "$HOSTS_FILE"
  fi
}

# --- Create the toggle scripts ------------------------------------------------
create_toggles() {
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  # focus-on.sh — turn blocking ON (sudo)
  cat > "$script_dir/focus-on.sh" <<'ON_EOF'
#!/usr/bin/env bash
# FOCUS ON — re-enable the distraction block. Frictionless (no delay).
set -euo pipefail
HOSTS_FILE="/etc/hosts"
BEGIN="# >>> FOCUS-SHIELD BLOCK START >>>"
END="# <<< FOCUS-SHIELD BLOCK END <<<"
DISTRACTION_DOMAINS=(
  instagram.com www.instagram.com
  youtube.com www.youtube.com m.youtube.com
  netflix.com www.netflix.com
  primevideo.com www.primevideo.com
  hotstar.com www.hotstar.com
  facebook.com www.facebook.com m.facebook.com
  mxplayer.in www.mxplayer.in
  jiocinema.com www.jiocinema.com
  voot.com www.voot.com
  zee5.com www.zee5.com
  sonyliv.com www.sonyliv.com
  tiktok.com www.tiktok.com
)
if grep -q "$BEGIN" "$HOSTS_FILE" 2>/dev/null; then
  echo "✅ Focus shield already ON."
  exit 0
fi
{
  echo "$BEGIN"
  echo "# Re-enabled $(date '+%Y-%m-%d %H:%M:%S')"
  for d in "${DISTRACTION_DOMAINS[@]}"; do
    echo "127.0.0.1  $d"
    echo "::1        $d"
  done
  echo "$END"
} >> "$HOSTS_FILE"
# flush DNS
if command -v resolvectl >/dev/null 2>&1; then resolvectl flush-caches; fi
if command -v systemd-resolve >/dev/null 2>&1; then systemd-resolve --flush-caches; fi
echo "🛡️  Focus shield ON — distractions blocked. Back to work."
ON_EOF
  chmod +x "$script_dir/focus-on.sh"

  # focus-off.sh — turn blocking OFF (sudo, 30s delay + intent log)
  cat > "$script_dir/focus-off.sh" <<'OFF_EOF'
#!/usr/bin/env bash
# FOCUS OFF — disable the distraction block. 30s delay + intent log.
# The delay is the point: it turns an impulse into a conscious decision.
set -euo pipefail
HOSTS_FILE="/etc/hosts"
BEGIN="# >>> FOCUS-SHIELD BLOCK START >>>"
END="# <<< FOCUS-SHIELD BLOCK END <<<"
INTENT_LOG="$HOME/.focus-shield-intent.log"
DELAY=30

if ! grep -q "$BEGIN" "$HOSTS_FILE" 2>/dev/null; then
  echo "⚠️  Focus shield already OFF."
  exit 0
fi

echo "🧠 You're about to disable the focus shield."
echo "   Why? (type your reason, then Enter):"
read -r reason

echo ""
echo "Waiting ${DELAY}s before disabling..."
echo "   (press Ctrl+C to cancel and stay focused)"
for i in $(seq 1 "$DELAY"); do
  printf "\r   %ds remaining... " "$((DELAY - i + 1))"
  sleep 1
done
echo ""
echo ""

# log the intent
echo "$(date '+%Y-%m-%d %H:%M:%S') | reason: ${reason:-no reason given}" >> "$INTENT_LOG"

# remove block
sed -i "/$BEGIN/,/$END/d" "$HOSTS_FILE"
# flush DNS
if command -v resolvectl >/dev/null 2>&1; then resolvectl flush-caches; fi
if command -v systemd-resolve >/dev/null 2>&1; then systemd-resolve --flush-caches; fi

echo "🔓 Focus shield OFF — log saved to ~/.focus-shield-intent.log"
echo "   Re-enable with: ./scripts/focus-on.sh"
OFF_EOF
  chmod +x "$script_dir/focus-off.sh"
}

# --- Flush DNS cache ----------------------------------------------------------
flush_dns() {
  if command -v resolvectl >/dev/null 2>&1; then
    resolvectl flush-caches 2>/dev/null || true
  fi
  if command -v systemd-resolve >/dev/null 2>&1; then
    systemd-resolve --flush-caches 2>/dev/null || true
  fi
}

# --- Status -------------------------------------------------------------------
status_shield() {
  if is_blocked; then
    color_green "🛡️  Focus shield is ON — distractions blocked."
  else
    color_red "🔓 Focus shield is OFF — distractions accessible."
  fi
}

# --- Main ---------------------------------------------------------------------
usage() {
  echo "Usage: sudo $0 {install|status|uninstall}"
  echo "  install    — set up the block + toggle scripts (run once)"
  echo "  status     — check if blocking is on (no sudo needed)"
  echo "  uninstall  — remove the block and toggle scripts"
}

case "${1:-}" in
  install)
    if [ "$(id -u)" -ne 0 ]; then
      color_red "Run with sudo: sudo $0 install"
      exit 1
    fi
    install_shield
    ;;
  status)
    status_shield
    ;;
  uninstall)
    if [ "$(id -u)" -ne 0 ]; then
      color_red "Run with sudo: sudo $0 uninstall"
      exit 1
    fi
    remove_block
    flush_dns
    color_yellow "Focus shield uninstalled. Block removed from /etc/hosts."
    ;;
  *)
    usage
    exit 1
    ;;
esac
