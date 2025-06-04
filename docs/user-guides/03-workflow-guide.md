# Complete Workflow Guide

## Digital Humanities Research Workflow

### Step 1: Organize Your Data
- Create folder structure by content type
- Prepare metadata CSV files
- Validate file formats

### Step 2: Upload Dataset
```bash
python nakala-client-upload.py --mode folder \
    --dataset "research_project_2024/" \
    --folder-config "research_config.csv" \
    --api-key "your-key"
```

### Step 3: Create Collections
```bash
python nakala-client-collection.py \
    --from-upload-output output.csv \
    --title "Research Project 2024"
```

### Step 4: Verify and Publish
- Check upload results in output.csv
- Verify collection creation
- Update status from private to public

## Common Workflows

### 1. Single Dataset Upload
```bash
# Upload a single dataset
python nakala-client-upload.py \
    --mode csv \
    --dataset dataset.csv \
    --image-dir images/ \
    --api-key "your-key"
```

### 2. Hierarchical Collection Creation
```bash
# Create main collection
python nakala-client-collection.py \
    --title "Research Project 2024" \
    --from-upload-output output.csv

# Create sub-collections by file type
python nakala-client-collection.py \
    --title "Research Data" \
    --data-ids "specific,data,ids" \
    --keywords "data,analysis"
```

### 3. Multilingual Dataset Upload
```bash
# Upload dataset with multilingual metadata
python nakala-client-upload.py \
    --mode folder \
    --dataset "multilingual_dataset/" \
    --folder-config "multilingual_config.csv" \
    --api-key "your-key"
```

## Best Practices

### Data Organization
1. Use consistent folder structure
2. Include comprehensive metadata
3. Validate files before upload
4. Use appropriate file formats

### Metadata Management
1. Include multilingual descriptions
2. Add relevant keywords
3. Specify proper licenses
4. Document authorship

### Collection Organization
1. Create logical hierarchies
2. Use descriptive titles
3. Include relevant keywords
4. Set appropriate access rights 