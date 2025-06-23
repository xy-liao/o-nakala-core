#!/usr/bin/env python3
"""
Cleanup Script for O-Nakala Test Data
Removes datasets and collections created during workflow testing to keep test platform clean.
"""

import csv
import json
import sys
import os
import requests
import time
from datetime import datetime

def load_upload_results(file_path=None):
    """Load dataset IDs from upload results."""
    dataset_ids = []
    
    # Try multiple possible filenames
    possible_files = file_path and [file_path] or [
        "upload_results.csv", 
        "fresh_upload_results.csv", 
        "workshop_upload_results.csv"
    ]
    
    upload_file = None
    for filename in possible_files:
        if os.path.exists(filename):
            upload_file = filename
            break
    
    if not upload_file:
        print(f"❌ No upload results file found!")
        print(f"   Looked for: {', '.join(possible_files)}")
        return dataset_ids
    
    print(f"📄 Found upload results: {upload_file}")
    with open(upload_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('identifier') and row.get('status') == 'OK':
                dataset_ids.append(row['identifier'])
    
    return dataset_ids

def load_collection_results(file_path="collections_output.csv"):
    """Load collection IDs from collection results."""
    collection_ids = []
    if not os.path.exists(file_path):
        print(f"ℹ️  Collection results file '{file_path}' not found (this is normal if collections weren't created)")
        return collection_ids
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('collection_id') and row.get('creation_status') == 'SUCCESS':
                collection_ids.append(row['collection_id'])
    
    return collection_ids

def delete_dataset(api_key, dataset_id, api_url="https://apitest.nakala.fr"):
    """Delete a single dataset."""
    headers = {'X-API-KEY': api_key}
    url = f"{api_url}/datas/{dataset_id}"
    
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return True, "Deleted successfully"
        elif response.status_code == 404:
            return True, "Already deleted or not found"
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def delete_collection(api_key, collection_id, api_url="https://apitest.nakala.fr"):
    """Delete a single collection."""
    headers = {'X-API-KEY': api_key}
    url = f"{api_url}/collections/{collection_id}"
    
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return True, "Deleted successfully"
        elif response.status_code == 404:
            return True, "Already deleted or not found"
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main cleanup function."""
    print("🧹 O-Nakala Test Data Cleanup Tool")
    print("=" * 50)
    
    # Check for API key
    api_key = os.environ.get('NAKALA_API_KEY')
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    if not api_key:
        print("❌ API key required!")
        print("Usage: python cleanup_test_data.py YOUR_API_KEY")
        print("   OR: export NAKALA_API_KEY=your-key && python cleanup_test_data.py")
        sys.exit(1)
    
    # Load data to cleanup
    datasets = load_upload_results()
    collections = load_collection_results()
    
    if not datasets and not collections:
        print("ℹ️  No test data found to cleanup.")
        print("   Make sure you're in the directory with upload_results.csv")
        return
    
    # Show what will be cleaned up
    print(f"📋 Found test data to cleanup:")
    if datasets:
        print(f"   📊 {len(datasets)} datasets")
    if collections:
        print(f"   📁 {len(collections)} collections")
    
    print(f"\n🔑 Using API key: {api_key[:8]}...")
    
    # Confirmation
    if '--force' not in sys.argv:
        confirm = input("\n⚠️  This will PERMANENTLY DELETE the test data. Continue? (yes/no): ")
        if confirm.lower() not in ['yes', 'y']:
            print("❌ Cleanup cancelled.")
            return
    
    # Cleanup collections first (they might reference datasets)
    success_count = 0
    error_count = 0
    
    if collections:
        print(f"\n🗂️  Cleaning up {len(collections)} collections...")
        for i, collection_id in enumerate(collections, 1):
            print(f"   {i}/{len(collections)} Deleting collection {collection_id}...", end=" ")
            success, message = delete_collection(api_key, collection_id)
            if success:
                print(f"✅ {message}")
                success_count += 1
            else:
                print(f"❌ {message}")
                error_count += 1
            time.sleep(0.5)  # Be gentle with the API
    
    # Cleanup datasets
    if datasets:
        print(f"\n📊 Cleaning up {len(datasets)} datasets...")
        for i, dataset_id in enumerate(datasets, 1):
            print(f"   {i}/{len(datasets)} Deleting dataset {dataset_id}...", end=" ")
            success, message = delete_dataset(api_key, dataset_id)
            if success:
                print(f"✅ {message}")
                success_count += 1
            else:
                print(f"❌ {message}")
                error_count += 1
            time.sleep(0.5)  # Be gentle with the API
    
    # Summary
    print(f"\n📊 Cleanup Summary:")
    print(f"   ✅ Successfully cleaned: {success_count}")
    print(f"   ❌ Errors: {error_count}")
    
    if error_count == 0:
        print(f"\n🎉 All test data cleaned up successfully!")
        print(f"   Test platform is now clean for the next user.")
    else:
        print(f"\n⚠️  Some items couldn't be deleted (might already be gone).")
    
    # Optional: backup result files
    if '--keep-files' not in sys.argv and (datasets or collections):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_files = ['upload_results.csv', 'collections_output.csv', 'quality_report.json', 'auto_data_modifications.csv']
        
        print(f"\n📁 Backing up result files...")
        for file in backup_files:
            if os.path.exists(file):
                backup_name = f"{file}.backup_{timestamp}"
                os.rename(file, backup_name)
                print(f"   📄 {file} → {backup_name}")
        
        print(f"✅ Result files backed up with timestamp {timestamp}")

if __name__ == "__main__":
    main()