# Nakala Client Upload Script

A Python script for uploading datasets and their associated files to the Nakala platform.

## Main Features:

1. **Batch Upload Support**: Upload multiple files and their metadata in a single operation
2. **CSV Dataset Processing**: Process dataset information from a CSV file
3. **Automatic File Validation**: Verify file existence before upload
4. **Robust Error Handling**: Implements retry mechanism for failed uploads
5. **Detailed Logging**: Comprehensive logging of all operations
6. **Metadata Management**: Handles complex metadata including authors, keywords, and rights

## Usage Examples:

```bash
# Basic usage with required parameters
python nakala-client-upload.py \
    --api-key "your-api-key" \
    --dataset dataset.csv \
    --image-dir img/

# Full usage with all options
python nakala-client-upload.py \
    --api-key "your-api-key" \
    --api-url "https://apitest.nakala.fr" \
    --dataset dataset.csv \
    --image-dir img/
```

## Command Line Arguments:

- `--api-key`: (Required) Your Nakala API key
- `--api-url`: (Optional) Nakala API URL (default: https://apitest.nakala.fr)
- `--dataset`: (Optional) Path to dataset CSV file (default: simple-dataset/dataset.csv)
- `--image-dir`: (Optional) Directory containing images (default: simple-dataset/img)

## Dataset CSV Format:

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
Processing entry 1/3: Martin-pêcheur
Uploading file: kingfisher.jpg
Successfully created data: 10.34847/nkl.f1c8y3w0
```

## Error Handling:

The script implements a robust retry mechanism:
- Automatically retries failed uploads up to 3 times
- Uses exponential backoff between retries
- Logs all errors and retry attempts
- Continues processing remaining files even if some uploads fail

## Integration with Collection Script:

After successful upload, you can use the generated `output.csv` with the collection script to create collections:

```bash
# Step 1: Upload data
python nakala-client-upload.py --api-key "your-api-key" --dataset dataset.csv --image-dir img/

# Step 2: Create collection from uploaded data
python nakala_collection_script.py --api-key "your-api-key" --title "My Collection" --from-upload-output output.csv
```

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
