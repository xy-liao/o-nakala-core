"""
Collection Management Operations

Handles collection creation and management for NAKALA workflow,
corresponding to Step 2 of the ultimate workflow.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import time
from o_nakala_core.collection import NakalaCollectionClient
from o_nakala_core.common.config import NakalaConfig

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
        Create collections using NakalaCollectionClient directly with real API calls.
        
        Args:
            upload_results_file: Path to upload results CSV (optional)
            
        Returns:
            Dict with collection creation results and statistics
        """
        self.logger.info("📁 Starting real collection creation...")
        
        # Use provided upload results file or default
        if upload_results_file:
            upload_file = Path(upload_results_file)
        else:
            upload_file = Path(self.config['base_path']) / 'upload_results.csv'
        
        if not upload_file.exists():
            raise FileNotFoundError(f"Upload results file not found: {upload_file}")
        
        # Initialize NAKALA client
        config = NakalaConfig(
            api_key=self.config['api_key'],
            api_url=self.config.get('api_url', 'https://apitest.nakala.fr')
        )
        
        # Execute collection creation
        start_time = time.time()
        try:
            self.logger.info(f"Creating collections from upload results: {upload_file}")
            
            # Read upload results and collections config
            upload_df = pd.read_csv(upload_file)
            collections_df = pd.read_csv(self.config['collections_csv'])
            
            collection_client = NakalaCollectionClient(config)
            collection_results = []
            
            for index, row in collections_df.iterrows():
                try:
                    # Prepare collection metadata with data items
                    collection_title = row.get('title', f'Collection {int(index) + 1}')
                    collection_description = row.get('description', '')
                    collection_status = row.get('status', 'private')
                    data_items_str = row.get('data_items', '')
                    
                    # Map data item titles to actual IDs from upload results
                    data_item_titles = data_items_str.split(';') if data_items_str else []
                    mapped_data_ids = []
                    
                    for title in data_item_titles:
                        title = title.strip()
                        if title:
                            # Find matching dataset ID from upload results
                            matching_row = upload_df[upload_df['title'] == title]
                            if not matching_row.empty:
                                data_id = matching_row.iloc[0]['identifier']
                                mapped_data_ids.append(data_id)
                                self.logger.debug(f"Mapped '{title}' to ID: {data_id}")
                            else:
                                self.logger.warning(f"No dataset found for title: '{title}'")
                    
                    if not mapped_data_ids:
                        self.logger.warning(f"No valid data items found for collection: {collection_title}")
                        collection_results.append({
                            'collection_id': f'failed_coll_{index}',
                            'collection_title': collection_title,
                            'status': collection_status,
                            'data_items_count': 0,
                            'data_items_ids': '',
                            'creation_status': 'FAILED',
                            'error_message': 'No valid data items found',
                            'timestamp': pd.Timestamp.now().isoformat()
                        })
                        continue
                    
                    # Create collection configuration
                    collection_config = {
                        'title': collection_title,
                        'description': collection_description,
                        'status': collection_status,
                        'data_ids': mapped_data_ids
                    }
                    
                    # Create collection using real API call
                    collection_id = collection_client.create_single_collection(collection_config)
                    
                    collection_results.append({
                        'collection_id': collection_id,
                        'collection_title': collection_title,
                        'status': collection_status,
                        'data_items_count': len(mapped_data_ids),
                        'data_items_ids': ';'.join(mapped_data_ids),
                        'creation_status': 'SUCCESS',
                        'error_message': None,
                        'timestamp': pd.Timestamp.now().isoformat()
                    })
                    
                    self.logger.info(f"✅ Created collection {int(index) + 1}: {collection_id}")
                    
                except Exception as e:
                    self.logger.error(f"❌ Failed to create collection {int(index) + 1}: {e}")
                    collection_results.append({
                        'collection_id': f'failed_coll_{index}',
                        'collection_title': row.get('title', 'Unknown'),
                        'status': 'private',
                        'data_items_count': 0,
                        'data_items_ids': '',
                        'creation_status': 'FAILED',
                        'error_message': str(e),
                        'timestamp': pd.Timestamp.now().isoformat()
                    })
            
            execution_time = time.time() - start_time
            
            # Save results to CSV
            self._save_collection_results(collection_results)
            
            self.logger.info("✅ Real collection creation completed successfully")
            return self._process_collection_results(execution_time)
            
        except Exception as e:
            self.logger.error(f"Collection creation failed: {e}")
            raise
    
    def _save_collection_results(self, collection_results):
        """Save collection results to CSV file."""
        try:
            # Convert collection results to DataFrame format
            results_data = []
            for result in collection_results:
                if hasattr(result, 'to_dict'):
                    results_data.append(result.to_dict())
                else:
                    results_data.append(result)
            
            df = pd.DataFrame(results_data)
            df.to_csv(self.collections_output_file, index=False)
            self.logger.info(f"Collection results saved to: {self.collections_output_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving collection results: {e}")
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
                'successful_collections': len(df[df['creation_status'] == 'SUCCESS']) if 'creation_status' in df.columns else len(df),
                'failed_collections': len(df[df['creation_status'] != 'SUCCESS']) if 'creation_status' in df.columns else 0,
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