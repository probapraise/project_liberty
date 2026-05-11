. "$PSScriptRoot\LifeOps.Common.ps1"

$taskName = 'LifeOpsCodexOperator'
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-LifeOpsLog "Removed startup task $taskName."
    Write-Host "Removed startup task: $taskName"
} else {
    Write-Host "Startup task was not installed: $taskName"
}
