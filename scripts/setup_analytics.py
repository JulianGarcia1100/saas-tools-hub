#!/usr/bin/env python3
"""
Google Analytics Setup Script
Configures GA4 tracking for the SEO affiliate site.
"""

import sys
from pathlib import Path

def update_analytics_config(measurement_id):
    """Update Hugo configuration with Google Analytics."""
    
    print(f"🔧 Setting up Google Analytics with ID: {measurement_id}")
    
    # Update Hugo config
    config_path = Path("hugo_site/config.yaml")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the placeholder GA ID
        updated_content = content.replace(
            'google_analytics: your_ga_property_id',
            f'google_analytics: {measurement_id}'
        )
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Updated Hugo configuration")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

def create_enhanced_tracking():
    """Create enhanced tracking for affiliate links."""
    
    print("🔧 Creating enhanced tracking code...")
    
    # Enhanced tracking JavaScript
    tracking_js = """
<!-- Enhanced Analytics Tracking -->
<script>
// Track affiliate link clicks
document.addEventListener('DOMContentLoaded', function() {
    // Track affiliate CTA clicks
    const affiliateLinks = document.querySelectorAll('.affiliate-cta a, a[href*="affiliate"], a[target="_blank"]');
    
    affiliateLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const linkText = this.textContent.trim();
            const linkUrl = this.href;
            const toolName = linkText.includes('HubSpot') ? 'HubSpot' : 
                           linkText.includes('Asana') ? 'Asana' :
                           linkText.includes('Monday') ? 'Monday.com' :
                           linkText.includes('Canva') ? 'Canva' :
                           linkText.includes('ConvertKit') ? 'ConvertKit' :
                           'Unknown Tool';
            
            // Send event to Google Analytics
            if (typeof gtag !== 'undefined') {
                gtag('event', 'affiliate_click', {
                    'tool_name': toolName,
                    'link_text': linkText,
                    'link_url': linkUrl,
                    'page_title': document.title,
                    'value': 1
                });
                
                console.log('📊 Tracked affiliate click:', toolName);
            }
        });
    });
    
    // Track email signup attempts
    const emailForms = document.querySelectorAll('form, .email-signup');
    emailForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'email_signup_attempt', {
                    'page_title': document.title,
                    'form_location': 'email_capture',
                    'value': 5
                });
                
                console.log('📊 Tracked email signup attempt');
            }
        });
    });
    
    // Track scroll depth for engagement
    let maxScroll = 0;
    window.addEventListener('scroll', function() {
        const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
        
        if (scrollPercent > maxScroll && scrollPercent % 25 === 0) {
            maxScroll = scrollPercent;
            
            if (typeof gtag !== 'undefined') {
                gtag('event', 'scroll_depth', {
                    'scroll_percent': scrollPercent,
                    'page_title': document.title
                });
            }
        }
    });
});
</script>
"""
    
    # Save enhanced tracking
    tracking_path = Path("hugo_site/layouts/partials/analytics.html")
    tracking_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(tracking_path, 'w', encoding='utf-8') as f:
            f.write(tracking_js)
        
        print("✅ Created enhanced tracking code")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tracking: {e}")
        return False

def update_base_template():
    """Update base template to include analytics."""
    
    print("🔧 Updating base template...")
    
    template_path = Path("hugo_site/layouts/_default/baseof.html")
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add analytics partial before closing head tag
        analytics_include = """
    <!-- Enhanced Analytics -->
    {{ if .Site.Params.google_analytics }}
    {{ partial "analytics.html" . }}
    {{ end }}
</head>"""
        
        updated_content = content.replace('</head>', analytics_include)
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Updated base template")
        return True
        
    except Exception as e:
        print(f"❌ Error updating template: {e}")
        return False

def setup_conversion_goals():
    """Display conversion goals setup instructions."""
    
    print("\n📊 Conversion Goals to Set Up in GA4:")
    print("=" * 50)
    
    goals = [
        {
            'name': 'Affiliate Click',
            'event': 'affiliate_click',
            'description': 'User clicks on affiliate link',
            'value': '$1.00'
        },
        {
            'name': 'Email Signup',
            'event': 'email_signup_attempt', 
            'description': 'User attempts email signup',
            'value': '$5.00'
        },
        {
            'name': 'High Engagement',
            'event': 'scroll_depth',
            'description': 'User scrolls 75% of page',
            'value': '$0.50'
        }
    ]
    
    for i, goal in enumerate(goals, 1):
        print(f"{i}. {goal['name']}")
        print(f"   Event: {goal['event']}")
        print(f"   Value: {goal['value']}")
        print(f"   Description: {goal['description']}")
        print()
    
    print("🎯 To set these up in GA4:")
    print("   1. Go to Admin → Events → Create Event")
    print("   2. Use the event names above")
    print("   3. Set up conversions for each event")

def main():
    """Main setup function."""
    print("🎯 Google Analytics Setup for SEO Affiliate Site")
    print("=" * 60)
    
    print("📋 This script will:")
    print("   1. Update Hugo config with your GA4 Measurement ID")
    print("   2. Add enhanced tracking for affiliate links")
    print("   3. Set up conversion tracking")
    print("   4. Create engagement metrics")
    print()
    
    # Get measurement ID from user
    measurement_id = input("Enter your GA4 Measurement ID (G-XXXXXXXXXX): ").strip()
    
    if not measurement_id.startswith('G-'):
        print("❌ Invalid Measurement ID. Should start with 'G-'")
        return
    
    print(f"\n🔧 Setting up analytics for: {measurement_id}")
    
    # Run setup steps
    steps = [
        ("Updating Hugo configuration", lambda: update_analytics_config(measurement_id)),
        ("Creating enhanced tracking", create_enhanced_tracking),
        ("Updating base template", update_base_template)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if step_func():
            success_count += 1
        else:
            print(f"❌ Failed: {step_name}")
    
    print(f"\n📊 Setup Results: {success_count}/{len(steps)} steps completed")
    
    if success_count == len(steps):
        print("\n🎉 Google Analytics setup complete!")
        print("\n🚀 Next steps:")
        print("   1. Rebuild your site: python build_site.bat")
        print("   2. Redeploy to Netlify")
        print("   3. Test tracking in GA4 Real-Time reports")
        print("   4. Set up conversion goals (see instructions above)")
        
        setup_conversion_goals()
    else:
        print("\n❌ Setup incomplete. Please check errors above.")

if __name__ == "__main__":
    main()
