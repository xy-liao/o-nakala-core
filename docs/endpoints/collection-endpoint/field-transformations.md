# Collection Field Transformations

## 🎯 Overview

This document provides **field-by-field transformation logic** for Collection endpoint CSV processing. Each CSV field is mapped to specific **NAKALA property URIs** with detailed transformation rules and JSON output examples.

## 🏗️ Transformation Architecture

### **Processing Pipeline**
```python
# Step 1: CSV Row Input
csv_row = {
    "title": "fr:Collection|en:Collection",
    "description": "fr:Description|en:Description", 
    "keywords": "fr:mot-clé;recherche|en:keyword;research",
    "creator": "Smith, John;Doe, Jane",
    "status": "published",
    "data_items": "files/code/|files/data/"
}

# Step 2: Field Transformation
metadata_dict = extract_metadata_fields(csv_row)
metas = NakalaCommonUtils.prepare_nakala_metadata(metadata_dict)

# Step 3: JSON Output
{
    "status": "published",
    "metas": [...],  # Transformed metadata array
    "datas": [...],  # Resolved data IDs
    "rights": []     # Access rights
}
```

### **Code Location**: `src/o_nakala_core/collection.py:129-139`
```python
def prepare_collection_metadata(self, collection_config: CollectionConfig) -> List[Dict[str, Any]]:
    metadata_dict = {
        "title": collection_config.title,
        "description": collection_config.description, 
        "keywords": collection_config.keywords,
    }
    return self.utils.prepare_nakala_metadata(metadata_dict)
```

## 📋 Field-by-Field Transformations

### **1. Title Field**

#### **CSV Input**
```csv
title
"Research Collection"
"fr:Collection de recherche|en:Research Collection"
```

#### **Transformation Logic**
- **Property URI**: `http://nakala.fr/terms#title`
- **Processing**: `NakalaCommonUtils.parse_multilingual_field()`
- **Language handling**: Creates separate entries per language

#### **JSON Output**
```json
// Single language
{
    "value": "Research Collection",
    "lang": "und",
    "typeUri": "http://www.w3.org/2001/XMLSchema#string",
    "propertyUri": "http://nakala.fr/terms#title"
}

// Multilingual
[
    {
        "value": "Collection de recherche", 
        "lang": "fr",
        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
        "propertyUri": "http://nakala.fr/terms#title"
    },
    {
        "value": "Research Collection",
        "lang": "en", 
        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
        "propertyUri": "http://nakala.fr/terms#title"
    }
]
```

### **2. Description Field**

#### **CSV Input**
```csv
description
"Collection of research data and analysis scripts"
"fr:Collection de données|en:Data collection"
```

#### **Transformation Logic**
- **Property URI**: `http://purl.org/dc/terms/description`
- **Processing**: Same multilingual parsing as title
- **Default**: Empty description allowed

#### **JSON Output**
```json
{
    "value": "Collection of research data and analysis scripts",
    "lang": "und",
    "typeUri": "http://www.w3.org/2001/XMLSchema#string", 
    "propertyUri": "http://purl.org/dc/terms/description"
}
```

### **3. Keywords Field**

#### **CSV Input**
```csv
keywords
"research;data;analysis"
"fr:recherche;données|en:research;data"
```

#### **Transformation Logic**
- **Property URI**: `http://purl.org/dc/terms/subject`
- **Processing**: Split by semicolon, then by language
- **Each keyword**: Separate metadata entry

#### **Code Reference**: `src/o_nakala_core/common/utils.py:172-184`
```python
if field_name == "keywords":
    for keyword in value.split(";"):
        keyword = keyword.strip()
        if keyword:
            metas.append({
                "value": keyword,
                "lang": lang if lang else "und",
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": property_uri,
            })
```

#### **JSON Output**
```json
[
    {
        "value": "research",
        "lang": "und",
        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
        "propertyUri": "http://purl.org/dc/terms/subject"
    },
    {
        "value": "data", 
        "lang": "und",
        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
        "propertyUri": "http://purl.org/dc/terms/subject"
    },
    {
        "value": "analysis",
        "lang": "und", 
        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
        "propertyUri": "http://purl.org/dc/terms/subject"
    }
]
```

### **4. Creator Field**

#### **CSV Input**
```csv
creator
"Smith, John"
"Smith, John;Doe, Jane;Wilson, Sarah"
```

#### **Transformation Logic**
- **Property URI**: `http://nakala.fr/terms#creator`
- **Processing**: Parse person format, create array
- **Format**: "Surname, Givenname" preferred

#### **Code Reference**: `src/o_nakala_core/common/utils.py:185-201`
```python
elif field_name in ["creator", "contributor"]:
    for person in value.split(";"):
        person = person.strip()
        if person and "," in person:
            surname, givenname = person.split(",", 1)
            person_data = {
                "givenname": givenname.strip(),
                "surname": surname.strip(),
            }
            creator_arrays[property_uri].append(person_data)
        elif person:
            creator_arrays[property_uri].append({"name": person})
```

#### **JSON Output**
```json
{
    "value": [
        {
            "givenname": "John",
            "surname": "Smith"
        },
        {
            "givenname": "Jane", 
            "surname": "Doe"
        },
        {
            "givenname": "Sarah",
            "surname": "Wilson"
        }
    ],
    "propertyUri": "http://nakala.fr/terms#creator"
}
```

### **5. Contributor Field**

#### **CSV Input**
```csv
contributor
"University Research Lab"
"fr:CNRS;Université|en:CNRS;University"
```

#### **Transformation Logic**
- **Property URI**: `http://purl.org/dc/terms/contributor`
- **Processing**: Same as creator but supports institutional names
- **Multilingual**: Supports institutional name translations

#### **JSON Output**
```json
// Institutional contributors
{
    "value": [
        {"name": "University Research Lab"}
    ],
    "propertyUri": "http://purl.org/dc/terms/contributor"
}

// Multilingual institutional
[
    {
        "value": [{"name": "CNRS"}, {"name": "Université"}],
        "lang": "fr",
        "propertyUri": "http://purl.org/dc/terms/contributor"
    },
    {
        "value": [{"name": "CNRS"}, {"name": "University"}], 
        "lang": "en",
        "propertyUri": "http://purl.org/dc/terms/contributor"
    }
]
```

### **6. Status Field**

#### **CSV Input**
```csv
status
published
pending
private
```

#### **Transformation Logic**
- **Direct mapping**: No property URI transformation
- **Collection payload**: Top-level status field
- **Validation**: Must be valid status value

#### **JSON Output**
```json
{
    "status": "published",  // Top-level field, not in metas array
    "metas": [...],
    "datas": [...]
}
```

### **7. Data Items Field**

#### **CSV Input**  
```csv
data_items
"files/code/"
"files/data/|files/results/|analysis/"
```

#### **Transformation Logic**
- **No property URI**: Used for dataset matching logic
- **Processing**: Pattern matching against uploaded dataset titles
- **Resolution**: Converts to actual dataset IDs

#### **Code Reference**: `src/o_nakala_core/collection.py:220-271`
```python
def create_collections_from_folder_config(self, folder_config_path, upload_output_path):
    # Match patterns against uploaded data titles
    data_ids = []
    for pattern in data_items.split("|"):
        pattern = pattern.strip()
        matching_items = [
            item for item in uploaded_data 
            if self.utils.matches_folder_type(item["title"], [pattern])
        ]
        data_ids.extend([item["id"] for item in matching_items])
```

#### **JSON Output**
```json
{
    "datas": [
        "10.34847/nkl.abc12345",  // Resolved from "files/code/" pattern
        "10.34847/nkl.def67890",  // Resolved from "files/data/" pattern
        "10.34847/nkl.ghi09876"   // Resolved from "files/results/" pattern
    ]
}
```

### **8. Extended Dublin Core Fields**

#### **Publisher**
```csv
publisher
"Research Institute"
```
**Property URI**: `http://purl.org/dc/terms/publisher`  
**JSON**: Standard string metadata entry

#### **Coverage**
```csv
coverage
"2020-2023"
"fr:France|en:France"
```
**Property URI**: `http://purl.org/dc/terms/coverage`  
**JSON**: String metadata with optional language

#### **Language**
```csv
language
fr
en
```
**Property URI**: `http://purl.org/dc/terms/language`  
**JSON**: Language code string

#### **Date**
```csv
date
2023-06-09
```
**Property URI**: `http://nakala.fr/terms#created`  
**JSON**: Date string (no language attribute)

#### **Relation**
```csv
relation
"https://doi.org/10.1234/related"
```
**Property URI**: `http://purl.org/dc/terms/relation`  
**JSON**: String metadata entry

#### **Source**
```csv
source
"Derived from National Survey"
```
**Property URI**: `http://purl.org/dc/terms/source`  
**JSON**: String metadata entry

#### **Rights**
```csv
rights
"group_id,ROLE_READER"
```
**Processing**: Converted to rights array in collection payload
**JSON**: 
```json
{
    "rights": [
        {
            "id": "group_id",
            "role": "ROLE_READER"
        }
    ]
}
```

## 🔄 Complete Transformation Example

### **Input CSV Row**
```csv
title,status,description,keywords,creator,contributor,data_items
"fr:Collection de recherche|en:Research Collection",published,"fr:Description|en:Description","fr:recherche;analyse|en:research;analysis","Smith, John;Doe, Jane","fr:CNRS|en:CNRS","files/code/|files/data/"
```

### **Transformed JSON Payload**
```json
{
    "status": "published",
    "metas": [
        {
            "value": "Collection de recherche",
            "lang": "fr", 
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://nakala.fr/terms#title"
        },
        {
            "value": "Research Collection",
            "lang": "en",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string", 
            "propertyUri": "http://nakala.fr/terms#title"
        },
        {
            "value": "Description",
            "lang": "fr",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://purl.org/dc/terms/description"
        },
        {
            "value": "Description", 
            "lang": "en",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://purl.org/dc/terms/description"
        },
        {
            "value": "recherche",
            "lang": "fr",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://purl.org/dc/terms/subject"
        },
        {
            "value": "analyse",
            "lang": "fr", 
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://purl.org/dc/terms/subject"
        },
        {
            "value": "research",
            "lang": "en",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://purl.org/dc/terms/subject"
        },
        {
            "value": "analysis",
            "lang": "en",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string", 
            "propertyUri": "http://purl.org/dc/terms/subject"
        },
        {
            "value": [
                {"givenname": "John", "surname": "Smith"},
                {"givenname": "Jane", "surname": "Doe"}
            ],
            "propertyUri": "http://nakala.fr/terms#creator"
        },
        {
            "value": [{"name": "CNRS"}],
            "lang": "fr",
            "propertyUri": "http://purl.org/dc/terms/contributor"
        },
        {
            "value": [{"name": "CNRS"}],
            "lang": "en", 
            "propertyUri": "http://purl.org/dc/terms/contributor"
        }
    ],
    "datas": [
        "10.34847/nkl.abc12345",  // Matched from "files/code/" pattern
        "10.34847/nkl.def67890"   // Matched from "files/data/" pattern
    ],
    "rights": []
}
```

## 🎯 Key Transformation Rules

### **Multilingual Processing**
1. **Parse**: Split by `|` for languages, `:` for lang/text separation
2. **Create**: Separate metadata entries per language
3. **Default**: Use `"und"` if no language code specified

### **Array Fields (Creator/Contributor)**
1. **Parse**: Split by `;` for multiple persons/institutions
2. **Format**: Detect "Surname, Givenname" vs simple names
3. **Combine**: Single metadata entry with value array

### **Keyword Processing**
1. **Split**: By `;` within each language
2. **Individual**: Each keyword gets separate metadata entry
3. **Language**: Inherited from multilingual parsing

### **Pattern Matching**
1. **Parse**: Split `data_items` by `|` 
2. **Match**: Against uploaded dataset titles
3. **Resolve**: Convert matches to dataset IDs

## 🔗 Related Documentation

- **[CSV Format Specification](./csv-format-specification.md)** - Complete field format rules
- **[Examples](../../../examples/sample_dataset/)** - Working transformation examples
- **[Common Utils Code](../../src/o_nakala_core/common/utils.py)** - Actual transformation functions

---

**Transformation Version**: 1.0  
**Code Compatibility**: NAKALA Client v2.0  
**Last Updated**: 2025-08-30