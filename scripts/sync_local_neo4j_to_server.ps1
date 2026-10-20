param(
    [string]$Server = "123.207.246.112",
    [string]$User = "ubuntu",
    [string]$PrivateKey = "$HOME\.ssh\gis_tencent_deploy",
    [int]$LocalBoltPort = 17687,
    [string]$RemoteDatabase = "neo4j",
    [string]$RemotePassword = "",
    [switch]$SkipExport,
    [switch]$PruneRelationships,
    [switch]$SkipHealthCheck
)

$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $RootDir "backend\.venv\Scripts\python.exe"
$ExportScript = Join-Path $RootDir "scripts\export_graph.py"
$ImportScript = Join-Path $RootDir "backend\import_snapshot.py"
$DeployEnv = Join-Path $RootDir "deploy\.env"

function Get-DotEnvValue {
    param(
        [string]$Path,
        [string]$Name
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return ""
    }

    $line = Get-Content -LiteralPath $Path | Where-Object {
        $_ -match "^\s*$([regex]::Escape($Name))\s*="
    } | Select-Object -First 1
    if (-not $line) {
        return ""
    }

    $value = ($line -split "=", 2)[1].Trim()
    if ($value.Length -ge 2) {
        if (($value.StartsWith('"') -and $value.EndsWith('"')) -or
            ($value.StartsWith("'") -and $value.EndsWith("'"))) {
            $value = $value.Substring(1, $value.Length - 2)
        }
    }
    return $value
}

function Wait-TcpPort {
    param(
        [string]$HostName,
        [int]$Port,
        [int]$TimeoutSeconds = 20
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $client = New-Object System.Net.Sockets.TcpClient
        try {
            $client.Connect($HostName, $Port)
            return
        } catch {
            Start-Sleep -Milliseconds 300
        } finally {
            $client.Dispose()
        }
    }
    throw "SSH tunnel did not open ${HostName}:$Port within $TimeoutSeconds seconds."
}

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Project Python environment not found: $Python"
}
if (-not (Test-Path -LiteralPath $PrivateKey)) {
    throw "SSH private key not found: $PrivateKey"
}
if (-not (Get-Command ssh.exe -ErrorAction SilentlyContinue)) {
    throw "ssh.exe was not found in PATH. Install or enable the OpenSSH client."
}

if (-not $RemotePassword) {
    $RemotePassword = $env:NEO4J_REMOTE_PASSWORD
}
if (-not $RemotePassword) {
    $RemotePassword = Get-DotEnvValue -Path $DeployEnv -Name "NEO4J_PASSWORD"
}
if (-not $RemotePassword) {
    throw "Remote Neo4j password is missing. Set deploy/.env NEO4J_PASSWORD or NEO4J_REMOTE_PASSWORD."
}

if (-not $SkipExport) {
    Write-Host "1/3 Exporting the local Neo4j graph..."
    & $Python $ExportScript
    if ($LASTEXITCODE -ne 0) {
        throw "Local Neo4j export failed. Use -SkipExport when data/graph-snapshot.json is already current."
    }
} else {
    Write-Host "1/3 Using the existing data/graph-snapshot.json..."
}

$sshArguments = @(
    "-N",
    "-i", $PrivateKey,
    "-o", "IdentitiesOnly=yes",
    "-o", "ExitOnForwardFailure=yes",
    "-o", "ServerAliveInterval=30",
    "-o", "ServerAliveCountMax=3",
    "-L", "${LocalBoltPort}:127.0.0.1:7687",
    "${User}@${Server}"
)

$tunnelProcess = $null
$environmentNames = @(
    "NEO4J_URI",
    "NEO4J_USER",
    "NEO4J_PASSWORD",
    "NEO4J_DATABASE"
)
$previousEnvironment = @{}

try {
    Write-Host "2/3 Opening an SSH tunnel to the remote Neo4j..."
    $tunnelProcess = Start-Process `
        -FilePath "ssh.exe" `
        -ArgumentList $sshArguments `
        -WindowStyle Hidden `
        -PassThru
    Wait-TcpPort -HostName "127.0.0.1" -Port $LocalBoltPort

    foreach ($name in $environmentNames) {
        $previousEnvironment[$name] = [Environment]::GetEnvironmentVariable(
            $name,
            "Process"
        )
    }
    $env:NEO4J_URI = "bolt://127.0.0.1:$LocalBoltPort"
    $env:NEO4J_USER = "neo4j"
    $env:NEO4J_PASSWORD = $RemotePassword
    $env:NEO4J_DATABASE = $RemoteDatabase

    Write-Host "3/3 Importing the local snapshot directly into remote Neo4j..."
    $importArguments = @("--apply")
    if ($PruneRelationships) {
        Write-Warning "PruneRelationships is enabled: stale relationships in the snapshot node scope will be deleted."
        $importArguments += "--prune-relationships"
    }
    & $Python $ImportScript @importArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Remote Neo4j synchronization failed."
    }
} finally {
    foreach ($name in $environmentNames) {
        [Environment]::SetEnvironmentVariable(
            $name,
            $previousEnvironment[$name],
            "Process"
        )
    }
    if ($tunnelProcess -and -not $tunnelProcess.HasExited) {
        Stop-Process -Id $tunnelProcess.Id -Force
        $tunnelProcess.Dispose()
    }
}

if (-not $SkipHealthCheck) {
    try {
        $health = Invoke-RestMethod `
            -Uri "http://$Server`:8080/api/health" `
            -TimeoutSec 10
        Write-Host "Remote API: $($health.status); Neo4j: $($health.database)"
    } catch {
        Write-Warning "Neo4j sync completed, but the public API health check failed: $($_.Exception.Message)"
    }
}

Write-Host "Synchronization completed without rebuilding or uploading the deployment package."
