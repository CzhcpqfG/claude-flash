# ⚡ claude-flash

> Your laptop screen blinks when Claude Code needs you. No popups. No mouse. No missed prompts.

![platform](https://img.shields.io/badge/platform-Windows%2011-blue)
![license](https://img.shields.io/badge/license-MIT-green)

Claude Code runs in the terminal. You look away. Minutes pass. Claude is waiting for your permission — but you didn't notice.

**claude-flash** blinks your laptop's backlight the moment Claude needs attention. Permission dialogs, input prompts, task completions — each gets its own visual nudge.

## How it looks

Your screen dims black for 400ms, snaps back for 150ms, repeats. Like someone flicking the lights — impossible to miss, no popups to dismiss.

## How it works

```
Claude event → settings.json hook → light_hook.py → blink_screen.ps1 → WMI backlight blink
```

Every blink is ~0.5 seconds. Screen brightness always restores — even if the script crashes.

## Quick start

**Prerequisites:** Windows laptop, Python 3, PowerShell 5+

```powershell
git clone https://github.com/CzhcpqfG/claude-flash.git D:\autolights
```

Then add this to your `~/.claude/settings.json`:

<details>
<summary>Click to expand hook config</summary>

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [{ "type": "command", "command": "py \"D:/autolights/light_hook.py\"" }]
      }
    ],
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
# Direct test — screen blinks 3 times
powershell -ExecutionPolicy Bypass -File "D:\autolights\blink_screen.ps1" -Count 3

# Hook pipeline test — screen blinks 2 times
echo '{"hook_event_name":"Stop"}' | py "D:/autolights/light_hook.py"
```

## Events mapped

| Claude event | Blinks | When |
|---|---|---|
| `PermissionRequest` | 2 | Permission dialog pops up |
| `Elicitation` | 2 | Claude asks you a question |
| `Notification` | 2 | Desktop notification fires |
| `Stop` | 2 | Task finishes |
| `SessionStart` | warmup | Primes WMI for instant response |

## Tuning

```powershell
blink_screen.ps1 -Count 3 -DarkMs 600 -LightMs 100 -DimPercent 0
```

| Param | Default | What it does |
|---|---|---|
| `-Count` | 3 | Number of blinks |
| `-DarkMs` | 400 | How long screen stays dim (ms) |
| `-LightMs` | 150 | Pause between blinks (ms) |
| `-DimPercent` | 0 | Brightness when dimmed (0 = off) |

## Why WMI

Uses the same backlight API as Windows itself. Night Light and HDR keep working. External monitors are unaffected. Gamma ramp hacks break color profiles — WMI doesn't.

## License

MIT
