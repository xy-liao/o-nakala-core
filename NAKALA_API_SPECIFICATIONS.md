# NAKALA API Official Specifications and Guidelines

## Based on Official Notebooks Analysis

This document summarizes the official NAKALA API specifications from the official notebooks to ensure our o-nakala-core project aligns with official expectations and standards.

## 1. NAKALA Overview

### What is NAKALA?
NAKALA is a Huma-Num service allowing researchers, teacher-researchers, or research teams to share, publish, and valorize all types of documented digital data (text files, sounds, images, videos, 3D objects, etc.) in a secure repository to publish them according to FAIR data principles (Findable, Accessible, Interoperable, Reusable).

### Architecture Components:
- **Core API**: https://api.nakala.fr/doc
- **Web interface**: https://nakala.fr for deposit and consultation
- **NAKALA_PRESS**: Website creation module

## 2. API Fundamentals

### Base URLs:
- **Production**: https://api.nakala.fr
- **Test Environment**: https://apitest.nakala.fr
- **Documentation**: https://api.nakala.fr/doc

### Core HTTP Structure:
```
Request:
- URL: Endpoint specific (e.g., /datas, /collections)
- Headers: Authentication, Content-Type, Accept-Language
- Verb: GET, POST, PUT, PATCH, DELETE
- Body: JSON content when required

Response:
- Status Code: 200, 201, 204, 401, 403, 404, 422, 500
- Headers: Response metadata
- Body: JSON content with results or error details
```

## 3. Authentication

### API Key System:
- Each user has a unique API key
- Obtained from user profile in NAKALA web interface
- Must be included in request header: `X-API-KEY: your-key-here`
- Test environment keys provided for testing

### Test Environment Credentials:
| Username | Password | API Key | Purpose |
|----------|----------|---------|---------|
| tnakala | IamTesting2020 | 01234567-89ab-cdef-0123-456789abcdef | Basic testing |
| unakala1 | IamTesting2020 | 33170cfe-f53c-550b-5fb6-4814ce981293 | Upload testing |
| unakala2 | IamTesting2020 | f41f5957-d396-3bb9-ce35-a4692773f636 | Collection testing |
| unakala3 | IamTesting2020 | aae99aba-476e-4ff2-2886-0aaf1bfa6fd2 | Curation testing |

## 4. JSON Format Standards

### Metadata Structure:
```json
{
    "value": "Nomenclature 3D du bâtiment C1-C5",
    "lang": "fr",
    "typeUri": "http://www.w3.org/2001/XMLSchema#string",
    "propertyUri": "http://nakala.fr/terms#title"
}
```

### Required Components:
- **value**: The actual metadata value
- **lang**: Language code (ISO-639-1 or ISO-639-3)
- **typeUri**: Data type (string, anyURI, etc.)
- **propertyUri**: Vocabulary URI (nakala.fr/terms# or purl.org/dc/terms/)

## 5. Core API Endpoints Structure

### Main Sections:
1. **search**: Search engine for data and collections
2. **datas**: Data management
3. **collections**: Collection management
4. **groups**: User group management
5. **users**: User management
6. **vocabularies**: Access to vocabularies

## 6. Data Item Management

### Data Creation Process:
1. **File Upload**: `POST /datas/uploads`
2. **Data Creation**: `POST /datas` with metadata and file references

### File Upload Requirements:
```python
# Upload request structure
files = [('file', (filename, open(filepath, 'rb'), mime_type))]
headers = {'X-API-KEY': api_key}
response = requests.post(api_url + '/datas/uploads', headers=headers, files=files)

# Response format
{
    "name": "filename.jpg",
    "sha1": "unique-file-identifier"
}
```

### Data Creation Requirements:
```json
{
    "status": "pending|published",
    "files": [
        {
            "name": "filename.jpg",
            "sha1": "file-identifier",
            "embargoed": "YYYY-MM-DD",
            "description": "Optional file description"
        }
    ],
    "metas": [
        {
            "propertyUri": "http://nakala.fr/terms#title",
            "value": "Data title",
            "lang": "fr",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        }
    ],
    "rights": [
        {
            "id": "user-or-group-id",
            "role": "ROLE_READER|ROLE_EDITOR|ROLE_ADMIN|ROLE_OWNER"
        }
    ],
    "collectionsIds": ["collection-id-1", "collection-id-2"]
}
```

### Required Metadata for Published Data:
- **http://nakala.fr/terms#title**: Data title
- **http://nakala.fr/terms#type**: Data type (from vocabularies)
- **http://nakala.fr/terms#creator**: Creator information
- **http://nakala.fr/terms#created**: Creation date (YYYY, YYYY-MM, or YYYY-MM-DD)
- **http://nakala.fr/terms#license**: License (from vocabularies)

### Creator Object Structure:
```json
{
    "value": {
        "givenname": "Jean",
        "surname": "Dupont",
        "orcid": "0000-0000-0000-0000"  // Optional
    },
    "propertyUri": "http://nakala.fr/terms#creator"
}
```

## 7. Collection Management

### Collection Creation:
```json
{
    "status": "private|public",
    "datas": ["data-id-1", "data-id-2"],  // Optional
    "metas": [
        {
            "propertyUri": "http://nakala.fr/terms#title",
            "value": "Collection title",
            "lang": "fr",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
        }
    ],
    "rights": [
        {
            "id": "user-or-group-id",
            "role": "ROLE_READER|ROLE_EDITOR|ROLE_ADMIN"
        }
    ]
}
```

### Collection Modification Options:
- `POST /collections/{id}/datas`: Add data items
- `POST /collections/{id}/metadatas`: Add metadata
- `POST /collections/{id}/rights`: Add rights
- `DELETE /collections/{id}/datas`: Remove data items
- `DELETE /collections/{id}/metadatas`: Remove metadata
- `DELETE /collections/{id}/rights`: Remove rights
- `PUT /collections/{id}/status/{status}`: Change status
- `PUT /collections/{id}`: Global update (replaces all information)

## 8. Rights Management

### Permission Levels:
- **ROLE_OWNER**: Resource owner (auto-assigned to depositor)
- **ROLE_ADMIN**: Administration rights (delete, share)
- **ROLE_EDITOR**: Edit rights (modify metadata, add data)
- **ROLE_READER**: Read-only access
- **ROLE_DEPOSITOR**: Auto-assigned to depositor (no inherent permissions)

### Group Management:
```json
{
    "name": "Group name",
    "users": [
        {
            "username": "humanid-username",
            "role": "ROLE_OWNER|ROLE_ADMIN|ROLE_USER"
        }
    ]
}
```

## 9. Vocabularies and Standards

### Key Vocabulary Endpoints:
- `GET /vocabularies/properties`: Available metadata fields
- `GET /vocabularies/metadatatypes`: Data type URIs
- `GET /vocabularies/languages`: Language codes
- `GET /vocabularies/datatypes`: Data type classifications
- `GET /vocabularies/licenses`: Available licenses

### Common Type URIs:
- **String**: `http://www.w3.org/2001/XMLSchema#string`
- **URI**: `http://www.w3.org/2001/XMLSchema#anyURI`
- **Date**: `http://www.w3.org/2001/XMLSchema#date`

### Common Property URIs:
- **NAKALA Terms**: `http://nakala.fr/terms#[property]`
- **Dublin Core**: `http://purl.org/dc/terms/[property]`

## 10. Batch Processing Guidelines

### CSV Structure for Batch Upload:
```csv
file,status,type,title,author,date,licence,description,keywords,rights
filename.jpg,pending,type-uri,Title,Surname,Firstname,YYYY-MM-DD,CC-BY-4.0,Description,keyword1;keyword2,user-id,ROLE_READER
```

### Processing Steps:
1. **Parse CSV**: Extract metadata for each row
2. **Upload Files**: Use `/datas/uploads` for each file
3. **Collect File Info**: Store sha1 and name from upload response
4. **Build Metadata**: Convert CSV data to API JSON format
5. **Create Data**: Use `/datas` endpoint with complete payload
6. **Log Results**: Track success/failure for each item

### Error Handling:
- Validate CSV structure before processing
- Handle upload failures gracefully
- Log detailed error messages
- Support resume functionality for large batches

## 11. Internationalization

### Language Support:
- **French**: Primary language
- **English**: Secondary language  
- **Spanish**: Additional support
- Use `Accept-Language: fr` header for French responses

### Multilingual Metadata:
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
        "value": "English title",
        "lang": "en",
        "typeUri": "http://www.w3.org/2001/XMLSchema#string"
    }
]
```

## 12. File and Media Management

### Supported File Types:
- **Images**: JPG, PNG, TIFF, etc.
- **Documents**: PDF, TXT, DOC, etc.
- **Data**: CSV, XML, JSON, etc.
- **Audio/Video**: MP3, MP4, etc.
- **3D Objects**: Various formats

### Embargo System:
- **embargoed**: Date when file becomes publicly accessible
- **Format**: "YYYY-MM-DD"
- **Behavior**: Files remain private until embargo date passes
- **Current date**: Makes file immediately accessible

### Viewers and APIs:
- **IIIF Image API**: For images
- **Embed URLs**: `https://api.nakala.fr/embed/{data-id}/{file-sha1}`
- **Direct access**: Available after embargo period

## 13. Validation and Quality Control

### API-Level Validation:
- **Creation**: Strict validation (all required fields)
- **Modification**: More permissive (core fields only)
- **Status dependent**: Published data has stricter requirements

### Required vs Optional Fields:
- **Always Required**: title, type (for data), API key
- **Required for Published**: creator, created, license
- **Optional**: description, keywords, alternative titles

### Error Response Format:
```json
{
    "code": 422,
    "message": "Data could not be submitted because of invalid data",
    "payload": {
        "validationErrors": [
            "The metadata http://nakala.fr/terms#title is required."
        ]
    }
}
```

## 14. Best Practices for Implementation

### API Client Design:
1. **Respect rate limits**: Add delays between requests
2. **Error handling**: Implement retry logic with exponential backoff
3. **Logging**: Comprehensive logging for debugging
4. **Validation**: Client-side validation before API calls
5. **Progress tracking**: For batch operations

### Data Organization:
1. **Collections first**: Create collections before adding data
2. **Batch processing**: Group related operations
3. **Metadata consistency**: Use standardized vocabularies
4. **Rights management**: Set appropriate permissions

### Development Guidelines:
1. **Use test environment**: Always test with apitest.nakala.fr
2. **Follow OpenAPI spec**: API documentation is authoritative
3. **Handle multilingual content**: Support French/English at minimum
4. **Implement proper authentication**: Secure API key handling

## 15. Integration Points for o-nakala-core

### CLI Commands Alignment:
- **upload**: Implements file upload + data creation workflow
- **collection**: Implements collection creation and management
- **curator**: Implements metadata modification and quality control
- **user-info**: Implements user information retrieval

### Configuration Requirements:
- **API URLs**: Support for both production and test environments
- **Authentication**: Secure API key storage and usage
- **Batch processing**: CSV parsing and processing capabilities
- **Error handling**: Comprehensive error reporting and recovery

### Quality Assurance:
- **Metadata validation**: Align with official vocabulary requirements
- **Rights management**: Implement proper permission handling
- **Internationalization**: Support multilingual metadata
- **Testing**: Comprehensive testing against official test environment

This specification serves as the authoritative reference for developing o-nakala-core in compliance with official NAKALA API standards and expectations.