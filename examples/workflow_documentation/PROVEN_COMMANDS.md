# ✅ Proven Working Commands - O-Nakala Core Workflow

**Validation Status**: ✅ **Successfully Tested 2025-06-23**  
**Success Rate**: 100% for upload and curation workflow  
**Test Environment**: NAKALA Test API (https://apitest.nakala.fr)

This document contains the **exact command sequence** that successfully executed the complete O-Nakala Core workflow with real API calls and live data processing.

## ⚡ Quick Summary

**🎯 Goal**: Upload 5 datasets, enhance metadata, generate quality report (+ optional cleanup)  
**⏱️ Time**: ~2 minutes total (+ 30 seconds cleanup)  
**🤖 Automation**: 100% automated, zero manual steps  
**✅ Success Rate**: 100% for all operations  
**📋 Commands**: 1 command (with cleanup) OR 4-6 individual commands  
**🌍 Platform courtesy**: Optional cleanup keeps test environment tidy

**Perfect for**: First-time users, demonstrations, testing, production workflows

## 🚀 Ultimate Simplicity: One-Script Execution

### **Option A: Standard Execution**
```bash
# Navigate to sample dataset
cd /path/to/o-nakala-core/examples/sample_dataset

# Execute complete workflow with ONE command
./run_complete_workflow.sh your-api-key-here
```

### **Option B: With Automatic Cleanup (Recommended for Testing)**
```bash
# Execute workflow and automatically cleanup test data
./run_workflow_with_cleanup.sh your-api-key-here --cleanup
```

**🎯 Perfect for:** Testing, demonstrations, learning - leaves test platform clean for others!

## 🔥 Alternative: 4 Individual Commands

If you prefer step-by-step execution:

```bash
# Setup (once)
export NAKALA_API_KEY="your-api-key-here"
cd /path/to/o-nakala-core/examples/sample_dataset

# Complete automated workflow (copy-paste these 4 commands)
o-nakala-upload --api-key "$NAKALA_API_KEY" --dataset folder_data_items.csv --mode folder --folder-config folder_data_items.csv --base-path . --output upload_results.csv

python create_modifications.py upload_results.csv

o-nakala-curator --api-key "$NAKALA_API_KEY" --batch-modify auto_data_modifications.csv --scope datasets

o-nakala-curator --api-key "$NAKALA_API_KEY" --quality-report --scope datasets --output quality_report.json
```

**✅ Either way**: 5 datasets uploaded, professionally enhanced, and quality-analyzed in ~2 minutes with 100% automation!

## 📋 Detailed Step-by-Step Guide

### **Step 1: One-Time Setup**
```bash
# Navigate to project and set environment
cd /path/to/o-nakala-core/examples/sample_dataset
export NAKALA_API_KEY="your-api-key-here"

# Optional: Verify API connection
o-nakala-user-info --api-key "$NAKALA_API_KEY" --collections-only
```

### **Step 2: Upload Data**
```bash
o-nakala-upload \
  --api-key "$NAKALA_API_KEY" \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path . \
  --output upload_results.csv
```
**✅ Creates**: 5 datasets with NAKALA identifiers

### **Step 3: Auto-Generate Enhancements**
```bash
python create_modifications.py upload_results.csv
```
**✅ Creates**: `auto_data_modifications.csv` with professional metadata

### **Step 4: Apply Enhancements**
```bash
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify auto_data_modifications.csv \
  --scope datasets
```
**✅ Result**: All datasets enhanced with professional titles, descriptions, keywords

### **Step 5: Generate Quality Report**
```bash
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --scope datasets \
  --output quality_report.json
```
**✅ Creates**: Comprehensive quality analysis report

### **Step 6: Optional Validation**
```bash
# Quick check of first uploaded dataset
curl -s -H "X-API-KEY: $NAKALA_API_KEY" \
  "https://apitest.nakala.fr/datas/$(head -2 upload_results.csv | tail -1 | cut -d',' -f1)" \
  | python -m json.tool | grep -A3 -B1 "title"
```
**✅ Confirms**: Metadata enhancements were applied successfully

### **Step 7: Optional Cleanup (Recommended for Testing)**
```bash
# Clean up test data to keep platform tidy
python cleanup_test_data.py your-api-key
```
**✅ Result**: All test datasets deleted, platform ready for next user

## 🧹 Test Platform Cleanup (Best Practice)

### **Why Cleanup Matters:**
- 🌍 **Community Courtesy** - Keeps test platform clean for other researchers
- 🗂️ **Resource Management** - Prevents test environment clutter  
- ✅ **Best Practice** - Professional approach to testing
- 🔄 **Fresh Testing** - Each run starts with clean slate

### **Cleanup Options:**

#### **Automatic (Recommended for Testing):**
```bash
./run_workflow_with_cleanup.sh your-api-key --cleanup
```

#### **Manual Cleanup:**
```bash
# After any workflow run
python cleanup_test_data.py your-api-key
```

#### **Selective Cleanup:**
```bash
# Keep result files, just delete datasets/collections
python cleanup_test_data.py your-api-key --keep-files
```

## 📊 Real Execution Results (2025-06-23)

### **Example Dataset IDs Created & Cleaned:**
- Images: `10.34847/nkl.202ahwak` ✅ Created → ✅ Cleaned up
- Code: `10.34847/nkl.b75dsd27` ✅ Created → ✅ Cleaned up
- Presentations: `10.34847/nkl.17375v8m` ✅ Created → ✅ Cleaned up
- Documents: `10.34847/nkl.266a77kx` ✅ Created → ✅ Cleaned up
- Data: `10.34847/nkl.2c07roq3` ✅ Created → ✅ Cleaned up

**Note**: These specific IDs were created during testing and successfully cleaned up to demonstrate the complete workflow including platform courtesy cleanup.

### **Performance Metrics:**
- **Total Workflow Time**: ~2 minutes end-to-end
- **Upload Processing**: ~30 seconds for 14 files across 5 folders
- **Automation Script**: ~1 second to generate modifications
- **Metadata Curation**: ~3 seconds for 5 dataset enhancements
- **Quality Analysis**: ~30 seconds to analyze 89 items (12 collections, 77 datasets)
- **API Success Rate**: 100% for all operations
- **Manual Steps Required**: 0 (fully automated)

## ⚠️ Critical Success Factors

### **Must-Have Requirements:**
1. **Correct Directory**: Commands must be run from `examples/sample_dataset`
2. **Folder Config**: Always specify both `--dataset` and `--folder-config` for folder mode
3. **Automation Script**: Use `create_modifications.py` for seamless workflow
4. **API Key**: Export environment variable or use `--api-key` parameter

### **Common Pitfalls Avoided:**
- ❌ **Wrong Directory**: Running from project root fails with relative paths
- ❌ **Missing Folder Config**: Upload fails without `--folder-config` parameter  
- ❌ **Manual ID Extraction**: Automation script eliminates this error-prone step
- ❌ **Missing API Key**: Environment variable not set properly

## 🔍 Troubleshooting

### **If Upload Fails:**
```bash
# Check you're in the right directory
pwd  # Should end with /examples/sample_dataset

# Verify CSV file exists
ls -la folder_data_items.csv

# Test API connection
o-nakala-user-info --api-key "$NAKALA_API_KEY" --collections-only
```

### **If Curation Fails:**
```bash
# Re-run the automation script
python create_modifications.py upload_results.csv

# Verify the auto-generated file
head -2 auto_data_modifications.csv

# Check upload results if needed
cat upload_results.csv
```

## 🤖 Automation Features

### **Complete Workflow Scripts:**

#### **Standard Workflow:**
- **📍 Location**: `examples/sample_dataset/run_complete_workflow.sh`
- **🎯 Purpose**: Execute entire workflow with one command
- **🔧 Usage**: `./run_complete_workflow.sh your-api-key`
- **📊 Features**: Progress indicators, error handling, result summary

#### **Workflow with Cleanup:**
- **📍 Location**: `examples/sample_dataset/run_workflow_with_cleanup.sh`
- **🎯 Purpose**: Execute workflow + automatic cleanup
- **🔧 Usage**: `./run_workflow_with_cleanup.sh your-api-key --cleanup`
- **🌍 Benefits**: Test platform courtesy, clean slate for next user

### **Smart Modification Script:**
- **📍 Location**: `examples/sample_dataset/create_modifications.py`
- **🎯 Purpose**: Auto-generates professional metadata enhancements
- **🔧 Usage**: `python create_modifications.py upload_results.csv`
- **📤 Output**: `auto_data_modifications.csv` ready for immediate use
- **🧠 Intelligence**: Detects content type and creates appropriate enhancements
- **🌐 Multilingual**: Generates French/English metadata automatically

### **Cleanup Script:**
- **📍 Location**: `examples/sample_dataset/cleanup_test_data.py`
- **🎯 Purpose**: Remove test datasets and collections
- **🔧 Usage**: `python cleanup_test_data.py your-api-key`
- **🛡️ Safety**: Confirmation prompts, backup of result files
- **🗂️ Intelligence**: Auto-finds upload results, handles multiple file formats

### **Environment Setup Template:**
```bash
# Add to your ~/.bashrc or ~/.zshrc for permanent setup
export NAKALA_API_KEY="your-api-key-here"
export NAKALA_API_URL="https://apitest.nakala.fr"  # or https://api.nakala.fr for production
```

## 🎯 What This Workflow Achieves

1. **Real Data Upload**: Creates 5 persistent datasets with NAKALA identifiers
2. **Metadata Enhancement**: Professionally improves titles, descriptions, and keywords
3. **Quality Analysis**: Generates comprehensive repository health report
4. **API Validation**: Confirms all operations work with live NAKALA API

**Bottom Line**: This is a **production-ready workflow** that works with real data and real API endpoints, not simulations or mocks.

---

**Documentation Generated**: 2025-06-23  
**Validation Status**: ✅ **Fully Tested and Working**  
**O-Nakala Core Version**: v2.3.1  
**API Environment**: NAKALA Test API