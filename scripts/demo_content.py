#!/usr/bin/env python3
"""
Demo Content Generator
Creates sample content to test the affiliate system without OpenAI.
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.affiliate_system.link_injector import AffiliateInjector
from src.site_management.hugo_manager import HugoManager

# Sample blog post content
SAMPLE_CONTENT = """
# Best CRM Tools for Small Business in 2024

Running a small business means wearing many hats, and managing customer relationships is one of the most important ones. The right CRM (Customer Relationship Management) tool can transform how you interact with customers, track sales, and grow your business.

## Why Small Businesses Need CRM Tools

Customer relationship management isn't just for large corporations. Small businesses actually benefit more from CRM tools because:

- **Better Organization**: Keep all customer information in one place
- **Improved Follow-up**: Never miss a sales opportunity again
- **Sales Automation**: Automate repetitive tasks to focus on growth
- **Data Insights**: Understand your customers better with analytics

## Top CRM Solutions for Small Businesses

### 1. HubSpot CRM

HubSpot offers one of the most comprehensive free CRM solutions available. It's perfect for small businesses just starting with customer relationship management.

**Key Features:**
- Free forever plan with essential features
- Contact management and deal tracking
- Email marketing integration
- Sales pipeline visualization

**Best For:** Startups and small businesses looking for a free, full-featured solution.

### 2. Salesforce Essentials

Salesforce is the world's leading CRM platform, and their Essentials plan is designed specifically for small businesses.

**Key Features:**
- Contact and account management
- Opportunity tracking
- Mobile app for on-the-go access
- Integration with popular business tools

**Best For:** Growing businesses that need enterprise-level features at a small business price.

## Email Marketing Integration

Many small businesses also need email marketing capabilities alongside their CRM. Tools like ConvertKit specialize in email marketing for creators and small businesses, offering:

- Automated email sequences
- Subscriber segmentation
- Landing page creation
- Integration with popular CRM systems

## Project Management Considerations

As your business grows, you'll also need project management tools to keep everything organized. Popular options include:

- **Asana**: Great for team collaboration and task management
- **Monday.com**: Visual project management with customizable workflows
- **Trello**: Simple, card-based project organization

## Design and Marketing Tools

Don't forget about design tools for creating marketing materials:

- **Canva**: Easy-to-use design platform for non-designers
- **Figma**: Professional design tool for more advanced users

## Automation and Workflow

To really scale your business, consider automation tools like:

- **Zapier**: Connect different apps and automate workflows
- **Make**: Visual automation platform for complex processes

## Conclusion

Choosing the right CRM tool is crucial for small business success. Start with a free option like HubSpot to understand your needs, then consider upgrading as your business grows.

The key is to choose a tool that grows with your business and integrates well with your other essential business tools for email marketing, project management, and automation.

Remember: the best CRM is the one your team will actually use consistently.
"""

async def demo_affiliate_injection():
    """Demonstrate affiliate link injection."""
    print("🎯 Demo: Affiliate Link Injection System")
    print("=" * 50)
    
    # Create sample content data
    content_data = {
        'keyword': 'best crm for small business',
        'title': 'Best CRM Tools for Small Business in 2024',
        'slug': 'best-crm-tools-small-business-2024',
        'meta_description': 'Discover the best CRM tools for small businesses in 2024. Compare features, pricing, and find the perfect customer relationship management solution.',
        'content': SAMPLE_CONTENT,
        'category': 'crm_tools',
        'search_intent': 'commercial',
        'word_count': len(SAMPLE_CONTENT.split()),
        'created_at': datetime.now().isoformat(),
        'status': 'draft'
    }
    
    print(f"📝 Original content: {content_data['word_count']} words")
    
    # Initialize affiliate injector
    injector = AffiliateInjector()
    
    # Inject affiliate links
    updated_content = await injector.inject_links(content_data)
    
    print(f"🔗 After affiliate injection: {updated_content['affiliate_links_count']} affiliate links added")
    
    # Show the difference
    print("\n📊 Affiliate Link Report:")
    report = injector.generate_link_report(updated_content['content'])
    print(f"   Link Density: {report['link_density']:.3f} (Target: {report['target_density']:.3f})")
    print(f"   Status: {report['density_status']}")
    print(f"   Tools Mentioned: {', '.join(report['mentioned_tools'])}")
    
    # Save to Hugo site
    print("\n💾 Saving to Hugo site...")
    hugo_manager = HugoManager()
    await hugo_manager.initialize()
    
    success = await hugo_manager.save_post(updated_content)
    if success:
        print("✅ Content saved to Hugo site successfully!")
        print(f"   File: hugo_site/content/posts/{updated_content['slug']}.md")
    else:
        print("❌ Failed to save content")
    
    return updated_content

async def demo_site_stats():
    """Show Hugo site statistics."""
    print("\n📊 Hugo Site Statistics:")
    
    hugo_manager = HugoManager()
    stats = await hugo_manager.get_site_stats()
    
    print(f"   Total Posts: {stats['total_posts']}")
    print(f"   Published: {stats['published_posts']}")
    print(f"   Drafts: {stats['draft_posts']}")

async def main():
    """Run the demo."""
    print("🚀 SEO Affiliate Content Site - Demo")
    print("Testing affiliate link injection and Hugo site management")
    print("=" * 60)
    
    try:
        # Demo affiliate injection
        content = await demo_affiliate_injection()
        
        # Show site stats
        await demo_site_stats()
        
        print("\n" + "=" * 60)
        print("🎉 Demo completed successfully!")
        print("\n📁 Check your generated content:")
        print(f"   File: SEO_Affiliate_Site/hugo_site/content/posts/{content['slug']}.md")
        print("\n🚀 Next steps:")
        print("   1. Add OpenAI billing to generate AI content")
        print("   2. Get SerpAPI key for keyword research")
        print("   3. Install Hugo for site building")
        print("   4. Set up Netlify for deployment")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
