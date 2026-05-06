# Simple GitHub Upload Script

Write-Host "Basketball Analysis - GitHub Upload" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Initialize Git
Write-Host "`nInitializing Git..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "Git initialized" -ForegroundColor Green
}

# Add files
Write-Host "`nAdding files..." -ForegroundColor Yellow
git add .
Write-Host "Files added" -ForegroundColor Green

# Create commit
Write-Host "`nCreating commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Basketball Analysis with AI-powered game analytics"
Write-Host "Commit created" -ForegroundColor Green

# Add remote
Write-Host "`nAdding remote..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/MuhammadAhmad174/basketball-Analysis.git"
git remote add origin $remoteUrl 2>$null
if ($LASTEXITCODE -ne 0) {
    git remote set-url origin $remoteUrl
}
Write-Host "Remote configured: $remoteUrl" -ForegroundColor Green

# Push to GitHub
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
Write-Host "This will push to: $remoteUrl" -ForegroundColor Cyan
$response = Read-Host "Continue? (y/n)"

if ($response -eq 'y') {
    git branch -M main
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nSUCCESS! Repository uploaded!" -ForegroundColor Green
        Write-Host "`nView at: https://github.com/MuhammadAhmad174/basketball-Analysis" -ForegroundColor Cyan
    } else {
        Write-Host "`nPush failed. Check error above." -ForegroundColor Red
        Write-Host "You may need to authenticate with GitHub" -ForegroundColor Yellow
    }
} else {
    Write-Host "`nCancelled. Push manually with: git push -u origin main" -ForegroundColor Yellow
}

Write-Host "`nDone!" -ForegroundColor Green
