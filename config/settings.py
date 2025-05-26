#!/usr/bin/env python3
"""
SEO Affiliate Site - Configuration Settings
Centralized configuration management for the entire application.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Main configuration class for the SEO Affiliate Site."""
    
    # Project Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    TEMPLATES_DIR = PROJECT_ROOT / "templates"
    HUGO_SITE_DIR = PROJECT_ROOT / "hugo_site"
    CONTENT_DIR = HUGO_SITE_DIR / "content" / "posts"
    SCRIPTS_DIR = PROJECT_ROOT / "scripts"
    
    # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_SEARCH_CONSOLE_CREDENTIALS = os.getenv("GOOGLE_SEARCH_CONSOLE_CREDENTIALS")
    GOOGLE_ANALYTICS_PROPERTY_ID = os.getenv("GOOGLE_ANALYTICS_PROPERTY_ID")
    
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    
    HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
    HUBSPOT_PORTAL_ID = os.getenv("HUBSPOT_PORTAL_ID")
    
    # Social Media APIs
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
    
    BUFFER_ACCESS_TOKEN = os.getenv("BUFFER_ACCESS_TOKEN")
    
    # Site Configuration
    SITE_URL = os.getenv("SITE_URL", "https://your-site.netlify.app")
    SITE_NAME = os.getenv("SITE_NAME", "SaaS Tools Hub")
    SITE_DESCRIPTION = os.getenv("SITE_DESCRIPTION", "Discover the best SaaS tools for your business")
    
    # Deployment Configuration
    NETLIFY_AUTH_TOKEN = os.getenv("NETLIFY_AUTH_TOKEN")
    NETLIFY_SITE_ID = os.getenv("NETLIFY_SITE_ID")
    
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO = os.getenv("GITHUB_REPO")
    
    # Email Configuration
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    
    # Slack Notifications
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
    
    # Content Generation Settings
    CONTENT_GENERATION_ENABLED = os.getenv("CONTENT_GENERATION_ENABLED", "true").lower() == "true"
    POSTS_PER_WEEK = int(os.getenv("POSTS_PER_WEEK", "10"))
    MIN_WORD_COUNT = int(os.getenv("MIN_WORD_COUNT", "800"))
    MAX_WORD_COUNT = int(os.getenv("MAX_WORD_COUNT", "2000"))
    
    # Affiliate Settings
    AFFILIATE_LINK_DENSITY = float(os.getenv("AFFILIATE_LINK_DENSITY", "0.03"))
    CTA_VARIATIONS = int(os.getenv("CTA_VARIATIONS", "5"))
    TRACK_AFFILIATE_CLICKS = os.getenv("TRACK_AFFILIATE_CLICKS", "true").lower() == "true"
    
    # Performance Tracking
    SERP_TRACKING_ENABLED = os.getenv("SERP_TRACKING_ENABLED", "true").lower() == "true"
    ANALYTICS_TRACKING_ENABLED = os.getenv("ANALYTICS_TRACKING_ENABLED", "true").lower() == "true"
    DAILY_REPORTS_ENABLED = os.getenv("DAILY_REPORTS_ENABLED", "true").lower() == "true"
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/seo_affiliate.db")
    BACKUP_ENABLED = os.getenv("BACKUP_ENABLED", "true").lower() == "true"
    BACKUP_FREQUENCY = os.getenv("BACKUP_FREQUENCY", "weekly")
    
    # Content Categories
    CONTENT_CATEGORIES = [
        "CRM Tools",
        "Email Marketing",
        "Project Management",
        "Design Tools",
        "Analytics Tools",
        "Automation Tools",
        "Communication Tools",
        "Development Tools",
        "Marketing Tools",
        "Sales Tools"
    ]
    
    # SEO Configuration
    SEO_CONFIG = {
        "target_keyword_density": 0.015,  # 1.5%
        "min_headings": 3,
        "max_headings": 8,
        "meta_description_length": (150, 160),
        "title_length": (50, 60),
        "internal_links_per_post": (2, 5),
        "external_links_per_post": (3, 7)
    }
    
    # Content Templates
    CONTENT_TEMPLATES = {
        "comparison": "Compare {tool1} vs {tool2}: Which {category} tool is better for {audience}?",
        "review": "{tool} Review: Is this {category} tool worth it for {audience}?",
        "alternatives": "Best {tool} Alternatives for {audience} in 2024",
        "guide": "Complete Guide to {category} Tools for {audience}",
        "best_of": "Best {category} Tools for {audience} in 2024"
    }
    
    # Social Media Templates
    SOCIAL_TEMPLATES = {
        "twitter_thread": [
            "🧵 Thread: {title}",
            "1/ {hook}",
            "2/ {point1}",
            "3/ {point2}",
            "4/ {point3}",
            "5/ {conclusion}"
        ],
        "linkedin_post": "{hook}\n\n{main_points}\n\n{cta}\n\n#{hashtags}"
    }
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Validate configuration and return list of missing required settings."""
        missing = []
        
        required_settings = [
            "OPENAI_API_KEY",
            "GOOGLE_API_KEY",
            "SERPAPI_KEY"
        ]
        
        for setting in required_settings:
            if not getattr(cls, setting):
                missing.append(setting)
        
        return missing
    
    @classmethod
    def create_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            cls.DATA_DIR,
            cls.DATA_DIR / "backups",
            cls.CONTENT_DIR,
            cls.HUGO_SITE_DIR / "static" / "images",
            cls.TEMPLATES_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_database_path(cls) -> Path:
        """Get the database file path."""
        if cls.DATABASE_URL.startswith("sqlite:///"):
            db_path = cls.DATABASE_URL.replace("sqlite:///", "")
            return Path(db_path)
        return cls.DATA_DIR / "seo_affiliate.db"


# Create settings instance
settings = Settings()

# Validate configuration on import
missing_config = settings.validate_config()
if missing_config:
    print(f"⚠️  Missing required configuration: {', '.join(missing_config)}")
    print("Please check your .env file and ensure all required API keys are set.")

# Create necessary directories
settings.create_directories()
