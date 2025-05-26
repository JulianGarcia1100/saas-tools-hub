#!/usr/bin/env python3
"""
Analytics Testing Script
Tests if Google Analytics is properly integrated and tracking.
"""

import requests
import time

def test_analytics_integration():
    """Test if analytics code is properly integrated."""
    print("🔍 Testing Google Analytics Integration")
    print("=" * 50)
    
    base_url = "https://imaginative-madeleine-0e6883.netlify.app"
    
    # Test pages for analytics code
    test_pages = [
        "/",
        "/posts/",
        "/posts/best-project-management-tools-for-small-teams/",
        "/posts/best-crm-tools-small-business-2024/"
    ]
    
    analytics_found = 0
    affiliate_tracking_found = 0
    
    for page in test_pages:
        url = base_url + page
        try:
            print(f"🔍 Testing: {page or 'Homepage'}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # Check for GA4 tracking code
                has_gtag = 'gtag(' in html
                has_ga_id = 'G-GVJF9RWZE9' in html
                has_affiliate_tracking = 'affiliate_click' in html
                has_email_tracking = 'email_signup_attempt' in html
                has_scroll_tracking = 'scroll_depth' in html
                
                print(f"   ✅ Page loads: OK")
                print(f"   📊 GA4 Code: {'✅' if has_gtag else '❌'}")
                print(f"   🏷️ GA4 ID: {'✅' if has_ga_id else '❌'}")
                print(f"   🔗 Affiliate Tracking: {'✅' if has_affiliate_tracking else '❌'}")
                print(f"   📧 Email Tracking: {'✅' if has_email_tracking else '❌'}")
                print(f"   📊 Scroll Tracking: {'✅' if has_scroll_tracking else '❌'}")
                
                if has_gtag and has_ga_id:
                    analytics_found += 1
                if has_affiliate_tracking:
                    affiliate_tracking_found += 1
                    
            else:
                print(f"   ❌ Page error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        time.sleep(0.5)
    
    # Summary
    print("=" * 50)
    print("📊 Analytics Integration Summary:")
    print(f"   Pages with GA4: {analytics_found}/{len(test_pages)}")
    print(f"   Pages with Affiliate Tracking: {affiliate_tracking_found}/{len(test_pages)}")
    
    if analytics_found == len(test_pages):
        print("\n🎉 Google Analytics fully integrated!")
        return True
    else:
        print(f"\n⚠️  Analytics missing on {len(test_pages) - analytics_found} pages")
        return False

def show_analytics_dashboard_guide():
    """Show how to access analytics data."""
    print("\n📊 How to View Your Analytics Data:")
    print("=" * 50)
    
    print("🔍 Real-Time Testing (Immediate):")
    print("   1. Go to: https://analytics.google.com/")
    print("   2. Select your property: 'SaaS Tools Hub'")
    print("   3. Click 'Realtime' in left sidebar")
    print("   4. Visit your site in another tab")
    print("   5. Watch real-time visitor data appear!")
    
    print("\n📈 Key Reports to Monitor:")
    print("   • Realtime → Overview (live visitors)")
    print("   • Reports → Engagement → Events (affiliate clicks)")
    print("   • Reports → Acquisition → Traffic acquisition (traffic sources)")
    print("   • Reports → Engagement → Pages and screens (popular content)")
    
    print("\n🎯 Custom Events to Track:")
    print("   • affiliate_click - Every affiliate link click")
    print("   • high_value_affiliate_click - Premium tool clicks")
    print("   • email_signup_attempt - Lead capture attempts")
    print("   • scroll_depth - User engagement levels")
    print("   • high_engagement - Users who scroll 75%+")
    
    print("\n💰 Revenue Insights:")
    print("   • Which blog posts generate most affiliate clicks")
    print("   • Which tools are most popular with your audience")
    print("   • User journey from discovery to conversion")
    print("   • Content performance and optimization opportunities")

def show_conversion_setup():
    """Show how to set up conversions in GA4."""
    print("\n🎯 Setting Up Conversions in GA4:")
    print("=" * 50)
    
    conversions = [
        {
            'name': 'Affiliate Click',
            'event': 'affiliate_click',
            'description': 'User clicks affiliate link',
            'value': 'Track all affiliate engagement'
        },
        {
            'name': 'High Value Click', 
            'event': 'high_value_affiliate_click',
            'description': 'Click on premium tools (HubSpot, Salesforce)',
            'value': 'Track high-revenue potential clicks'
        },
        {
            'name': 'Email Signup',
            'event': 'email_signup_attempt',
            'description': 'User attempts email signup',
            'value': 'Track lead generation'
        },
        {
            'name': 'High Engagement',
            'event': 'high_engagement', 
            'description': 'User scrolls 75%+ of page',
            'value': 'Track content engagement'
        }
    ]
    
    print("📋 Steps to set up conversions:")
    print("   1. Go to GA4 → Admin → Events")
    print("   2. Click 'Create event' for each event below")
    print("   3. Mark as 'Conversion' in the toggle")
    print()
    
    for i, conv in enumerate(conversions, 1):
        print(f"{i}. {conv['name']}")
        print(f"   Event name: {conv['event']}")
        print(f"   Purpose: {conv['value']}")
        print()

def main():
    """Main testing function."""
    print("🎯 Google Analytics Testing & Setup Guide")
    print("Testing your deployed site for analytics integration")
    print("=" * 70)
    
    # Test analytics integration
    success = test_analytics_integration()
    
    if success:
        print("🎉 Analytics integration successful!")
        show_analytics_dashboard_guide()
        show_conversion_setup()
        
        print("\n" + "=" * 70)
        print("🚀 Next Steps:")
        print("   1. ✅ Redeploy to Netlify (if not done)")
        print("   2. 🔍 Test real-time tracking in GA4")
        print("   3. 🎯 Set up conversion events")
        print("   4. 📊 Monitor affiliate click performance")
        print("   5. 📈 Generate more content to scale tracking")
        
    else:
        print("⚠️  Please redeploy to Netlify first, then run this test again")

if __name__ == "__main__":
    main()
