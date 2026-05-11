. "$PSScriptRoot\LifeOps.Common.ps1"
$python = Initialize-LifeOpsEnvironment
& $python -m lifeops.cli write-daily-summary
