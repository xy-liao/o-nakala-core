#!/usr/bin/env python3
"""
Demonstrate batch modification command
"""

import csv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nakala_client.curator import CuratorConfig, NakalaCuratorClient

def simulate_batch_modify_command():
    print("🔍 Simulating: ./nakala-curator.py --batch-modify example_modifications.csv --dry-run")
    print("=" * 75)
    
    config = CuratorConfig(
        api_key="aae99aba-476e-4ff2-2886-0aaf1bfa6fd2",
        api_url="https://apitest.nakala.fr",
        batch_size=10
    )
    
    # Load modifications from CSV (simulating the --batch-modify command)
    modifications = []
    csv_file = "example_modifications.csv"
    
    print(f"📂 Loading modifications from: {csv_file}")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('action') == 'modify':
                changes = {}
                
                # Check each field for changes
                if row.get('new_title'):
                    changes['title'] = row['new_title']
                if row.get('new_description'):
                    changes['description'] = row['new_description']
                if row.get('new_keywords'):
                    changes['keywords'] = row['new_keywords']
                if row.get('new_license'):
                    changes['license'] = row['new_license']
                if row.get('new_language'):
                    changes['language'] = row['new_language']
                if row.get('creator'):
                    changes['creator'] = row['creator']
                
                if changes:
                    modifications.append({
                        'id': row['id'],
                        'changes': changes,
                        'current_metadata': {
                            'title': row.get('current_title', ''),
                            'description': row.get('current_description', ''),
                            'keywords': row.get('current_keywords', ''),
                            'license': row.get('current_license', ''),
                            'language': row.get('current_language', ''),
                            'creator': row.get('creator', '')
                        }
                    })
    
    print(f"📊 Loaded {len(modifications)} modifications from CSV")
    
    # Process with curator
    curator = NakalaCuratorClient(config)
    result = curator.batch_modify_metadata(modifications, dry_run=True)
    
    # Display results
    summary = result.get_summary()
    
    print(f"\n📈 Batch Modification Results (DRY RUN):")
    print(f"   Total processed: {summary['total_processed']}")
    print(f"   Would succeed: {summary['successful']}")
    print(f"   Would fail: {summary['failed']}")
    print(f"   Would skip: {summary['skipped']}")
    print(f"   Success rate: {summary['success_rate']:.1f}%")
    print(f"   Duration: {summary.get('duration_seconds', 'N/A')} seconds")
    
    if result.successful:
        print(f"\n✅ Successful Modifications (DRY RUN):")
        for success in result.successful:
            print(f"   📄 {success['id']}:")
            for field, value in success['changes'].items():
                preview = value[:50] + '...' if len(str(value)) > 50 else value
                print(f"      • {field}: {preview}")
    
    if result.failed:
        print(f"\n❌ Failed Modifications:")
        for failure in result.failed:
            print(f"   📄 {failure['id']}: {failure['error']}")
    
    if result.warnings:
        print(f"\n⚠️ Warnings:")
        for warning in result.warnings[:3]:  # Show first 3
            print(f"   • {warning}")
    
    print(f"\n💡 Next Steps:")
    print(f"   • Review the results above")
    print(f"   • If satisfied, remove --dry-run to apply changes")
    print(f"   • Command: ./nakala-curator.py --batch-modify example_modifications.csv")

if __name__ == '__main__':
    simulate_batch_modify_command()