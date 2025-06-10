# O-Nakala Core - Interactive Notebooks

This directory contains Jupyter notebooks demonstrating the complete O-Nakala Core workflow for workshops and educational purposes.

## 📚 Available Notebooks

### `workshop_demo.ipynb`
**Complete workflow demonstration** covering:
- Installation and setup
- Data upload workflows
- Collection creation and management
- Quality analysis and curation
- End-to-end research data pipeline

## 🚀 Quick Start

### For Workshop Participants

1. **Install Jupyter** (if not already installed):
```bash
pip install jupyter
```

2. **Launch the notebook**:
```bash
cd examples/notebooks
jupyter notebook workshop_demo.ipynb
```

3. **Follow the notebook cells** - the notebook will guide you through installing o-nakala-core from PyPI

### For Local Development

If you're working with the source code:
```bash
# Install in development mode
pip install -e ../../[cli]

# Start Jupyter
jupyter notebook
```

## 🔑 API Key Setup

The notebooks use the **NAKALA test environment** for safe experimentation:

```python
# Test API key (safe for workshops)
NAKALA_API_KEY = "33170cfe-f53c-550b-5fb6-4814ce981293"
NAKALA_BASE_URL = "https://apitest.nakala.fr"
```

## 📋 Requirements

See `requirements.txt` for the minimal dependencies needed to run these notebooks.

## 🎯 Learning Objectives

After completing these notebooks, participants will understand:

1. **Installation and Setup**
   - Installing o-nakala-core from PyPI
   - Environment configuration
   - API authentication

2. **Upload Workflows**
   - Single file uploads
   - Batch upload from CSV configurations
   - File validation and metadata processing

3. **Collection Management**
   - Creating thematic collections
   - Organizing uploaded datasets
   - Collection metadata and relationships

4. **Quality Curation**
   - Metadata quality analysis
   - **Hands-on batch modification demonstration**
   - Creating and validating modification templates
   - Safe dry-run testing and execution
   - Results verification workflows

5. **Production Integration**
   - CLI tool usage
   - Python API integration
   - Error handling and debugging

## 🔗 Related Documentation

- [Workflow Documentation](../workflow_documentation/) - Detailed step-by-step guides
- [Sample Dataset](../sample_dataset/) - Example data used in demonstrations
- [User Guides](../../docs/user-guides/) - Complete user documentation

## 🎓 Workshop Usage

These notebooks are designed for:
- **Academic workshops** on research data management
- **Digital humanities training** sessions
- **Institutional onboarding** for NAKALA users
- **Self-paced learning** for researchers

Each notebook includes:
- ✅ Clear learning objectives
- ✅ Step-by-step instructions
- ✅ Real example data
- ✅ **Interactive batch modification demo**
- ✅ Error handling demonstrations
- ✅ Best practices and tips

---

**Built for researchers and data management education.**