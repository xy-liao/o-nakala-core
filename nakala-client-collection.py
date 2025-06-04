import csv
import json
import logging
import argparse
from typing import Dict, Any, List, Optional, TypedDict, Collection
import requests
from datetime import datetime
import openapi_client
from openapi_client.rest import ApiException
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nakala_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MappingDiagnostics(TypedDict):
    folder: Dict[str, Dict[str, Any]]
    matched_items: List[str]
    unmatched_folders: List[str]

class CollectionResult(TypedDict):
    title: str
    status: str
    data_ids: List[str]
    data_count: int
    creation_status: str
    error: str
    id: str
    timestamp: str
    mapping_diagnostics: Optional[MappingDiagnostics]

class NakalaCollectionManager:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.configuration = openapi_client.Configuration(host=api_url)
        self.configuration.api_key['apiKey'] = api_key

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def create_collection(self, collection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new collection in Nakala."""
        try:
            headers = {
                'Content-Type': 'application/json',
                'X-API-KEY': self.api_key
            }
            # Log the full payload for debugging
            payload_str = json.dumps(collection_data, ensure_ascii=False, indent=2)
            logger.info(f"Payload: {payload_str}")
            
            response = requests.post(
                f"{self.api_url}/collections",
                headers=headers,
                data=json.dumps(collection_data)
            )
            
            if response.status_code == 201:
                result = response.json()
                collection_id = result.get('payload', {}).get('id', 'Unknown ID')
                logger.info(f"Created collection: {collection_id}")
                return result
            else:
                raise ApiException(
                    status=response.status_code,
                    reason=response.text
                )
                
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def add_data_to_collection(self, collection_id: str, data_ids: List[str]) -> bool:
        """Add data items to an existing collection."""
        try:
            headers = {
                'Content-Type': 'application/json',
                'X-API-KEY': self.api_key
            }
            
            response = requests.post(
                f"{self.api_url}/collections/{collection_id}/datas",
                headers=headers,
                data=json.dumps(data_ids)
            )
            
            if response.status_code == 201:
                logger.info(f"Successfully added {len(data_ids)} data items to collection {collection_id}")
                return True
            else:
                raise ApiException(status=response.status_code, reason=response.text)
                
        except Exception as e:
            logger.error(f"Error adding data to collection {collection_id}: {e}")
            raise

    def prepare_collection_metadata(self, title: str, description: str, 
                                  keywords: List[str], lang: str = "fr") -> List[Dict[str, Any]]:
        """Prepare metadata for collection creation."""
        metas = []
        
        # Title metadata (required)
        metas.append({
            "value": title,
            "lang": lang,
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://nakala.fr/terms#title"
        })
        
        # Description metadata
        if description:
            metas.append({
                "value": description,
                "lang": lang,
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/description"
            })
        
        # Keywords metadata
        for keyword in keywords:
            if keyword.strip():
                metas.append({
                    "value": keyword.strip(),
                    "lang": lang,
                    "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                    "propertyUri": "http://purl.org/dc/terms/subject"
                })
        
        return metas

    def create_collection_from_uploaded_data(self, output_csv: str, collection_title: str,
                                           collection_description: str = "", 
                                           keywords: List[str] = None,
                                           status: str = "private") -> Optional[str]:
        """Create a collection from successfully uploaded data items."""
        keywords = keywords or []
        
        # Read uploaded data from output CSV
        data_ids = []
        try:
            with open(output_csv, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['status'] == 'OK' and row['identifier']:
                        data_ids.append(row['identifier'])
            
            if not data_ids:
                logger.error("No successfully uploaded data found in output CSV")
                return None
                
            logger.info(f"Found {len(data_ids)} successfully uploaded data items")
            
        except Exception as e:
            logger.error(f"Error reading output CSV {output_csv}: {e}")
            return None

        # Prepare collection metadata
        metas = self.prepare_collection_metadata(
            title=collection_title,
            description=collection_description,
            keywords=keywords
        )

        # Create collection payload
        collection_data = {
            "status": status,
            "datas": data_ids,
            "metas": metas,
            "rights": []  # Empty rights array - only creator will have access initially
        }

        try:
            # Create the collection
            result = self.create_collection(collection_data)
            collection_id = result.get('payload', {}).get('id')
            
            if collection_id:
                logger.info(f"Collection '{collection_title}' created successfully with ID: {collection_id}")
                return collection_id
            else:
                logger.error("Collection creation failed - no ID returned")
                return None
                
        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            return None

    def create_collection_from_id_list(self, data_ids: List[str], collection_title: str,
                                     collection_description: str = "",
                                     keywords: List[str] = None,
                                     status: str = "private") -> Optional[str]:
        """Create a collection from a list of data IDs."""
        keywords = keywords or []
        
        if not data_ids:
            logger.error("No data IDs provided")
            return None

        # Prepare collection metadata
        metas = self.prepare_collection_metadata(
            title=collection_title,
            description=collection_description,
            keywords=keywords
        )

        # Create collection payload
        collection_data = {
            "status": status,
            "datas": data_ids,
            "metas": metas,
            "rights": []
        }

        try:
            # Create the collection
            result = self.create_collection(collection_data)
            collection_id = result.get('payload', {}).get('id')
            
            if collection_id:
                logger.info(f"Collection '{collection_title}' created successfully with ID: {collection_id}")
                return collection_id
            else:
                logger.error("Collection creation failed - no ID returned")
                return None
                
        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            return None

    def _matches_folder_type(self, folder_path: str, title: str) -> bool:
        """Enhanced matching logic for folder paths to titles."""
        folder_name = folder_path.split('/')[-1]
        
        # Create mapping of folder names to expected title patterns
        folder_mappings = {
            'code': ['code', 'fichiers de code'],
            'data': ['data', 'données'],
            'documents': ['documents', 'research documents'],
            'images': ['images', 'collection d\'images'],
            'presentations': ['presentations', 'matériaux de présentation']
        }
        
        title_lower = title.lower()
        
        # Check direct folder name match
        if folder_name in title_lower:
            return True
        
        # Check mapped patterns
        if folder_name in folder_mappings:
            return any(pattern in title_lower for pattern in folder_mappings[folder_name])
        
        return False

    def _parse_multilingual_field(self, value: str) -> list:
        """Parse a field like 'fr:Texte FR|en:Text EN' into a list of (lang, value) tuples."""
        if not value:
            return []
        result = []
        for part in value.split('|'):
            if ':' in part:
                lang, val = part.split(':', 1)
                result.append((lang.strip(), val.strip()))
            else:
                # fallback: no lang specified
                result.append((None, part.strip()))
        return result

    def _prepare_collection_metadata_from_config(self, config: Dict[str, str]) -> List[Dict[str, Any]]:
        """Prepare metadata for collection from configuration, handling multilingual fields."""
        metas = []
        # Title (required, multilingual)
        for lang, val in self._parse_multilingual_field(config.get('title', '')):
            metas.append({
                "value": val,
                "lang": lang if lang else 'und',
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#title"
            })
        # Description (multilingual)
        for lang, val in self._parse_multilingual_field(config.get('description', '')):
            metas.append({
                "value": val,
                "lang": lang if lang else 'und',
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/description"
            })
        # Keywords (multilingual, multi-value)
        for kw_field in self._parse_multilingual_field(config.get('keywords', '')):
            lang, val = kw_field
            for keyword in val.split(';'):
                if keyword.strip():
                    metas.append({
                        "value": keyword.strip(),
                        "lang": lang if lang else 'und',
                        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                        "propertyUri": "http://purl.org/dc/terms/subject"
                    })
        # Creator (multilingual, multi-value)
        for lang, val in self._parse_multilingual_field(config.get('creator', '')):
            for creator in val.split(';'):
                if creator.strip():
                    metas.append({
                        "value": creator.strip(),
                        "lang": lang if lang else 'und',
                        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                        "propertyUri": "http://purl.org/dc/terms/creator"
                    })
        # Contributor (multilingual, multi-value)
        for lang, val in self._parse_multilingual_field(config.get('contributor', '')):
            for contributor in val.split(';'):
                if contributor.strip():
                    metas.append({
                        "value": contributor.strip(),
                        "lang": lang if lang else 'und',
                        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                        "propertyUri": "http://purl.org/dc/terms/contributor"
                    })
        # Publisher (multilingual)
        for lang, val in self._parse_multilingual_field(config.get('publisher', '')):
            metas.append({
                "value": val,
                "lang": lang if lang else 'und',
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/publisher"
            })
        # Date (multilingual)
        for lang, val in self._parse_multilingual_field(config.get('date', '')):
            metas.append({
                "value": val,
                "lang": lang if lang else 'und',
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/date"
            })
        # Rights (multilingual)
        for lang, val in self._parse_multilingual_field(config.get('rights', '')):
            metas.append({
                "value": val,
                "lang": lang if lang else 'und',
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/rights"
            })
        # Coverage (multilingual)
        for lang, val in self._parse_multilingual_field(config.get('coverage', '')):
            metas.append({
                "value": val,
                "lang": lang if lang else 'und',
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/coverage"
            })
        # Relation (multilingual)
        for lang, val in self._parse_multilingual_field(config.get('relation', '')):
            metas.append({
                "value": val,
                "lang": lang if lang else 'und',
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/relation"
            })
        # Source (multilingual)
        for lang, val in self._parse_multilingual_field(config.get('source', '')):
            metas.append({
                "value": val,
                "lang": lang if lang else 'und',
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/source"
            })
        return metas

    def generate_collection_report(self, collection_results: List[CollectionResult], output_file: str = 'collections_output.csv'):
        """Generate a CSV report of created collections."""
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header row
                writer.writerow([
                    'collection_id', 'collection_title', 'status', 'data_items_count', 
                    'data_items_ids', 'creation_status', 'error_message', 'timestamp'
                ])
                
                # Data rows
                for result in collection_results:
                    writer.writerow([
                        result.get('id', ''),
                        result.get('title', ''),
                        result.get('status', ''),
                        result.get('data_count', 0),
                        ';'.join(result.get('data_ids', [])),
                        result.get('creation_status', 'ERROR'),
                        result.get('error', ''),
                        result.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    ])
                    
            logger.info(f"Collection report saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error generating collection report: {e}")

    def _create_single_collection_with_report(
        self,
        config: Dict[str, str],
        uploaded_items: Dict[str, str]
    ) -> CollectionResult:
        """Create collection and return detailed result for reporting."""
        result: CollectionResult = {
            'title': config.get('title', 'Unknown'),
            'status': config.get('status', 'private'),
            'data_ids': [],
            'data_count': 0,
            'creation_status': 'ERROR',
            'error': '',
            'id': '',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'mapping_diagnostics': None
        }
        
        try:
            # Validate required fields
            if 'data_items' not in config:
                result['error'] = "Missing required field: data_items"
                return result
                
            if 'title' not in config:
                result['error'] = "Missing required field: title"
                return result
            
            # Map folder paths to data IDs
            data_item_folders = config['data_items'].split('|')
            collection_data_ids: List[str] = []
            
            logger.info(f"Creating collection: {config['title']}")
            logger.info(f"Looking for folder types: {data_item_folders}")
            logger.info(f"Available items: {list(uploaded_items.keys())}")
            
            # Track mapping diagnostics
            mapping_diagnostics: MappingDiagnostics = {
                'folder': {},
                'matched_items': [],
                'unmatched_folders': []
            }
            
            for folder_path in data_item_folders:
                matched_items: List[str] = []
                folder_name = folder_path.split('/')[-1]
                mapping_diagnostics['folder'][folder_name] = {
                    'path': folder_path,
                    'matches': []
                }
                
                for title, data_id in uploaded_items.items():
                    if self._matches_folder_type(folder_path, title):
                        collection_data_ids.append(data_id)
                        matched_items.append(title)
                        mapping_diagnostics['folder'][folder_name]['matches'].append({
                            'title': title,
                            'id': data_id
                        })
                
                if matched_items:
                    logger.info(
                        f"Folder '{folder_path}' matched: {matched_items}"
                    )
                    mapping_diagnostics['matched_items'].extend(matched_items)
                else:
                    logger.warning(f"Folder '{folder_path}' matched no items")
                    mapping_diagnostics['unmatched_folders'].append(folder_path)
            
            # Log detailed mapping diagnostics
            logger.info("Collection mapping diagnostics:")
            logger.info(json.dumps(mapping_diagnostics, indent=2))
            
            if not collection_data_ids:
                result['error'] = (
                    f"No data items found for folders: {data_item_folders}"
                )
                result['mapping_diagnostics'] = mapping_diagnostics
                return result
            
            result['data_ids'] = collection_data_ids
            result['data_count'] = len(collection_data_ids)
            result['mapping_diagnostics'] = mapping_diagnostics
            
            # Create collection
            metas = self._prepare_collection_metadata_from_config(config)
            collection_data = {
                "status": config['status'],
                "datas": collection_data_ids,
                "metas": metas,
                "rights": []
            }
            
            api_result = self.create_collection(collection_data)
            collection_id = api_result.get('payload', {}).get('id')
            
            if collection_id:
                result['id'] = collection_id
                result['creation_status'] = 'SUCCESS'
                logger.info(
                    f"Created collection: {config['title']} with ID: {collection_id}"
                )
            else:
                result['error'] = "No collection ID returned from API"
                
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Error creating collection {config['title']}: {e}")
        
        return result

    def create_collections_from_folder_config(
        self,
        output_csv: str,
        folder_collections_csv: str
    ) -> List[str]:
        """Create collections based on folder collections configuration."""
        created_collection_ids: List[str] = []
        collection_results: List[CollectionResult] = []
        
        # 1. Read uploaded data items and map by folder type
        uploaded_items: Dict[str, str] = {}
        try:
            with open(output_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['status'] == 'OK':
                        title = row['title']
                        uploaded_items[title] = row['identifier']
            
            if not uploaded_items:
                logger.error("No successfully uploaded data found in output CSV")
                return created_collection_ids
                
            logger.info(f"Found {len(uploaded_items)} uploaded data items")
            
        except Exception as e:
            logger.error(f"Error reading output CSV {output_csv}: {e}")
            return created_collection_ids
        
        # 2. Read folder collections configuration and create collections
        try:
            with open(folder_collections_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for collection_config in reader:
                    result = self._create_single_collection_with_report(
                        collection_config,
                        uploaded_items
                    )
                    collection_results.append(result)
                    
                    if result['creation_status'] == 'SUCCESS':
                        created_collection_ids.append(result['id'])
            
            # Generate CSV report
            self.generate_collection_report(collection_results)
            
            logger.info(
                f"Created {len(created_collection_ids)} collections from config"
            )
            
        except Exception as e:
            logger.error(
                f"Error reading folder collections CSV {folder_collections_csv}: {e}"
            )
            return created_collection_ids
        
        return created_collection_ids

def main():
    parser = argparse.ArgumentParser(description='Manage Nakala collections')
    parser.add_argument('--api-url', default='https://apitest.nakala.fr',
                      help='Nakala API URL')
    parser.add_argument('--api-key', required=True,
                      help='Nakala API key')
    
    # Collection creation options
    parser.add_argument('--title',
                      help='Collection title')
    parser.add_argument('--description', default='',
                      help='Collection description')
    parser.add_argument('--keywords', default='',
                      help='Comma-separated keywords for the collection')
    parser.add_argument('--status', choices=['private', 'public'], default='private',
                      help='Collection status (private or public)')
    
    # Data source options
    parser.add_argument('--from-upload-output', 
                      help='Path to upload output CSV file')
    parser.add_argument('--data-ids',
                      help='Comma-separated list of data IDs')
    parser.add_argument('--from-folder-collections',
                      help='Path to folder collections CSV file')
    
    # Report options
    parser.add_argument('--collection-report', default='collections_output.csv',
                      help='Filename for collection creation report')
    
    args = parser.parse_args()
    
    # Validate required arguments
    if args.from_folder_collections and not args.from_upload_output:
        parser.error("--from-upload-output is required when using --from-folder-collections")
    
    if not any([args.from_folder_collections, args.from_upload_output, args.data_ids]):
        parser.error("One of --from-folder-collections, --from-upload-output, or --data-ids is required")
    
    # Only require title for single collection creation
    if (args.from_upload_output or args.data_ids) and not args.from_folder_collections and not args.title:
        parser.error("--title is required when creating a single collection")
    
    # Initialize collection manager
    manager = NakalaCollectionManager(
        api_url=args.api_url,
        api_key=args.api_key
    )
    
    try:
        if args.from_folder_collections:
            collection_ids = manager.create_collections_from_folder_config(
                output_csv=args.from_upload_output,
                folder_collections_csv=args.from_folder_collections
            )
            
            if collection_ids:
                logger.info(f"Successfully created {len(collection_ids)} collections")
                for collection_id in collection_ids:
                    logger.info(f"Collection ID: {collection_id}")
            else:
                logger.error("No collections were created")
                
        elif args.from_upload_output:
            # Parse keywords
            keywords = [k.strip() for k in args.keywords.split(',') if k.strip()] if args.keywords else []
            
            collection_id = manager.create_collection_from_uploaded_data(
                output_csv=args.from_upload_output,
                collection_title=args.title,
                collection_description=args.description,
                keywords=keywords,
                status=args.status
            )
            
            if collection_id:
                logger.info(f"Successfully created collection with ID: {collection_id}")
            else:
                logger.error("Failed to create collection")
                
        elif args.data_ids:
            # Parse keywords
            keywords = [k.strip() for k in args.keywords.split(',') if k.strip()] if args.keywords else []
            
            # Parse data IDs
            data_ids = [id.strip() for id in args.data_ids.split(',') if id.strip()]
            
            collection_id = manager.create_collection_from_id_list(
                data_ids=data_ids,
                collection_title=args.title,
                collection_description=args.description,
                keywords=keywords,
                status=args.status
            )
            
            if collection_id:
                logger.info(f"Successfully created collection with ID: {collection_id}")
            else:
                logger.error("Failed to create collection")
                
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == '__main__':
    main()
