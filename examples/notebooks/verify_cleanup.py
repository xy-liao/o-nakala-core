#!/usr/bin/env python3
"""
Verification Script for O-Nakala Cleanup
Verifies that datasets were actually deleted from the NAKALA server.
"""

import csv
import json
import sys
import os
import requests
import time

def verify_deletion(api_key, dataset_id, api_url="https://apitest.nakala.fr"):
    """Verify a dataset was actually deleted from NAKALA server."""
    headers = {'X-API-KEY': api_key}
    url = f"{api_url}/datas/{dataset_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return True, "✅ Confirmed deleted"
        elif response.status_code == 200:
            return False, "❌ Still exists on server"
        else:
            return None, f"⚠️ Unexpected response: {response.status_code}"
    except Exception as e:
        return None, f"❌ Error checking: {str(e)}"

def main():
    """Verify cleanup was successful."""
    print("🔍 NAKALA Cleanup Verification Tool")
    print("=" * 40)
    
    # Check for API key
    api_key = os.environ.get('NAKALA_API_KEY')
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    if not api_key:
        print("❌ API key required!")
        print("Usage: python verify_cleanup.py YOUR_API_KEY")
        sys.exit(1)
    
    # Look for backup files to find what was supposedly deleted
    backup_files = [f for f in os.listdir('.') if f.endswith('.backup_20250623_134422')]
    
    if not backup_files:
        print("ℹ️  No backup files found - no cleanup to verify")
        return
    
    # Find the upload results backup
    upload_backup = None
    for f in backup_files:
        if 'upload_results' in f or 'fresh_upload_results' in f:
            upload_backup = f
            break
    
    if not upload_backup:
        print("❌ No upload results backup found to verify against")
        return
    
    print(f"📄 Checking against backup: {upload_backup}")
    
    # Read the backed up upload results
    dataset_ids = []
    with open(upload_backup, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('identifier') and row.get('status') == 'OK':
                dataset_ids.append(row['identifier'])
    
    if not dataset_ids:
        print("❌ No dataset IDs found in backup file")
        return
    
    print(f"🔑 Using API key: {api_key[:8]}...")
    print(f"📊 Verifying deletion of {len(dataset_ids)} datasets...")
    print()
    
    # Verify each dataset was deleted
    verified_deleted = 0
    still_exists = 0
    check_errors = 0
    
    for i, dataset_id in enumerate(dataset_ids, 1):
        print(f"   {i}/{len(dataset_ids)} Checking {dataset_id}...", end=" ")
        
        deleted, message = verify_deletion(api_key, dataset_id)
        print(message)
        
        if deleted is True:
            verified_deleted += 1
        elif deleted is False:
            still_exists += 1
        else:
            check_errors += 1
        
        time.sleep(0.3)  # Be gentle with API
    
    print()
    print("📊 Verification Summary:")
    print(f"   ✅ Confirmed deleted: {verified_deleted}")
    print(f"   ❌ Still exists: {still_exists}")
    print(f"   ⚠️ Check errors: {check_errors}")
    
    if still_exists == 0 and check_errors == 0:
        print()
        print("🎉 Cleanup verification PASSED!")
        print("   All datasets were successfully removed from NAKALA server.")
    elif still_exists > 0:
        print()
        print("⚠️  Cleanup verification FAILED!")
        print(f"   {still_exists} datasets still exist on server.")
        print("   You may need to run cleanup again.")
    else:
        print()
        print("❓ Verification inconclusive due to API errors.")

if __name__ == "__main__":
    main()