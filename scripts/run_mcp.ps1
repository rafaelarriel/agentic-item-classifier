<#!
.SYNOPSIS
Atalho opcional para iniciar o MCP a partir da raiz do projeto.
#>
$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot
python -m app.mcp.server
