. "$PSScriptRoot\LifeOps.Common.ps1"

$taskName = 'LifeOpsCodexOperator'
$ps = Get-LifeOpsPowerShell
$startScript = Join-Path $PSScriptRoot 'Start-LifeOps.ps1'
$argument = "-NoProfile -ExecutionPolicy Bypass -File `"$startScript`""
$action = New-ScheduledTaskAction -Execute $ps -Argument $argument
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description 'Start LifeOps Codex Operator at user logon.' -Force | Out-Null
Write-LifeOpsLog "Installed startup task $taskName."
Write-Host "Installed startup task: $taskName"
