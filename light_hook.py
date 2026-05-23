# -*- coding: utf-8 -*-
"""
Claude Code Hook: Screen Brightness Blink

Reads hook event JSON from stdin, blinks screen on Notification/Stop.
Warms up WMI on SessionStart so subsequent blinks are instant.
"""
import sys
import json
import subprocess
import os

BLINK_SCRIPT = r'D:\autolights\blink_screen.ps1'


def warmup_wmi():
    """Query WMI brightness once so subsequent calls avoid 20-50s cold start."""
    try:
        subprocess.run(
            ['powershell', '-ExecutionPolicy', 'Bypass', '-Command',
             'Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightness | Out-Null'],
            capture_output=True, timeout=30
        )
    except Exception:
        pass


def trigger_blink(count):
    if not os.path.exists(BLINK_SCRIPT):
        return
    try:
        subprocess.run(
            ['powershell', '-ExecutionPolicy', 'Bypass', '-File', BLINK_SCRIPT,
             '-Count', str(count)],
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

        if event_type == "SessionStart":
            warmup_wmi()
        elif event_type in ("PermissionRequest", "Elicitation"):
            trigger_blink(2)
        elif event_type == "Notification":
            trigger_blink(2)
        elif event_type == "Stop":
            trigger_blink(2)
    except Exception:
        pass


if __name__ == "__main__":
    main()
