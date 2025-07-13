# LinkedIn Monitor PowerShell Launcher
Write-Host "🔍 LinkedIn Monitor" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.7 or higher." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if required files exist
$requiredFiles = @("linkedin_monitor.py", "requirements.txt")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Found $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing $file" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Check if .env file exists
if (Test-Path ".env") {
    Write-Host "✅ Found .env file" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found. Running setup..." -ForegroundColor Yellow
    python setup.py
}

Write-Host ""
Write-Host "🚀 Starting LinkedIn Monitor..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the monitor" -ForegroundColor Yellow
Write-Host ""

try {
    python linkedin_monitor.py
} catch {
    Write-Host "❌ Error running LinkedIn Monitor: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
} 