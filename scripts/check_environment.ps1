$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $PSScriptRoot
$BackendPython = Join-Path $RootDir "backend\.venv\Scripts\python.exe"
$FrontendDir = Join-Path $RootDir "frontend"

if (-not (Test-Path -LiteralPath $BackendPython)) {
    throw "Backend virtual environment not found: $BackendPython"
}

Write-Host "Backend Python:"
& $BackendPython --version
& $BackendPython -m pip --version
& $BackendPython -m pip check

Write-Host "Frontend Node.js:"
Push-Location $FrontendDir
try {
    node --version
    npm --version
}
finally {
    Pop-Location
}

Write-Host "Environment check completed."
