# Security Commands Reference

## 🛡️ GitGuardian & Security Tools Quick Reference

### Daily Security Checks
```bash
# Full security scan (recommended daily)
./scan_secrets.sh

# Quick GitGuardian scan of current changes
ggshield secret scan pre-commit

# Full GitGuardian repository scan (comprehensive)
ggshield secret scan path . --recursive
```

### GitGuardian CLI Commands
```bash
# Authentication
ggshield auth login                    # Login to GitGuardian
ggshield auth logout                   # Logout from GitGuardian

# Scanning
ggshield secret scan path <path>       # Scan specific path
ggshield secret scan pre-commit        # Scan staged files
ggshield secret scan ci                # Scan for CI/CD

# Git integration
ggshield secret scan repo <repo-url>   # Scan remote repository
ggshield secret scan commit-range <range>  # Scan commit range
```

### detect-secrets Commands  
```bash
# Scan for secrets
detect-secrets scan --all-files .

# Create/update baseline
detect-secrets scan --update .secrets.baseline

# Audit detected secrets
detect-secrets audit .secrets.baseline
```

### Environment Variables
```bash
# View loaded environment variables (without exposing values)
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('ESV_API_KEY:', 'Set' if os.getenv('ESV_API_KEY') else 'Not Set')"

# Test .env file loading
python -c "from dotenv import load_dotenv; load_dotenv(); print('Environment loaded successfully')"
```

### File Permissions & Security
```bash
# Set secure .env permissions
chmod 600 .env

# Check .env permissions
ls -la .env

# Verify .env in .gitignore
grep "^\.env$" .gitignore
```

### Git Security
```bash
# Check for secrets in git history
git log -p --all -S "api_key_string_here"

# Remove secrets from git history (DANGEROUS)
git filter-repo --replace-text <(echo "secret==>***REDACTED***")

# Force push cleaned history (coordinate with team!)
git push --force-with-lease origin main
```

## 🔧 Troubleshooting

### GitGuardian Issues
```bash
# Check authentication status
ggshield auth status

# Re-authenticate
ggshield auth login --method=token

# Test API connectivity
ggshield quota
```

### detect-secrets Issues
```bash
# Regenerate baseline (if too many false positives)
detect-secrets scan --baseline .secrets.baseline --update

# Add false positive to baseline
detect-secrets scan --baseline .secrets.baseline --update --all-files
```

## 📋 Best Practices

1. **Never commit secrets** - Use environment variables
2. **Run `./scan_secrets.sh` daily** - Catch issues early  
3. **Use pre-commit hooks** - Automatic protection
4. **Keep .env permissions at 600** - Restrict access
5. **Rotate exposed secrets immediately** - If leaked, change them
6. **Review GitGuardian dashboard weekly** - Check for new alerts

## 🚨 Emergency Response

If secrets are detected:

1. **Stop** - Don't commit/push
2. **Remove** - Delete secrets from code
3. **Environment** - Move to .env file
4. **Rotate** - Change the exposed secret
5. **History** - Clean git history if already committed
6. **Push** - Force push cleaned history (if needed)

## 🔗 Useful Links

- [GitGuardian Dashboard](https://dashboard.gitguardian.com/)
- [GitGuardian CLI Docs](https://docs.gitguardian.com/ggshield-docs/)
- [detect-secrets](https://github.com/Yelp/detect-secrets)
