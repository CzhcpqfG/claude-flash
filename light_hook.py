# -*- coding: utf-8 -*-
"""
Claude Code Hook: Fullscreen Overlay Pulse

Reads hook event JSON from stdin and runs the overlay pulse.
"""
import json
import subprocess
import sys
from pathlib import Path

FLASH_SCRIPT = Path(__file__).with_name('flash_overlay.py')


def trigger_flash(count=3):
    if not FLASH_SCRIPT.exists():
        return
    try:
        subprocess.run(
            ['py', str(FLASH_SCRIPT), str(count)],
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

        if event_type in ("PermissionRequest", "Elicitation", "Notification", "Stop"):
            trigger_flash(3)
    except Exception:
        pass


if __name__ == "__main__":
    main()
