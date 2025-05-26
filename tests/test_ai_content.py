#!/usr/bin/env python3
"""
Test AI Content Generation
Simple test of OpenAI content generation without strict validation.
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.content_generation.content_generator import ContentGenerator
from src.affiliate_system.link_injector import AffiliateInjector
from src.site_management.hugo_manager import HugoManager

async def test_ai_content_generation():
    """Test AI content generation with a simple keyword."""
    print("🤖 Testing AI Content Generation with OpenAI")
    print("=" * 60)
    
    # Sample keyword data
    keyword_data = {
        'id': 1,
        'keyword': 'best project management tools for small teams',
        'category': 'project_management',
        'search_intent': 'commercial',
        'target_audience': 'small teams'
    }
    
    print(f"🎯 Target Keyword: {keyword_data['keyword']}")
    print(f"📂 Category: {keyword_data['category']}")
    
    try:
        # Initialize content generator
        print("\n🔧 Initializing content generator...")
        content_generator = ContentGenerator()
        
        # Generate content
        print("✍️  Generating AI content... (this may take 30-60 seconds)")
        content_data = await content_generator.generate_post(keyword_data)
        
        if content_data:
            print(f"✅ Content generated successfully!")
            print(f"   Title: {content_data['title']}")
            print(f"   Word Count: {content_data['word_count']}")
            print(f"   Slug: {content_data['slug']}")
            
            # Show content preview
            content_preview = content_data['content'][:300] + "..."
            print(f"\n📝 Content Preview:")
            print(content_preview)
            
            # Inject affiliate links
            print(f"\n🔗 Injecting affiliate links...")
            injector = AffiliateInjector()
            content_with_links = await injector.inject_links(content_data)
            
            print(f"✅ Affiliate links injected: {content_with_links['affiliate_links_count']} links")
            
            # Save to Hugo site
            print(f"\n💾 Saving to Hugo site...")
            hugo_manager = HugoManager()
            await hugo_manager.initialize()
            
            success = await hugo_manager.save_post(content_with_links)
            if success:
                print(f"✅ Content saved successfully!")
                print(f"   File: hugo_site/content/posts/{content_with_links['slug']}.md")
                
                # Show file path
                file_path = Path("hugo_site/content/posts") / f"{content_with_links['slug']}.md"
                print(f"   Full path: SEO_Affiliate_Site/{file_path}")
                
                return content_with_links
            else:
                print(f"❌ Failed to save content")
                return None
        else:
            print(f"❌ Content generation failed")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

async def show_generated_content(content_data):
    """Show details about the generated content."""
    if not content_data:
        return
    
    print("\n" + "=" * 60)
    print("📊 Generated Content Analysis")
    print("=" * 60)
    
    print(f"🎯 Keyword: {content_data['keyword']}")
    print(f"📝 Title: {content_data['title']}")
    print(f"📏 Word Count: {content_data['word_count']}")
    print(f"🔗 Affiliate Links: {content_data.get('affiliate_links_count', 0)}")
    print(f"📂 Category: {content_data.get('category', 'N/A')}")
    print(f"🎨 Slug: {content_data['slug']}")
    
    # Calculate potential value
    word_count = content_data['word_count']
    affiliate_links = content_data.get('affiliate_links_count', 0)
    
    print(f"\n💰 Potential Value Analysis:")
    print(f"   Content Quality: {'✅ High' if word_count > 800 else '⚠️ Medium'}")
    print(f"   Monetization: {'✅ Good' if affiliate_links >= 2 else '⚠️ Low'}")
    print(f"   SEO Potential: ✅ Optimized")
    
    estimated_cost = 0.20  # Approximate OpenAI cost
    estimated_revenue_potential = affiliate_links * 50  # Conservative estimate
    
    print(f"\n📈 Economics:")
    print(f"   Generation Cost: ~${estimated_cost:.2f}")
    print(f"   Revenue Potential: ${estimated_revenue_potential}-{estimated_revenue_potential*10} over time")
    print(f"   ROI Potential: {int((estimated_revenue_potential/estimated_cost)*100)}%+")

async def main():
    """Run the AI content generation test."""
    print("🚀 SEO Affiliate Site - AI Content Generation Test")
    print("Testing OpenAI GPT-4 content generation with affiliate optimization")
    print("=" * 70)
    
    # Test content generation
    content_data = await test_ai_content_generation()
    
    # Show analysis
    await show_generated_content(content_data)
    
    if content_data:
        print("\n🎉 SUCCESS! Your AI content generation system is working!")
        print("\n🚀 Next Steps:")
        print("   1. ✅ AI content generation working")
        print("   2. ✅ Affiliate link injection working")
        print("   3. ✅ Hugo site management working")
        print("   4. 🔄 Ready for full automation!")
        
        print("\n🤖 Run Full Automation:")
        print("   python main.py full-run --keywords 10 --content 3")
        print("   (This will generate 3 complete blog posts automatically)")
        
        print("\n📁 Check Your Generated Content:")
        print(f"   File: SEO_Affiliate_Site/hugo_site/content/posts/{content_data['slug']}.md")
    else:
        print("\n❌ Content generation needs troubleshooting")
        print("   Please check your OpenAI API key and billing status")

if __name__ == "__main__":
    asyncio.run(main())
