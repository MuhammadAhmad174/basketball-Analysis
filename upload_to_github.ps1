# Complete GitHub Upload Script
# This script will prepare and upload your repository to GitHub

Write-Host "🚀 Basketball Analysis - GitHub Upload Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Step 1: Cleanup
Write-Host "`n📋 Step 1: Cleaning up repository..." -ForegroundColor Yellow
.\cleanup_for_github.ps1

# Step 2: Check if git is initialized
Write-Host "`n📋 Step 2: Initializing Git..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "  ✅ Git initialized" -ForegroundColor Green
} else {
    Write-Host "  ℹ️  Git already initialized" -ForegroundColor Blue
}

# Step 3: Configure git (optional - will use global config if not set)
Write-Host "`n📋 Step 3: Git Configuration" -ForegroundColor Yellow
$userName = git config user.name
$userEmail = git config user.email

if (-not $userName) {
    Write-Host "  ⚠️  Git user.name not set" -ForegroundColor Red
    $name = Read-Host "  Enter your name"
    git config user.name "$name"
}

if (-not $userEmail) {
    Write-Host "  ⚠️  Git user.email not set" -ForegroundColor Red
    $email = Read-Host "  Enter your email"
    git config user.email "$email"
}

Write-Host "  ✅ Git configured" -ForegroundColor Green
Write-Host "     Name: $(git config user.name)" -ForegroundColor Gray
Write-Host "     Email: $(git config user.email)" -ForegroundColor Gray

# Step 4: Add all files
Write-Host "`n📋 Step 4: Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "  ✅ Files added" -ForegroundColor Green

# Step 5: Create commit
Write-Host "`n📋 Step 5: Creating commit..." -ForegroundColor Yellow
$commitMessage = @"
🎉 Initial commit: Basketball Analysis with AI-powered game analytics

Features:
- Player and ball tracking with YOLO models
- Team assignment and possession detection
- Pass and interception detection
- Speed and distance metrics
- CSV data export
- AI-powered game analysis with ML models
- Comprehensive visualizations and reports
- 50+ engineered features
- Predictive models for possession and passes
- Player performance classification
"@

git commit -m $commitMessage
Write-Host "  ✅ Commit created" -ForegroundColor Green

# Step 6: Add remote
Write-Host "`n📋 Step 6: Adding remote repository..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/MuhammadAhmad174/basketball-Analysis.git"

# Check if remote already exists
$existingRemote = git remote get-url origin 2>$null

if ($existingRemote) {
    Write-Host "  ℹ️  Remote 'origin' already exists: $existingRemote" -ForegroundColor Blue
    $response = Read-Host "  Do you want to update it? (y/n)"
    if ($response -eq 'y') {
        git remote set-url origin $remoteUrl
        Write-Host "  ✅ Remote updated" -ForegroundColor Green
    }
} else {
    git remote add origin $remoteUrl
    Write-Host "  ✅ Remote added: $remoteUrl" -ForegroundColor Green
}

# Step 7: Create main branch and push
Write-Host "`n📋 Step 7: Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "  ⚠️  This will push to: $remoteUrl" -ForegroundColor Yellow
$response = Read-Host "  Continue? (y/n)"

if ($response -eq 'y') {
    git branch -M main
    
    Write-Host "  📤 Pushing to GitHub..." -ForegroundColor Cyan
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✨ SUCCESS! Repository uploaded to GitHub!" -ForegroundColor Green
        Write-Host "`n🔗 View your repository at:" -ForegroundColor Cyan
        Write-Host "   https://github.com/MuhammadAhmad174/basketball-Analysis" -ForegroundColor White
        
        Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
        Write-Host "  1. Add repository description and topics" -ForegroundColor White
        Write-Host "  2. Upload a social preview image" -ForegroundColor White
        Write-Host "  3. Enable GitHub Pages (optional)" -ForegroundColor White
        Write-Host "  4. Share your repository!" -ForegroundColor White
        
        Write-Host "`n📚 See GITHUB_UPLOAD_GUIDE.md for more details" -ForegroundColor Gray
    } else {
        Write-Host "`n❌ Push failed. Please check the error message above." -ForegroundColor Red
        Write-Host "   Common issues:" -ForegroundColor Yellow
        Write-Host "   - Authentication required (use GitHub token or SSH)" -ForegroundColor Gray
        Write-Host "   - Repository does not exist on GitHub" -ForegroundColor Gray
        Write-Host "   - No permission to push" -ForegroundColor Gray
    }
} else {
    Write-Host "`n⏸️  Push cancelled. You can push manually later with:" -ForegroundColor Yellow
    Write-Host "   git push -u origin main" -ForegroundColor White
}

Write-Host "`n✅ Script complete!" -ForegroundColor Green
