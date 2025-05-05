# Git Auto-Push Script
$ErrorActionPreference = "Stop"

Write-Host "🔄 Checking Git status..." -ForegroundColor Cyan

# Get current branch name
$currentBranch = git rev-parse --abbrev-ref HEAD

# Check if there are any changes to commit
$status = git status --porcelain

if ($status) {
    Write-Host "📝 Changes detected. Adding files..." -ForegroundColor Yellow
    git add .
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = Read-Host "Enter commit message (or press Enter for timestamp-based message)"
    
    if ([string]::IsNullOrWhiteSpace($commitMessage)) {
        $commitMessage = "Auto-commit at $timestamp"
    }
    
    Write-Host "📦 Committing changes..." -ForegroundColor Yellow
    git commit -m $commitMessage
}

# Check if branch has upstream
$hasUpstream = git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>$null

if (-not $hasUpstream) {
    Write-Host "⚠️ No upstream branch set. Setting upstream..." -ForegroundColor Yellow
    git push --set-upstream origin $currentBranch
} else {
    Write-Host "⬆️ Pushing changes..." -ForegroundColor Yellow
    git push
}

Write-Host "✅ Done!" -ForegroundColor Green 