# ⚡ claude-flash

> Your screen pulses when Claude Code needs you. No popups. No mouse. No missed prompts.

![platform](https://img.shields.io/badge/platform-Windows%2011-blue)
![license](https://img.shields.io/badge/license-MIT-green)

Claude Code runs in the terminal. You look away. Minutes pass. Claude is waiting for your permission — but you didn't notice.

**claude-flash** creates a fullscreen overlay pulse on every monitor the moment Claude needs attention. Permission dialogs, input prompts, task completions — each gets a gentle visual nudge.

## How it looks

Black semi-transparent overlay fades in for 100ms, fades out for 400ms, repeats 3 times. Like the screen taking a soft breath — noticeable but not jarring. White flash mode also available if you prefer bright alerts.

## How it works

```
Claude event → settings.json hook → light_hook.py → flash_overlay.py → fullscreen overlay on all monitors
```

Zero dependencies beyond Python stdlib. Creates per-monitor layered windows with `WS_EX_NOACTIVATE` — never steals focus, no taskbar entry, no Alt+Tab.

## Quick start

**Prerequisites:** Windows, Python 3

```powershell
git clone https://github.com/CzhcpqfG/claude-flash.git D:\autolights
```

Add to `~/.claude/settings.json`:

<details>
<summary>Click to expand hook config</summary>

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "*",
        "hooks": [{ "type": "command", "command": "py \"D:/autolights/light_hook.py\"" }]
      }
    ],
    "Elicitation": [
      {
        "matcher": "*",
        "hooks": [{ "type": "command", "command": "py \"D:/autolights/light_hook.py\"" }]
      }
    ],
    "Notification": [
      {
        "matcher": "*",
        "hooks": [{ "type": "command", "command": "py \"D:/autolights/light_hook.py\"" }]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [{ "type": "command", "command": "py \"D:/autolights/light_hook.py\"" }]
      }
    ]
  }
}
```
</details>

**Test it:**

```powershell
# Direct test — 3 black pulses
py "D:/autolights/flash_overlay.py"

# White flash mode
py "D:/autolights/flash_overlay.py" 3 100 400 100 white

# Hook pipeline test
echo '{"hook_event_name":"Stop"}' | py "D:/autolights/light_hook.py"
```

## Events

| Claude event | Pulses | When |
|---|---|---|
| `PermissionRequest` | 3 | Permission dialog pops up |
| `Elicitation` | 3 | Claude asks you a question |
| `Notification` | 3 | Desktop notification fires |
| `Stop` | 3 | Task finishes |

## Tuning

```
flash_overlay.py <count> <dark_ms> <light_ms> <alpha> <mode>
```

| Param | Default | What it does |
|---|---|---|
| `count` | 3 | Number of pulses |
| `dark_ms` | 100 | Overlay visible duration (ms) |
| `light_ms` | 400 | Pause between pulses (ms) |
| `alpha` | 100 | Overlay opacity (0-255) |
| `mode` | black | `black` or `white` |

## Why overlay instead of brightness

- **Instant** — no WMI cold start delay
- **All monitors** — works on external displays
- **Safe** — doesn't touch backlight, HDR, or Night Light
- **Focus-safe** — `WS_EX_NOACTIVATE` keeps terminal in focus

Also includes `blink_screen.ps1` (WMI brightness approach) as a fallback.

## License

MIT
