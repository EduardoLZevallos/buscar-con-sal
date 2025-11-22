#!/usr/bin/env python3
"""
Generate articles-index.json for Lunr.js search
"""
import os
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

def extract_text_from_html(html_file):
    """Extract text content from HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Limit to first 5000 chars for indexing
        return text[:5000]
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return ""

def extract_title_from_html(html_file):
    """Extract title from HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Try title tag first
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
            # Remove common suffixes
            title = re.sub(r'\s*\|\s*.*$', '', title)
            if title:
                return title
        
        # Fallback to filename
        return Path(html_file).stem.replace('_', ' ').replace('-', ' ')
    except Exception:
        return Path(html_file).stem.replace('_', ' ').replace('-', ' ')

def main():
    articles_dir = Path('articles')
    articles = []
    
    if not articles_dir.exists():
        print(f"Error: {articles_dir} directory not found")
        return
    
    print("Scanning HTML files...")
    html_files = sorted(articles_dir.glob('*.html'))
    
    for html_file in html_files:
        title = extract_title_from_html(html_file)
        content = extract_text_from_html(html_file)
        path = f"articles/{html_file.name}"
        
        articles.append({
            'title': title,
            'content': content,
            'path': path
        })
        
        if len(articles) % 100 == 0:
            print(f"  Processed {len(articles)}/{len(html_files)} files...")
    
    # Save index
    with open('articles-index.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Generated articles-index.json with {len(articles)} articles")

if __name__ == '__main__':
    main()

