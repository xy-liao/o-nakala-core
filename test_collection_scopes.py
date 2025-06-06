#!/usr/bin/env python3
"""
Test different collection scopes to understand where our collections are.
"""

import os
import json
import requests

def get_api_config():
    """Get API configuration."""
    api_key = os.getenv('NAKALA_API_KEY')
    api_url = "https://apitest.nakala.fr"
    
    if not api_key:
        print("ERROR: NAKALA_API_KEY environment variable not set")
        return None, None
    
    return api_url, api_key

def extract_title(metas, language='fr'):
    """Extract title from metadata array."""
    if not metas:
        return 'No title'
        
    for meta in metas:
        property_uri = meta.get('propertyUri', '')
        meta_lang = meta.get('lang', '')
        
        if 'title' in property_uri.lower() and meta_lang == language:
            return meta.get('value', '')
    
    for meta in metas:
        property_uri = meta.get('propertyUri', '')
        if 'title' in property_uri.lower():
            return meta.get('value', '')
            
    return 'No title found'

def test_collection_scope(scope: str, api_url: str, api_key: str):
    """Test a specific collection scope."""
    print(f"\n--- Testing scope: {scope} ---")
    
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    query_body = {
        'page': 1,
        'limit': 1000
    }
    
    try:
        response = requests.post(f"{api_url}/users/collections/{scope}", headers=headers, json=query_body, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            collections = data.get('data', [])
            print(f"Found {len(collections)} collections")
            
            # Look for our collections
            our_collection_ids = [
                "10.34847/nkl.ab97q400",
                "10.34847/nkl.e0cf86y9", 
                "10.34847/nkl.cb81u5mo"
            ]
            
            found_ours = []
            for collection in collections:
                collection_id = collection.get('identifier', '')
                if collection_id in our_collection_ids:
                    found_ours.append(collection)
                    print(f"  ✓ FOUND OUR COLLECTION: {collection_id}")
                    print(f"    Title: {extract_title(collection.get('metas', []))}")
                    print(f"    Status: {collection.get('status', 'unknown')}")
                    print(f"    Data count: {collection.get('data_count', 0)}")
            
            if not found_ours:
                print(f"  ✗ None of our collections found in scope '{scope}'")
                
                # Show first few as examples
                if collections:
                    print("  Example collections:")
                    for col in collections[:3]:
                        title = extract_title(col.get('metas', []))
                        print(f"    - {title} ({col.get('identifier', 'no-id')})")
            
            return found_ours
            
        else:
            print(f"Failed: {response.text}")
            return []
            
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    """Test different collection scopes."""
    print("Collection Scope Investigation")
    print("=" * 50)
    
    api_url, api_key = get_api_config()
    if not api_url:
        return 1
    
    print(f"API URL: {api_url}")
    
    # Test different scopes
    scopes = ['all', 'owned', 'deposited', 'shared', 'editable', 'readable']
    
    total_found = 0
    for scope in scopes:
        found = test_collection_scope(scope, api_url, api_key)
        total_found += len(found)
    
    print(f"\n" + "=" * 50)
    print(f"SUMMARY: Found our collections in {total_found} scopes total")
    print("=" * 50)
    
    return 0

if __name__ == '__main__':
    exit(main())