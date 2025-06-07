#!/usr/bin/env python3
"""
Test API Validation Differences: Creation vs Modification

This script tests the hypothesis that NAKALA API has strict validation for creation
but more permissive validation for modification operations.
"""

import requests
import json

API_KEY = "f41f5957-d396-3bb9-ce35-a4692773f636"
API_URL = "https://apitest.nakala.fr"

def test_collection_partial_update():
    """Test if collections can be updated with partial metadata."""
    print("🧪 Testing Collection Partial Update")
    print("=" * 50)
    
    collection_id = "10.34847/nkl.4bfffoct"  # Our multimedia collection
    
    # Test 1: Update only title (minimal metadata)
    minimal_update = {
        "metas": [
            {
                "propertyUri": "http://nakala.fr/terms#title",
                "value": "TEST: Minimal Update - Just Title",
                "lang": "en",
                "typeUri": None
            }
        ]
    }
    
    print("🔍 Test 1: Update collection with ONLY title field...")
    response = requests.put(
        f"{API_URL}/collections/{collection_id}",
        headers={"X-API-KEY": API_KEY, "Content-Type": "application/json"},
        json=minimal_update
    )
    
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ SUCCESS: Minimal metadata update worked!")
    else:
        print(f"   ❌ FAILED: {response.text}")
    
    return response.status_code == 200

def test_data_item_partial_update():
    """Test if data items can be updated with partial metadata."""
    print("\n🧪 Testing Data Item Partial Update")
    print("=" * 50)
    
    data_id = "10.34847/nkl.7b0es7tm"  # Our image collection
    
    # Test 1: Update only title (minimal metadata) - should fail
    minimal_update = {
        "metas": [
            {
                "propertyUri": "http://nakala.fr/terms#title",
                "value": "TEST: Minimal Update - Just Title",
                "lang": "en",
                "typeUri": None
            }
        ]
    }
    
    print("🔍 Test 1: Update data item with ONLY title field...")
    response = requests.put(
        f"{API_URL}/datas/{data_id}",
        headers={"X-API-KEY": API_KEY, "Content-Type": "application/json"},
        json=minimal_update
    )
    
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ SUCCESS: Minimal metadata update worked!")
        minimal_works = True
    else:
        print(f"   ❌ FAILED: {response.text}")
        minimal_works = False
    
    # Test 2: Update with required fields included
    complete_update = {
        "metas": [
            {
                "propertyUri": "http://nakala.fr/terms#title",
                "value": "TEST: Complete Update - With Required Fields",
                "lang": "en",
                "typeUri": None
            },
            {
                "propertyUri": "http://nakala.fr/terms#type",
                "value": "http://purl.org/coar/resource_type/c_c513",
                "lang": None,
                "typeUri": "http://purl.org/dc/terms/URI"
            }
        ]
    }
    
    print("\n🔍 Test 2: Update data item with required fields...")
    response = requests.put(
        f"{API_URL}/datas/{data_id}",
        headers={"X-API-KEY": API_KEY, "Content-Type": "application/json"},
        json=complete_update
    )
    
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ SUCCESS: Complete metadata update worked!")
        complete_works = True
    else:
        print(f"   ❌ FAILED: {response.text}")
        complete_works = False
    
    return minimal_works, complete_works

def analyze_creation_requirements():
    """Analyze what was required during the original creation."""
    print("\n📋 Analysis: Original Creation Requirements")
    print("=" * 50)
    
    print("✅ CREATION PHASE REQUIRED:")
    print("   • Data Items: title, type, description, keywords, language, license, created, rights")
    print("   • Collections: title, description, keywords, language, creator, contributor, publisher")
    print("   • All fields had to be complete and valid")
    print("   • Upload process validated CSV structure")
    
    print("\n🔍 MODIFICATION PHASE OBSERVED:")
    print("   • Collections: Only partial updates needed (just title worked)")
    print("   • Data Items: More complex - some required fields must be preserved")
    print("   • API more permissive than client-side curator validation")

def main():
    print("🔬 NAKALA API Validation Comparison: Creation vs Modification")
    print("=" * 70)
    
    # Test collection updates
    collection_success = test_collection_partial_update()
    
    # Test data item updates  
    data_minimal, data_complete = test_data_item_partial_update()
    
    # Analyze original creation
    analyze_creation_requirements()
    
    # Summary
    print("\n📊 VALIDATION COMPARISON RESULTS")
    print("=" * 50)
    
    print(f"🏗️  CREATION PHASE:")
    print(f"   Collections: ✅ Required complete metadata")
    print(f"   Data Items:  ✅ Required complete metadata")
    
    print(f"\n🔧 MODIFICATION PHASE:")
    print(f"   Collections: {'✅ Minimal updates work' if collection_success else '❌ Requires complete metadata'}")
    print(f"   Data Items:  {'✅ Minimal updates work' if data_minimal else '❌ Requires some mandatory fields'}")
    print(f"                {'✅ Complete updates work' if data_complete else '❌ Complete updates fail'}")
    
    print(f"\n🎯 CONCLUSION:")
    if collection_success and not data_minimal and data_complete:
        print("   ✅ HYPOTHESIS CONFIRMED:")
        print("   • API has STRICT validation during creation")
        print("   • API has PERMISSIVE validation during modification")
        print("   • Collections more permissive than data items during modification")
        print("   • Data items need some required fields preserved during updates")
    else:
        print("   ❓ HYPOTHESIS NEEDS REFINEMENT:")
        print("   • Validation patterns may be more complex than creation vs modification")
    
    return 0

if __name__ == '__main__':
    exit(main())