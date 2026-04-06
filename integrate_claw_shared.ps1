
Write-Host "🦞 CLAWPACK - UNIFIED LLM INTEGRATION" -ForegroundColor Cyan
Write-Host "="*70

# 1. BACKUP ALL AGENTS
Write-Host "`n📦 Creating backup..." -ForegroundColor Yellow
$backupDir = "agents_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item -Path "agents" -Destination $backupDir -Recurse -ErrorAction SilentlyContinue
Write-Host "✅ Backup saved to: $backupDir" -ForegroundColor Green

# 2. CREATE THE UNIFIED IMPORT HEADER FOR AGENTS
$unifiedHeader = @'
# Unified LLM from claw_shared
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from claw_shared.llm_integration import llm
'@

# 3. UPDATE EACH AGENT
$agentFiles = @(
    "agents/docuclaw/docuclaw_shared.py",
    "agents/mediclaw/mediclaw_shared.py",
    "agents/polyclaw/polyclaw_shared.py",
    "agents/unified/unified_shared.py"
)

Write-Host "`n🔄 Updating agents..." -ForegroundColor Yellow

foreach ($file in $agentFiles) {
    if (Test-Path $file) {
        Write-Host "  Updating: $file" -ForegroundColor Gray
        $content = Get-Content $file -Raw
        
        # Remove old key code
        $content = $content -replace '(?s)# Secure API key loading.*?raise ValueError\("Missing API key"\)\s+', ''
        $content = $content -replace 'CLOUD_API_KEY = os.environ.get\("OPENROUTER_API_KEY"\)', ''
        $content = $content -replace 'CLOUD_API_KEY = "[^"]*"', ''
        
        # Add unified header at top
        if ($content -match '^#!/usr/bin/env python3') {
            $content = $content -replace '(#!/usr/bin/env python3\r?\n)', "`$1$unifiedHeader`n"
        } else {
            $content = "$unifiedHeader`n$content"
        }
        
        # Replace _call_ai method
        $newCallAi = @'
    def _call_ai(self, prompt: str, task: str = "general") -> str:
        """Use unified LLM from claw_shared"""
        return llm.generate_with_learning(prompt, task)
'@
        
        if ($content -match 'def _call_ai') {
            $content = $content -replace '(?s)def _call_ai\(self,.*?\) -> str:.*?(?=\n    def|\n    \w|\Z)', $newCallAi
        }
        
        Set-Content $file $content -NoNewline
        Write-Host "    ✅ Updated" -ForegroundColor Green
    }
}

# 4. VERIFY NO HARDCODED KEYS
Write-Host "`n🔍 Verifying no hardcoded keys remain..." -ForegroundColor Yellow
$keysFound = Get-ChildItem -Path "agents" -Recurse -Filter "*.py" | Select-String -Pattern "sk-or-v1-"
if ($keysFound) {
    Write-Host "⚠️ WARNING: Hardcoded keys still found" -ForegroundColor Red
} else {
    Write-Host "✅ No hardcoded keys found!" -ForegroundColor Green
}

# 5. TEST THE SYSTEM
Write-Host "`n🧪 Testing unified LLM system..." -ForegroundColor Yellow
python -c "
import sys
sys.path.insert(0, 'C:/Users/greg/dev/clawpack')
from claw_shared.llm_integration import llm
result = llm.generate_with_learning('Say hello', 'general')
print('✅ Unified LLM is working!' if result and not result.startswith('❌') else '❌ Test failed')
"

Write-Host "`n" + "="*70
Write-Host "🎉 INTEGRATION COMPLETE!" -ForegroundColor Green
Write-Host "="*70
Write-Host "`nTest with: python agents/docuclaw/docuclaw_shared.py" -ForegroundColor Cyan
Write-Host "Then type: /write test" -ForegroundColor Cyan
🚀 RUN THE FIXED SCRIPT