#!/usr/bin/env python3
"""
Test Keyword Research System
Tests keyword discovery with current API setup.
"""

import sys
import asyncio
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.keyword_research.keyword_discovery import KeywordDiscovery

async def test_keyword_discovery():
    """Test keyword discovery system."""
    print("🎯 Testing Keyword Discovery System")
    print("=" * 50)
    
    try:
        # Initialize keyword discovery
        async with KeywordDiscovery() as keyword_discovery:
            print("🔍 Discovering keywords...")
            
            # Test with a small number first
            keywords = await keyword_discovery.discover_keywords(count=10)
            
            if keywords:
                print(f"✅ Successfully discovered {len(keywords)} keywords!")
                print("\n📋 Sample Keywords Found:")
                
                for i, keyword_data in enumerate(keywords[:5], 1):
                    print(f"   {i}. {keyword_data['keyword']}")
                    print(f"      Category: {keyword_data.get('category', 'N/A')}")
                    print(f"      Intent: {keyword_data.get('search_intent', 'N/A')}")
                    print(f"      Source: {keyword_data.get('source', 'N/A')}")
                    print()
                
                if len(keywords) > 5:
                    print(f"   ... and {len(keywords) - 5} more keywords")
                
                return True
            else:
                print("❌ No keywords discovered")
                return False
                
    except Exception as e:
        print(f"❌ Keyword discovery error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_pattern_generation():
    """Test pattern-based keyword generation."""
    print("\n🎯 Testing Pattern-Based Keyword Generation")
    print("=" * 50)
    
    try:
        keyword_discovery = KeywordDiscovery()
        
        # Test pattern generation (doesn't require API)
        pattern_keywords = await keyword_discovery._generate_pattern_keywords(5)
        
        if pattern_keywords:
            print(f"✅ Generated {len(pattern_keywords)} pattern-based keywords!")
            print("\n📋 Pattern Keywords:")
            
            for i, keyword_data in enumerate(pattern_keywords, 1):
                print(f"   {i}. {keyword_data['keyword']}")
                print(f"      Category: {keyword_data.get('category', 'N/A')}")
                print(f"      Audience: {keyword_data.get('target_audience', 'N/A')}")
                print()
            
            return True
        else:
            print("❌ No pattern keywords generated")
            return False
            
    except Exception as e:
        print(f"❌ Pattern generation error: {e}")
        return False

async def main():
    """Run keyword research tests."""
    print("🚀 SEO Affiliate Site - Keyword Research Test")
    print("Testing keyword discovery capabilities")
    print("=" * 60)
    
    # Test pattern generation (works without APIs)
    pattern_ok = await test_pattern_generation()
    
    # Test full keyword discovery (uses Google Autocomplete)
    discovery_ok = await test_keyword_discovery()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"   Pattern Generation: {'✅ PASS' if pattern_ok else '❌ FAIL'}")
    print(f"   Keyword Discovery: {'✅ PASS' if discovery_ok else '❌ FAIL'}")
    
    if pattern_ok and discovery_ok:
        print("\n🎉 Keyword research system is working!")
        print("\n🚀 Ready for content generation:")
        print("   1. Add OpenAI billing")
        print("   2. Run: python main.py full-run --keywords 10 --content 2")
        print("   3. Watch AI generate SEO content automatically!")
    elif pattern_ok:
        print("\n⚠️  Pattern generation working, API discovery needs attention")
        print("   You can still generate content with pattern-based keywords")
    else:
        print("\n❌ Keyword research needs troubleshooting")

if __name__ == "__main__":
    asyncio.run(main())
