# Curator Endpoint Validation

## 🎯 Overview

This directory contains **validation tools and reports** for Curator endpoint CSV files. The validation system ensures batch modifications can be applied successfully with proper field transformation, multilingual processing, and access rights management.

## 🛠️ Available Tools

### **1. Curator CSV Validator** (`/tools/curator_validator.py`)
**Purpose**: Comprehensive validation of Curator endpoint CSV files for batch modification

**Features**:
- ✅ **Structure validation** - Required columns (id, action) and new_ prefix fields
- ✅ **Content validation** - NAKALA ID format and modification field validation
- ✅ **Transformation testing** - Real metadata generation with 280+ field mappings
- ✅ **Multilingual validation** - Language syntax and format verification
- ✅ **Rights validation** - Access rights format checking
- ✅ **Modification analysis** - Ensures meaningful modifications are specified
- ✅ **Detailed reporting** - Human-readable validation reports

**Usage**:
```bash
# Basic validation
python tools/curator_validator.py path/to/modifications.csv

# Generate JSON report
python tools/curator_validator.py path/to/modifications.csv --json

# Save report to file
python tools/curator_validator.py path/to/modifications.csv --report validation_report.md
```

## 📊 Validation Results

### **Example Files Validation Status**

| Example File | Status | Metadata Entries | Total Modifications | Issues |
|-------------|--------|------------------|-------------------|--------|
| `basic-modification.csv` | ✅ **VALID** | 3 per row | 3 per row | None |
| `multilingual-modification.csv` | ✅ **VALID** | 9-10 per row | 9-10 per row | None |
| `complete-modification.csv` | ✅ **VALID** | 17 per row | 19 per row | None |
| `rights-management.csv` | ✅ **VALID** | 0 per row* | 2 per row | None |

*Rights and status modifications go to top-level fields, not metadata array

### **Validation Coverage**

#### **✅ Structure Validation**
- Required column presence (`id`, `action`)
- Valid action value (`modify` only)
- Modification field detection (`new_*` prefix)
- Curator-specific column validation
- Template export field recognition (`current_*` columns)

#### **✅ Content Validation**
- NAKALA identifier format validation
- Modification field completeness
- Action value constraints (`modify` only)
- Multilingual format syntax (`lang:text|lang:text`)
- Rights format validation (`group_id,ROLE_NAME`)
- Status value validation (`pending`/`published`/`private`)

#### **✅ Transformation Testing**
- Real field mapping using curator-specific transformations
- Format-specific processing (multilingual, semicolon_split, array, rights_list)
- JSON structure validation
- Property URI mapping verification
- Modification counting and analysis

## 🔧 Validation Logic

### **Required Fields Validation**
```python
required_columns = ['id', 'action']

def _validate_required_fields(row, row_num):
    # NAKALA ID format validation
    if not self._is_valid_nakala_id(resource_id):
        self.errors.append(f"Invalid NAKALA identifier: {resource_id}")
    
    # Action must be 'modify'
    if str(action).strip() != 'modify':
        self.errors.append(f"Invalid action '{action}' - must be 'modify'")
```

### **NAKALA ID Validation**
```python
def _is_valid_nakala_id(identifier):
    # Validates formats like:
    # 10.34847/nkl.abc12345
    # 11280/def67890 
    # 10.34847/nkl.ghi09876.v2
    pattern = r'^((10\.34847/nkl\.|11280/)[a-z0-9]{8})(\\.v([0-9]+))?$'
    return bool(re.match(pattern, identifier))
```

### **Modification Field Processing**
```python
def _test_transformation(df):
    for field, value in row_dict.items():
        if field.startswith('new_') and field in CURATOR_FIELD_MAPPINGS:
            field_config = CURATOR_FIELD_MAPPINGS[field]
            
            # Process by format type
            if field_config['format'] == 'multilingual':
                entries = process_multilingual_field(value, property_uri)
            elif field_config['format'] == 'semicolon_split':
                entries = process_semicolon_split_field(value, property_uri)
            # ... etc
```

### **Validation Levels**
1. **ERRORS** - Must be fixed before batch modification
   - Missing required fields (id, action)
   - Invalid NAKALA identifier formats
   - Invalid action values (not 'modify')
   - Malformed rights format
   - Invalid status values
   - Transformation failures

2. **WARNINGS** - Should be reviewed
   - No modification fields specified
   - Unknown columns (ignored during processing)
   - Suboptimal formats (language codes, multilingual syntax)
   - Unknown roles in rights field

3. **INFO** - Processing details
   - Row and column counts
   - Metadata generation statistics
   - Total modification counts

## 🎓 Using Validation in Workflow

### **1. Pre-Modification Validation**
```bash
# Always validate before applying modifications
python tools/curator_validator.py my_modifications.csv

# If valid, proceed with dry run
python -m src.nakala_client.cli.curator \
  --modify-metadata my_modifications.csv \
  --api-key $API_KEY \
  --dry-run
```

### **2. Template Validation**
```bash
# Export template and validate
python -m src.nakala_client.cli.curator \
  --export-template \
  --ids "id1,id2,id3" \
  --output template.csv

# Edit template, then validate
python tools/curator_validator.py template.csv
```

### **3. Automated Testing**
```bash
# Test all curator examples automatically
for file in docs/endpoints/curator-endpoint/examples/*.csv; do
    echo "Testing $file..."
    python tools/curator_validator.py "$file"
done
```

### **4. Continuous Integration**
```yaml
# Example CI pipeline step
- name: Validate Curator CSV examples
  run: |
    for csv in docs/endpoints/curator-endpoint/examples/*.csv; do
      python tools/curator_validator.py "$csv" || exit 1
    done
```

## 🐛 Common Issues & Solutions

### **Issue: "Invalid NAKALA identifier format"**
**Solution**: Use proper NAKALA identifier format
```csv
# ✅ Correct formats
id
10.34847/nkl.abc12345
11280/def67890
10.34847/nkl.ghi09876.v2

# ❌ Invalid formats
id
abc123
nakala-123
nkl.abc123
```

### **Issue: "Invalid action - must be 'modify'"**
**Solution**: Use exactly 'modify' for action
```csv
# ✅ Correct
action
modify

# ❌ Invalid
action
update
edit
change
```

### **Issue: "No modification fields (new_*) found"**
**Solution**: Include at least one new_ prefixed field
```csv
# ✅ Correct - has modification fields
id,action,new_title,new_description
10.34847/nkl.abc123,modify,"New Title","New Description"

# ❌ No modifications
id,action
10.34847/nkl.abc123,modify
```

### **Issue: "Rights entry must be in format 'group_id,ROLE_NAME'"**
**Solution**: Use correct rights format
```csv
# ✅ Correct
new_rights
"group123,ROLE_READER"
"group1,ROLE_EDITOR;group2,ROLE_READER"

# ❌ Incorrect
new_rights
"READER:group123"
"group123=READER"
"group123 READER"
```

### **Issue: "Multilingual part missing language code"**
**Solution**: Use proper multilingual syntax
```csv
# ✅ Correct multilingual format
new_title
"fr:Titre français|en:English Title"

# ❌ Incorrect format
new_title
"Titre français|English Title"
"fr-Titre français|en-English Title"
```

## 📈 Validation Reports

### **Sample Report Structure**
```markdown
# Curator CSV Validation Report

**Status**: ✅ VALID / ❌ INVALID
**Errors**: N
**Warnings**: N

## Information
- ℹ️ Loaded CSV with X rows and Y columns
- ℹ️ Row N: Generated X metadata entries (Y total modifications)

## Errors (if any)
- ❌ Row N: Specific error description

## Warnings (if any)
- ⚠️ Row N: Warning description

## Recommendations
- Specific actionable recommendations
```

## 🎯 Curator-Specific Validation Features

### **Field Format Recognition**
The validator recognizes all curator field formats:
- **`multilingual`**: title, description, keywords, publisher, coverage, etc.
- **`semicolon_split`**: creator (creates individual metadata entries)
- **`array`**: contributor (creates array-based metadata)
- **`rights_list`**: rights (creates rights array structure)
- **`string`**: language, format, identifier, status

### **Modification Analysis**
- **Field counting**: Tracks metadata vs top-level modifications
- **Content analysis**: Ensures meaningful modifications are specified
- **Empty field handling**: Ignores empty modification fields
- **Template support**: Recognizes current_* columns from exports

### **NAKALA ID Intelligence**
- **Format validation**: Supports both 10.34847/nkl.* and 11280/* formats
- **Version support**: Handles versioned identifiers (.v2, .v3, etc.)
- **Error guidance**: Provides specific format error messages

### **Rights Management Validation**
- **Format checking**: Validates group_id,ROLE format
- **Role validation**: Checks against known NAKALA roles
- **Multiple rights**: Supports semicolon-separated rights lists
- **Error specificity**: Pinpoints exact format issues

## 🔄 Transformation Testing

### **Real Field Processing**
```python
# Test actual curator transformations
field_config = CURATOR_FIELD_MAPPINGS["new_title"]
# Result: {"property_uri": "http://nakala.fr/terms#title", "format": "multilingual"}

processed_metadata = process_multilingual_field(value, property_uri)
# Result: [{"propertyUri": "...", "value": "...", "lang": "fr"}]
```

### **Validation Integration**
- **Structure checking**: Validates generated JSON metadata
- **Property URI mapping**: Verifies correct field mappings
- **Format compliance**: Tests format-specific processing
- **Error detection**: Catches transformation failures

## 🔗 Related Documentation

- **[CSV Format Specification](../csv-format-specification.md)** - Complete format rules
- **[Field Transformations](../field-transformations.md)** - 280+ field transformation logic
- **[Examples](../examples/)** - Working curator CSV examples
- **[Curator Overview](../README.md)** - Batch modification workflow

---

**Tool version**: v1.0 ✅  
**All examples validated**: ✅  
**Field mappings tested**: 280+ mappings ✅  
**NAKALA ID validation**: Full format support ✅  
**Last updated**: 2025-06-09