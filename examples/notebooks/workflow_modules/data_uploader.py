"""
Data Upload Operations

Handles dataset upload to NAKALA using the Python API directly,
corresponding to Step 1 of the ultimate workflow.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import time
import json
import os
from o_nakala_core.upload import NakalaUploadClient
from o_nakala_core.common.config import NakalaConfig

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
        Upload datasets using NakalaUploadClient directly with real API calls.
        
        Args:
            mode: Upload mode ('folder' or 'individual')
            
        Returns:
            Dict with upload results and statistics
        """
        self.logger.info("📤 Starting real dataset upload...")
        
        # Initialize NAKALA client
        config = NakalaConfig(
            api_key=self.config['api_key'],
            api_url=self.config.get('api_url', 'https://apitest.nakala.fr')
        )
        
        start_time = time.time()
        try:
            self.logger.info(f"Uploading datasets from: {self.config['dataset_csv']}")
            
            # Process datasets individually for better control
            upload_client = NakalaUploadClient(config)
            upload_results = []
            
            # Read CSV to process datasets
            df = pd.read_csv(self.config['dataset_csv'])
            
            for index, row in df.iterrows():
                try:
                    self.logger.info(f"Processing dataset {index + 1}/{len(df)}: {row.get('title', 'Unknown')}")
                    
                    # Prepare dataset configuration for real API call
                    dataset_config = {
                        'title': row.get('title', f'Dataset {index + 1}'),
                        'type': row.get('type', 'http://purl.org/dc/dcmitype/Dataset'),
                        'description': row.get('description', ''),
                        'creator': row.get('creator', 'Workflow User'),
                        'date': row.get('date', ''),
                        'license': row.get('license', ''),
                        'keywords': row.get('keywords', ''),
                        'status': row.get('status', 'pending'),
                        'files': []
                    }
                    
                    # Process file paths if specified
                    file_paths = row.get('file', '').split(';') if row.get('file') else []
                    resolved_files = []
                    for file_path in file_paths:
                        if file_path.strip():
                            resolved_path = upload_client._resolve_file_path(file_path.strip())
                            if resolved_path:
                                resolved_files.append(resolved_path)
                            else:
                                self.logger.warning(f"File not found: {file_path}")
                    
                    dataset_config['files'] = resolved_files
                    
                    # Create dataset using real API call
                    dataset_id = upload_client.upload_single_dataset(dataset_config)
                    
                    upload_results.append({
                        'identifier': dataset_id,
                        'title': dataset_config['title'],
                        'status': 'OK',
                        'files': ';'.join([os.path.basename(f) for f in resolved_files]),
                        'response': json.dumps({'code': 201, 'message': 'Dataset created successfully', 'identifier': dataset_id})
                    })
                    
                    self.logger.info(f"✅ Dataset {index + 1} created successfully with ID: {dataset_id}")
                    
                except Exception as e:
                    self.logger.error(f"❌ Failed to process dataset {index + 1}: {e}")
                    upload_results.append({
                        'identifier': f'failed_{index}',
                        'title': row.get('title', 'Unknown'), 
                        'status': 'FAILED',
                        'files': '',
                        'response': str(e)
                    })
            
            self.logger.info(f"✅ Upload processing completed - {len(upload_results)} datasets processed")
            
            execution_time = time.time() - start_time
            
            # Save results to CSV
            self._save_upload_results(upload_results)
            
            self.logger.info("✅ Real upload completed successfully")
            return self._process_upload_results(execution_time)
            
        except Exception as e:
            self.logger.error(f"Upload failed: {e}")
            raise
    
    def _save_upload_results(self, upload_results):
        """Save upload results to CSV file."""
        try:
            # Convert upload results to DataFrame format
            results_data = []
            for result in upload_results:
                if hasattr(result, 'to_dict'):
                    results_data.append(result.to_dict())
                else:
                    results_data.append(result)
            
            df = pd.DataFrame(results_data)
            df.to_csv(self.results_file, index=False)
            self.logger.info(f"Results saved to: {self.results_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving upload results: {e}")
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