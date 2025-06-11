# Nakala Client Upload Script

A Python script for uploading datasets and their associated files to the Nakala platform.

## Main Features:

1. **Multiple Upload Modes**:
   - CSV-based dataset upload
   - Folder-based dataset upload with automatic organization
2. **Intelligent File Processing**:
   - Automatic file type detection
   - Dynamic MIME type detection
   - File validation and existence checks
3. **Metadata Management**:
   - Multilingual support for titles, descriptions, and keywords
   - Complex metadata including authors, keywords, and rights
   - Automatic metadata generation from folder structure
4. **Robust Error Handling**:
   - Automatic retry mechanism for failed uploads
   - Comprehensive error logging
   - Graceful failure handling
5. **Detailed Logging**:
   - Upload progress tracking
   - Success/failure information
   - Detailed error messages

## Usage Examples:

```bash
# CSV Mode (Basic)
o-nakala-upload \
    --api-key "your-api-key" \
    --dataset dataset.csv \
    --base-path img/

# CSV Mode (Full)
o-nakala-upload \
    --api-key "your-api-key" \
    --api-url "https://apitest.nakala.fr" \
    --dataset dataset.csv \
    --base-path img/

# Folder Mode
o-nakala-upload \
    --api-key "your-api-key" \
    --mode folder \
    --dataset "path/to/dataset" \
    --folder-config "path/to/folder_config.csv"
```

## Command Line Arguments:

- `--api-key`: (Required) Your Nakala API key
- `--api-url`: (Optional) Nakala API URL (default: https://apitest.nakala.fr)
- `--dataset`: (Required) Path to dataset CSV file or folder
- `--image-dir`: (Optional) Directory containing images (for CSV mode)
- `--mode`: (Optional) Upload mode: 'csv' or 'folder' (default: 'csv')
- `--folder-config`: (Required for folder mode) Path to folder configuration CSV

## Dataset Formats:

### CSV Mode Format:
The script expects a CSV file with the following columns:

1. `files`: Semicolon-separated list of filenames
2. `status`: Status of the upload (e.g., "private", "public")
3. `type`: Type of the data
4. `title`: Title of the data
5. `authors`: Semicolon-separated list of authors (format: "surname,givenname")
6. `created`: Creation date
7. `license`: License information
8. `description`: Description of the data
9. `keywords`: Semicolon-separated list of keywords
10. `rights`: Semicolon-separated list of rights (format: "group_id,role")

Example CSV row:
```csv
files,status,type,title,authors,created,license,description,keywords,rights
image1.jpg;image2.jpg,private,Image,Smith,John;Doe,Jane,2024-01-01,CC-BY,Description,keyword1;keyword2,de0f2a9b-a198-48a4-8074-db5120187a16,admin
```

### Folder Mode Format:
The folder configuration CSV should contain:

1. `file`: Folder path
2. `status`: Upload status
3. `type`: Data type
4. `title`: Multilingual title (format: "lang:title|lang:title")
5. `description`: Multilingual description
6. `keywords`: Multilingual keywords
7. `license`: License information
8. `rights`: Rights configuration
9. `author`: Author information
10. `date`: Creation date
11. `language`: Language information
12. `temporal`: Temporal coverage
13. `spatial`: Spatial coverage

Example folder configuration:
```csv
file,status,type,title,description,keywords,license,rights,author,date,language,temporal,spatial
images,private,Image,en:Image Collection|fr:Collection d'Images,en:Collection of images|fr:Collection d'images,en:images;photography|fr:images;photographie,CC-BY,de0f2a9b-a198-48a4-8074-db5120187a16,admin,Smith,John,2024-01-01,en,2024,World
```

## Output:

The script generates two output files:

1. `output.csv`: Contains upload results with columns:
   - identifier: Nakala ID of the uploaded data
   - files: List of uploaded files with their SHA1 hashes
   - title: Title of the data
   - status: Upload status (OK or ERROR)
   - response: Full API response

2. `nakala_upload.log`: Detailed log file containing:
   - Upload progress
   - Success/failure information
   - Error messages
   - API responses

## Example Success Output:
```
Processing entry 1/3: Image Collection
Uploading file: image1.jpg
Successfully created data: 10.34847/nkl.f1c8y3w0
```

## Error Handling:

The script implements a robust error handling system:
- Automatic retry mechanism for failed uploads (up to 3 attempts)
- Exponential backoff between retries
- Comprehensive error logging
- Graceful failure handling for individual files
- Continues processing remaining files even if some uploads fail

## Requirements:

- Python 3.6+
- Required packages:
  - requests
  - openapi_client
  - tenacity
  - csv
  - logging
  - datetime
  - typing
  - mimetypes
  - pathlib

## Integration with Collection Script:

After successful upload, you can use the generated `output.csv` with the collection script to create collections:

```bash
# Step 1: Upload data
o-nakala-upload --api-key "your-api-key" --mode folder --dataset "path/to/dataset" --folder-config "path/to/folder_config.csv"

# Step 2: Create collection from uploaded data
o-nakala-collection --api-key "your-api-key" --title "My Collection" --from-upload-output output.csv
```
