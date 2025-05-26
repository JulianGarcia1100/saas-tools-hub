#!/usr/bin/env python3
"""
SEO Affiliate Content Site - Main Application
Automated SEO content generation and affiliate marketing system.
"""

import click
import sys
import asyncio
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from loguru import logger

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from config.settings import settings
from src.database.db_manager import DatabaseManager
from src.keyword_research.keyword_discovery import KeywordDiscovery
from src.content_generation.content_generator import ContentGenerator
from src.site_management.hugo_manager import HugoManager
from src.affiliate_system.link_injector import AffiliateInjector
from src.performance_tracking.serp_tracker import SerpTracker
from src.automation.scheduler import AutomationScheduler

console = Console()

class SEOAffiliateApp:
    """Main application class for the SEO Affiliate Content Site."""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.keyword_discovery = KeywordDiscovery()
        self.content_generator = ContentGenerator()
        self.hugo_manager = HugoManager()
        self.affiliate_injector = AffiliateInjector()
        self.serp_tracker = SerpTracker()
        self.scheduler = AutomationScheduler()
        
        # Configure logging
        logger.add(
            settings.DATA_DIR / "logs" / "app.log",
            rotation="1 day",
            retention="30 days",
            level="INFO"
        )
    
    async def initialize(self):
        """Initialize the application and all components."""
        console.print(Panel.fit("🚀 Initializing SEO Affiliate Content Site", style="bold blue"))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Initialize database
            task1 = progress.add_task("Setting up database...", total=None)
            await self.db_manager.initialize()
            progress.update(task1, completed=True)
            
            # Initialize Hugo site
            task2 = progress.add_task("Setting up Hugo site...", total=None)
            await self.hugo_manager.initialize()
            progress.update(task2, completed=True)
            
            # Validate API keys
            task3 = progress.add_task("Validating API configurations...", total=None)
            missing_config = settings.validate_config()
            if missing_config:
                console.print(f"❌ Missing configuration: {', '.join(missing_config)}", style="red")
                return False
            progress.update(task3, completed=True)
            
            console.print("✅ Application initialized successfully!", style="green")
            return True
    
    async def discover_keywords(self, count: int = 50):
        """Discover new keywords for content generation."""
        console.print(f"🔍 Discovering {count} new keywords...")
        
        keywords = await self.keyword_discovery.discover_keywords(count)
        
        if keywords:
            console.print(f"✅ Discovered {len(keywords)} new keywords")
            for keyword in keywords[:10]:  # Show first 10
                console.print(f"  • {keyword['keyword']} (Volume: {keyword['search_volume']})")
            
            if len(keywords) > 10:
                console.print(f"  ... and {len(keywords) - 10} more")
        else:
            console.print("❌ No new keywords discovered", style="red")
        
        return keywords
    
    async def generate_content(self, count: int = 10, keywords: Optional[list] = None):
        """Generate SEO-optimized content."""
        console.print(f"✍️  Generating {count} pieces of content...")
        
        if not keywords:
            # Get keywords from database
            keywords = await self.db_manager.get_pending_keywords(count)
        
        if not keywords:
            console.print("❌ No keywords available for content generation", style="red")
            return []
        
        generated_content = []
        
        with Progress(console=console) as progress:
            task = progress.add_task("Generating content...", total=count)
            
            for i, keyword_data in enumerate(keywords[:count]):
                try:
                    # Generate content
                    content = await self.content_generator.generate_post(keyword_data)
                    
                    if content:
                        # Inject affiliate links
                        content_with_links = await self.affiliate_injector.inject_links(content)
                        
                        # Save to Hugo site
                        await self.hugo_manager.save_post(content_with_links)
                        
                        generated_content.append(content_with_links)
                        
                        # Update database
                        await self.db_manager.mark_keyword_used(keyword_data['keyword'])
                        
                        console.print(f"✅ Generated: {content['title']}")
                    
                    progress.update(task, advance=1)
                    
                except Exception as e:
                    logger.error(f"Error generating content for {keyword_data['keyword']}: {e}")
                    console.print(f"❌ Failed to generate content for: {keyword_data['keyword']}", style="red")
                    progress.update(task, advance=1)
        
        console.print(f"✅ Generated {len(generated_content)} pieces of content")
        return generated_content
    
    async def deploy_site(self):
        """Deploy the Hugo site to Netlify."""
        console.print("🚀 Deploying site to Netlify...")
        
        try:
            # Build Hugo site
            await self.hugo_manager.build_site()
            
            # Deploy to Netlify
            deployment_url = await self.hugo_manager.deploy_to_netlify()
            
            if deployment_url:
                console.print(f"✅ Site deployed successfully: {deployment_url}", style="green")
                return deployment_url
            else:
                console.print("❌ Deployment failed", style="red")
                return None
                
        except Exception as e:
            logger.error(f"Deployment error: {e}")
            console.print(f"❌ Deployment error: {e}", style="red")
            return None
    
    async def track_performance(self):
        """Track SERP performance and analytics."""
        console.print("📊 Tracking performance...")
        
        try:
            # Update SERP rankings
            await self.serp_tracker.update_rankings()
            
            # Generate performance report
            report = await self.serp_tracker.generate_report()
            
            console.print("✅ Performance tracking completed")
            console.print(f"📈 Total tracked keywords: {report['total_keywords']}")
            console.print(f"🎯 Average position: {report['average_position']:.1f}")
            console.print(f"📊 Total clicks: {report['total_clicks']}")
            
            return report
            
        except Exception as e:
            logger.error(f"Performance tracking error: {e}")
            console.print(f"❌ Performance tracking error: {e}", style="red")
            return None
    
    async def start_automation(self):
        """Start the automated content generation and monitoring."""
        console.print("🤖 Starting automation scheduler...")
        
        try:
            await self.scheduler.start()
            console.print("✅ Automation started successfully", style="green")
            
        except Exception as e:
            logger.error(f"Automation error: {e}")
            console.print(f"❌ Automation error: {e}", style="red")
    
    async def stop_automation(self):
        """Stop the automation scheduler."""
        console.print("⏹️  Stopping automation...")
        
        try:
            await self.scheduler.stop()
            console.print("✅ Automation stopped", style="green")
            
        except Exception as e:
            logger.error(f"Error stopping automation: {e}")
            console.print(f"❌ Error stopping automation: {e}", style="red")


@click.group()
def cli():
    """SEO Affiliate Content Site - Automated content generation and affiliate marketing."""
    pass

@cli.command()
@click.option('--count', default=50, help='Number of keywords to discover')
async def discover(count):
    """Discover new keywords for content generation."""
    app = SEOAffiliateApp()
    await app.initialize()
    await app.discover_keywords(count)

@cli.command()
@click.option('--count', default=10, help='Number of content pieces to generate')
async def generate(count):
    """Generate SEO-optimized content."""
    app = SEOAffiliateApp()
    await app.initialize()
    await app.generate_content(count)

@cli.command()
async def deploy():
    """Deploy the site to Netlify."""
    app = SEOAffiliateApp()
    await app.initialize()
    await app.deploy_site()

@cli.command()
async def track():
    """Track SERP performance and analytics."""
    app = SEOAffiliateApp()
    await app.initialize()
    await app.track_performance()

@cli.command()
async def automate():
    """Start automated content generation and monitoring."""
    app = SEOAffiliateApp()
    await app.initialize()
    await app.start_automation()

@cli.command()
@click.option('--keywords', default=10, help='Number of keywords to discover')
@click.option('--content', default=5, help='Number of content pieces to generate')
async def full_run(keywords, content):
    """Run the complete workflow: discover keywords, generate content, and deploy."""
    app = SEOAffiliateApp()
    
    if not await app.initialize():
        return
    
    # Discover keywords
    discovered_keywords = await app.discover_keywords(keywords)
    
    if discovered_keywords:
        # Generate content
        generated_content = await app.generate_content(content, discovered_keywords)
        
        if generated_content:
            # Deploy site
            await app.deploy_site()
            
            # Track performance
            await app.track_performance()

if __name__ == '__main__':
    # Handle async commands
    import inspect
    
    def async_command(f):
        def wrapper(*args, **kwargs):
            if inspect.iscoroutinefunction(f):
                return asyncio.run(f(*args, **kwargs))
            return f(*args, **kwargs)
        return wrapper
    
    # Apply async wrapper to all commands
    for command in cli.commands.values():
        if hasattr(command, 'callback'):
            command.callback = async_command(command.callback)
    
    cli()
