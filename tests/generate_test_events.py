#!/usr/bin/env python3
"""
Generate Test Events
Simulates user behavior to generate analytics events for testing.
"""

import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def simulate_user_behavior():
    """Simulate realistic user behavior to generate analytics events."""
    
    print("🤖 Simulating User Behavior for Analytics Testing")
    print("=" * 60)
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Initialize Chrome driver
        print("🌐 Opening browser...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1200, 800)
        
        base_url = "https://imaginative-madeleine-0e6883.netlify.app"
        
        # Test sequence
        test_actions = [
            {
                'name': 'Homepage Visit',
                'url': base_url,
                'actions': ['scroll_slow', 'wait_3s']
            },
            {
                'name': 'Posts Page',
                'url': f"{base_url}/posts/",
                'actions': ['scroll_slow', 'wait_2s']
            },
            {
                'name': 'Project Management Post',
                'url': f"{base_url}/posts/best-project-management-tools-for-small-teams/",
                'actions': ['scroll_slow', 'click_affiliate', 'wait_5s']
            },
            {
                'name': 'CRM Tools Post', 
                'url': f"{base_url}/posts/best-crm-tools-small-business-2024/",
                'actions': ['scroll_slow', 'click_affiliate', 'wait_3s']
            }
        ]
        
        for i, test in enumerate(test_actions, 1):
            print(f"\n{i}. {test['name']}")
            print(f"   URL: {test['url']}")
            
            # Navigate to page
            driver.get(test['url'])
            time.sleep(2)
            
            # Execute actions
            for action in test['actions']:
                if action == 'scroll_slow':
                    print("   📜 Scrolling slowly...")
                    # Scroll in increments to trigger scroll depth events
                    for scroll_pos in [0.25, 0.5, 0.75, 1.0]:
                        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {scroll_pos});")
                        time.sleep(1)
                
                elif action == 'click_affiliate':
                    print("   🔗 Looking for affiliate links...")
                    try:
                        # Find affiliate links
                        affiliate_links = driver.find_elements(By.CSS_SELECTOR, ".affiliate-cta a")
                        if affiliate_links:
                            link = affiliate_links[0]
                            print(f"   🎯 Clicking: {link.text[:30]}...")
                            
                            # Scroll to link first
                            driver.execute_script("arguments[0].scrollIntoView(true);", link)
                            time.sleep(1)
                            
                            # Click the link (will open in new tab)
                            link.click()
                            time.sleep(2)
                            
                            # Close the new tab and return to original
                            if len(driver.window_handles) > 1:
                                driver.switch_to.window(driver.window_handles[-1])
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                        else:
                            print("   ⚠️  No affiliate links found")
                    except Exception as e:
                        print(f"   ❌ Error clicking affiliate link: {e}")
                
                elif action.startswith('wait_'):
                    wait_time = int(action.split('_')[1][0])
                    print(f"   ⏱️  Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
        
        print("\n✅ User behavior simulation completed!")
        print("📊 Check Google Analytics Real-time reports for events")
        
    except Exception as e:
        print(f"❌ Error during simulation: {e}")
        print("💡 Make sure Chrome browser is installed")
        
    finally:
        try:
            driver.quit()
        except:
            pass

def manual_testing_guide():
    """Provide manual testing instructions."""
    
    print("\n🎯 Manual Testing Guide")
    print("=" * 40)
    
    print("If automated testing doesn't work, do this manually:")
    print()
    print("1. 🌐 Open your site: https://imaginative-madeleine-0e6883.netlify.app/")
    print("2. 📊 Open GA4 Real-time: https://analytics.google.com/")
    print("3. 🔍 Navigate to: Realtime → Events")
    print()
    print("4. 🧪 Test these actions on your site:")
    print("   • Click 'Posts' in navigation")
    print("   • Click 'Read more' on any blog post")
    print("   • Scroll down slowly on a blog post")
    print("   • Click any 'Try [Tool] free' button")
    print("   • Scroll to bottom of post")
    print()
    print("5. 📈 Watch for these events in GA4:")
    print("   • page_view")
    print("   • scroll_depth")
    print("   • affiliate_click")
    print("   • high_engagement")
    print()
    print("6. ⏱️  Events may take 1-2 minutes to appear")

def check_events_in_ga4():
    """Instructions for checking events in GA4."""
    
    print("\n📊 Checking Events in GA4")
    print("=" * 40)
    
    print("After testing, check these locations in GA4:")
    print()
    print("🔍 Real-time Events:")
    print("   1. Go to: Realtime → Events")
    print("   2. Look for: affiliate_click, scroll_depth, high_engagement")
    print()
    print("📈 Historical Events:")
    print("   1. Go to: Reports → Engagement → Events")
    print("   2. Look for your custom events")
    print("   3. Click event name for details")
    print()
    print("🎯 Setting up Conversions:")
    print("   1. Find your events in the Events report")
    print("   2. Toggle 'Mark as conversion' for:")
    print("      • affiliate_click")
    print("      • high_value_affiliate_click") 
    print("      • email_signup_attempt")
    print("      • high_engagement")
    print()
    print("💡 If events don't appear:")
    print("   • Wait 24 hours for data processing")
    print("   • Check browser console for errors")
    print("   • Verify GA4 tag is firing")

def main():
    """Main function."""
    print("🎯 Analytics Event Testing")
    print("Generating test events for Google Analytics")
    print("=" * 50)
    
    print("Choose testing method:")
    print("1. 🤖 Automated browser simulation")
    print("2. 📖 Manual testing guide")
    print("3. 📊 Check existing events in GA4")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        try:
            simulate_user_behavior()
        except ImportError:
            print("❌ Selenium not installed. Install with: pip install selenium")
            print("📖 Showing manual testing guide instead...")
            manual_testing_guide()
    elif choice == "2":
        manual_testing_guide()
    elif choice == "3":
        check_events_in_ga4()
    else:
        print("📖 Showing manual testing guide...")
        manual_testing_guide()
    
    print("\n" + "=" * 50)
    print("🎉 Testing guide complete!")
    print("📊 Check GA4 Real-time reports: https://analytics.google.com/")

if __name__ == "__main__":
    main()
