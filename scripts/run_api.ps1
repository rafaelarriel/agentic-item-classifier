<#!
.SYNOPSIS
Atalho opcional para iniciar a API em modo de desenvolvimento.
#>
$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
