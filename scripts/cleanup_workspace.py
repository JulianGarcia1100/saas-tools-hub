#!/usr/bin/env python3
"""
Workspace Cleanup Script
Organizes the SEO Affiliate Site project structure.
"""

import os
import shutil
from pathlib import Path

def cleanup_workspace():
    """Clean up and organize the workspace."""
    
    print("🧹 Cleaning up SEO Affiliate Site workspace...")
    
    # Create organized directory structure
    directories = {
        'scripts': 'Utility scripts and tools',
        'docs': 'Documentation and guides', 
        'tests': 'Test files and validation scripts',
        'tools': 'Development and maintenance tools',
        'backups': 'Backup files and archives'
    }
    
    # Create directories if they don't exist
    for dir_name, description in directories.items():
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir()
            print(f"✅ Created {dir_name}/ - {description}")
    
    # Move files to appropriate directories
    file_moves = {
        # Scripts
        'scripts/': [
            'add_ai_keywords.py',
            'check_db.py', 
            'demo_content.py',
            'quick_start.py',
            'setup_analytics.py',
            'setup_search_console.py',
            'cleanup_workspace.py'
        ],
        # Tests
        'tests/': [
            'test_ai_content.py',
            'test_analytics.py',
            'test_fixed_site.py',
            'test_full_system.py',
            'test_google_api.py',
            'test_keyword_research.py',
            'test_live_site.py',
            'test_setup.py',
            'generate_test_events.py'
        ],
        # Tools
        'tools/': [
            'install_hugo.bat',
            'install_hugo.ps1',
            'build_site.bat',
            '🎯_Launch_SEO_Site.bat'
        ],
        # Docs
        'docs/': [
            'affiliate_signup_guide.md'
        ]
    }
    
    # Move files
    for target_dir, files in file_moves.items():
        for file_name in files:
            source = Path(file_name)
            if source.exists():
                target = Path(target_dir) / file_name
                try:
                    shutil.move(str(source), str(target))
                    print(f"📁 Moved {file_name} → {target_dir}")
                except Exception as e:
                    print(f"❌ Error moving {file_name}: {e}")
    
    # Clean up temporary files
    temp_patterns = [
        '*.pyc',
        '__pycache__',
        '*.log',
        'sitemap-test.xml'
    ]
    
    print("\n🗑️ Removing temporary files...")
    
    # Remove __pycache__ directories
    for pycache in Path('.').rglob('__pycache__'):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            print(f"🗑️ Removed {pycache}")
    
    # Remove test sitemap
    test_sitemap = Path('hugo_site/static/sitemap-test.xml')
    if test_sitemap.exists():
        test_sitemap.unlink()
        print(f"🗑️ Removed {test_sitemap}")
    
    print("\n✅ Workspace cleanup complete!")
    print("\n📁 Organized Project Structure:")
    print("├── src/                    # Core application code")
    print("├── hugo_site/              # Hugo static site")
    print("├── scripts/                # Utility scripts")
    print("├── tests/                  # Test files")
    print("├── tools/                  # Development tools")
    print("├── docs/                   # Documentation")
    print("├── config/                 # Configuration files")
    print("├── data/                   # Database and logs")
    print("└── templates/              # Content templates")

if __name__ == "__main__":
    cleanup_workspace()
