param(
    [int]$IntervalSeconds = 60
)

. "$PSScriptRoot\LifeOps.Common.ps1"
try {
    $python = Initialize-LifeOpsEnvironment
    Write-LifeOpsLog 'Run-Watcher.ps1 entered.'
    & $python -m lifeops.activity_watcher --interval $IntervalSeconds
} catch {
    Write-LifeOpsLog "Run-Watcher.ps1 stopped: $($_.Exception.Message)"
    exit 1
}
