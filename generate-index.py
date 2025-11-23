# /// script
# dependencies = [
#   "beautifulsoup4",
#   "lunr",
# ]
# ///
"""
Generate articles-index.json and pre-built Lunr index for faster loading
"""
import os
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from lunr import lunr

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
        # Limit to first 2000 chars for indexing (optimized for performance with 8000+ articles)
        # 2000 chars (~330 words) is sufficient for search while keeping file size manageable
        return text[:2000]
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

def extract_date_from_html(html_file):
    """Extract date from HTML file using schema:dateCreated"""
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Look for span with property="schema:dateCreated"
        date_span = soup.find('span', {'property': 'schema:dateCreated'})
        if date_span and date_span.get('content'):
            # Extract ISO 8601 date: 2022-06-04T23:37:23+00:00
            date_str = date_span.get('content')
            # Return just the date part (YYYY-MM-DD) for sorting
            return date_str.split('T')[0] if 'T' in date_str else date_str
        
        return None
    except Exception:
        return None

def main():
    articles_dir = Path('articles')
    articles = []
    
    if not articles_dir.exists():
        print(f"Error: {articles_dir} directory not found")
        return
    
    print("Scanning HTML files...")
    html_files = sorted(articles_dir.glob('*.html'))
    
    # Filter out pagination/index files
    def should_include_file(filename):
        """Filter out pagination and index files"""
        name = filename.name
        # Exclude files with ?page= in the name (pagination)
        if '?page=' in name:
            return False
        # Exclude index.html files
        if name == 'index.html':
            return False
        # Exclude node, activity, tracker files (these are index pages)
        if name in ['node.html', 'activity.html', 'tracker.html']:
            return False
        return True
    
    html_files = [f for f in html_files if should_include_file(f)]
    
    for html_file in html_files:
        title = extract_title_from_html(html_file)
        content = extract_text_from_html(html_file)
        date = extract_date_from_html(html_file)
        path = f"articles/{html_file.name}"
        
        articles.append({
            'title': title,
            'content': content,
            'path': path,
            'date': date or ''  # Use empty string if no date found
        })
        
        if len(articles) % 100 == 0:
            print(f"  Processed {len(articles)}/{len(html_files)} files...")
    
    # Save articles index (compact JSON for smaller file size)
    with open('articles-index.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, separators=(',', ':'), ensure_ascii=False)
    
    print(f"✓ Generated articles-index.json with {len(articles)} articles")
    
    # Pre-build Lunr index for faster client-side loading
    print("Building Lunr search index...")
    idx = lunr(
        ref='id',
        fields=[
            {'field_name': 'title', 'boost': 10},
            {'field_name': 'content'}
        ],
        documents=[
            {
                'id': str(i),
                'title': article['title'],
                'content': article['content']
            }
            for i, article in enumerate(articles)
        ]
    )
    
    # Serialize and save the index
    index_serialized = idx.serialize()
    with open('lunr-index.json', 'w', encoding='utf-8') as f:
        json.dump(index_serialized, f, separators=(',', ':'), ensure_ascii=False)
    
    print(f"✓ Generated pre-built lunr-index.json")
    print(f"\nTotal size: articles-index.json + lunr-index.json")

if __name__ == '__main__':
    main()

