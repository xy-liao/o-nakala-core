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

## 🔧 Workflow Modules

The `workflow_modules/` directory contains Python modules that power the notebooks:

- `workflow_config.py` - Configuration management and validation
- `data_uploader.py` - Dataset upload operations
- `collection_manager.py` - Collection creation and organization
- `metadata_enhancer.py` - Automatic metadata improvement
- `curator_operations.py` - Batch metadata curation
- `quality_analyzer.py` - Quality analysis and reporting
- `workflow_summary.py` - Comprehensive result summaries

## 🚀 Quick Start

### Prerequisites
```bash
pip install jupyter o-nakala-core[cli]
```

### Running the Notebooks
```bash
cd examples/notebooks
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

## 📋 Dependencies

See `requirements.txt` for the complete list of dependencies needed to run these notebooks.

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