# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

O-Nakala-Core is a comprehensive Python client library for the Nakala research data repository API. The project provides tools for uploading datasets, managing collections, and curating research data. It features both legacy v1.0 scripts and a modern v2.0 architecture with unified utilities.

**📚 DOCUMENTATION**: See [`docs_organized/`](docs_organized/) for the complete organized documentation structure.

**🎯 STATUS**: V2.0 complete with real curation successfully applied and validated.

## Development Commands

### Environment Setup
```bash
# Install dependencies for v2.0 (recommended)
pip install -r requirements-new.txt

# Install in development mode
pip install -e .

# Configuration setup
cp config/.env.template .env
# Edit .env with your API credentials
```

### Testing and Validation
```bash
# Run v2.0 implementation tests
python test_v2_implementation.py

# Validate scripts work
python nakala-client-upload-v2.py --help
python nakala-client-collection-v2.py --help
python nakala-curator.py --help

# Test validation mode (no actual uploads)
python nakala-client-upload-v2.py --api-key YOUR_KEY --dataset sample_dataset/folder_data_items.csv --validate-only

# Run complete workflow test (simulated)
python test_complete_workflow.py

# Real workflow execution (requires API key)
python nakala-client-upload-v2.py --api-url https://apitest.nakala.fr --api-key YOUR_KEY \
  --dataset sample_dataset/folder_data_items.csv --folder-config sample_dataset/folder_data_items.csv \
  --mode folder --output upload_results.csv --base-path sample_dataset

python nakala-client-collection-v2.py --api-url https://apitest.nakala.fr --api-key YOUR_KEY \
  --from-folder-collections sample_dataset/folder_collections.csv \
  --from-upload-output upload_results.csv

python nakala-curator.py --api-url https://apitest.nakala.fr --api-key YOUR_KEY \
  --quality-report --output quality_report.json
```

### Development Tools
```bash
# Linting and formatting (from setup.py dev extras)
black src/
flake8 src/
mypy src/

# Run tests
pytest
pytest --cov=nakala_client
```

## Architecture Overview

### V2.0 Modern Architecture (Recommended)
- **Unified Common Package**: `src/nakala_client/common/` contains shared utilities
  - `config.py`: Configuration management with environment variable support
  - `utils.py`: Common HTTP operations, path resolution, logging setup
  - `exceptions.py`: Custom exception hierarchy for better error handling
- **Modular Clients**: Each functionality (upload, collection, curator) is a separate module
- **CLI Scripts**: V2.0 scripts (`*-v2.py`) use the common package internally
- **Backward Compatibility**: V1.0 scripts remain functional during transition

### V1.0 Legacy Architecture (Maintained)
- **Standalone Scripts**: Original `nakala-client-*.py` files are self-contained
- **Direct Implementation**: All functionality embedded in individual script files
- **Zero Dependencies**: Scripts work independently without the common package

### Key Architectural Patterns

#### Configuration Management
The `NakalaConfig` class in `src/nakala_client/common/config.py` handles:
- Environment variable loading (NAKALA_API_KEY, NAKALA_BASE_URL, etc.)
- Default values for metadata (license, language, rights)
- Request timeouts and retry settings
- Path validation and resolution

#### Error Handling
Custom exception hierarchy in `src/nakala_client/common/exceptions.py`:
- `NakalaError`: Base exception class
- `NakalaAPIError`: API-related errors (HTTP status codes)
- `NakalaValidationError`: Data validation failures
- `NakalaFileError`: File operation issues
- `NakalaAuthenticationError`: API key/authentication problems

#### HTTP Operations
Common utilities in `src/nakala_client/common/utils.py` provide:
- Retry logic with exponential backoff using tenacity
- Standard header management (API keys, content types)
- Request/response logging and debugging
- Path resolution and validation

## Common Development Tasks

### Adding New Client Modules
1. Create new module in `src/nakala_client/`
2. Import common utilities: `from .common import NakalaConfig, NakalaCommonUtils, etc.`
3. Follow the pattern established in `upload.py` and `collection.py`
4. Add CLI entry point in `setup.py` console_scripts
5. Create corresponding v2.0 script in root directory

### Working with the API
- **Test Environment**: `https://apitest.nakala.fr` (recommended for development)
- **Production Environment**: `https://api.nakala.fr` (for production use)
- **Authentication**: X-API-KEY header with valid API key
- **Rate Limiting**: Built-in retry logic with exponential backoff
- **Error Handling**: Comprehensive exception hierarchy in `common/exceptions.py`

### Dataset Processing
- **Folder Mode**: Process directory structures with metadata CSV files
- **CSV Mode**: Process individual dataset definitions from CSV
- **File Support**: Images, documents, code, data files with automatic MIME detection
- **Metadata**: Multilingual support (French/English) with controlled vocabularies
- **Validation**: Pre-upload validation with --validate-only flag

### Collection Management
- **Folder-based Collections**: Automatic grouping based on folder structures
- **Manual Collections**: Create collections from specific data IDs
- **Metadata Inheritance**: Collections inherit and extend dataset metadata
- **Status Management**: Private/public collection status control

### Data Curation
- **Quality Assessment**: Automated metadata quality scoring
- **Duplicate Detection**: Content-based similarity analysis
- **Batch Modifications**: CSV-based bulk metadata updates
- **Validation Tools**: Comprehensive metadata validation against NAKALA requirements

## File Structure Understanding

### Package Organization
```
src/nakala_client/           # Main package
├── __init__.py             # Package exports and version
├── upload.py               # Upload module (v2.0)
├── collection.py           # Collection module (v2.0)
├── curator.py              # Curation module (v2.0)
├── user_info.py           # User information module
└── common/                 # Shared utilities
    ├── config.py          # Configuration classes
    ├── utils.py           # HTTP utilities and helpers
    └── exceptions.py      # Custom exceptions
```

### CLI Scripts
- `nakala-client-*-v2.py`: Modern scripts using v2.0 architecture
- `nakala-client-*.py`: Legacy standalone scripts (v1.0)
- Both versions maintain identical CLI interfaces for compatibility

### OpenAPI Client
- `nakala-python-client/`: Auto-generated client from Nakala OpenAPI spec
- Used internally by both v1.0 and v2.0 implementations
- Contains model definitions and API endpoint handlers

## Configuration and Environment

### Environment Variables
Required:
- `NAKALA_API_KEY`: Your Nakala API key

Optional:
- `NAKALA_BASE_URL`: API base URL (defaults to test environment)
- `NAKALA_DEFAULT_LICENSE`: Default license for uploads
- `NAKALA_DEFAULT_LANGUAGE`: Default language code
- `NAKALA_DEFAULT_RIGHTS`: Default rights string

### Configuration Files
- `config/.env.template`: Template for environment variables
- `sample_dataset/`: Example datasets and configuration files
- CSV configuration files define folder mappings and metadata

## Testing Strategy

The project uses `test_v2_implementation.py` for integration testing:
- Validates package structure and imports
- Tests CLI script functionality
- Verifies configuration loading
- Ensures backward compatibility between v1.0 and v2.0

For development, prefer the v2.0 architecture while maintaining v1.0 compatibility.