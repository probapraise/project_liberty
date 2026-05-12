param(
    [string]$Choice = 'return_now',
    [Nullable[int]]$DurationMinutes = $null,
    [string]$Reason = 'LifeOps intervention loop self-check'
)

. "$PSScriptRoot\LifeOps.Common.ps1"

try {
    $python = Initialize-LifeOpsEnvironment
    $args = @('-m', 'lifeops.intervention_self_check', '--choice', $Choice, '--reason', $Reason)
    if ($null -ne $DurationMinutes) {
        $args += @('--duration-minutes', $DurationMinutes)
    }
    & $python @args
    exit $LASTEXITCODE
} catch {
    Write-LifeOpsLog "Test-InterventionLoop.ps1 failed: $($_.Exception.Message)"
    Write-Host "Intervention loop self-check failed: $($_.Exception.Message)"
    exit 1
}
