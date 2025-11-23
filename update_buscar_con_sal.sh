#!/bin/bash
# Update articles and deploy to GitHub Pages

set -e  # Exit on error

# Set UV path
UV="/home/me/.local/bin/uv"

echo "🚀 Starting workflow to update articles and deploy..."

# Step 1: Copy articles
echo ""
echo "============================================================"
echo "Step 1: Copy articles from backup"
echo "============================================================"
"$UV" run copy-all-articles.py

# Step 2: Generate index
echo ""
echo "============================================================"
echo "Step 2: Generate search index"
echo "============================================================"
"$UV" run generate-index.py

# Step 3: Check git status
echo ""
echo "============================================================"
echo "Step 3: Checking git status..."
echo "============================================================"
git status --short

# Check if there are changes
if [ -z "$(git status --porcelain articles/ articles-index.json)" ]; then
    echo ""
    echo "✓ No changes to commit. Everything is up to date!"
    exit 0
fi

# Step 4: Stage changes
echo ""
echo "============================================================"
echo "Step 4: Staging changes"
echo "============================================================"
git add articles/ articles-index.json

# Step 5: Commit
echo ""
echo "============================================================"
echo "Step 5: Committing changes"
echo "============================================================"
git commit -m "Update articles and search index"

# Step 6: Push (with confirmation)
echo ""
echo "============================================================"
echo "Ready to push to GitHub Pages"
echo "============================================================"
echo "This will deploy the changes to the live site."
echo ""
read -p "Push to main? (yes/no): " -r
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]] && [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Push cancelled by user"
    exit 0
fi

echo ""
echo "============================================================"
echo "Step 6: Pushing to GitHub"
echo "============================================================"
git push origin main

echo ""
echo "============================================================"
echo "✅ Workflow completed successfully!"
echo "Your changes should be live on GitHub Pages shortly."
echo "============================================================"