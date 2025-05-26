#!/usr/bin/env python3
"""
Update HubSpot form IDs in all HTML files in the public directory.
This script replaces placeholder values with real HubSpot form IDs.
"""

import os
import re
from pathlib import Path

def update_hubspot_forms():
    """Update all HTML files with correct HubSpot form IDs."""
    
    # Your actual HubSpot IDs
    PORTAL_ID = "242884057"
    FORM_ID = "42c2c4f6-b032-421b-b9b2-879acb08e826"
    
    # Directory containing the built HTML files
    public_dir = Path("hugo_site/public")
    
    if not public_dir.exists():
        print("❌ Public directory not found. Make sure you're in the project root.")
        return False
    
    print("🔧 Updating HubSpot form IDs in HTML files...")
    
    # Find all HTML files
    html_files = list(public_dir.rglob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found in public directory.")
        return False
    
    updated_count = 0
    
    for html_file in html_files:
        try:
            # Read the file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if this file contains HubSpot form code
            if 'hubspot-form' not in content and 'hbspt.forms.create' not in content:
                continue
            
            original_content = content
            
            # Replace placeholder portal ID
            content = content.replace('your_hubspot_portal_id', PORTAL_ID)
            content = content.replace('"your_hubspot_portal_id"', f'"{PORTAL_ID}"')
            
            # Replace placeholder form ID  
            content = content.replace('your-form-id', FORM_ID)
            content = content.replace('"your-form-id"', f'"{FORM_ID}"')
            
            # Update the script source to use the correct region
            content = content.replace(
                'src=//js.hsforms.net/forms/v2.js',
                'src=//js-na2.hsforms.net/forms/embed/v2.js'
            )
            
            # Only write if content changed
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                updated_count += 1
                print(f"✅ Updated: {html_file.relative_to(public_dir)}")
        
        except Exception as e:
            print(f"❌ Error updating {html_file}: {e}")
            continue
    
    print(f"\n🎉 Successfully updated {updated_count} HTML files!")
    print(f"📝 Portal ID: {PORTAL_ID}")
    print(f"📝 Form ID: {FORM_ID}")
    
    return updated_count > 0

def verify_updates():
    """Verify that the updates were applied correctly."""
    
    print("\n🔍 Verifying updates...")
    
    # Check a sample file
    sample_file = Path("hugo_site/public/posts/best-crm-tools-small-business-2024/index.html")
    
    if not sample_file.exists():
        print("❌ Sample file not found for verification.")
        return False
    
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for the real IDs
        if '242884057' in content and '42c2c4f6-b032-421b-b9b2-879acb08e826' in content:
            print("✅ Verification successful! HubSpot form IDs are correctly updated.")
            return True
        else:
            print("❌ Verification failed. Placeholder values may still exist.")
            return False
    
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

if __name__ == "__main__":
    print("🚀 HubSpot Form ID Updater")
    print("=" * 40)
    
    # Change to the project directory
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    os.chdir(project_dir)
    
    # Update the forms
    success = update_hubspot_forms()
    
    if success:
        # Verify the updates
        verify_updates()
        
        print("\n🎯 Next Steps:")
        print("1. Deploy the updated public folder to Netlify")
        print("2. Test the newsletter signup on your live site")
        print("3. Check HubSpot dashboard for form submissions")
    else:
        print("\n❌ Update failed. Please check the error messages above.")
