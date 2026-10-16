param(
    [string]$Server = "123.207.246.112",
    [string]$User = "ubuntu",
    [string]$PrivateKey = "$HOME\.ssh\gis_tencent_deploy",
    [int]$LocalBoltPort = 17687,
    [int]$LocalHttpPort = 17474
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $PrivateKey)) {
    throw "SSH private key not found: $PrivateKey"
}

Write-Host "Opening secure tunnels for GIS traffic knowledge graph..."
Write-Host "Neo4j Bolt: bolt://localhost:$LocalBoltPort"
Write-Host "Neo4j Browser: http://localhost:$LocalHttpPort"
Write-Host "Press Ctrl+C to close the tunnel."

ssh `
    -N `
    -i $PrivateKey `
    -o IdentitiesOnly=yes `
    -o ExitOnForwardFailure=yes `
    -o ServerAliveInterval=30 `
    -o ServerAliveCountMax=3 `
    -L "${LocalBoltPort}:127.0.0.1:7687" `
    -L "${LocalHttpPort}:127.0.0.1:7474" `
    "${User}@${Server}"
