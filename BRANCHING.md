# Git Branching Strategy

This project follows **Git Flow** branching model.

## Branch Structure

### Main Branches
- **`master`** - Production-ready code. Deploy from here only.
- **`develop`** - Integration branch. Base for all features.

### Feature Branches
- **`feature/core-infrastructure`** - Flask app, config, models, database
- **`feature/admin-panel`** - Admin routes and authentication
- **`feature/email-tracking`** - Email sending, open/click tracking
- **`feature/analytics`** - Dashboard, reports, metrics

### Workflow

1. **Create new feature** (from develop):
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** and commit:
   ```bash
   git add .
   git commit -m "Add feature description"
   ```

3. **Push to GitHub**:
   ```bash
   git push -u origin feature/your-feature-name
   ```

4. **Create Pull Request** on GitHub (from feature → develop)

5. **After review approval**, merge to develop:
   ```bash
   git checkout develop
   git pull origin develop
   git merge feature/your-feature-name
   ```

6. **Release to master** (when ready for production):
   ```bash
   git checkout master
   git pull origin master
   git merge develop
   git tag -a v1.0.0 -m "Version 1.0.0"
   git push origin master --tags
   ```

## Commit Message Convention

```
type(scope): description

[optional body]
[optional footer]
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style (formatting, etc.)
- `refactor` - Code refactoring
- `test` - Add tests
- `chore` - Build, dependencies, tooling

**Examples:**
```
feat(admin): add campaign deletion endpoint
fix(email): correct SMTP connection timeout
docs(readme): update installation steps
```

## Current Branch Status

| Branch | Status | Purpose |
|--------|--------|---------|
| master | ← MAIN STABLE | Production releases |
| develop | ← INTEGRATE | Development integration |
| feature/core-infrastructure | Active | App foundation |
| feature/admin-panel | Active | Admin features |
| feature/email-tracking | Active | Email functionality |
| feature/analytics | Active | Reporting & analytics |

## Protection Rules (Recommended for GitHub)

Set on GitHub repository settings:
- **`master`** - Require PR reviews before merge, block direct pushes
- **`develop`** - Require PR reviews, allow force push for maintainers only
- All branches - Require status checks to pass

## First Time Setup

After cloning:
```bash
git clone https://github.com/Drish973/spear-phisher.git
cd spear-phisher
git checkout develop
```

This ensures you start from the latest development branch.
