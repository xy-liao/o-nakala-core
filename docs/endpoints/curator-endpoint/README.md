# Curator Endpoint Documentation

## 🎯 Overview

The **Curator endpoint** provides **batch metadata curation** capabilities for existing NAKALA resources. Unlike Upload and Collection endpoints that create new resources, the Curator endpoint **modifies existing datasets and collections** through sophisticated CSV-based batch operations.

## 🔄 Curator Workflow

### **Standard Curation Process**
```mermaid
graph LR
    A[Existing Resources] --> B[Export Curator Template]
    B --> C[Edit CSV Metadata]
    C --> D[Validate Modifications]
    D --> E[Batch Apply Changes]
    E --> F[Updated Resources]
```

### **Key Capabilities**
| Capability | Description | Use Case |
|------------|-------------|----------|
| **Batch Metadata Editing** | Modify metadata for multiple resources | Quality improvement campaigns |
| **Template Export** | Generate CSV templates from existing data | Systematic metadata enhancement |
| **Multilingual Updates** | Add/edit multilingual metadata | Internationalization projects |
| **Access Rights Management** | Batch modify permissions | Rights management workflows |
| **Quality Analysis** | Metadata quality assessment | Data quality auditing |

## 🏗️ Curator Architecture

### **CSV Processing Modes**

#### **1. Modification Mode** (Primary)
**Purpose**: Edit existing resource metadata
**Format**: Uses `new_` prefix for all modification fields
```csv
id,action,new_title,new_description,new_keywords
10.34847/nkl.abc123,modify,"Updated Title","Updated Description","new;keywords"
```

#### **2. Creation Mode** (Legacy)
**Purpose**: Create new resources (similar to Upload endpoint)
**Format**: Standard field names without prefixes
```csv
file,status,type,title,description
files/data.csv,pending,dataset,"Title","Description"
```

### **CSV-to-JSON Transformation Pipeline**
```python
# Step 1: CSV Mode Detection
csv_mode = detect_csv_mode(fieldnames)
# Result: 'modify' for curator operations, 'create' for upload-style

# Step 2: Field Mapping Resolution
field_config = CSV_FIELD_MAPPINGS[csv_field]
# Maps: new_title → http://nakala.fr/terms#title

# Step 3: Value Processing
processed_value = process_field_value(value, field_config)
# Handles: multilingual, semicolon_split, array formats

# Step 4: JSON Metadata Generation
metadata_entry = {
    "propertyUri": field_config['property_uri'],
    "value": processed_value,
    "lang": language_code,  # for multilingual
    "typeUri": "http://www.w3.org/2001/XMLSchema#string"
}
```

## 🎯 Quick Start Guide

### **Prerequisites**
1. **Existing Resources**: Datasets or collections already in NAKALA
2. **Resource IDs**: NAKALA identifiers for resources to modify
3. **API Access**: Valid NAKALA API key with modification rights

### **Basic Batch Modification**
```bash
# 1. Export template from existing resources
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --export-template \
  --ids "10.34847/nkl.abc123,10.34847/nkl.def456" \
  --output curator_template.csv

# 2. Edit the CSV file with desired changes
# Modify new_title, new_description, etc. columns

# 3. Dry run to preview changes
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --modify-metadata curator_template.csv \
  --dry-run

# 4. Apply modifications
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --modify-metadata curator_template.csv
```

### **Template Export Options**
```bash
# Export specific resources
o-nakala-curator \
  --export-template \
  --ids "id1,id2,id3" \
  --output template.csv

# Export from collection
o-nakala-curator \
  --export-template \
  --collection-id "10.34847/nkl.collection123" \
  --output collection_template.csv

# Export with quality analysis
o-nakala-curator \
  --export-template \
  --ids "id1,id2" \
  --analyze-quality \
  --output analyzed_template.csv
```

## 🔧 Processing Features

### **1. Intelligent CSV Detection**
**Code Reference**: `src/o_nakala_core/curator.py:1434`
```python
def _detect_csv_mode(self, fieldnames):
    if 'action' in fieldnames and any(f.startswith('new_') for f in fieldnames):
        return 'modify'  # Curator modification format
    elif 'file' in fieldnames or 'folder' in fieldnames:
        return 'create'  # Upload format
    else:
        return 'modify'  # Default to modification
```

### **2. Comprehensive Field Mapping**
**280+ Field Mappings** covering:
- **Core metadata**: title, description, creator, contributor
- **Dublin Core extended**: coverage, relation, source, publisher
- **Access control**: rights, accessRights, status
- **Technical**: format, identifier, alternative

### **3. Advanced Value Processing**
- **Multilingual**: `"fr:Français|en:English"` → separate metadata entries
- **Semicolon split**: `"Author1;Author2"` → multiple creator entries
- **Array format**: Direct array values for contributor fields
- **Rights processing**: `"group_id,ROLE"` → proper rights structures

### **4. Batch Processing with Safety**
- **Configurable batch sizes**: Prevent API overload
- **Rate limiting**: Automatic delay between API calls
- **Error recovery**: Continue processing after individual failures
- **Comprehensive logging**: Detailed operation reporting

## 🎓 Curator CSV Format

### **Required Structure**
```csv
id,action,new_title,new_description
10.34847/nkl.example123,modify,"Updated Title","Updated Description"
```

### **Core Required Fields**
- **`id`**: NAKALA resource identifier
- **`action`**: Operation type (must be `modify`)
- **Modification fields**: Any field with `new_` prefix

### **Supported Modification Fields**
- **`new_title`**: Resource title (supports multilingual)
- **`new_description`**: Resource description (supports multilingual)
- **`new_keywords`**: Subject keywords (semicolon-separated)
- **`new_creator`**: Creator(s) (semicolon-separated)
- **`new_contributor`**: Contributor(s) (semicolon-separated)
- **`new_rights`**: Access rights (group_id,ROLE format)
- **`new_status`**: Publication status
- **`new_language`**: Primary language
- **Extended Dublin Core**: coverage, relation, source, publisher

## 🌐 Multilingual Enhancement

### **Adding Multilingual Metadata**
```csv
id,action,new_title,new_description
10.34847/nkl.abc123,modify,"fr:Titre français|en:English Title","fr:Description française|en:English Description"
```

### **Language Processing Logic**
1. **Parse multilingual**: Split by `|` for languages
2. **Extract language codes**: Split by `:` for lang/text
3. **Generate metadata**: Separate entries per language
4. **Preserve existing**: Only replace specified languages

## 📊 Template Export Features

### **Current Value Preservation**
Generated templates include both current and modification columns:
```csv
id,current_title,new_title,current_description,new_description
10.34847/nkl.abc123,"Current Title","","Current Description",""
```

### **Quality Analysis Integration**
Templates can include quality assessment:
```csv
id,quality_score,missing_fields,new_title,new_description
10.34847/nkl.abc123,75,"creator;language","","Enhanced Description"
```

## 🔍 Quality Analysis Features

### **Metadata Quality Metrics**
- **Completeness**: Percentage of filled vs empty fields
- **Language coverage**: Multilingual metadata availability  
- **Required fields**: Presence of essential metadata
- **Format compliance**: Standard format adherence

### **Quality Reports**
- **Resource-level scores**: Individual quality assessments
- **Batch statistics**: Overall quality metrics
- **Improvement recommendations**: Specific enhancement suggestions
- **Trend analysis**: Quality changes over time

## 📈 Expected Results

### **Successful Batch Modification**
- **Resources updated**: One per CSV row with valid modifications
- **Metadata preserved**: Existing metadata not being modified remains
- **Multilingual entries**: Separate metadata per language
- **Access rights**: Updated permissions as specified
- **Operation report**: Detailed success/failure logging

### **Modification Report Output**
```csv
id,status,modified_fields,errors,warnings
10.34847/nkl.abc123,success,"title;description",,"Language code 'und' used"
10.34847/nkl.def456,failed,"",Field validation error,""
```

## 🛠️ Advanced Operations

### **Rights Management**
```csv
id,action,new_rights
10.34847/nkl.abc123,modify,"group_id1,ROLE_READER;group_id2,ROLE_EDITOR"
```

### **Status Batch Updates**
```csv
id,action,new_status
10.34847/nkl.abc123,modify,published
10.34847/nkl.def456,modify,pending
```

### **Institutional Metadata**
```csv
id,action,new_contributor,new_publisher
10.34847/nkl.abc123,modify,"fr:CNRS;Université|en:CNRS;University","Research Institute"
```

## 🔗 Related Documentation

- **[CSV Format Specification](./csv-format-specification.md)** - Complete CSV format rules
- **[Field Transformations](./field-transformations.md)** - Field-by-field transformation logic
- **[Examples](../../../examples/sample_dataset/)** - Working curator CSV examples
- **[Validation](./validation/)** - Curator CSV validation tools

---

**API Endpoints**: `/datas/{id}`, `/collections/{id}` (PUT)  
**Authentication**: API key with modification rights required  
**Rate Limits**: Configurable batch processing with delays  
**Last Updated**: 2025-06-09