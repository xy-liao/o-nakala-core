"""
Basic usage example for the Nakala Python Connector.

This script demonstrates how to use the Nakala API client to:
1. Initialize the client
2. Create metadata for a data object
3. Upload files
4. Create a data object
5. Search for data objects
6. Create and manage collections
"""

import os
from datetime import datetime
from dotenv import load_dotenv

# Import the Nakala API client
from nakala_connector import NakalaAPI, NakalaError

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("NAKALA_API_KEY")
    if not api_key:
        print("Error: NAKALA_API_KEY environment variable not set")
        print("Please create a .env file with your API key:")
        print("NAKALA_API_KEY=your-api-key-here")
        return
    
    # Initialize the Nakala API client
    with NakalaAPI(api_key=api_key) as nakala:
        try:
            print("=== Nakala API Client Initialized ===\n")
            
            # Example 1: Create a simple data object with metadata
            print("=== Example 1: Create a Data Object ===")
            
            # Create a metadata builder
            builder = nakala.metadata_builder()
            
            # Add required metadata
            builder.add_title("Sample Research Data - " + datetime.now().strftime("%Y-%m-%d %H:%M"))
            builder.add_description("This is a sample dataset uploaded using the Nakala Python Connector.")
            
            # Add creator information
            builder.add_creator({
                "given_name": "John",
                "family_name": "Doe",
                "affiliation": "École française d'Extrême-Orient",
                "identifier": "https://orcid.org/0000-0000-0000-0000"
            })
            
            # Add a subject
            builder.add_subject({
                "value": "Digital Humanities",
                "scheme": "keywords"
            })
            
            # Set resource type
            builder.add_metadata_entry({
                "propertyUri": "http://purl.org/dc/terms/type",
                "values": [{"value": "Dataset"}]
            })
            
            # Build the metadata
            metadata = builder.build()
            
            # Print the metadata (for demonstration)
            print("\nGenerated Metadata:")
            print("-----------------")
            for meta in metadata["metas"]:
                print(f"{meta['propertyUri']}: {meta['values']}")
            
            # Example 2: Upload a file (commented out to prevent accidental uploads)
            """
            print("\n=== Example 2: Upload a File ===")
            file_path = "path/to/your/file.pdf"
            
            if os.path.exists(file_path):
                print(f"Uploading file: {file_path}")
                upload_result = nakala.files.upload_file(file_path)
                print(f"File uploaded successfully. SHA1: {upload_result.get('sha1')}")
                
                # Add the file to our metadata
                metadata["files"] = [{
                    "sha1": upload_result["sha1"],
                    "filename": os.path.basename(file_path)
                }]
            else:
                print(f"File not found: {file_path}")
                print("Skipping file upload...")
            """
            
            # Example 3: Search for data objects (commented out to prevent accidental searches)
            """
            print("\n=== Example 3: Search for Data Objects ===")
            search_results = nakala.search_data(
                query="digital humanities",
                limit=3
            )
            
            print(f"Found {search_results.get('numFound', 0)} results")
            if search_results.get('docs'):
                print("\nFirst 3 results:")
                for i, doc in enumerate(search_results['docs'][:3], 1):
                    print(f"{i}. {doc.get('title', 'Untitled')} (ID: {doc.get('id')})")
            """
            
            # Example 4: Create a collection (commented out to prevent accidental creation)
            """
            print("\n=== Example 4: Create a Collection ===")
            collection = nakala.collections.create_collection(
                title="My Research Collection",
                description="A collection of research data files",
                metadata={"project": "Digital Humanities Research"}
            )
            
            print(f"Created collection: {collection.get('title')} (ID: {collection.get('id')})")
            """
            
            print("\n=== Examples Complete ===")
            
        except NakalaError as e:
            print(f"Error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")

if __name__ == "__main__":
    main()
