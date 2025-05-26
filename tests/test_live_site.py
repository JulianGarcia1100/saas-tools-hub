#!/usr/bin/env python3
"""
Live Site Testing Script
Tests your deployed Netlify site for functionality and SEO.
"""

import requests
from urllib.parse import urljoin
import time

def test_live_site(base_url):
    """Test the live site functionality."""
    print(f"🌐 Testing Live Site: {base_url}")
    print("=" * 60)
    
    # Test pages to check
    test_pages = [
        "",  # Homepage
        "posts/",  # Blog index
        "posts/best-project-management-tools-for-small-teams/",
        "posts/best-crm-tools-small-business-2024/",
        "posts/top-free-design-tools-for-designers-2023/",
        "posts/how-to-choose-analytics-tools-for-coaches/",
        "sitemap.xml",
        "categories/",
        "tags/"
    ]
    
    results = []
    
    for page in test_pages:
        url = urljoin(base_url, page)
        try:
            print(f"🔍 Testing: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {page or 'Homepage'}: OK ({response.status_code})")
                
                # Check for affiliate links
                if 'posts/' in page and page != 'posts/':
                    affiliate_count = response.text.count('affiliate-cta')
                    link_count = response.text.count('target="_blank"')
                    print(f"   🔗 Affiliate CTAs: {affiliate_count}")
                    print(f"   🔗 External Links: {link_count}")
                
                # Check for SEO elements
                if '<title>' in response.text:
                    title_start = response.text.find('<title>') + 7
                    title_end = response.text.find('</title>')
                    title = response.text[title_start:title_end]
                    print(f"   📝 Title: {title[:50]}...")
                
                results.append((page, True, response.status_code))
            else:
                print(f"❌ {page or 'Homepage'}: Error ({response.status_code})")
                results.append((page, False, response.status_code))
                
        except Exception as e:
            print(f"❌ {page or 'Homepage'}: Failed - {e}")
            results.append((page, False, "Error"))
        
        time.sleep(0.5)  # Be nice to the server
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"   ✅ Passed: {passed}/{total} pages")
    print(f"   📈 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your site is working perfectly!")
        print("\n🚀 Next Steps:")
        print("   1. Submit to Google Search Console")
        print("   2. Set up Google Analytics")
        print("   3. Generate more content")
        print("   4. Monitor affiliate earnings")
    else:
        print(f"\n⚠️  {total-passed} pages need attention")
    
    return results

def check_seo_basics(base_url):
    """Check basic SEO elements."""
    print(f"\n🔍 SEO Analysis for: {base_url}")
    print("=" * 60)
    
    try:
        response = requests.get(base_url, timeout=10)
        html = response.text
        
        # Check meta tags
        has_title = '<title>' in html
        has_description = 'meta name="description"' in html
        has_og_tags = 'property="og:' in html
        has_twitter_tags = 'name="twitter:' in html
        has_canonical = 'rel="canonical"' in html
        
        print(f"📝 Title Tag: {'✅' if has_title else '❌'}")
        print(f"📝 Meta Description: {'✅' if has_description else '❌'}")
        print(f"📱 Open Graph Tags: {'✅' if has_og_tags else '❌'}")
        print(f"🐦 Twitter Cards: {'✅' if has_twitter_tags else '❌'}")
        print(f"🔗 Canonical URL: {'✅' if has_canonical else '❌'}")
        
        # Check for affiliate links
        affiliate_ctas = html.count('affiliate-cta')
        external_links = html.count('target="_blank"')
        
        print(f"💰 Affiliate CTAs: {affiliate_ctas}")
        print(f"🔗 External Links: {external_links}")
        
        seo_score = sum([has_title, has_description, has_og_tags, has_twitter_tags, has_canonical])
        print(f"\n📊 SEO Score: {seo_score}/5 ({(seo_score/5)*100:.0f}%)")
        
        if seo_score >= 4:
            print("🎉 Excellent SEO setup!")
        elif seo_score >= 3:
            print("✅ Good SEO setup")
        else:
            print("⚠️  SEO needs improvement")
            
    except Exception as e:
        print(f"❌ SEO check failed: {e}")

def main():
    """Main testing function."""
    print("🎯 Live Site Testing Tool")
    print("Testing your deployed Netlify site")
    print("=" * 70)
    
    # You'll need to update this with your actual Netlify URL
    base_url = "https://imaginative-madeleine-0e6883.netlify.app/"
    
    print(f"🌐 Target Site: {base_url}")
    print("📋 This will test:")
    print("   • Page accessibility")
    print("   • Affiliate link presence")
    print("   • SEO optimization")
    print("   • Site functionality")
    print()
    
    # Test site functionality
    results = test_live_site(base_url)
    
    # Check SEO basics
    check_seo_basics(base_url)
    
    print("\n" + "=" * 70)
    print("🎉 Testing Complete!")
    print(f"🌐 Your live site: {base_url}")

if __name__ == "__main__":
    main()
