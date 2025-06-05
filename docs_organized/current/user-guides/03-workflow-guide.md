# Complete Workflow Guide

## Digital Humanities Research Workflow

### Step 1: Organize Your Data
- Create folder structure by content type (e.g., `files/code`, `files/data`, `files/documents`)
- Prepare metadata CSV files:
  - `folder_data_items.csv` for data items
  - `folder_collections.csv` for collections
- Validate file formats and metadata
- Ensure folder paths in CSV files match actual directory structure

### Step 2: Upload Dataset
```bash
# Important: Use the correct base path for your dataset
python nakala-client-upload.py --mode folder \
    --dataset "sample_dataset" \
    --folder-config "sample_dataset/folder_data_items.csv" \
    --api-key "your-key"
```

Note: The `--dataset` parameter should point to the base directory containing your `files` folder. The script will automatically handle the folder structure within it.

### Step 3: Create Collections
```bash
python nakala-client-collection.py \
    --api-key "your-key" \
    --from-folder-collections "sample_dataset/folder_collections.csv" \
    --from-upload-output "output.csv" \
    --collection-report "collections_output.csv"
```

### Step 4: Verify and Publish
- Check upload results in `output.csv`
- Verify collection creation in `collections_output.csv`
- Review collection structure and relationships
- Check collection mapping diagnostics in the logs
- Update status from private to public if needed

## Common Workflows

### 1. Folder-Based Collection Creation
```bash
# Create collections based on folder structure
python nakala-client-collection.py \
    --api-key "your-key" \
    --from-folder-collections "folder_collections.csv" \
    --from-upload-output "output.csv" \
    --collection-report "collections_output.csv"
```

The script will provide detailed collection mapping diagnostics showing:
- Which folders were matched
- Which data items were included
- Any unmatched folders
- Collection creation status

### 2. Single Collection Creation
```bash
# Create a single collection
python nakala-client-collection.py \
    --api-key "your-key" \
    --title "fr:Collection Title|en:Collection Title" \
    --description "fr:Description|en:Description" \
    --keywords "fr:keywords|en:keywords" \
    --from-upload-output output.csv
```

### 3. Multilingual Dataset Upload and Collection
```bash
# Upload dataset with multilingual metadata
python nakala-client-upload.py \
    --mode folder \
    --dataset "multilingual_dataset/" \
    --folder-config "folder_data_items.csv" \
    --api-key "your-key"

# Create collections with multilingual metadata
python nakala-client-collection.py \
    --api-key "your-key" \
    --from-folder-collections "folder_collections.csv" \
    --from-upload-output "output.csv"
```

## Best Practices

### Data Organization
1. Use consistent folder structure:
   ```
   project/
   ├── files/
   │   ├── code/
   │   ├── data/
   │   ├── documents/
   │   ├── images/
   │   └── presentations/
   ├── folder_data_items.csv
   └── folder_collections.csv
   ```
2. Include comprehensive metadata in both French and English
3. Validate files before upload
4. Use appropriate file formats

### Metadata Management
1. Include multilingual descriptions (fr|en format)
2. Add relevant keywords in both languages
3. Specify proper licenses (CC-BY-4.0, CC-BY-NC-4.0, etc.)
4. Document authorship and contributions
5. Include coverage and relations

### Collection Organization
1. Create logical hierarchies based on content type
2. Use descriptive bilingual titles
3. Include relevant multilingual keywords
4. Set appropriate access rights
5. Maintain consistent metadata across collections

### Collection Relationships
1. Define clear relationships between collections
2. Use appropriate relation types
3. Document project associations
4. Maintain consistent coverage information
5. Link related collections through metadata 