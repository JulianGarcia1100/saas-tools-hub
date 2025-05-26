#!/usr/bin/env python3
"""
Test Fixed Site
Tests the site after applying 404 fixes.
"""

import requests
import time

def test_navigation_links():
    """Test the specific navigation that was failing."""
    base_url = "https://imaginative-madeleine-0e6883.netlify.app"
    
    print("🔧 Testing Fixed Navigation Links")
    print("=" * 50)
    
    # Test the problematic URLs
    test_urls = [
        f"{base_url}/",  # Homepage
        f"{base_url}/posts/",  # Posts index (was failing)
        f"{base_url}/posts/best-project-management-tools-for-small-teams/",  # Individual post
        f"{base_url}/categories/",  # Categories
        f"{base_url}/tags/",  # Tags
    ]
    
    for url in test_urls:
        try:
            print(f"🔍 Testing: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ SUCCESS: {response.status_code}")
                
                # Check if it's actually the right content
                if "/posts/" in url and url.endswith("/posts/"):
                    if "Posts" in response.text or "blog" in response.text.lower():
                        print("   📝 Posts page content detected")
                    else:
                        print("   ⚠️  Might be redirected to wrong page")
                        
            else:
                print(f"❌ FAILED: {response.status_code}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        time.sleep(1)  # Be nice to the server
    
    print("\n" + "=" * 50)
    print("🎯 Navigation Test Complete")
    print("\nIf all tests show ✅ SUCCESS, your site is fixed!")
    print("If any show ❌ FAILED, you may need to wait a few minutes for Netlify to update.")

def test_specific_post_links():
    """Test direct links to blog posts."""
    base_url = "https://imaginative-madeleine-0e6883.netlify.app"
    
    print("\n📝 Testing Individual Blog Posts")
    print("=" * 50)
    
    posts = [
        "best-project-management-tools-for-small-teams",
        "best-crm-tools-small-business-2024", 
        "top-free-design-tools-for-designers-2023",
        "how-to-choose-analytics-tools-for-coaches"
    ]
    
    for post in posts:
        url = f"{base_url}/posts/{post}/"
        try:
            print(f"🔍 Testing: {post}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ SUCCESS: Post accessible")
                
                # Check for affiliate links
                affiliate_count = response.text.count('affiliate-cta')
                print(f"   🔗 Affiliate CTAs found: {affiliate_count}")
                
            else:
                print(f"❌ FAILED: {response.status_code}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    print("🎯 Testing Fixed SEO Affiliate Site")
    print("Checking if 404 errors are resolved")
    print("=" * 60)
    
    print("⏳ Note: If you just redeployed, wait 1-2 minutes for changes to take effect")
    print()
    
    test_navigation_links()
    test_specific_post_links()
    
    print("\n" + "=" * 60)
    print("🎉 Testing Complete!")
    print("\n🌐 Your site: https://imaginative-madeleine-0e6883.netlify.app/")
    print("\n📋 What was fixed:")
    print("   ✅ Added _redirects file for Netlify routing")
    print("   ✅ Fixed baseURL in Hugo config")
    print("   ✅ Added custom 404 page")
    print("   ✅ Proper URL structure for all pages")
