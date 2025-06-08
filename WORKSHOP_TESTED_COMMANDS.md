# Workshop Tested Commands - O-Nakala Core

## ✅ Real API Testing Results

**Test Date:** 2025-06-08  
**API Key:** f41f5957-d396-3bb9-ce35-a4692773f636  
**Test Environment:** https://apitest.nakala.fr

## 🎯 Complete Working Workflow

### Environment Setup
```bash
# Required environment variables
export NAKALA_API_KEY="f41f5957-d396-3bb9-ce35-a4692773f636"
export PYTHONPATH=/Users/syl/Documents/GitHub/o-nakala-core

# Navigate to sample dataset
cd /Users/syl/Documents/GitHub/o-nakala-core/examples/sample_dataset
```

### 1. API Connection Test
```bash
python -m src.nakala_client.cli.user_info --verbose
```
**Result:** ✅ Connected successfully
- User: Utilisateur Nakala #2
- Collections: 115, Datasets: 442

### 2. Data Upload (14 Files → 5 Datasets)
```bash
python -m src.nakala_client.cli.upload \
  --api-key "$NAKALA_API_KEY" \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path . \
  --output workshop_upload_output.csv
```
**Result:** ✅ 100% Success
- Images: `10.34847/nkl.fb44hl62`
- Code: `10.34847/nkl.cff2x967`  
- Presentations: `10.34847/nkl.1b5dzn74`
- Documents: `10.34847/nkl.36be24x4`
- Data: `10.34847/nkl.490900a4`

### 3. Collection Creation (5 Datasets → 3 Collections)
```bash
python -m src.nakala_client.cli.collection \
  --api-key "$NAKALA_API_KEY" \
  --from-upload-output workshop_upload_output.csv \
  --from-folder-collections folder_collections.csv
```
**Result:** ✅ 100% Success
- Code and Data: `10.34847/nkl.9d9601xz`
- Documents: `10.34847/nkl.b6c5mr3o`
- Multimedia: `10.34847/nkl.7066ek9p`

### 4. Quality Analysis
```bash
python -m src.nakala_client.cli.curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --verbose
```
**Result:** ✅ Repository-wide analysis completed
- 387 collections analyzed, 841 datasets scanned
- Common issue: Missing creator fields identified

### 5. Batch Metadata Modifications

#### Collections Fix (Creator Fields)
```bash
python -m src.nakala_client.cli.curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify workshop_collection_fix_correct.csv \
  --dry-run \
  --verbose

# After validation, apply changes
python -m src.nakala_client.cli.curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify workshop_collection_fix_correct.csv \
  --verbose
```
**Result:** ✅ 3/3 collections updated successfully

## 📋 Required CSV Formats

### Upload Configuration (folder_data_items.csv)
```csv
file,status,type,title,alternative,author,contributor,date,license,description,keywords,language,temporal,spatial,accessRights,identifier,rights
files/code/,pending,http://purl.org/coar/resource_type/c_5ce6,fr:Fichiers de code|en:Code Files,...
```

### Collection Configuration (folder_collections.csv)
```csv
title,status,description,keywords,language,creator,contributor,publisher,date,rights,coverage,relation,source,data_items
"fr:Collection de Code et Données|en:Code and Data Collection",private,"fr:Collection contenant des scripts...",
```

### Batch Modifications (workshop_collection_fix_correct.csv)
```csv
id,action,new_creator
10.34847/nkl.9d9601xz,modify,"Doe, John;Smith, Jane"
10.34847/nkl.b6c5mr3o,modify,"Smith, Jane;Doe, John"
10.34847/nkl.7066ek9p,modify,"Smith, Jane;Doe, John"
```

## 🎓 Workshop Success Metrics

| Phase | Files/Items | Success Rate | Time |
|-------|-------------|--------------|------|
| Upload | 14 files | 100% | ~2 seconds |
| Collections | 3 collections | 100% | ~1 second |
| Quality Analysis | 387 collections | 100% | ~10 seconds |
| Batch Modifications | 3 updates | 100% | ~1 second |

## 🔧 Troubleshooting Tips

### Common Issues & Solutions

1. **Module Import Error**
   ```bash
   # Ensure PYTHONPATH is set correctly
   export PYTHONPATH=/Users/syl/Documents/GitHub/o-nakala-core
   ```

2. **CSV Format Issues**
   - Batch modifications require: `id`, `action`, `new_fieldname` columns
   - Use `modify` as action value
   - Field names must have `new_` prefix for modifications

3. **API Connection**
   - Verify API key is active: Test with user_info command
   - Check network connectivity to apitest.nakala.fr

## 🚀 Ready for Production

All CLI commands have been tested with real API calls and work reliably for workshop training scenarios. The system demonstrates:

- ✅ **Folder-mode uploads** with automatic file organization
- ✅ **Collection creation** from upload outputs  
- ✅ **Quality analysis** with comprehensive reporting
- ✅ **Batch modifications** with field-level updates
- ✅ **Multilingual metadata** support throughout
- ✅ **Error handling** and validation at each step

**Conclusion:** The O-Nakala Core system is ready for institutional workshops and training programs.