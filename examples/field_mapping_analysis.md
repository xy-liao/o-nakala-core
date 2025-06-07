# CSV-to-API Field Mapping Analysis

## Current Limitation Identified

**Issue:** The curator batch modification only processes `new_title` and `new_description` fields in the CSV parser.

**Location:** `/src/nakala_client/curator.py` lines 1158-1163

**Current Code:**
```python
changes = {}
if row.get("new_title"):
    changes["title"] = row["new_title"]
if row.get("new_description"):
    changes["description"] = row["new_description"]
# Add more fields as needed <- This comment indicates incomplete implementation
```

## Available Metadata Fields in NAKALA Items

Based on API inspection of data item `10.34847/nkl.3aa9p7u3`:

| Property URI | Language Support | Example Values | CSV Column Name |
|-------------|------------------|----------------|-----------------|
| `http://nakala.fr/terms#title` | ✅ fr/en | "Collection d'images" | `new_title` ✅ |
| `http://purl.org/dc/terms/description` | ✅ fr/en | "Collection d'images de recherche..." | `new_description` ✅ |
| `http://purl.org/dc/terms/subject` | ✅ fr/en | "images", "visuel", "recherche" | `new_keywords` ❌ |
| `http://nakala.fr/terms#created` | ❌ No | "2023-05-21" | `new_date` ❌ |
| `http://nakala.fr/terms#license` | ❌ No | "CC-BY-4.0" | `new_license` ❌ |
| `http://nakala.fr/terms#type` | ❌ No | "http://purl.org/coar/resource_type/c_c513" | `new_type` ❌ |
| `http://purl.org/dc/terms/rights` | ❌ No | "de0f2a9b-a198-48a4-8074-db5120187a16,ROLE_READER" | `new_rights` ❌ |

**Legend:**
- ✅ = Currently supported by curator
- ❌ = Not supported by curator parser (needs enhancement)

## Missing Creator Field Analysis

**Critical Finding:** No `http://nakala.fr/terms#creator` field exists in the data items examined.

This explains why:
1. Validation reports missing creator fields
2. Our attempts to add creators via batch modification have not worked
3. Creator fields may need to be added during initial upload, not modification

## Required Enhancements

### 1. Expand CSV Parser Support
Add support for all modifiable fields in curator.py:
```python
# Enhanced parser needed:
if row.get("new_keywords"):
    changes["keywords"] = row["new_keywords"]
if row.get("new_author"):
    changes["author"] = row["new_author"]  # Maps to creator
if row.get("new_license"):
    changes["license"] = row["new_license"]
# ... etc for all fields
```

### 2. Creator Field Handling
Need to investigate:
- Whether creator can be added post-creation
- Correct property URI for creator field
- API requirements for creator metadata

### 3. Template Generation Enhancement
The export template should include ALL modifiable fields, not just basic ones.

## Working Example (Current Implementation)

With current limitations, only these modifications work:

```csv
id,action,new_title,new_description
10.34847/nkl.3aa9p7u3,modify,fr:Enhanced Title|en:Enhanced Title,fr:Enhanced description|en:Enhanced description
```

## Recommended CSV Format (Future Enhancement)

Once parser is enhanced:

```csv
id,action,new_title,new_description,new_keywords,new_author,new_license,new_type
10.34847/nkl.3aa9p7u3,modify,fr:Title|en:Title,fr:Desc|en:Desc,fr:mot1;mot2|en:word1;word2,Dupont\,Jean,CC-BY-4.0,http://purl.org/coar/resource_type/c_c513
```