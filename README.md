# O-Nakala Core

A comprehensive Python library and CLI toolkit for interacting with the NAKALA research data repository, designed specifically for digital humanities workflows.

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (recommended)
pip install o-nakala-core

# With CLI tools
pip install o-nakala-core[cli]

# Install from source
git clone https://github.com/xy-liao/o-nakala-core.git
cd o-nakala-core
pip install -e .[cli]
```

### Basic Usage

```bash
# Set your API key
export NAKALA_API_KEY="your-api-key"

# Upload data (folder mode requires --folder-config)
o-nakala-upload \
  --api-key "$NAKALA_API_KEY" \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path examples/sample_dataset \
  --output upload_results.csv

# Create collections from uploaded data
o-nakala-collection \
  --api-key "$NAKALA_API_KEY" \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv

# Generate quality report
o-nakala-curator --api-key "$NAKALA_API_KEY" --quality-report

# Apply metadata enhancements
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify modifications.csv \
  --scope datasets
```

## 🛠️ Features

### Core Modules
- **📤 Upload**: Batch upload of research datasets with metadata
- **📚 Collection**: Create and manage thematic collections
- **🔧 Curator**: Advanced metadata curation and quality management
- **👤 User Info**: Account management and permissions

### Key Capabilities
- **Foundational metadata management** for core Dublin Core fields
- **Multilingual metadata** support (French, English, Spanish, German)
- **Batch operations** for large-scale data management
- **Quality validation** and enhancement tools
- **CSV-driven workflows** for academic reproducibility
- **Comprehensive logging** and error handling

### 🚧 **Production-Ready Core Features**
Current implementation provides comprehensive functionality for NAKALA data management including:
- **Complete API integration** for uploads, collections, and curation
- **Robust error handling** and validation
- **CSV-driven workflows** for reproducible research
- **Quality analysis** and metadata validation
- **Batch operations** for large-scale data management

## 📖 Documentation

### User Guides
- [📤 Upload Guide](docs/user-guides/01-upload-guide.md) - Complete upload workflows
- [📚 Collection Guide](docs/user-guides/02-collection-guide.md) - Collection management  
- [📋 Workflow Guide](docs/user-guides/03-workflow-guide.md) - End-to-end processes
- [🔧 Curator Field Reference](docs/curator-field-reference.md) - Current field documentation
- [❓ FAQ](docs/user-guides/05-faq.md) - Common questions and solutions

### Technical Reference
- [📋 Field Reference](docs/curator-field-reference.md) - Complete metadata field documentation
- [🔧 API Endpoints](docs/endpoints/) - Detailed endpoint specifications and examples
- [🏛️ Property URI Mapping](docs/property-uri-mapping.md) - NAKALA metadata schema reference

### Quick Reference
```bash
# Show complete field reference
o-nakala-curator --list-fields

# Get help for any command
o-nakala-upload --help
o-nakala-collection --help  
o-nakala-curator --help
o-nakala-user-info --help
```

## 🎓 Getting Started

### Example Workflows
Complete hands-on examples with real datasets:

```bash
cd examples/sample_dataset
# Review the CSV configurations
cat folder_data_items.csv
cat folder_collections.csv

# Run the complete workflow
o-nakala-upload --api-key YOUR_KEY --dataset folder_data_items.csv --mode folder
o-nakala-collection --api-key YOUR_KEY --from-folder-collections folder_collections.csv --from-upload-output output.csv
```

The examples cover:
- Data upload (5 datasets, 14 files)
- Collection creation (3 thematic collections)  
- Quality curation and analysis
- Metadata enhancement

## 📁 Project Structure

```
o-nakala-core/
├── src/o_nakala_core/         # Core library modules
│   ├── cli/                   # Command-line interfaces  
│   ├── common/                # Shared utilities
│   ├── upload.py              # Upload functionality
│   ├── collection.py          # Collection management
│   ├── curator.py             # Metadata curation
│   └── user_info.py           # User management
├── docs/                      # Documentation and guides
├── examples/                  # Sample datasets and workflows
│   ├── sample_dataset/        # Complete workflow example
│   └── simple-dataset/        # Basic usage example
└── api/                       # API reference materials
```

## 🔧 CLI Reference

### Upload Data
```bash
# Upload from CSV configuration
o-nakala-upload \
  --api-key YOUR_KEY \
  --dataset examples/sample_dataset/folder_data_items.csv \
  --mode csv

# Upload from folder mode (requires --folder-config)
o-nakala-upload \
  --api-key YOUR_KEY \
  --dataset examples/sample_dataset/folder_data_items.csv \
  --base-path examples/sample_dataset \
  --mode folder \
  --folder-config examples/sample_dataset/folder_data_items.csv \
  --output upload_results.csv
```

### Manage Collections
```bash
# Create from upload results
o-nakala-collection \
  --api-key YOUR_KEY \
  --title "My Collection" \
  --from-upload-output upload_results.csv

# Create from folder configuration
o-nakala-collection \
  --api-key YOUR_KEY \
  --from-folder-collections examples/sample_dataset/folder_collections.csv \
  --from-upload-output upload_results.csv
```

### Curate Metadata
```bash
# Generate quality report
o-nakala-curator --quality-report --api-key YOUR_KEY

# Batch modify metadata
o-nakala-curator --batch-modify changes.csv --dry-run --api-key YOUR_KEY

# Validate metadata
o-nakala-curator --validate-metadata --scope datasets --api-key YOUR_KEY
```

## 📁 Examples

### 🎓 Interactive Workshop
**Hands-on Jupyter notebook** with complete workflow demonstration:

```bash
cd examples/notebooks
jupyter lab workshop_demo.ipynb
```

The workshop covers:
- ✅ Installation and setup
- 📤 Data upload workflows (CLI + Python API)
- 📚 Collection management
- 🔧 Quality analysis and curation
- 🎯 Best practices and troubleshooting

### Sample Dataset
Complete academic example with:
- Multi-language metadata (French/English)
- 5 data categories (code, data, documents, images, presentations)
- Collection definitions and relationships

```bash
cd examples/sample_dataset
# Review folder_data_items.csv and folder_collections.csv
```

### Simple Dataset  
Minimal example for quick testing:

```bash
cd examples/simple-dataset
# Bird images with basic metadata
```

## 🌐 Environment Setup

```bash
# Required
export NAKALA_API_KEY="your-api-key"

# Optional (defaults to test environment)
export NAKALA_BASE_URL="https://apitest.nakala.fr"  # Test
# export NAKALA_BASE_URL="https://api.nakala.fr"     # Production
```

## 🧹 Maintenance

### Cleanup
Remove development artifacts and reset to clean state:

```bash
# Preview what would be cleaned
python cleanup.py --dry-run

# Clean everything
python cleanup.py

# Keep log files for debugging  
python cleanup.py --keep-logs
```

## 🚨 Common Issues

### "Folder config is required for folder mode"
**Solution**: Add the `--folder-config` parameter:
```bash
o-nakala-upload --api-key YOUR_KEY --dataset file.csv --mode folder --folder-config file.csv --base-path .
```

### "Item [ID] not found in datasets or collections"  
**Solution**: Update collection IDs in modification CSV files using the latest IDs from `collections_output.csv`

### Commands not found (o-nakala-upload, etc.)
**Solution**: Install with CLI support and activate virtual environment:
```bash
pip install -e ".[cli]"
source .venv/bin/activate
```

### File path issues
**Solution**: Ensure you're in the correct directory and verify file paths:
```bash
cd examples/sample_dataset
ls -la *.csv files/
```

For detailed troubleshooting, see: [docs/user-guides/troubleshooting.md](docs/user-guides/troubleshooting.md)

## 🔗 Links

- **[NAKALA Platform](https://nakala.fr)** - Main repository platform
- **[Test Environment](https://test.nakala.fr/)** - Safe testing environment  
- **[API Documentation](https://api.nakala.fr/doc)** - Complete API reference
- **[xy-liao/o-nakala-core](https://github.com/xy-liao/o-nakala-core)** - Project repository

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests on the [GitHub repository](https://github.com/xy-liao/o-nakala-core).

---

**Built for researchers and data management professionals.**
