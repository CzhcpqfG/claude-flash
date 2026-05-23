# claude-flash

> A gentle screen pulse for Claude Code prompts.

Claude Code is easy to miss when it is waiting in a terminal tab. **claude-flash** adds a subtle fullscreen breathing pulse whenever Claude needs your attention — no popups, no sound, no focus stealing.

## What it does

When Claude Code asks for input, requests permission, or finishes a task, your screen softly darkens and fades back a few times.

Default effect:

- black translucent overlay
- 3 slow breathing pulses
- works across all monitors
- never steals focus from your terminal

## How it works

```text
Claude Code hook → light_hook.py → flash_overlay.py → transparent overlay windows
```

`flash_overlay.py` uses Python `ctypes` to create topmost layered windows with `WS_EX_NOACTIVATE`, so the alert is visible without changing the active window.

No packages required.

## Install

Clone the repo somewhere stable, for example:

```powershell
git clone https://github.com/CzhcpqfG/claude-flash.git D:\claude-flash
```

Then add these hooks to `~/.claude/settings.json`.

> If you cloned to a different location, update the path in each `command`.

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "*",
        "hooks": [{ "type": "command", "command": "py \"D:/claude-flash/light_hook.py\"" }]
      }
    ],
    "Elicitation": [
      {
        "matcher": "*",
        "hooks": [{ "type": "command", "command": "py \"D:/claude-flash/light_hook.py\"" }]
      }
    ],
    "Notification": [
      {
        "matcher": "*",
        "hooks": [{ "type": "command", "command": "py \"D:/claude-flash/light_hook.py\"" }]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [{ "type": "command", "command": "py \"D:/claude-flash/light_hook.py\"" }]
      }
    ]
  }
}
```

## Test

```powershell
# Direct pulse preview
py "D:/claude-flash/flash_overlay.py"

# Simulate a Claude Code Stop hook
'{"hook_event_name":"Stop"}' | py "D:/claude-flash/light_hook.py"
```

## Events

| Claude Code event | Effect |
|---|---|
| `PermissionRequest` | 3 breathing pulses |
| `Elicitation` | 3 breathing pulses |
| `Notification` | 3 breathing pulses |
| `Stop` | 3 breathing pulses |

## Customize

```powershell
py flash_overlay.py <count> <fade_in_ms> <fade_out_ms> <rest_ms> <alpha> <mode>
```

Defaults:

```powershell
py flash_overlay.py 3 450 650 700 90 black
```

| Parameter | Default | Description |
|---|---:|---|
| `count` | `3` | Number of breathing pulses |
| `fade_in_ms` | `450` | Time to fade the overlay in |
| `fade_out_ms` | `650` | Time to fade the overlay out |
| `rest_ms` | `700` | Pause between pulses |
| `alpha` | `90` | Max opacity, from `0` to `255` |
| `mode` | `black` | `black` or `white` overlay |

Examples:

```powershell
# Softer
py flash_overlay.py 3 500 700 800 60 black

# More noticeable
py flash_overlay.py 4 350 500 500 120 black

# Bright flash mode
py flash_overlay.py 3 120 180 300 120 white
```

## Why not use screen brightness?

Brightness APIs are slow to warm up, usually affect only laptop panels, and may not work on external monitors. The overlay approach is instant, reversible, and display-agnostic.

`blink_screen.ps1` is kept as a fallback for people who prefer real backlight blinking.

## Requirements

- Windows
- Python 3

## License

MIT
