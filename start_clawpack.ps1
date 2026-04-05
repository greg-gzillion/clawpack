# start_clawpack.ps1
Write-Host "🦞 Starting Clawpack..." -ForegroundColor Cyan

# Set environment variables
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:11434"
$env:ANTHROPIC_API_KEY = "ollama"

# Check if Ollama is running
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "Starting Ollama..." -ForegroundColor Yellow
    Start-Process "C:\Users\greg\AppData\Local\Programs\Ollama\ollama.exe"
    Start-Sleep -Seconds 5
}

Write-Host "✅ Environment ready!" -ForegroundColor Green
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Yellow
Write-Host "  python train_all_agents_on_tx.py"
Write-Host "  python query_agent_tx_knowledge.py eagleclaw"