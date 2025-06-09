# Collection Endpoint Validation

## 🎯 Overview

This directory contains **validation tools and reports** for Collection endpoint CSV files. The validation system ensures collections can be created successfully with proper metadata structure and folder pattern matching.

## 🛠️ Available Tools

### **1. Collection CSV Validator** (`/tools/collection_validator.py`)
**Purpose**: Comprehensive validation of Collection endpoint CSV files

**Features**:
- ✅ **Structure validation** - Required columns (title, status, data_items)
- ✅ **Content validation** - Field values and Dublin Core constraints  
- ✅ **Transformation testing** - Real metadata generation testing
- ✅ **Pattern validation** - Folder pattern format checking
- ✅ **Multilingual validation** - Language syntax verification
- ✅ **Detailed reporting** - Human-readable validation reports

**Usage**:
```bash
# Basic validation
python tools/collection_validator.py path/to/collections.csv

# Generate JSON report
python tools/collection_validator.py path/to/collections.csv --json

# Save report to file
python tools/collection_validator.py path/to/collections.csv --report validation_report.md
```

## 📊 Validation Results

### **Example Files Validation Status**

| Example File | Status | Metadata Entries | Issues | Collections |
|-------------|--------|------------------|--------|-------------|
| `basic-collection.csv` | ✅ **VALID** | 6 per row | None | 2 collections |
| `multilingual-collection.csv` | ✅ **VALID** | 12 per row | None | 2 collections |
| `complete-collection.csv` | ✅ **VALID** | 20 per row | None | 1 collection |

### **Validation Coverage**

#### **✅ Structure Validation**
- Required column presence (`title`, `status`, `data_items`)
- Valid column names against Dublin Core property URIs
- Non-empty DataFrame validation
- Collection-specific field requirements

#### **✅ Content Validation**  
- Required field completeness
- Status value constraints (`pending`/`published`/`private`)
- Data items pattern format validation
- Multilingual format syntax (`lang:text|lang:text`)
- Date format recommendations (ISO 8601)
- Rights format validation (`group_id,ROLE`)
- Folder pattern reasonableness checking

#### **✅ Transformation Testing**
- Real metadata generation using `NakalaCommonUtils.prepare_nakala_metadata()`
- JSON structure validation
- Dublin Core property URI mapping verification
- Array handling for creators and contributors
- Language code processing
- Collection-specific field handling

## 🔧 Validation Logic

### **Required Fields Validation**
```python
required_columns = ['title', 'status', 'data_items']

# Check each row
def _validate_required_fields(row, row_num):
    # Title must be non-empty
    if pd.isna(title) or not str(title).strip():
        self.errors.append(f"Row {row_num}: Missing or empty title")
    
    # Status must be valid
    if status not in ['pending', 'published', 'private']:
        self.errors.append(f"Row {row_num}: Invalid status")
        
    # Data items must be non-empty
    if pd.isna(data_items) or not str(data_items).strip():
        self.errors.append(f"Row {row_num}: Missing data_items")
```

### **Folder Pattern Validation**
```python
def _is_valid_folder_pattern(pattern):
    common_patterns = [
        'files/', 'data/', 'code/', 'documents/', 'images/', 
        'results/', 'src/', 'scripts/', 'analysis/'
    ]
    return any(common in pattern.lower() for common in common_patterns)
```

### **Validation Levels**
1. **ERRORS** - Must be fixed before collection creation
   - Missing required fields (title, status, data_items)
   - Invalid status values
   - Transformation failures
   - Malformed metadata structures

2. **WARNINGS** - Should be reviewed
   - Unknown columns (ignored during processing)
   - Suboptimal formats (date formats, pattern formats)
   - Incomplete multilingual syntax
   - Unusual folder patterns

3. **INFO** - Processing details
   - Row and column counts
   - Metadata generation statistics
   - Successful transformation confirmations

## 🎓 Using Validation in Workflow

### **1. Pre-Creation Validation**
```bash
# Always validate before creating collections
python tools/collection_validator.py my_collections.csv

# If valid, proceed with creation
python -m src.nakala_client.cli.collection \
  --from-folder-collections my_collections.csv \
  --from-upload-output upload_report.csv \
  --api-key $API_KEY
```

### **2. Automated Testing**
```bash
# Test all collection examples automatically
for file in docs/endpoints/collection-endpoint/examples/*.csv; do
    echo "Testing $file..."
    python tools/collection_validator.py "$file"
done
```

### **3. Continuous Integration**
```yaml
# Example CI pipeline step
- name: Validate Collection CSV examples
  run: |
    for csv in docs/endpoints/collection-endpoint/examples/*.csv; do
      python tools/collection_validator.py "$csv" || exit 1
    done
```

## 🐛 Common Issues & Solutions

### **Issue: "Missing required columns"**
**Solution**: Ensure CSV has required columns
```csv
# Required columns for collections
title,status,data_items

# Optional but common
title,status,description,keywords,creator,data_items
```

### **Issue: "Invalid status"**
**Solution**: Use only valid status values
```csv
status
pending     # ✅ Valid
published   # ✅ Valid  
private     # ✅ Valid
draft       # ❌ Invalid
active      # ❌ Invalid
```

### **Issue: "Missing or empty data_items"**
**Solution**: Provide folder patterns for dataset matching
```csv
# ✅ Correct patterns
data_items
"files/code/"
"files/data/|files/results/"
"code|programming|analysis"

# ❌ Empty or missing
data_items
""
```

### **Issue: "Transformation failed"**
**Solution**: Check multilingual field formats
```csv
# ✅ Correct multilingual format
title
"fr:Collection française|en:French Collection"

# ❌ Incorrect format
title
"Collection française - French Collection"
```

### **Issue: "Pattern may not match typical folder structures"**
**Solution**: Use recognizable folder patterns
```csv
# ✅ Good patterns
data_items
"files/code/"
"data/"
"results/"

# ⚠️ May not match
data_items
"xyz/"
"temp/"
```

## 📈 Validation Reports

### **Sample Report Structure**
```markdown
# Collection CSV Validation Report

**Status**: ✅ VALID / ❌ INVALID
**Errors**: N
**Warnings**: N

## Information
- ℹ️ Loaded CSV with X rows and Y columns
- ℹ️ Row N: Generated X metadata entries

## Errors (if any)
- ❌ Row N: Specific error description

## Warnings (if any)  
- ⚠️ Row N: Warning description

## Recommendations
- Specific actionable recommendations
```

## 🎯 Collection-Specific Validation Features

### **Dublin Core Field Support**
The validator recognizes all Dublin Core fields supported by collections:
- **Core fields**: title, description, creator, contributor, publisher
- **Extended fields**: coverage, relation, source, language, date
- **Technical fields**: rights, keywords (subject), data_items

### **Folder Pattern Intelligence**
- **Common patterns**: Recognizes standard folder names
- **Multiple patterns**: Validates pipe-separated pattern lists
- **Pattern warnings**: Flags unusual patterns that may not match

### **Multilingual Validation**
- **Syntax checking**: Validates `lang:text|lang:text` format
- **Language codes**: Checks for reasonable language code formats
- **Content validation**: Ensures non-empty text for each language

### **Metadata Generation Testing**
- **Real transformation**: Uses actual `NakalaCommonUtils` functions
- **Structure validation**: Checks generated JSON metadata structure
- **Property URI mapping**: Validates correct Dublin Core mappings

## 🔗 Related Documentation

- **[CSV Format Specification](../csv-format-specification.md)** - Complete format rules
- **[Field Transformations](../field-transformations.md)** - Transformation logic
- **[Examples](../examples/)** - Working collection CSV examples
- **[Collection Overview](../README.md)** - Collection workflow and architecture

---

**Tool version**: v1.0 ✅  
**All examples validated**: ✅  
**Metadata generation tested**: ✅  
**Last updated**: 2025-06-09