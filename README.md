# O-Nakala Core

A comprehensive Python library and CLI toolkit for interacting with the NAKALA research data repository, designed specifically for digital humanities workflows.

## 🎯 User-Friendly Design Philosophy

**O-Nakala Core provides simplified CSV interfaces** while maintaining full compatibility with the official NAKALA API. You work with intuitive formats like `"Dupont,Jean"` for creators and `"fr:Titre|en:Title"` for multilingual fields - the library handles the complex API transformations automatically.

**Key Benefits:**
- ✅ **Simple CSV formats** instead of complex JSON structures
- ✅ **Batch operations** from spreadsheet files  
- ✅ **Full API compliance** - all official NAKALA features supported
- ✅ **No API knowledge required** - focus on your research data

## 📚 Documentation Navigation

### **🎯 Start Here Based on Your Goal**

| I want to... | Go to... | Time |
|--------------|----------|------|
| **Try it quickly** | [Quick Start](#🚀-quick-start) below | 5 min |
| **Upload my first dataset** | [Upload Guide](docs/user-guides/01-upload-guide.md) | 15 min |
| **Complete research workflow** | [Workflow Guide](docs/user-guides/03-workflow-guide.md) | 60 min |
| **Organize data into collections** | [Collection Guide](docs/user-guides/02-collection-guide.md) | 30 min |
| **Improve metadata quality** | [Curation Guide](docs/user-guides/04-curation-guide.md) | 45 min |
| **See working examples** | [Examples Directory](examples/) | 20 min |
| **Learn interactively** | [Jupyter Notebook](examples/notebooks/workflow_notebook.ipynb) | 30 min |
| **Solve problems** | [Troubleshooting](docs/user-guides/05-troubleshooting.md) | As needed |
| **Understand API details** | [Endpoint Documentation](docs/endpoints/) | Reference |

### **📂 Documentation Structure**

```
📖 Documentation Overview
├── 📘 User Guides - How to accomplish tasks
├── 🔧 API Reference - Technical specifications  
├── 💡 Examples - Working code and data
├── 📋 Official Specs - NAKALA API reference
└── 🛠️ Development - Setup and contribution
```

**New to NAKALA?** Start with [User Guides](docs/user-guides/) → Try [Examples](examples/) → Reference [API Docs](docs/endpoints/) as needed.

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (recommended)
pip install o-nakala-core[cli,ml]  # Complete installation

# Alternative options
pip install o-nakala-core          # Core library only
pip install o-nakala-core[cli]     # With CLI tools

# Install from source
git clone https://github.com/xy-liao/o-nakala-core.git
cd o-nakala-core
pip install -e .[cli,ml]
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
- **🔧 Curator**: Metadata curation and quality management
- **👤 User Info**: Account management and permissions

### Key Capabilities
- **Complete API integration** for uploads, collections, and curation
- **Automated metadata curation** with pattern recognition and community insights
- **Metadata pre-population** with contextual suggestions
- **Resource relationship discovery** and mapping
- **Multilingual metadata** support with Dublin Core fields
- **CSV-driven workflows** for reproducible research
- **Quality validation** and enhancement tools
- **Batch operations** for large-scale data management
- **Comprehensive error handling** and logging

### 🔬 **Automated Enhancement Features**
- **Pattern Learning**: Discovers metadata patterns from existing data
- **Content Analysis**: Content similarity and clustering
- **Community Analytics**: Repository-wide metadata recommendations
- **Pre-population Engine**: Context-aware field suggestions
- **Relationship Discovery**: Finds connections between resources
- **Data Analysis**: Data-driven field value predictions

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

> **📝 Note**: The examples below use a public test API key for demonstration purposes. Find the current test key in [api/api_keys.md](api/api_keys.md). For production use, create your own API key at https://nakala.fr.

```bash
cd examples/sample_dataset
# Review the CSV configurations
cat folder_data_items.csv
cat folder_collections.csv

# Set API key (see api/api_keys.md for test key)
export NAKALA_API_KEY="[see-api/api_keys.md]"

# Run the complete workflow (v2.4.3 with automated enhancement)
o-nakala-upload --api-key "$NAKALA_API_KEY" \
  --dataset folder_data_items.csv --mode folder \
  --folder-config folder_data_items.csv --base-path . \
  --output upload_results.csv

o-nakala-collection --api-key "$NAKALA_API_KEY" \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv \
  --collection-report collections_output.csv

# Quality analysis (v2.4.3)
o-nakala-curator --api-key "$NAKALA_API_KEY" \
  --quality-report --scope collections
# Now includes: Pattern analysis, community insights, relationship discovery
```

The examples cover:
- Data upload (5 datasets, 14 files) with smart pre-population
- Collection creation (3 thematic collections) with relationship discovery
- Quality curation and analysis
- Automated metadata enhancement
- Community-driven insights and recommendations

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
│   └── notebooks/             # Interactive workshop notebooks
└── api/                       # API reference materials
```


## 📁 Examples

### 🎓 Interactive Workshop
**Hands-on Jupyter notebook** with complete workflow demonstration:

```bash
cd examples/notebooks
jupyter lab workflow_notebook.ipynb
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
cd examples/sample_dataset
# Complete workflow with professional datasets
```

## 🌐 Environment Setup

```bash
# Required - Get test key from api/api_keys.md
export NAKALA_API_KEY="your-api-key"

# Optional (defaults to test environment)
export NAKALA_BASE_URL="https://apitest.nakala.fr"  # Test
# export NAKALA_BASE_URL="https://api.nakala.fr"     # Production
```

## 🧹 Maintenance

### Project Cleanup
To clean up temporary files and development artifacts:

```bash
# Remove log files and temporary outputs
find . -name "*.log" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
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
