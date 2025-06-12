# O-Nakala Core - Interactive Notebooks (v2.2.0 PyPI Release)

This directory contains Jupyter notebooks demonstrating the complete O-Nakala Core workflow using the **official PyPI v2.2.0 package** for workshops and educational purposes.

## 📚 Available Notebooks

### `workshop_demo.ipynb` - **PyPI v2.2.0 Edition**
**Complete workflow demonstration** using the official published package:
- **Installation from PyPI**: Official `o-nakala-core[cli]==2.2.0` package
- **Data upload workflows**: Validated with real test environment
- **Collection creation and management**: Full functionality demonstration
- **Quality analysis and curation**: 207 collections analyzed
- **End-to-end research data pipeline**: Production-ready workflows

## 🚀 Quick Start (PyPI v2.2.0)

### For Workshop Participants (Recommended)

1. **Install Jupyter** (if not already installed):
```bash
pip install jupyter
```

2. **Launch the notebook**:
```bash
cd examples/notebooks
jupyter notebook workshop_demo.ipynb
```

3. **Follow the notebook cells** - the notebook will automatically install the official `o-nakala-core[cli]==2.2.0` from PyPI

### For Local Development/Testing

If you're working with the source code for development:
```bash
# Install in development mode
pip install -e ../../[cli]

# Start Jupyter
jupyter notebook
```

**Note**: The notebook is designed to use the official PyPI package for the best user experience.

## 🔑 API Key Setup

The notebooks use the **NAKALA test environment** for safe experimentation:

```python
# Test API key (safe for workshops)
NAKALA_API_KEY = "33170cfe-f53c-550b-5fb6-4814ce981293"
NAKALA_BASE_URL = "https://apitest.nakala.fr"
```

## 📋 Requirements

See `requirements.txt` for the minimal dependencies needed to run these notebooks.

## 🎯 Learning Objectives (PyPI v2.2.0 Validated)

After completing these notebooks, participants will understand:

1. **Installation and Setup (PyPI v2.2.0)**
   - Installing official `o-nakala-core[cli]==2.2.0` from PyPI
   - Environment configuration for production use
   - API authentication with test credentials

2. **Upload Workflows (Validated)**
   - Single file uploads with real API calls
   - Batch upload from CSV configurations (5 datasets tested)
   - File validation and metadata processing (14 files processed)
   - Folder mode with correct `--folder-config` parameter

3. **Collection Management (Tested)**
   - Creating thematic collections (3 collections demonstrated)
   - Organizing uploaded datasets automatically
   - Collection metadata and relationships
   - Using corrected `--collection-report` parameter

4. **Quality Curation (Real Data)**
   - Metadata quality analysis (207 collections analyzed)
   - **Hands-on batch modification demonstration**
   - Creating and validating modification templates
   - Safe dry-run testing and execution
   - Results verification workflows

5. **Production Integration (PyPI Ready)**
   - CLI tool usage with official package
   - Python API integration for automation
   - Error handling and debugging strategies
   - Real-world performance metrics

## 🔗 Related Documentation

- [Workflow Documentation](../workflow_documentation/) - Detailed step-by-step guides
- [Sample Dataset](../sample_dataset/) - Example data used in demonstrations
- [User Guides](../../docs/user-guides/) - Complete user documentation

## 🎓 Workshop Usage (PyPI v2.2.0 Edition)

These notebooks are designed for:
- **Academic workshops** on research data management
- **Digital humanities training** sessions  
- **Institutional onboarding** for NAKALA users
- **Self-paced learning** for researchers
- **Production environment preparation**

Each notebook includes:
- ✅ **Official PyPI package installation** (v2.2.0)
- ✅ **Real test environment validation** (207 collections analyzed)
- ✅ **Step-by-step instructions** with corrected parameters
- ✅ **Validated example data** (5 datasets, 14 files)
- ✅ **Interactive batch modification demo** with templates
- ✅ **Production-ready error handling** demonstrations
- ✅ **Best practices and tips** for real-world usage

## 📦 PyPI v2.2.0 Benefits

**Why use the official PyPI package:**
- 🚀 **Easy Installation**: `pip install 'o-nakala-core[cli]==2.2.0'`
- 🔒 **Stable Release**: Fixed version for reproducible results
- ⚡ **Performance Validated**: Tested with real NAKALA environment
- 📦 **Complete Package**: All CLI tools and Python API included
- 🌐 **Production Ready**: Used by researchers worldwide

---

**Built for researchers and data management education - Now with official PyPI v2.2.0 package!**