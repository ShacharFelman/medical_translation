param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AdditionalArgs
)

$ComposeFile = "docker-compose.yml"
$OutputDir = "output"
$InsightsFile = Join-Path $OutputDir "analytics_insights.txt"

# Ensure output directory exists
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Force -Path $OutputDir
}

try {
    Write-Host "Starting analytics module and MongoDB..."
    Write-Host "The process may take a few minutes. Please wait..."
    
    # Run docker-compose and capture the output
    $output = docker-compose -f $ComposeFile up --build $AdditionalArgs
    
    # Save the output to a file
    $output | Out-File -FilePath $InsightsFile

    Write-Host "`nAnalytics process complete."
    Write-Host "Results can be found in the '$OutputDir' directory:"
    Write-Host "1. Insights: $InsightsFile"
    Write-Host "2. Visualization plots: Various PNG files"
    Write-Host "`nTo view the results, check the files in the '$OutputDir' directory."
}
finally {
    Write-Host "`nShutting down containers..."
    docker-compose -f $ComposeFile down
    docker image prune -f
}