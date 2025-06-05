#!/usr/bin/env python3
"""
Demonstrate metadata validation command
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nakala_client.curator import CuratorConfig, NakalaCuratorClient

# Simulate validation command output
def simulate_validation_command():
    print("🔍 Simulating: ./nakala-curator.py --validate-metadata --scope all")
    print("=" * 60)
    
    config = CuratorConfig(
        api_key="aae99aba-476e-4ff2-2886-0aaf1bfa6fd2",
        api_url="https://apitest.nakala.fr"
    )
    
    # Sample metadata items (simulating what would come from user's collections)
    sample_items = [
        {
            'id': 'collection-001',
            'title': 'Medieval Manuscripts Collection',
            'creator': 'University Library',
            'description': 'A comprehensive collection of digitized medieval manuscripts from the 12th to 15th centuries, including illuminated texts and historical documents.',
            'keywords': 'medieval, manuscripts, history, illuminated',
            'language': 'la',
            'license': 'CC-BY-4.0'
        },
        {
            'id': 'dataset-002', 
            'title': 'Temperature Data',
            'creator': '',  # Error: missing creator
            'description': 'Data',  # Error: too short
            'keywords': '',
            'language': 'en',
            'license': 'CC-BY-4.0'
        },
        {
            'id': 'collection-003',
            'title': 'Archaeological Survey Results',
            'creator': 'Dr. Sarah Johnson',
            'description': 'Survey results from the 2023 archaeological excavation in southern France, including pottery fragments, tools, and structural remains.',
            'keywords': 'archaeology, excavation, pottery, tools',
            'language': 'fr',
            'license': 'CC-BY-SA-4.0'
        }
    ]
    
    curator = NakalaCuratorClient(config)
    result = curator.batch_validate_metadata(sample_items)
    
    print(f"📊 Metadata Validation Results:")
    print(f"   Total items validated: {result['total_items']}")
    print(f"   Valid items: {result['valid_items']}")
    print(f"   Items with errors: {result['items_with_errors']}")
    print(f"   Items with warnings: {result['items_with_warnings']}")
    
    print(f"\n📋 Detailed Validation Results:")
    for detail in result['validation_details']:
        print(f"\n   📄 {detail['title']}")
        print(f"      ID: {detail['id']}")
        
        if detail['errors']:
            print(f"      ❌ Errors:")
            for error in detail['errors']:
                print(f"         • {error}")
        
        if detail['warnings']:
            print(f"      ⚠️  Warnings:")
            for warning in detail['warnings']:
                print(f"         • {warning}")
                
        if detail['suggestions']:
            print(f"      💡 Suggestions:")
            for suggestion in detail['suggestions']:
                print(f"         • {suggestion}")
        
        if not detail['errors'] and not detail['warnings']:
            print(f"      ✅ Validation: Passed")

if __name__ == '__main__':
    simulate_validation_command()