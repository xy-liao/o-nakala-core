# Property URI Mapping Reference

Complete mapping between CSV field names, NAKALA property URIs, and Dublin Core terms used in the o-nakala-core library.

## Overview

The o-nakala-core library maps human-readable CSV field names to standardized property URIs from NAKALA and Dublin Core vocabularies. This mapping ensures consistent metadata representation while maintaining user-friendly interfaces.

## Core Property URI Mappings

### NAKALA-Specific Properties

| CSV Field | Property URI | Vocabulary | Type | Description |
|-----------|-------------|------------|------|-------------|
| **title** | `http://nakala.fr/terms#title` | NAKALA | string | Resource title (multilingual) |
| **author** / **creator** | `http://nakala.fr/terms#creator` | NAKALA | object/array | Resource creators |
| **type** | `http://nakala.fr/terms#type` | NAKALA | anyURI | Resource type (COAR vocabulary) |
| **license** | `http://nakala.fr/terms#license` | NAKALA | string | License identifier |
| **date** / **created** | `http://nakala.fr/terms#created` | NAKALA | date | Creation date |

### Dublin Core Qualified Properties

| CSV Field | Property URI | Vocabulary | Type | Description |
|-----------|-------------|------------|------|-------------|
| **description** | `http://purl.org/dc/terms/description` | DC Terms | string | Resource description (multilingual) |
| **keywords** / **subject** | `http://purl.org/dc/terms/subject` | DC Terms | string | Subject keywords (multilingual) |
| **contributor** | `http://purl.org/dc/terms/contributor` | DC Terms | string | Contributors |
| **publisher** | `http://purl.org/dc/terms/publisher` | DC Terms | string | Publisher information |
| **language** | `http://purl.org/dc/terms/language` | DC Terms | string | Content language |
| **temporal** | `http://purl.org/dc/terms/temporal` | DC Terms | string | Temporal coverage |
| **spatial** | `http://purl.org/dc/terms/spatial` | DC Terms | string | Spatial coverage |
| **coverage** | `http://purl.org/dc/terms/coverage` | DC Terms | string | General coverage |
| **relation** | `http://purl.org/dc/terms/relation` | DC Terms | string/anyURI | Related resources |
| **source** | `http://purl.org/dc/terms/source` | DC Terms | string | Source information |
| **rights** | `http://purl.org/dc/terms/rights` | DC Terms | string | Rights statement |
| **format** | `http://purl.org/dc/terms/format` | DC Terms | string | File format |
| **identifier** | `http://purl.org/dc/terms/identifier` | DC Terms | string | External identifiers |

## Field Type Specifications

### String Types
**TypeUri**: `http://www.w3.org/2001/XMLSchema#string`

Used for text-based metadata fields:
- title, description, keywords
- contributor, publisher, source
- rights, coverage (when textual)

### URI Types
**TypeUri**: `http://www.w3.org/2001/XMLSchema#anyURI`

Used for reference fields:
- type (COAR Resource Type URI)
- relation (when linking to external resources)
- identifier (when using URI-based identifiers)

### Date Types
**TypeUri**: `http://www.w3.org/2001/XMLSchema#date`

Used for temporal fields:
- created, date (W3C-DTF format)

### Object Types
**TypeUri**: Custom object structure

Used for complex fields:
- creator/author (person object with givenname, surname, orcid)

## Multilingual Metadata Structure

For multilingual fields, the library generates multiple metadata entries:

```json
[
  {
    "propertyUri": "http://nakala.fr/terms#title",
    "value": "Titre français",
    "lang": "fr",
    "typeUri": "http://www.w3.org/2001/XMLSchema#string"
  },
  {
    "propertyUri": "http://nakala.fr/terms#title", 
    "value": "English Title",
    "lang": "en",
    "typeUri": "http://www.w3.org/2001/XMLSchema#string"
  }
]
```

## Creator/Author Object Structure

The creator field uses a special object format:

```json
{
  "propertyUri": "http://nakala.fr/terms#creator",
  "value": [
    {
      "givenname": "Jean",
      "surname": "Dupont",
      "orcid": "0000-0000-0000-0000"
    }
  ]
}
```

## Collection-Specific Mappings

Collections use the same property URIs but with different requirements:

| Field | Property URI | Required for Collections | Notes |
|-------|-------------|-------------------------|--------|
| **title** | `http://nakala.fr/terms#title` | ✅ Required | Collection title |
| **status** | Collection status | ✅ Required | "private" or "public" |
| **description** | `http://purl.org/dc/terms/description` | Optional | Collection description |
| **data_items** | Referenced items | Optional | Data item relationships |

## Vocabulary Constants in Code

The library defines these mappings in `src/nakala_client/common/utils.py`:

```python
PROPERTY_URIS = {
    'type': 'http://nakala.fr/terms#type',
    'title': 'http://nakala.fr/terms#title',
    'creator': 'http://nakala.fr/terms#creator',
    'created': 'http://nakala.fr/terms#created',
    'license': 'http://nakala.fr/terms#license',
    'description': 'http://purl.org/dc/terms/description',
    'subject': 'http://purl.org/dc/terms/subject',
    'contributor': 'http://purl.org/dc/terms/contributor',
    'publisher': 'http://purl.org/dc/terms/publisher',
    'rights': 'http://purl.org/dc/terms/rights',
    'coverage': 'http://purl.org/dc/terms/coverage',
    'relation': 'http://purl.org/dc/terms/relation',
    'source': 'http://purl.org/dc/terms/source',
    'language': 'http://purl.org/dc/terms/language',
    'format': 'http://purl.org/dc/terms/format',
    'identifier': 'http://purl.org/dc/terms/identifier'
}
```

## Controlled Vocabularies

### Resource Types (COAR)
The type field must use COAR Resource Type vocabulary:
- Dataset: `http://purl.org/coar/resource_type/c_ddb1`
- Image: `http://purl.org/coar/resource_type/c_c513`
- Text: `http://purl.org/coar/resource_type/c_18cc`
- Collection: `http://purl.org/coar/resource_type/c_12cc`

### Licenses
Standard license identifiers:
- CC-BY-4.0, CC-BY-SA-4.0, CC-BY-NC-4.0
- CC0-1.0
- GPL-3.0, MIT, Apache-2.0

### Languages
ISO 639-1 language codes:
- fr (French), en (English), es (Spanish), de (German)
- Full list available via NAKALA API: `/vocabularies/languages`

## Transformation Examples

### CSV Input to API Format

**CSV:**
```csv
title,description,keywords,author,type,license
"fr:Données climat|en:Climate data","fr:Description|en:Description","fr:climat;météo|en:climate;weather","Dupont,Jean","http://purl.org/coar/resource_type/c_ddb1","CC-BY-4.0"
```

**API JSON:**
```json
[
  {
    "propertyUri": "http://nakala.fr/terms#title",
    "value": "Données climat",
    "lang": "fr",
    "typeUri": "http://www.w3.org/2001/XMLSchema#string"
  },
  {
    "propertyUri": "http://nakala.fr/terms#title",
    "value": "Climate data", 
    "lang": "en",
    "typeUri": "http://www.w3.org/2001/XMLSchema#string"
  },
  {
    "propertyUri": "http://nakala.fr/terms#creator",
    "value": [{"givenname": "Jean", "surname": "Dupont"}]
  },
  {
    "propertyUri": "http://nakala.fr/terms#type",
    "value": "http://purl.org/coar/resource_type/c_ddb1",
    "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI"
  }
]
```

## API Endpoints for Vocabularies

Retrieve controlled vocabularies via NAKALA API:

- **Properties**: `GET /vocabularies/properties`
- **Types**: `GET /vocabularies/datatypes`
- **Languages**: `GET /vocabularies/languages`
- **Licenses**: `GET /vocabularies/licenses`
- **Metadata Types**: `GET /vocabularies/metadatatypes`

## Usage in Different Modules

### Upload Module
Uses property URIs for initial data creation with complete metadata requirements.

### Collection Module  
Uses subset of property URIs focused on collection-specific metadata.

### Curator Module
Uses property URIs for metadata modifications with validation and transformation.

### User Info Module
Retrieves metadata using property URIs for display and analysis.

## Best Practices

1. **Use standard property URIs** - Stick to the defined mappings for consistency
2. **Validate controlled vocabularies** - Ensure type, license, and language values are valid
3. **Handle multilingual content properly** - Use language-specific metadata entries
4. **Maintain object structure** - Especially for creator/author fields
5. **Check API vocabulary endpoints** - For the latest controlled vocabulary values

## Related Documentation

- [Curator Field Reference](curator-field-reference.md) - Complete field reference with examples
- [NAKALA API Specifications](../NAKALA_API_SPECIFICATIONS.md) - Official API documentation
- [Dublin Core Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) - Dublin Core specification
- [COAR Resource Types](https://vocabularies.coar-repositories.org/resource_types/) - Resource type vocabulary