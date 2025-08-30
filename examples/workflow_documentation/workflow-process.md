# Complete Workflow Process

This document outlines the complete O-Nakala Core workflow methodology proven in production environments.

## Overview

The O-Nakala Core workflow transforms research files and folders into organized, discoverable, and preserved digital assets in the NAKALA repository.

## Stage 1: Preparation (5-15 minutes)

### File Organization
```bash
# Organize your files in a clear structure
research_project/
├── data/
├── documents/
├── images/
├── code/
└── presentations/
```

### CSV Creation
Create metadata CSV files describing your data:

```csv
file,status,type,title,creator,date,license,description
data/results.csv,pending,dataset,"Research Results","Smith,Jane","2024-01-15",CC-BY-4.0,"Analysis results from study"
```

## Stage 2: Validation (5-10 minutes)

### Preview and Test
```bash
# Validate metadata and preview before upload
o-nakala-preview --csv folder_data_items.csv --interactive

# Check file accessibility  
o-nakala-preview --csv folder_data_items.csv --validate-files
```

### Quality Checks
- Verify all files exist and are accessible
- Confirm metadata completeness
- Test resource type mappings
- Validate license specifications

## Stage 3: Upload (10-30 minutes)

### API Configuration
```bash
# Set environment variables
export NAKALA_API_KEY="your-api-key"
export NAKALA_API_URL="https://apitest.nakala.fr"  # or production
```

### Execute Upload
```bash
# Upload with progress tracking
o-nakala-upload \
  --dataset folder_data_items.csv \
  --mode folder \
  --base-path . \
  --output upload_results.csv
```

## Stage 4: Organization (5-15 minutes)

### Create Collections
```bash
# Organize uploaded data into collections
o-nakala-collection \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv
```

### Hierarchy Setup
- Group related data items
- Create logical collection structures
- Apply consistent naming conventions

## Stage 5: Quality Assurance (10-20 minutes)

### Quality Analysis
```bash
# Generate quality reports
o-nakala-curator \
  --quality-report \
  --scope all \
  --output quality_analysis.csv
```

### Validation Steps
- Check metadata completeness scores
- Verify collection organization
- Test access permissions
- Validate preservation metadata

## Stage 6: Publication (5-10 minutes)

### Status Updates
```bash
# Update status from pending to published
o-nakala-curator \
  --update-status published \
  --scope collections
```

### Final Verification
- Test public accessibility
- Verify persistent identifiers
- Check citation formats
- Confirm discovery metadata

## Success Metrics

### Completeness Indicators
- ✅ All files successfully uploaded
- ✅ Collections properly organized  
- ✅ Metadata quality scores >80%
- ✅ No validation errors
- ✅ Public access functional

### Performance Benchmarks
- **Small datasets** (1-50 files): 15-30 minutes total
- **Medium datasets** (51-200 files): 30-60 minutes total  
- **Large datasets** (200+ files): 1-3 hours total

## Error Recovery

### Common Issues
1. **File upload failures**: Check file permissions and network connectivity
2. **Metadata validation errors**: Review CSV format and required fields
3. **API timeout issues**: Reduce batch sizes and retry
4. **Collection creation failures**: Verify collection naming conventions

### Recovery Procedures
```bash
# Resume failed uploads
o-nakala-upload --resume upload_results.csv

# Fix metadata issues
o-nakala-preview --csv corrected_metadata.csv --validate

# Retry collection creation
o-nakala-collection --retry-failed collection_results.csv
```

## Next Steps

- **Production deployment**: [Institutional Setup Guide](institutional-setup.md)
- **Large-scale processing**: [Batch Processing Guide](batch-processing.md)
- **Quality optimization**: [Best Practices Guide](best-practices.md)