#!/usr/bin/env python3
"""
Database Manager for SEO Affiliate Content Site
Handles all database operations including keywords, content, and performance tracking.
"""

import sqlite3
import asyncio
import aiosqlite
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path
import json
from loguru import logger

from config.settings import settings

class DatabaseManager:
    """Manages all database operations for the SEO affiliate site."""

    def __init__(self):
        self.db_path = settings.get_database_path()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize the database with required tables."""
        async with aiosqlite.connect(self.db_path) as db:
            await self._create_tables(db)
            await db.commit()

        logger.info("Database initialized successfully")

    async def _create_tables(self, db: aiosqlite.Connection):
        """Create all required database tables."""

        # Keywords table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE NOT NULL,
                search_volume INTEGER,
                keyword_difficulty INTEGER,
                competition_level TEXT,
                search_intent TEXT,
                category TEXT,
                target_audience TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_at TIMESTAMP NULL
            )
        """)

        # Content table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword_id INTEGER,
                title TEXT NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                meta_description TEXT,
                word_count INTEGER,
                affiliate_links_count INTEGER,
                internal_links_count INTEGER,
                status TEXT DEFAULT 'draft',
                published_at TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (keyword_id) REFERENCES keywords (id)
            )
        """)

        # SERP tracking table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS serp_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword_id INTEGER,
                url TEXT NOT NULL,
                position INTEGER,
                clicks INTEGER DEFAULT 0,
                impressions INTEGER DEFAULT 0,
                ctr REAL DEFAULT 0.0,
                tracked_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (keyword_id) REFERENCES keywords (id)
            )
        """)

        # Affiliate performance table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS affiliate_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id INTEGER,
                affiliate_tool TEXT NOT NULL,
                affiliate_url TEXT NOT NULL,
                clicks INTEGER DEFAULT 0,
                conversions INTEGER DEFAULT 0,
                revenue REAL DEFAULT 0.0,
                tracked_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content (id)
            )
        """)

        # Site analytics table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS site_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_url TEXT NOT NULL,
                page_views INTEGER DEFAULT 0,
                unique_visitors INTEGER DEFAULT 0,
                bounce_rate REAL DEFAULT 0.0,
                avg_time_on_page INTEGER DEFAULT 0,
                tracked_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Email subscribers table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS email_subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                source_page TEXT,
                lead_magnet TEXT,
                status TEXT DEFAULT 'active',
                subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                unsubscribed_at TIMESTAMP NULL
            )
        """)

        # Social media posts table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS social_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id INTEGER,
                platform TEXT NOT NULL,
                post_content TEXT NOT NULL,
                post_url TEXT,
                engagement_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'scheduled',
                scheduled_at TIMESTAMP,
                posted_at TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content (id)
            )
        """)

        # Create indexes for better performance
        await db.execute("CREATE INDEX IF NOT EXISTS idx_keywords_status ON keywords(status)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_keywords_category ON keywords(category)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_content_status ON content(status)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_serp_tracking_date ON serp_tracking(tracked_date)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_affiliate_performance_date ON affiliate_performance(tracked_date)")

    # Keyword operations
    async def add_keywords(self, keywords: List[Dict[str, Any]]) -> int:
        """Add multiple keywords to the database."""
        async with aiosqlite.connect(self.db_path) as db:
            added_count = 0

            for keyword_data in keywords:
                try:
                    await db.execute("""
                        INSERT OR IGNORE INTO keywords
                        (keyword, search_volume, keyword_difficulty, competition_level,
                         search_intent, category, target_audience)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        keyword_data['keyword'],
                        keyword_data.get('search_volume', 0),
                        keyword_data.get('keyword_difficulty', 0),
                        keyword_data.get('competition_level', 'unknown'),
                        keyword_data.get('search_intent', 'informational'),
                        keyword_data.get('category', 'general'),
                        keyword_data.get('target_audience', 'general')
                    ))

                    if db.total_changes > 0:
                        added_count += 1

                except Exception as e:
                    logger.error(f"Error adding keyword {keyword_data.get('keyword', 'unknown')}: {e}")

            await db.commit()
            logger.info(f"Added {added_count} new keywords to database")
            return added_count

    async def get_pending_keywords(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get pending keywords for content generation."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            cursor = await db.execute("""
                SELECT * FROM keywords
                WHERE status = 'pending'
                ORDER BY search_volume DESC, created_at ASC
                LIMIT ?
            """, (limit,))

            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def mark_keyword_used(self, keyword: str) -> bool:
        """Mark a keyword as used."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE keywords
                SET status = 'used', used_at = CURRENT_TIMESTAMP
                WHERE keyword = ?
            """, (keyword,))

            await db.commit()
            return db.total_changes > 0

    # Content operations
    async def save_content(self, content_data: Dict[str, Any]) -> int:
        """Save generated content to the database."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO content
                (keyword_id, title, slug, content, meta_description, word_count,
                 affiliate_links_count, internal_links_count, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                content_data.get('keyword_id'),
                content_data['title'],
                content_data['slug'],
                content_data['content'],
                content_data.get('meta_description', ''),
                content_data.get('word_count', 0),
                content_data.get('affiliate_links_count', 0),
                content_data.get('internal_links_count', 0),
                content_data.get('status', 'draft')
            ))

            content_id = cursor.lastrowid
            await db.commit()

            logger.info(f"Saved content: {content_data['title']} (ID: {content_id})")
            return content_id

    async def get_published_content(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get published content for performance tracking."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            cursor = await db.execute("""
                SELECT c.*, k.keyword
                FROM content c
                LEFT JOIN keywords k ON c.keyword_id = k.id
                WHERE c.status = 'published'
                ORDER BY c.published_at DESC
                LIMIT ?
            """, (limit,))

            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    # Performance tracking operations
    async def save_serp_data(self, serp_data: List[Dict[str, Any]]) -> int:
        """Save SERP tracking data."""
        async with aiosqlite.connect(self.db_path) as db:
            saved_count = 0

            for data in serp_data:
                try:
                    await db.execute("""
                        INSERT OR REPLACE INTO serp_tracking
                        (keyword_id, url, position, clicks, impressions, ctr, tracked_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        data['keyword_id'],
                        data['url'],
                        data['position'],
                        data.get('clicks', 0),
                        data.get('impressions', 0),
                        data.get('ctr', 0.0),
                        data['tracked_date']
                    ))
                    saved_count += 1

                except Exception as e:
                    logger.error(f"Error saving SERP data: {e}")

            await db.commit()
            return saved_count

    async def get_performance_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get performance summary for the last N days."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            since_date = (datetime.now() - timedelta(days=days)).date()

            # Get SERP performance
            cursor = await db.execute("""
                SELECT
                    COUNT(DISTINCT keyword_id) as total_keywords,
                    AVG(position) as avg_position,
                    SUM(clicks) as total_clicks,
                    SUM(impressions) as total_impressions,
                    AVG(ctr) as avg_ctr
                FROM serp_tracking
                WHERE tracked_date >= ?
            """, (since_date,))

            serp_data = dict(await cursor.fetchone())

            # Get content stats
            cursor = await db.execute("""
                SELECT
                    COUNT(*) as total_content,
                    COUNT(CASE WHEN status = 'published' THEN 1 END) as published_content,
                    AVG(word_count) as avg_word_count,
                    AVG(affiliate_links_count) as avg_affiliate_links
                FROM content
                WHERE created_at >= ?
            """, (since_date,))

            content_data = dict(await cursor.fetchone())

            return {
                'serp_performance': serp_data,
                'content_stats': content_data,
                'period_days': days
            }

    # Affiliate performance operations
    async def save_affiliate_performance(self, performance_data: List[Dict[str, Any]]) -> int:
        """Save affiliate performance data."""
        async with aiosqlite.connect(self.db_path) as db:
            saved_count = 0

            for data in performance_data:
                try:
                    await db.execute("""
                        INSERT OR REPLACE INTO affiliate_performance
                        (content_id, affiliate_tool, affiliate_url, clicks, conversions, revenue, tracked_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        data['content_id'],
                        data['affiliate_tool'],
                        data['affiliate_url'],
                        data.get('clicks', 0),
                        data.get('conversions', 0),
                        data.get('revenue', 0.0),
                        data['tracked_date']
                    ))
                    saved_count += 1

                except Exception as e:
                    logger.error(f"Error saving affiliate performance data: {e}")

            await db.commit()
            return saved_count

    # Email subscriber operations
    async def add_email_subscriber(self, email: str, source_page: str = None, lead_magnet: str = None) -> bool:
        """Add a new email subscriber."""
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("""
                    INSERT OR IGNORE INTO email_subscribers
                    (email, source_page, lead_magnet)
                    VALUES (?, ?, ?)
                """, (email, source_page, lead_magnet))

                await db.commit()
                return db.total_changes > 0

            except Exception as e:
                logger.error(f"Error adding email subscriber {email}: {e}")
                return False

    async def get_subscriber_count(self) -> int:
        """Get total number of active subscribers."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT COUNT(*) FROM email_subscribers
                WHERE status = 'active'
            """)

            result = await cursor.fetchone()
            return result[0] if result else 0

    # Social media operations
    async def save_social_post(self, post_data: Dict[str, Any]) -> int:
        """Save social media post data."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO social_posts
                (content_id, platform, post_content, post_url, status, scheduled_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                post_data.get('content_id'),
                post_data['platform'],
                post_data['post_content'],
                post_data.get('post_url'),
                post_data.get('status', 'scheduled'),
                post_data.get('scheduled_at')
            ))

            post_id = cursor.lastrowid
            await db.commit()
            return post_id

    # Analytics operations
    async def save_analytics_data(self, analytics_data: List[Dict[str, Any]]) -> int:
        """Save site analytics data."""
        async with aiosqlite.connect(self.db_path) as db:
            saved_count = 0

            for data in analytics_data:
                try:
                    await db.execute("""
                        INSERT OR REPLACE INTO site_analytics
                        (page_url, page_views, unique_visitors, bounce_rate, avg_time_on_page, tracked_date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        data['page_url'],
                        data.get('page_views', 0),
                        data.get('unique_visitors', 0),
                        data.get('bounce_rate', 0.0),
                        data.get('avg_time_on_page', 0),
                        data['tracked_date']
                    ))
                    saved_count += 1

                except Exception as e:
                    logger.error(f"Error saving analytics data: {e}")

            await db.commit()
            return saved_count

    # Utility operations
    async def backup_database(self, backup_path: Path = None) -> bool:
        """Create a backup of the database."""
        if not backup_path:
            backup_path = settings.DATA_DIR / "backups" / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

        backup_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            async with aiosqlite.connect(self.db_path) as source:
                async with aiosqlite.connect(backup_path) as backup:
                    await source.backup(backup)

            logger.info(f"Database backed up to: {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            return False

    async def get_database_stats(self) -> Dict[str, int]:
        """Get database statistics."""
        async with aiosqlite.connect(self.db_path) as db:
            stats = {}

            tables = ['keywords', 'content', 'serp_tracking', 'affiliate_performance',
                     'site_analytics', 'email_subscribers', 'social_posts']

            for table in tables:
                cursor = await db.execute(f"SELECT COUNT(*) FROM {table}")
                result = await cursor.fetchone()
                stats[table] = result[0] if result else 0

            return stats
