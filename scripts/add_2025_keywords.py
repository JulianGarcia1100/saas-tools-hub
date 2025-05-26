#!/usr/bin/env python3
"""
Add 2025 seasonal keywords and comparison keywords to the database.
"""

import asyncio
import sqlite3
from pathlib import Path

async def add_2025_keywords():
    """Add 2025 seasonal and comparison keywords to the database."""
    
    # 2025 Seasonal + Comparison Keywords (High Commercial Intent)
    seasonal_keywords = [
        {
            'keyword': 'best saas tools for small business 2025',
            'search_volume': 3200,
            'keyword_difficulty': 68,
            'competition_level': 'high',
            'search_intent': 'commercial',
            'category': 'seasonal_roundup',
            'target_audience': 'small_business'
        },
        {
            'keyword': 'top ai productivity tools 2025',
            'search_volume': 2800,
            'keyword_difficulty': 65,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'ai_tools',
            'target_audience': 'professionals'
        },
        {
            'keyword': 'hubspot vs salesforce 2025 comparison',
            'search_volume': 2400,
            'keyword_difficulty': 72,
            'competition_level': 'high',
            'search_intent': 'commercial',
            'category': 'tool_comparison',
            'target_audience': 'business_owners'
        },
        {
            'keyword': 'best project management software 2025',
            'search_volume': 2600,
            'keyword_difficulty': 70,
            'competition_level': 'high',
            'search_intent': 'commercial',
            'category': 'project_management',
            'target_audience': 'teams'
        },
        {
            'keyword': 'asana vs monday vs clickup comparison',
            'search_volume': 1800,
            'keyword_difficulty': 64,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'tool_comparison',
            'target_audience': 'project_managers'
        },
        {
            'keyword': 'top email marketing platforms 2025',
            'search_volume': 2200,
            'keyword_difficulty': 66,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'email_marketing',
            'target_audience': 'marketers'
        },
        {
            'keyword': 'convertkit vs mailchimp vs constant contact',
            'search_volume': 1600,
            'keyword_difficulty': 62,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'tool_comparison',
            'target_audience': 'email_marketers'
        },
        {
            'keyword': 'best ai writing tools for content creators 2025',
            'search_volume': 2000,
            'keyword_difficulty': 58,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'ai_tools',
            'target_audience': 'content_creators'
        },
        {
            'keyword': 'canva vs adobe creative suite vs figma',
            'search_volume': 1400,
            'keyword_difficulty': 60,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'tool_comparison',
            'target_audience': 'designers'
        },
        {
            'keyword': 'top business automation tools 2025',
            'search_volume': 1800,
            'keyword_difficulty': 63,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'automation_tools',
            'target_audience': 'entrepreneurs'
        }
    ]
    
    # Connect to database
    db_path = Path('data/seo_affiliate.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insert 2025 keywords
    for keyword_data in seasonal_keywords:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO keywords 
                (keyword, search_volume, keyword_difficulty, competition_level, search_intent, category, target_audience)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                keyword_data['keyword'],
                keyword_data['search_volume'],
                keyword_data['keyword_difficulty'],
                keyword_data['competition_level'],
                keyword_data['search_intent'],
                keyword_data['category'],
                keyword_data['target_audience']
            ))
            print(f"✅ Added: {keyword_data['keyword']}")
        except Exception as e:
            print(f"❌ Error adding {keyword_data['keyword']}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Added {len(seasonal_keywords)} 2025 seasonal keywords to database!")
    print("\n📊 Keyword Categories Added:")
    categories = {}
    for kw in seasonal_keywords:
        cat = kw['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for category, count in categories.items():
        print(f"   • {category}: {count} keywords")

if __name__ == "__main__":
    asyncio.run(add_2025_keywords())
