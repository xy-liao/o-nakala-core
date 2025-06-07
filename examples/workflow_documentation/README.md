# Complete O-Nakala Core Workflow Documentation

This directory documents a complete data lifecycle workflow using O-Nakala Core, from initial upload through collection organization to metadata curation.

## Workflow Overview

This example demonstrates the full capabilities of O-Nakala Core by processing a sample research dataset through all phases of digital repository management:

1. **Data Upload** - Batch upload of research files organized by type
2. **Collection Creation** - Automatic organization into thematic collections
3. **Quality Analysis** - Comprehensive metadata validation and reporting
4. **Batch Curation** - Systematic metadata enhancement and corrections

## Results Summary

### 📊 Processing Statistics
- **Files Processed**: 14 individual files across 5 content categories
- **Datasets Created**: 5 organized data items
- **Collections Created**: 3 thematic collections
- **Metadata Enhancements**: 8 batch modification operations
- **Success Rate**: 100% for all operations
- **Languages**: Full bilingual support (French/English)

### 🏷️ Generated Identifiers
**Data Items:**
- Images: `10.34847/nkl.bf0fxt5e`
- Code: `10.34847/nkl.181eqe75`
- Presentations: `10.34847/nkl.9edeiw5z`
- Documents: `10.34847/nkl.2b617444`
- Data: `10.34847/nkl.5f40fo9t`

**Collections:**
- Code and Data: `10.34847/nkl.adfc67q4`
- Documents: `10.34847/nkl.d8328982`
- Multimedia: `10.34847/nkl.1c39i9oq`

## File Structure

```
workflow_documentation/
├── README.md                           # This overview document
├── 01_setup_and_environment/
│   ├── environment_setup.md            # API configuration and authentication
│   └── successful_commands.sh          # Validated command sequences
├── 02_data_upload/
│   ├── upload_workflow.md              # Upload process documentation
│   ├── folder_data_items.csv           # Source configuration
│   └── upload_output.csv               # Results and identifiers
├── 03_collection_creation/
│   ├── collection_workflow.md          # Collection creation process
│   ├── folder_collections.csv          # Collection definitions
│   └── collections_output.csv          # Created collection details
├── 04_quality_analysis/
│   ├── quality_analysis.md             # Quality assessment process
│   └── quality_report_summary.json     # Key findings and recommendations
├── 05_metadata_curation/
│   ├── curation_workflow.md            # Batch modification process
│   ├── data_modifications.csv          # Data item enhancements
│   ├── collection_modifications.csv    # Collection enhancements
│   └── modification_results.md         # Applied changes summary
└── 06_validation_and_results/
    ├── final_validation.md             # Post-curation validation
    └── workflow_summary.md             # Complete process overview
```

## Quick Start Commands

For users who want to replicate this workflow:

```bash
# 1. Set environment
export NAKALA_API_KEY="your-test-api-key"
export NAKALA_BASE_URL="https://apitest.nakala.fr"

# 2. Install O-Nakala Core
pip install -e .

# 3. Upload data
nakala-upload --api-key "$NAKALA_API_KEY" \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path .

# 4. Create collections
nakala-collection --api-key "$NAKALA_API_KEY" \
  --from-upload-output output.csv \
  --from-folder-collections folder_collections.csv

# 5. Generate quality report
nakala-curator --api-key "$NAKALA_API_KEY" --quality-report

# 6. Apply metadata enhancements
nakala-curator --api-key "$NAKALA_API_KEY" \
  --batch-modify data_modifications.csv \
  --scope datasets

nakala-curator --api-key "$NAKALA_API_KEY" \
  --batch-modify collection_modifications.csv \
  --scope collections
```

## Key Learnings

### ✅ What Works Well
- **Folder-based uploads** with proper CSV configuration
- **Automatic collection organization** based on folder patterns
- **Batch metadata modifications** with proper field naming
- **Multilingual support** throughout the workflow
- **Quality validation** before and after modifications

### ⚠️ Important Considerations
- **API Key Security**: Always use test keys for development
- **Field Validation**: Collection 'creator' field requires special handling
- **CSV Format**: Batch modifications require specific column naming (e.g., 'new_keywords')
- **Dry Run Testing**: Always test modifications with --dry-run first

### 🔄 Recommended Workflow
1. Start with well-structured source data and clear folder organization
2. Use CSV configurations for reproducible, documented processes
3. Validate uploads immediately after creation
4. Apply metadata enhancements systematically with batch operations
5. Generate final quality reports to confirm improvements

## Support and Documentation

- **Field Reference**: Use `nakala-curator --list-fields` for complete field documentation
- **Command Help**: All commands support `--help` for detailed usage
- **Test Environment**: Always use NAKALA test API for development and learning

---

*This documentation was generated from a successful end-to-end workflow executed on 2025-06-08 using O-Nakala Core v2.0.0*