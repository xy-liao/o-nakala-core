# CSV to NAKALA API Transformation - Technical Analysis

## 🎯 Overview

The CSV-to-JSON transformation is the **technical heart** and **most complex component** of O-Nakala Core. This document provides a comprehensive technical analysis of how user-friendly CSV data is transformed into NAKALA API-compliant JSON structures.

## 🔥 The Core Challenge

### User Reality (Simple CSV Input)
```csv
title,description,keywords,creator
"My Research Data","Study of medieval manuscripts","manuscripts;medieval;research","Smith, John"
```

### NAKALA API Reality (Complex JSON Output)
```json
{
  "metas": [
    {
      "propertyUri": "http://nakala.fr/terms#title",
      "value": "My Research Data",
      "lang": "en",
      "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    },
    {
      "propertyUri": "http://nakala.fr/terms#description", 
      "value": "Study of medieval manuscripts",
      "lang": "en",
      "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    },
    {
      "propertyUri": "http://nakala.fr/terms#subject",
      "value": "manuscripts",
      "lang": "en",
      "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    },
    {
      "propertyUri": "http://nakala.fr/terms#subject",
      "value": "medieval",
      "lang": "en",
      "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    },
    {
      "propertyUri": "http://nakala.fr/terms#subject",
      "value": "research",
      "lang": "en",
      "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    },
    {
      "propertyUri": "http://nakala.fr/terms#creator",
      "value": "Smith, John",
      "lang": "en",
      "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    }
  ],
  "status": "pending",
  "rightsOfDatasets": [...],
  "files": [...]
}
```

## 🏗️ Multi-Layer Transformation Pipeline

### Layer 1: Field Name Mapping
**Location**: `src/nakala_client/common/utils.py:38-55`
**Function**: Static property URI mapping

```python
PROPERTY_URIS = {
    "type": "http://nakala.fr/terms#type",
    "title": "http://nakala.fr/terms#title",
    "creator": "http://nakala.fr/terms#creator",
    "description": "http://purl.org/dc/terms/description",
    "alternative": "http://purl.org/dc/terms/alternative",
    "contributor": "http://purl.org/dc/terms/contributor",
    "publisher": "http://purl.org/dc/terms/publisher",
    "date": "http://purl.org/dc/terms/date",
    "license": "http://purl.org/dc/terms/license",
    "keywords": "http://nakala.fr/terms#subject",
    "language": "http://purl.org/dc/terms/language",
    "temporal": "http://purl.org/dc/terms/temporal",
    "spatial": "http://purl.org/dc/terms/spatial",
    "accessRights": "http://purl.org/dc/terms/accessRights",
    "identifier": "http://purl.org/dc/terms/identifier",
    "rights": "http://purl.org/dc/terms/rights",
    "relation": "http://purl.org/dc/terms/relation",
    "source": "http://purl.org/dc/terms/source",
    "coverage": "http://purl.org/dc/terms/coverage"
}
```

### Layer 2: Multilingual Format Processing
**Location**: `src/nakala_client/common/utils.py:87-113`
**Function**: `parse_multilingual_field()`

**Input Formats Supported:**
```python
# Simple text
"Basic research data"

# Multilingual format
"fr:Données de recherche|en:Research Data"

# Multiple languages
"fr:Données|en:Data|es:Datos|de:Daten"
```

**Processing Logic:**
```python
@staticmethod
def parse_multilingual_field(value: str) -> List[Tuple[Optional[str], str]]:
    """
    Parse multilingual field values.
    Returns list of (language_code, text) tuples.
    """
    if not value or pd.isna(value):
        return []
    
    value = str(value).strip()
    if not value:
        return []
    
    # Check if it's multilingual format (contains |)
    if '|' in value:
        entries = []
        for entry in value.split('|'):
            entry = entry.strip()
            if ':' in entry:
                lang, text = entry.split(':', 1)
                entries.append((lang.strip(), text.strip()))
            else:
                entries.append((None, entry))
        return entries
    else:
        return [(None, value)]
```

### Layer 3: Advanced Multilingual and Array Processing
**Location**: `src/nakala_client/curator.py:1788-1859`
**Function**: `_process_multilingual_value()`

**Complex Format Support:**
```python
# Keywords with multilingual and semicolon separation
"fr:manuscrits;médiéval;recherche|en:manuscripts;medieval;research"

# Contributors with institutional affiliations
"fr:Université Paris 1|en:University Paris 1"

# Multiple creators
"Smith, John;Doe, Jane;Martin, Pierre"
```

**Advanced Processing Logic:**
```python
def _process_multilingual_value(self, field_name: str, value: str) -> List[Dict[str, Any]]:
    """
    Process multilingual values with support for arrays and complex formats.
    Handles keywords, creators, contributors with proper separation.
    """
    property_uri = self.field_mappings.get(field_name, {}).get('property_uri')
    if not property_uri:
        return []
    
    # Parse multilingual entries
    lang_entries = self._parse_multilingual_entries(value)
    metadata_entries = []
    
    for lang, text in lang_entries:
        # Handle array fields (keywords, creators, etc.)
        if field_name in ['new_keywords', 'keywords']:
            # Split on multiple separators: ; , | newline
            items = self._parse_keywords(text)
            for item in items:
                metadata_entries.append({
                    "propertyUri": property_uri,
                    "value": item.strip(),
                    "lang": lang,
                    "typeUri": "http://www.w3.org/2001/XMLSchema#string"
                })
        else:
            metadata_entries.append({
                "propertyUri": property_uri,
                "value": text.strip(),
                "lang": lang,
                "typeUri": "http://www.w3.org/2001/XMLSchema#string"
            })
    
    return metadata_entries
```

### Layer 4: CSV Field Mapping Configuration
**Location**: `src/nakala_client/curator.py:34-120`
**Purpose**: Comprehensive field mapping with validation rules

```python
CSV_FIELD_MAPPINGS = {
    'new_title': {
        'api_field': 'title',
        'property_uri': 'http://nakala.fr/terms#title',
        'multilingual': True,
        'required': True,
        'description': 'Title of the resource (multilingual supported)'
    },
    'new_description': {
        'api_field': 'description',
        'property_uri': 'http://purl.org/dc/terms/description',
        'multilingual': True,
        'required': False,
        'description': 'Description of the resource'
    },
    'new_keywords': {
        'api_field': 'keywords',
        'property_uri': 'http://nakala.fr/terms#subject',
        'multilingual': True,
        'array': True,
        'separators': [';', ',', '|', '\n'],
        'description': 'Keywords/subjects (semicolon-separated, multilingual)'
    },
    'new_creator': {
        'api_field': 'creator',
        'property_uri': 'http://nakala.fr/terms#creator',
        'multilingual': False,
        'array': True,
        'separators': [';', ','],
        'description': 'Creators/authors (semicolon-separated)'
    },
    'new_contributor': {
        'api_field': 'contributor',
        'property_uri': 'http://purl.org/dc/terms/contributor',
        'multilingual': True,
        'array': True,
        'separators': [';', ','],
        'description': 'Contributors (institutions, collaborators)'
    },
    'new_type': {
        'api_field': 'type',
        'property_uri': 'http://nakala.fr/terms#type',
        'vocabulary': 'coar_resource_types',
        'validation': 'uri',
        'description': 'COAR resource type URI'
    },
    'new_license': {
        'api_field': 'license',
        'property_uri': 'http://purl.org/dc/terms/license',
        'vocabulary': 'licenses',
        'validation': 'controlled',
        'description': 'License identifier (CC-BY, CC-BY-SA, etc.)'
    },
    'new_language': {
        'api_field': 'language',
        'property_uri': 'http://purl.org/dc/terms/language',
        'vocabulary': 'iso_languages',
        'validation': 'iso_code',
        'description': 'Language codes (ISO 639-1)'
    },
    'new_rights': {
        'api_field': 'rights',
        'property_uri': 'http://purl.org/dc/terms/rights',
        'complex_format': True,
        'description': 'Access rights and permissions'
    },
    'new_relation': {
        'api_field': 'relation',
        'property_uri': 'http://purl.org/dc/terms/relation',
        'multilingual': True,
        'description': 'Related resources or relationships'
    },
    'new_source': {
        'api_field': 'source',
        'property_uri': 'http://purl.org/dc/terms/source',
        'multilingual': True,
        'description': 'Source information'
    },
    'new_coverage': {
        'api_field': 'coverage',
        'property_uri': 'http://purl.org/dc/terms/coverage',
        'multilingual': True,
        'description': 'Spatial or temporal coverage'
    }
}
```

### Layer 5: CSV Parsing and Row Processing
**Location**: `src/nakala_client/curator.py:1374-1432`
**Functions**: CSV parsing with mode detection

```python
def parse_csv_modifications(self, csv_file_path: str) -> List[Dict[str, Any]]:
    """
    Parse CSV file and detect operation mode (creation vs modification).
    Returns list of parsed modifications/creations.
    """
    modifications = []
    
    try:
        df = pd.read_csv(csv_file_path)
        logger.info(f"Loaded CSV with {len(df)} rows and columns: {list(df.columns)}")
        
        # Auto-detect CSV mode
        if 'id' in df.columns and 'action' in df.columns:
            csv_mode = 'modify'
            logger.info("Auto-detected CSV mode: modify")
        else:
            csv_mode = 'create'
            logger.info("Auto-detected CSV mode: create")
        
        for index, row in df.iterrows():
            if csv_mode == 'modify':
                parsed_row = self._parse_modification_row(row)
            else:
                parsed_row = self._parse_creation_row(row)
            
            if parsed_row:
                modifications.append(parsed_row)
        
        logger.info(f"Parsed {len(modifications)} modifications from CSV")
        return modifications
        
    except Exception as e:
        logger.error(f"Failed to parse CSV file {csv_file_path}: {e}")
        raise
```

### Layer 6: Final JSON Payload Creation
**Location**: `src/nakala_client/curator.py:1640-1786`
**Function**: `_apply_modification()`

**Final Transformation Logic:**
```python
def _apply_modification(self, item_data: Dict, modifications: Dict) -> Dict:
    """
    Apply modifications to create final NAKALA API JSON payload.
    Handles complex metadata structure creation.
    """
    try:
        # Start with existing metadata or create new structure
        if 'metas' in item_data:
            current_metas = item_data['metas']
        else:
            current_metas = []
        
        # Process each modification field
        for field_name, new_value in modifications.items():
            if field_name.startswith('new_'):
                # Remove existing metadata for this field
                property_uri = self.field_mappings.get(field_name, {}).get('property_uri')
                if property_uri:
                    current_metas = [m for m in current_metas if m.get('propertyUri') != property_uri]
                
                # Add new metadata entries
                new_entries = self._process_multilingual_value(field_name, new_value)
                current_metas.extend(new_entries)
        
        # Create final payload
        payload = {
            'metas': current_metas,
            'status': item_data.get('status', 'pending')
        }
        
        # Add additional fields if present
        if 'rightsOfDatasets' in item_data:
            payload['rightsOfDatasets'] = item_data['rightsOfDatasets']
        
        return payload
        
    except Exception as e:
        logger.error(f"Failed to apply modification: {e}")
        raise
```

## 🔧 Code Locations Reference

### Core Transformation Functions
| Function | Location | Purpose |
|----------|----------|---------|
| `prepare_nakala_metadata()` | `common/utils.py:116-227` | Main transformation entry point |
| `parse_multilingual_field()` | `common/utils.py:87-113` | Basic multilingual parsing |
| `_process_multilingual_value()` | `curator.py:1788-1859` | Advanced multilingual processing |
| `parse_csv_modifications()` | `curator.py:1374-1432` | CSV parsing with mode detection |
| `_apply_modification()` | `curator.py:1640-1786` | Final JSON payload creation |

### Configuration and Mapping
| Component | Location | Purpose |
|-----------|----------|---------|
| `PROPERTY_URIS` | `common/utils.py:38-55` | Field → URI mapping |
| `CSV_FIELD_MAPPINGS` | `curator.py:34-120` | Complete field configuration |
| Field validation rules | `curator.py:121-150` | Validation logic per field |

### Processing Functions
| Function | Location | Purpose |
|----------|----------|---------|
| `_parse_keywords()` | `curator.py:1861-1877` | Keyword array processing |
| `_parse_modification_row()` | `curator.py:1443-1460` | Modification CSV format |
| `_parse_creation_row()` | `curator.py:1462-1483` | Creation CSV format |
| `_process_csv_entry()` | `upload.py:378-434` | Upload CSV processing |

## 🚨 Complexity Pain Points

### 1. Multiple CSV Modes
- **Creation mode**: Direct field names (`title`, `creator`)
- **Modification mode**: Prefixed fields (`new_title`, `new_creator`)
- **Upload mode**: Different structure entirely

### 2. Multilingual Format Variations
```python
# Simple
"Research Data"

# Basic multilingual
"fr:Données|en:Data"

# Complex with arrays
"fr:mot1;mot2|en:word1;word2"

# Institutional multilingual
"fr:Université Paris 1|en:University Paris 1"
```

### 3. Array Field Processing
Different separators for different contexts:
- **Keywords**: `;`, `,`, `|`, newline
- **Creators**: `;`, `,`
- **Contributors**: `;`, `,`

### 4. Field Validation Complexity
- **URI validation** for resource types
- **ISO code validation** for languages
- **Controlled vocabulary** for licenses
- **Complex rights format** validation

### 5. Error Propagation
Errors can occur at multiple levels:
- CSV parsing errors
- Field mapping errors
- Multilingual format errors
- API validation errors
- JSON structure errors

## 🎯 Next Steps: Endpoint-by-Endpoint Analysis

This technical analysis provides the foundation for systematic improvement:

1. **Upload Endpoint** - Analyze `upload.py` transformation
2. **Collection Endpoint** - Analyze `collection.py` transformation
3. **Curator Endpoint** - Analyze `curator.py` batch transformation
4. **Field-by-Field** - Document each metadata field's transformation rules
5. **Error Handling** - Improve error messages and validation
6. **User Tools** - Create validation and preview utilities

## 📚 Related Documentation

- [Field Reference](curator-field-reference.md) - Complete field documentation
- [Property URI Mapping](property-uri-mapping.md) - Field mapping reference
- [NAKALA API Specifications](../api/guide_description.md) - Official API documentation

---

**Status**: Technical analysis complete  
**Next Phase**: Endpoint-by-endpoint documentation and improvement  
**Goal**: Make CSV transformation transparent and user-friendly