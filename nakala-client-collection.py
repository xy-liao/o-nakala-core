import csv
import json
import logging
import argparse
from typing import Dict, Any, List, Optional
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

class NakalaCollectionManager:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.configuration = openapi_client.Configuration(host=api_url)
        self.configuration.api_key['apiKey'] = api_key

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def create_collection(self, collection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new collection in Nakala."""
        try:
            headers = {
                'Content-Type': 'application/json',
                'X-API-KEY': self.api_key
            }
            
            response = requests.post(
                f"{self.api_url}/collections",
                headers=headers,
                data=json.dumps(collection_data)
            )
            
            if response.status_code == 201:
                result = response.json()
                logger.info(f"Successfully created collection: {result.get('payload', {}).get('id', 'Unknown ID')}")
                return result
            else:
                raise ApiException(status=response.status_code, reason=response.text)
                
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

def main():
    parser = argparse.ArgumentParser(description='Manage Nakala collections')
    parser.add_argument('--api-url', default='https://apitest.nakala.fr',
                      help='Nakala API URL')
    parser.add_argument('--api-key', required=True,
                      help='Nakala API key')
    
    # Collection creation options
    parser.add_argument('--title', required=True,
                      help='Collection title')
    parser.add_argument('--description', default='',
                      help='Collection description')
    parser.add_argument('--keywords', default='',
                      help='Comma-separated keywords for the collection')
    parser.add_argument('--status', choices=['private', 'public'], default='private',
                      help='Collection status (private or public)')
    
    # Data source options (mutually exclusive)
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument('--from-upload-output', 
                            help='Path to upload output CSV file')
    source_group.add_argument('--data-ids',
                            help='Comma-separated list of data IDs')
    
    args = parser.parse_args()
    
    # Parse keywords
    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()] if args.keywords else []
    
    # Initialize collection manager
    manager = NakalaCollectionManager(
        api_url=args.api_url,
        api_key=args.api_key
    )
    
    try:
        collection_id = None
        
        if args.from_upload_output:
            # Create collection from upload output CSV
            collection_id = manager.create_collection_from_uploaded_data(
                output_csv=args.from_upload_output,
                collection_title=args.title,
                collection_description=args.description,
                keywords=keywords,
                status=args.status
            )
        elif args.data_ids:
            # Create collection from data ID list
            data_ids = [id.strip() for id in args.data_ids.split(',') if id.strip()]
            collection_id = manager.create_collection_from_id_list(
                data_ids=data_ids,
                collection_title=args.title,
                collection_description=args.description,
                keywords=keywords,
                status=args.status
            )
        
        if collection_id:
            print(f"Collection created successfully: {collection_id}")
        else:
            print("Collection creation failed")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == '__main__':
    main()
