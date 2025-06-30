#!/bin/bash
# Comprehensive security scan script

echo "🛡️  SECURITY SCAN REPORT"
echo "========================"
echo "📅 $(date)"
echo ""

# 1. Detect-secrets scan
echo "🔍 1. Scanning for secrets with detect-secrets..."
if detect-secrets scan --baseline .secrets.baseline --all-files; then
    echo "✅ No new secrets detected by detect-secrets"
else
    echo "❌ New secrets found by detect-secrets! Review immediately."
fi
echo ""

# 1.5. GitGuardian scan (if authenticated)
echo "🔍 1.5. Scanning with GitGuardian CLI..."
if command -v ggshield >/dev/null 2>&1; then
    echo "   - Running GitGuardian scan on staged/modified files..."
    if git diff --name-only --cached 2>/dev/null | head -1 | grep -q .; then
        # Scan staged files if any
        ggshield secret scan pre-commit 2>/dev/null && echo "✅ No secrets in staged files" || echo "⚠️  Secrets detected in staged files"
    else
        echo "   - No staged files to scan"
        echo "   - Note: Full repository scan available with 'ggshield secret scan path . --recursive'"
    fi
else
    echo "⚠️  GitGuardian CLI not available"
fi
echo ""

# 2. Check for common security issues
echo "🔍 2. Checking for common security issues..."

# Check for hardcoded passwords/keys in Python files
echo "   - Checking Python files for hardcoded credentials..."
if grep -r -i "password\|secret\|key\|token" --include="*.py" . | grep -v ".env\|os.getenv\|environment" | grep -q "="; then
    echo "⚠️  Potential hardcoded credentials found in Python files!"
    grep -r -i "password\|secret\|key\|token" --include="*.py" . | grep -v ".env\|os.getenv\|environment" | grep "="
else
    echo "✅ No hardcoded credentials found in Python files"
fi

# Check .env file permissions
echo "   - Checking .env file permissions..."
if [ -f ".env" ]; then
    if [ $(stat -c "%a" .env) = "600" ]; then
        echo "✅ .env file has secure permissions (600)"
    else
        echo "⚠️  .env file permissions should be 600 (current: $(stat -c "%a" .env))"
        echo "   Fix with: chmod 600 .env"
    fi
else
    echo "ℹ️  No .env file found"
fi

# Check if .env is in .gitignore
echo "   - Checking if .env is in .gitignore..."
if grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo "✅ .env is properly ignored by git"
else
    echo "❌ .env is NOT in .gitignore! Add it immediately."
fi

echo ""
echo "🛡️  Security scan complete!"
echo "========================"
