#!/usr/bin/env python3
"""
Test script to verify curator can find and analyze our specific uploaded datasets.
"""

import os
import json
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nakala_client.curator import NakalaCuratorClient, CuratorConfig
from nakala_client.user_info import NakalaUserInfoClient

# Our uploaded dataset IDs
OUR_DATASET_IDS = [
    "10.34847/nkl.a1c6rxsi",
    "10.34847/nkl.622f0624", 
    "10.34847/nkl.f73alm0t",
    "10.34847/nkl.77b54li1",
    "10.34847/nkl.1bf85j8k"
]

# Our collection IDs
OUR_COLLECTION_IDS = [
    "10.34847/nkl.ab97q400",
    "10.34847/nkl.e0cf86y9", 
    "10.34847/nkl.cb81u5mo"
]

def main():
    """Test curator with our specific items."""
    
    # Create configuration
    config = CuratorConfig(
        api_url="https://apitest.nakala.fr",
        api_key=os.getenv('NAKALA_API_KEY')
    )
    
    if not config.validate():
        print("ERROR: Configuration validation failed")
        return 1
    
    print("Testing Curator with Specific Uploaded Items")
    print("=" * 50)
    
    # Create user info client to get all data
    user_client = NakalaUserInfoClient(config)
    profile = user_client.get_complete_user_profile()
    
    print(f"Total user datasets: {len(profile['datasets'])}")
    print(f"Total user collections: {len(profile['collections'])}")
    
    # Find our specific items
    our_datasets = []
    our_collections = []
    
    for dataset in profile['datasets']:
        if dataset['id'] in OUR_DATASET_IDS:
            our_datasets.append(dataset)
            print(f"✓ Found our dataset: {dataset['title']} ({dataset['id']})")
    
    for collection in profile['collections']:
        if collection['id'] in OUR_COLLECTION_IDS:
            our_collections.append(collection)
            print(f"✓ Found our collection: {collection['title']} ({collection['id']})")
    
    print(f"\nFound {len(our_datasets)}/{len(OUR_DATASET_IDS)} of our datasets")
    print(f"Found {len(our_collections)}/{len(OUR_COLLECTION_IDS)} of our collections")
    
    # Test curator analysis on our items
    curator = NakalaCuratorClient(config)
    
    if our_datasets:
        print("\n" + "=" * 50)
        print("ANALYZING OUR DATASETS")
        print("=" * 50)
        
        validation_result = curator.batch_validate_metadata(our_datasets)
        print(f"Validation results:")
        print(f"  Total items: {validation_result['total_items']}")
        print(f"  Valid items: {validation_result['valid_items']}")
        print(f"  Items with errors: {validation_result['items_with_errors']}")
        print(f"  Items with warnings: {validation_result['items_with_warnings']}")
        
        # Show details for each item
        for detail in validation_result['validation_details']:
            print(f"\n  {detail['title']} ({detail['id']}):")
            if detail['errors']:
                print(f"    Errors: {detail['errors']}")
            if detail['warnings']:
                print(f"    Warnings: {detail['warnings']}")
            if detail['suggestions']:
                print(f"    Suggestions: {detail['suggestions']}")
    
    if our_collections:
        print("\n" + "=" * 50)
        print("ANALYZING OUR COLLECTIONS")
        print("=" * 50)
        
        validation_result = curator.batch_validate_metadata(our_collections)
        print(f"Validation results:")
        print(f"  Total items: {validation_result['total_items']}")
        print(f"  Valid items: {validation_result['valid_items']}")
        print(f"  Items with errors: {validation_result['items_with_errors']}")
        print(f"  Items with warnings: {validation_result['items_with_warnings']}")
        
        # Show details for each item
        for detail in validation_result['validation_details']:
            print(f"\n  {detail['title']} ({detail['id']}):")
            if detail['errors']:
                print(f"    Errors: {detail['errors']}")
            if detail['warnings']:
                print(f"    Warnings: {detail['warnings']}")
            if detail['suggestions']:
                print(f"    Suggestions: {detail['suggestions']}")
    
    # Test duplicate detection on our datasets
    if len(our_datasets) > 1:
        print("\n" + "=" * 50)
        print("TESTING DUPLICATE DETECTION")
        print("=" * 50)
        
        duplicates = curator.duplicate_detector.find_duplicates(our_datasets)
        print(f"Found {len(duplicates)} potential duplicate pairs")
        
        for item1, item2, similarity in duplicates:
            print(f"  {item1['title']} <-> {item2['title']} (similarity: {similarity:.3f})")
    
    print("\n" + "=" * 50)
    print("CURATOR TEST COMPLETE")
    print("=" * 50)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())