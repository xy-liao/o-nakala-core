import csv
import os
import json
import logging
import argparse
from typing import Dict, Any, List
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
        logging.FileHandler('nakala_upload.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NakalaUploader:
    def __init__(self, api_url: str, api_key: str, dataset_path: str, image_dir: str):
        self.api_url = api_url
        self.api_key = api_key
        self.dataset_path = dataset_path
        self.image_dir = image_dir
        self.configuration = openapi_client.Configuration(host=api_url)
        self.configuration.api_key['apiKey'] = api_key
        self.valid_group_ids = ['de0f2a9b-a198-48a4-8074-db5120187a16']

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def upload_file(self, file_path: str, filename: str) -> Dict[str, Any]:
        """Upload a single file to Nakala with retry mechanism."""
        try:
            payload: Dict[str, Any] = {}
            files = [
                ('file', (filename, open(file_path, 'rb'), 'image/jpeg'))
            ]
            headers = {'X-API-KEY': self.api_key}
            
            response = requests.request(
                'POST',
                f"{self.api_url}/datas/uploads",
                headers=headers,
                data=payload,
                files=files
            )
            
            if response.status_code == 201:
                file_info = response.json()
                file_info['embargoed'] = datetime.now().strftime("%Y-%m-%d")
                return file_info
            else:
                raise ApiException(status=response.status_code, reason=response.text)
                
        except Exception as e:
            logger.error(f"Error uploading file {filename}: {e}")
            raise

    def validate_file_exists(self, filename: str) -> bool:
        """Validate that a file exists in the image directory."""
        file_path = os.path.join(self.image_dir, filename)
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        return True

    def prepare_metadata(self, data: List[str]) -> List[Dict[str, Any]]:
        """Prepare metadata for a dataset entry."""
        metas = []
        
        # Type metadata
        metas.append({
            "value": data[2],
            "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
            "propertyUri": "http://nakala.fr/terms#type"
        })
        
        # Title metadata
        metas.append({
            "value": data[3],
            "lang": "fr",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://nakala.fr/terms#title"
        })
        
        # Authors metadata
        for author in data[4].split(';'):
            surname_givenname = author.split(',')
            if len(surname_givenname) == 2:
                author_data = {
                    "givenname": surname_givenname[1].strip(),
                    "surname": surname_givenname[0].strip()
                }
                metas.append({
                    "value": [author_data],
                    "propertyUri": "http://nakala.fr/terms#creator"
                })
        
        # Add other metadata
        metas.extend([
            {
                "value": data[5],
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#created"
            },
            {
                "value": data[6],
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#license"
            },
            {
                "value": data[7],
                "lang": "fr",
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/description"
            }
        ])
        
        # Keywords metadata
        for keyword in data[8].split(';'):
            if keyword:
                metas.append({
                    "value": keyword,
                    "lang": "fr",
                    "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                    "propertyUri": "http://purl.org/dc/terms/subject"
                })
        
        return metas

    def prepare_rights(self, datarights: List[str]) -> List[Dict[str, Any]]:
        """Prepare rights information for a dataset entry."""
        rights = []
        for dataright in datarights:
            if dataright:
                right_parts = dataright.split(',')
                if len(right_parts) == 2:
                    group_id = right_parts[0].strip()
                    if group_id in self.valid_group_ids:
                        rights.append({
                            "id": group_id,
                            "role": right_parts[1].strip()
                        })
        return rights

    def process_dataset(self) -> None:
        """Process the entire dataset and upload to Nakala."""
        output_path = 'output.csv'
        with open(output_path, 'w', newline='') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['identifier', 'files', 'title', 'status', 'response'])
            
            with open(self.dataset_path, newline='') as f:
                reader = csv.reader(f)
                dataset = list(reader)
            dataset.pop(0)  # Remove header row
            
            total_entries = len(dataset)
            for num, data in enumerate(dataset, 1):
                logger.info(f"Processing entry {num}/{total_entries}: {data[3]}")
                
                output_data = ['', '', data[3], '', '']
                nakala_files = []
                output_files = []
                
                try:
                    # Process files
                    filenames = data[0].split(';')
                    for filename in filenames:
                        if not self.validate_file_exists(filename):
                            continue
                            
                        logger.info(f"Uploading file: {filename}")
                        file_info = self.upload_file(
                            os.path.join(self.image_dir, filename),
                            filename
                        )
                        nakala_files.append(file_info)
                        output_files.append(f"{filename},{file_info['sha1']}")
                    
                    # Prepare metadata and rights
                    metas = self.prepare_metadata(data)
                    rights = self.prepare_rights(data[9].split(';'))
                    
                    # Create data payload
                    data_payload = {
                        "status": data[1],
                        "files": nakala_files,
                        "metas": metas,
                        "rights": rights
                    }
                    
                    # Upload to Nakala
                    headers = {
                        'Content-Type': 'application/json',
                        'X-API-KEY': self.api_key
                    }
                    response = requests.request(
                        'POST',
                        f"{self.api_url}/datas",
                        headers=headers,
                        data=json.dumps(data_payload)
                    )
                    
                    if response.status_code == 201:
                        result = response.json()
                        logger.info(f"Successfully created data: {result['payload']['id']}")
                        output_data[0] = result["payload"]["id"]
                        output_data[1] = ';'.join(output_files)
                        output_data[3] = 'OK'
                        output_data[4] = response.text
                    else:
                        raise ApiException(status=response.status_code, reason=response.text)
                        
                except Exception as e:
                    logger.error(f"Error processing entry: {e}")
                    output_data[3] = 'ERROR'
                    output_data[4] = str(e)
                
                output_writer.writerow(output_data)

def main():
    parser = argparse.ArgumentParser(description='Upload datasets to Nakala')
    parser.add_argument('--api-url', default='https://apitest.nakala.fr',
                      help='Nakala API URL')
    parser.add_argument('--api-key', required=True,
                      help='Nakala API key')
    parser.add_argument('--dataset', default='simple-dataset/dataset.csv',
                      help='Path to dataset CSV file')
    parser.add_argument('--image-dir', default='simple-dataset/img',
                      help='Directory containing images')
    
    args = parser.parse_args()
    
    uploader = NakalaUploader(
        api_url=args.api_url,
        api_key=args.api_key,
        dataset_path=args.dataset,
        image_dir=args.image_dir
    )
    
    try:
        uploader.process_dataset()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == '__main__':
    main()
