param(
    [int]$IntervalSeconds = 60
)

. "$PSScriptRoot\LifeOps.Common.ps1"
try {
    $python = Initialize-LifeOpsEnvironment
    Write-LifeOpsLog 'Run-EventDispatcher.ps1 entered.'
    & $python -m lifeops.event_dispatcher --interval $IntervalSeconds
} catch {
    Write-LifeOpsLog "Run-EventDispatcher.ps1 stopped: $($_.Exception.Message)"
    exit 1
}
