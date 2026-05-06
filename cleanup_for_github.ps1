# Cleanup script for GitHub upload
# Run this before pushing to GitHub

Write-Host "🧹 Cleaning up repository for GitHub..." -ForegroundColor Cyan

# Remove extra documentation files
Write-Host "`n📄 Removing extra documentation files..." -ForegroundColor Yellow
$filesToRemove = @(
    "README_UPDATES.md",
    "ARCHITECTURE.md"
)

foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  ✅ Removed: $file" -ForegroundColor Green
    }
}

# Remove output directories (they'll be recreated)
Write-Host "`n📁 Cleaning output directories..." -ForegroundColor Yellow
$dirsToClean = @(
    "output_videos",
    "csv_output",
    "stubs"
)

foreach ($dir in $dirsToClean) {
    if (Test-Path $dir) {
        Get-ChildItem -Path $dir -Recurse | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
        Write-Host "  ✅ Cleaned: $dir/" -ForegroundColor Green
    }
}

# Remove Python cache
Write-Host "`n🐍 Removing Python cache..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "  ✅ Python cache removed" -ForegroundColor Green

# Create necessary directories
Write-Host "`n📂 Creating necessary directories..." -ForegroundColor Yellow
$dirsToCreate = @(
    "output_videos",
    "csv_output",
    "stubs"
)

foreach ($dir in $dirsToCreate) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✅ Created: $dir/" -ForegroundColor Green
    }
}

# Create .gitkeep files to preserve empty directories
Write-Host "`n📌 Adding .gitkeep files..." -ForegroundColor Yellow
foreach ($dir in $dirsToCreate) {
    $gitkeepPath = Join-Path $dir ".gitkeep"
    if (-not (Test-Path $gitkeepPath)) {
        New-Item -ItemType File -Path $gitkeepPath -Force | Out-Null
        Write-Host "  ✅ Added: $dir/.gitkeep" -ForegroundColor Green
    }
}

Write-Host "`n✨ Cleanup complete! Repository is ready for GitHub." -ForegroundColor Green
Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review the changes" -ForegroundColor White
Write-Host "  2. Initialize git: git init" -ForegroundColor White
Write-Host "  3. Add files: git add ." -ForegroundColor White
Write-Host "  4. Commit: git commit -m 'Initial commit with game analysis integration'" -ForegroundColor White
Write-Host "  5. Add remote: git remote add origin https://github.com/MuhammadAhmad174/basketball-Analysis.git" -ForegroundColor White
Write-Host "  6. Push: git push -u origin main" -ForegroundColor White
