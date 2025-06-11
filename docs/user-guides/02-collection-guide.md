# Nakala Client Collection Script

A Python script for managing collections on the Nakala platform.

## Main Features:

1. **Create collection from upload output**: Uses the `output.csv` file from your upload script to automatically create a collection with all successfully uploaded data items.

2. **Create collection from data ID list**: Allows manual specification of data IDs for collection creation.

3. **Create collections from folder structure**: Automatically creates collections based on folder organization and configuration files.

4. **Comprehensive metadata support**: Handles multilingual metadata (French/English) including:
   - Titles and descriptions
   - Keywords and subjects
   - Creators and contributors
   - Publishers and dates
   - Rights and licenses
   - Coverage and relations
   - Sources

5. **Error handling and retry logic**: Implements robust error handling with automatic retries for failed API calls.

6. **Collection mapping diagnostics**: Provides detailed information about:
   - Folder matching process
   - Data item inclusion
   - Collection creation status
   - Any unmatched folders

## Usage Examples:

```bash
# Create collection from upload output
o-nakala-collection \
    --api-key "your-api-key" \
    --title "My Bird Collection" \
    --description "A collection of bird photographs" \
    --keywords "birds,wildlife,photography" \
    --status private \
    --from-upload-output output.csv

# Create collection from specific data IDs
o-nakala-collection \
    --api-key "your-api-key" \
    --title "Selected Images" \
    --description "Curated selection of images" \
    --keywords "selection,curated" \
    --status public \
    --data-ids "10.34847/nkl.f1c8y3w0,10.34847/nkl.3bdeo0xj"

# Create collections from folder structure
o-nakala-collection \
    --api-key "your-api-key" \
    --from-folder-collections "folder_collections.csv" \
    --from-upload-output "output.csv" \
    --collection-report "collections_output.csv"
```

## Folder-Based Collection Creation

The script supports creating collections based on folder structure using two CSV files:

1. **folder_collections.csv**: Defines collection metadata and folder mappings
   ```csv
   title,status,description,keywords,language,creator,contributor,publisher,date,rights,coverage,relation,source,data_items
   fr:Collection Title|en:Collection Title,private,fr:Description|en:Description,fr:keywords|en:keywords,fr,Creator1;Creator2,Contributor1;Contributor2,Publisher,2024-05-21,CC-BY-4.0,fr:coverage|en:coverage,fr:relation|en:relation,fr:source|en:source,folder1|folder2
   ```

2. **output.csv**: Contains uploaded data items information
   ```csv
   file,status,type,title,identifier
   folder1/file1.txt,OK,type,fr:Title|en:Title,10.34847/nkl.xxxxx
   ```

## Collection Structure Example

The script creates collections with the following structure:

```
Collections
├── Code and Data Collection
│   ├── Code Files
│   └── Research Data
├── Documents Collection
│   └── Research Documents
└── Multimedia Collection
    ├── Image Collection
    └── Presentation Materials
```

## Command Line Arguments:

- `--api-key`: (Required) Your Nakala API key
- `--api-url`: (Optional) Nakala API URL (default: https://apitest.nakala.fr)
- `--title`: Collection title (required for single collection creation)
- `--description`: Collection description
- `--keywords`: Comma-separated keywords
- `--status`: Collection status (private or public, default: private)
- `--from-upload-output`: Path to upload output CSV file
- `--data-ids`: Comma-separated list of data IDs
- `--from-folder-collections`: Path to folder collections configuration CSV
- `--collection-report`: Path to save collection creation report

## Output:

The script provides:
- Detailed logging information
- Collection IDs upon successful creation
- Error messages if creation fails
- Collection report in CSV format
- Log file: `nakala_collection.log`

## Example Success Output:
```
Found 5 uploaded data items
Created collection: fr:Collection de Code et Données |en:Code and Data Collection with ID: 10.34847/nkl.xxxxx
Created collection: fr:Collection de Documents|en:Documents Collection with ID: 10.34847/nkl.yyyyy
Created collection: fr:Collection Multimédia PERFECT|en:Multimedia Collection with ID: 10.34847/nkl.zzzzz
Collection report saved to: collections_output.csv
```

## Collection Report Format

The collection report (`collections_output.csv`) includes:
- Collection ID
- Collection title
- Status
- Number of data items
- Data item IDs
- Creation status
- Error messages (if any)
- Timestamp

This approach provides a flexible and powerful way to manage collections while maintaining proper metadata standards and supporting multilingual content.

## Collection Mapping Diagnostics

The script provides detailed diagnostics about the collection creation process:

```json
{
  "folder": {
    "code": {
      "path": "files/code",
      "matches": [
        {
          "title": "fr:Fichiers de code|en:Code Files",
          "id": "10.34847/nkl.xxxxx"
        }
      ]
    }
  },
  "matched_items": ["fr:Fichiers de code|en:Code Files"],
  "unmatched_folders": []
}
```

This output helps you:
1. Verify correct folder matching
2. Check data item inclusion
3. Identify any unmatched folders
4. Track collection creation status

## Successful Collection Creation

When collections are created successfully, you'll see output like:

```
Found 5 uploaded data items
Creating collection: fr:Collection de Code et Données |en:Code and Data Collection
Created collection: 10.34847/nkl.5aee9iwt
Created collection: fr:Collection de Code et Données |en:Code and Data Collection with ID: 10.34847/nkl.5aee9iwt
```

The script will create:
1. A collection report in `collections_output.csv`
2. Detailed logs in `nakala_collection.log`
3. Collection IDs for each created collection