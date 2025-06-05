#!/usr/bin/env python3
"""
Example usage of the Nakala Curator Client

This example demonstrates the main features of the curator architecture:
- User information retrieval
- Metadata validation
- Quality reporting
- Batch modification preparation

Requirements:
- NAKALA_API_KEY environment variable set
- Valid Nakala API access
"""

import os
import sys
import json
from pathlib import Path

# Add the src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from nakala_client import (
    NakalaUserInfoClient,
    NakalaCuratorClient,
    CuratorConfig,
    NakalaConfig
)

def main():
    """Demonstrate curator functionality."""
    
    # Check for API key
    api_key = os.getenv('NAKALA_API_KEY')
    if not api_key:
        print("Please set NAKALA_API_KEY environment variable")
        return 1
    
    print("🔍 Nakala Curator Example")
    print("=" * 50)
    
    try:
        # Create configuration
        config = CuratorConfig(
            api_url='https://apitest.nakala.fr',
            api_key=api_key,
            batch_size=10,
            dry_run_default=True
        )
        
        if not config.validate():
            print("❌ Configuration validation failed")
            return 1
        
        print("✅ Configuration validated")
        
        # 1. Get user information
        print("\n📊 Retrieving user information...")
        user_client = NakalaUserInfoClient(config)
        
        try:
            user_info = user_client.get_user_info()
            print(f"   User: {user_info.get('firstname', '')} {user_info.get('lastname', '')}")
            print(f"   Email: {user_info.get('email', '')}")
            print(f"   Institution: {user_info.get('institution', 'N/A')}")
        except Exception as e:
            print(f"   ⚠️  Could not retrieve user info: {e}")
        
        # 2. Get collections and datasets summary
        print("\n📚 Retrieving collections and datasets...")
        try:
            collections = user_client.get_user_collections()
            datasets = user_client.get_user_datasets()
            
            print(f"   Collections: {len(collections)}")
            print(f"   Datasets: {len(datasets)}")
            
            if collections:
                print("   Recent collections:")
                for col in collections[:3]:
                    print(f"     - {col.get('title', 'Untitled')} ({col.get('status', 'unknown')})")
            
            if datasets:
                print("   Recent datasets:")
                for ds in datasets[:3]:
                    print(f"     - {ds.get('title', 'Untitled')} ({ds.get('status', 'unknown')})")
        
        except Exception as e:
            print(f"   ⚠️  Could not retrieve collections/datasets: {e}")
            collections, datasets = [], []
        
        # 3. Create curator client and demonstrate features
        print("\n🛠️  Initializing curator client...")
        curator = NakalaCuratorClient(config)
        
        # 4. Metadata validation example
        if collections or datasets:
            print("\n🔍 Validating metadata quality...")
            all_items = collections + datasets
            
            if all_items:
                validation_result = curator.batch_validate_metadata(all_items[:5])  # Limit for example
                
                print(f"   Total items validated: {validation_result['total_items']}")
                print(f"   Valid items: {validation_result['valid_items']}")
                print(f"   Items with errors: {validation_result['items_with_errors']}")
                print(f"   Items with warnings: {validation_result['items_with_warnings']}")
                
                # Show some validation details
                if validation_result['validation_details']:
                    print("\n   Sample validation results:")
                    for detail in validation_result['validation_details'][:2]:
                        print(f"     📄 {detail['title'][:50]}...")
                        if detail['errors']:
                            print(f"        ❌ Errors: {', '.join(detail['errors'][:2])}")
                        if detail['warnings']:
                            print(f"        ⚠️  Warnings: {', '.join(detail['warnings'][:2])}")
        
        # 5. Quality report example
        print("\n📈 Generating quality report...")
        try:
            quality_report = curator.generate_quality_report()
            
            print(f"   Overall quality score: {quality_report['overall_quality_score']:.1f}%")
            
            if quality_report['recommendations']:
                print("   Recommendations:")
                for rec in quality_report['recommendations'][:3]:
                    print(f"     • {rec}")
            else:
                print("   ✅ No major issues found!")
        
        except Exception as e:
            print(f"   ⚠️  Could not generate quality report: {e}")
        
        # 6. Template export example
        if collections or datasets:
            print("\n📄 Exporting modification template...")
            template_path = "modification_template_example.csv"
            
            try:
                sample_items = (collections + datasets)[:5]
                curator.export_modifications_template(sample_items, template_path)
                print(f"   ✅ Template exported to: {template_path}")
                print(f"   You can edit this file and use it with --batch-modify")
            except Exception as e:
                print(f"   ⚠️  Could not export template: {e}")
        
        # 7. Batch modification simulation
        print("\n🔄 Demonstrating batch modification (dry run)...")
        sample_modifications = [
            {
                'id': 'example-id-1',
                'changes': {
                    'title': 'Updated Title Example',
                    'description': 'Updated description for demonstration'
                },
                'current_metadata': {
                    'title': 'Original Title',
                    'description': 'Original description',
                    'creator': 'Example Creator'
                }
            }
        ]
        
        try:
            result = curator.batch_modify_metadata(sample_modifications, dry_run=True)
            summary = result.get_summary()
            
            print(f"   Dry run completed:")
            print(f"     Total processed: {summary['total_processed']}")
            print(f"     Would succeed: {summary['successful']}")
            print(f"     Would fail: {summary['failed']}")
            print(f"     Success rate: {summary['success_rate']:.1f}%")
        
        except Exception as e:
            print(f"   ⚠️  Batch modification simulation failed: {e}")
        
        print("\n✅ Curator example completed successfully!")
        print("\nNext steps:")
        print("  • Use ./nakala-user-info.py to get detailed user information")
        print("  • Use ./nakala-curator.py --quality-report for comprehensive analysis")
        print("  • Use ./nakala-curator.py --export-template for batch modifications")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())