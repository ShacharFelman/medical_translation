param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$TestNames,
    [switch]$nomongo
)

$TestsToRun = if ($TestNames) {
    ($TestNames | ForEach-Object { "tests.$_" }) -join ','
}
else {
    "all"
}

if ($TestsToRun -eq "all") {
    Write-Host "No specific tests specified. Running all tests."
}
else {
    Write-Host "Running tests: $TestsToRun"
}

$ComposeFile = if ($nomongo) {
    "docker-compose.nomongo.test.yml"
}
else {
    "docker-compose.test.yml"
}

try {
    $env:TESTS_TO_RUN = $TestsToRun
    docker-compose -f $ComposeFile up --build
}
finally {
    docker image prune -f
}
