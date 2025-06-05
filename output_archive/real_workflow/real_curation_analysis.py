#!/usr/bin/env python3
"""
Real Curation Analysis Script

Performs comprehensive curation analysis on live NAKALA datasets and collections.
"""

import os
import json
import requests
from datetime import datetime

# Live dataset and collection IDs from our real workflow
DATASETS = [
    "10.34847/nkl.9626xmez",  # Image Collection
    "10.34847/nkl.a1fd48xw",  # Code Files
    "10.34847/nkl.2d5ct4ug",  # Presentation Materials
    "10.34847/nkl.ffe86j1z",  # Research Documents
    "10.34847/nkl.b4815a9y"   # Research Data
]

COLLECTIONS = [
    "10.34847/nkl.948e1iey",  # Code and Data Collection
    "10.34847/nkl.d1fe9i5v",  # Documents Collection
    "10.34847/nkl.e3db4y09"   # Multimedia Collection
]

def get_api_key():
    """Get API key from environment file."""
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('NAKALA_API_KEY='):
                return line.split('=', 1)[1].strip()
    return None

def analyze_dataset_metadata(dataset_id, api_key):
    """Analyze metadata quality for a dataset."""
    url = f"https://apitest.nakala.fr/datas/{dataset_id}"
    headers = {'X-API-KEY': api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract metadata
        metas = data.get('metas', [])
        files = data.get('files', [])
        
        # Analyze metadata quality
        titles = [m for m in metas if 'title' in m.get('propertyUri', '')]
        descriptions = [m for m in metas if 'description' in m.get('propertyUri', '')]
        subjects = [m for m in metas if 'subject' in m.get('propertyUri', '')]
        
        quality_score = 0
        quality_details = []
        
        # Title quality (25 points)
        if titles:
            multilingual_titles = len(set(m.get('lang') for m in titles if m.get('lang')))
            if multilingual_titles >= 2:
                quality_score += 25
                quality_details.append("✅ Multilingual titles present")
            else:
                quality_score += 15
                quality_details.append("⚠️  Single language title")
        else:
            quality_details.append("❌ No title found")
        
        # Description quality (25 points)
        if descriptions:
            multilingual_desc = len(set(m.get('lang') for m in descriptions if m.get('lang')))
            avg_desc_length = sum(len(m.get('value', '')) for m in descriptions) / len(descriptions)
            if multilingual_desc >= 2 and avg_desc_length > 50:
                quality_score += 25
                quality_details.append("✅ Comprehensive multilingual descriptions")
            elif avg_desc_length > 30:
                quality_score += 15
                quality_details.append("⚠️  Adequate descriptions")
            else:
                quality_score += 5
                quality_details.append("⚠️  Brief descriptions")
        else:
            quality_details.append("❌ No descriptions found")
        
        # Subject/Keywords quality (25 points)
        if subjects:
            multilingual_subjects = len(set(m.get('lang') for m in subjects if m.get('lang')))
            total_subjects = len(subjects)
            if multilingual_subjects >= 2 and total_subjects >= 6:
                quality_score += 25
                quality_details.append("✅ Rich multilingual keywords")
            elif total_subjects >= 3:
                quality_score += 15
                quality_details.append("⚠️  Adequate keywords")
            else:
                quality_score += 5
                quality_details.append("⚠️  Few keywords")
        else:
            quality_details.append("❌ No keywords found")
        
        # File completeness (25 points)
        if files:
            file_count = len(files)
            file_types = len(set(f.get('extension', '').lower() for f in files))
            if file_count >= 3 and file_types >= 2:
                quality_score += 25
                quality_details.append("✅ Diverse file collection")
            elif file_count >= 2:
                quality_score += 15
                quality_details.append("⚠️  Multiple files")
            else:
                quality_score += 10
                quality_details.append("⚠️  Single file")
        else:
            quality_details.append("❌ No files found")
        
        return {
            'id': dataset_id,
            'title': next((m.get('value') for m in titles if m.get('lang') == 'fr'), 'Unknown'),
            'quality_score': quality_score,
            'quality_details': quality_details,
            'file_count': len(files),
            'metadata_count': len(metas),
            'multilingual_support': len(set(m.get('lang') for m in metas if m.get('lang'))),
            'status': data.get('status'),
            'created_date': data.get('creDate')
        }
        
    except Exception as e:
        return {
            'id': dataset_id,
            'error': str(e),
            'quality_score': 0
        }

def analyze_collection_structure(collection_id, api_key):
    """Analyze collection structure and data organization."""
    url = f"https://apitest.nakala.fr/collections/{collection_id}"
    headers = {'X-API-KEY': api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        collection_data = response.json()
        
        # Get collection items
        items_url = f"https://apitest.nakala.fr/collections/{collection_id}/datas"
        items_response = requests.get(items_url, headers=headers, timeout=30)
        items_response.raise_for_status()
        items_data = items_response.json()
        
        items = items_data.get('data', [])
        metas = collection_data.get('metas', [])
        
        # Analyze collection quality
        titles = [m for m in metas if 'title' in m.get('propertyUri', '')]
        descriptions = [m for m in metas if 'description' in m.get('propertyUri', '')]
        
        collection_quality = {
            'id': collection_id,
            'title': next((m.get('value') for m in titles if m.get('lang') == 'fr'), 'Unknown'),
            'item_count': len(items),
            'metadata_completeness': len(metas),
            'multilingual_titles': len([m for m in titles if m.get('lang') in ['fr', 'en']]),
            'multilingual_descriptions': len([m for m in descriptions if m.get('lang') in ['fr', 'en']]),
            'status': collection_data.get('status'),
            'created_date': collection_data.get('creDate'),
            'items': [item.get('identifier') for item in items]
        }
        
        return collection_quality
        
    except Exception as e:
        return {
            'id': collection_id,
            'error': str(e)
        }

def main():
    """Perform comprehensive real curation analysis."""
    api_key = get_api_key()
    if not api_key:
        print("❌ No API key found in .env file")
        return
    
    print("🔍 Starting Real Curation Analysis...")
    print("=" * 60)
    
    # Analyze datasets
    print("\n📊 Dataset Quality Analysis:")
    print("-" * 40)
    
    dataset_results = []
    total_quality_score = 0
    
    for dataset_id in DATASETS:
        print(f"\nAnalyzing {dataset_id}...")
        result = analyze_dataset_metadata(dataset_id, api_key)
        dataset_results.append(result)
        
        if 'error' not in result:
            print(f"  📋 Title: {result['title']}")
            print(f"  🎯 Quality Score: {result['quality_score']}/100")
            print(f"  📁 Files: {result['file_count']}")
            print(f"  🌐 Languages: {result['multilingual_support']}")
            print("  📝 Quality Details:")
            for detail in result['quality_details']:
                print(f"    {detail}")
            total_quality_score += result['quality_score']
        else:
            print(f"  ❌ Error: {result['error']}")
    
    # Analyze collections
    print("\n🗂️  Collection Structure Analysis:")
    print("-" * 40)
    
    collection_results = []
    
    for collection_id in COLLECTIONS:
        print(f"\nAnalyzing {collection_id}...")
        result = analyze_collection_structure(collection_id, api_key)
        collection_results.append(result)
        
        if 'error' not in result:
            print(f"  📋 Title: {result['title']}")
            print(f"  📊 Items: {result['item_count']}")
            print(f"  🌐 Multilingual Titles: {result['multilingual_titles']}")
            print(f"  📝 Multilingual Descriptions: {result['multilingual_descriptions']}")
            print(f"  📂 Status: {result['status']}")
        else:
            print(f"  ❌ Error: {result['error']}")
    
    # Generate summary
    print("\n📈 Curation Summary:")
    print("-" * 40)
    
    successful_datasets = [r for r in dataset_results if 'error' not in r]
    successful_collections = [r for r in collection_results if 'error' not in r]
    
    if successful_datasets:
        avg_quality = total_quality_score / len(successful_datasets)
        print(f"  📊 Average Dataset Quality: {avg_quality:.1f}/100")
        print(f"  ✅ Datasets Analyzed: {len(successful_datasets)}/{len(DATASETS)}")
        print(f"  📁 Total Files: {sum(r['file_count'] for r in successful_datasets)}")
        print(f"  🌐 Multilingual Support: {all(r['multilingual_support'] >= 2 for r in successful_datasets)}")
    
    if successful_collections:
        total_items = sum(r['item_count'] for r in successful_collections)
        print(f"  🗂️  Collections Analyzed: {len(successful_collections)}/{len(COLLECTIONS)}")
        print(f"  📊 Total Collection Items: {total_items}")
        print(f"  🌐 All Multilingual: {all(r['multilingual_titles'] >= 2 for r in successful_collections)}")
    
    # Save detailed results
    full_results = {
        'analysis_date': datetime.now().isoformat(),
        'summary': {
            'average_dataset_quality': avg_quality if successful_datasets else 0,
            'datasets_analyzed': len(successful_datasets),
            'collections_analyzed': len(successful_collections),
            'total_files': sum(r['file_count'] for r in successful_datasets) if successful_datasets else 0,
            'multilingual_coverage': all(r['multilingual_support'] >= 2 for r in successful_datasets) if successful_datasets else False
        },
        'dataset_analysis': dataset_results,
        'collection_analysis': collection_results
    }
    
    output_file = 'real_comprehensive_curation_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(full_results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    print("\n🎉 Real Curation Analysis Complete!")

if __name__ == '__main__':
    main()