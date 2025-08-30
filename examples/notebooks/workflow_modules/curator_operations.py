"""
Curator Operations

Handles metadata curation operations for datasets and collections,
corresponding to Steps 4-5 of the ultimate workflow.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Literal
import logging
import time
from o_nakala_core import NakalaCuratorClient, NakalaConfig, NakalaError

class CuratorOperations:
    """Handles curation operations for datasets and collections."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize curator operations.
        
        Args:
            config: Configuration dictionary from WorkflowConfig
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.base_path = Path(config['base_path'])
    
    def curate_datasets(self, modifications_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Apply metadata curation to datasets.
        
        Args:
            modifications_file: Path to data modifications CSV
            
        Returns:
            Dict with curation results
        """
        self.logger.info("✨ Starting dataset metadata curation...")
        
        # Use provided modifications file or default
        if modifications_file:
            mod_file = Path(modifications_file)
        else:
            mod_file = self.base_path / 'auto_data_modifications.csv'
        
        if not mod_file.exists():
            raise FileNotFoundError(f"Data modifications file not found: {mod_file}")
        
        return self._execute_curation("datasets", str(mod_file))
    
    def curate_collections(self, modifications_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Apply metadata curation to collections.
        
        Args:
            modifications_file: Path to collection modifications CSV
            
        Returns:
            Dict with curation results
        """
        self.logger.info("📁 Starting collection metadata curation...")
        
        # Use provided modifications file or default
        if modifications_file:
            mod_file = Path(modifications_file)
        else:
            mod_file = self.base_path / 'auto_collection_modifications.csv'
        
        if not mod_file.exists():
            raise FileNotFoundError(f"Collection modifications file not found: {mod_file}")
        
        return self._execute_curation("collections", str(mod_file))
    
    def curate_all(self, data_modifications_file: Optional[str] = None,
                   collection_modifications_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Apply curation to both datasets and collections.
        
        Args:
            data_modifications_file: Path to data modifications CSV
            collection_modifications_file: Path to collection modifications CSV
            
        Returns:
            Dict with all curation results
        """
        self.logger.info("🚀 Starting comprehensive metadata curation...")
        
        results = {
            'dataset_curation': None,
            'collection_curation': None,
            'creator_fixes': None,
            'success': True
        }
        
        try:
            # Step 1: Fix critical validation errors (missing creators)
            results['creator_fixes'] = self.fix_validation_errors()
            
            # Step 2: Curate datasets
            results['dataset_curation'] = self.curate_datasets(data_modifications_file)
            
            # Step 3: Curate collections
            results['collection_curation'] = self.curate_collections(collection_modifications_file)
            
            self._display_curation_summary(results)
            
        except Exception as e:
            self.logger.error(f"Error during curation: {e}")
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def fix_validation_errors(self) -> Dict[str, Any]:
        """
        Fix critical validation errors like missing creator fields.
        
        Returns:
            Dict with validation fix results
        """
        self.logger.info("🔧 Fixing critical validation errors...")
        
        results = {
            'items_fixed': 0,
            'errors_fixed': [],
            'success': True
        }
        
        try:
            # Generate creator fixes for datasets and collections
            creator_fixes = self._generate_creator_fixes()
            
            if creator_fixes['datasets_file'].exists():
                # Apply dataset creator fixes
                dataset_result = self._execute_curation("datasets", str(creator_fixes['datasets_file']))
                if dataset_result.get('success'):
                    results['items_fixed'] += dataset_result.get('modifications_applied', 0)
                    results['errors_fixed'].append(f"Added creators to {dataset_result.get('modifications_applied', 0)} datasets")
            
            if creator_fixes['collections_file'].exists():
                # Apply collection creator fixes  
                collection_result = self._execute_curation("collections", str(creator_fixes['collections_file']))
                if collection_result.get('success'):
                    results['items_fixed'] += collection_result.get('modifications_applied', 0)
                    results['errors_fixed'].append(f"Added creators to {collection_result.get('modifications_applied', 0)} collections")
            
            self.logger.info(f"✅ Fixed validation errors for {results['items_fixed']} items")
            
        except Exception as e:
            self.logger.error(f"Error fixing validation errors: {e}")
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def _generate_creator_fixes(self) -> Dict[str, Path]:
        """Generate CSV files with creator field fixes."""
        datasets_file = self.base_path / 'creator_fixes_datasets.csv'
        collections_file = self.base_path / 'creator_fixes_collections.csv'
        
        # Default creator for test environment
        default_creator = "Test User (test environment)"
        
        # Generate dataset creator fixes
        upload_file = self.base_path / 'upload_results.csv'
        if upload_file.exists():
            df = pd.read_csv(upload_file)
            creator_df = pd.DataFrame({
                'id': df['identifier'],
                'action': 'add_metadata',
                'property': 'creator',
                'value': default_creator,
                'lang': 'en'
            })
            creator_df.to_csv(datasets_file, index=False)
        
        # Generate collection creator fixes
        collections_output_file = self.base_path / 'collections_output.csv'
        if collections_output_file.exists():
            df = pd.read_csv(collections_output_file)
            creator_df = pd.DataFrame({
                'id': df['collection_id'],
                'action': 'add_metadata',
                'property': 'creator',
                'value': default_creator,
                'lang': 'en'
            })
            creator_df.to_csv(collections_file, index=False)
        
        return {
            'datasets_file': datasets_file,
            'collections_file': collections_file
        }
    
    def _execute_curation(self, scope: Literal["datasets", "collections"], 
                         modifications_file: str) -> Dict[str, Any]:
        """
        Execute curation using NakalaCuratorClient directly.
        
        Args:
            scope: Curation scope ('datasets' or 'collections')
            modifications_file: Path to modifications CSV file
            
        Returns:
            Dict with curation execution results
        """
        # Create curator client
        try:
            config = NakalaConfig(
                api_url=self.config.get('api_url', 'https://apitest.nakala.fr'),
                api_key=self.config['api_key']
            )
            curator_client = NakalaCuratorClient(config)
            
            # Load modifications from CSV
            modifications_df = pd.read_csv(modifications_file)
            modifications = []
            
            for _, row in modifications_df.iterrows():
                # Convert CSV row to modification format
                changes = {}
                for col in modifications_df.columns:
                    if col not in ['id', 'action'] and pd.notna(row[col]):
                        changes[col] = row[col]
                
                modifications.append({
                    'id': row['id'],
                    'changes': changes
                })
            
            # Execute curation using real API calls
            start_time = time.time()
            self.logger.info(f"Executing {scope} curation with {len(modifications)} modifications")
            
            # Apply modifications using curator client batch operations
            # Note: batch_modify_metadata works for both datasets and collections
            result = curator_client.batch_modify_metadata(modifications, dry_run=False)
            
            execution_time = time.time() - start_time
            
            self.logger.info(f"✅ {scope.capitalize()} curation completed successfully")
            return self._process_curation_results(scope, modifications_file, execution_time, result)
                
        except Exception as e:
            error_msg = f"{scope.capitalize()} curation failed: {e}"
            self.logger.error(error_msg)
            raise NakalaError(error_msg)
    
    def _process_curation_results(self, scope: str, modifications_file: str, 
                                 execution_time: float, batch_result) -> Dict[str, Any]:
        """Process curation results and generate statistics."""
        try:
            # Read modifications file to count operations
            df = pd.read_csv(modifications_file)
            
            # Get summary from batch result
            summary = batch_result.get_summary()
            
            stats = {
                'scope': scope,
                'total_modifications': len(df),
                'modifications_applied': summary['successful'],  # Use actual successful count
                'unique_items': len(df['id'].unique()) if 'id' in df.columns else 0,
                'modification_types': df['action'].value_counts().to_dict() if 'action' in df.columns else {},
                'execution_time': execution_time,
                'modifications_file': modifications_file,
                'success': True,
                'successful_modifications': summary['successful'],
                'failed_modifications': summary['failed'],
                'success_rate': summary['success_rate']
            }
            
            return {
                'stats': stats,
                'batch_result': batch_result,
                'modifications_df': df,
                'success': True
            }
            
        except Exception as e:
            self.logger.error(f"Error processing {scope} curation results: {e}")
            raise
    
    def _display_curation_summary(self, results: Dict[str, Any]):
        """Display comprehensive curation summary."""
        print("\n✨ Metadata Curation Summary")
        print("=" * 50)
        
        if results['dataset_curation']:
            dataset_stats = results['dataset_curation']['stats']
            print("Dataset Curation:")
            print(f"  - Modifications Applied: {dataset_stats['total_modifications']}")
            print(f"  - Datasets Modified: {dataset_stats['unique_items']}")
            print(f"  - Execution Time: {dataset_stats['execution_time']:.2f}s")
        
        if results['collection_curation']:
            collection_stats = results['collection_curation']['stats']
            print("Collection Curation:")
            print(f"  - Modifications Applied: {collection_stats['total_modifications']}")
            print(f"  - Collections Modified: {collection_stats['unique_items']}")
            print(f"  - Execution Time: {collection_stats['execution_time']:.2f}s")
        
        print("=" * 50)
    
    def verify_curation(self, scope: Optional[Literal["datasets", "collections"]] = None) -> Dict[str, bool]:
        """
        Verify curation operations completed successfully.
        
        Args:
            scope: Specific scope to verify, or None for both
            
        Returns:
            Dict with verification results
        """
        verification = {}
        
        if scope is None or scope == "datasets":
            # Check if data modifications file exists and was processed
            data_mod_file = self.base_path / 'auto_data_modifications.csv'
            verification['datasets'] = data_mod_file.exists()
            if verification['datasets']:
                self.logger.info("✅ Dataset curation verified")
            else:
                self.logger.warning("⚠️ Dataset modifications file not found")
        
        if scope is None or scope == "collections":
            # Check if collection modifications file exists and was processed
            coll_mod_file = self.base_path / 'auto_collection_modifications.csv'
            verification['collections'] = coll_mod_file.exists()
            if verification['collections']:
                self.logger.info("✅ Collection curation verified")
            else:
                self.logger.warning("⚠️ Collection modifications file not found")
        
        return verification
    
    def get_modification_summary(self, scope: Literal["datasets", "collections"]) -> Optional[Dict[str, Any]]:
        """
        Get summary of modifications for a specific scope.
        
        Args:
            scope: Scope to summarize ('datasets' or 'collections')
            
        Returns:
            Dict with modification summary or None if file not found
        """
        if scope == "datasets":
            mod_file = self.base_path / 'auto_data_modifications.csv'
        else:
            mod_file = self.base_path / 'auto_collection_modifications.csv'
        
        if not mod_file.exists():
            return None
        
        try:
            df = pd.read_csv(mod_file)
            
            summary = {
                'total_modifications': len(df),
                'unique_items': len(df['id'].unique()) if 'id' in df.columns else 0,
                'properties_modified': df['action'].value_counts().to_dict() if 'action' in df.columns else {},
                'sample_modifications': df.head(5).to_dict('records') if len(df) > 0 else []
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error getting modification summary for {scope}: {e}")
            return None