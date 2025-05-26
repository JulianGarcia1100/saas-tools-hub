#!/usr/bin/env python3
"""
Add AI-focused keywords to the database for content generation.
"""

import asyncio
import sqlite3
from pathlib import Path

async def add_ai_keywords():
    """Add AI-focused keywords to the database."""

    # AI-focused high-converting keywords
    ai_keywords = [
        {
            'keyword': 'best ai tools for small business automation 2024',
            'search_volume': 2400,
            'keyword_difficulty': 65,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'ai_tools',
            'target_audience': 'small_business'
        },
        {
            'keyword': 'ai-powered crm software comparison for startups',
            'search_volume': 1800,
            'keyword_difficulty': 60,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'crm_tools',
            'target_audience': 'startups'
        },
        {
            'keyword': 'top artificial intelligence project management tools',
            'search_volume': 1600,
            'keyword_difficulty': 58,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'project_management',
            'target_audience': 'business_teams'
        },
        {
            'keyword': 'ai email marketing automation platforms for agencies',
            'search_volume': 1200,
            'keyword_difficulty': 55,
            'competition_level': 'low',
            'search_intent': 'commercial',
            'category': 'email_marketing',
            'target_audience': 'agencies'
        },
        {
            'keyword': 'best ai analytics tools for data-driven decisions',
            'search_volume': 1400,
            'keyword_difficulty': 62,
            'competition_level': 'medium',
            'search_intent': 'commercial',
            'category': 'analytics_tools',
            'target_audience': 'data_analysts'
        }
    ]

    # Connect to database
    db_path = Path('data/seo_affiliate.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert AI keywords
    for keyword_data in ai_keywords:
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

    print(f"\n🎉 Added {len(ai_keywords)} AI-focused keywords to database!")

if __name__ == "__main__":
    asyncio.run(add_ai_keywords())
