# Nakala API Implementation Notes

## Hybrid Approach: OpenAPI Client and Requests

We needed to implement a hybrid approach using both the OpenAPI generated client and the `requests` library due to specific requirements and limitations encountered during implementation.

### File Upload Implementation

#### Why Use `requests` for File Upload?

1. **Multipart Form Data Handling**
   - The OpenAPI client had limitations with properly formatting multipart/form-data
   - The working implementation in `tp-depot-par-lot.py` used `requests` with the following format:
   ```python
   postfiles=[('file', (filename, open(file_path, 'rb'), 'image/jpeg'))]
   ```
   - This specific format is required by Nakala's API for file uploads

2. **Response Structure**
   - File upload response only includes minimal fields:
     - `sha1`: The file's SHA1 hash
   - Other fields like `size` and `mime_type` are not consistently returned

### OpenAPI Client Usage

#### Data Creation Inconsistencies

1. **Parameter Names**
   - The OpenAPI generated client expects different parameter names than what the API actually accepts
   - Current workaround: Use `requests` for file upload and maintain compatibility with the OpenAPI client for metadata

2. **Type Validation**
   - The OpenAPI client implements strict type validation
   - Need to ensure proper typing, especially for metadata values that can be either strings or dictionaries

### Working Implementation Structure

```python
class UploadedFile:
    """Represents a successfully uploaded file in Nakala."""
    sha1: str
    filename: str
    embargoed: Optional[str] = None

def upload_file(filename: str, file_path: str) -> UploadedFile:
    """Upload using requests for proper multipart handling."""
    with open(file_path, 'rb') as f:
        postfiles = [('file', (filename, f, 'image/jpeg'))]
        headers = {'X-API-KEY': API_KEY}
        response = requests.post(
            f"{API_URL}/datas/uploads",
            headers=headers,
            data={},
            files=postfiles
        )
```

### Metadata Structure

Required metadata format for the API:
```python
meta = {
    "value": str | {"surname": str, "givenname": str},
    "typeUri": str,
    "propertyUri": str,
    "lang": Optional[str]
}
```

### Known Issues and Solutions

1. **File Upload Response**
   - Issue: Inconsistent response fields from `/datas/uploads` endpoint
   - Solution: Only rely on `sha1` field and maintain filename locally

2. **Data Creation Parameters**
   - Issue: OpenAPI client validation errors for parameter names
   - Solution: Need to update OpenAPI specification to match actual API requirements

3. **Content Type Handling**
   - Issue: Must explicitly set `'image/jpeg'` for image uploads
   - Note: May need to implement MIME type detection for other file types

## Recommendations

1. Consider updating the OpenAPI specification to match actual API requirements
2. Implement proper MIME type detection based on file extensions
3. Add validation for required metadata fields before submission
4. Consider implementing retry logic for file uploads
5. Add proper error handling for network issues during file upload

## API Endpoint Reference

- File Upload: `POST /datas/uploads`
  - Headers: `X-API-KEY`
  - Format: multipart/form-data
  - Required Fields: `file`

- Data Creation: `POST /datas`
  - Required Fields:
    - `status`
    - `group_identifier`
    - `files` (array of uploaded file info)
    - `metas` (array of metadata)
