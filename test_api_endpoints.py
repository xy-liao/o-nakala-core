#!/usr/bin/env python3
"""
Test script to investigate NAKALA API endpoints and verify access to uploaded data.
"""

import os
import json
import requests
import sys
from typing import Dict, Any, List

# IDs from the successful upload and collection creation
DATASET_IDS = [
    "10.34847/nkl.a1c6rxsi",
    "10.34847/nkl.622f0624", 
    "10.34847/nkl.f73alm0t",
    "10.34847/nkl.77b54li1",
    "10.34847/nkl.1bf85j8k"
]

COLLECTION_IDS = [
    "10.34847/nkl.ab97q400",
    "10.34847/nkl.e0cf86y9", 
    "10.34847/nkl.cb81u5mo"
]

def get_api_config():
    """Get API configuration from environment."""
    api_key = os.getenv('NAKALA_API_KEY')
    api_url = "https://apitest.nakala.fr"
    
    if not api_key:
        print("ERROR: NAKALA_API_KEY environment variable not set")
        sys.exit(1)
    
    return api_url, api_key

def test_direct_access(item_id: str, item_type: str, api_url: str, api_key: str):
    """Test direct access to a specific item."""
    print(f"\n--- Testing direct access to {item_type}: {item_id} ---")
    
    if item_type == "dataset":
        url = f"{api_url}/datas/{item_id}"
    else:  # collection
        url = f"{api_url}/collections/{item_id}"
    
    headers = {'X-API-KEY': api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Successfully accessed item")
            print(f"  Title: {extract_title(data.get('metas', []))}")
            print(f"  Status: {data.get('status', 'unknown')}")
            print(f"  Created: {data.get('creDate', 'unknown')}")
            return True
        else:
            print(f"✗ Failed to access item: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error accessing item: {e}")
        return False

def test_user_endpoints(api_url: str, api_key: str):
    """Test the correct user endpoints."""
    print("\n--- Testing user endpoints ---")
    
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    # Test user info endpoint
    print("\n1. Testing /users/me")
    try:
        response = requests.get(f"{api_url}/users/me", headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"✓ User: {user_data.get('fullname', 'N/A')}")
            print(f"  Email: {user_data.get('mail', 'N/A')}")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test collections endpoint with POST
    print("\n2. Testing POST /users/collections/all")
    try:
        query_body = {
            "page": 1,
            "limit": 1000
        }
        response = requests.post(f"{api_url}/users/collections/all", headers=headers, json=query_body, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            collections = data.get('data', [])
            print(f"✓ Found {len(collections)} collections")
            for col in collections[:3]:  # Show first 3
                title = extract_title(col.get('metas', []))
                print(f"  - {title} ({col.get('identifier', 'no-id')})")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test datasets endpoint with POST
    print("\n3. Testing POST /users/datas/all")
    try:
        query_body = {
            "page": 1,
            "limit": 1000
        }
        response = requests.post(f"{api_url}/users/datas/all", headers=headers, json=query_body, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            datasets = data.get('data', [])
            print(f"✓ Found {len(datasets)} datasets")
            for ds in datasets[:3]:  # Show first 3
                title = extract_title(ds.get('metas', []))
                print(f"  - {title} ({ds.get('identifier', 'no-id')})")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")

def extract_title(metas: List[Dict], language: str = 'fr') -> str:
    """Extract title from metadata array."""
    if not metas:
        return 'No title'
        
    # Look for title in preferred language first
    for meta in metas:
        property_uri = meta.get('propertyUri', '')
        meta_lang = meta.get('lang', '')
        
        if 'title' in property_uri.lower() and meta_lang == language:
            return meta.get('value', '')
    
    # Fall back to any language
    for meta in metas:
        property_uri = meta.get('propertyUri', '')
        if 'title' in property_uri.lower():
            return meta.get('value', '')
            
    return 'No title found'

def test_collection_items(collection_id: str, api_url: str, api_key: str):
    """Test accessing items in a collection."""
    print(f"\n--- Testing collection items for {collection_id} ---")
    
    url = f"{api_url}/collections/{collection_id}/datas"
    headers = {'X-API-KEY': api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('data', [])
            print(f"✓ Found {len(items)} items in collection")
            for item in items:
                title = extract_title(item.get('metas', []))
                print(f"  - {title} ({item.get('identifier', 'no-id')})")
            return True
        else:
            print(f"✗ Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Main test function."""
    print("NAKALA API Endpoint Investigation")
    print("=" * 50)
    
    api_url, api_key = get_api_config()
    print(f"API URL: {api_url}")
    print(f"API Key: {api_key[:8]}...")
    
    # Test direct access to uploaded datasets
    print("\n" + "=" * 50)
    print("TESTING DIRECT DATASET ACCESS")
    print("=" * 50)
    
    dataset_access_count = 0
    for dataset_id in DATASET_IDS:
        if test_direct_access(dataset_id, "dataset", api_url, api_key):
            dataset_access_count += 1
    
    print(f"\nDataset access summary: {dataset_access_count}/{len(DATASET_IDS)} accessible")
    
    # Test direct access to created collections
    print("\n" + "=" * 50)
    print("TESTING DIRECT COLLECTION ACCESS")
    print("=" * 50)
    
    collection_access_count = 0
    for collection_id in COLLECTION_IDS:
        if test_direct_access(collection_id, "collection", api_url, api_key):
            collection_access_count += 1
    
    print(f"\nCollection access summary: {collection_access_count}/{len(COLLECTION_IDS)} accessible")
    
    # Test user endpoints
    print("\n" + "=" * 50)
    print("TESTING USER ENDPOINTS")
    print("=" * 50)
    
    test_user_endpoints(api_url, api_key)
    
    # Test collection item access
    print("\n" + "=" * 50)
    print("TESTING COLLECTION ITEM ACCESS")
    print("=" * 50)
    
    for collection_id in COLLECTION_IDS[:1]:  # Test first collection
        test_collection_items(collection_id, api_url, api_key)
    
    print("\n" + "=" * 50)
    print("INVESTIGATION COMPLETE")
    print("=" * 50)

if __name__ == '__main__':
    main()