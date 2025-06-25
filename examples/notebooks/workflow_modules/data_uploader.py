"""
Data Upload Operations

Handles dataset upload to NAKALA using the Python API directly,
corresponding to Step 1 of the ultimate workflow.
"""

import subprocess
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import time

class DataUploader:
    """Handles data upload operations for NAKALA workflow."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize data uploader.
        
        Args:
            config: Configuration dictionary from WorkflowConfig
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.results_file = Path(config['base_path']) / 'upload_results.csv'
    
    def upload_datasets(self, mode: str = "folder") -> Dict[str, Any]:
        """
        Upload datasets using o-nakala-upload CLI command.
        
        Args:
            mode: Upload mode ('folder' or 'individual')
            
        Returns:
            Dict with upload results and statistics
        """
        self.logger.info("📤 Starting dataset upload...")
        
        # Prepare command
        cmd = [
            "o-nakala-upload",
            "--api-key", self.config['api_key'],
            "--dataset", self.config['dataset_csv'],
            "--mode", mode,
            "--base-path", self.config['base_path'],
            "--output", str(self.results_file)
        ]
        
        if mode == "folder":
            cmd.extend(["--folder-config", self.config['dataset_csv']])
        
        # Execute upload
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
                self.logger.info("✅ Upload completed successfully")
                return self._process_upload_results(execution_time)
            else:
                error_msg = f"Upload failed: {result.stderr}"
                self.logger.error(error_msg)
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
                
        except subprocess.TimeoutExpired:
            self.logger.error("Upload timed out after 5 minutes")
            raise
        except FileNotFoundError:
            self.logger.error("o-nakala-upload command not found. Ensure o-nakala-core[cli] is installed.")
            raise
    
    def _process_upload_results(self, execution_time: float) -> Dict[str, Any]:
        """Process and analyze upload results."""
        if not self.results_file.exists():
            raise FileNotFoundError(f"Upload results file not found: {self.results_file}")
        
        # Read results
        try:
            df = pd.read_csv(self.results_file)
            
            # Calculate statistics
            stats = {
                'total_datasets': len(df),
                'successful_uploads': len(df[df['status'] == 'OK']) if 'status' in df.columns else len(df),
                'failed_uploads': len(df[df['status'] != 'OK']) if 'status' in df.columns else 0,
                'execution_time': execution_time,
                'results_file': str(self.results_file),
                'first_dataset_id': df.iloc[0]['identifier'] if len(df) > 0 and 'identifier' in df.columns else None
            }
            
            # Display summary
            self._display_upload_summary(stats, df)
            
            return {
                'stats': stats,
                'results_df': df,
                'success': True
            }
            
        except Exception as e:
            self.logger.error(f"Error processing upload results: {e}")
            raise
    
    def _display_upload_summary(self, stats: Dict[str, Any], df: pd.DataFrame):
        """Display upload summary information."""
        print("\n📊 Upload Summary")
        print("=" * 40)
        print(f"Total Datasets: {stats['total_datasets']}")
        print(f"Successful: {stats['successful_uploads']}")
        print(f"Failed: {stats['failed_uploads']}")
        print(f"Execution Time: {stats['execution_time']:.2f} seconds")
        
        if stats['first_dataset_id']:
            print(f"First Dataset ID: {stats['first_dataset_id']}")
        
        # Show first few results
        if len(df) > 0:
            print("\n📋 First Few Results:")
            print(df.head(3).to_string(index=False))
        
        print("=" * 40)
    
    def get_upload_results(self) -> Optional[pd.DataFrame]:
        """Get upload results as pandas DataFrame."""
        if self.results_file.exists():
            return pd.read_csv(self.results_file)
        return None
    
    def verify_upload(self) -> bool:
        """Verify upload was successful and results are available."""
        if not self.results_file.exists():
            self.logger.warning("Upload results file not found")
            return False
        
        try:
            df = pd.read_csv(self.results_file)
            if len(df) == 0:
                self.logger.warning("Upload results file is empty")
                return False
            
            # Check if we have required columns
            required_columns = ['identifier']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                self.logger.warning(f"Missing required columns: {missing_columns}")
                return False
            
            self.logger.info("✅ Upload verification successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying upload: {e}")
            return False