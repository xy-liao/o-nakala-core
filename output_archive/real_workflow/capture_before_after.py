#!/usr/bin/env python3
"""
Before/After Curation Comparison Script

Captures metadata before curation, applies changes, captures after, and shows differences.
"""

import os
import json
import requests
from datetime import datetime

# Target datasets for curation demonstration
DATASETS = [
    "10.34847/nkl.9626xmez",  # Image Collection - will enhance
    "10.34847/nkl.a1fd48xw",  # Code Files - will enhance
]

def get_api_key():
    """Get API key from environment file."""
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('NAKALA_API_KEY='):
                return line.split('=', 1)[1].strip()
    return None

def capture_metadata_snapshot(dataset_id, api_key, label):
    """Capture current metadata state."""
    url = f"https://apitest.nakala.fr/datas/{dataset_id}"
    headers = {'X-API-KEY': api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract key metadata for comparison
        metas = data.get('metas', [])
        
        snapshot = {
            'dataset_id': dataset_id,
            'timestamp': datetime.now().isoformat(),
            'label': label,
            'status': data.get('status'),
            'metadata_fields': len(metas),
            'titles': [m for m in metas if 'title' in m.get('propertyUri', '')],
            'descriptions': [m for m in metas if 'description' in m.get('propertyUri', '')],
            'subjects': [m for m in metas if 'subject' in m.get('propertyUri', '')],
            'all_metas': metas  # Complete metadata for detailed comparison
        }
        
        return snapshot
        
    except Exception as e:
        print(f"❌ Error capturing {label} snapshot for {dataset_id}: {e}")
        return None

def apply_metadata_enhancement(dataset_id, api_key):
    """Apply actual metadata enhancements to a dataset."""
    url = f"https://apitest.nakala.fr/datas/{dataset_id}"
    headers = {'X-API-KEY': api_key}
    
    try:
        # Get current metadata
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        current_data = response.json()
        current_metas = current_data.get('metas', [])
        
        # Prepare enhanced metadata based on dataset
        enhanced_metas = []
        
        # Keep non-title, non-description, non-subject metadata unchanged
        for meta in current_metas:
            property_uri = meta.get('propertyUri', '')
            if not any(field in property_uri.lower() for field in ['title', 'description', 'subject']):
                enhanced_metas.append(meta)
        
        # Add enhanced metadata based on dataset type
        if dataset_id == "10.34847/nkl.9626xmez":  # Image Collection
            # Enhanced titles
            enhanced_metas.extend([
                {
                    'value': 'Collection d\'images scientifiques enrichies',
                    'lang': 'fr',
                    'propertyUri': 'http://nakala.fr/terms#title'
                },
                {
                    'value': 'Enhanced Scientific Image Collection',
                    'lang': 'en',
                    'propertyUri': 'http://nakala.fr/terms#title'
                }
            ])
            
            # Enhanced descriptions
            enhanced_metas.extend([
                {
                    'value': 'Collection d\'images et données visuelles pour la recherche scientifique avec analyse des tendances de température et documentation photographique des sites d\'étude',
                    'lang': 'fr',
                    'propertyUri': 'http://purl.org/dc/terms/description'
                },
                {
                    'value': 'Collection of images and visual data for scientific research including temperature trend analysis and photographic documentation of study sites',
                    'lang': 'en',
                    'propertyUri': 'http://purl.org/dc/terms/description'
                }
            ])
            
            # Enhanced keywords
            enhanced_keywords_fr = ['images', 'visuel', 'recherche', 'scientifique', 'température', 'analyse', 'photographie', 'sites']
            enhanced_keywords_en = ['images', 'visual', 'research', 'scientific', 'temperature', 'analysis', 'photography', 'sites']
            
        elif dataset_id == "10.34847/nkl.a1fd48xw":  # Code Files
            # Enhanced titles
            enhanced_metas.extend([
                {
                    'value': 'Scripts d\'analyse de données avancés',
                    'lang': 'fr',
                    'propertyUri': 'http://nakala.fr/terms#title'
                },
                {
                    'value': 'Advanced Data Analysis Scripts',
                    'lang': 'en',
                    'propertyUri': 'http://nakala.fr/terms#title'
                }
            ])
            
            # Enhanced descriptions
            enhanced_metas.extend([
                {
                    'value': 'Scripts Python et R pour l\'analyse avancée de données de recherche incluant le prétraitement, le nettoyage et les techniques d\'analyse statistique pour les études environnementales',
                    'lang': 'fr',
                    'propertyUri': 'http://purl.org/dc/terms/description'
                },
                {
                    'value': 'Python and R scripts for advanced research data analysis including preprocessing, cleaning and statistical analysis techniques for environmental studies',
                    'lang': 'en',
                    'propertyUri': 'http://purl.org/dc/terms/description'
                }
            ])
            
            # Enhanced keywords
            enhanced_keywords_fr = ['code', 'programmation', 'scripts', 'python', 'r', 'analyse', 'données', 'statistique', 'environnement']
            enhanced_keywords_en = ['code', 'programming', 'scripts', 'python', 'r', 'analysis', 'data', 'statistical', 'environment']
        
        # Add enhanced keywords
        for keyword in enhanced_keywords_fr:
            enhanced_metas.append({
                'value': keyword,
                'lang': 'fr',
                'propertyUri': 'http://purl.org/dc/terms/subject'
            })
        
        for keyword in enhanced_keywords_en:
            enhanced_metas.append({
                'value': keyword,
                'lang': 'en',
                'propertyUri': 'http://purl.org/dc/terms/subject'
            })
        
        # Apply the enhancement
        update_payload = {'metas': enhanced_metas}
        headers['Content-Type'] = 'application/json'
        
        response = requests.put(url, headers=headers, json=update_payload, timeout=30)
        response.raise_for_status()
        
        print(f"✅ Successfully enhanced metadata for {dataset_id}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to enhance {dataset_id}: {e}")
        return False

def compare_snapshots(before, after):
    """Compare before and after snapshots."""
    if not before or not after:
        return {"error": "Missing snapshot data"}
    
    comparison = {
        'dataset_id': before['dataset_id'],
        'comparison_timestamp': datetime.now().isoformat(),
        'changes_detected': False,
        'changes': {
            'titles': {'before': [], 'after': [], 'changed': False},
            'descriptions': {'before': [], 'after': [], 'changed': False},
            'subjects': {'before': [], 'after': [], 'changed': False},
            'metadata_count': {'before': before['metadata_fields'], 'after': after['metadata_fields'], 'changed': False}
        },
        'summary': {}
    }
    
    # Compare titles
    before_titles = [f"{m['lang']}: {m['value']}" for m in before['titles']]
    after_titles = [f"{m['lang']}: {m['value']}" for m in after['titles']]
    comparison['changes']['titles'] = {
        'before': before_titles,
        'after': after_titles,
        'changed': before_titles != after_titles
    }
    
    # Compare descriptions
    before_descriptions = [f"{m['lang']}: {m['value']}" for m in before['descriptions']]
    after_descriptions = [f"{m['lang']}: {m['value']}" for m in after['descriptions']]
    comparison['changes']['descriptions'] = {
        'before': before_descriptions,
        'after': after_descriptions,
        'changed': before_descriptions != after_descriptions
    }
    
    # Compare subjects/keywords
    before_subjects = [f"{m['lang']}: {m['value']}" for m in before['subjects']]
    after_subjects = [f"{m['lang']}: {m['value']}" for m in after['subjects']]
    comparison['changes']['subjects'] = {
        'before': before_subjects,
        'after': after_subjects,
        'changed': before_subjects != after_subjects
    }
    
    # Compare metadata count
    comparison['changes']['metadata_count']['changed'] = before['metadata_fields'] != after['metadata_fields']
    
    # Determine if any changes occurred
    comparison['changes_detected'] = any(
        comparison['changes'][field]['changed'] 
        for field in ['titles', 'descriptions', 'subjects', 'metadata_count']
    )
    
    # Generate summary
    if comparison['changes_detected']:
        summary_parts = []
        if comparison['changes']['titles']['changed']:
            summary_parts.append("titles updated")
        if comparison['changes']['descriptions']['changed']:
            summary_parts.append("descriptions enhanced")
        if comparison['changes']['subjects']['changed']:
            summary_parts.append("keywords enriched")
        if comparison['changes']['metadata_count']['changed']:
            count_diff = after['metadata_fields'] - before['metadata_fields']
            summary_parts.append(f"metadata fields {'increased' if count_diff > 0 else 'decreased'} by {abs(count_diff)}")
        
        comparison['summary'] = {
            'changes_applied': summary_parts,
            'enhancement_quality': 'significant' if len(summary_parts) >= 2 else 'moderate'
        }
    else:
        comparison['summary'] = {'changes_applied': ['no changes detected'], 'enhancement_quality': 'none'}
    
    return comparison

def main():
    """Execute before/after curation comparison."""
    api_key = get_api_key()
    if not api_key:
        print("❌ No API key found in .env file")
        return
    
    print("🔍 Starting Before/After Curation Comparison")
    print("=" * 60)
    
    all_comparisons = []
    
    for dataset_id in DATASETS:
        print(f"\n📋 Processing Dataset: {dataset_id}")
        print("-" * 40)
        
        # Capture BEFORE snapshot
        print("📸 Capturing BEFORE snapshot...")
        before_snapshot = capture_metadata_snapshot(dataset_id, api_key, "BEFORE")
        
        if before_snapshot:
            print(f"   ✅ Before: {before_snapshot['metadata_fields']} metadata fields")
            print(f"   📝 Titles: {len(before_snapshot['titles'])}")
            print(f"   📝 Descriptions: {len(before_snapshot['descriptions'])}")
            print(f"   🏷️  Keywords: {len(before_snapshot['subjects'])}")
        
        # Apply CURATION ENHANCEMENTS
        print("🛠️  Applying curation enhancements...")
        enhancement_success = apply_metadata_enhancement(dataset_id, api_key)
        
        if enhancement_success:
            # Small delay to ensure changes are processed
            import time
            time.sleep(2)
            
            # Capture AFTER snapshot
            print("📸 Capturing AFTER snapshot...")
            after_snapshot = capture_metadata_snapshot(dataset_id, api_key, "AFTER")
            
            if after_snapshot:
                print(f"   ✅ After: {after_snapshot['metadata_fields']} metadata fields")
                print(f"   📝 Titles: {len(after_snapshot['titles'])}")
                print(f"   📝 Descriptions: {len(after_snapshot['descriptions'])}")
                print(f"   🏷️  Keywords: {len(after_snapshot['subjects'])}")
                
                # Compare snapshots
                comparison = compare_snapshots(before_snapshot, after_snapshot)
                all_comparisons.append(comparison)
                
                # Display immediate comparison
                if comparison['changes_detected']:
                    print("   🎉 CHANGES DETECTED!")
                    for change_type, change_info in comparison['changes'].items():
                        if change_info['changed']:
                            print(f"     • {change_type.upper()}: Changed")
                else:
                    print("   ⚠️  No changes detected")
            else:
                print("   ❌ Failed to capture after snapshot")
        else:
            print("   ❌ Enhancement failed")
    
    # Save complete comparison results
    results = {
        'comparison_timestamp': datetime.now().isoformat(),
        'datasets_processed': len(DATASETS),
        'successful_enhancements': len(all_comparisons),
        'comparisons': all_comparisons
    }
    
    output_file = 'before_after_curation_comparison.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    # Generate summary report
    print("\n📊 CURATION COMPARISON SUMMARY")
    print("=" * 60)
    
    enhanced_count = sum(1 for comp in all_comparisons if comp['changes_detected'])
    print(f"📈 Datasets Enhanced: {enhanced_count}/{len(DATASETS)}")
    
    if enhanced_count > 0:
        print("\n🔄 Changes Applied:")
        for comparison in all_comparisons:
            if comparison['changes_detected']:
                dataset_id = comparison['dataset_id']
                changes = comparison['summary']['changes_applied']
                print(f"   • {dataset_id}: {', '.join(changes)}")
        
        print(f"\n💾 Detailed comparison saved to: {output_file}")
        print("🎉 Curation enhancements successfully applied and documented!")
    else:
        print("⚠️  No enhancements were applied")

if __name__ == '__main__':
    main()