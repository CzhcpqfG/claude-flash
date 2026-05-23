# autolights

Screen brightness blink notification for Claude Code hooks. Flashes the laptop backlight when Claude needs your attention — no popups, no mouse interference.

## How it works

```
Claude Code event → settings.json hook → light_hook.py → blink_screen.ps1 → WMI brightness blink
```

- `light_hook.py` — Python hook dispatcher, reads event JSON from stdin
- `blink_screen.ps1` — PowerShell WMI script, dims and restores laptop backlight

WMI is warmed up on `SessionStart` so subsequent blinks are instant (avoids 20-50s WMI cold start).

## Setup

### 1. Clone and install

```powershell
git clone https://github.com/CzhcpqfG/autolights.git D:\autolights
```

No dependencies — just Python 3 and PowerShell.

### 2. Configure Claude Code hooks

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "py \"D:/autolights/light_hook.py\""
          }
        ]
      }
    ],
    "PermissionRequest": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "py \"D:/autolights/light_hook.py\""
          }
        ]
      }
    ],
    "Elicitation": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "py \"D:/autolights/light_hook.py\""
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "py \"D:/autolights/light_hook.py\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "py \"D:/autolights/light_hook.py\""
          }
        ]
      }
    ]
  }
}
```

### 3. Test

```powershell
# Direct blink test (3 flashes)
powershell -ExecutionPolicy Bypass -File "D:\autolights\blink_screen.ps1" -Count 3

# Hook pipeline test
echo '{"hook_event_name":"Stop"}' | py "D:/autolights/light_hook.py"
```

## Events

| Event | Blinks | When |
|---|---|---|
| `SessionStart` | none | WMI warmup only |
| `PermissionRequest` | 2 | Permission dialog appears |
| `Elicitation` | 2 | Claude asks for input |
| `Notification` | 2 | Desktop notification |
| `Stop` | 2 | Task completed |

## blink_screen.ps1 parameters

```
-Count 3        # Number of blinks
-DarkMs 400     # Milliseconds screen stays dim
-LightMs 150    # Milliseconds between blinks
-DimPercent 0   # Brightness level during dim (0-100)
```

## Requirements

- Windows laptop with built-in display (WMI brightness control)
- Python 3
- PowerShell 5+
