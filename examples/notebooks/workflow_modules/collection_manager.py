"""
Collection Management Operations

Handles collection creation and management for NAKALA workflow,
corresponding to Step 2 of the ultimate workflow.
"""

import subprocess
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import time

class CollectionManager:
    """Handles collection creation and management operations."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize collection manager.
        
        Args:
            config: Configuration dictionary from WorkflowConfig
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.collections_output_file = Path(config['base_path']) / 'collections_output.csv'
    
    def create_collections(self, upload_results_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Create collections using o-nakala-collection CLI command.
        
        Args:
            upload_results_file: Path to upload results CSV (optional)
            
        Returns:
            Dict with collection creation results and statistics
        """
        self.logger.info("📁 Starting collection creation...")
        
        # Use provided upload results file or default
        if upload_results_file:
            upload_file = Path(upload_results_file)
        else:
            upload_file = Path(self.config['base_path']) / 'upload_results.csv'
        
        if not upload_file.exists():
            raise FileNotFoundError(f"Upload results file not found: {upload_file}")
        
        # Prepare command
        cmd = [
            "o-nakala-collection",
            "--api-key", self.config['api_key'],
            "--from-upload-output", str(upload_file),
            "--from-folder-collections", self.config['collections_csv'],
            "--collection-report", str(self.collections_output_file)
        ]
        
        # Execute collection creation
        start_time = time.time()
        try:
            self.logger.info(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.config['base_path'],
                timeout=300  # 5 minute timeout
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                self.logger.info("✅ Collection creation completed successfully")
                return self._process_collection_results(execution_time)
            else:
                error_msg = f"Collection creation failed: {result.stderr}"
                self.logger.error(error_msg)
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
                
        except subprocess.TimeoutExpired:
            self.logger.error("Collection creation timed out after 5 minutes")
            raise
        except FileNotFoundError:
            self.logger.error("o-nakala-collection command not found. Ensure o-nakala-core[cli] is installed.")
            raise
    
    def _process_collection_results(self, execution_time: float) -> Dict[str, Any]:
        """Process and analyze collection creation results."""
        if not self.collections_output_file.exists():
            raise FileNotFoundError(f"Collections output file not found: {self.collections_output_file}")
        
        try:
            df = pd.read_csv(self.collections_output_file)
            
            # Calculate statistics
            stats = {
                'total_collections': len(df),
                'successful_collections': len(df[df['status'] == 'success']) if 'status' in df.columns else len(df),
                'failed_collections': len(df[df['status'] == 'failed']) if 'status' in df.columns else 0,
                'execution_time': execution_time,
                'collections_file': str(self.collections_output_file),
                'first_collection_id': df.iloc[0]['collection_id'] if len(df) > 0 and 'collection_id' in df.columns else None
            }
            
            # Display summary
            self._display_collection_summary(stats, df)
            
            return {
                'stats': stats,
                'results_df': df,
                'success': True
            }
            
        except Exception as e:
            self.logger.error(f"Error processing collection results: {e}")
            raise
    
    def _display_collection_summary(self, stats: Dict[str, Any], df: pd.DataFrame):
        """Display collection creation summary."""
        print("\n📁 Collection Creation Summary")
        print("=" * 45)
        print(f"Total Collections: {stats['total_collections']}")
        print(f"Successful: {stats['successful_collections']}")
        print(f"Failed: {stats['failed_collections']}")
        print(f"Execution Time: {stats['execution_time']:.2f} seconds")
        
        if stats['first_collection_id']:
            print(f"First Collection ID: {stats['first_collection_id']}")
        
        # Show first few results
        if len(df) > 0:
            print("\n📋 First Few Collections:")
            print(df.head(3).to_string(index=False))
        
        print("=" * 45)
    
    def get_collections_results(self) -> Optional[pd.DataFrame]:
        """Get collection results as pandas DataFrame."""
        if self.collections_output_file.exists():
            return pd.read_csv(self.collections_output_file)
        return None
    
    def verify_collections(self) -> bool:
        """Verify collection creation was successful."""
        if not self.collections_output_file.exists():
            self.logger.warning("Collections output file not found")
            return False
        
        try:
            df = pd.read_csv(self.collections_output_file)
            if len(df) == 0:
                self.logger.warning("Collections output file is empty")
                return False
            
            # Check if we have required columns
            required_columns = ['collection_id']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                self.logger.warning(f"Missing required columns: {missing_columns}")
                return False
            
            self.logger.info("✅ Collection verification successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying collections: {e}")
            return False
    
    def list_collections(self) -> Optional[Dict[str, Any]]:
        """List created collections with their details."""
        df = self.get_collections_results()
        if df is None:
            return None
        
        collections_info = []
        for _, row in df.iterrows():
            collection_info = {
                'id': row.get('collection_id', 'Unknown'),
                'title': row.get('title', 'Unknown'),
                'status': row.get('status', 'Unknown'),
                'created_at': row.get('created_at', 'Unknown')
            }
            collections_info.append(collection_info)
        
        return {
            'total_count': len(collections_info),
            'collections': collections_info
        }