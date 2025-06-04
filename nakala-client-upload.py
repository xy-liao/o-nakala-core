import csv
import os
import json
import logging
import argparse
from typing import Dict, Any, List, Optional
import requests
from datetime import datetime
import openapi_client
from openapi_client.rest import ApiException
from tenacity import retry, stop_after_attempt, wait_exponential
import mimetypes
from pathlib import Path

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

class FileTypeDetector:
    """Detects and categorizes file types based on extensions and MIME types."""
    
    def __init__(self):
        self.type_mapping = {
            'code': ['.py', '.js', '.java', '.cpp', '.h', '.cs', '.php'],
            'data': ['.csv', '.json', '.xml', '.xlsx', '.db', '.sql'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp'],
            'presentations': ['.ppt', '.pptx', '.key', '.odp']
        }
    
    def detect_type(self, file_path: str) -> str:
        """Detect the type of file based on extension and MIME type."""
        ext = os.path.splitext(file_path)[1].lower()
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # Check extension mapping
        for type_name, extensions in self.type_mapping.items():
            if ext in extensions:
                return type_name
        
        # Fallback to MIME type
        if mime_type:
            if mime_type.startswith('image/'):
                return 'images'
            elif mime_type.startswith('text/'):
                return 'documents'
            elif mime_type.startswith('application/pdf'):
                return 'documents'
        
        return 'other'

class MetadataGenerator:
    """Generates metadata from folder structure and file information."""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.type_detector = FileTypeDetector()
    
    def generate_metadata(self, file_path: str, folder_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate metadata for a file based on its path and folder configuration."""
        relative_path = os.path.relpath(file_path, self.base_path)
        file_type = self.type_detector.detect_type(file_path)
        
        # Get folder-specific metadata
        folder_metadata = folder_config.get(os.path.dirname(relative_path), {})
        
        # Generate basic metadata
        metadata = {
            "type": file_type,
            "title": os.path.splitext(os.path.basename(file_path))[0],
            "created": datetime.now().strftime("%Y-%m-%d"),
            "license": folder_metadata.get('license', 'CC-BY'),
            "description": folder_metadata.get('description', ''),
            "keywords": folder_metadata.get('keywords', '').split(';'),
            "rights": folder_metadata.get('rights', '').split(';')
        }
        
        return metadata

class FolderDatasetProcessor:
    """Handles folder-based dataset processing."""
    
    def __init__(self, base_path: str, folder_config_path: str):
        self.base_path = base_path
        self.folder_config = self._load_folder_config(folder_config_path)
        self.metadata_generator = MetadataGenerator(base_path)
    
    def _load_folder_config(self, config_path: str) -> Dict[str, Any]:
        """Load folder configuration from CSV file."""
        config = {}
        with open(config_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                folder_path = row['file'].rstrip('/')
                config[folder_path] = {
                    'status': row['status'],
                    'type': row['type'],
                    'title': row['title'],
                    'description': row['description'],
                    'license': row['license'],
                    'keywords': row['keywords'],
                    'rights': row['rights'],
                    'author': row['author'],
                    'contributor': row['contributor'],
                    'date': row['date'],
                    'language': row['language'],
                    'temporal': row['temporal'],
                    'spatial': row['spatial']
                }
        return config
    
    def process_folder(self) -> List[Dict[str, Any]]:
        """Process all files in the folder structure, grouped by folder."""
        folder_files = {}  # Dictionary to group files by folder
        
        for root, _, files in os.walk(self.base_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Get the relative path from the base directory
                    rel_path = os.path.relpath(os.path.dirname(file_path), self.base_path)
                    if rel_path in self.folder_config:
                        if rel_path not in folder_files:
                            folder_files[rel_path] = {
                                'metadata': self.folder_config[rel_path].copy(),
                                'files': []
                            }
                        folder_files[rel_path]['files'].append(file_path)
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {e}")
        
        # Convert the grouped files into results
        results = []
        for folder_path, folder_data in folder_files.items():
            results.append({
                'folder_path': folder_path,
                'metadata': folder_data['metadata'],
                'files': folder_data['files']
            })
        
        return results

class NakalaUploader:
    def __init__(self, api_url: str, api_key: str, dataset_path: str, image_dir: str, mode: str = 'csv', folder_config: Optional[str] = None):
        self.api_url = api_url
        self.api_key = api_key
        self.dataset_path = dataset_path
        self.image_dir = image_dir
        self.mode = mode
        self.folder_config = folder_config
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
        """Process the dataset based on the selected mode."""
        if self.mode == 'csv':
            self._process_csv_dataset()
        elif self.mode == 'folder':
            self._process_folder_dataset()
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def _process_folder_dataset(self) -> None:
        """Process a folder-based dataset."""
        processor = FolderDatasetProcessor(self.dataset_path, self.folder_config)
        results = processor.process_folder()
        
        output_path = 'output.csv'
        with open(output_path, 'w', newline='') as output:
            output_writer = csv.writer(output)
            output_writer.writerow(['identifier', 'files', 'title', 'status', 'response'])
            
            for result in results:
                try:
                    # Upload all files in the folder
                    file_infos = []
                    for file_path in result['files']:
                        file_info = self.upload_file(
                            file_path,
                            os.path.basename(file_path)
                        )
                        file_infos.append(file_info)
                    
                    # Prepare metadata and rights
                    metadata = result['metadata']
                    metas = self.prepare_metadata_from_dict(metadata)
                    rights = self.prepare_rights(metadata.get('rights', '').split(';'))
                    
                    # Create data payload with all files
                    data_payload = {
                        "status": metadata.get('status', 'pending'),
                        "files": file_infos,
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
                        result_json = response.json()
                        logger.info(f"Successfully created data: {result_json['payload']['id']}")
                        
                        # Write all files to output
                        file_list = ','.join([f"{os.path.basename(f)},{fi['sha1']}" for f, fi in zip(result['files'], file_infos)])
                        output_writer.writerow([
                            result_json["payload"]["id"],
                            file_list,
                            metadata.get('title', 'unknown'),
                            'OK',
                            response.text
                        ])
                    else:
                        raise ApiException(status=response.status_code, reason=response.text)
                    
                except Exception as e:
                    logger.error(f"Error processing folder {result.get('folder_path', 'unknown')}: {e}")
                    file_list = ','.join([os.path.basename(f) for f in result.get('files', [])])
                    output_writer.writerow([
                        '',
                        file_list,
                        result.get('metadata', {}).get('title', 'unknown'),
                        'ERROR',
                        str(e)
                    ])

    def prepare_metadata_from_dict(self, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepare metadata from a dictionary."""
        metas = []
        
        # Type metadata
        metas.append({
            "value": metadata['type'],
            "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
            "propertyUri": "http://nakala.fr/terms#type"
        })
        
        # Title metadata (handle multilingual titles)
        title_parts = metadata['title'].split('|')
        for title_part in title_parts:
            lang, title = title_part.split(':', 1)
            metas.append({
                "value": title.strip(),
                "lang": lang.strip(),
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#title"
            })
        
        # Author metadata
        for author in metadata['author'].split(';'):
            if author:
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
                "value": metadata['date'],
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#created"
            },
            {
                "value": metadata['license'],
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#license"
            }
        ])
        
        # Description metadata (handle multilingual descriptions)
        desc_parts = metadata['description'].split('|')
        for desc_part in desc_parts:
            lang, desc = desc_part.split(':', 1)
            metas.append({
                "value": desc.strip(),
                "lang": lang.strip(),
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/description"
            })
        
        # Keywords metadata (handle multilingual keywords)
        keyword_parts = metadata['keywords'].split('|')
        for keyword_part in keyword_parts:
            lang, keywords = keyword_part.split(':', 1)
            for keyword in keywords.split(';'):
                if keyword:
                    metas.append({
                        "value": keyword.strip(),
                        "lang": lang.strip(),
                        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                        "propertyUri": "http://purl.org/dc/terms/subject"
                    })
        
        return metas

def main():
    parser = argparse.ArgumentParser(description='Upload datasets to Nakala')
    parser.add_argument('--api-url', default='https://apitest.nakala.fr',
                      help='Nakala API URL')
    parser.add_argument('--api-key', required=True,
                      help='Nakala API key')
    parser.add_argument('--dataset', default='simple-dataset/dataset.csv',
                      help='Path to dataset CSV file or folder')
    parser.add_argument('--image-dir', default='simple-dataset/img',
                      help='Directory containing images')
    parser.add_argument('--mode', choices=['csv', 'folder'], default='csv',
                      help='Upload mode: csv (current) or folder (new)')
    parser.add_argument('--folder-config',
                      help='Path to folder configuration CSV (for folder mode)')
    
    args = parser.parse_args()
    
    uploader = NakalaUploader(
        api_url=args.api_url,
        api_key=args.api_key,
        dataset_path=args.dataset,
        image_dir=args.image_dir,
        mode=args.mode,
        folder_config=args.folder_config
    )
    
    try:
        uploader.process_dataset()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == '__main__':
    main()
