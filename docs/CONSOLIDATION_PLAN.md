# O-Nakala Core Consolidation Plan

## 🎯 **Goal: Unified CSV Workflow**

Make the curator fully compatible with existing rich sample datasets, eliminating the gap between upload and curation capabilities.

---

## 🔍 **Current State Analysis**

### **Upload Client Capabilities**
- ✅ Processes 17+ fields directly from sample datasets
- ✅ Handles complex multilingual patterns
- ✅ Supports creation workflows
- ✅ Complex rights and access control

### **Curator Limitations**  
- ❌ Requires `new_` prefixes for modifications only
- ❌ Missing 5+ critical fields (rights, accessRights, status)
- ❌ Cannot create new resources (modification-only)
- ❌ Incomplete multilingual format support

### **Gap Impact**
- Users can upload with rich CSV but can't modify with same format
- Sample datasets are incompatible with curator
- Fragmented user experience

---

## 📋 **Phase 1: Critical Field Integration (Week 1-2)**

### **Add Missing Field Mappings**

#### **Priority 1: Access Control Fields**
```python
# Add to CSV_FIELD_MAPPINGS in curator.py:

'rights': {
    'api_field': 'rights',
    'property_uri': 'http://purl.org/dc/terms/rights',
    'multilingual': False,
    'required': False,
    'format': 'rights_list'
},
'accessRights': {
    'api_field': 'accessRights',
    'property_uri': 'http://purl.org/dc/terms/accessRights',
    'multilingual': False,
    'required': False
},
'status': {
    'api_field': 'status',
    'property_uri': 'http://nakala.fr/terms#status',
    'multilingual': False,
    'required': False,
    'controlled_vocabulary': ['draft', 'pending', 'published', 'embargoed']
}
```

#### **Priority 2: Technical Fields**
```python
'file': {
    'api_field': 'file',
    'property_uri': 'http://nakala.fr/terms#file',
    'multilingual': False,
    'required': False,
    'format': 'file_reference'
},
'data_items': {
    'api_field': 'dataItems',
    'property_uri': 'http://nakala.fr/terms#dataItems',
    'multilingual': False,
    'required': False,
    'format': 'folder_patterns'
}
```

### **Dual Field Name Support**

#### **Flexible CSV Parser**
```python
def parse_csv_modifications(self, csv_path: str, mode='modify'):
    """
    Enhanced parser supporting both creation and modification formats.
    
    Modes:
    - 'modify': Expects new_ prefixes, requires 'action' column
    - 'create': Direct field names, creates new resources
    - 'auto': Auto-detect based on column names
    """
    
    modifications = []
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        # Auto-detect mode if not specified
        if mode == 'auto':
            mode = self._detect_csv_mode(reader.fieldnames)
            
        for row_num, row in enumerate(reader, start=2):
            
            if mode == 'modify':
                # Current modification mode (requires action column)
                if row.get("action") == "modify":
                    changes = self._parse_modification_row(row)
                    if changes:
                        modifications.append({
                            "id": row["id"], 
                            "changes": changes,
                            "row_number": row_num
                        })
                        
            elif mode == 'create':
                # New creation mode (direct field names)
                changes = self._parse_creation_row(row)
                if changes:
                    modifications.append({
                        "file_or_folder": row.get("file", row.get("folder", "")),
                        "metadata": changes,
                        "row_number": row_num
                    })
    
    return modifications

def _detect_csv_mode(self, fieldnames):
    """Auto-detect CSV format based on column names."""
    if 'action' in fieldnames and any(f.startswith('new_') for f in fieldnames):
        return 'modify'
    elif 'file' in fieldnames or 'folder' in fieldnames:
        return 'create'
    else:
        return 'modify'  # Default to modification mode

def _parse_creation_row(self, row):
    """Parse row with direct field names (upload format)."""
    changes = {}
    
    for csv_field, value in row.items():
        if csv_field and value and str(value).strip():
            
            # Map direct field names to curator mappings
            curator_field = self._map_direct_field_to_curator(csv_field)
            
            if curator_field and curator_field in CSV_FIELD_MAPPINGS:
                field_config = CSV_FIELD_MAPPINGS[curator_field]
                api_field = field_config['api_field']
                
                # Process value according to field configuration
                processed_value = self._process_field_value(value, field_config)
                changes[api_field] = processed_value
                
    return changes

def _map_direct_field_to_curator(self, field_name):
    """Map direct field names to curator field names."""
    mapping = {
        'title': 'new_title',
        'description': 'new_description', 
        'keywords': 'new_keywords',
        'author': 'new_author',
        'creator': 'new_creator',
        'contributor': 'new_contributor',
        'license': 'new_license',
        'type': 'new_type',
        'date': 'new_date',
        'language': 'new_language',
        'temporal': 'new_temporal',
        'spatial': 'new_spatial',
        'relation': 'new_relation',
        'source': 'new_source',
        'identifier': 'new_identifier',
        'alternative': 'new_alternative',
        'publisher': 'new_publisher',
        'rights': 'rights',
        'accessRights': 'accessRights', 
        'status': 'status'
    }
    return mapping.get(field_name)
```

---

## 📋 **Phase 2: Enhanced Format Support (Week 2-3)**

### **Complex Multilingual Patterns**

#### **Enhanced Multilingual Processing**
```python
def _process_multilingual_field(self, value, field_config):
    """Enhanced multilingual field processing."""
    
    # Handle complex patterns like "fr:fr|en:en" for language field
    if field_config['api_field'] == 'language' and '|' in str(value):
        # Extract language codes from pattern
        parts = str(value).split('|')
        languages = []
        for part in parts:
            if ':' in part:
                lang_code = part.split(':')[1]
                if lang_code not in languages:
                    languages.append(lang_code)
        return languages[0] if languages else 'fr'  # Default to first language
    
    # Handle standard multilingual patterns "fr:text|en:text" 
    if '|' in str(value):
        entries = []
        parts = str(value).split('|')
        for part in parts:
            if ':' in part:
                lang, content = part.split(':', 1)
                
                if field_config['api_field'] == 'keywords':
                    # Handle semicolon-separated keywords
                    keywords = content.split(';')
                    for keyword in keywords:
                        if keyword.strip():
                            entries.append({
                                "value": keyword.strip(),
                                "lang": lang,
                                "propertyUri": field_config['property_uri']
                            })
                else:
                    entries.append({
                        "value": content,
                        "lang": lang, 
                        "propertyUri": field_config['property_uri']
                    })
        return entries
    
    # Simple non-multilingual value
    return str(value).strip()
```

### **Rights and Access Control**

#### **Rights Format Processing**
```python
def _process_rights_field(self, value, field_config):
    """Process complex rights format."""
    
    # Handle format: "group_uuid,ROLE_READER" 
    if ',' in str(value):
        parts = str(value).split(',')
        if len(parts) == 2:
            group_id, role = parts
            return {
                "groupId": group_id.strip(),
                "role": role.strip()
            }
    
    # Handle simple rights text
    return {
        "value": str(value).strip(),
        "propertyUri": field_config['property_uri']
    }
```

---

## 📋 **Phase 3: Unified CLI Interface (Week 3)**

### **Enhanced Curator Commands**

#### **Support Both Creation and Modification**
```bash
# Current modification workflow
nakala-curator --batch-modify modifications.csv --scope collections

# New creation workflow (using existing sample dataset format)
nakala-curator --batch-create folder_data_items.csv --mode create --scope datasets
nakala-curator --batch-create folder_collections.csv --mode create --scope collections

# Auto-detect mode
nakala-curator --batch-process folder_data_items.csv --auto-detect
```

#### **Template Generation for Both Modes**
```bash
# Generate modification template (current)
nakala-curator --export-template modifications_template.csv --scope collections --mode modify

# Generate creation template (new)
nakala-curator --export-template creation_template.csv --scope datasets --mode create

# Generate template matching existing sample format
nakala-curator --export-template sample_format.csv --format sample-dataset
```

---

## 📋 **Phase 4: Validation Enhancement (Week 3-4)**

### **Comprehensive Validation**

#### **Support Both Workflow Types**
```python
def validate_metadata(self, metadata, mode='modify'):
    """Enhanced validation supporting both creation and modification."""
    
    validation_result = {
        'errors': [],
        'warnings': [],
        'suggestions': []
    }
    
    if mode == 'create':
        # Strict validation for new resources
        required_fields = self._get_required_fields_for_creation()
        validation_result['errors'].extend(
            self._validate_required_fields(metadata, required_fields)
        )
    elif mode == 'modify':
        # Permissive validation for modifications
        validation_result['warnings'].extend(
            self._validate_modification_fields(metadata)
        )
    
    # Common validation for both modes
    validation_result['errors'].extend(
        self._validate_field_formats(metadata)
    )
    validation_result['warnings'].extend(
        self._validate_controlled_vocabularies(metadata)
    )
    
    return validation_result
```

---

## 🎯 **Success Criteria**

### **Week 2 Milestone**
- ✅ Curator can process existing `folder_data_items.csv` without modifications
- ✅ All 17 fields from sample datasets are supported
- ✅ Rights and access control fields working

### **Week 3 Milestone**  
- ✅ Curator can process existing `folder_collections.csv` without modifications
- ✅ Complex multilingual patterns handled correctly
- ✅ Both creation and modification workflows working

### **Week 4 Milestone**
- ✅ Complete validation for both workflow types
- ✅ Template generation matching sample format
- ✅ Comprehensive test coverage

---

## 🚀 **Benefits of Consolidation**

### **Immediate Benefits**
- **Single CSV format** for both upload and curation
- **Utilize full potential** of existing sample datasets  
- **Reduced user confusion** and support burden
- **Better test coverage** using real-world examples

### **Foundation for Roadmap**
- **Comprehensive field support** as baseline for dynamic discovery
- **Unified architecture** ready for intelligent enhancements
- **Real-world validation** of complex multilingual patterns
- **User experience consistency** for future wizard interface

---

## 📈 **Next Steps After Consolidation**

With a consolidated, comprehensive curator supporting all sample dataset capabilities:

1. **Enhanced Validation** with vocabulary integration
2. **Dynamic Field Discovery** from NAKALA APIs  
3. **Intelligent Pre-population** based on user context
4. **Interactive Wizard** building on solid foundation

**Timeline**: 3-4 weeks for consolidation → Ready for advanced roadmap implementation

---

**Result**: Transform curator from "modification-only tool with gaps" to "comprehensive metadata management foundation" that fully leverages our existing rich sample datasets and provides consistent user experience.