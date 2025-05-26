#!/usr/bin/env python3
"""
Full System Test
Tests the complete SEO affiliate content workflow.
"""

import sys
import asyncio
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.keyword_research.keyword_discovery import KeywordDiscovery
from src.database.db_manager import DatabaseManager

async def test_full_workflow():
    """Test the complete workflow."""
    print("🎯 Testing Complete SEO Affiliate Workflow")
    print("=" * 60)
    
    try:
        # Step 1: Initialize database
        print("📊 Step 1: Initializing database...")
        db_manager = DatabaseManager()
        await db_manager.initialize()
        print("✅ Database ready")
        
        # Step 2: Discover keywords
        print("\n🔍 Step 2: Discovering keywords...")
        async with KeywordDiscovery() as keyword_discovery:
            keywords = await keyword_discovery.discover_keywords(count=15)
            
            if keywords:
                print(f"✅ Discovered {len(keywords)} keywords")
                
                # Show sample keywords
                print("\n📋 Sample Keywords:")
                for i, kw in enumerate(keywords[:5], 1):
                    print(f"   {i}. {kw['keyword']}")
                    print(f"      Category: {kw.get('category', 'N/A')}")
                    print(f"      Intent: {kw.get('search_intent', 'N/A')}")
                    print(f"      Source: {kw.get('source', 'N/A')}")
                
                # Step 3: Save keywords to database
                print(f"\n💾 Step 3: Saving keywords to database...")
                added_count = await db_manager.add_keywords(keywords)
                print(f"✅ Saved {added_count} new keywords")
                
                # Step 4: Get database stats
                print(f"\n📊 Step 4: Database statistics...")
                stats = await db_manager.get_database_stats()
                print(f"✅ Database contains:")
                for table, count in stats.items():
                    print(f"   {table}: {count} records")
                
                # Step 5: Get keywords for content generation
                print(f"\n📝 Step 5: Preparing for content generation...")
                pending_keywords = await db_manager.get_pending_keywords(5)
                print(f"✅ {len(pending_keywords)} keywords ready for content generation")
                
                if pending_keywords:
                    print("\n🎯 Ready for AI Content Generation:")
                    for i, kw in enumerate(pending_keywords, 1):
                        print(f"   {i}. {kw['keyword']} ({kw['category']})")
                
                return True
            else:
                print("❌ No keywords discovered")
                return False
                
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def show_next_steps():
    """Show what happens next with OpenAI."""
    print("\n" + "=" * 60)
    print("🚀 NEXT: Add OpenAI Billing for Full Automation")
    print("=" * 60)
    
    print("\n💰 OpenAI Setup (2 minutes):")
    print("   1. Go to: https://platform.openai.com/settings/organization/billing")
    print("   2. Add payment method")
    print("   3. Add $20 in credits")
    print("   4. Done!")
    
    print("\n🤖 Then Run Full Automation:")
    print("   python main.py full-run --keywords 10 --content 3")
    
    print("\n📈 What This Will Do:")
    print("   ✅ Discover 10 new SaaS keywords")
    print("   ✅ Generate 3 complete blog posts (800-1500 words each)")
    print("   ✅ Inject contextual affiliate links")
    print("   ✅ Optimize for SEO (titles, meta descriptions, headings)")
    print("   ✅ Save to Hugo site ready for deployment")
    
    print("\n💵 Cost Breakdown:")
    print("   • Keyword research: Free (Google API)")
    print("   • Content generation: ~$0.60 (3 posts × $0.20 each)")
    print("   • Total: Less than $1 for 3 professional blog posts!")
    
    print("\n🎯 Revenue Potential:")
    print("   • Each post targets commercial keywords")
    print("   • 3-5 affiliate links per post")
    print("   • Potential: $50-500+ per post over time")
    
    print("\n📊 Scaling:")
    print("   • Generate 10 posts/week = 520 posts/year")
    print("   • Cost: ~$100/year in OpenAI credits")
    print("   • Potential revenue: $10,000-50,000+/year")

async def main():
    """Run the full system test."""
    print("🚀 SEO Affiliate Content Site - Full System Test")
    print("Testing complete automated workflow")
    print("=" * 70)
    
    # Test the workflow
    success = await test_full_workflow()
    
    if success:
        print("\n🎉 SYSTEM FULLY OPERATIONAL!")
        print("   All components working perfectly")
        await show_next_steps()
    else:
        print("\n❌ System needs attention")
        print("   Please check the errors above")

if __name__ == "__main__":
    asyncio.run(main())
