# O-Nakala Core - Interactive Workflow Center

**Complete hub for NAKALA data management workflows with interactive demonstrations and automation tools.**

## 📋 Overview

This directory serves as the **complete operations center** for O-Nakala Core workflows, containing all scripts, modules, and automation tools needed for NAKALA data management. All operational components have been centralized here while data remains in `../sample_dataset/`.

## 🏗️ Architecture

### **Operations Hub**
```
notebooks/
├── README.md                        # This guide - operations overview
├── workflow_notebook.ipynb          # Interactive workflow demonstration
├── run_workflow.sh                  # Complete automation script
├── v2_5_0_workflow_demo.py          # Enhanced preview demonstration
├── cleanup_test_data.py             # Test data cleanup utility
├── verify_cleanup.py                # Cleanup verification
├── workflow_modules/                # Core workflow components
└── [Generated outputs]              # Clean results from workflow executions
```

### **Integrated Features:**
- Metadata enhancement integrated into preview tool (`o-nakala-preview --enhance`)
- Collection modification support built-in
- Automatic CSV generation for workflow outputs

### **Data Repository**
```
../sample_dataset/                      # Research data and configurations only
├── folder_collections.csv             # Collection configuration
├── folder_data_items.csv              # Dataset upload configuration
└── files/                             # Sample research files
```

## 🔍 Smart Preview Tool

### **Intelligent Metadata Enhancement**
**Key Feature**: Metadata enhancement integrated directly into the preview tool.

**Usage**:
```bash
# Smart preview with enhancement suggestions
o-nakala-preview --csv your_data.csv --enhance --interactive

# Auto-apply high-confidence improvements  
o-nakala-preview --csv your_data.csv --enhance
```

**Enhanced Features**:
- ✅ **Content-aware detection** (code, images, documents, data, presentations)
- ✅ **Professional multilingual metadata** (French/English) 
- ✅ **Confidence scoring** for each suggestion
- ✅ **Interactive control** - accept/reject individual enhancements
- ✅ **Automatic application** of high-confidence improvements
- ✅ **File preservation** - original CSV kept, enhanced version created
- ✅ **Real-time preview** - see exactly what will be enhanced

### **v2_5_0_workflow_demo.py** (Demo Script)
**Purpose**: Demonstrate the complete workflow capabilities
**Usage**: `python v2_5_0_workflow_demo.py`  
**Shows**: Enhanced preview capabilities and workflow automation

## 🚀 Complete Workflows

### **1. ✨ Enhanced Workflow** (Recommended)
```bash
# Step 1: Preview with intelligent enhancements
o-nakala-preview --csv examples/sample_dataset/folder_data_items.csv --enhance --interactive

# Step 2: Upload with enhanced metadata  
o-nakala-upload --csv examples/sample_dataset/folder_data_items_enhanced.csv --api-key YOUR_KEY
```

**🎯 Streamlined: Just 2 Commands!**

### **2. Complete Automated Workflow** 
```bash
cd examples/notebooks  # IMPORTANT: Must run from operations center
./run_workflow.sh your-api-key --cleanup
```

**8-Step Automated Process** (still works, but scattered scripts removed):
1. **Data Upload** - Creates datasets from sample files
2. **Collection Creation** - Organizes datasets into thematic collections
3. **Metadata Enhancement** - Integrated into preview tool
4. **Quality Analysis** - Comprehensive validation report
5. **Validation Fixes** - Automatically fixes common validation errors
6. **Dataset Curation** - Applies enhanced metadata to datasets
7. **Collection Curation** - Applies enhanced metadata to collections  
8. **Data Management** - Publication status, rights, and analytics

### **2. Interactive Notebook Workflow**
```bash
cd examples/notebooks
jupyter lab workflow_notebook.ipynb
```

**Real API Demonstrations**:
- Live authentication and user analytics
- Actual dataset upload operations
- Real collection creation and management
- Professional metadata curation
- Error handling and network resilience

### **3. Demo & Learning**
```bash
cd examples/notebooks

# See the workflow demonstration
python v2_5_0_workflow_demo.py

# Try the preview tool
o-nakala-preview --csv ../sample_dataset/folder_data_items.csv --enhance --interactive
```

## 🔧 Workflow Modules

### **Core Components** (`workflow_modules/`)
- **workflow_config.py** - Configuration management and validation
- **data_uploader.py** - Dataset upload operations using o-nakala-core
- **collection_manager.py** - Collection creation and organization  
- **metadata_enhancer.py** - Updated to use scripts in notebooks directory
- **curator_operations.py** - Batch metadata curation
- **quality_analyzer.py** - Quality analysis and reporting
- **workflow_summary.py** - Comprehensive result summaries
- **advanced_data_manager.py** - Publication and rights management

### **Module Integration**
- **Notebooks import workflow modules** (not o-nakala-core directly)
- **Workflow modules import o-nakala-core** (from PyPI package)
- **Scripts use direct CLI commands** for maximum compatibility
- **Paths configured** for centralized operations structure

## 📊 Generated Outputs

### **Results Files** (Created during workflow execution)
- `upload_results.csv` - Dataset upload results with identifiers
- `collections_output.csv` - Collection creation results  
- `auto_data_modifications.csv` - Generated dataset metadata enhancements
- `auto_collection_modifications.csv` - Generated collection metadata enhancements
- `quality_report.json` - Comprehensive quality analysis
- `creator_fixes_*.csv` - Validation error corrections

### **Log Files**
- `o_nakala_core.log` - Main application logs
- `nakala_upload.log` - Upload operation logs
- `nakala_collection.log` - Collection operation logs

## 🔑 Configuration

### **API Setup**
```bash
# Test environment (safe for workshops)
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_API_URL="https://apitest.nakala.fr"
```

### **Prerequisites**
```bash
pip install o-nakala-core[cli,dev,ml] jupyter pandas pathlib
```

## 🎯 Key Benefits

### **Organized Structure**
- ✅ **Centralized operations** in notebooks directory
- ✅ **Clear separation** between operations and data
- ✅ **Efficient workflow** with co-located scripts
- ✅ **Complete automation** with interactive demonstrations

### **User-Friendly Experience** 
- ✅ **Single location** for all workflow operations
- ✅ **Interactive learning** with Jupyter notebooks
- ✅ **Simple maintenance** and updates
- ✅ **Portable operations** hub

### **Production Quality**
- ✅ **Robust error handling** throughout workflows
- ✅ **Comprehensive automation** with quality checks
- ✅ **Complete documentation** aligned with implementation
- ✅ **Educational materials** for training and onboarding

## 🔗 Related Resources

- **Data Repository**: `../sample_dataset/` - Sample research files and configurations
- **Documentation**: `../workflow_documentation/` - Detailed process guides and troubleshooting
- **API Reference**: `../../api/` - NAKALA API specifications and test keys
- **User Guides**: `../../docs/user-guides/` - Complete documentation

## 🎓 Educational Value

**Perfect for**:
- Digital humanities workshops
- Research data management training  
- Institutional NAKALA onboarding
- Development and testing workflows
- Understanding production-ready automation

**Learning Outcomes**:
- Complete NAKALA workflow mastery
- Professional metadata curation techniques
- Automation and scripting best practices
- Error handling and quality assurance
- Production deployment strategies

---

**Role**: Complete operations center for O-Nakala Core workflows  
**Architecture**: Centralized operations hub with streamlined data repository  
**Status**: Production-ready with comprehensive automation and interactive demonstrations