# Nakala Connector Design Based on the Official Notebook

After reviewing the notebook, I can see that it demonstrates a step-by-step process for batch uploading data to Nakala, starting from a CSV file with metadata and associated files. Let me incorporate these insights into a more focused connector design.

## Core Design Principles

1. **Workflow-Based Architecture**: The connector should follow the natural workflow shown in the notebook:
    - File upload to temporary storage
    - Metadata construction
    - Data object creation with files and metadata
    - Collection assignment
    - Rights management
2. **CSV Integration**: Since batch uploads via CSV are a common use case, the connector should have built-in support for this workflow.
3. **Vocabulary Mapping**: The connector should handle mapping between user-friendly terms and Nakala's URI-based vocabulary system.

## Unified Connector Structure

I still recommend a unified connector, but with a clearer structure that reflects the Nakala API's workflow:

```
nakala_connector/
├── __init__.py
├── client.py                # Main client class with auth
├── models/                  # Data models
│   ├── __init__.py
│   ├── metadata.py          # Metadata models (handles all metadata types)
│   ├── file.py              # File handling models
│   └── rights.py            # Rights and permissions models
├── services/                # Logical service components
│   ├── __init__.py
│   ├── upload_service.py    # Handles file uploads
│   ├── data_service.py      # Handles data objects
│   ├── collection_service.py # Handles collections
│   ├── search_service.py    # Handles search functionality
│   └── vocabulary_service.py # Handles vocabulary lookups
├── batch/                   # Batch processing functionality
│   ├── __init__.py
│   ├── csv_importer.py      # CSV import logic
│   └── mappings.py          # Vocabulary mapping logic
├── exceptions.py            # Custom exceptions
├── utils.py                 # Utility functions
└── constants.py             # API endpoints, vocabulary URIs, etc.

```

## Key Components Based on the Notebook

### 1. File Upload Service

The notebook shows a clear pattern for uploading files to Nakala's temporary storage:

```python
class UploadService:
    def __init__(self, client):
        self.client = client

    def upload_file(self, file_path, mime_type=None):
        """Upload a file to Nakala temporary storage."""
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, mime_type)}
            headers = {'X-API-KEY': self.client.api_key}
            response = requests.post(
                f"{self.client.base_url}/datas/uploads",
                headers=headers,
                files=files
            )

            if response.status_code == 201:
                return response.json()
            else:
                raise NakalaUploadError(f"Upload failed: {response.text}")

    def set_embargo(self, file_data, embargo_date=None):
        """Add embargo date to file data returned from upload."""
        file_data["embargoed"] = embargo_date or datetime.now().strftime("%Y-%m-%d")
        return file_data

```

### 2. Metadata Construction

The notebook shows a detailed approach to constructing metadata. We can encapsulate this in a metadata builder:

```python
class MetadataBuilder:
    """Helper class for building Nakala metadata structures."""

    @staticmethod
    def create_type(type_value, mapping=None):
        """Create a type metadata entry."""
        if mapping and type_value in mapping:
            type_value = mapping[type_value]

        return {
            "value": type_value,
            "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
            "propertyUri": "http://nakala.fr/terms#type"
        }

    @staticmethod
    def create_title(title, language="fr"):
        """Create a title metadata entry."""
        return {
            "value": title,
            "lang": language,
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://nakala.fr/terms#title"
        }

    @staticmethod
    def create_creator(surname=None, givenname=None, orcid=None):
        """Create a creator metadata entry."""
        # For anonymous creators
        if surname is None and givenname is None:
            return {
                "value": None,
                "propertyUri": "http://nakala.fr/terms#creator"
            }

        value = {
            "surname": surname,
            "givenname": givenname
        }

        if orcid:
            value["orcid"] = orcid

        return {
            "value": value,
            "propertyUri": "http://nakala.fr/terms#creator"
        }

    @staticmethod
    def create_created(date_value):
        """Create a created date metadata entry."""
        # For unknown dates
        if not date_value:
            return {
                "value": None,
                "propertyUri": "http://nakala.fr/terms#created"
            }

        return {
            "value": date_value,
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://nakala.fr/terms#created"
        }

    @staticmethod
    def create_license(license_value):
        """Create a license metadata entry."""
        return {
            "value": license_value,
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://nakala.fr/terms#license"
        }

    @staticmethod
    def create_description(description, language="fr"):
        """Create a description metadata entry."""
        return {
            "value": description,
            "lang": language,
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://purl.org/dc/terms/description"
        }

    @staticmethod
    def create_subject(keyword, language=None, is_uri=False):
        """Create a subject (keyword) metadata entry."""
        meta = {
            "value": keyword,
            "propertyUri": "http://purl.org/dc/terms/subject"
        }

        if is_uri:
            meta["typeUri"] = "http://www.w3.org/2001/XMLSchema#anyURI"
        else:
            meta["typeUri"] = "http://www.w3.org/2001/XMLSchema#string"
            if language:
                meta["lang"] = language

        return meta

```

### 3. Data Service for Creating Data Objects

Building on the notebook's approach to creating data objects:

```python
class DataService:
    def __init__(self, client):
        self.client = client
        self.upload_service = UploadService(client)

    def create_data(self, metadata, files=None, status="pending", rights=None, collection_ids=None):
        """Create a data object in Nakala."""
        payload = {
            "status": status,
            "metas": metadata
        }

        if files:
            payload["files"] = files

        if rights:
            payload["rights"] = rights

        if collection_ids:
            payload["collectionsIds"] = collection_ids

        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.client.api_key
        }

        response = requests.post(
            f"{self.client.base_url}/datas",
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise NakalaDataCreationError(f"Data creation failed: {response.text}")

    def create_data_with_files(self, metadata, file_paths, status="pending",
                              rights=None, collection_ids=None, embargo_date=None):
        """Upload files and create a data object in one operation."""
        uploaded_files = []

        for file_path in file_paths:
            try:
                # Upload the file
                file_data = self.upload_service.upload_file(file_path)

                # Add embargo if specified
                file_data = self.upload_service.set_embargo(file_data, embargo_date)

                uploaded_files.append(file_data)
            except Exception as e:
                raise NakalaFileUploadError(f"Failed to upload {file_path}: {str(e)}")

        # Create the data object with the uploaded files
        return self.create_data(
            metadata=metadata,
            files=uploaded_files,
            status=status,
            rights=rights,
            collection_ids=collection_ids
        )

```

### 4. CSV Batch Processing

Based on the notebook's approach to CSV batch processing:

```python
class CSVImporter:
    def __init__(self, client, mappings=None):
        self.client = client
        self.data_service = DataService(client)
        self.metadata_builder = MetadataBuilder()
        self.mappings = mappings or {}

    def import_from_csv(self, csv_file, file_dir, output_file=None, delimiter=','):
        """Import data from a CSV file."""
        # Read CSV file
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=delimiter)
            headers = next(reader)  # Read header row
            dataset = list(reader)

        # Setup output file if specified
        output_writer = None
        if output_file:
            output = open(output_file, 'w', newline='', encoding='utf-8')
            output_writer = csv.writer(output)
            output_writer.writerow(['identifier', 'files', 'title', 'status', 'response'])

        results = []

        # Process each row
        for num, row in enumerate(dataset):
            try:
                # Process the row according to your CSV structure
                # This is where you'd adapt to your specific CSV format
                result = self._process_row(num, row, headers, file_dir)
                results.append(result)

                if output_writer:
                    output_writer.writerow([
                        result.get('identifier', ''),
                        ';'.join(result.get('files', [])),
                        result.get('title', ''),
                        result.get('status', 'ERROR'),
                        result.get('response', '')
                    ])
            except Exception as e:
                # Log error and continue with next row
                print(f"Error processing row {num}: {str(e)}")
                if output_writer:
                    output_writer.writerow(['', '', row[3] if len(row) > 3 else '', 'ERROR', str(e)])

        if output_file:
            output.close()

        return results

    def _process_row(self, num, row, headers, file_dir):
        """Process a single row from the CSV file."""
        # Extract data from row based on headers
        # Map data to Nakala metadata format
        # Upload files and create data object
        # This method would be customized based on your CSV structure

```

### 5. Main Client Class

Putting it all together in the main client class:

```python
class NakalaClient:
    """Client for the NAKALA API."""

    def __init__(self, api_key=None, base_url="https://api.nakala.fr"):
        self.api_key = api_key
        self.base_url = base_url

        # Initialize services
        self.upload = UploadService(self)
        self.data = DataService(self)
        self.collection = CollectionService(self)
        self.search = SearchService(self)
        self.vocabulary = VocabularyService(self)

        # Initialize batch processor
        self.batch = CSVImporter(self)

    def get_metadata_builder(self):
        """Get a metadata builder helper."""
        return MetadataBuilder()

```

## Example Usage

Based on the notebook's workflow, here's how your connector might be used:

```python
# Initialize client
client = NakalaClient(api_key="your_api_key")

# Option 1: Manual upload and data creation
# Upload a file
file_data = client.upload.upload_file("path/to/image.jpg")
file_data = client.upload.set_embargo(file_data, "2023-12-31")

# Build metadata
builder = client.get_metadata_builder()
metadata = [
    builder.create_type("Image", mapping={"Image": "http://purl.org/coar/resource_type/c_c513"}),
    builder.create_title("My Image Title"),
    builder.create_creator("Doe", "John"),
    builder.create_created("2023-01-01"),
    builder.create_license("CC-BY-4.0"),
    builder.create_description("An example image")
]

# Create data with the file
result = client.data.create_data(
    metadata=metadata,
    files=[file_data],
    status="pending",
    collection_ids=["10.34847/nkl.12345678"]
)

# Option 2: Batch import from CSV
result = client.batch.import_from_csv(
    csv_file="metadata.csv",
    file_dir="files/",
    output_file="import_results.csv"
)

```

## Vocabulary Mappings

The notebook demonstrates the importance of mapping user-friendly terms to Nakala's vocabulary URIs. Your connector should include default mappings:

```python
DEFAULT_TYPE_MAPPINGS = {
    "Article de journal": "http://purl.org/coar/resource_type/c_6501",
    "Cours": "http://purl.org/coar/resource_type/c_e059",
    "Image": "http://purl.org/coar/resource_type/c_c513",
    "Poster": "http://purl.org/coar/resource_type/c_6670",
    "Présentation": "http://purl.org/coar/resource_type/c_c94f",
    "Set de données": "http://purl.org/coar/resource_type/c_ddb1",
    "Texte": "http://purl.org/coar/resource_type/c_18cf",
    # Add more mappings based on Nakala's vocabulary
}

```

## Conclusion and Recommendations

After reviewing the notebook, I still recommend a unified connector approach, but with a structure that more closely follows the workflow demonstrated in the notebook:

1. **Build around the upload-metadata-create workflow**: The connector should make this common pattern easy to use.
2. **Emphasize batch processing**: The CSV import functionality is clearly a core use case and should be a first-class feature.
3. **Provide helpers for metadata construction**: The notebook shows that building correct metadata is crucial and potentially complex, especially for creators, dates, and multilingual metadata.
4. **Support vocabulary mapping**: Include default mappings for common terms to Nakala URIs and make it easy to extend with custom mappings.
5. **Handle errors and reporting**: The notebook demonstrates good practices for error handling and reporting during batch imports.

This approach would provide a connector that is both user-friendly for common tasks and flexible enough for advanced usage. By following the patterns established in the official notebook, the connector will be more intuitive for users already familiar with Nakala's API.
