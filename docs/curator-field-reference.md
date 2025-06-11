# Curator Field Reference Guide

Complete reference for all fields supported by the o-nakala-core curator module for both data items and collections.

## Overview

The curator module provides **foundational metadata management** for core Dublin Core fields (~40% of full NAKALA API capabilities). This reference covers currently supported fields, with a roadmap toward [Complete Metadata Management](COMPLETE_METADATA_SYSTEM_DESIGN.md).

**Current Scope**: Basic metadata modification via CSV batch operations  
**Future Vision**: Dynamic template generation, intelligent pre-population, and comprehensive field support

See [Complete Metadata System Design](COMPLETE_METADATA_SYSTEM_DESIGN.md) for full roadmap.

## Data Item Fields

### Core Metadata Fields

| CSV Column | Property URI | Multilingual | Required | Format | Example |
|------------|-------------|--------------|----------|---------|---------|
| **title** | `http://nakala.fr/terms#title` | ✅ Yes | ✅ Required | `"fr:French\|en:English"` | `"fr:Données climatiques\|en:Climate data"` |
| **description** | `http://purl.org/dc/terms/description` | ✅ Yes | ✅ Required | Same as title | `"fr:Description française\|en:English description"` |
| **keywords** | `http://purl.org/dc/terms/subject` | ✅ Yes | Optional | `"fr:mot1;mot2\|en:word1;word2"` | `"fr:climat;météo\|en:climate;weather"` |
| **alternative** | Alternative titles | ✅ Yes | Optional | Same as title | `"fr:Titre alternatif\|en:Alternative title"` |

### People and Contributors

| CSV Column | Property URI | Multilingual | Required | Format | Example |
|------------|-------------|--------------|----------|---------|---------|
| **author** | `http://purl.org/dc/terms/creator` | ❌ No | ✅ Required | `"Surname,Givenname"` | `"Dupont,Jean"` |
| **creator** | `http://purl.org/dc/terms/creator` | ❌ No | Optional | `"Surname,Givenname"` | `"Smith,John;Doe,Jane"` |
| **contributor** | `http://purl.org/dc/terms/contributor` | ❌ No | Optional | `"Surname,Givenname"` | `"Smith,John;Martin,Alice"` |
| **publisher** | `http://purl.org/dc/terms/publisher` | ❌ No | Optional | Organization name | `"CNRS"` |

### Technical Metadata

| CSV Column | Property URI | Multilingual | Required | Format | Example |
|------------|-------------|--------------|----------|---------|---------|
| **type** | `http://nakala.fr/terms#type` | ❌ No | ✅ Required | COAR Resource Type URI | `"http://purl.org/coar/resource_type/c_ddb1"` |
| **license** | `http://nakala.fr/terms#license` | ❌ No | ✅ Required | License identifier | `"CC-BY-4.0"` |
| **date** | `http://nakala.fr/terms#created` | ❌ No | ✅ Required | W3C-DTF format | `"2024-01-15"` or `"2024-01"` or `"2024"` |
| **language** | `http://purl.org/dc/terms/language` | ❌ No | Optional | ISO language code | `"fr"` or `"en"` |

### Coverage and Relations

| CSV Column | Property URI | Multilingual | Required | Format | Example |
|------------|-------------|--------------|----------|---------|---------|
| **temporal** | `http://purl.org/dc/terms/coverage` | ❌ No | Optional | Date range or period | `"2020/2023"` or `"Medieval period"` |
| **spatial** | `http://purl.org/dc/terms/coverage` | ❌ No | Optional | Geographic location | `"France"` or `"45.7640,4.8357"` |
| **relation** | `http://purl.org/dc/terms/relation` | ❌ No | Optional | URI or text | `"https://example.com/related"` |
| **source** | `http://purl.org/dc/terms/source` | ❌ No | Optional | Source reference | `"Original dataset from..."` |
| **identifier** | `http://purl.org/dc/terms/identifier` | ❌ No | Optional | External identifier | `"DOI:10.1234/example"` |

### Access and Rights

| CSV Column | Property URI | Multilingual | Required | Format | Example |
|------------|-------------|--------------|----------|---------|---------|
| **accessRights** | Access rights info | ❌ No | Optional | Access description | `"Open access"` |
| **rights** | Rights/permissions | ❌ No | Optional | `"group_id,role"` | `"group123,ROLE_EDITOR"` |

## Collection Fields

Collections support a subset of data item fields plus collection-specific metadata:

### Collection-Specific Fields

| CSV Column | Property URI | Multilingual | Required | Format | Example |
|------------|-------------|--------------|----------|---------|---------|
| **title** | `http://nakala.fr/terms#title` | ✅ Yes | ✅ Required | `"fr:French\|en:English"` | `"fr:Collection de données\|en:Data collection"` |
| **status** | Collection status | ❌ No | ✅ Required | `private\|public` | `"public"` |
| **data_items** | Referenced data items | ❌ No | Optional | Data item IDs | `"folder_pattern_*"` |

### Supported Dublin Core Fields for Collections

Collections also support these fields from the data item list:
- description, keywords, language
- **creator** (✅ FULLY SUPPORTED), author, contributor, publisher
- date, temporal, spatial
- relation, source, rights, coverage

**Note**: Both `new_creator` and `new_author` fields are now fully supported for collections via batch modifications using the format `"Creator1,Name;Creator2,Name"`.

## Multilingual Format Specification

### Format Rules:
```
"language_code:content|language_code:content"
```

### Supported Languages:
- **fr**: French
- **en**: English  
- **es**: Spanish
- **de**: German
- (Any ISO 639-1 language code)

### Examples:
```csv
# Single language
title,"Simple English Title"

# Multiple languages
title,"fr:Titre français|en:English Title"

# Keywords with multilingual support
keywords,"fr:mot-clé1;mot-clé2|en:keyword1;keyword2"

# Description with multiple languages
description,"fr:Une description détaillée en français|en:A detailed description in English"
```

## Batch Modification CSV Format

For batch modifications, use this CSV structure:

```csv
id,action,current_title,new_title,current_description,new_description,new_creator
10.34847/nkl.abc123,modify,"Old Title","fr:Nouveau titre|en:New Title","Old description","fr:Nouvelle description|en:New description","Smith,John;Doe,Jane"
```

### Batch Modification Fields:

| Field | Description | Required | Format |
|-------|-------------|----------|---------|
| **id** | NAKALA identifier | ✅ Required | `"10.34847/nkl.identifier"` |
| **action** | Modification action | ✅ Required | `update\|validate\|enhance` |
| **current_[field]** | Current value (verification) | Optional | Same as field format |
| **new_[field]** | New value to set | Optional | Same as field format |

## Field Validation Rules

### Required Field Validation:
- **Data Items**: title, author (creator), type, license, date
- **Collections**: title, status (creator recommended but optional)

### Format Validation:
- **Dates**: Must follow W3C-DTF (YYYY-MM-DD, YYYY-MM, or YYYY)
- **Languages**: Must be valid ISO 639-1 codes
- **Licenses**: Must be from controlled vocabulary
- **Type**: Must be valid COAR Resource Type URI

### Content Validation:
- **Title**: Minimum 3 characters, maximum 250 characters
- **Description**: Minimum 10 characters recommended
- **Keywords**: Maximum 10 keywords per language recommended
- **Authors**: Must follow "Surname,Givenname" format

## Usage Examples

### Single Item Update:
```bash
o-nakala-curator update-item 10.34847/nkl.abc123 \
  --title "fr:Nouveau titre|en:New Title" \
  --description "fr:Nouvelle description|en:New description"
```

### Batch Update from CSV:
```bash
# General batch modifications
o-nakala-curator --batch-modify modifications.csv \
  --api-key YOUR_KEY \
  --dry-run

# Add creators to collections
o-nakala-curator --batch-modify collection_creators.csv \
  --scope collections \
  --api-key YOUR_KEY
```

### Validation Only:
```bash
o-nakala-curator validate-metadata data_items.csv \
  --api-key YOUR_KEY \
  --output-report validation_report.json
```

## Error Handling

### Common Validation Errors:
- **Missing required fields**: Ensure title, creator, type, license, date are present
- **Invalid multilingual format**: Check language codes and separator format
- **Invalid dates**: Use W3C-DTF format (YYYY-MM-DD)
- **Invalid license**: Use valid license identifier from vocabulary
- **Invalid type**: Use valid COAR Resource Type URI

### Troubleshooting:
1. **Use dry-run mode** to test modifications before applying
2. **Check field format** against examples in this reference
3. **Validate CSV structure** before batch operations
4. **Review error logs** for specific field validation failures

## Best Practices

1. **Always backup** data before bulk modifications
2. **Use dry-run mode** for testing modifications
3. **Validate CSV format** before batch operations
4. **Follow multilingual conventions** for international datasets
5. **Use controlled vocabularies** for type, license, and language fields
6. **Include current values** in batch modifications for verification
7. **Test with small batches** before large-scale operations

## Related Documentation

- [Upload Guide](01-upload-guide.md) - For initial data upload
- [Collection Guide](02-collection-guide.md) - For collection management
- [Workflow Guide](03-workflow-guide.md) - For complete workflows
- [Troubleshooting](troubleshooting.md) - For error resolution