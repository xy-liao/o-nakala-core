# O-Nakala Core - Interactive Notebooks

This directory contains Jupyter notebooks demonstrating the complete O-Nakala Core workflow for educational and development purposes.

## 📚 Available Notebooks

### `ultimate_workflow_notebook.ipynb`
**Complete end-to-end NAKALA workflow demonstration**:
- Data upload with folder mode configuration
- Collection creation and management
- Metadata enhancement and curation
- Quality analysis and reporting
- Comprehensive workflow summary

### `workshop_demo.ipynb`
**Workshop demonstration materials**:
- Interactive tutorials for learning NAKALA workflows
- Hands-on exercises with real test data
- Step-by-step guidance for common tasks

### `run_ultimate_workflow.sh`
**Complete workflow automation script**:
- End-to-end workflow execution via CLI
- Automated data upload, collection creation, and quality analysis
- Optional cleanup mode to remove test data
- Uses sample_dataset for demonstration

### Cleanup Scripts
**NAKALA test data cleanup utilities**:
- `cleanup_all_unakala1_data.py` - Remove all data from unakala1 user
- `cleanup_test_data.py` - Selective cleanup based on upload results
- `verify_cleanup.py` - Verify cleanup completion

## 🔧 Workflow Modules Architecture

### Critical Dependency Relationship
**⚠️ IMPORTANT**: The notebooks **require** the `workflow_modules/` directory to function:

```
ultimate_workflow_notebook.ipynb
├── sys.path.append('workflow_modules')  # Required path setup
├── from workflow_config import WorkflowConfig
├── from data_uploader import DataUploader
├── from collection_manager import CollectionManager
└── [...other workflow module imports]
```

### Module Functionality
The `workflow_modules/` directory contains Python modules that power the notebooks:

- `workflow_config.py` - Configuration management and validation
- `data_uploader.py` - Dataset upload operations using o-nakala-core
- `collection_manager.py` - Collection creation and organization
- `metadata_enhancer.py` - Automatic metadata improvement
- `curator_operations.py` - Batch metadata curation
- `quality_analyzer.py` - Quality analysis and reporting
- `workflow_summary.py` - Comprehensive result summaries
- `advanced_data_manager.py` - Publication and rights management

### How It Works
1. **Notebooks import workflow modules** (not o-nakala-core directly)
2. **Workflow modules import o-nakala-core** (from PyPI package)
3. **Shell scripts execute notebooks** via nbconvert

### Portability
The entire `notebooks/` directory is **self-contained and portable**:
- Copy the whole `notebooks/` folder anywhere
- Install `pip install o-nakala-core[cli]`
- Everything works independently

## 🚀 Quick Start

### Prerequisites
```bash
pip install jupyter o-nakala-core[cli]
```

### Running the Notebooks
```bash
cd examples/notebooks
# IMPORTANT: Must be in the notebooks directory for workflow_modules to be found
jupyter lab ultimate_workflow_notebook.ipynb
```

### Running the Automated Script
```bash
cd examples/notebooks
./run_ultimate_workflow.sh YOUR_API_KEY

# With cleanup (removes test data afterward)
./run_ultimate_workflow.sh YOUR_API_KEY --cleanup
```

### Manual Cleanup
```bash
cd examples/notebooks
# Remove all test data for unakala1 user
python cleanup_all_unakala1_data.py YOUR_API_KEY

# Selective cleanup based on upload results
python cleanup_test_data.py YOUR_API_KEY
```

## 🔑 API Configuration

The notebooks use the NAKALA test environment for safe experimentation:

```python
# Test API credentials (safe for workshops)
API_KEY = "33170cfe-f53c-550b-5fb6-4814ce981293"
API_URL = "https://apitest.nakala.fr"
```

## 📋 Dependencies & File Structure

### Required Files Structure
```
notebooks/
├── ultimate_workflow_notebook.ipynb    # Main notebook
├── workshop_demo.ipynb                 # Demo notebook
├── run_ultimate_workflow.sh            # Automation script
├── workflow_modules/                   # REQUIRED modules directory
│   ├── __init__.py
│   ├── workflow_config.py
│   ├── data_uploader.py
│   ├── collection_manager.py
│   ├── curator_operations.py
│   ├── metadata_enhancer.py
│   ├── quality_analyzer.py
│   ├── workflow_summary.py
│   └── advanced_data_manager.py
├── requirements.txt                    # Python dependencies
└── [cleanup scripts and logs]
```

### Python Dependencies
See `requirements.txt` for the complete list of dependencies needed to run these notebooks.

**Key Dependencies:**
- `o-nakala-core[cli]` - Core NAKALA functionality
- `jupyter` - For interactive notebooks
- `pandas` - Data processing
- `pathlib` - File handling

## 🎯 Learning Objectives

After completing these notebooks, users will understand:

1. **Complete NAKALA Workflow**
   - Data preparation and upload
   - Collection organization strategies
   - Quality analysis and improvement
   - Metadata curation best practices

2. **Automation with Python**
   - Using workflow modules for batch operations
   - Error handling and validation
   - Results analysis and reporting

3. **Production Best Practices**
   - Configuration management
   - Quality assurance workflows
   - Documentation and reproducibility

## 🔗 Related Resources

- [Sample Dataset](../sample_dataset/) - Example data used in demonstrations
- [Workflow Documentation](../workflow_documentation/) - Detailed process guides
- [User Guides](../../docs/user-guides/) - Complete documentation

## 🎓 Educational Use

These notebooks are designed for:
- Digital humanities workshops
- Research data management training
- Institutional NAKALA onboarding
- Self-paced learning for researchers
- Development and testing workflows

---

**Interactive learning for NAKALA research data management**