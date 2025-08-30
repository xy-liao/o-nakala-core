# Best Practices for O-Nakala Core

This guide compiles proven best practices for efficient, reliable, and scalable research data management using O-Nakala Core, based on lessons learned from production environments.

## Overview

These best practices emerge from extensive real-world usage across digital humanities institutions, research libraries, and academic organizations. They focus on maximizing success rates while minimizing complexity and maintenance overhead.

## Project Organization Best Practices

### File Structure Organization

#### Recommended Directory Structure
```
research_project/
├── raw_data/           # Original, unmodified source files
├── processed_data/     # Cleaned and analyzed data
├── documentation/      # Research protocols and methodology  
├── scripts/           # Analysis and processing code
├── outputs/           # Results, figures, publications
├── metadata/          # CSV files for NAKALA upload
├── backup/            # Local backups before upload
└── nakala_results/    # Upload results and logs
```

#### File Naming Conventions
```bash
# Use consistent, descriptive naming
survey_data_2024-03-15.csv          # Good: includes date
interview_transcript_participant_01.pdf  # Good: clear identification
analysis_script_v2.py               # Good: version indicated

# Avoid problematic names  
data.csv                            # Bad: too generic
file (1).pdf                       # Bad: spaces and special chars
temp123.txt                         # Bad: non-descriptive
```

### CSV Metadata Preparation

#### Essential Field Standards
```csv
# Minimum viable metadata (always include)
file,status,type,title,creator,date,license,description

# Enhanced metadata (recommended)
file,status,type,title,alternative,creator,contributor,date,license,description,keywords,language,temporal,spatial,accessRights,identifier,rights
```

#### Metadata Quality Guidelines
1. **Consistent Creator Format**: "Last,First" or "Last,First;Last2,First2"
2. **Standard Date Format**: ISO 8601 (YYYY-MM-DD) 
3. **Descriptive Titles**: Include context, not just filenames
4. **Meaningful Keywords**: Use semicolon-separated, controlled vocabulary
5. **Complete Descriptions**: 1-3 sentences explaining content and context

## Workflow Best Practices

### Pre-Upload Phase

#### Always Preview First
```bash
# Interactive validation - catches 90% of issues
o-nakala-preview --csv folder_data_items.csv --interactive

# Batch validation for large datasets
o-nakala-preview --csv folder_data_items.csv --validate-only --json-output validation_report.json
```

#### File Validation Checklist
- [ ] All files exist and are accessible
- [ ] File permissions allow reading (chmod 644 for files, 755 for directories)
- [ ] No special characters in filenames (avoid spaces, accents, symbols)
- [ ] File sizes are reasonable (<500MB per file for optimal performance)
- [ ] Backup of original data created

### Upload Phase

#### Optimal Upload Configuration
```bash
# Production-tested settings
o-nakala-upload \
  --dataset folder_data_items.csv \
  --mode folder \
  --base-path . \
  --output upload_results.csv \
  --timeout 300 \
  --max-retries 3 \
  --verbose
```

#### Batch Processing Strategy
```bash
# For large datasets (100+ files), split into batches
split -l 50 large_dataset.csv batch_
for batch in batch_*; do
    echo "Processing $batch..."
    o-nakala-upload --dataset $batch --output results_$batch.csv
    sleep 60  # Rate limiting
done
```

### Post-Upload Phase

#### Immediate Verification
```bash
# Verify upload completeness
upload_count=$(grep -c "success" upload_results.csv)
total_count=$(tail -n +2 folder_data_items.csv | wc -l)
echo "Uploaded: $upload_count / $total_count"

# Check for errors
grep "error\|failed" upload_results.csv || echo "All uploads successful"
```

#### Collection Organization
```bash
# Create logical collections immediately after upload
o-nakala-collection \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv
```

## Performance Optimization

### Network Optimization

#### Connection Management
```bash
# Set optimal timeout values
export NAKALA_TIMEOUT=300          # 5 minutes per request
export NAKALA_MAX_RETRIES=5        # Reasonable retry limit
export NAKALA_RETRY_DELAY=30       # 30 seconds between retries
```

#### Bandwidth Considerations
- **Peak Hours**: Avoid 9 AM - 5 PM European time for large uploads
- **File Size Limits**: Split files >100MB into smaller chunks when possible
- **Concurrent Operations**: Limit to 1-2 simultaneous uploads per API key

### Memory and Storage Management

#### Efficient File Processing
```bash
# Process files in chunks for large datasets
find data/ -name "*.csv" -print0 | xargs -0 -n 10 -P 2 process_batch.sh

# Clean temporary files regularly
find /tmp -name "o-nakala-*" -mtime +1 -delete
```

#### Monitoring Resource Usage
```bash
# Check available resources before large operations
check_resources() {
    echo "Disk space:"
    df -h . | tail -n 1
    echo "Memory usage:"
    free -h | grep Mem
    echo "System load:"
    uptime
}
```

## Quality Assurance Best Practices

### Metadata Quality Control

#### Systematic Validation
```bash
# Multi-stage validation process
validation_pipeline() {
    local csv_file=$1
    
    echo "Stage 1: Format validation"
    o-nakala-preview --csv $csv_file --validate-only || return 1
    
    echo "Stage 2: Content validation"
    python validate_metadata_content.py $csv_file || return 1
    
    echo "Stage 3: Completeness check"
    o-nakala-curator --validate-completeness --csv $csv_file || return 1
    
    echo "All validation stages passed"
}
```

#### Quality Metrics Tracking
```bash
# Generate quality reports
o-nakala-curator \
  --quality-report \
  --scope all \
  --output quality_metrics_$(date +%Y%m%d).csv

# Track improvement over time
python analyze_quality_trends.py quality_metrics_*.csv
```

### Error Prevention

#### Common Pitfall Avoidance
1. **File Path Issues**: Always use relative paths from base directory
2. **Encoding Problems**: Ensure UTF-8 encoding for all CSV files
3. **API Key Management**: Never commit API keys to version control
4. **Resource Type Confusion**: Use COAR resource type URIs consistently
5. **Collection Naming**: Avoid special characters in collection names

#### Proactive Monitoring
```bash
# Set up automated health checks
health_check() {
    echo "Checking API connectivity..."
    curl -f -H "X-API-KEY: $NAKALA_API_KEY" $NAKALA_API_URL/users/me
    
    echo "Checking local file accessibility..."
    find . -name "*.csv" ! -readable -print
    
    echo "Checking metadata format..."
    for csv in *.csv; do
        o-nakala-preview --csv $csv --validate-only --quiet || echo "WARNING: $csv has issues"
    done
}
```

## Security and Access Management

### API Key Security
```bash
# Store API keys securely
echo "NAKALA_API_KEY=your-key-here" >> ~/.env
export $(grep -v '^#' ~/.env | xargs)

# Never log API keys
sed 's/api-key [^ ]*/api-key [REDACTED]/g' upload.log > sanitized.log
```

### Access Rights Management
```bash
# Set appropriate access levels
o-nakala-collection \
  --set-access-rights "open" \
  --for-collection "research_data_2024"

# Review permissions regularly  
o-nakala-user-info --api-key $NAKALA_API_KEY --permissions-report
```

## Documentation and Maintenance

### Record Keeping

#### Upload Documentation
```bash
# Create upload summary
cat > upload_summary_$(date +%Y%m%d).md << EOF
# Upload Summary $(date)

## Dataset Information
- CSV File: $CSV_FILE
- Total Files: $TOTAL_FILES
- Upload Date: $(date)
- API Endpoint: $NAKALA_API_URL

## Results
- Successful: $SUCCESS_COUNT
- Failed: $FAILED_COUNT
- Collections Created: $COLLECTION_COUNT

## Quality Metrics
- Average Completeness: $AVG_COMPLETENESS%
- Metadata Fields: $FIELD_COUNT

## Notes
$UPLOAD_NOTES
EOF
```

#### Change Tracking
```bash
# Version control for metadata
git init metadata_history/
cp *.csv metadata_history/
cd metadata_history/
git add *.csv
git commit -m "Metadata version $(date +%Y%m%d_%H%M%S)"
```

### Maintenance Schedules

#### Daily Tasks
- Check upload logs for errors
- Verify API key validity  
- Monitor storage usage
- Review recent quality metrics

#### Weekly Tasks  
- Generate comprehensive quality reports
- Update metadata standards documentation
- Review and clean temporary files
- Test backup and recovery procedures

#### Monthly Tasks
- Analyze workflow performance trends
- Update best practices documentation
- Review and optimize batch processing scripts
- Conduct comprehensive security audit

## Team and Institutional Best Practices

### Multi-User Workflows

#### Role-Based Responsibilities
- **Data Collectors**: File organization and initial metadata
- **Metadata Specialists**: Quality control and enhancement
- **Technical Staff**: Upload execution and error resolution
- **Project Managers**: Workflow oversight and reporting

#### Collaboration Tools
```bash
# Shared configuration management
git clone institutional_nakala_config.git
source institutional_nakala_config/setup.sh

# Standardized project templates
cp -r /shared/nakala_templates/basic_research_project ./
```

### Institutional Standards

#### Metadata Standardization
- Use institutional controlled vocabulary
- Implement consistent creator authority records
- Standardize collection naming conventions
- Apply uniform licensing and rights statements

#### Workflow Documentation
- Maintain institutional workflow guides
- Document local customizations and extensions
- Create training materials for new team members
- Establish quality assurance procedures

## Troubleshooting and Support

### Self-Service Diagnostics
```bash
# Automated troubleshooting script
troubleshoot() {
    echo "=== O-Nakala Core Diagnostics ==="
    
    echo "1. Environment Check:"
    python --version
    pip show o-nakala-core
    
    echo "2. API Connectivity:"
    curl -H "X-API-KEY: $NAKALA_API_KEY" $NAKALA_API_URL/users/me
    
    echo "3. File System Check:"
    ls -la *.csv 2>/dev/null || echo "No CSV files found"
    
    echo "4. Recent Errors:"
    grep -i error *.log 2>/dev/null | tail -5
}
```

### Escalation Procedures
1. **Level 1**: Self-service using troubleshooting guides
2. **Level 2**: Consult institutional documentation and team
3. **Level 3**: Review official documentation and examples
4. **Level 4**: Contact NAKALA platform support
5. **Level 5**: Report issues to O-Nakala Core project

## Continuous Improvement

### Performance Monitoring
```bash
# Track workflow performance
track_performance() {
    local start_time=$(date +%s)
    
    # Execute workflow
    o-nakala-upload --dataset $1 --output results.csv
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo "Workflow completed in $duration seconds" >> performance.log
}
```

### Knowledge Sharing
- Document lessons learned from each project
- Share successful configurations and scripts
- Contribute improvements back to the community
- Participate in user forums and discussions

These best practices provide a foundation for reliable, efficient, and scalable research data management with O-Nakala Core. Regular review and adaptation of these practices ensures continued success as projects grow and requirements evolve.