# 🎉 O-Nakala Core v2.1.4 - First Public Release

**Release Date**: June 10, 2025  
**PyPI Package**: [o-nakala-core](https://pypi.org/project/o-nakala-core/)

---

## 🚀 Welcome to O-Nakala Core!

We're excited to announce the **first public release** of O-Nakala Core, a comprehensive Python library and CLI toolkit designed specifically for digital humanities researchers working with the NAKALA research data repository.

### 🎯 What is O-Nakala Core?

O-Nakala Core bridges the gap between researchers and the NAKALA platform, providing intuitive tools for:
- **Batch data uploads** with rich metadata support
- **Collection management** for thematic organization
- **Quality analysis and curation** of research datasets
- **Automated workflows** for reproducible research data management

Built for researchers in digital humanities, cultural heritage, and academic data management.

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
- `nakala-upload` - Data upload and validation
- `nakala-collection` - Collection creation and management
- `nakala-curator` - Quality analysis and batch modifications
- `nakala-user-info` - Account management and statistics

### 🐍 **Python API**
Complete programmatic access for:
- Research workflow automation
- Custom application integration
- Advanced data processing pipelines
- CI/CD integration

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install o-nakala-core[cli]

# Basic usage
export NAKALA_API_KEY="your-api-key"
nakala-upload --dataset data.csv --mode csv
```

### First Steps

```python
from o_nakala_core.upload import NakalaUploadClient
from o_nakala_core.common.config import NakalaConfig

# Configure client
config = NakalaConfig()
config.api_key = "your-api-key"

# Upload data
client = NakalaUploadClient(config)
result = client.upload_single_dataset({
    "title": "My Research Dataset",
    "type": "http://purl.org/coar/resource_type/c_ddb1",
    "files": ["data.csv", "readme.txt"]
})
```

---

## 📚 Documentation & Examples

### **Complete Workshop Notebook** 🎓
Interactive Jupyter notebook with hands-on demonstrations:
- [Workshop Demo](examples/notebooks/workshop_demo.ipynb)
- Covers complete workflow from installation to advanced curation
- **NEW**: Batch modification demonstration with template creation
- Safe test environment with validated credentials

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

## 🏆 Production Ready

### **Comprehensive Testing**
- **99 tests passing** (0 failures, 2 skipped)
- **18% code coverage** across 6,170+ lines of code
- **Real API integration** tested with NAKALA test environment
- **End-to-end workflow validation**

### **Code Quality**
- **Black formatting** for consistent Python style
- **Type hints** throughout codebase
- **Comprehensive error handling** with custom exception hierarchy
- **Modular architecture** for easy extension

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

### **Supported Environments**
- **Operating Systems**: Windows, macOS, Linux
- **Python Versions**: 3.9, 3.10, 3.11, 3.12
- **NAKALA Environments**: Production and test APIs

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
- **NAKALA Platform** by Huma-Num for API and infrastructure
- **Digital Humanities Community** for requirements and feedback
- **Open Source Contributors** for testing and improvements

### **Development**
Built with ❤️ for the research community by an independent developer.

---

## 🎯 Get Started Today

```bash
# Install and try it now
pip install o-nakala-core[cli]

# Run the interactive workshop
cd examples/notebooks
jupyter notebook workshop_demo.ipynb

# Start managing your research data professionally
nakala-upload --help
```

**Ready to transform your research data management?**

[📥 Install from PyPI](https://pypi.org/project/o-nakala-core/) | [📚 Read the Docs](docs/) | [🎓 Try the Workshop](examples/notebooks/)

---

*O-Nakala Core v2.1.4 - Empowering research through better data management.*