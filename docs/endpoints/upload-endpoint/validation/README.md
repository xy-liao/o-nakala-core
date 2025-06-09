# Upload Endpoint Validation

## 🎯 Overview

This directory contains **validation tools and reports** for Upload endpoint CSV files. All tools are designed to catch issues before actual upload attempts.

## 🛠️ Available Tools

### **1. Upload CSV Validator** (`/tools/upload_validator.py`)
**Purpose**: Comprehensive validation of Upload endpoint CSV files

**Features**:
- ✅ **Structure validation** - Required columns and formats
- ✅ **Content validation** - Field values and constraints  
- ✅ **Transformation testing** - Real metadata generation
- ✅ **Mode detection** - Automatic folder/CSV mode detection
- ✅ **Detailed reporting** - Human-readable validation reports

**Usage**:
```bash
# Basic validation
python tools/upload_validator.py path/to/your.csv

# Specify mode explicitly
python tools/upload_validator.py path/to/your.csv --mode folder

# Generate JSON report
python tools/upload_validator.py path/to/your.csv --json

# Save report to file
python tools/upload_validator.py path/to/your.csv --report validation_report.md
```

## 📊 Validation Results

### **Example Files Validation Status**

| Example File | Status | Mode | Metadata Entries | Issues |
|-------------|--------|------|------------------|--------|
| `basic-folder-upload.csv` | ✅ **VALID** | folder | 8 per row | None |
| `multilingual-folder-upload.csv` | ✅ **VALID** | folder | 13 per row | None |
| `csv-mode-upload.csv` | ✅ **VALID** | csv | 8 per row | None |
| `complete-metadata-upload.csv` | ✅ **VALID** | folder | 18 per row | None |

### **Validation Coverage**

#### **✅ Structure Validation**
- Required column presence (`file`/`files`, `status`, `type`, `title`)
- Valid column names against property URI mapping
- Non-empty DataFrame validation
- Mode-specific structure requirements

#### **✅ Content Validation**  
- Required field completeness
- Status value constraints (`pending`/`published`)
- URI format validation for type fields
- Multilingual format syntax (`lang:text|lang:text`)
- Date format recommendations (ISO 8601)
- Rights format validation (`group_id,ROLE`)

#### **✅ Transformation Testing**
- Real metadata generation using `NakalaCommonUtils.prepare_nakala_metadata()`
- JSON structure validation
- Property URI mapping verification
- Array handling for creators and keywords
- Language code processing

## 🔧 Validation Logic

### **Mode Detection**
```python
def _detect_csv_mode(df):
    if 'file' in df.columns:
        return 'folder'  # Folder-based upload
    elif 'files' in df.columns:
        return 'csv'     # Explicit file lists
    else:
        return 'folder'  # Default fallback
```

### **Required Fields by Mode**
```python
required_columns = {
    'folder': ['file', 'status', 'type', 'title'],
    'csv': ['files', 'status', 'type', 'title']
}
```

### **Validation Levels**
1. **ERRORS** - Must be fixed before upload
   - Missing required columns/fields
   - Invalid status values
   - Transformation failures
   - Malformed metadata structures

2. **WARNINGS** - Should be reviewed
   - Unknown columns (ignored during processing)
   - Suboptimal formats (non-URI types, date formats)
   - Incomplete multilingual syntax

3. **INFO** - Processing details
   - Row and column counts
   - Mode detection results
   - Metadata generation statistics

## 🎓 Using Validation in Workflow

### **1. Pre-Upload Validation**
```bash
# Always validate before uploading
python tools/upload_validator.py my_dataset.csv

# If valid, proceed with upload
python -m src.nakala_client.cli.upload --dataset my_dataset.csv --api-key $API_KEY
```

### **2. Automated Testing**
```bash
# Test all examples automatically
for file in docs/endpoints/upload-endpoint/examples/*.csv; do
    echo "Testing $file..."
    python tools/upload_validator.py "$file"
done
```

### **3. Continuous Integration**
```yaml
# Example CI pipeline step
- name: Validate CSV examples
  run: |
    for csv in docs/endpoints/upload-endpoint/examples/*.csv; do
      python tools/upload_validator.py "$csv" || exit 1
    done
```

## 🐛 Common Issues & Solutions

### **Issue: "Missing required columns"**
**Solution**: Ensure CSV has required columns for your mode
```csv
# Folder mode requires
file,status,type,title

# CSV mode requires  
files,status,type,title
```

### **Issue: "Invalid status"**
**Solution**: Use only valid status values
```csv
status
pending    # ✅ Valid
published  # ✅ Valid
draft      # ❌ Invalid
```

### **Issue: "Transformation failed"**
**Solution**: Check field formats, especially multilingual fields
```csv
# ✅ Correct multilingual format
title
"fr:Titre français|en:English title"

# ❌ Incorrect format
title
"français - english"
```

### **Issue: "Unknown columns will be ignored"**
**Solution**: Use correct column names from specification
```csv
# ✅ Correct
creator,contributor,keywords

# ❌ Will be ignored
author,authors,tags
```

## 📈 Validation Reports

### **Sample Report Structure**
```markdown
# Upload CSV Validation Report

**Status**: ✅ VALID / ❌ INVALID
**Mode**: folder / csv
**Errors**: N
**Warnings**: N

## Information
- ℹ️ Loaded CSV with X rows and Y columns
- ℹ️ Auto-detected mode: folder
- ℹ️ Row N: Generated X metadata entries

## Errors (if any)
- ❌ Row N: Specific error description

## Warnings (if any)  
- ⚠️ Row N: Warning description

## Recommendations
- Specific actionable recommendations
```

## 🔗 Related Documentation

- **[CSV Format Specification](../csv-format-specification.md)** - Complete format rules
- **[Field Transformations](../field-transformations.md)** - Transformation logic
- **[Examples](../examples/)** - Working CSV examples
- **[Troubleshooting](../troubleshooting.md)** - Common issues and solutions

---

**Last updated**: 2025-06-09 ✅  
**Tool version**: v1.0 ✅  
**All examples validated**: ✅