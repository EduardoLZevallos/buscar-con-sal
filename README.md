# Buscar con Sal - Articles Search

A simple static website for searching and browsing articles from Tortilla con Sal using Lunr.js.

## Setup

1. Generate the search index:
```bash
python3 generate-index.py
```

This creates `articles-index.json` with all article metadata.

## Local Testing

Since the site uses `fetch()`, you need to serve it with a local server:

```bash
# Python
python3 -m http.server 8000
# Then visit http://localhost:8000

# Or Node.js
npx serve .
```

## GitHub Pages Deployment

1. Push to GitHub
2. Enable GitHub Pages in repository settings (Settings → Pages)
3. Select the branch (usually `main`) and `/ (root)` folder
4. The site will be available at `https://yourusername.github.io/repo-name/`

## Files

- `index.html` - Main search page
- `articles-index.json` - Generated search index (run `generate-index.py` to regenerate)
- `generate-index.py` - Script to generate the search index from HTML files
- `articles/` - HTML article files (1,329 articles)
- `.nojekyll` - Tells GitHub Pages not to use Jekyll

## Search Features

- Full-text search across all articles
- Title-based search (boosted)
- Content-based search
- Real-time results as you type
- Search term highlighting
