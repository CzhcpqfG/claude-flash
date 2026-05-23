param(
    [int]$Count = 3,
    [int]$DimPercent = 0,
    [int]$DarkMs = 400,
    [int]$LightMs = 150
)

$ErrorActionPreference = 'SilentlyContinue'

$monitor = $null
$originalBrightness = $null

try {
    $monitor = Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightnessMethods
    if (-not $monitor) { exit 0 }

    $current = Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightness
    $originalBrightness = $current.CurrentBrightness

    for ($i = 0; $i -lt $Count; $i++) {
        $monitor | Invoke-CimMethod -MethodName WmiSetBrightness -Arguments @{
            Brightness = $DimPercent
            Timeout = 0
        } | Out-Null

        Start-Sleep -Milliseconds $DarkMs

        $monitor | Invoke-CimMethod -MethodName WmiSetBrightness -Arguments @{
            Brightness = $originalBrightness
            Timeout = 0
        } | Out-Null

        if ($i -lt $Count - 1) {
            Start-Sleep -Milliseconds $LightMs
        }
    }
}
finally {
    if ($originalBrightness -ne $null -and $monitor -ne $null) {
        $monitor | Invoke-CimMethod -MethodName WmiSetBrightness -Arguments @{
            Brightness = $originalBrightness
            Timeout = 0
        } | Out-Null
    }
}
