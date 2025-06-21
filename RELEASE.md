# 🎉 O-Nakala Core v2.3.0 - Enhanced Code Quality Release

**Release Date**: June 21, 2025  
**PyPI Package**: [o-nakala-core](https://pypi.org/project/o-nakala-core/) - **v2.3.0 Official**

---

## 🚀 Welcome to O-Nakala Core v2.3.0!

We're excited to announce the **enhanced code quality release** of O-Nakala Core v2.3.0, an **independent** comprehensive Python library and CLI toolkit designed specifically for digital humanities researchers working with the NAKALA research data repository (developed by Huma-Num).

### 🔬 **v2.3.0 Validation Results**
This release has been **extensively tested and validated** with enhanced code quality:
- ✅ **5 datasets uploaded** successfully with 14 files processed
- ✅ **3 collections created** with automatic organization
- ✅ **207 collections analyzed** for quality assessment
- ✅ **631 datasets discovered** in comprehensive testing
- ✅ **Fresh build validation** completed from PyPI package
- ✅ **CLI parameters corrected** and validated
- ✅ **68+ code quality fixes** across 12 files
- ✅ **Zero flake8 violations** - complete style compliance
- ✅ **240 tests passing** with improved maintainability

### 🎯 What is O-Nakala Core?

O-Nakala Core is an **independent, community-driven library** that bridges the gap between researchers and the NAKALA platform (by Huma-Num), providing intuitive tools for:
- **Batch data uploads** with rich metadata support
- **Collection management** for thematic organization
- **Quality analysis and curation** of research datasets
- **Automated workflows** for reproducible research data management

Built **independently** for researchers in digital humanities, cultural heritage, and academic data management.

---

## ✨ Key Features

### 📤 **Upload Management**
- Single file and batch upload capabilities
- CSV-driven workflows for reproducible research
- Comprehensive metadata validation and processing
- File integrity verification with SHA1 hashing
- Retry mechanisms with exponential backoff

### 📚 **Collection Management**
- Create and organize thematic collections
- Batch operations from CSV configurations
- Seamless integration with upload workflows
- Multilingual metadata support (French, English, Spanish, German)

### 🔧 **Advanced Curation Tools**
- **Quality analysis** with detailed metadata completeness reports
- **Batch modification** capabilities for large-scale metadata updates
- **Template-based workflows** for consistent data management
- **Dry-run validation** for safe testing before execution

### 🖥️ **CLI Tools**
Four powerful command-line interfaces:
- `o-nakala-upload` - Data upload and validation
- `o-nakala-collection` - Collection creation and management
- `o-nakala-curator` - Quality analysis and batch modifications
- `o-nakala-user-info` - Account management and statistics

### 🐍 **Python API**
Complete programmatic access for:
- Research workflow automation
- Custom application integration
- Advanced data processing pipelines
- CI/CD integration

---

## 🚀 Quick Start (v2.3.0 Validated)

### Installation

```bash
# Install official v2.3.0 from PyPI
pip install 'o-nakala-core[cli]==2.3.0'

# Basic usage (corrected parameters)
export NAKALA_API_KEY="your-api-key"
o-nakala-upload --dataset data.csv --mode folder --folder-config data.csv --base-path .
```

### First Steps (v2.3.0 Python API)

```python
from o_nakala_core.upload import NakalaUploadClient
from o_nakala_core.common.config import NakalaConfig

# Configure client (v2.3.0 validated with enhanced code quality)
config = NakalaConfig(
    api_key="your-api-key",
    api_url="https://apitest.nakala.fr"  # or https://api.nakala.fr for production
)

# Upload data (tested with real environment)
client = NakalaUploadClient(config)
result = client.upload_single_dataset({
    "title": "My Research Dataset",
    "type": "http://purl.org/coar/resource_type/c_ddb1",
    "files": ["data.csv", "readme.txt"]
})
```

---

## 📚 Documentation & Examples

### **Complete Workshop Notebook** 🎓 **v2.3.0 Enhanced Edition**
Interactive Jupyter notebook using the official PyPI package:
- [Workshop Demo](examples/notebooks/workshop_demo.ipynb) - **Updated for v2.3.0**
- **Official PyPI installation**: `pip install 'o-nakala-core[cli]==2.3.0'`
- **Real test results**: 5 datasets, 207 collections analyzed
- **Corrected CLI parameters**: Validated --folder-config usage
- **Batch modification demonstration** with template creation
- **Production-ready workflows** with validated test environment
- **Enhanced code quality**: Zero flake8 violations and improved maintainability

### **User Guides** 📖
- [Upload Guide](docs/user-guides/01-upload-guide.md) - Complete upload workflows
- [Collection Guide](docs/user-guides/02-collection-guide.md) - Collection management
- [Workflow Guide](docs/user-guides/03-workflow-guide.md) - End-to-end processes
- [FAQ](docs/user-guides/05-faq.md) - Common questions and solutions

### **Sample Datasets** 📊
Real-world examples included:
- Multi-language research project (French/English)
- 5 data categories: code, data, documents, images, presentations
- Complete CSV configurations for reproducible workflows

---

## 🏆 Production Ready (v2.3.0 Enhanced Quality)

### **Comprehensive Testing & Real-World Validation**
- **240 tests passing** (0 failures, 2 skipped)
- **20% code coverage** across 6,170+ lines of code
- **Fresh build validation** completed from PyPI package
- **Real API integration** tested with NAKALA test environment
- **End-to-end workflow validation** with actual data:
  - ✅ 5 datasets uploaded successfully (14 files)
  - ✅ 3 collections created with automatic organization
  - ✅ 207 collections analyzed in quality assessment
  - ✅ CLI parameters corrected and validated
  - ✅ Workshop notebook updated for PyPI v2.3.0
  - ✅ Full cycle batch modification testing completed

### **Enhanced Code Quality (v2.3.0)**
- **Zero flake8 violations** - complete style compliance
- **68+ code quality fixes** across 12 files:
  - Removed unused imports and variables
  - Fixed whitespace and formatting issues
  - Improved exception handling patterns
  - Cleaned up f-string usage
- **Black formatting** for consistent Python style
- **Type hints** throughout codebase
- **Comprehensive error handling** with custom exception hierarchy
- **Modular architecture** for easy extension
- **Improved maintainability** and readability

### **Documentation Excellence**
- **Complete user guides** for all workflows
- **API reference** with detailed examples
- **Best practices** and security guidelines
- **Troubleshooting** guides and support

---

## 🌍 Use Cases

### **Academic Research**
- Digital humanities projects
- Cultural heritage digitization
- Research data management
- Collaborative data sharing

### **Institutional Workflows**
- University library systems
- Research center data management
- Multi-researcher project coordination
- Automated publication pipelines

### **Educational Applications**
- Research data management training
- Digital humanities workshops
- Academic skill development
- Reproducible research practices

---

## 🔧 Technical Specifications

### **Requirements**
- Python 3.9+
- Requests ≥2.32.3
- Tenacity ≥9.1.2
- Optional: Click, Rich, Python-dotenv for CLI features

### **Supported Environments (v2.3.0 Tested)**
- **Operating Systems**: Windows, macOS, Linux
- **Python Versions**: 3.9, 3.10, 3.11, 3.12
- **NAKALA Environments**: Production and test APIs (validated)
- **Installation**: PyPI package with CLI extras
- **Deployment**: Production-ready for institutional use
- **Code Quality**: Fully compliant with modern Python standards

### **Integration Ready**
- CI/CD pipeline support
- Docker container compatible
- Environment variable configuration
- Logging and monitoring integration

---

## 🤝 Community & Support

### **Getting Help**
- **Documentation**: Complete guides and examples included
- **Issues**: Report bugs and feature requests on GitHub
- **NAKALA Platform**: Official support at [nakala.fr](https://nakala.fr)

### **Contributing**
- Open source development welcome
- Issue reports and feature suggestions appreciated
- Pull requests encouraged for improvements

### **Workshop & Training**
- Interactive Jupyter notebook included
- Hands-on batch modification demonstrations
- Best practices and troubleshooting guides
- Safe test environment for learning

---

## 🔮 Roadmap

### **Upcoming Features**
- Enhanced machine learning integration
- Advanced relationship management
- Expanded vocabulary support
- Additional file format support

### **Community Priorities**
- User feedback integration
- Performance optimizations
- Extended documentation
- Additional language support

---

## 📄 License & Credits

### **License**
MIT License - see [LICENSE](LICENSE) file for details.

### **Acknowledgments**
- **NAKALA Platform** by Huma-Num for providing the API and infrastructure
- **Digital Humanities Community** for requirements and feedback
- **Open Source Contributors** for testing and improvements

### **Development**
Built with ❤️ for the research community by an **independent developer**.

**Note**: O-Nakala Core is an independent, community-driven project. While it interfaces with the NAKALA platform (developed by Huma-Num), this library is developed and maintained independently to serve the research community's needs.

---

## 🎯 Get Started Today (v2.3.0 Enhanced Quality Release)

```bash
# Install official v2.3.0 from PyPI
pip install 'o-nakala-core[cli]==2.3.0'

# Run the interactive workshop (PyPI v2.3.0 edition)
cd examples/notebooks
jupyter notebook workshop_demo.ipynb

# Start managing your research data professionally (validated commands)
o-nakala-upload --help
o-nakala-collection --help
o-nakala-curator --help
o-nakala-user-info --help
```

### 🆕 **What's New in v2.3.0**

**Enhanced Code Quality & Maintainability:**
- ✅ **Zero flake8 violations** - Complete style compliance
- ✅ **68+ code quality fixes** - Cleaner, more maintainable code
- ✅ **Improved error handling** - Better exception patterns
- ✅ **Optimized imports** - Removed unused dependencies
- ✅ **Enhanced readability** - Consistent formatting throughout

**All existing functionality preserved with improved reliability and maintainability.**

**Ready to transform your research data management with enhanced v2.3.0?**

[📥 Install from PyPI](https://pypi.org/project/o-nakala-core/) | [📚 Read the Docs](docs/) | [🎓 Try the Workshop](examples/notebooks/)

---

*O-Nakala Core v2.3.0 - Enhanced code quality for professional research data management.*