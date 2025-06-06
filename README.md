# NAKALA Client - Python Library for Research Data Management

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/badge/PyPI-Coming%20Soon-orange)](https://pypi.org)

**A comprehensive Python client for the NAKALA research data repository API, developed by École française d'Extrême-Orient (EFEO).**

## 🎯 Overview

NAKALA Client provides professional-grade tools for managing research data in the NAKALA repository. It supports the complete research data lifecycle: upload, organization into collections, quality curation, and automated workflows.

### Key Features

- **📤 Data Upload**: Bulk upload with automatic metadata extraction
- **📚 Collection Management**: Organize datasets into thematic collections  
- **🔍 Data Curation**: Quality assessment and batch metadata modifications
- **⚙️ Workflow Automation**: Scriptable operations for research pipelines
- **🌐 Multi-environment**: Test and production API support
- **🔧 CLI Tools**: Command-line interface for all operations

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (when published)
pip install nakala-client

# Or install from source
git clone https://github.com/efeo/o-nakala-core.git
cd o-nakala-core
pip install -e .
```

### Verify Installation

```bash
# Quick verification
python test_installation.py

# Test CLI commands
nakala-upload --help
nakala-collection --help
nakala-curator --help
nakala-user-info --help
```

### CLI Usage (Recommended)

```bash
# Upload research data
nakala-upload \
  --api-url "https://apitest.nakala.fr" \
  --api-key "YOUR_KEY" \
  --mode folder \
  --dataset "folder_data_items.csv" \
  --base-path "your_data/"

# Create collections  
nakala-collection \
  --api-url "https://apitest.nakala.fr" \
  --api-key "YOUR_KEY" \
  --from-upload-output "upload_results.csv"

# Analyze data quality
nakala-curator \
  --api-url "https://apitest.nakala.fr" \
  --api-key "YOUR_KEY" \
  --quality-report \
  --output "quality_report.json"
```

### Python API Usage

```python
from nakala_client.upload import main as upload_main
from nakala_client.collection import main as collection_main
from nakala_client.common import NakalaConfig

# Set up configuration
import os
os.environ['NAKALA_API_KEY'] = 'your-api-key'
os.environ['NAKALA_BASE_URL'] = 'https://apitest.nakala.fr'

# Use through CLI interface or direct module imports
# (See developer documentation for advanced Python API usage)
```

## 📚 Learning Resources

### 🎓 Interactive Workshop
Complete the hands-on workshop to learn all features:

```bash
cd o-nakala-workshop
pip install -r requirements.txt
jupyter lab NAKALA_Complete_Workflow.ipynb
```

**Workshop Contents:**
- 📤 Data upload (5 datasets, 14 files)
- 📚 Collection creation (3 thematic collections)  
- 🔍 Quality curation and analysis
- 📋 Comprehensive reporting

### 📖 Documentation
- **[User Guides](docs/user-guides/)** - Step-by-step tutorials
- **[Examples](examples/)** - Sample datasets and configurations
- **[API Reference](https://api.nakala.fr/swagger-ui/)** - Complete API documentation

## 🏗️ Architecture

### V2.0 Modern Design
```
src/nakala_client/
├── upload.py              # Data upload functionality
├── collection.py          # Collection management  
├── curator.py             # Quality curation tools
├── user_info.py          # Account information
├── cli/                   # Command-line interfaces
│   ├── upload.py         # nakala-upload
│   ├── collection.py     # nakala-collection
│   └── curator.py        # nakala-curator
└── common/                # Shared utilities
    ├── config.py         # Configuration management
    ├── utils.py          # HTTP utilities
    └── exceptions.py     # Error handling
```

### Key Components

**📤 Upload Engine**
- Folder-based organization
- Automatic MIME type detection  
- Resumable uploads
- Metadata validation

**📚 Collection Manager**
- Thematic grouping
- Hierarchical organization
- Bulk operations
- Status management

**🔍 Curation Suite**
- Quality scoring
- Duplicate detection
- Metadata enhancement
- Automated recommendations

## 🌟 Supported Use Cases

### Digital Humanities Research
- **Manuscript Digitization**: Images, transcriptions, metadata
- **Text Corpora**: Classical texts with linguistic annotations
- **Archaeological Data**: Site records, artifact catalogs, analyses

### Academic Workflows
- **Research Data Management**: Structured dataset organization
- **Collaborative Projects**: Shared collections and permissions
- **Publication Preparation**: Data packaging for article supplements

### Institutional Repositories
- **Bulk Migration**: Legacy system data transfer
- **Quality Assurance**: Automated metadata validation
- **Collection Development**: Thematic organization strategies

## 📊 Real-World Performance

**Production Metrics** (from EFEO usage):
- ✅ **14 files** uploaded in ~4 seconds
- ✅ **3 collections** created in ~1 second  
- ✅ **5 datasets** with 100% success rate
- ✅ **Multi-language** metadata (French/English)

## 🔧 Configuration

### Environment Setup
```bash
# Required
export NAKALA_API_KEY="your-api-key"

# Optional  
export NAKALA_BASE_URL="https://apitest.nakala.fr"  # Test environment
export NAKALA_DEFAULT_LICENSE="CC-BY-4.0"
export NAKALA_DEFAULT_LANGUAGE="fr"
```

### File Configuration
```python
# config.py
from nakala_client.common import NakalaConfig

config = NakalaConfig(
    api_key="your-key",
    api_url="https://apitest.nakala.fr",
    default_license="CC-BY-4.0",
    timeout=30
)
```

## 🧪 Testing

```bash
# Run test suite
pytest

# Test with coverage
pytest --cov=nakala_client

# Integration tests
python test_v2_implementation.py
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### Development Setup
```bash
git clone https://github.com/efeo/o-nakala-core.git
cd o-nakala-core
pip install -e .
pip install -r requirements.txt
```

### Code Style
- **Black** for formatting
- **Flake8** for linting  
- **MyPy** for type checking
- **Pytest** for testing

## 📈 Roadmap

### Current (v2.0)
- ✅ Complete API coverage
- ✅ CLI tools
- ✅ Workshop materials
- ✅ Production validation

### Future (v2.1+)
- 🔄 Advanced duplicate detection
- 📊 Enhanced analytics
- 🌐 Web interface integration
- 🔗 External system connectors

## 🏛️ About EFEO

**École française d'Extrême-Orient** is a French research institution dedicated to the study of Asian civilizations. This tool supports EFEO's mission of advancing digital humanities research and cultural heritage preservation.

**Related Projects:**
- Digital manuscript collections
- Classical Chinese text analysis
- Archaeological site documentation
- Cultural heritage digitization

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙋 Support

### Getting Help
- **Documentation**: [docs/](docs/)
- **Workshop**: Interactive learning materials in `o-nakala-workshop/`
- **Issues**: GitHub Issues for bug reports
- **API Reference**: https://api.nakala.fr/swagger-ui/

### Contact
- **Institution**: École française d'Extrême-Orient
- **Email**: digital@efeo.fr
- **Website**: https://www.efeo.fr

---

**🎉 Ready to manage research data professionally? Start with the [workshop](o-nakala-workshop/) or explore the [documentation](docs/)!**