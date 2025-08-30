# Quality Assurance Guide

This document outlines comprehensive quality assurance procedures for O-Nakala Core workflows, ensuring reliable and reproducible research data management processes.

## Overview

Quality assurance in O-Nakala Core involves systematic validation at each stage of the workflow, from initial file preparation through final publication in NAKALA.

## Pre-Upload Quality Checks

### File Validation
```bash
# Check file accessibility and permissions
o-nakala-preview --csv folder_data_items.csv --validate-files

# Verify file integrity
find . -name "*.csv" -exec file {} \;
find . -name "*.pdf" -exec pdfinfo {} \; 2>/dev/null
```

### Metadata Quality Assessment
```bash
# Interactive metadata validation
o-nakala-preview --csv folder_data_items.csv --interactive

# Export validation report
o-nakala-preview --csv folder_data_items.csv --json-output validation_report.json
```

## Upload Quality Monitoring

### Progress Tracking
```bash
# Monitor upload with detailed logging
o-nakala-upload \
  --dataset folder_data_items.csv \
  --mode folder \
  --output upload_results.csv \
  --verbose

# Verify upload completeness
grep -c "success" upload_results.csv
grep "error\|failed" upload_results.csv
```

### Immediate Post-Upload Validation
```bash
# Check uploaded data integrity
o-nakala-user-info --api-key $NAKALA_API_KEY --collections-only

# Validate metadata preservation
o-nakala-curator --quality-report --scope recent --output qa_report.csv
```

## Collection Quality Control

### Organization Verification
```bash
# Verify collection structure
o-nakala-collection --from-upload-output upload_results.csv --dry-run

# Check collection metadata completeness
o-nakala-curator --quality-report --scope collections
```

### Cross-Collection Consistency
- Consistent naming conventions across collections
- Standardized metadata vocabulary usage
- Uniform rights and licensing specifications
- Proper hierarchical organization

## Metadata Quality Metrics

### Completeness Scores
- **Minimum Acceptable**: 60% metadata completeness
- **Good Practice**: 80% metadata completeness  
- **Excellence Standard**: 95% metadata completeness

### Required Field Validation
```bash
# Check essential metadata fields
o-nakala-curator --validate-required-fields --scope all

# Verify Dublin Core compliance
o-nakala-curator --dublin-core-check --output dc_validation.csv
```

### Language and Encoding Validation
- UTF-8 encoding verification for all text fields
- Language code consistency (ISO 639-1)
- Multilingual metadata support validation

## Automated Quality Assurance

### Continuous Integration Checks
```bash
#!/bin/bash
# qa_pipeline.sh - Automated QA pipeline

# Stage 1: Pre-upload validation
echo "Stage 1: Validating files and metadata..."
o-nakala-preview --csv $1 --validate-only || exit 1

# Stage 2: Test upload (dry run)
echo "Stage 2: Testing upload process..."
o-nakala-upload --dataset $1 --dry-run --api-key $TEST_API_KEY || exit 1

# Stage 3: Quality metrics
echo "Stage 3: Generating quality metrics..."
o-nakala-curator --quality-report --output qa_metrics.csv

echo "Quality assurance pipeline completed successfully!"
```

### Error Detection and Alerts
- File corruption detection
- Metadata format validation
- API response error monitoring
- Upload completeness verification

## Quality Assurance Checklist

### Pre-Upload Checklist
- [ ] All referenced files exist and are accessible
- [ ] CSV format validation passes
- [ ] Required metadata fields present
- [ ] File permissions correctly set
- [ ] Backup of original data created

### Upload Process Checklist
- [ ] API key valid and permissions confirmed
- [ ] Upload progress monitored
- [ ] Error logs reviewed
- [ ] Upload completeness verified
- [ ] Immediate validation performed

### Post-Upload Checklist
- [ ] All files successfully uploaded
- [ ] Metadata integrity preserved
- [ ] Collections properly organized
- [ ] Access permissions correctly set
- [ ] Quality metrics meet standards

### Publication Checklist
- [ ] Final quality review completed
- [ ] Persistent identifiers assigned
- [ ] Public accessibility verified
- [ ] Citation information complete
- [ ] Documentation updated

## Quality Metrics and Reporting

### Key Performance Indicators
- **Upload Success Rate**: >98% successful uploads
- **Metadata Completeness**: >80% average completeness
- **Error Recovery Time**: <24 hours for critical issues
- **User Satisfaction**: >4.5/5 documentation clarity rating

### Regular Quality Reports
```bash
# Weekly quality assessment
o-nakala-curator \
  --quality-report \
  --scope all \
  --time-range "7 days" \
  --output weekly_qa_report.csv

# Generate quality dashboard
python generate_qa_dashboard.py weekly_qa_report.csv
```

## Troubleshooting Quality Issues

### Common Quality Problems
1. **Incomplete Uploads**: Network interruptions, file permission issues
2. **Metadata Corruption**: Encoding problems, field mapping errors
3. **Collection Disorganization**: Naming conflicts, hierarchy errors
4. **Access Permission Problems**: Rights misconfiguration, user authorization issues

### Quality Recovery Procedures
```bash
# Resume failed uploads
o-nakala-upload --resume upload_results.csv

# Fix metadata issues
o-nakala-curator --repair-metadata --scope failed-items

# Reorganize collections
o-nakala-collection --reorganize --from-config collection_config.csv
```

## Best Practices for Quality Assurance

### Preventive Measures
1. **Standardized Workflows**: Use consistent processes across all projects
2. **Automated Validation**: Implement systematic checks at each stage
3. **Regular Backups**: Maintain copies of original data and configurations
4. **Documentation Updates**: Keep procedures current with library changes

### Continuous Improvement
- Regular workflow assessment and optimization
- User feedback integration for process improvement
- Tool and procedure updates based on lessons learned
- Knowledge sharing across research teams

## Integration with Institutional Workflows

### Large-Scale Quality Management
- Batch validation procedures for institutional datasets
- Multi-user quality assurance workflows
- Integration with institutional backup and archival systems
- Compliance with institutional data management policies

This quality assurance framework ensures reliable, reproducible research data management processes that maintain high standards throughout the complete O-Nakala Core workflow.