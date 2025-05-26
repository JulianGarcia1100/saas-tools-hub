#!/usr/bin/env python3
"""
Database Initialization Script
Sets up the database with initial data and configurations.
"""

import asyncio
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.database.db_manager import DatabaseManager
from config.settings import settings

async def main():
    """Initialize the database with sample data."""
    print("🔧 Initializing SEO Affiliate Site Database...")
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Initialize database
    await db_manager.initialize()
    
    # Add sample keywords
    sample_keywords = [
        {
            'keyword': 'best crm for small business',
            'search_volume': 1200,
            'keyword_difficulty': 25,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'crm_tools',
            'target_audience': 'small businesses'
        },
        {
            'keyword': 'email marketing tools for freelancers',
            'search_volume': 800,
            'keyword_difficulty': 20,
            'competition_level': 'low',
            'search_intent': 'commercial',
            'category': 'email_marketing',
            'target_audience': 'freelancers'
        },
        {
            'keyword': 'project management software comparison',
            'search_volume': 950,
            'keyword_difficulty': 30,
            'competition_level': 'medium',
            'search_intent': 'informational',
            'category': 'project_management',
            'target_audience': 'general'
        },
        {
            'keyword': 'canva alternatives for designers',
            'search_volume': 600,
            'keyword_difficulty': 18,
            'competition_level': 'low',
            'search_intent': 'commercial',
            'category': 'design_tools',
            'target_audience': 'designers'
        },
        {
            'keyword': 'zapier vs make automation',
            'search_volume': 400,
            'keyword_difficulty': 22,
            'competition_level': 'low',
            'search_intent': 'commercial',
            'category': 'automation_tools',
            'target_audience': 'entrepreneurs'
        }
    ]
    
    # Add keywords to database
    added_count = await db_manager.add_keywords(sample_keywords)
    print(f"✅ Added {added_count} sample keywords to database")
    
    # Get database stats
    stats = await db_manager.get_database_stats()
    print(f"📊 Database Statistics:")
    for table, count in stats.items():
        print(f"   {table}: {count} records")
    
    print("🎉 Database initialization completed!")

if __name__ == "__main__":
    asyncio.run(main())
