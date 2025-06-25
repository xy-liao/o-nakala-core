"""
Curator Operations

Handles metadata curation operations for datasets and collections,
corresponding to Steps 4-5 of the ultimate workflow.
"""

import subprocess
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Literal
import logging
import time

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
            'success': True
        }
        
        try:
            # Curate datasets
            results['dataset_curation'] = self.curate_datasets(data_modifications_file)
            
            # Curate collections
            results['collection_curation'] = self.curate_collections(collection_modifications_file)
            
            self._display_curation_summary(results)
            
        except Exception as e:
            self.logger.error(f"Error during curation: {e}")
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def _execute_curation(self, scope: Literal["datasets", "collections"], 
                         modifications_file: str) -> Dict[str, Any]:
        """
        Execute curation using o-nakala-curator CLI command.
        
        Args:
            scope: Curation scope ('datasets' or 'collections')
            modifications_file: Path to modifications CSV file
            
        Returns:
            Dict with curation execution results
        """
        # Prepare command
        cmd = [
            "o-nakala-curator",
            "--api-key", self.config['api_key'],
            "--batch-modify", modifications_file,
            "--scope", scope
        ]
        
        # Execute curation
        start_time = time.time()
        try:
            self.logger.info(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.base_path),
                timeout=600  # 10 minute timeout for curation
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                self.logger.info(f"✅ {scope.capitalize()} curation completed successfully")
                return self._process_curation_results(scope, modifications_file, execution_time, result.stdout)
            else:
                error_msg = f"{scope.capitalize()} curation failed: {result.stderr}"
                self.logger.error(error_msg)
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"{scope.capitalize()} curation timed out after 10 minutes")
            raise
        except FileNotFoundError:
            self.logger.error("o-nakala-curator command not found. Ensure o-nakala-core[cli] is installed.")
            raise
    
    def _process_curation_results(self, scope: str, modifications_file: str, 
                                 execution_time: float, stdout: str) -> Dict[str, Any]:
        """Process curation results and generate statistics."""
        try:
            # Read modifications file to count operations
            df = pd.read_csv(modifications_file)
            
            stats = {
                'scope': scope,
                'total_modifications': len(df),
                'unique_items': len(df['identifier'].unique()) if 'identifier' in df.columns else 0,
                'modification_types': df['property'].value_counts().to_dict() if 'property' in df.columns else {},
                'execution_time': execution_time,
                'modifications_file': modifications_file,
                'success': True
            }
            
            # Parse stdout for additional information if available
            if "successfully modified" in stdout.lower():
                # Try to extract success count from output
                import re
                success_match = re.search(r'(\d+).*successfully', stdout)
                if success_match:
                    stats['successful_modifications'] = int(success_match.group(1))
            
            return {
                'stats': stats,
                'stdout': stdout,
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
            print(f"Dataset Curation:")
            print(f"  - Modifications Applied: {dataset_stats['total_modifications']}")
            print(f"  - Datasets Modified: {dataset_stats['unique_items']}")
            print(f"  - Execution Time: {dataset_stats['execution_time']:.2f}s")
        
        if results['collection_curation']:
            collection_stats = results['collection_curation']['stats']
            print(f"Collection Curation:")
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
                'unique_items': len(df['identifier'].unique()) if 'identifier' in df.columns else 0,
                'properties_modified': df['property'].value_counts().to_dict() if 'property' in df.columns else {},
                'sample_modifications': df.head(5).to_dict('records') if len(df) > 0 else []
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error getting modification summary for {scope}: {e}")
            return None