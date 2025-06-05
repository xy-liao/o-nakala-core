#!/usr/bin/env python3
"""
Simple Nakala Curator Demonstration

This demonstrates the key curator features with mock data to show you 
how each command works, since the OpenAPI client needs some fixes.
"""

import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nakala_client.curator import (
    CuratorConfig, 
    NakalaCuratorClient, 
    NakalaMetadataValidator,
    NakalaDuplicateDetector,
    BatchModificationResult
)

def demo_quality_report():
    """Demonstrate quality report generation."""
    print("🔍 STEP 1: Quality Report Generation")
    print("=" * 50)
    
    config = CuratorConfig(
        api_key="aae99aba-476e-4ff2-2886-0aaf1bfa6fd2",
        api_url="https://apitest.nakala.fr"
    )
    
    # Mock data to demonstrate validation
    sample_items = [
        {
            'id': 'data-001',
            'title': 'Complete Dataset with Good Metadata',
            'creator': 'John Smith',
            'description': 'This is a well-documented dataset with complete metadata information including proper descriptions and keywords.',
            'keywords': 'research, data analysis, academic',
            'language': 'en',
            'license': 'CC-BY-4.0'
        },
        {
            'id': 'data-002',
            'title': 'Incomplete Dataset',
            'creator': '',  # Missing creator
            'description': 'Short desc',  # Too short
            'keywords': '',
            'language': 'fr',
            'license': 'CC-BY-4.0'
        },
        {
            'id': 'data-003',
            'title': 'Poor Quality Metadata',
            'creator': 'Jane Doe',
            'description': '',  # Missing description
            'keywords': 'test',
            'language': 'unknown',  # Invalid language
            'license': 'custom-license'  # Non-standard license
        }
    ]
    
    # Initialize validator
    validator = NakalaMetadataValidator(config)
    
    print(f"📊 Analyzing {len(sample_items)} sample items...")
    
    # Validate each item
    validation_results = []
    for item in sample_items:
        validation = validator.validate_metadata_quality(item)
        validation_results.append({
            'id': item['id'],
            'title': item['title'][:40] + '...' if len(item['title']) > 40 else item['title'],
            'errors': validation['errors'],
            'warnings': validation['warnings'],
            'suggestions': validation['suggestions']
        })
    
    # Calculate quality metrics
    total_items = len(sample_items)
    items_with_errors = sum(1 for r in validation_results if r['errors'])
    items_with_warnings = sum(1 for r in validation_results if r['warnings'])
    valid_items = total_items - items_with_errors
    quality_score = (valid_items / total_items) * 100
    
    # Display results
    print(f"📈 Quality Report Summary:")
    print(f"   Total items: {total_items}")
    print(f"   Valid items: {valid_items}")
    print(f"   Items with errors: {items_with_errors}")
    print(f"   Items with warnings: {items_with_warnings}")
    print(f"   Overall quality score: {quality_score:.1f}%")
    
    print(f"\n📋 Detailed Results:")
    for result in validation_results:
        print(f"\n   📄 {result['title']}")
        print(f"      ID: {result['id']}")
        if result['errors']:
            print(f"      ❌ Errors: {'; '.join(result['errors'])}")
        if result['warnings']:
            print(f"      ⚠️  Warnings: {'; '.join(result['warnings'])}")
        if result['suggestions']:
            print(f"      💡 Suggestions: {'; '.join(result['suggestions'])}")
        if not result['errors'] and not result['warnings']:
            print(f"      ✅ Metadata quality: Good")
    
    return validation_results

def demo_duplicate_detection():
    """Demonstrate duplicate detection."""
    print(f"\n🔍 STEP 2: Duplicate Detection")
    print("=" * 50)
    
    config = CuratorConfig(
        api_key="aae99aba-476e-4ff2-2886-0aaf1bfa6fd2",
        duplicate_threshold=0.7  # Lower threshold for demo
    )
    
    # Sample items with potential duplicates
    sample_items = [
        {
            'id': 'data-001',
            'title': 'Climate Change Research Dataset 2023',
            'description': 'Comprehensive analysis of temperature variations and precipitation patterns across Europe'
        },
        {
            'id': 'data-002', 
            'title': 'European Climate Research Data 2023',
            'description': 'Analysis of temperature variations and precipitation patterns in European regions'
        },
        {
            'id': 'data-003',
            'title': 'Historical Music Archive',
            'description': 'Collection of baroque music compositions from the 18th century'
        },
        {
            'id': 'data-004',
            'title': 'Climate Change Temperature Data',
            'description': 'Temperature and precipitation analysis for European climate research'
        }
    ]
    
    detector = NakalaDuplicateDetector(config)
    duplicates = detector.find_duplicates(sample_items)
    
    print(f"🔍 Analyzed {len(sample_items)} items for duplicates")
    print(f"🔗 Found {len(duplicates)} potential duplicate pairs")
    
    if duplicates:
        print(f"\n📋 Duplicate Pairs:")
        for i, (item1, item2, similarity) in enumerate(duplicates, 1):
            print(f"\n   {i}. Similarity: {similarity:.1%}")
            print(f"      📄 Item 1: {item1['title']} ({item1['id']})")
            print(f"      📄 Item 2: {item2['title']} ({item2['id']})")
            print(f"      🔍 Recommendation: Review for potential merge or deduplication")
    else:
        print("   ✅ No duplicates found above threshold")

def demo_batch_modifications():
    """Demonstrate batch modification capabilities."""
    print(f"\n🔄 STEP 3: Batch Modifications (Dry Run)")
    print("=" * 50)
    
    config = CuratorConfig(
        api_key="aae99aba-476e-4ff2-2886-0aaf1bfa6fd2",
        batch_size=10,
        dry_run_default=True
    )
    
    # Sample modifications
    modifications = [
        {
            'id': 'data-001',
            'changes': {
                'title': 'Updated Climate Change Research Dataset 2023',
                'description': 'Enhanced comprehensive analysis of temperature variations and precipitation patterns across Europe with additional metadata'
            },
            'current_metadata': {
                'title': 'Climate Change Research Dataset 2023',
                'description': 'Comprehensive analysis of temperature variations',
                'creator': 'Research Team'
            }
        },
        {
            'id': 'data-002',
            'changes': {
                'keywords': 'climate, research, Europe, temperature, precipitation',
                'license': 'CC-BY-4.0'
            },
            'current_metadata': {
                'title': 'European Climate Research Data 2023',
                'creator': 'Jane Smith',
                'description': 'Analysis of temperature variations'
            }
        },
        {
            'id': 'data-003',
            'changes': {
                'description': 'Comprehensive collection of baroque music compositions from the 18th century, digitized and catalogued for academic research'
            },
            'current_metadata': {
                'title': 'Historical Music Archive',
                'creator': 'Music Department',
                'description': 'Collection of baroque music'
            }
        }
    ]
    
    # Create curator and process modifications
    curator = NakalaCuratorClient(config)
    result = curator.batch_modify_metadata(modifications, dry_run=True)
    
    # Display results
    summary = result.get_summary()
    print(f"📊 Batch Modification Results (DRY RUN):")
    print(f"   Total processed: {summary['total_processed']}")
    print(f"   Would succeed: {summary['successful']}")
    print(f"   Would fail: {summary['failed']}")
    print(f"   Would skip: {summary['skipped']}")
    print(f"   Success rate: {summary['success_rate']:.1f}%")
    
    if result.successful:
        print(f"\n✅ Successful Modifications:")
        for success in result.successful[:3]:  # Show first 3
            print(f"   📄 {success['id']}: {list(success['changes'].keys())}")
    
    if result.failed:
        print(f"\n❌ Failed Modifications:")
        for failure in result.failed:
            print(f"   📄 {failure['id']}: {failure['error']}")

def demo_template_export():
    """Demonstrate template export."""
    print(f"\n📄 STEP 4: Export Modification Template")
    print("=" * 50)
    
    config = CuratorConfig(api_key="aae99aba-476e-4ff2-2886-0aaf1bfa6fd2")
    
    # Sample items for template
    sample_items = [
        {
            'id': 'data-001',
            'title': 'Dataset Title 1',
            'description': 'Current description 1',
            'keywords': 'keyword1, keyword2',
            'license': 'CC-BY-4.0',
            'language': 'en'
        },
        {
            'id': 'data-002', 
            'title': 'Dataset Title 2',
            'description': 'Current description 2',
            'keywords': 'keyword3, keyword4',
            'license': 'CC-BY-SA-4.0',
            'language': 'fr'
        }
    ]
    
    curator = NakalaCuratorClient(config)
    template_path = "sample_modifications_template.csv"
    
    curator.export_modifications_template(sample_items, template_path)
    
    print(f"📄 Template exported to: {template_path}")
    print(f"📋 Template contains {len(sample_items)} items ready for modification")
    print(f"💡 Edit this file and use with --batch-modify command")
    
    # Show a sample of what the template looks like
    print(f"\n📖 Template Preview (first few columns):")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:3]  # Header + 2 data rows
            for i, line in enumerate(lines):
                cols = line.strip().split(',')[:5]  # Show first 5 columns
                if i == 0:
                    print(f"   Header: {', '.join(cols)}...")
                else:
                    print(f"   Row {i}: {', '.join(cols)}...")
    except Exception as e:
        print(f"   Could not preview template: {e}")

def main():
    """Run all curator demonstrations."""
    print("🛠️  Nakala Curator - Full Demonstration")
    print("🔑 Using API Key: aae99aba-476e-4ff2-2886-0aaf1bfa6fd2")
    print("🌐 Target API: https://apitest.nakala.fr")
    print("=" * 70)
    
    try:
        # Step 1: Quality Report
        demo_quality_report()
        
        # Step 2: Duplicate Detection  
        demo_duplicate_detection()
        
        # Step 3: Batch Modifications
        demo_batch_modifications()
        
        # Step 4: Template Export
        demo_template_export()
        
        print(f"\n✅ All curator demonstrations completed successfully!")
        print(f"\n🎯 Next Steps:")
        print(f"   • Use ./nakala-curator.py --quality-report for real data")
        print(f"   • Edit the generated CSV template for batch modifications")
        print(f"   • Always test with --dry-run before applying changes")
        print(f"   • Check the exported template: sample_modifications_template.csv")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())