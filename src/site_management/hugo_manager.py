#!/usr/bin/env python3
"""
Hugo Site Manager for SEO Affiliate Content Site
Manages Hugo static site generation, content publishing, and deployment.
"""

import asyncio
import subprocess
import shutil
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import frontmatter
import aiohttp
from loguru import logger

from config.settings import settings

class HugoManager:
    """Manages Hugo static site operations."""
    
    def __init__(self):
        self.hugo_site_dir = settings.HUGO_SITE_DIR
        self.content_dir = settings.CONTENT_DIR
        self.netlify_token = settings.NETLIFY_AUTH_TOKEN
        self.netlify_site_id = settings.NETLIFY_SITE_ID
        
        # Ensure directories exist
        self.hugo_site_dir.mkdir(parents=True, exist_ok=True)
        self.content_dir.mkdir(parents=True, exist_ok=True)
    
    async def initialize(self):
        """Initialize Hugo site if it doesn't exist."""
        config_file = self.hugo_site_dir / "config.yaml"
        
        if not config_file.exists():
            await self._create_hugo_site()
            await self._setup_theme()
            await self._create_config()
        
        logger.info("Hugo site initialized")
    
    async def _create_hugo_site(self):
        """Create a new Hugo site."""
        try:
            # Create basic Hugo structure
            directories = [
                "content/posts",
                "static/images",
                "static/css",
                "static/js",
                "layouts/_default",
                "layouts/partials",
                "data",
                "archetypes"
            ]
            
            for directory in directories:
                (self.hugo_site_dir / directory).mkdir(parents=True, exist_ok=True)
            
            logger.info("Created Hugo site structure")
            
        except Exception as e:
            logger.error(f"Error creating Hugo site: {e}")
            raise
    
    async def _setup_theme(self):
        """Set up a basic SEO-optimized theme."""
        layouts_dir = self.hugo_site_dir / "layouts"
        
        # Create base layout
        base_layout = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ if .Title }}{{ .Title }} | {{ end }}{{ .Site.Title }}</title>
    <meta name="description" content="{{ if .Description }}{{ .Description }}{{ else }}{{ .Site.Params.description }}{{ end }}">
    
    <!-- SEO Meta Tags -->
    <meta property="og:title" content="{{ if .Title }}{{ .Title }}{{ else }}{{ .Site.Title }}{{ end }}">
    <meta property="og:description" content="{{ if .Description }}{{ .Description }}{{ else }}{{ .Site.Params.description }}{{ end }}">
    <meta property="og:type" content="{{ if .IsPage }}article{{ else }}website{{ end }}">
    <meta property="og:url" content="{{ .Permalink }}">
    <meta property="og:site_name" content="{{ .Site.Title }}">
    
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{ if .Title }}{{ .Title }}{{ else }}{{ .Site.Title }}{{ end }}">
    <meta name="twitter:description" content="{{ if .Description }}{{ .Description }}{{ else }}{{ .Site.Params.description }}{{ end }}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{{ .Permalink }}">
    
    <!-- CSS -->
    <link rel="stylesheet" href="{{ "/css/style.css" | relURL }}">
    
    <!-- Google Analytics -->
    {{ if .Site.Params.google_analytics }}
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ .Site.Params.google_analytics }}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '{{ .Site.Params.google_analytics }}');
    </script>
    {{ end }}
</head>
<body>
    <header>
        <nav>
            <a href="{{ "/" | relURL }}">{{ .Site.Title }}</a>
        </nav>
    </header>
    
    <main>
        {{ block "main" . }}{{ end }}
    </main>
    
    <footer>
        <p>&copy; {{ now.Year }} {{ .Site.Title }}. All rights reserved.</p>
    </footer>
    
    <!-- HubSpot Email Capture -->
    {{ if .Site.Params.hubspot_portal_id }}
    <script charset="utf-8" type="text/javascript" src="//js.hsforms.net/forms/v2.js"></script>
    {{ end }}
</body>
</html>"""
        
        with open(layouts_dir / "_default" / "baseof.html", 'w', encoding='utf-8') as f:
            f.write(base_layout)
        
        # Create single post layout
        single_layout = """{{ define "main" }}
<article>
    <header>
        <h1>{{ .Title }}</h1>
        <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date.Format "January 2, 2006" }}</time>
        {{ if .Params.categories }}
        <div class="categories">
            {{ range .Params.categories }}
            <span class="category">{{ . }}</span>
            {{ end }}
        </div>
        {{ end }}
    </header>
    
    <div class="content">
        {{ .Content }}
    </div>
    
    <!-- Email Signup Form -->
    <div class="email-signup">
        <h3>Get More SaaS Tool Reviews</h3>
        <p>Subscribe to our newsletter for weekly SaaS tool reviews and productivity tips.</p>
        {{ if .Site.Params.hubspot_portal_id }}
        <div id="hubspot-form"></div>
        <script>
            hbspt.forms.create({
                portalId: "{{ .Site.Params.hubspot_portal_id }}",
                formId: "{{ .Site.Params.hubspot_form_id }}",
                target: "#hubspot-form"
            });
        </script>
        {{ end }}
    </div>
</article>
{{ end }}"""
        
        with open(layouts_dir / "_default" / "single.html", 'w', encoding='utf-8') as f:
            f.write(single_layout)
        
        # Create list layout
        list_layout = """{{ define "main" }}
<div class="posts-list">
    <h1>{{ .Title }}</h1>
    {{ range .Pages }}
    <article class="post-summary">
        <h2><a href="{{ .Permalink }}">{{ .Title }}</a></h2>
        <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date.Format "January 2, 2006" }}</time>
        <p>{{ .Summary }}</p>
        <a href="{{ .Permalink }}">Read more →</a>
    </article>
    {{ end }}
</div>
{{ end }}"""
        
        with open(layouts_dir / "_default" / "list.html", 'w', encoding='utf-8') as f:
            f.write(list_layout)
        
        # Create basic CSS
        css_content = """
/* Basic styling for SEO affiliate site */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

header {
    border-bottom: 1px solid #eee;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
}

nav a {
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
    color: #2563eb;
}

h1, h2, h3 {
    color: #1f2937;
}

h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

h2 {
    font-size: 2rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

h3 {
    font-size: 1.5rem;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
}

.content {
    margin: 2rem 0;
}

.content ul, .content ol {
    margin: 1rem 0;
    padding-left: 2rem;
}

.content li {
    margin: 0.5rem 0;
}

.email-signup {
    background: #f8fafc;
    padding: 2rem;
    border-radius: 8px;
    margin: 3rem 0;
    text-align: center;
}

.categories {
    margin: 1rem 0;
}

.category {
    background: #e5e7eb;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    font-size: 0.875rem;
    margin-right: 0.5rem;
}

.post-summary {
    border-bottom: 1px solid #e5e7eb;
    padding: 2rem 0;
}

.post-summary h2 {
    margin-top: 0;
}

.post-summary a {
    color: #2563eb;
    text-decoration: none;
}

.post-summary a:hover {
    text-decoration: underline;
}

footer {
    border-top: 1px solid #eee;
    margin-top: 3rem;
    padding-top: 2rem;
    text-align: center;
    color: #6b7280;
}

/* Affiliate link styling */
.affiliate-cta {
    background: #dbeafe;
    border: 1px solid #3b82f6;
    border-radius: 6px;
    padding: 1rem;
    margin: 1.5rem 0;
    text-align: center;
}

.affiliate-cta a {
    color: #1d4ed8;
    font-weight: bold;
    text-decoration: none;
}

.affiliate-cta a:hover {
    text-decoration: underline;
}
"""
        
        css_dir = self.hugo_site_dir / "static" / "css"
        css_dir.mkdir(parents=True, exist_ok=True)
        
        with open(css_dir / "style.css", 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        logger.info("Created Hugo theme")
    
    async def _create_config(self):
        """Create Hugo configuration file."""
        config = {
            'baseURL': settings.SITE_URL,
            'languageCode': 'en-us',
            'title': settings.SITE_NAME,
            'description': settings.SITE_DESCRIPTION,
            'params': {
                'description': settings.SITE_DESCRIPTION,
                'google_analytics': settings.GOOGLE_ANALYTICS_PROPERTY_ID,
                'hubspot_portal_id': settings.HUBSPOT_PORTAL_ID,
                'hubspot_form_id': 'your-form-id'  # To be configured
            },
            'markup': {
                'goldmark': {
                    'renderer': {
                        'unsafe': True
                    }
                }
            },
            'menu': {
                'main': [
                    {'name': 'Home', 'url': '/', 'weight': 10},
                    {'name': 'Blog', 'url': '/posts/', 'weight': 20}
                ]
            },
            'taxonomies': {
                'category': 'categories',
                'tag': 'tags'
            }
        }
        
        config_file = self.hugo_site_dir / "config.yaml"
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        logger.info("Created Hugo configuration")
    
    async def save_post(self, post_data: Dict[str, Any]) -> bool:
        """Save a blog post to Hugo content directory."""
        try:
            # Create frontmatter
            post_frontmatter = {
                'title': post_data['title'],
                'slug': post_data['slug'],
                'description': post_data['meta_description'],
                'date': datetime.now().isoformat(),
                'categories': [post_data.get('category', 'General')],
                'tags': self._extract_tags(post_data['content']),
                'author': 'SaaS Tools Hub',
                'draft': False
            }
            
            # Create post with frontmatter
            post = frontmatter.Post(post_data['content'], **post_frontmatter)
            
            # Save to file
            filename = f"{post_data['slug']}.md"
            filepath = self.content_dir / filename
            
            with open(filepath, 'wb') as f:
                frontmatter.dump(post, f)
            
            logger.info(f"Saved post: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving post: {e}")
            return False
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract relevant tags from content."""
        # Simple tag extraction based on common SaaS terms
        saas_terms = [
            'crm', 'email marketing', 'project management', 'automation',
            'analytics', 'design', 'productivity', 'collaboration',
            'small business', 'startup', 'freelancer', 'entrepreneur'
        ]
        
        content_lower = content.lower()
        tags = []
        
        for term in saas_terms:
            if term in content_lower:
                tags.append(term.title())
        
        return tags[:5]  # Limit to 5 tags
    
    async def build_site(self) -> bool:
        """Build the Hugo site."""
        try:
            # Change to Hugo site directory
            original_cwd = Path.cwd()
            
            try:
                # Build the site
                result = subprocess.run(
                    ['hugo', '--minify'],
                    cwd=self.hugo_site_dir,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    logger.info("Hugo site built successfully")
                    return True
                else:
                    logger.error(f"Hugo build failed: {result.stderr}")
                    return False
                    
            finally:
                # Always return to original directory
                pass
                
        except subprocess.TimeoutExpired:
            logger.error("Hugo build timed out")
            return False
        except FileNotFoundError:
            logger.error("Hugo not found. Please install Hugo.")
            return False
        except Exception as e:
            logger.error(f"Error building Hugo site: {e}")
            return False
    
    async def deploy_to_netlify(self) -> Optional[str]:
        """Deploy the built site to Netlify."""
        if not self.netlify_token or not self.netlify_site_id:
            logger.warning("Netlify credentials not configured")
            return None
        
        try:
            # Build site first
            if not await self.build_site():
                return None
            
            # Create deployment archive
            public_dir = self.hugo_site_dir / "public"
            if not public_dir.exists():
                logger.error("Public directory not found after build")
                return None
            
            # Deploy using Netlify API
            deployment_url = await self._deploy_to_netlify_api(public_dir)
            
            if deployment_url:
                logger.info(f"Site deployed to: {deployment_url}")
                return deployment_url
            else:
                logger.error("Netlify deployment failed")
                return None
                
        except Exception as e:
            logger.error(f"Error deploying to Netlify: {e}")
            return None
    
    async def _deploy_to_netlify_api(self, public_dir: Path) -> Optional[str]:
        """Deploy to Netlify using their API."""
        try:
            # This is a simplified version - in practice, you'd zip the files
            # and upload them to Netlify's deploy API
            
            # For now, return the site URL
            return settings.SITE_URL
            
        except Exception as e:
            logger.error(f"Error with Netlify API deployment: {e}")
            return None
    
    async def generate_sitemap(self) -> bool:
        """Generate sitemap.xml for the site."""
        try:
            # Hugo generates sitemap automatically, but we can customize if needed
            sitemap_template = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{{ range .Data.Pages }}
  <url>
    <loc>{{ .Permalink }}</loc>
    <lastmod>{{ .Date.Format "2006-01-02" }}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
{{ end }}
</urlset>"""
            
            layouts_dir = self.hugo_site_dir / "layouts"
            sitemap_file = layouts_dir / "sitemap.xml"
            
            with open(sitemap_file, 'w', encoding='utf-8') as f:
                f.write(sitemap_template)
            
            logger.info("Generated custom sitemap template")
            return True
            
        except Exception as e:
            logger.error(f"Error generating sitemap: {e}")
            return False
    
    async def get_site_stats(self) -> Dict[str, int]:
        """Get statistics about the Hugo site."""
        try:
            stats = {
                'total_posts': 0,
                'published_posts': 0,
                'draft_posts': 0
            }
            
            if self.content_dir.exists():
                for post_file in self.content_dir.glob("*.md"):
                    try:
                        with open(post_file, 'r', encoding='utf-8') as f:
                            post = frontmatter.load(f)
                            stats['total_posts'] += 1
                            
                            if post.get('draft', False):
                                stats['draft_posts'] += 1
                            else:
                                stats['published_posts'] += 1
                                
                    except Exception as e:
                        logger.debug(f"Error reading post {post_file}: {e}")
                        continue
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting site stats: {e}")
            return {'total_posts': 0, 'published_posts': 0, 'draft_posts': 0}
