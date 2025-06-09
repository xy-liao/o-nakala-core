# V2.0 Migration Guide

## Overview

This guide helps you migrate from the original Nakala client scripts (v1.0) to the new improved v2.0 architecture while maintaining full backward compatibility.

## 🔄 Migration Strategy

### Phase 1: Parallel Operation (Current)
- Both v1.0 and v2.0 scripts work simultaneously
- Same configuration files and datasets
- Identical CLI interfaces and output formats
- Zero breaking changes

### Phase 2: Testing & Validation
- Test v2.0 scripts with your existing datasets
- Compare outputs between v1.0 and v2.0
- Validate all workflows work correctly

### Phase 3: Gradual Migration
- Start using v2.0 scripts for new projects
- Continue using v1.0 for critical production workflows
- Migrate when confident in v2.0 stability

## 📋 Key Differences

### Improved Error Handling
**V1.0 Behavior:**
```python
# Basic error handling
try:
    result = upload_file()
except Exception as e:
    print(f"Error: {e}")
```

**V2.0 Behavior:**
```python
# Comprehensive error handling with context
try:
    result = upload_file()
except NakalaAPIError as e:
    logger.error(f"API Error: {e.message} (Status: {e.status_code})")
except FileValidationError as e:
    logger.error(f"File Error: {e.message} (File: {e.filename})")
```

### Enhanced Logging
**V1.0:** Basic print statements
```bash
Processing file: image.jpg
Upload complete
```

**V2.0:** Structured logging with context
```bash
2024-01-15 10:30:15 - INFO - Processing dataset 1/5: "Bird Photography"
2024-01-15 10:30:16 - INFO - Uploading file 1/2: image.jpg (1.2MB)
2024-01-15 10:30:18 - INFO - File uploaded successfully: sha1=abc123...
2024-01-15 10:30:19 - INFO - Creating dataset with 2 files and 8 metadata fields
2024-01-15 10:30:20 - SUCCESS - Dataset created: 10.34847/nkl.xyz789
```

### Validation Improvements
**V2.0 adds:**
- File existence validation before upload attempts
- Metadata field validation against Nakala schema
- Configuration file validation
- CSV format validation
- Network connectivity checks

## 🚀 Migration Steps

### Step 1: Test V2.0 Scripts

Test the new scripts with your existing data:

```bash
# Test upload script
nakala-upload \
  --api-key YOUR_KEY \
  --dataset your_existing_dataset.csv \
  --folder-config your_existing_config.csv \
  --mode folder

# Test collection script  
nakala-collection \
  --api-key YOUR_KEY \
  --from-folder-collections your_collections.csv \
  --from-upload-output output.csv
```

### Step 2: Compare Outputs

Compare the outputs between v1.0 and v2.0:

```bash
# Run both versions
python nakala-client-upload.py [args] > output_v1.csv
nakala-upload [args] > output_v2.csv

# Compare results
diff output_v1.csv output_v2.csv
```

### Step 3: Update Scripts Gradually

Start updating your automation scripts:

```bash
# Instead of:
python nakala-client-upload.py --api-key $KEY --dataset data.csv

# Use:
nakala-upload --api-key $KEY --dataset data.csv
```

## 📊 Configuration Compatibility

### Environment Files
Your existing `.env` files work with both versions:

```bash
# .env (works with both v1.0 and v2.0)
NAKALA_API_KEY=your-api-key
NAKALA_API_URL=https://apitest.nakala.fr
DEFAULT_FOLDER_PATH=./datasets
DEFAULT_OUTPUT_PATH=./output
```

### CSV Data Files
All existing CSV files work unchanged:

```csv
# folder_data_items.csv (compatible with both versions)
folder,status,type,title,author,date,license,description,keywords,rights
bird_photos,pending,http://purl.org/coar/resource_type/c_c513,...
```

## 🔧 Advanced Features in V2.0

### 1. Enhanced Configuration
```python
# V2.0 supports structured configuration
from nakala_client.common.config import NakalaConfig

config = NakalaConfig()
config.validate()  # Comprehensive validation
```

### 2. Better Error Recovery
```bash
# V2.0 provides detailed error diagnostics
nakala-upload --debug --validate-only your_data.csv
```

### 3. Extensible Architecture
```python
# V2.0 provides reusable components for custom scripts
from nakala_client.common.utils import prepare_metadata, upload_files
from nakala_client.common.exceptions import NakalaAPIError
```

## 🎯 When to Migrate

### Immediate Migration Recommended For:
- **New projects** - Start with v2.0 for better experience
- **Development environments** - Test new features and improvements
- **Scripts with frequent errors** - Benefit from better error handling

### Gradual Migration For:
- **Production workflows** - Ensure stability before switching
- **Automated pipelines** - Test thoroughly in staging first
- **Large datasets** - Validate with smaller test batches

### Keep V1.0 For:
- **Critical production systems** - Until v2.0 is fully validated
- **Legacy integrations** - If migration cost is high
- **Emergency fallback** - V1.0 remains available as backup

## 🆘 Troubleshooting Migration

### Issue: V2.0 Script Not Found
```bash
# Solution: Install the package properly
pip install -e .
# or use full path
python /path/to/nakala-upload
```

### Issue: Different Outputs
```bash
# Check detailed logs
nakala-upload --debug [args]
# Compare with v1.0 behavior
```

### Issue: New Error Messages
V2.0 provides more detailed errors - this is normal and helpful:
```bash
# V1.0: "Upload failed"
# V2.0: "Upload failed: File 'image.jpg' not found in directory './images/'"
```

## 📞 Getting Help

1. **Documentation**: Check the [troubleshooting guide](../troubleshooting.md)
2. **Comparison Testing**: Run both versions side-by-side
3. **Gradual Migration**: Start with non-critical workflows
4. **Rollback Plan**: V1.0 scripts remain available for fallback

Remember: **There's no rush to migrate**. Both versions work simultaneously, so you can migrate at your own pace while ensuring everything works correctly.