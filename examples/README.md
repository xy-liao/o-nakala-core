# O-Nakala Core Examples

This directory contains example datasets, configurations, and workflows for learning and testing the O-Nakala Core system.

## 🧭 Quick Navigation

### **🎯 Choose Your Learning Style**

| Learning Style | Directory | Time | Best For |
|----------------|-----------|------|----------|
| **📊 See It Work** | [sample_dataset/](sample_dataset/) | 15 min | Quick validation |
| **🎓 Learn Step-by-Step** | [notebooks/](notebooks/) | 30 min | Interactive tutorial |
| **📋 Follow Process** | [workflow_documentation/](workflow_documentation/) | 60 min | Understanding methodology |

### **🚀 Quick Start Options**

| I want to... | Go to... | Command |
|--------------|----------|---------|
| **Try basic upload** | [sample_dataset/](sample_dataset/) | `o-nakala-upload --dataset folder_data_items.csv` |
| **Run full workflow** | [notebooks/](notebooks/) | `jupyter lab workflow_notebook.ipynb` |
| **See proven results** | [workflow_documentation/](workflow_documentation/) | Browse documentation |

## 📁 Directory Structure

### `/sample_dataset/` - Complete Example Dataset
- **Purpose**: Comprehensive example with 14 files across 5 categories
- **Use case**: Full workflow testing, workshop training, API validation
- **Contents**:
  - `folder_data_items.csv` - Dataset metadata configuration
  - `folder_collections.csv` - Collection organization configuration
  - `files/` - Sample research files (images, code, documents, data, presentations)
  - Workshop exercise files for batch modifications

### `/notebooks/` - Interactive Jupyter Notebooks
- **Purpose**: Complete workflow demonstrations and tutorials
- **Use case**: Educational materials, step-by-step learning
- **Contents**: 
  - `workflow_notebook.ipynb` - Complete O-Nakala Core workflow
  - `workflow_modules/` - Python modules for workflow operations
  - `workflow_modules/` - Python modules for workflow operations
  - `run_workflow.sh` - Shell script automation for notebook workflows

### `/workflow_documentation/` - Process Documentation
- **Purpose**: Documented workflows and success metrics
- **Use case**: Understanding system capabilities and performance
- **Contents**: Workflow guides, process documentation

## 🚀 Quick Start

### 1. Complete Workflow Test
```bash
cd sample_dataset
# See sample_dataset/README.md for complete workflow instructions
./run_workflow.sh YOUR_API_KEY --cleanup
```

### 2. Interactive Workflow Tutorial
```bash
cd notebooks
jupyter lab workflow_notebook.ipynb
# Follow the step-by-step workflow in the notebook
```

## 📚 File Types Included

### Research Data Examples
- **Code**: R scripts, Python modules
- **Data**: CSV datasets, analysis results
- **Documents**: Markdown papers, protocols, literature reviews
- **Images**: Photographs, charts, visualizations
- **Presentations**: Conference talks, stakeholder updates

### Configuration Examples
- **Upload configurations**: Metadata templates for different file types
- **Collection configurations**: Thematic organization patterns
- **Batch modification templates**: Field update examples

## 🎓 Educational Use

### For Workshops
1. **Interactive**: Use `notebooks/workflow_notebook.ipynb` for step-by-step learning
2. **Complete**: Use `sample_dataset/` for full workflow demonstrations
3. **Level 3**: Use workshop CSV files for advanced metadata management

### For Development
1. **Testing**: Use examples to validate code changes
2. **Debugging**: Sample data for reproducing issues
3. **Documentation**: Examples for user guides and tutorials

## 🔧 Configuration Files

### Essential Files (DO NOT MODIFY)
- `folder_data_items.csv` - Core dataset configuration
- `folder_collections.csv` - Collection organization template
- `files/` directory structure - Sample research data

### Workflow Architecture
- `workflow_modules/` - Python modules for complete workflow automation
- `workflow_notebook.ipynb` - Step-by-step interactive tutorial (depends on workflow_modules)
- `workflow_modules/` - Supporting Python modules for notebook operations
- `run_workflow.sh` - Shell script that executes the notebook programmatically

## ⚠️ Important Notes

### API Keys
- Never commit real API keys to the repository
- Use test API keys for workshop exercises
- Set `NAKALA_API_KEY` environment variable for security

### File Modifications
- Sample files in `files/` are for reference only
- Workshop CSV files can be modified for exercises
- Always use `--dry-run` before applying batch modifications

### Data Persistence
- Uploads to test API are temporary
- Production uploads require institutional credentials
- Workshop data is cleaned up periodically

## 🔄 Workflow Component Relationships

### Architecture Overview
The examples use a **3-layer architecture**:

1. **o-nakala-core PyPI package** - Core functionality (`pip install o-nakala-core`)
2. **workflow_modules/** - Custom wrapper modules for complex workflows
3. **Notebooks & Scripts** - User interfaces (Jupyter notebooks, shell scripts)

### Dependencies
```
workflow_notebook.ipynb
├── workflow_modules/
│   ├── data_uploader.py
│   ├── collection_manager.py
│   ├── curator_operations.py
│   └── [other modules]
│       └── o-nakala-core (PyPI package)
└── run_workflow.sh
    └── executes notebook via nbconvert
```

### Usage Options
- **Interactive**: Run `workflow_notebook.ipynb` in Jupyter
- **Automated**: Run `./run_workflow.sh` for batch processing
- **Programmatic**: Import workflow_modules directly in your Python code

## 📦 Portability & Independence

### Self-Contained Examples
The `/examples` directory is **completely portable** and can be copied anywhere:

```bash
# Copy examples to any location
cp -r /path/to/o-nakala-core/examples /new/location/

# Install only the PyPI package
pip install o-nakala-core[cli]

# Everything works independently!
cd /new/location/examples/notebooks
jupyter lab workflow_notebook.ipynb
```

### What's Included
- ✅ Complete sample datasets
- ✅ All workflow modules
- ✅ Configuration templates
- ✅ Shell scripts for automation
- ✅ Documentation and guides

### External Dependencies
- **Python 3.8+** with standard libraries
- **o-nakala-core PyPI package** (`pip install o-nakala-core`)
- **Jupyter** for interactive notebooks (optional)

## 📖 Related Documentation

- [User Guides](../docs/user-guides/) - Step-by-step instructions
- [API Documentation](../docs/endpoints/) - NAKALA API documentation
- [Troubleshooting](../docs/user-guides/05-troubleshooting.md) - Common issues and solutions

## 🤝 Contributing Examples

To add new examples:
1. Follow the existing directory structure
2. Include README documentation
3. Provide both simple and complex variations
4. Test with real API before submitting
5. Update this README with new examples

---

**Ready for workshops, development, and production workflows.**