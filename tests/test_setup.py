#!/usr/bin/env python3
"""
Quick Setup Test Script
Tests basic functionality with your API keys.
"""

import sys
import asyncio
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    import openai
    from dotenv import load_dotenv
    import os
    print("✅ Core imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Load environment variables
load_dotenv()

async def test_openai():
    """Test OpenAI API connection."""
    print("\n🔧 Testing OpenAI API...")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ OpenAI API key not configured")
        return False

    try:
        client = openai.AsyncOpenAI(api_key=api_key)

        # Test with a simple completion
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello from your SEO Affiliate Content Site!' in exactly those words."}
            ],
            max_tokens=50
        )

        result = response.choices[0].message.content.strip()
        print(f"✅ OpenAI API working! Response: {result}")
        return True

    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("\n🔧 Testing configuration...")

    try:
        from config.settings import settings
        print(f"✅ Settings loaded")
        print(f"   Site Name: {settings.SITE_NAME}")
        print(f"   Site URL: {settings.SITE_URL}")
        print(f"   Min Word Count: {settings.MIN_WORD_COUNT}")
        print(f"   Posts Per Week: {settings.POSTS_PER_WEEK}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_affiliate_config():
    """Test affiliate configuration."""
    print("\n🔧 Testing affiliate configuration...")

    try:
        import yaml
        config_path = Path("config/affiliate_links.yaml")

        with open(config_path, 'r', encoding='utf-8') as f:
            affiliate_data = yaml.safe_load(f)

        tools_count = len([k for k in affiliate_data.keys() if k != 'default_ctas'])
        print(f"✅ Affiliate config loaded: {tools_count} tools configured")

        # Show a few tools
        sample_tools = list(affiliate_data.keys())[:3]
        for tool in sample_tools:
            if tool != 'default_ctas':
                tool_data = affiliate_data[tool]
                print(f"   • {tool_data.get('name', tool)}: {tool_data.get('category', 'N/A')}")

        return True
    except Exception as e:
        print(f"❌ Affiliate config error: {e}")
        return False

async def test_database():
    """Test database initialization."""
    print("\n🔧 Testing database...")

    try:
        from src.database.db_manager import DatabaseManager

        db_manager = DatabaseManager()
        await db_manager.initialize()

        stats = await db_manager.get_database_stats()
        print(f"✅ Database initialized successfully")
        print(f"   Tables created: {len(stats)}")

        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

async def main():
    """Run all tests."""
    print("🎯 SEO Affiliate Content Site - Setup Test")
    print("=" * 50)

    tests = [
        ("Configuration", test_config),
        ("Affiliate Config", test_affiliate_config),
        ("Database", test_database),
        ("OpenAI API", test_openai),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 50)
    print("📊 Test Results:")

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1

    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("\n🎉 All tests passed! Your system is ready.")
        print("\n🚀 Next steps:")
        print("   1. Get SerpAPI key for keyword research")
        print("   2. Run: python main.py full-run --keywords 5 --content 1")
        print("   3. Check generated content in hugo_site/content/posts/")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
