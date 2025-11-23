# /// script
# dependencies = []
# ///
"""
Copy all article HTML files from backup directory to articles directory
"""
import os
import shutil
from pathlib import Path

def should_copy_file(filepath):
    """Determine if a file should be copied"""
    name = filepath.name
    
    # Exclude pagination/index files
    if '?page=' in name:
        return False
    if name == 'index.html':
        return False
    if name in ['node.html', 'activity.html', 'tracker.html', 'search.html']:
        return False
    
    # Include all other HTML files
    return True

def main():
    source_dir = Path('/media/me/storage_union/website-backups/tortillaconsal')
    target_dir = Path('articles')
    
    target_dir.mkdir(exist_ok=True)
    
    # Find all HTML files in source
    print("Scanning source directory...")
    html_files = list(source_dir.rglob('*.html'))
    
    # Filter files
    files_to_copy = [f for f in html_files if should_copy_file(f)]
    
    print(f"Found {len(files_to_copy)} HTML files to copy")
    
    copied = 0
    skipped = 0
    errors = 0
    
    for html_file in files_to_copy:
        try:
            target_file = target_dir / html_file.name
            
            # If file already exists, check if it's the same
            if target_file.exists():
                if target_file.stat().st_size == html_file.stat().st_size:
                    skipped += 1
                    continue
            
            shutil.copy2(html_file, target_file)
            copied += 1
            
            if copied % 100 == 0:
                print(f"  Copied {copied}/{len(files_to_copy)} files...")
                
        except Exception as e:
            print(f"Error copying {html_file}: {e}")
            errors += 1
    
    print(f"\n✓ Copied {copied} files")
    print(f"  Skipped {skipped} files (already exist)")
    print(f"  Errors: {errors}")
    print(f"  Total files in articles/: {len(list(target_dir.glob('*.html')))}")

if __name__ == '__main__':
    main()
