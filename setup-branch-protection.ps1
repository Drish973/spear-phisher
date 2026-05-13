# Branch Protection Setup Script for GitHub (PowerShell)
# This script sets up branch protection rules using GitHub CLI
# Usage: .\setup-branch-protection.ps1

$REPO = "Drish973/spear-phisher"

Write-Host "Setting up branch protection rules for $REPO..." -ForegroundColor Cyan
Write-Host ""

# Protect master branch
Write-Host "Protecting 'master' branch..." -ForegroundColor Yellow

$masterProtection = @{
    required_status_checks = $null
    enforce_admins = $true
    required_pull_request_reviews = @{
        dismiss_stale_reviews = $true
        require_code_owner_reviews = $false
        required_approving_review_count = 1
    }
    restrictions = $null
    required_linear_history = $true
    allow_force_pushes = $false
    allow_deletions = $false
} | ConvertTo-Json

$masterProtection | gh api repos/$REPO/branches/master/protection --input -

# Protect develop branch
Write-Host "Protecting 'develop' branch..." -ForegroundColor Yellow

$developProtection = @{
    required_status_checks = $null
    enforce_admins = $true
    required_pull_request_reviews = @{
        dismiss_stale_reviews = $true
        require_code_owner_reviews = $false
        required_approving_review_count = 1
    }
    restrictions = $null
    required_linear_history = $true
    allow_force_pushes = $false
    allow_deletions = $false
} | ConvertTo-Json

$developProtection | gh api repos/$REPO/branches/develop/protection --input -

Write-Host ""
Write-Host "✓ Branch protection rules configured!" -ForegroundColor Green
Write-Host ""
Write-Host "Protected branches:" -ForegroundColor Cyan
Write-Host "  • master - Requires PR with 1 approval"
Write-Host "  • develop - Requires PR with 1 approval"
