# Nakala Python Connector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/nakala-connector.svg)](https://pypi.org/project/nakala-connector/)
[![PyPI Version](https://img.shields.io/pypi/v/nakala-connector.svg)](https://pypi.org/project/nakala-connector/)

A Python client for interacting with the Nakala API, providing a high-level interface for managing data objects, files, collections, and search functionality.

## Features

- **Data Management**: Create, read, update, and delete data objects
- **File Handling**: Upload, download, and manage files
- **Collections**: Organize data objects into collections
- **Search**: Powerful search capabilities with filtering and faceting
- **Metadata**: Comprehensive support for Nakala metadata standards
- **Validation**: Built-in validation for metadata and API requests
- **Type Annotations**: Full type hints for better IDE support and code quality

## Installation

```bash
pip install nakala-connector
```

## Quick Start

```python
from nakala_connector import NakalaAPI, MetadataBuilder

# Initialize the client with your API key
nakala = NakalaAPI(api_key="your-api-key-here")

try:
    # Create a metadata builder
    builder = nakala.metadata_builder()
    
    # Add metadata
    builder.add_title("My Research Data")
    builder.add_description("This is a sample dataset for demonstration purposes.")
    builder.add_creator({"name": "John Doe", "affiliation": "EFEO"})
    
    # Build the metadata
    metadata = builder.build()
    
    # Upload a file and create a data object
    file_path = "path/to/your/file.pdf"
    result = nakala.upload_data(
        metadata=metadata,
        file_paths=[file_path]
    )
    
    print(f"Created data object with ID: {result['id']}")
    
    # Search for data objects
    search_results = nakala.search_data(
        query="research data",
        filters={"type": "Dataset"},
        limit=10
    )
    
    print(f"Found {search_results['numFound']} matching data objects")
    
finally:
    # Clean up
    nakala.close()
```

## Documentation

For detailed documentation, including API reference and usage examples, please visit the [official documentation](https://nakala-connector.readthedocs.io/).

## Development

### Setting Up for Development

1. Clone the repository:
   ```bash
   git clone https://github.com/EFEO/nakala-connector.git
   cd nakala-connector
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode with all dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

```bash
pytest
```

### Code Style

This project uses `black` for code formatting and `isort` for import sorting. To ensure your code adheres to the project's style guidelines, run:

```bash
black .
isort .
```

### Building Documentation

To build the documentation locally:

```bash
cd docs
make html
```

The documentation will be available in `docs/_build/html/`.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, or suggest improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [École française d'Extrême-Orient (EFEO)](https://www.efeo.fr/)
- [Nakala](https://www.nakala.fr/) - The digital repository for research data

## Contact

For questions or support, please contact [EFEO](mailto:contact@efeo.fr).
