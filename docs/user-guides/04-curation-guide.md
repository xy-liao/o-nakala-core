# Curation Guide

Metadata curation and quality management tools for NAKALA data repositories.

## Overview

O-Nakala Core provides comprehensive metadata curation capabilities to help improve data quality through validation, batch modifications, and quality reporting.

## Quick Start

### Installation
```bash
# Standard installation includes curation tools
pip install o-nakala-core[cli]
```

### Basic Curation Workflow
```bash
# Generate quality report
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --scope all \
  --output quality_report.json

# Validate metadata
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --validate-metadata \
  --scope collections

# Detect potential duplicates
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --detect-duplicates \
  --collections collection_id_1,collection_id_2
```

## Core Features

### 1. Quality Reporting

Generate comprehensive reports about your metadata quality.

**What it analyzes:**
- Required field completeness
- Metadata consistency across items
- Field format validation
- License and permission compliance

**Usage:**
```bash
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --scope all \
  --output quality_report.json
```

### 2. Metadata Validation

Validate metadata against NAKALA requirements before publication.

**Validation checks:**
- Required fields presence
- Field format compliance
- URI and link validity
- Language code validation

**Usage:**
```bash
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --validate-metadata \
  --scope collections
```

### 3. Batch Modifications

Apply metadata changes to multiple items using CSV files.

**Supported modifications:**
- Update titles, descriptions, keywords
- Change licenses and permissions
- Modify creator and contributor information
- Update dates and temporal coverage

**Workflow:**
```bash
# 1. Export template for your items
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --export-template modifications_template.csv \
  --collections collection_id

# 2. Edit the CSV file with your changes

# 3. Apply modifications (dry run first)
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify modifications.csv \
  --dry-run

# 4. Apply actual modifications
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify modifications.csv
```

### 4. Duplicate Detection

Identify potential duplicate items in your collections.

**Detection methods:**
- Title similarity analysis
- File hash comparison
- Metadata pattern matching
- Manual review recommendations

**Usage:**
```bash
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --detect-duplicates \
  --collections collection_id_1,collection_id_2 \
  --output duplicates_report.json
```

## Complete Workflow Example

### End-to-End Curation Process
```bash
# 1. Upload your data
o-nakala-upload \
  --api-key "$NAKALA_API_KEY" \
  --dataset folder_data_items.csv \
  --mode folder \
  --base-path ./my_dataset \
  --output upload_results.csv

# 2. Create collections
o-nakala-collection \
  --api-key "$NAKALA_API_KEY" \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv

# 3. Generate quality report
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --scope all \
  --output quality_report.json

# 4. Export modification template
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --export-template modifications.csv \
  --collections collection_id

# 5. Apply batch modifications
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify modifications.csv \
  --dry-run
```

## Quality Report Output

The quality report provides structured analysis in JSON format:

```json
{
  "summary": {
    "total_items": 150,
    "collections": 5,
    "validation_errors": 12,
    "missing_required_fields": 8
  },
  "field_analysis": {
    "title": {"complete": 148, "missing": 2},
    "description": {"complete": 140, "missing": 10},
    "creator": {"complete": 145, "missing": 5}
  },
  "recommendations": [
    "Complete missing titles for 2 items",
    "Add descriptions for 10 items",
    "Validate 3 items with invalid date formats"
  ]
}
```

## Field Reference

The curator supports all standard NAKALA metadata fields. Use `--list-fields` to see complete field documentation:

```bash
o-nakala-curator --list-fields
```

## Troubleshooting

### Common Issues

**"API authentication failed"**
```bash
# Verify your API key is correct
export NAKALA_API_KEY="your_api_key_here"
o-nakala-curator --api-key "$NAKALA_API_KEY" --quality-report
```

**"Collection not found"**
```bash
# List your collections first
o-nakala-user-info --api-key "$NAKALA_API_KEY" --collections-only
```

**"Batch modification failed"**
```bash
# Always test with dry-run first
o-nakala-curator --batch-modify modifications.csv --dry-run

# Check CSV format matches field requirements
o-nakala-curator --list-fields
```

### Performance Tips

```bash
# For large datasets, use smaller batch sizes
o-nakala-curator \
  --batch-modify modifications.csv \
  --batch-size 25

# Use scoped operations for better performance
o-nakala-curator \
  --quality-report \
  --scope collections \
  --collections specific_collection_id
```

## Best Practices

### 1. Test Before Production
- Always use `--dry-run` for batch modifications
- Generate quality reports before making changes
- Validate metadata before publishing

### 2. Regular Maintenance
- Run quality reports periodically
- Check for duplicates after major uploads
- Update metadata as standards evolve

### 3. Batch Processing
- Use CSV templates for consistent formatting
- Process related items together
- Keep modification records for audit trails

### 4. Field Management
- Use `--list-fields` to understand field requirements
- Follow NAKALA metadata schemas
- Validate URI formats for linked data

## Related Documentation

- [Curator Field Reference](../curator-field-reference.md) - Complete field documentation
- [Workflow Guide](03-workflow-guide.md) - End-to-end processes
- [API Endpoints](../endpoints/) - Technical specifications
- [Troubleshooting](05-troubleshooting.md) - Common questions and problem solving

## 📚 Official NAKALA Resources

### **Metadata Standards & Quality**
- **[Metadata Description Guide](https://documentation.huma-num.fr/nakala-guide-de-description/)** - Official Dublin Core specifications for NAKALA
- **[Data Preparation Guide](https://documentation.huma-num.fr/nakala-preparer-ses-donnees/)** - Best practices for research data quality
- **[Official NAKALA Documentation](https://documentation.huma-num.fr/nakala/)** - Complete platform standards

### **Quality Assurance**
- **[NAKALA User Manual](https://documentation.huma-num.fr/nakala/)** - Official best practices
- **[Test API Documentation](https://apitest.nakala.fr/doc)** - Validate metadata via API
- **[NAKALA Test Platform](https://test.nakala.fr)** - Safe environment for quality testing with sample data

---

**The curation tools provide systematic metadata management for research data repositories, ensuring quality and consistency across your NAKALA collections.**