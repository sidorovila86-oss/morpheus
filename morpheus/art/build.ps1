# Builds all pixel-art sprites into art/out/
# Usage: powershell -ExecutionPolicy Bypass -File build.ps1
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Add-Type -Path (Join-Path $here "src\Art.cs") -ReferencedAssemblies System.Drawing
[Art]::Build((Join-Path $here "out"))
Write-Output "Sprites written to $(Join-Path $here 'out')"
