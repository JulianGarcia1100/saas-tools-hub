#!/usr/bin/env python3
"""
Google API Test Script
Tests Google Custom Search API functionality.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_custom_search():
    """Test Google Custom Search API."""
    print("🔧 Testing Google Custom Search API...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")
    
    if not api_key or api_key == "your_google_api_key_here":
        print("❌ Google API key not configured")
        return False
    
    if not search_engine_id or search_engine_id == "your_search_engine_id_here":
        print("❌ Google Custom Search Engine ID not configured")
        return False
    
    try:
        # Test search
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': 'best CRM software',
            'num': 3
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'items' in data:
                print(f"✅ Google Custom Search API working!")
                print(f"   Found {len(data['items'])} results for 'best CRM software'")
                
                for i, item in enumerate(data['items'][:2], 1):
                    print(f"   {i}. {item['title']}")
                    print(f"      {item['link']}")
                
                return True
            else:
                print("❌ No search results returned")
                return False
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Google API error: {e}")
        return False

def test_google_autocomplete():
    """Test Google Autocomplete (alternative method)."""
    print("\n🔧 Testing Google Autocomplete (backup method)...")
    
    try:
        # This doesn't require API key - uses public endpoint
        url = "http://suggestqueries.google.com/complete/search"
        params = {
            'client': 'firefox',
            'q': 'best crm for'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # Try to parse the response
            text = response.text
            if 'best crm for' in text.lower():
                print("✅ Google Autocomplete working!")
                print("   This can be used as backup for keyword suggestions")
                return True
            else:
                print("❌ Unexpected response format")
                return False
        else:
            print(f"❌ Autocomplete request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Autocomplete error: {e}")
        return False

def main():
    """Run Google API tests."""
    print("🎯 Google API Configuration Test")
    print("=" * 40)
    
    # Test Custom Search API
    custom_search_ok = test_google_custom_search()
    
    # Test Autocomplete as backup
    autocomplete_ok = test_google_autocomplete()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"   Custom Search API: {'✅ PASS' if custom_search_ok else '❌ FAIL'}")
    print(f"   Autocomplete API: {'✅ PASS' if autocomplete_ok else '❌ FAIL'}")
    
    if custom_search_ok:
        print("\n🎉 Google API setup complete!")
        print("   Your system can now perform keyword research")
    elif autocomplete_ok:
        print("\n⚠️  Custom Search API not working, but Autocomplete is available")
        print("   You can still do basic keyword research")
    else:
        print("\n❌ Google API setup needs attention")
        print("   Please check your API key and Search Engine ID")
    
    print("\n📋 Setup Summary:")
    print("   1. ✅ Go to: https://console.cloud.google.com/apis/library")
    print("   2. ✅ Enable 'Custom Search API'")
    print("   3. ✅ Create API credentials")
    print("   4. ✅ Create Custom Search Engine: https://programmablesearchengine.google.com/")
    print("   5. ✅ Update .env file with API key and Search Engine ID")

if __name__ == "__main__":
    main()
