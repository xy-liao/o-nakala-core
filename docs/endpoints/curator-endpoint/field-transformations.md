# Curator Field Transformations

## 🎯 Overview

This document provides **field-by-field transformation logic** for Curator endpoint CSV processing. The Curator endpoint specializes in **batch metadata modification** with sophisticated field mapping, multilingual processing, and selective update capabilities.

## 🏗️ Transformation Architecture

### **Processing Pipeline**
```python
# Step 1: CSV Row Input (Modification Format)
csv_row = {
    "id": "10.34847/nkl.abc12345",
    "action": "modify",
    "new_title": "fr:Nouveau titre|en:New Title",
    "new_description": "fr:Description mise à jour|en:Updated description",
    "new_keywords": "fr:recherche;données|en:research;data",
    "new_creator": "Smith, John;Doe, Jane"
}

# Step 2: Field Resolution via CSV_FIELD_MAPPINGS
field_config = CSV_FIELD_MAPPINGS["new_title"]
# Result: {
#   'property_uri': 'http://nakala.fr/terms#title',
#   'format': 'multilingual',
#   'required': False
# }

# Step 3: Value Processing by Format Type
processed_metadata = process_field_value(value, field_config)

# Step 4: JSON Metadata Generation
updated_metas = generate_metadata_entries(processed_metadata)
```

### **Code Location**: `src/o_nakala_core/curator.py:1624+`
```python
def _apply_modification(self, item_id: str, modifications: Dict[str, Any]) -> Dict[str, Any]:
    # Process each modification field
    for csv_field, value in modifications.items():
        if csv_field in self.CSV_FIELD_MAPPINGS:
            field_config = self.CSV_FIELD_MAPPINGS[csv_field]
            processed_value = self._process_field_value(value, field_config)
            # Generate JSON metadata for API
```

## 📋 Field-by-Field Transformations

### **1. ID Field (Required)**

#### **CSV Input**
```csv
id
10.34847/nkl.abc12345
11280/def67890
```

#### **Transformation Logic**
- **Purpose**: Target resource identification
- **Validation**: NAKALA identifier format checking
- **API Usage**: Used in PUT request URL path

#### **Processing**
```python
# Validation
if not self._is_valid_nakala_id(item_id):
    raise ValueError(f"Invalid NAKALA identifier: {item_id}")

# API endpoint construction
api_url = f"{self.base_url}/datas/{item_id}"
```

#### **No JSON Output**: Used for API routing, not in metadata

### **2. Action Field (Required)**

#### **CSV Input**
```csv
action
modify
```

#### **Transformation Logic**
- **Purpose**: Operation type specification
- **Validation**: Must be exactly `modify`
- **Processing**: Controls CSV parsing mode

#### **Processing**
```python
def _detect_csv_mode(self, fieldnames):
    if 'action' in fieldnames and any(f.startswith('new_') for f in fieldnames):
        return 'modify'  # Curator modification mode
```

#### **No JSON Output**: Used for processing control, not in metadata

### **3. New Title Field**

#### **CSV Input**
```csv
new_title
"Updated Research Dataset"
"fr:Jeu de données de recherche|en:Research Dataset"
```

#### **Transformation Logic**
- **Property URI**: `http://nakala.fr/terms#title`
- **Format**: `multilingual`
- **Processing**: `parse_multilingual_value()`

#### **Code Reference**: `CSV_FIELD_MAPPINGS` line 89
```python
"new_title": {
    "property_uri": "http://nakala.fr/terms#title",
    "format": "multilingual",
    "required": False
}
```

#### **JSON Output**
```json
// Single language
{
    "propertyUri": "http://nakala.fr/terms#title",
    "value": "Updated Research Dataset",
    "lang": "und",
    "typeUri": "http://www.w3.org/2001/XMLSchema#string"
}

// Multilingual
[
    {
        "propertyUri": "http://nakala.fr/terms#title",
        "value": "Jeu de données de recherche",
        "lang": "fr",
        "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    },
    {
        "propertyUri": "http://nakala.fr/terms#title", 
        "value": "Research Dataset",
        "lang": "en",
        "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    }
]
```

### **4. New Description Field**

#### **CSV Input**
```csv
new_description
"Enhanced description with additional context"
"fr:Description améliorée|en:Enhanced description"
```

#### **Transformation Logic**
- **Property URI**: `http://purl.org/dc/terms/description`
- **Format**: `multilingual`
- **Processing**: Same multilingual parsing as title

#### **JSON Output**
```json
{
    "propertyUri": "http://purl.org/dc/terms/description",
    "value": "Enhanced description with additional context",
    "lang": "und",
    "typeUri": "http://www.w3.org/2001/XMLSchema#string"
}
```

### **5. New Keywords Field**

#### **CSV Input**
```csv
new_keywords
"research;data;analysis;updated"
"fr:recherche;données|en:research;data"
```

#### **Transformation Logic**
- **Property URI**: `http://purl.org/dc/terms/subject`
- **Format**: `multilingual`
- **Processing**: Split by semicolon, then by language

#### **Code Reference**: `CSV_FIELD_MAPPINGS` line 95
```python
"new_keywords": {
    "property_uri": "http://purl.org/dc/terms/subject",
    "format": "multilingual",
    "required": False
}
```

#### **Processing Logic**
```python
def process_keywords(value, lang=None):
    keywords = value.split(';')
    metadata_entries = []
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword:
            metadata_entries.append({
                "propertyUri": "http://purl.org/dc/terms/subject",
                "value": keyword,
                "lang": lang or "und",
                "typeUri": "http://www.w3.org/2001/XMLSchema#string"
            })
    return metadata_entries
```

#### **JSON Output**
```json
[
    {
        "propertyUri": "http://purl.org/dc/terms/subject",
        "value": "research",
        "lang": "und",
        "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    },
    {
        "propertyUri": "http://purl.org/dc/terms/subject",
        "value": "data",
        "lang": "und", 
        "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    },
    {
        "propertyUri": "http://purl.org/dc/terms/subject",
        "value": "analysis",
        "lang": "und",
        "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    }
]
```

### **6. New Creator Field**

#### **CSV Input**
```csv
new_creator
"Smith, John"
"Smith, John;Doe, Jane;Wilson, Sarah"
```

#### **Transformation Logic**
- **Property URI**: `http://nakala.fr/terms#creator`
- **Format**: `semicolon_split`
- **Processing**: Parse person format, create individual entries

#### **Code Reference**: `CSV_FIELD_MAPPINGS` line 101
```python
"new_creator": {
    "property_uri": "http://nakala.fr/terms#creator", 
    "format": "semicolon_split",
    "required": False
}
```

#### **Processing Logic**
```python
def process_semicolon_split(value, property_uri):
    persons = value.split(';')
    metadata_entries = []
    for person in persons:
        person = person.strip()
        if person:
            metadata_entries.append({
                "propertyUri": property_uri,
                "value": person,
                "typeUri": "http://www.w3.org/2001/XMLSchema#string"
            })
    return metadata_entries
```

#### **JSON Output**
```json
[
    {
        "propertyUri": "http://nakala.fr/terms#creator",
        "value": "Smith, John",
        "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    },
    {
        "propertyUri": "http://nakala.fr/terms#creator", 
        "value": "Doe, Jane",
        "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    },
    {
        "propertyUri": "http://nakala.fr/terms#creator",
        "value": "Wilson, Sarah", 
        "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    }
]
```

### **7. New Contributor Field**

#### **CSV Input**
```csv
new_contributor
"University Research Lab"
"fr:CNRS;Université|en:CNRS;University"
```

#### **Transformation Logic**
- **Property URI**: `http://purl.org/dc/terms/contributor`
- **Format**: `array`
- **Processing**: Create array-based metadata entry

#### **Code Reference**: `CSV_FIELD_MAPPINGS` line 107
```python
"new_contributor": {
    "property_uri": "http://purl.org/dc/terms/contributor",
    "format": "array", 
    "required": False
}
```

#### **Processing Logic**
```python
def process_array_format(value, property_uri):
    # For multilingual contributor fields
    if '|' in value:
        # Process multilingual array
        lang_entries = []
        for lang_part in value.split('|'):
            lang, text = lang_part.split(':', 1)
            contributors = text.split(';')
            contributor_objects = [{"name": c.strip()} for c in contributors if c.strip()]
            lang_entries.append({
                "propertyUri": property_uri,
                "value": contributor_objects,
                "lang": lang.strip()
            })
        return lang_entries
    else:
        # Simple array
        contributors = value.split(';')
        contributor_objects = [{"name": c.strip()} for c in contributors if c.strip()]
        return [{
            "propertyUri": property_uri,
            "value": contributor_objects
        }]
```

#### **JSON Output**
```json
// Simple contributor
{
    "propertyUri": "http://purl.org/dc/terms/contributor",
    "value": [
        {"name": "University Research Lab"}
    ]
}

// Multilingual contributor
[
    {
        "propertyUri": "http://purl.org/dc/terms/contributor",
        "value": [
            {"name": "CNRS"},
            {"name": "Université"}
        ],
        "lang": "fr"
    },
    {
        "propertyUri": "http://purl.org/dc/terms/contributor",
        "value": [
            {"name": "CNRS"}, 
            {"name": "University"}
        ],
        "lang": "en"
    }
]
```

### **8. New Rights Field**

#### **CSV Input**
```csv
new_rights
"de0f2a9b-a198-48a4-8074-db5120187a16,ROLE_READER"
"group1,ROLE_EDITOR;group2,ROLE_READER"
```

#### **Transformation Logic**
- **Property URI**: `http://purl.org/dc/terms/rights`
- **Format**: `rights_list`
- **Processing**: Parse group_id,ROLE format

#### **Code Reference**: `CSV_FIELD_MAPPINGS` line 113
```python
"new_rights": {
    "property_uri": "http://purl.org/dc/terms/rights",
    "format": "rights_list",
    "required": False
}
```

#### **Processing Logic**
```python
def process_rights_list(value):
    rights_entries = []
    for right_entry in value.split(';'):
        right_entry = right_entry.strip()
        if ',' in right_entry:
            group_id, role = right_entry.split(',', 1)
            rights_entries.append({
                "id": group_id.strip(),
                "role": role.strip()
            })
    return rights_entries
```

#### **JSON Output**
```json
// Note: Rights go in top-level "rights" array, not "metas"
{
    "rights": [
        {
            "id": "de0f2a9b-a198-48a4-8074-db5120187a16",
            "role": "ROLE_READER"
        }
    ]
}

// Multiple rights
{
    "rights": [
        {
            "id": "group1", 
            "role": "ROLE_EDITOR"
        },
        {
            "id": "group2",
            "role": "ROLE_READER"
        }
    ]
}
```

### **9. New Status Field**

#### **CSV Input**
```csv
new_status
published
pending
private
```

#### **Transformation Logic**
- **Property URI**: `http://nakala.fr/terms#status`
- **Format**: `string`
- **Processing**: Direct value assignment

#### **JSON Output**
```json
// Note: Status goes in top-level "status" field, not "metas"
{
    "status": "published"
}
```

### **10. Extended Dublin Core Fields**

#### **New Publisher**
```csv
new_publisher
"Research Institute"
```
**Property URI**: `http://purl.org/dc/terms/publisher`  
**Format**: `multilingual`
**JSON**: Standard multilingual metadata entry

#### **New Coverage**
```csv
new_coverage
"2020-2023"
"fr:France|en:France"
```
**Property URI**: `http://purl.org/dc/terms/coverage`  
**Format**: `multilingual`
**JSON**: Multilingual metadata entry

#### **New Language** 
```csv
new_language
fr
en
```
**Property URI**: `http://purl.org/dc/terms/language`  
**Format**: `string`
**JSON**: Simple string metadata entry

#### **New Alternative**
```csv
new_alternative
"Alternative Title"
```
**Property URI**: `http://purl.org/dc/terms/alternative`  
**Format**: `multilingual`
**JSON**: Multilingual metadata entry

## 🔄 Complete Transformation Example

### **Input CSV Row**
```csv
id,action,new_title,new_description,new_keywords,new_creator,new_contributor,new_rights,new_status
10.34847/nkl.abc12345,modify,"fr:Données mises à jour|en:Updated Data","fr:Description améliorée|en:Enhanced description","fr:recherche;données|en:research;data","Smith, John;Doe, Jane","fr:CNRS|en:CNRS","group123,ROLE_READER",published
```

### **Transformed JSON Payload**
```json
{
    "status": "published",
    "metas": [
        {
            "propertyUri": "http://nakala.fr/terms#title",
            "value": "Données mises à jour",
            "lang": "fr",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        },
        {
            "propertyUri": "http://nakala.fr/terms#title",
            "value": "Updated Data", 
            "lang": "en",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        },
        {
            "propertyUri": "http://purl.org/dc/terms/description",
            "value": "Description améliorée",
            "lang": "fr",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        },
        {
            "propertyUri": "http://purl.org/dc/terms/description",
            "value": "Enhanced description",
            "lang": "en", 
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        },
        {
            "propertyUri": "http://purl.org/dc/terms/subject",
            "value": "recherche",
            "lang": "fr",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        },
        {
            "propertyUri": "http://purl.org/dc/terms/subject",
            "value": "données",
            "lang": "fr",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        },
        {
            "propertyUri": "http://purl.org/dc/terms/subject", 
            "value": "research",
            "lang": "en",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        },
        {
            "propertyUri": "http://purl.org/dc/terms/subject",
            "value": "data",
            "lang": "en",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        },
        {
            "propertyUri": "http://nakala.fr/terms#creator",
            "value": "Smith, John",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        },
        {
            "propertyUri": "http://nakala.fr/terms#creator",
            "value": "Doe, Jane",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        },
        {
            "propertyUri": "http://purl.org/dc/terms/contributor",
            "value": [{"name": "CNRS"}],
            "lang": "fr"
        },
        {
            "propertyUri": "http://purl.org/dc/terms/contributor",
            "value": [{"name": "CNRS"}],
            "lang": "en"
        }
    ],
    "rights": [
        {
            "id": "group123",
            "role": "ROLE_READER"
        }
    ]
}
```

## 🎯 Key Transformation Rules

### **Field Processing Formats**
1. **`multilingual`**: Parse `lang:text|lang:text`, create entries per language
2. **`semicolon_split`**: Split by `;`, create individual metadata entries  
3. **`array`**: Create array-based metadata with object values
4. **`rights_list`**: Parse `group_id,ROLE`, create rights array
5. **`string`**: Direct string value assignment

### **Selective Modification**
1. **Empty fields**: Ignored, no modification applied
2. **Non-empty fields**: Replace existing metadata completely
3. **Missing fields**: Current metadata preserved unchanged
4. **Language merging**: Update specified languages only

### **Validation Strategy**
1. **Permissive modification**: Uses modification validation rules (less strict)
2. **Field existence**: Only validates fields being modified
3. **Format compliance**: Validates multilingual and rights syntax
4. **Resource access**: Verifies modification permissions

## 🔗 Related Documentation

- **[CSV Format Specification](../../CSV_FORMAT_GUIDE.md#curator-csv-format)** - Complete field format rules
- **[Examples](../../../examples/sample_dataset/)** - Working curator transformation examples
- **[Curator Code](../../src/o_nakala_core/curator.py)** - Complete transformation implementation
- **[CSV Field Mappings](../../src/o_nakala_core/curator.py#L89-L369)** - 280+ field mappings

---

**Transformation Version**: 1.0  
**Code Compatibility**: NAKALA Curator v2.0  
**Field Mappings**: 280+ supported transformations  
**Last Updated**: 2025-08-30