# Common Utilities Reference

## Overview

The `nakala_client.common` package provides shared utilities, configuration management, and exception handling for all Nakala client modules. This reference documents the public API and usage patterns.

## 📦 Package Structure

```
nakala_client/common/
├── __init__.py          # Package exports and version info
├── utils.py             # Core utility functions
├── config.py            # Configuration classes
└── exceptions.py        # Custom exception classes
```

## 🔧 Core Utilities (`utils.py`)

### Metadata Processing

#### `prepare_metadata(metadata_dict: Dict, default_lang: str = 'fr') -> List[Dict]`

Converts a metadata dictionary to Nakala API format.

**Parameters:**
- `metadata_dict`: Dictionary containing metadata fields
- `default_lang`: Default language for fields without explicit language

**Returns:** List of metadata objects in Nakala API format

**Example:**
```python
from nakala_client.common.utils import prepare_metadata

metadata = {
    'title': 'Research Dataset',
    'title_en': 'Research Dataset',
    'title_fr': 'Jeu de données de recherche',
    'author': 'Doe, John',
    'date': '2024-01-15',
    'license': 'CC-BY-4.0'
}

nakala_metadata = prepare_metadata(metadata)
# Returns list of Nakala API metadata objects
```

#### `parse_multilingual_field(value: str, field_name: str) -> List[Dict]`

Parses multilingual field values with language suffixes.

**Parameters:**
- `value`: Field value (may contain language markers)
- `field_name`: Base field name (e.g., 'title', 'description')

**Returns:** List of language-specific metadata objects

**Example:**
```python
# Parse field with multiple languages
title_metadata = parse_multilingual_field(
    "English Title|Titre Français", 
    "title"
)
# Returns metadata for both English and French titles
```

### File Operations

#### `upload_file_to_nakala(api_client: NakalaAPIClient, file_path: Path) -> Dict`

Uploads a single file to Nakala temporary storage.

**Parameters:**
- `api_client`: Configured Nakala API client
- `file_path`: Path to file to upload

**Returns:** File metadata including SHA-1 hash

**Raises:**
- `FileValidationError`: If file doesn't exist or isn't readable
- `NakalaAPIError`: If upload fails

**Example:**
```python
from pathlib import Path
from nakala_client.common.utils import upload_file_to_nakala, create_api_client

api_client = create_api_client(config)
file_info = upload_file_to_nakala(api_client, Path("./image.jpg"))
print(f"Uploaded: {file_info['sha1']}")
```

#### `validate_file_exists(file_path: Path, base_dir: Path) -> Path`

Validates file existence and returns absolute path.

**Parameters:**
- `file_path`: File path (relative or absolute)
- `base_dir`: Base directory for relative paths

**Returns:** Absolute path to validated file

**Raises:**
- `FileValidationError`: If file doesn't exist

**Example:**
```python
from pathlib import Path
from nakala_client.common.utils import validate_file_exists

# Validate and resolve file path
absolute_path = validate_file_exists(
    Path("../images/photo.jpg"), 
    Path("./datasets")
)
```

### API Client Management

#### `create_api_client(config: NakalaConfig) -> NakalaAPIClient`

Creates configured API client with error handling.

**Parameters:**
- `config`: Nakala configuration object

**Returns:** Configured API client with retry logic

**Example:**
```python
from nakala_client.common.config import NakalaConfig
from nakala_client.common.utils import create_api_client

config = NakalaConfig.from_env()
api_client = create_api_client(config)
```

### Logging Configuration

#### `setup_logging(level: str = 'INFO', log_file: Optional[str] = None) -> logging.Logger`

Configures consistent logging across modules.

**Parameters:**
- `level`: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR')
- `log_file`: Optional log file path

**Returns:** Configured logger instance

**Example:**
```python
from nakala_client.common.utils import setup_logging

# Basic logging to console
logger = setup_logging('INFO')

# Logging to file with debug level
logger = setup_logging('DEBUG', 'nakala_debug.log')

logger.info("Processing started")
logger.debug("Detailed processing information")
```

### Validation Functions

#### `validate_csv_format(csv_path: Path, required_columns: List[str]) -> None`

Validates CSV file format and required columns.

**Parameters:**
- `csv_path`: Path to CSV file
- `required_columns`: List of required column names

**Raises:**
- `FileValidationError`: If CSV is invalid or missing columns

#### `validate_metadata_field(field_name: str, field_value: Any) -> None`

Validates individual metadata field against Nakala requirements.

**Parameters:**
- `field_name`: Metadata field name
- `field_value`: Field value to validate

**Raises:**
- `MetadataValidationError`: If field is invalid

## ⚙️ Configuration Management (`config.py`)

### Base Configuration

#### `class NakalaConfig`

Base configuration class for all Nakala clients.

**Attributes:**
```python
@dataclass
class NakalaConfig:
    api_key: str                              # Required: Nakala API key
    api_url: str = "https://apitest.nakala.fr"  # API endpoint URL
    default_folder_path: str = "./datasets"     # Default data folder
    default_output_path: str = "./output"       # Default output folder
    timeout: int = 300                          # Request timeout (seconds)
    retry_attempts: int = 3                     # Number of retry attempts
    log_level: str = 'INFO'                     # Logging level
    log_file: Optional[str] = None              # Log file path
```

**Methods:**

##### `@classmethod from_env(cls) -> 'NakalaConfig'`

Load configuration from environment variables.

**Environment Variables:**
- `NAKALA_API_KEY`: API key (required)
- `NAKALA_API_URL`: API endpoint URL
- `NAKALA_DEFAULT_FOLDER_PATH`: Default folder path
- `NAKALA_DEFAULT_OUTPUT_PATH`: Default output path
- `NAKALA_TIMEOUT`: Request timeout
- `NAKALA_RETRY_ATTEMPTS`: Retry attempts
- `NAKALA_LOG_LEVEL`: Logging level
- `NAKALA_LOG_FILE`: Log file path

**Example:**
```python
# Load from environment
config = NakalaConfig.from_env()

# Manual configuration
config = NakalaConfig(
    api_key="your-api-key",
    api_url="https://apitest.nakala.fr",
    log_level="DEBUG"
)
```

##### `validate(self) -> None`

Validates configuration parameters.

**Raises:**
- `ConfigurationError`: If configuration is invalid

### Specialized Configurations

#### `class UploadConfig(NakalaConfig)`

Upload-specific configuration extending base configuration.

**Additional Attributes:**
```python
@dataclass
class UploadConfig(NakalaConfig):
    batch_size: int = 50                    # Datasets per batch
    concurrent_uploads: int = 3             # Concurrent file uploads
    skip_existing: bool = True              # Skip existing datasets
    validate_before_upload: bool = True     # Pre-upload validation
    create_missing_folders: bool = True     # Create missing directories
```

#### `class CollectionConfig(NakalaConfig)`

Collection-specific configuration extending base configuration.

**Additional Attributes:**
```python
@dataclass
class CollectionConfig(NakalaConfig):
    create_missing_collections: bool = True    # Auto-create collections
    update_existing: bool = False             # Update existing collections
    inherit_permissions: bool = True          # Inherit parent permissions
    default_collection_status: str = 'private'  # Default visibility
```

## 🚨 Exception Handling (`exceptions.py`)

### Exception Hierarchy

```
NakalaClientError (base)
├── NakalaAPIError (API-related errors)
├── FileValidationError (file-related errors)
├── ConfigurationError (configuration errors)
├── MetadataValidationError (metadata errors)
└── SecurityError (security-related errors)
```

### Base Exception

#### `class NakalaClientError(Exception)`

Base exception for all Nakala client errors.

**Attributes:**
- `message`: Error message
- `context`: Optional context dictionary

### API Exceptions

#### `class NakalaAPIError(NakalaClientError)`

API-related errors with HTTP status codes.

**Constructor:**
```python
def __init__(self, message: str, status_code: int = None, response_data: dict = None)
```

**Attributes:**
- `status_code`: HTTP status code
- `response_data`: API response data

**Example:**
```python
try:
    response = api_client.post('/datas', data=payload)
except NakalaAPIError as e:
    if e.status_code == 413:
        print("File too large")
    elif e.status_code == 401:
        print("Authentication failed")
    print(f"API Error: {e.message}")
```

### File Exceptions

#### `class FileValidationError(NakalaClientError)`

File validation and processing errors.

**Constructor:**
```python
def __init__(self, message: str, filename: str = None, line_number: int = None)
```

**Attributes:**
- `filename`: Name of problematic file
- `line_number`: Line number (for CSV errors)

**Example:**
```python
try:
    validate_file_exists(file_path, base_dir)
except FileValidationError as e:
    print(f"File error: {e.message}")
    if e.filename:
        print(f"Problem file: {e.filename}")
```

### Metadata Exceptions

#### `class MetadataValidationError(NakalaClientError)`

Metadata format and content validation errors.

**Constructor:**
```python
def __init__(self, message: str, field_name: str = None, field_value: str = None)
```

**Attributes:**
- `field_name`: Name of problematic field
- `field_value`: Invalid field value

## 🔍 Usage Patterns

### Standard Module Setup

```python
from nakala_client.common.config import UploadConfig
from nakala_client.common.utils import setup_logging, create_api_client
from nakala_client.common.exceptions import NakalaAPIError, FileValidationError

class CustomModule:
    def __init__(self, config: UploadConfig):
        self.config = config
        self.logger = setup_logging(config.log_level, config.log_file)
        self.api_client = create_api_client(config)
    
    def process_data(self, data_path: Path):
        try:
            # Use common utilities
            validated_path = validate_file_exists(data_path, self.config.default_folder_path)
            result = upload_file_to_nakala(self.api_client, validated_path)
            return result
        except FileValidationError as e:
            self.logger.error(f"File validation failed: {e.message}")
            raise
        except NakalaAPIError as e:
            self.logger.error(f"API operation failed: {e.message}")
            raise
```

### Error Handling Pattern

```python
def robust_operation():
    try:
        # Operation that might fail
        result = risky_operation()
        return result
    except NakalaAPIError as e:
        logger.error(f"API Error: {e.message} (Status: {e.status_code})")
        if e.status_code == 413:
            logger.info("Consider splitting large files")
        elif e.status_code == 429:
            logger.info("Rate limited - waiting before retry")
        raise
    except FileValidationError as e:
        logger.error(f"File Error: {e.message}")
        if e.filename:
            logger.error(f"Problem file: {e.filename}")
        raise
    except Exception as e:
        logger.exception("Unexpected error occurred")
        raise NakalaClientError(f"Operation failed: {str(e)}") from e
```

### Configuration Loading

```python
# Priority order: environment variables, config file, defaults
try:
    # Try environment first
    config = UploadConfig.from_env()
except ConfigurationError:
    # Fall back to manual configuration
    config = UploadConfig(
        api_key=input("Enter API key: "),
        api_url="https://apitest.nakala.fr"
    )

# Always validate configuration
config.validate()
```

## 🧪 Testing Utilities

### Test Configuration

```python
# Test configuration for unit tests
@pytest.fixture
def test_config():
    return NakalaConfig(
        api_key="test-key",
        api_url="https://apitest.nakala.fr",
        timeout=30,
        log_level="DEBUG"
    )
```

### Mock API Client

```python
# Mock API client for testing
@pytest.fixture
def mock_api_client():
    client = Mock()
    client.post.return_value.json.return_value = {"status": "success"}
    return client
```

This common utilities package provides a solid foundation for building consistent, reliable Nakala client modules with proper error handling, configuration management, and logging.