# Nakala API Implementation Notes

## Current Implementation Status

### ✅ **Issues Resolved**
1. ~~Hard-coded MIME types~~ → Now uses dynamic detection
2. ~~Missing CSV processing~~ → Fully implemented
3. ~~File validation issues~~ → Enhanced validation added

### 🔄 **Current Features**
- Dynamic MIME type detection: ✅ Implemented
- Folder processing: ✅ Complete
- Multilingual support: ✅ Working
- Error handling: ✅ Robust
- Retry mechanism: ✅ Implemented with exponential backoff

## Technical Implementation Details

### Hybrid API Client Approach
```python
# Using requests for file uploads
        response = requests.post(
    f"{self.api_url}/datas/uploads",
    headers={'X-API-KEY': self.api_key},
    files=[('file', (filename, open(file_path, 'rb'), mime_type))]
)

# Using OpenAPI client for metadata
from openapi_client.rest import ApiException
```

### Dynamic MIME Type Detection
```python
# Detect MIME type dynamically
mime_type, _ = mimetypes.guess_type(file_path)
if not mime_type:
    mime_type = 'application/octet-stream'
```

### Enhanced File Validation
```python
def validate_file_exists_absolute(self, file_path: str) -> bool:
    """Validate that a file exists using absolute path."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False
    if not os.path.isfile(file_path):
        logger.error(f"Path is not a file: {file_path}")
        return False
    return True
```

## Known Issues and Solutions

### 1. API Rate Limiting
- **Issue**: API may reject requests if too many are made
- **Solution**: Implemented retry with exponential backoff
- **Status**: ✅ Resolved

### 2. Large File Uploads
- **Issue**: Timeout on large file uploads
- **Solution**: Added chunked upload support
- **Status**: ✅ Resolved

### 3. Multilingual Metadata
- **Issue**: Complex metadata format
- **Solution**: Implemented structured metadata handling
- **Status**: ✅ Resolved

## Best Practices

### File Upload
1. Always validate files before upload
2. Use dynamic MIME type detection
3. Implement proper error handling
4. Log all upload attempts

### Metadata Handling
1. Validate metadata format
2. Support multilingual content
3. Use proper property URIs
4. Include required fields

### Error Handling
1. Implement retry mechanism
2. Log detailed error messages
3. Provide clear user feedback
4. Handle edge cases gracefully

## Hybrid Approach: OpenAPI Client and Requests

We needed to implement a hybrid approach using both the OpenAPI generated client and the `