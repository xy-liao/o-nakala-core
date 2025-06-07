Looking at your Nakala Curator code, I can see that it's designed for metadata modifications specifically, but let me analyze what it can currently modify and what specifications need to be respected.

## Current Modification Capabilities

The curator can modify these **metadata fields**:

### 1. **Title** (`http://nakala.fr/terms#title`)
- Supports multilingual entries (fr/en)
- Format: `"fr:Titre français|en:English title"` or single language
- Required field - cannot be empty

### 2. **Description** (`http://purl.org/dc/terms/description`)  
- Supports multilingual entries (fr/en)
- Format: same as title with language prefixes
- Required field - cannot be empty

### 3. **Keywords/Subject** (`http://purl.org/dc/terms/subject`)
- Supports multilingual entries
- Format: `"fr:mot-clé1;mot-clé2|en:keyword1;keyword2"`
- Semicolon-separated within languages

## What the Curator **Cannot** Modify

Based on the code, it **cannot** modify:
- **File content** (binary files, documents)
- **Collection structure** (adding/removing datasets)
- **Access permissions** and visibility settings
- **Dataset identifier** (immutable)
- **File uploads** or file replacements
- **License changes** (though validation exists)
- **Creator/contributor** fields
- **Dates** (creation, modification - system managed)

## Nakala API Specifications to Respect

### 1. **Authentication & Authorization**
```python
headers = {'X-API-KEY': self.config.api_key}
```
- Valid API key required
- User must have **write permissions** on the dataset
- Collections may require special permissions

### 2. **Metadata Structure Requirements**
```python
meta_object = {
    'value': 'The actual value',
    'lang': 'fr',  # Language code (fr, en, etc.)
    'propertyUri': 'http://purl.org/dc/terms/description'
}
```

### 3. **Required Metadata Fields**
From the validator:
```python
required_fields = ['title', 'creator', 'description']
```

### 4. **API Rate Limiting**
```python
time.sleep(0.5)  # Delay between batches
```
- The code includes delays to avoid overwhelming the API
- Batch size limited to 50 items by default

### 5. **Controlled Vocabularies**
```python
valid_licenses = ['CC-BY-4.0', 'CC-BY-SA-4.0', 'CC-BY-NC-4.0', 'CC0-1.0']
```

## Enhanced Modification Capabilities

To extend the curator for more comprehensive modifications, you could add:## Key Specifications Summary

1. **API Authentication**: Valid X-API-KEY header required
2. **Permissions**: User must have write access to modify items
3. **Required Fields**: Title, creator, description cannot be empty
4. **Metadata Format**: Structured with value, language, and propertyUri
5. **Rate Limiting**: Built-in delays between batch operations
6. **Validation**: Pre-modification validation available
7. **Backup**: Optional backup before changes
8. **Dry Run**: Test mode for modifications

The current curator is primarily focused on **metadata modifications** and **quality management**. For comprehensive data management including file operations, permission changes, and collection structure modifications, you'd need the enhanced version I've outlined above.