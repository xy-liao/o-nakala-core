#!/usr/bin/env python3
"""
Test script to investigate collection access and find alternative ways to access collection data.
"""

import os
import json
import requests
import sys

# Our collection IDs
OUR_COLLECTION_IDS = [
    "10.34847/nkl.ab97q400",
    "10.34847/nkl.e0cf86y9", 
    "10.34847/nkl.cb81u5mo"
]

def get_api_config():
    """Get API configuration."""
    api_key = os.getenv('NAKALA_API_KEY')
    api_url = "https://apitest.nakala.fr"
    
    if not api_key:
        print("ERROR: NAKALA_API_KEY environment variable not set")
        sys.exit(1)
    
    return api_url, api_key

def test_collection_via_search(collection_id: str, api_url: str, api_key: str):
    """Try to find collection via search endpoint."""
    print(f"\n--- Testing search for collection {collection_id} ---")
    
    headers = {'X-API-KEY': api_key}
    
    # Try search endpoint
    search_url = f"{api_url}/search"
    params = {
        'q': collection_id,
        'collectionId': collection_id
    }
    
    try:
        response = requests.get(search_url, headers=headers, params=params, timeout=30)
        print(f"Search Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Search results: {data}")
        else:
            print(f"Search failed: {response.text}")
    except Exception as e:
        print(f"Search error: {e}")

def find_collections_in_user_data(api_url: str, api_key: str):
    """Find our collections in the user collections list."""
    print("\n--- Searching for our collections in user data ---")
    
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    # Get user collections with detailed output
    query_body = {
        'page': 1,
        'limit': 1000
    }
    
    try:
        response = requests.post(f"{api_url}/users/collections/all", headers=headers, json=query_body, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            collections = data.get('data', [])
            
            print(f"Found {len(collections)} total collections")
            
            our_found_collections = []
            for collection in collections:
                collection_id = collection.get('identifier', '')
                if collection_id in OUR_COLLECTION_IDS:
                    our_found_collections.append(collection)
                    print(f"✓ Found our collection: {collection_id}")
                    print(f"  Title: {extract_title(collection.get('metas', []))}")
                    print(f"  Status: {collection.get('status', 'unknown')}")
                    print(f"  Created: {collection.get('creDate', 'unknown')}")
                    print(f"  Data count: {collection.get('data_count', 0)}")
                    
                    # Try to get more details
                    if 'data_count' in collection and collection['data_count'] > 0:
                        print(f"  -> Collection has {collection['data_count']} items")
            
            if not our_found_collections:
                print("✗ None of our collections found in user collections list")
                
                # Show first few collections as examples
                print("\nExample collections found:")
                for col in collections[:3]:
                    title = extract_title(col.get('metas', []))
                    print(f"  - {title} ({col.get('identifier', 'no-id')})")
            
            return our_found_collections
            
        else:
            print(f"Failed to get user collections: {response.text}")
            return []
            
    except Exception as e:
        print(f"Error getting user collections: {e}")
        return []

def extract_title(metas, language='fr'):
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

def test_datasets_for_collection_references(api_url: str, api_key: str):
    """Check if datasets reference collections."""
    print("\n--- Checking datasets for collection references ---")
    
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    # Get user datasets
    query_body = {
        'page': 1,
        'limit': 100  # Just get recent ones
    }
    
    try:
        response = requests.post(f"{api_url}/users/datas/all", headers=headers, json=query_body, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            datasets = data.get('data', [])
            
            print(f"Checking {len(datasets)} recent datasets...")
            
            datasets_with_collections = 0
            for dataset in datasets:
                # Check if dataset has collection references
                collections = dataset.get('collections', [])
                if collections:
                    datasets_with_collections += 1
                    title = extract_title(dataset.get('metas', []))
                    print(f"  Dataset '{title}' is in {len(collections)} collections:")
                    for col_ref in collections:
                        print(f"    - Collection ID: {col_ref}")
                        if col_ref in OUR_COLLECTION_IDS:
                            print(f"      *** This is one of our collections! ***")
            
            print(f"\nFound {datasets_with_collections} datasets with collection references")
            
        else:
            print(f"Failed to get datasets: {response.text}")
            
    except Exception as e:
        print(f"Error getting datasets: {e}")

def main():
    """Main test function."""
    print("Collection Access Investigation")
    print("=" * 50)
    
    api_url, api_key = get_api_config()
    print(f"API URL: {api_url}")
    print(f"Testing collection IDs: {OUR_COLLECTION_IDS}")
    
    # Look for collections in user data
    found_collections = find_collections_in_user_data(api_url, api_key)
    
    # Check dataset collection references
    test_datasets_for_collection_references(api_url, api_key)
    
    # Try search for each collection
    for collection_id in OUR_COLLECTION_IDS:
        test_collection_via_search(collection_id, api_url, api_key)
    
    print("\n" + "=" * 50)
    print("COLLECTION INVESTIGATION COMPLETE")
    print("=" * 50)

if __name__ == '__main__':
    main()