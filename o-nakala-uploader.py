#!/usr/bin/env python3
"""
Nakala API Batch Uploader

This script uploads datasets to the Nakala API from a CSV file.
Each dataset can contain multiple files and metadata.
"""

import csv
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

import requests
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('nakala_upload.log')
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class NakalaConfig:
    """Configuration for Nakala API."""
    api_url: str
    api_key: str
    input_csv: str
    output_csv: str
    image_dir: str

class NakalaUploader:
    """Handles the upload process to Nakala API."""
    
    def __init__(self, config: NakalaConfig):
        self.config = config
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': config.api_key
        }
        
    def read_dataset(self) -> List[List[str]]:
        """Read the input CSV file."""
        try:
            with open(self.config.input_csv, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                dataset = list(reader)
                dataset.pop(0)  # Remove header row
                return dataset
        except FileNotFoundError:
            logger.error(f"Input file not found: {self.config.input_csv}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error reading input file: {e}")
            sys.exit(1)

    def upload_file(self, filename: str) -> Optional[Dict]:
        """Upload a single file to Nakala."""
        file_path = Path(self.config.image_dir) / filename
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None

        try:
            payload = {}
            postfiles = [('file', (filename, open(file_path, 'rb'), 'image/jpeg'))]
            response = requests.post(
                f"{self.config.api_url}/datas/uploads",
                headers={'X-API-KEY': self.config.api_key},
                data=payload,
                files=postfiles
            )
            
            if response.status_code == 201:
                file_data = response.json()
                file_data["embargoed"] = time.strftime("%Y-%m-%d")
                return file_data
            else:
                logger.error(f"Upload failed for {filename}: {response.text}")
                return None
                
        except RequestException as e:
            logger.error(f"Network error uploading {filename}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error uploading {filename}: {e}")
            return None

    def create_metadata(self, data: List[str]) -> Dict:
        """Create metadata structure for a dataset."""
        filenames = data[0].split(';')
        status = data[1]
        datatype = data[2]
        title = data[3]
        authors = data[4].split(';')
        date = data[5]
        license = data[6]
        description = data[7]
        keywords = data[8].split(';')
        datarights = data[9].split(';')

        metas = [
            {
                "value": datatype,
                "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
                "propertyUri": "http://nakala.fr/terms#type"
            },
            {
                "value": title,
                "lang": "fr",
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#title"
            }
        ]

        # Add authors
        for author in authors:
            surname, givenname = author.split(',')
            metas.append({
                "value": {
                    "givenname": givenname,
                    "surname": surname
                },
                "propertyUri": "http://nakala.fr/terms#creator"
            })

        # Add other metadata
        metas.extend([
            {
                "value": date,
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#created"
            },
            {
                "value": license,
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#license"
            },
            {
                "value": description,
                "lang": "fr",
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/description"
            }
        ])

        # Add keywords
        for keyword in keywords:
            metas.append({
                "value": keyword,
                "lang": "fr",
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/subject"
            })

        # Process rights
        rights = []
        for dataright in datarights:
            if ',' in dataright:
                right_id, role = dataright.split(',')
                rights.append({"id": right_id, "role": role})

        return {
            "status": status,
            "metas": metas,
            "rights": rights
        }

    def process_dataset(self, num: int, data: List[str]) -> Optional[Dict]:
        """Process a single dataset."""
        logger.info(f"Processing dataset {num}: {data[3]}")
        
        # Upload files
        files = []
        output_files = []
        for filename in data[0].split(';'):
            logger.info(f"Uploading file: {filename}")
            file_data = self.upload_file(filename)
            if file_data:
                files.append(file_data)
                output_files.append(f"{filename},{file_data['sha1']}")
            else:
                return None

        # Create metadata
        metadata = self.create_metadata(data)
        metadata["files"] = files

        # Upload dataset
        try:
            response = requests.post(
                f"{self.config.api_url}/datas",
                headers=self.headers,
                data=json.dumps(metadata)
            )
            
            if response.status_code == 201:
                result = response.json()
                logger.info(f"Dataset {num} created successfully: {result['payload']['id']}")
                return {
                    "identifier": result["payload"]["id"],
                    "files": ";".join(output_files),
                    "title": data[3],
                    "status": "OK",
                    "response": response.text
                }
            else:
                logger.error(f"Failed to create dataset {num}: {response.text}")
                return {
                    "identifier": "",
                    "files": ";".join(output_files),
                    "title": data[3],
                    "status": "ERROR",
                    "response": response.text
                }
                
        except Exception as e:
            logger.error(f"Error creating dataset {num}: {e}")
            return None

    def run(self):
        """Run the upload process."""
        dataset = self.read_dataset()
        
        with open(self.config.output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['identifier', 'files', 'title', 'status', 'response'])
            
            for num, data in enumerate(dataset):
                result = self.process_dataset(num, data)
                if result:
                    writer.writerow([
                        result["identifier"],
                        result["files"],
                        result["title"],
                        result["status"],
                        result["response"]
                    ])

def main():
    """Main entry point."""
    config = NakalaConfig(
        api_url='https://apitest.nakala.fr',
        api_key='aae99aba-476e-4ff2-2886-0aaf1bfa6fd2',
        input_csv='simple-dataset/dataset.csv',
        output_csv='output.csv',
        image_dir='simple-dataset/img'
    )
    
    uploader = NakalaUploader(config)
    uploader.run()

if __name__ == '__main__':
    main()