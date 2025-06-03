#!/usr/bin/env python3
"""
Nakala Batch Uploader using Nakala Connector

This script provides a command-line interface for batch uploading datasets to Nakala
using the Nakala Python Connector. It reads metadata from a CSV file and handles
file uploads and metadata creation in a structured way.
"""

import csv
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Any

from dotenv import load_dotenv, find_dotenv
from nakala_connector.api import NakalaAPI
from nakala_connector.exceptions import NakalaError

# Load environment variables from .env file
load_dotenv(find_dotenv(usecwd=True))

# Debug: Check if API key is loaded
api_key = os.getenv('NAKALA_API_KEY')
if not api_key:
    print("Error: NAKALA_API_KEY not found in environment variables")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Environment variables: {os.environ.get('NAKALA_API_KEY')}")
    sys.exit(1)

# Set up logging with debug level
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('nakala_uploader.log')
    ]
)

# Enable debug logging for requests and urllib3
logging.getLogger('requests').setLevel(logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

@dataclass
class UploaderConfig:
    """Configuration for the batch uploader."""
    api_key: str
    input_csv: str
    output_csv: str
    files_dir: str
    base_url: str = "https://api.nakala.fr"


class NakalaBatchUploader:
    """Handles batch uploading of datasets to Nakala using the Nakala Connector."""
    
    def __init__(self, config: UploaderConfig):
        """Initialize the uploader with configuration."""
        self.config = config
        print(f"Initializing NakalaAPI with API key: {config.api_key[:4]}...{config.api_key[-4:]} and base_url: {config.base_url}")
        self.nakala = NakalaAPI(api_key=config.api_key, base_url=config.base_url)
        print("NakalaAPI initialized successfully")
        
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
    
    def process_row(self, row: List[str]) -> Dict[str, Any]:
        """Process a single row from the CSV and return result dictionary."""
        try:
            # Unpack row data (adjust indices based on your CSV structure)
            filenames = row[0].split(';')
            status = row[1]
            datatype = row[2]
            title = row[3]
            authors = row[4].split(';')
            date = row[5]
            license_uri = row[6]
            description = row[7]
            keywords = row[8].split(';')
            datarights = row[9].split(';') if len(row) > 9 else []
            
            # Create metadata using the Nakala connector's builder
            builder = self.nakala.metadata_builder()
            
            # Set basic metadata
            builder.set_status(status)
            builder.add_title(title, lang="fr")
            builder.add_description(description, lang="fr")
            
            # Add creators
            for author in authors:
                if not author.strip():
                    continue
                    
                # Handle different name formats
                if ',' in author:
                    # Format: "Doe, John"
                    parts = [p.strip() for p in author.split(',')]
                    if len(parts) == 2:
                        creator_data = {
                            "familyName": parts[0],  # Using the correct field name
                            "givenName": parts[1]    # Using the correct field name
                        }
                    else:
                        # Fallback to name if format is unexpected
                        creator_data = {"name": author.strip()}
                else:
                    # Handle space-separated names
                    parts = author.strip().split()
                    if len(parts) >= 2:
                        creator_data = {
                            "givenName": ' '.join(parts[:-1]),  # Using the correct field name
                            "familyName": parts[-1]            # Using the correct field name
                        }
                    else:
                        creator_data = {"name": author.strip()}
                
                # Add the creator with the properly formatted data
                try:
                    builder.add_creator(creator_data)
                except Exception as e:
                    logger.error(f"Error adding creator '{author}': {e}")
                    # Fallback to using the name directly
                    builder.add_creator({"name": author.strip()})
            
            # Add subjects/keywords
            for keyword in keywords:
                if keyword.strip():
                    builder.add_subject(keyword.strip())
            
            # Add type
            builder.add_metadata_entry({
                "propertyUri": "http://nakala.fr/terms#type",
                "values": [{"value": datatype}]
            })
            
            # Add creation date
            if date:
                builder.add_metadata_entry({
                    "propertyUri": "http://nakala.fr/terms#created",
                    "values": [{"value": date}]
                })
            
            # Add license
            if license_uri:
                builder.add_metadata_entry({
                    "propertyUri": "http://nakala.fr/terms#license",
                    "values": [{"value": license_uri}]
                })
            
            # Process files
            uploaded_files = []
            for filename in filenames:
                if not filename.strip():
                    continue
                file_path = Path(self.config.files_dir) / filename.strip()
                logger.info(f"Uploading file: {file_path}")
                try:
                    # Upload file
                    file_data = self.nakala.files.upload_file(str(file_path))
                    uploaded_files.append({
                        'name': filename,
                        'sha1': file_data.get('sha1', ''),
                        'embargoed': file_data.get('embargoed', '')
                    })
                except NakalaError as e:
                    logger.error(f"Error uploading file {filename}: {e}")
                    return {
                        'identifier': '',
                        'files': ';'.join(f["name"] for f in uploaded_files),
                        'title': title,
                        'status': 'ERROR',
                        'response': str(e)
                    }
            # Create the data object
            metadata = builder.build()
            metadata['files'] = [
                {k: v for k, v in f.items() if k != 'embargoed' or v}
                for f in uploaded_files
            ]
            # Remove 'rights' if empty or not present
            if 'rights' in metadata and (not metadata['rights'] or metadata['rights'] == {}):
                del metadata['rights']
            # Fix creators and subjects: ensure values are objects with 'value' key
            for entry in metadata.get('metas', []):
                if entry['propertyUri'] in [
                    'http://purl.org/dc/terms/creator',
                    'http://purl.org/dc/terms/subject']:
                    entry['values'] = [
                        v if isinstance(v, dict) and 'value' in v else {'value': v}
                        for v in entry['values']
                    ]
            # Merge duplicate propertyUri entries
            metas = metadata.get('metas', [])
            merged = {}
            for entry in metas:
                uri = entry['propertyUri']
                if uri not in merged:
                    merged[uri] = {'propertyUri': uri, 'values': []}
                merged[uri]['values'].extend(entry['values'])
            metadata['metas'] = list(merged.values())
            logger.debug(f"Metadata payload being sent: {metadata}")
            # Create the data object in Nakala
            result = self.nakala.data.create_data(metadata)
            return {
                'identifier': result.get('payload', {}).get('id', ''),
                'files': ';'.join(f['name'] for f in uploaded_files),
                'title': title,
                'status': 'OK',
                'response': str(result)
            }
            
        except Exception as e:
            logger.error(f"Error processing row: {e}", exc_info=True)
            return {
                'identifier': '',
                'files': '',
                'title': row[3] if len(row) > 3 else 'Unknown',
                'status': 'ERROR',
                'response': str(e)
            }
    
    def run(self):
        """Run the batch upload process."""
        dataset = self.read_dataset()
        
        # Create output directory if it doesn't exist
        output_path = Path(self.config.output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['identifier', 'files', 'title', 'status', 'response'])
            
            for row in dataset:
                result = self.process_row(row)
                if result:
                    writer.writerow([
                        result['identifier'],
                        result['files'],
                        result['title'],
                        result['status'],
                        result['response']
                    ])
                    f.flush()  # Ensure data is written after each row


def load_config() -> UploaderConfig:
    """Load configuration from environment variables and command line."""
    # Load .env file if it exists
    env_path = find_dotenv(usecwd=True)
    if env_path:
        load_dotenv(env_path)
    
    # Get API key from environment
    api_key = os.getenv('NAKALA_API_KEY')
    if not api_key:
        logger.error("NAKALA_API_KEY environment variable not set")
        print("Please set the NAKALA_API_KEY environment variable or add it to a .env file")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Looking for .env file at: {os.path.join(os.getcwd(), '.env')}")
        sys.exit(1)
    
    # Get other configuration from command line or use defaults
    import argparse
    parser = argparse.ArgumentParser(description='Upload datasets to Nakala')
    parser.add_argument('--input', '-i', default='dataset.csv', help='Input CSV file')
    parser.add_argument('--output', '-o', default='output.csv', help='Output CSV file')
    parser.add_argument('--dir', '-d', default='.', help='Directory containing files to upload')
    parser.add_argument('--env', '-e', default='prod', choices=['test', 'prod'], 
                       help='Environment (test or prod)')
    
    args = parser.parse_args()
    
    # Force using test environment
    print("Forcing test environment (https://apitest.nakala.fr)")
    base_url = 'https://apitest.nakala.fr'
    
    # Print debug info
    print(f"Using API key: {api_key[:4]}...{api_key[-4:]}")
    print(f"Base URL: {base_url}")
    print(f"Input file: {args.input}")
    print(f"Files directory: {args.dir}")
    
    return UploaderConfig(
        api_key=api_key,
        input_csv=args.input,
        output_csv=args.output,
        files_dir=args.dir,
        base_url=base_url
    )


def main():
    """Main entry point."""
    try:
        config = load_config()
        uploader = NakalaBatchUploader(config)
        uploader.run()
        logger.info("Batch upload completed successfully")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
