# -*- coding: utf-8 -*-
"""
Claude Code Hook: Fullscreen Overlay Flash

Reads hook event JSON from stdin, flashes screen on Claude events.
Uses flash_overlay.py — camera-flash effect, all monitors, zero delay.
"""
import sys
import json
import subprocess
import os

FLASH_SCRIPT = r'D:\autolights\flash_overlay.py'


def trigger_flash(count=3):
    if not os.path.exists(FLASH_SCRIPT):
        return
    try:
        subprocess.run(
            ['py', FLASH_SCRIPT, str(count)],
            capture_output=True, timeout=10
        )
    except Exception:
        pass


def main():
    data = sys.stdin.read()
    if not data.strip():
        return

    try:
        event = json.loads(data)
        event_type = event.get("hook_event_name", event.get("event"))

        if event_type in ("SessionStart", "PermissionRequest", "Elicitation",
                          "Notification", "Stop"):
            trigger_flash(2)
    except Exception:
        pass


if __name__ == "__main__":
    main()
