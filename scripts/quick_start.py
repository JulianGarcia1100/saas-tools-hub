#!/usr/bin/env python3
"""
SEO Affiliate Content Site - Quick Start Script
Automated setup and first content generation.
"""

import asyncio
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
import subprocess

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

console = Console()

async def main():
    """Quick start setup and demo."""
    
    console.print(Panel.fit(
        "🎯 SEO Affiliate Content Site - Quick Start",
        style="bold blue"
    ))
    
    console.print("\n🚀 Welcome to the SEO Affiliate Content Site!")
    console.print("This script will help you get started with automated content generation.\n")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        console.print("❌ No .env file found!", style="red")
        console.print("Please copy .env.example to .env and configure your API keys.")
        
        if Confirm.ask("Would you like me to create a basic .env file for you?"):
            create_env_file()
            console.print("✅ Created .env file. Please edit it with your API keys before continuing.")
        
        return
    
    # Check dependencies
    console.print("📦 Checking dependencies...")
    if not check_dependencies():
        console.print("❌ Missing dependencies. Please run: pip install -r requirements.txt")
        return
    
    # Check Hugo installation
    console.print("🔧 Checking Hugo installation...")
    if not check_hugo():
        console.print("❌ Hugo not found. Please install Hugo: https://gohugo.io/installation/")
        return
    
    console.print("✅ All dependencies check passed!\n")
    
    # Import after dependency check
    try:
        from main import SEOAffiliateApp
    except ImportError as e:
        console.print(f"❌ Import error: {e}")
        console.print("Please ensure all dependencies are installed.")
        return
    
    # Initialize app
    app = SEOAffiliateApp()
    
    console.print("🔧 Initializing application...")
    if not await app.initialize():
        console.print("❌ Failed to initialize application. Check your API keys in .env file.")
        return
    
    console.print("✅ Application initialized successfully!\n")
    
    # Quick demo
    if Confirm.ask("Would you like to run a quick demo? (Generate 3 keywords and 1 piece of content)"):
        await run_demo(app)
    
    # Show next steps
    show_next_steps()

def create_env_file():
    """Create a basic .env file from the example."""
    try:
        example_file = Path(".env.example")
        env_file = Path(".env")
        
        if example_file.exists():
            content = example_file.read_text()
            env_file.write_text(content)
        else:
            # Create minimal .env file
            minimal_env = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Google APIs
GOOGLE_API_KEY=your_google_api_key_here
SERPAPI_KEY=your_serpapi_key_here

# Site Configuration
SITE_URL=https://your-site.netlify.app
SITE_NAME=SaaS Tools Hub
SITE_DESCRIPTION=Discover the best SaaS tools for your business

# Content Generation Settings
CONTENT_GENERATION_ENABLED=true
POSTS_PER_WEEK=10
MIN_WORD_COUNT=800
MAX_WORD_COUNT=2000
"""
            env_file.write_text(minimal_env)
        
    except Exception as e:
        console.print(f"Error creating .env file: {e}")

def check_dependencies():
    """Check if required Python packages are installed."""
    required_packages = [
        'openai', 'aiohttp', 'pyyaml', 'rich', 'click', 
        'loguru', 'aiosqlite', 'frontmatter', 'textstat'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        console.print(f"Missing packages: {', '.join(missing_packages)}")
        return False
    
    return True

def check_hugo():
    """Check if Hugo is installed."""
    try:
        result = subprocess.run(['hugo', 'version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

async def run_demo(app):
    """Run a quick demo of the system."""
    console.print("\n🎯 Running Quick Demo...\n")
    
    try:
        # Discover keywords
        console.print("🔍 Discovering keywords...")
        keywords = await app.discover_keywords(3)
        
        if keywords:
            console.print(f"✅ Discovered {len(keywords)} keywords:")
            for kw in keywords:
                console.print(f"  • {kw['keyword']} (Volume: {kw.get('search_volume', 'N/A')})")
        
        # Generate content
        if keywords:
            console.print("\n✍️  Generating content...")
            content = await app.generate_content(1, keywords[:1])
            
            if content:
                console.print(f"✅ Generated content: {content[0]['title']}")
                console.print(f"   Word count: {content[0]['word_count']}")
                console.print(f"   Affiliate links: {content[0].get('affiliate_links_count', 0)}")
        
        console.print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        console.print(f"❌ Demo failed: {e}")

def show_next_steps():
    """Show next steps to the user."""
    console.print("\n" + "="*60)
    console.print("🎯 Next Steps:", style="bold green")
    console.print()
    console.print("1. 📝 Configure your .env file with API keys:")
    console.print("   • OpenAI API key for content generation")
    console.print("   • Google API key for keyword research")
    console.print("   • SerpAPI key for competition analysis")
    console.print()
    console.print("2. 🚀 Generate your first batch of content:")
    console.print("   python main.py full-run --keywords 20 --content 5")
    console.print()
    console.print("3. 🌐 Deploy your site:")
    console.print("   python main.py deploy")
    console.print()
    console.print("4. 📊 Start monitoring performance:")
    console.print("   python main.py track")
    console.print()
    console.print("5. 🤖 Enable automation:")
    console.print("   python main.py automate")
    console.print()
    console.print("📚 For detailed documentation, see: docs/README.md")
    console.print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
