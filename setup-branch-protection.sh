#!/bin/bash
# Branch Protection Setup Script for GitHub
# This script sets up branch protection rules using GitHub CLI

REPO="Drish973/spear-phisher"

echo "Setting up branch protection rules for $REPO..."

# Protect master branch
echo "Protecting 'master' branch..."
gh api repos/$REPO/branches/master/protection \
  --input - <<EOF
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF

# Protect develop branch
echo "Protecting 'develop' branch..."
gh api repos/$REPO/branches/develop/protection \
  --input - <<EOF
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF

echo ""
echo "✓ Branch protection rules configured!"
echo ""
echo "Protected branches:"
echo "  • master - Requires PR with 1 approval"
echo "  • develop - Requires PR with 1 approval"
