"""
Metadata Enhancement Operations

Handles automatic metadata enhancement generation for datasets and collections,
corresponding to Step 3 of the ultimate workflow.
"""

import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
import pandas as pd

class MetadataEnhancer:
    """Handles automatic metadata enhancement generation."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize metadata enhancer.
        
        Args:
            config: Configuration dictionary from WorkflowConfig
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.base_path = Path(config['base_path'])
        
        # Output files for generated modifications
        self.data_modifications_file = self.base_path / 'auto_data_modifications.csv'
        self.collection_modifications_file = self.base_path / 'auto_collection_modifications.csv'
    
    def generate_data_enhancements(self, upload_results_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate automatic metadata enhancements for datasets.
        
        Args:
            upload_results_file: Path to upload results CSV
            
        Returns:
            Dict with enhancement generation results
        """
        self.logger.info("🤖 Generating dataset metadata enhancements...")
        
        # Use provided upload results file or default
        if upload_results_file:
            input_file = Path(upload_results_file)
        else:
            input_file = self.base_path / 'upload_results.csv'
        
        if not input_file.exists():
            raise FileNotFoundError(f"Upload results file not found: {input_file}")
        
        # Execute Python script for data modifications
        try:
            cmd = ["python", "create_modifications.py", str(input_file)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.base_path),
                timeout=120
            )
            
            if result.returncode == 0:
                self.logger.info("✅ Dataset enhancements generated successfully")
                return self._process_data_enhancements()
            else:
                error_msg = f"Dataset enhancement generation failed: {result.stderr}"
                self.logger.error(error_msg)
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
                
        except subprocess.TimeoutExpired:
            self.logger.error("Dataset enhancement generation timed out")
            raise
        except FileNotFoundError:
            self.logger.error("create_modifications.py script not found")
            raise
    
    def generate_collection_enhancements(self, collections_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate automatic metadata enhancements for collections.
        
        Args:
            collections_file: Path to collections output CSV
            
        Returns:
            Dict with enhancement generation results
        """
        self.logger.info("🤖 Generating collection metadata enhancements...")
        
        # Use provided collections file or default
        if collections_file:
            input_file = Path(collections_file)
        else:
            input_file = self.base_path / 'collections_output.csv'
        
        if not input_file.exists():
            raise FileNotFoundError(f"Collections file not found: {input_file}")
        
        # Execute Python script for collection modifications
        try:
            cmd = ["python", "create_collection_modifications.py", str(input_file)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.base_path),
                timeout=120
            )
            
            if result.returncode == 0:
                self.logger.info("✅ Collection enhancements generated successfully")
                return self._process_collection_enhancements()
            else:
                error_msg = f"Collection enhancement generation failed: {result.stderr}"
                self.logger.error(error_msg)
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
                
        except subprocess.TimeoutExpired:
            self.logger.error("Collection enhancement generation timed out")
            raise
        except FileNotFoundError:
            self.logger.error("create_collection_modifications.py script not found")
            raise
    
    def generate_all_enhancements(self, upload_results_file: Optional[str] = None, 
                                 collections_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate all metadata enhancements (both datasets and collections).
        
        Args:
            upload_results_file: Path to upload results CSV
            collections_file: Path to collections output CSV
            
        Returns:
            Dict with all enhancement generation results
        """
        self.logger.info("🚀 Generating all metadata enhancements...")
        
        results = {
            'data_enhancements': None,
            'collection_enhancements': None,
            'success': True
        }
        
        try:
            # Generate dataset enhancements
            results['data_enhancements'] = self.generate_data_enhancements(upload_results_file)
            
            # Generate collection enhancements
            results['collection_enhancements'] = self.generate_collection_enhancements(collections_file)
            
            self._display_enhancement_summary(results)
            
        except Exception as e:
            self.logger.error(f"Error generating enhancements: {e}")
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def _process_data_enhancements(self) -> Dict[str, Any]:
        """Process generated data enhancement results."""
        if not self.data_modifications_file.exists():
            raise FileNotFoundError(f"Data modifications file not found: {self.data_modifications_file}")
        
        try:
            df = pd.read_csv(self.data_modifications_file)
            
            stats = {
                'total_modifications': len(df),
                'unique_datasets': len(df['identifier'].unique()) if 'identifier' in df.columns else 0,
                'modification_types': df['property'].value_counts().to_dict() if 'property' in df.columns else {},
                'modifications_file': str(self.data_modifications_file)
            }
            
            return {
                'stats': stats,
                'modifications_df': df,
                'success': True
            }
            
        except Exception as e:
            self.logger.error(f"Error processing data enhancements: {e}")
            raise
    
    def _process_collection_enhancements(self) -> Dict[str, Any]:
        """Process generated collection enhancement results."""
        if not self.collection_modifications_file.exists():
            raise FileNotFoundError(f"Collection modifications file not found: {self.collection_modifications_file}")
        
        try:
            df = pd.read_csv(self.collection_modifications_file)
            
            stats = {
                'total_modifications': len(df),
                'unique_collections': len(df['identifier'].unique()) if 'identifier' in df.columns else 0,
                'modification_types': df['property'].value_counts().to_dict() if 'property' in df.columns else {},
                'modifications_file': str(self.collection_modifications_file)
            }
            
            return {
                'stats': stats,
                'modifications_df': df,
                'success': True
            }
            
        except Exception as e:
            self.logger.error(f"Error processing collection enhancements: {e}")
            raise
    
    def _display_enhancement_summary(self, results: Dict[str, Any]):
        """Display enhancement generation summary."""
        print("\n🤖 Metadata Enhancement Summary")
        print("=" * 50)
        
        if results['data_enhancements']:
            data_stats = results['data_enhancements']['stats']
            print(f"Dataset Modifications: {data_stats['total_modifications']}")
            print(f"Datasets Enhanced: {data_stats['unique_datasets']}")
        
        if results['collection_enhancements']:
            coll_stats = results['collection_enhancements']['stats']
            print(f"Collection Modifications: {coll_stats['total_modifications']}")
            print(f"Collections Enhanced: {coll_stats['unique_collections']}")
        
        print("=" * 50)
    
    def get_data_modifications(self) -> Optional[pd.DataFrame]:
        """Get generated data modifications as DataFrame."""
        if self.data_modifications_file.exists():
            return pd.read_csv(self.data_modifications_file)
        return None
    
    def get_collection_modifications(self) -> Optional[pd.DataFrame]:
        """Get generated collection modifications as DataFrame."""
        if self.collection_modifications_file.exists():
            return pd.read_csv(self.collection_modifications_file)
        return None
    
    def verify_enhancements(self) -> Dict[str, bool]:
        """Verify that enhancement files were generated successfully."""
        verification = {
            'data_enhancements': self.data_modifications_file.exists(),
            'collection_enhancements': self.collection_modifications_file.exists()
        }
        
        if verification['data_enhancements']:
            self.logger.info("✅ Data enhancements file verified")
        else:
            self.logger.warning("⚠️ Data enhancements file not found")
        
        if verification['collection_enhancements']:
            self.logger.info("✅ Collection enhancements file verified")
        else:
            self.logger.warning("⚠️ Collection enhancements file not found")
        
        return verification