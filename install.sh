#!/usr/bin/env bash
set -euo pipefail

SCRIPT_NAME="wrld-logout"
SRC_FILE="wrld-logout.py"
DEST="$HOME/.local/bin/$SCRIPT_NAME"
WINDOW_TAG="WrldLogout"

echo "This will install $SCRIPT_NAME to $DEST"
echo "[ WARN ] Optimised only for Hyprland (tested on 5.0.1)"
read -r -p "Continue? [y/N]: " answer
answer=${answer,,}   # lowercase

case "$answer" in
  y|yes)
    if ! command -v python3 >/dev/null 2>&1; then
      echo "Error: python3 is not installed or not in PATH."
      exit 1
    fi

    if [[ ! -f "$SRC_FILE" ]]; then
      echo "Error: $SRC_FILE not found in $(pwd)."
      exit 1
    fi

    mkdir -p "$(dirname "$DEST")"
    install -m755 "$SRC_FILE" "$DEST"

    echo "Installed $SCRIPT_NAME to $DEST"
    echo "Launching to apply Hyprland window rules..."

    "$DEST" &
    WC_PID=$!
    sleep 0.5
    
    echo "Done! Window tag: $WINDOW_TAG"
    echo
    echo "In your approach to add this into ~/.config/hypr/hyprland.conf"
    echo
    printf 'windowrule = floating, tag=4, class:%s\n' "$WINDOW_TAG"
    ;;
  *)
    echo "Installation aborted by user."
    exit 1
    ;;
esac
