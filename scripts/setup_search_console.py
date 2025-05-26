#!/usr/bin/env python3
"""
Google Search Console Setup Script
Helps configure GSC verification and submit sitemaps.
"""

import re
from pathlib import Path

def add_verification_code(verification_code):
    """Add Google Search Console verification code to the site."""
    
    print(f"🔧 Adding verification code: {verification_code[:20]}...")
    
    template_path = Path("hugo_site/layouts/_default/baseof.html")
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the placeholder with actual verification code
        updated_content = content.replace(
            'REPLACE_WITH_YOUR_VERIFICATION_CODE',
            verification_code
        )
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Verification code added successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error adding verification code: {e}")
        return False

def create_sitemap_submission_guide():
    """Create guide for submitting sitemaps."""
    
    print("\n📋 Sitemap Submission Guide")
    print("=" * 50)
    
    print("After verification, submit these sitemaps to GSC:")
    print()
    print("1. 🗺️ Main Sitemap:")
    print("   URL: https://imaginative-madeleine-0e6883.netlify.app/sitemap.xml")
    print("   Contains: All pages, posts, categories, tags")
    print()
    print("2. 📝 Posts Sitemap:")
    print("   URL: https://imaginative-madeleine-0e6883.netlify.app/posts/sitemap.xml")
    print("   Contains: All blog posts")
    print()
    print("3. 🏷️ Categories Sitemap:")
    print("   URL: https://imaginative-madeleine-0e6883.netlify.app/categories/sitemap.xml")
    print("   Contains: All category pages")
    print()
    print("📋 How to submit:")
    print("   1. Go to GSC → Sitemaps")
    print("   2. Enter sitemap URL (without domain)")
    print("   3. Click 'Submit'")
    print("   4. Repeat for each sitemap")

def create_indexing_requests():
    """Create list of URLs to request indexing for."""
    
    print("\n🚀 URL Indexing Requests")
    print("=" * 50)
    
    base_url = "https://imaginative-madeleine-0e6883.netlify.app"
    
    # Your 10 blog posts
    posts = [
        "best-crm-tools-small-business-2024",
        "best-project-management-tools-for-small-teams", 
        "discord-review-for-e-commerce-stores",
        "free-email-marketing-for-designers-top-tools",
        "getting-started-with-discord-for-remote-teams",
        "how-to-choose-analytics-tools-for-coaches",
        "top-analytics-tools-comparison-for-restaurants",
        "top-crm-tools-benefits-for-restaurants",
        "top-free-design-tools-for-designers-2023",
        "top-hotjar-alternatives-for-real-estate-agents"
    ]
    
    print("📝 Request indexing for these URLs in GSC:")
    print("   (Go to URL Inspection → Enter URL → Request Indexing)")
    print()
    
    # Priority URLs (highest commercial value)
    print("🎯 Priority URLs (submit first):")
    priority_posts = [
        "best-crm-tools-small-business-2024",
        "best-project-management-tools-for-small-teams",
        "free-email-marketing-for-designers-top-tools",
        "top-analytics-tools-comparison-for-restaurants"
    ]
    
    for post in priority_posts:
        print(f"   {base_url}/posts/{post}/")
    
    print(f"\n📄 All Blog Posts ({len(posts)} total):")
    for post in posts:
        print(f"   {base_url}/posts/{post}/")
    
    print(f"\n🏠 Important Pages:")
    important_pages = [
        "",  # Homepage
        "posts/",  # Blog index
        "categories/",  # Categories
        "tags/"  # Tags
    ]
    
    for page in important_pages:
        print(f"   {base_url}/{page}")

def show_gsc_optimization_tips():
    """Show tips for optimizing in Google Search Console."""
    
    print("\n📈 GSC Optimization Tips")
    print("=" * 50)
    
    print("🔍 Monitor These Reports:")
    print("   • Performance → Search Results (track rankings)")
    print("   • Coverage → Valid pages (ensure all indexed)")
    print("   • Enhancements → Core Web Vitals (site speed)")
    print("   • Security & Manual Actions (penalties)")
    print()
    print("📊 Key Metrics to Track:")
    print("   • Total clicks (traffic from Google)")
    print("   • Total impressions (how often you appear)")
    print("   • Average CTR (click-through rate)")
    print("   • Average position (ranking)")
    print()
    print("🎯 Optimization Actions:")
    print("   • Improve titles for low CTR pages")
    print("   • Optimize meta descriptions")
    print("   • Fix coverage issues")
    print("   • Monitor Core Web Vitals")
    print()
    print("⚡ Quick Wins:")
    print("   • Submit new content immediately")
    print("   • Fix any crawl errors")
    print("   • Optimize for mobile-first indexing")
    print("   • Monitor search appearance")

def main():
    """Main setup function."""
    print("🔍 Google Search Console Setup")
    print("Complete guide for SEO indexing")
    print("=" * 60)
    
    print("📋 Setup Process:")
    print("1. Go to: https://search.google.com/search-console/")
    print("2. Add property: https://imaginative-madeleine-0e6883.netlify.app")
    print("3. Choose HTML tag verification method")
    print("4. Copy the verification code")
    print("5. Run this script with your code")
    print()
    
    # Get verification code from user
    verification_code = input("Enter your GSC verification code (or 'skip' to see guides): ").strip()
    
    if verification_code.lower() != 'skip' and verification_code:
        # Clean the verification code (remove quotes, spaces)
        verification_code = verification_code.strip('"\'')
        
        if add_verification_code(verification_code):
            print("\n🚀 Next steps:")
            print("   1. Rebuild site: .\\build_site.bat")
            print("   2. Redeploy to Netlify")
            print("   3. Verify in GSC")
            print("   4. Submit sitemaps")
            print("   5. Request indexing for priority URLs")
    
    # Show guides regardless
    create_sitemap_submission_guide()
    create_indexing_requests()
    show_gsc_optimization_tips()
    
    print("\n" + "=" * 60)
    print("🎯 GSC Setup Complete!")
    print("Your site will start appearing in Google search results within 1-7 days")
    print("Monitor progress in GSC Performance reports")

if __name__ == "__main__":
    main()
