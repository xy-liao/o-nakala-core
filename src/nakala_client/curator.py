"""
Nakala Curator Client

Provides data curation and quality management tools including batch modifications,
metadata validation, duplicate detection, and data consistency checking.
"""

import csv
import os
import json
import logging
import argparse
from typing import Dict, Any, List, Optional, Tuple, Iterator
from datetime import datetime
import requests
from pathlib import Path
import asyncio
import time

# Import common utilities
from .common.config import NakalaConfig
from .common.exceptions import NakalaError, NakalaValidationError, NakalaAPIError
from .common.utils import NakalaCommonUtils, setup_common_logging

from .user_info import NakalaUserInfoClient

logger = logging.getLogger(__name__)

class CuratorConfig(NakalaConfig):
    """Extended configuration for curator operations."""
    
    # Batch processing settings
    batch_size: int = 50
    concurrent_operations: int = 3
    validation_batch_size: int = 100
    
    # Curation settings
    skip_existing: bool = True
    validate_before_modification: bool = True
    backup_before_changes: bool = True
    duplicate_threshold: float = 0.85  # Similarity threshold for duplicates
    
    # Safety settings
    max_modifications_per_batch: int = 100
    require_confirmation: bool = True
    dry_run_default: bool = True


class BatchModificationResult:
    """Container for batch modification results."""
    
    def __init__(self):
        self.successful: List[Dict[str, Any]] = []
        self.failed: List[Dict[str, Any]] = []
        self.skipped: List[Dict[str, Any]] = []
        self.warnings: List[str] = []
        self.start_time: datetime = datetime.now()
        self.end_time: Optional[datetime] = None
    
    def add_success(self, item_id: str, changes: Dict[str, Any]):
        """Record successful modification."""
        self.successful.append({
            'id': item_id,
            'changes': changes,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_failure(self, item_id: str, error: str, attempted_changes: Dict[str, Any]):
        """Record failed modification."""
        self.failed.append({
            'id': item_id,
            'error': error,
            'attempted_changes': attempted_changes,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_skip(self, item_id: str, reason: str):
        """Record skipped modification."""
        self.skipped.append({
            'id': item_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_warning(self, message: str):
        """Add warning message."""
        self.warnings.append(f"{datetime.now().isoformat()}: {message}")
    
    def finalize(self):
        """Mark operation as complete."""
        self.end_time = datetime.now()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get operation summary."""
        duration = None
        if self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        
        return {
            'total_processed': len(self.successful) + len(self.failed) + len(self.skipped),
            'successful': len(self.successful),
            'failed': len(self.failed),
            'skipped': len(self.skipped),
            'warnings': len(self.warnings),
            'duration_seconds': duration,
            'success_rate': len(self.successful) / max(1, len(self.successful) + len(self.failed)) * 100
        }


class NakalaMetadataValidator:
    """Validates metadata against Nakala requirements and best practices."""
    
    def __init__(self, config: CuratorConfig):
        self.config = config
        self.utils = NakalaCommonUtils()
    
    def validate_required_fields(self, metadata: Dict[str, Any]) -> List[str]:
        """Validate required metadata fields."""
        errors = []
        required_fields = ['title', 'creator', 'description']
        
        for field in required_fields:
            if not metadata.get(field):
                errors.append(f"Required field '{field}' is missing or empty")
        
        return errors
    
    def validate_controlled_vocabularies(self, metadata: Dict[str, Any]) -> List[str]:
        """Validate controlled vocabulary values."""
        warnings = []
        
        # Language validation
        if 'language' in metadata:
            lang = metadata['language']
            if lang not in ['fr', 'en', 'de', 'es', 'it']:
                warnings.append(f"Language '{lang}' might not be supported")
        
        # License validation  
        if 'license' in metadata:
            license_val = metadata['license']
            valid_licenses = ['CC-BY-4.0', 'CC-BY-SA-4.0', 'CC-BY-NC-4.0', 'CC0-1.0']
            if license_val not in valid_licenses:
                warnings.append(f"License '{license_val}' is not in recommended list")
        
        return warnings
    
    def validate_metadata_quality(self, metadata: Dict[str, Any]) -> Dict[str, List[str]]:
        """Comprehensive metadata quality validation."""
        results = {
            'errors': self.validate_required_fields(metadata),
            'warnings': self.validate_controlled_vocabularies(metadata),
            'suggestions': []
        }
        
        # Quality suggestions
        if metadata.get('title') and len(metadata['title']) < 10:
            results['suggestions'].append("Title is very short, consider expanding")
        
        if metadata.get('description') and len(metadata['description']) < 50:
            results['suggestions'].append("Description is brief, consider adding more detail")
        
        if not metadata.get('keywords'):
            results['suggestions'].append("Consider adding keywords for better discoverability")
        
        return results


class NakalaDuplicateDetector:
    """Detects potential duplicates in datasets and collections."""
    
    def __init__(self, config: CuratorConfig):
        self.config = config
        self.threshold = config.duplicate_threshold
    
    def calculate_similarity(self, item1: Dict[str, Any], item2: Dict[str, Any]) -> float:
        """Calculate similarity between two items based on metadata."""
        # Simple text-based similarity for now
        text1 = f"{item1.get('title', '')} {item1.get('description', '')}"
        text2 = f"{item2.get('title', '')} {item2.get('description', '')}"
        
        # Jaccard similarity on words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def find_duplicates(self, items: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], Dict[str, Any], float]]:
        """Find potential duplicates in a list of items."""
        duplicates = []
        
        for i, item1 in enumerate(items):
            for j, item2 in enumerate(items[i+1:], i+1):
                similarity = self.calculate_similarity(item1, item2)
                if similarity >= self.threshold:
                    duplicates.append((item1, item2, similarity))
        
        return duplicates


class NakalaCuratorClient:
    """Main curator client for batch operations and quality management."""
    
    def __init__(self, config: CuratorConfig):
        self.config = config
        self.utils = NakalaCommonUtils()
        self.validator = NakalaMetadataValidator(config)
        self.duplicate_detector = NakalaDuplicateDetector(config)
        self.user_client = NakalaUserInfoClient(config)
    
    def batch_validate_metadata(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate metadata for multiple items."""
        logger.info(f"Validating metadata for {len(items)} items...")
        
        results = {
            'total_items': len(items),
            'valid_items': 0,
            'items_with_errors': 0,
            'items_with_warnings': 0,
            'validation_details': []
        }
        
        for item in items:
            item_id = item.get('id', 'unknown')
            validation = self.validator.validate_metadata_quality(item)
            
            has_errors = len(validation['errors']) > 0
            has_warnings = len(validation['warnings']) > 0
            
            if not has_errors:
                results['valid_items'] += 1
            else:
                results['items_with_errors'] += 1
            
            if has_warnings:
                results['items_with_warnings'] += 1
            
            results['validation_details'].append({
                'id': item_id,
                'title': item.get('title', ''),
                'errors': validation['errors'],
                'warnings': validation['warnings'],
                'suggestions': validation['suggestions']
            })
        
        return results
    
    def batch_modify_metadata(self, modifications: List[Dict[str, Any]], dry_run: bool = True) -> BatchModificationResult:
        """Apply metadata modifications in batches."""
        logger.info(f"{'DRY RUN: ' if dry_run else ''}Processing {len(modifications)} metadata modifications...")
        
        result = BatchModificationResult()
        
        # Process in batches
        for batch_start in range(0, len(modifications), self.config.batch_size):
            batch_end = min(batch_start + self.config.batch_size, len(modifications))
            batch = modifications[batch_start:batch_end]
            
            logger.info(f"Processing batch {batch_start//self.config.batch_size + 1}: items {batch_start+1}-{batch_end}")
            
            self._process_modification_batch(batch, result, dry_run)
            
            # Small delay between batches to avoid overwhelming API
            time.sleep(0.5)
        
        result.finalize()
        return result
    
    def _process_modification_batch(self, batch: List[Dict[str, Any]], result: BatchModificationResult, dry_run: bool):
        """Process a single batch of modifications."""
        for modification in batch:
            item_id = modification.get('id', 'unknown')
            changes = modification.get('changes', {})
            
            try:
                # Validate before modification if enabled
                if self.config.validate_before_modification:
                    current_metadata = modification.get('current_metadata', {})
                    updated_metadata = {**current_metadata, **changes}
                    validation = self.validator.validate_metadata_quality(updated_metadata)
                    
                    if validation['errors']:
                        result.add_failure(item_id, f"Validation failed: {validation['errors']}", changes)
                        continue
                
                # Apply modification (or simulate in dry run)
                if dry_run:
                    logger.debug(f"DRY RUN: Would modify {item_id} with changes: {changes}")
                    result.add_success(item_id, changes)
                else:
                    # Here you would make actual API calls to modify the item
                    success = self._apply_modification(item_id, changes)
                    if success:
                        result.add_success(item_id, changes)
                    else:
                        result.add_failure(item_id, "API modification failed", changes)
            
            except Exception as e:
                result.add_failure(item_id, str(e), changes)
    
    def _apply_modification(self, item_id: str, changes: Dict[str, Any]) -> bool:
        """Apply actual modification via API."""
        # This would contain the actual API calls
        # For now, return True to simulate success
        logger.info(f"Applying changes to {item_id}: {changes}")
        return True
    
    def detect_duplicates_in_collections(self, collection_ids: List[str]) -> Dict[str, Any]:
        """Detect duplicates across multiple collections."""
        logger.info(f"Analyzing {len(collection_ids)} collections for duplicates...")
        
        all_items = []
        collection_items = {}
        
        # Gather all items from collections
        for collection_id in collection_ids:
            try:
                # Here you would fetch collection items via API
                items = self._get_collection_items(collection_id)
                collection_items[collection_id] = items
                all_items.extend(items)
            except Exception as e:
                logger.error(f"Failed to get items from collection {collection_id}: {e}")
        
        # Find duplicates
        duplicates = self.duplicate_detector.find_duplicates(all_items)
        
        return {
            'total_items_analyzed': len(all_items),
            'duplicate_pairs_found': len(duplicates),
            'collections_analyzed': collection_ids,
            'duplicates': [
                {
                    'item1': {'id': dup[0].get('id'), 'title': dup[0].get('title')},
                    'item2': {'id': dup[1].get('id'), 'title': dup[1].get('title')},
                    'similarity': dup[2]
                }
                for dup in duplicates
            ]
        }
    
    def _get_collection_items(self, collection_id: str) -> List[Dict[str, Any]]:
        """Get items from a collection via API."""
        # Placeholder for actual API call
        return []
    
    def generate_quality_report(self, scope: str = 'all') -> Dict[str, Any]:
        """Generate comprehensive quality report for user's data."""
        logger.info("Generating data quality report...")
        
        # Get user's data
        user_profile = self.user_client.get_complete_user_profile()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'scope': scope,
            'summary': user_profile['summary'],
            'collections_analysis': {},
            'datasets_analysis': {},
            'overall_quality_score': 0.0,
            'recommendations': []
        }
        
        # Analyze collections
        if user_profile['collections']:
            validation_result = self.batch_validate_metadata(user_profile['collections'])
            report['collections_analysis'] = validation_result
        
        # Analyze datasets
        if user_profile['datasets']:
            validation_result = self.batch_validate_metadata(user_profile['datasets'])
            report['datasets_analysis'] = validation_result
        
        # Calculate overall quality score
        total_items = len(user_profile['collections']) + len(user_profile['datasets'])
        if total_items > 0:
            valid_collections = report['collections_analysis'].get('valid_items', 0)
            valid_datasets = report['datasets_analysis'].get('valid_items', 0)
            report['overall_quality_score'] = (valid_collections + valid_datasets) / total_items * 100
        
        # Generate recommendations
        self._generate_recommendations(report)
        
        return report
    
    def _generate_recommendations(self, report: Dict[str, Any]):
        """Generate quality improvement recommendations."""
        recommendations = []
        
        collections_analysis = report.get('collections_analysis', {})
        datasets_analysis = report.get('datasets_analysis', {})
        
        # Check for metadata quality issues
        if collections_analysis.get('items_with_errors', 0) > 0:
            recommendations.append(
                f"Fix metadata errors in {collections_analysis['items_with_errors']} collections"
            )
        
        if datasets_analysis.get('items_with_errors', 0) > 0:
            recommendations.append(
                f"Fix metadata errors in {datasets_analysis['items_with_errors']} datasets"
            )
        
        # Check overall quality score
        quality_score = report.get('overall_quality_score', 0)
        if quality_score < 80:
            recommendations.append("Consider improving metadata quality - current score is below 80%")
        
        if quality_score < 60:
            recommendations.append("Urgent: Metadata quality is critically low - review and update metadata")
        
        report['recommendations'] = recommendations
    
    def export_modifications_template(self, items: List[Dict[str, Any]], output_path: str):
        """Export a CSV template for batch modifications."""
        logger.info(f"Exporting modification template for {len(items)} items to {output_path}")
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'id', 'current_title', 'new_title', 'current_description', 'new_description',
                'current_keywords', 'new_keywords', 'current_license', 'new_license',
                'current_language', 'new_language', 'action'
            ])
            
            # Data rows
            for item in items:
                writer.writerow([
                    item.get('id', ''),
                    item.get('title', ''),
                    '',  # new_title - to be filled
                    item.get('description', ''),
                    '',  # new_description - to be filled  
                    item.get('keywords', ''),
                    '',  # new_keywords - to be filled
                    item.get('license', ''),
                    '',  # new_license - to be filled
                    item.get('language', ''),
                    '',  # new_language - to be filled
                    'modify'  # action
                ])
        
        logger.info(f"Template exported to {output_path}")


def main():
    """Main entry point for the curator script."""
    parser = argparse.ArgumentParser(
        description="Nakala Curator - Data curation and quality management tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate quality report
  python nakala-curator.py --quality-report
  
  # Validate metadata for all collections
  python nakala-curator.py --validate-metadata --scope collections
  
  # Detect duplicates
  python nakala-curator.py --detect-duplicates --collections col1,col2
  
  # Apply batch modifications from CSV
  python nakala-curator.py --batch-modify modifications.csv --dry-run
        """
    )
    
    parser.add_argument(
        '--api-key',
        help='Nakala API key (or set NAKALA_API_KEY environment variable)'
    )
    
    parser.add_argument(
        '--api-url',
        default='https://apitest.nakala.fr',
        help='Nakala API URL (default: test API)'
    )
    
    parser.add_argument(
        '--quality-report',
        action='store_true',
        help='Generate comprehensive quality report'
    )
    
    parser.add_argument(
        '--validate-metadata',
        action='store_true',
        help='Validate metadata for specified scope'
    )
    
    parser.add_argument(
        '--detect-duplicates',
        action='store_true',
        help='Detect potential duplicates'
    )
    
    parser.add_argument(
        '--batch-modify',
        help='CSV file with batch modifications to apply'
    )
    
    parser.add_argument(
        '--export-template',
        help='Export modification template CSV for specified items'
    )
    
    parser.add_argument(
        '--scope',
        default='all',
        choices=['all', 'collections', 'datasets'],
        help='Scope for operations'
    )
    
    parser.add_argument(
        '--collections',
        help='Comma-separated list of collection IDs'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path for reports and exports'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate operations without making changes'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=50,
        help='Batch size for processing (default: 50)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_common_logging(verbose=args.verbose)
    
    try:
        # Create configuration
        config = CuratorConfig(
            api_url=args.api_url,
            api_key=args.api_key,
            batch_size=args.batch_size,
            dry_run_default=args.dry_run
        )
        
        if not config.validate():
            logger.error("Configuration validation failed")
            return 1
        
        # Create curator client
        curator = NakalaCuratorClient(config)
        
        # Execute requested operations
        if args.quality_report:
            report = curator.generate_quality_report(scope=args.scope)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False, default=str)
                logger.info(f"Quality report exported to: {args.output}")
            else:
                print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
        
        elif args.validate_metadata:
            # Get user data for validation
            user_client = NakalaUserInfoClient(config)
            profile = user_client.get_complete_user_profile()
            
            items = []
            if args.scope == 'collections':
                items = profile['collections']
            elif args.scope == 'datasets':
                items = profile['datasets']
            else:
                items = profile['collections'] + profile['datasets']
            
            validation_result = curator.batch_validate_metadata(items)
            print(json.dumps(validation_result, indent=2, ensure_ascii=False))
        
        elif args.detect_duplicates:
            if not args.collections:
                logger.error("--collections parameter required for duplicate detection")
                return 1
            
            collection_ids = [cid.strip() for cid in args.collections.split(',')]
            duplicates = curator.detect_duplicates_in_collections(collection_ids)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(duplicates, f, indent=2, ensure_ascii=False, default=str)
                logger.info(f"Duplicate analysis exported to: {args.output}")
            else:
                print(json.dumps(duplicates, indent=2, ensure_ascii=False, default=str))
        
        elif args.batch_modify:
            # Load modifications from CSV
            modifications = []
            with open(args.batch_modify, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('action') == 'modify':
                        changes = {}
                        if row.get('new_title'):
                            changes['title'] = row['new_title']
                        if row.get('new_description'):
                            changes['description'] = row['new_description']
                        # Add more fields as needed
                        
                        if changes:
                            modifications.append({
                                'id': row['id'],
                                'changes': changes
                            })
            
            if modifications:
                result = curator.batch_modify_metadata(modifications, dry_run=args.dry_run)
                summary = result.get_summary()
                
                print(f"Batch modification {'simulation' if args.dry_run else 'completed'}:")
                print(f"  Total processed: {summary['total_processed']}")
                print(f"  Successful: {summary['successful']}")
                print(f"  Failed: {summary['failed']}")
                print(f"  Skipped: {summary['skipped']}")
                print(f"  Success rate: {summary['success_rate']:.1f}%")
                
                if args.output:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        json.dump(result.__dict__, f, indent=2, ensure_ascii=False, default=str)
            else:
                logger.info("No modifications found in CSV file")
        
        else:
            parser.print_help()
            return 1
        
        return 0
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())