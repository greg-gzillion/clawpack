# copy_missing_agents.ps1 - Copy missing agents from /dev/ to clawpack/agents/

$originalPath = "C:\Users\greg\dev"
$clawpackPath = "C:\Users\greg\dev\clawpack\agents"

$missingAgents = @(
    "claw",
    "clawpack",
    "clawpack-backup-security",
    "TX",)

Write-Host "🔄 Copying missing agents to clawpack..." -ForegroundColor Cyan

foreach ($agentName in $missingAgents) {
    $source = Join-Path $originalPath $agentName
    $dest = Join-Path $clawpackPath $agentName
    
    if (Test-Path $source) {
        Write-Host "`n📁 Copying $agentName..." -ForegroundColor Yellow
        robocopy $source $dest /E /COPY:DAT /R:2 /W:5 /XD "__pycache__" ".git" "venv" ".venv"
        Write-Host "   ✅ Copied to clawpack/agents/$agentName" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Source not found: $agentName" -ForegroundColor Red
    }
}

Write-Host "`n✅ Copy complete!" -ForegroundColor Green
Write-Host "Run 'git status' to see what was added" -ForegroundColor Cyan
