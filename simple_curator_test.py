#!/usr/bin/env python3
"""
Simple curator test to validate core functionality
"""

import csv
import json
import requests
from pathlib import Path

# Configuration
API_KEY = "33170cfe-f53c-550b-5fb6-4814ce981293"
API_URL = "https://apitest.nakala.fr"

def load_modifications(csv_file):
    """Load modifications from CSV file"""
    modifications = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            modifications.append(row)
    return modifications

def get_data_item(data_id):
    """Get current metadata for a data item"""
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(f"{API_URL}/datas/{data_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to get data item {data_id}: {response.status_code}")
        return None

def update_data_item(data_id, metadata):
    """Update metadata for a data item"""
    headers = {"X-API-KEY": API_KEY, "Content-Type": "application/json"}
    payload = {"metas": metadata}
    
    response = requests.put(f"{API_URL}/datas/{data_id}", 
                           headers=headers, 
                           json=payload)
    
    if response.status_code in [200, 204]:
        return True
    else:
        print(f"❌ Failed to update {data_id}: {response.status_code} - {response.text}")
        return False

def apply_modification(mod, dry_run=True):
    """Apply a single modification"""
    data_id = mod['id']
    
    print(f"\n🔄 Processing {data_id}")
    
    # Get current metadata
    current_data = get_data_item(data_id)
    if not current_data:
        return False
        
    current_metas = current_data.get('metas', [])
    
    # Find and update keywords
    new_keywords = mod.get('new_keywords', '').strip()
    if new_keywords:
        # Remove existing subject/keywords metadata
        filtered_metas = [m for m in current_metas 
                         if 'subject' not in m.get('propertyUri', '').lower()]
        
        # Add new keywords
        for lang_value in new_keywords.split('|'):
            if ':' in lang_value:
                lang, keywords = lang_value.split(':', 1)
                for keyword in keywords.split(';'):
                    if keyword.strip():
                        filtered_metas.append({
                            "propertyUri": "http://purl.org/dc/terms/subject",
                            "value": keyword.strip(),
                            "lang": lang.strip(),
                            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
                        })
        
        current_metas = filtered_metas
    
    # Add relation if specified
    new_relation = mod.get('new_relation', '').strip()
    if new_relation:
        # Remove existing relation metadata
        current_metas = [m for m in current_metas 
                        if 'relation' not in m.get('propertyUri', '').lower()]
        
        # Add new relation
        for lang_value in new_relation.split('|'):
            if ':' in lang_value:
                lang, relation = lang_value.split(':', 1)
                current_metas.append({
                    "propertyUri": "http://purl.org/dc/terms/relation",
                    "value": relation.strip(),
                    "lang": lang.strip(),
                    "typeUri": "http://www.w3.org/2001/XMLSchema#string"
                })
    
    if dry_run:
        print(f"  🔍 DRY RUN: Would update with {len(current_metas)} metadata entries")
        if new_keywords:
            print(f"  📝 Keywords: {new_keywords[:50]}...")
        if new_relation:
            print(f"  🔗 Relation: {new_relation[:50]}...")
        return True
    else:
        # Actually apply the update
        success = update_data_item(data_id, current_metas)
        if success:
            print(f"  ✅ Successfully updated {data_id}")
        return success

def main():
    print("🎯 Simple Curator Test")
    print("=" * 50)
    
    # Load modifications
    modifications = load_modifications('test_curator_modifications.csv')
    print(f"📋 Loaded {len(modifications)} modifications")
    
    # Test with dry run first
    print("\n🔍 DRY RUN MODE")
    print("-" * 30)
    success_count = 0
    for mod in modifications:
        if apply_modification(mod, dry_run=True):
            success_count += 1
    
    print(f"\n📊 DRY RUN Results: {success_count}/{len(modifications)} successful")
    
    # Apply for real automatically for testing
    apply_for_real = True
    print("\n🚀 Proceeding with real modifications...")
    
    if apply_for_real:
        print("\n🚀 APPLYING MODIFICATIONS")
        print("-" * 30)
        real_success_count = 0
        for mod in modifications:
            if apply_modification(mod, dry_run=False):
                real_success_count += 1
        
        print(f"\n🎉 FINAL Results: {real_success_count}/{len(modifications)} successfully applied")
        
        # Save results
        with open('curator_test_results.json', 'w') as f:
            json.dump({
                'timestamp': str(Path(__file__).stat().st_mtime),
                'total_modifications': len(modifications),
                'successful_modifications': real_success_count,
                'modifications_applied': [mod['id'] for mod in modifications[:real_success_count]]
            }, f, indent=2)
        print("📄 Results saved to curator_test_results.json")
    else:
        print("❌ Modifications not applied")

if __name__ == "__main__":
    main()