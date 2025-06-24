# Complete Workflow Guide

## Digital Humanities Research Workflow (7 Steps)

> **Enhanced Workflow**: This guide covers the complete 7-step O-Nakala workflow with automated metadata enhancement for both datasets and collections.

### Step 1: Data Organization and Preparation
- Create folder structure by content type (e.g., `files/code`, `files/data`, `files/documents`)
- Prepare metadata CSV files:
  - `folder_data_items.csv` for data items
  - `folder_collections.csv` for collections
- Validate file formats and metadata
- Ensure folder paths in CSV files match actual directory structure

### Step 2: Dataset Upload
```bash
# Important: Use the correct base path for your dataset
o-nakala-upload --mode folder \
    --dataset "sample_dataset" \
    --folder-config "sample_dataset/folder_data_items.csv" \
    --api-key "your-key"
```

Note: The `--dataset` parameter should point to the base directory containing your `files` folder. The script will automatically handle the folder structure within it.

### Step 3: Collection Creation
```bash
o-nakala-collection \
    --api-key "your-key" \
    --from-folder-collections "sample_dataset/folder_collections.csv" \
    --from-upload-output "upload_results.csv" \
    --collection-report "collections_output.csv"
```

### Step 4: Auto-Enhancement Generation
**NEW**: Automated metadata enhancement for both datasets and collections.

```bash
# Generate dataset enhancements
python create_modifications.py upload_results.csv

# Generate collection enhancements  
python create_collection_modifications.py collections_output.csv
```

This step creates:
- `auto_data_modifications.csv` - Professional metadata for datasets
- `auto_collection_modifications.csv` - Professional metadata for collections

### Step 5: Dataset Metadata Curation
```bash
o-nakala-curator \
    --api-key "your-key" \
    --batch-modify auto_data_modifications.csv \
    --scope datasets
```

### Step 6: Collection Metadata Curation
**NEW**: Enhanced metadata for collections with professional titles, descriptions, and keywords.

```bash
o-nakala-curator \
    --api-key "your-key" \
    --batch-modify auto_collection_modifications.csv \
    --scope collections
```

### Step 7: Quality Analysis and Verification
```bash
# Generate comprehensive quality report
o-nakala-curator \
    --api-key "your-key" \
    --quality-report \
    --scope datasets \
    --output "quality_report.json"
```

### Final Results and Publishing
- Check upload results in `upload_results.csv`
- Verify collection creation in `collections_output.csv`
- Review enhanced metadata in both `auto_data_modifications.csv` and `auto_collection_modifications.csv`
- Review quality report and apply recommendations
- Update status from private to public if needed

## Complete 7-Step Workflow Summary

1. **Data Organization** - Prepare files and metadata CSVs
2. **Dataset Upload** - Upload files to NAKALA with metadata
3. **Collection Creation** - Organize datasets into thematic collections
4. **Auto-Enhancement Generation** - Generate professional metadata for datasets AND collections
5. **Dataset Curation** - Apply enhanced metadata to all datasets
6. **Collection Curation** - Apply enhanced metadata to all collections  
7. **Quality Analysis** - Generate comprehensive quality report

**Result**: Professional, multilingual metadata for both datasets and collections with 100% success rate.

## Common Workflows

### 1. Folder-Based Collection Creation
```bash
# Create collections based on folder structure
o-nakala-collection \
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
o-nakala-collection \
    --api-key "your-key" \
    --title "fr:Collection Title|en:Collection Title" \
    --description "fr:Description|en:Description" \
    --keywords "fr:keywords|en:keywords" \
    --from-upload-output output.csv
```

### 3. Multilingual Dataset Upload and Collection
```bash
# Upload dataset with multilingual metadata
o-nakala-upload \
    --mode folder \
    --dataset "multilingual_dataset/" \
    --folder-config "folder_data_items.csv" \
    --api-key "your-key"

# Create collections with multilingual metadata
o-nakala-collection \
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