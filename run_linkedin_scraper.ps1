#!/usr/bin/env pwsh
# LinkedIn Notifications Scraper PowerShell Script

Write-Host "LinkedIn Notifications Scraper" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Make sure you have:" -ForegroundColor Yellow
Write-Host "1. Chrome running with: chrome --remote-debugging-port=9222" -ForegroundColor White
Write-Host "2. LinkedIn notifications page open and logged in" -ForegroundColor White
Write-Host "3. SLACK_WEBHOOK_URL configured in config.env" -ForegroundColor White
Write-Host ""

$response = Read-Host "Press Enter to continue or 'q' to quit"
if ($response -eq 'q') {
    exit
}

Write-Host ""
Write-Host "Starting scraper..." -ForegroundColor Green
python linkedin_notifications_scraper.py

Write-Host ""
Write-Host "Script completed. Press Enter to exit..." -ForegroundColor Cyan
Read-Host
