# O-Nakala Core Automation Scripts

This directory contains automation scripts that make the O-Nakala workflow completely seamless and user-friendly.

## 🚀 Main Workflow Scripts

### **run_complete_workflow.sh**
- **Purpose**: Execute complete workflow in one command
- **Usage**: `./run_complete_workflow.sh your-api-key`
- **Features**: Progress indicators, error handling, result summary

### **run_workflow_with_cleanup.sh** ⭐ **Recommended**
- **Purpose**: Execute workflow + automatic cleanup
- **Usage**: `./run_workflow_with_cleanup.sh your-api-key --cleanup`
- **Benefits**: Platform courtesy, leaves test environment clean

## 🤖 Supporting Scripts

### **create_modifications.py**
- **Purpose**: Auto-generate metadata enhancements from upload results
- **Usage**: `python create_modifications.py upload_results.csv`
- **Intelligence**: Detects content types, creates professional metadata
- **Output**: `auto_data_modifications.csv` ready for curator

### **cleanup_test_data.py**
- **Purpose**: Remove test datasets/collections from NAKALA platform
- **Usage**: `python cleanup_test_data.py your-api-key`
- **Safety**: Confirmation prompts, file backups, error handling

### **verify_cleanup.py**
- **Purpose**: Verify datasets were actually deleted from server
- **Usage**: `python verify_cleanup.py your-api-key`
- **Verification**: Makes real API calls to confirm deletion

## 📋 Configuration Files

### **folder_data_items.csv**
- **Purpose**: Define datasets to be uploaded
- **Format**: Standard O-Nakala upload configuration
- **Content**: 5 sample datasets (images, code, documents, presentations, data)

### **folder_collections.csv**
- **Purpose**: Define collections to be created
- **Format**: Standard O-Nakala collection configuration
- **Content**: 3 thematic collections with multilingual metadata

## 🎯 Quick Start

### **Option 1: One Command (Recommended for Testing)**
```bash
cd examples/sample_dataset
./run_workflow_with_cleanup.sh your-api-key --cleanup
```

### **Option 2: Step by Step**
```bash
cd examples/sample_dataset
./run_complete_workflow.sh your-api-key
# Optionally cleanup later:
python cleanup_test_data.py your-api-key
```

## ✅ Features

- **100% Automation** - Zero manual steps required
- **Platform Courtesy** - Optional cleanup keeps test environment tidy
- **Error Handling** - Robust error detection and reporting
- **Safety First** - Confirmation prompts and file backups
- **Real Validation** - Actual API calls, no mocks or simulations
- **Professional Results** - Production-ready metadata enhancements

## 📊 Expected Results

- **Upload**: 5 datasets created with NAKALA identifiers
- **Enhancement**: Professional metadata applied to all datasets
- **Analysis**: Comprehensive quality report generated
- **Cleanup**: All test data removed (optional)
- **Time**: ~2 minutes total execution

## 🛡️ Safety Guarantees

- Only affects data created by the workflow
- Never touches existing datasets or collections
- Preserves all original source files
- Creates backups before any deletions
- Requires confirmation for destructive operations

---

**Perfect for**: Demonstrations, testing, learning, production workflows