# Error Recovery Guide

This guide provides systematic approaches to recovering from errors and failures in O-Nakala Core workflows, ensuring minimal data loss and efficient problem resolution.

## Overview

Error recovery in O-Nakala Core focuses on identifying failure points, implementing recovery procedures, and preventing future issues through robust error handling strategies.

## Common Error Categories

### 1. Network and Connectivity Errors

#### Symptoms
- Connection timeouts during uploads
- API request failures
- Intermittent upload interruptions

#### Recovery Procedures
```bash
# Check API connectivity
curl -H "X-API-KEY: $NAKALA_API_KEY" $NAKALA_API_URL/users/me

# Resume interrupted uploads
o-nakala-upload --resume upload_results.csv --retry-failed

# Retry with increased timeouts
o-nakala-upload --dataset data.csv --timeout 300 --max-retries 5
```

### 2. File Access and Permission Errors

#### Symptoms
- "Permission denied" errors
- "File not found" messages
- Path resolution failures

#### Recovery Procedures
```bash
# Check file permissions
find . -name "*.csv" ! -perm -r-- -exec ls -la {} \;

# Fix permission issues
chmod -R 644 data_files/
chmod 755 data_directories/

# Verify file accessibility
o-nakala-preview --csv data.csv --validate-files
```

### 3. Metadata Validation Errors

#### Symptoms
- CSV format validation failures
- Required field missing errors
- Invalid metadata values

#### Recovery Procedures
```bash
# Identify metadata issues
o-nakala-preview --csv data.csv --validate-only --verbose

# Export detailed error report
o-nakala-preview --csv data.csv --error-report validation_errors.json

# Fix common metadata issues
python fix_metadata.py data.csv validation_errors.json
```

## Systematic Error Recovery Process

### Step 1: Error Identification and Assessment

```bash
# Capture complete error information
o-nakala-upload --dataset data.csv --verbose --log-file upload.log 2>&1

# Analyze error patterns
grep -i "error\|failed\|exception" upload.log

# Check system resources
df -h  # Check disk space
free -h  # Check memory usage
```

### Step 2: Immediate Recovery Actions

#### For Upload Failures
```bash
# Check upload progress
tail -f upload.log

# Identify failed items
grep "failed" upload_results.csv > failed_items.csv

# Retry failed uploads only
o-nakala-upload --retry-list failed_items.csv --api-key $NAKALA_API_KEY
```

#### For Metadata Errors
```bash
# Create backup of original metadata
cp original_data.csv backup_data_$(date +%Y%m%d_%H%M%S).csv

# Apply metadata fixes
python scripts/fix_common_errors.py original_data.csv > corrected_data.csv

# Validate corrections
o-nakala-preview --csv corrected_data.csv --validate-only
```

### Step 3: Comprehensive Recovery Validation

```bash
# Verify recovery completeness
python validate_recovery.py upload_results.csv failed_items.csv

# Run quality assurance checks
o-nakala-curator --quality-report --scope recovered-items

# Test complete workflow
o-nakala-preview --csv recovered_data.csv --interactive
```

## Specific Error Recovery Scenarios

### Scenario 1: Partial Upload Failure

**Problem**: Upload stops at 60% completion due to network timeout

**Recovery Process**:
```bash
# 1. Assess current state
grep "success\|completed" upload_results.csv | wc -l  # Count successful uploads
grep "failed\|error" upload_results.csv > remaining_items.csv

# 2. Resume from checkpoint
o-nakala-upload --resume upload_results.csv --max-retries 3

# 3. Validate recovery
o-nakala-user-info --api-key $NAKALA_API_KEY --recent-uploads
```

### Scenario 2: Collection Creation Failure

**Problem**: Collections fail to create after successful uploads

**Recovery Process**:
```bash
# 1. Verify uploaded data exists
o-nakala-user-info --api-key $NAKALA_API_KEY --data-only

# 2. Retry collection creation
o-nakala-collection \
  --from-upload-output upload_results.csv \
  --retry-failed \
  --verbose

# 3. Manual collection assignment if needed
python assign_to_collections.py upload_results.csv collection_mapping.csv
```

### Scenario 3: API Authentication Errors

**Problem**: API key becomes invalid during long-running processes

**Recovery Process**:
```bash
# 1. Verify API key status
curl -H "X-API-KEY: $NAKALA_API_KEY" $NAKALA_API_URL/users/me

# 2. Refresh or update API key
export NAKALA_API_KEY="new-valid-key"

# 3. Resume operations with new authentication
o-nakala-upload --resume upload_results.csv --api-key $NAKALA_API_KEY
```

### Scenario 4: Metadata Corruption During Upload

**Problem**: Some metadata becomes corrupted during the upload process

**Recovery Process**:
```bash
# 1. Identify corrupted items
o-nakala-curator --validate-metadata --scope all --output corrupted_items.csv

# 2. Download and compare original metadata
python compare_metadata.py original_data.csv corrupted_items.csv

# 3. Apply metadata corrections
o-nakala-curator --fix-metadata --from-file metadata_corrections.csv
```

## Automated Error Recovery

### Recovery Scripts

#### Basic Recovery Script
```bash
#!/bin/bash
# auto_recovery.sh - Automated error recovery

UPLOAD_FILE=$1
API_KEY=$2
MAX_ATTEMPTS=3
CURRENT_ATTEMPT=1

while [ $CURRENT_ATTEMPT -le $MAX_ATTEMPTS ]; do
    echo "Attempt $CURRENT_ATTEMPT of $MAX_ATTEMPTS"
    
    if o-nakala-upload --dataset $UPLOAD_FILE --api-key $API_KEY --output results_attempt_$CURRENT_ATTEMPT.csv; then
        echo "Upload successful on attempt $CURRENT_ATTEMPT"
        exit 0
    else
        echo "Attempt $CURRENT_ATTEMPT failed"
        CURRENT_ATTEMPT=$((CURRENT_ATTEMPT + 1))
        sleep 30  # Wait before retry
    fi
done

echo "All recovery attempts failed"
exit 1
```

#### Intelligent Recovery Script
```python
# intelligent_recovery.py - Smart error recovery
import time
import subprocess
import json

def analyze_error_type(error_log):
    """Analyze error log to determine recovery strategy"""
    with open(error_log, 'r') as f:
        content = f.read().lower()
    
    if 'network' in content or 'timeout' in content:
        return 'network_retry'
    elif 'permission' in content or 'access' in content:
        return 'permission_fix'
    elif 'metadata' in content or 'validation' in content:
        return 'metadata_repair'
    else:
        return 'generic_retry'

def apply_recovery_strategy(strategy, dataset_file):
    """Apply appropriate recovery strategy"""
    if strategy == 'network_retry':
        return retry_with_backoff(dataset_file)
    elif strategy == 'permission_fix':
        return fix_permissions_and_retry(dataset_file)
    elif strategy == 'metadata_repair':
        return repair_metadata_and_retry(dataset_file)
    else:
        return generic_retry(dataset_file)
```

### Monitoring and Alerting

```bash
# Monitor for errors in real-time
tail -f upload.log | grep -i "error\|failed" | while read line; do
    echo "ERROR DETECTED: $line" | mail -s "O-Nakala Upload Error" admin@institution.edu
done

# Daily error summary
grep -i "error\|failed" /var/log/o-nakala-*.log | wc -l > daily_error_count.txt
```

## Prevention Strategies

### Proactive Error Prevention

#### Pre-Upload Validation
```bash
# Comprehensive pre-upload check
validate_before_upload() {
    local csv_file=$1
    
    echo "Validating file accessibility..."
    o-nakala-preview --csv $csv_file --validate-files || return 1
    
    echo "Validating metadata format..."
    o-nakala-preview --csv $csv_file --validate-only || return 1
    
    echo "Checking API connectivity..."
    curl -f -H "X-API-KEY: $NAKALA_API_KEY" $NAKALA_API_URL/users/me || return 1
    
    echo "All pre-upload validations passed"
    return 0
}
```

#### Robust Configuration
```bash
# Set conservative timeouts and retry policies
export NAKALA_TIMEOUT=300
export NAKALA_MAX_RETRIES=5
export NAKALA_RETRY_DELAY=30

# Enable detailed logging
export NAKALA_LOG_LEVEL=DEBUG
export NAKALA_LOG_FILE="/var/log/o-nakala-$(date +%Y%m%d).log"
```

### Error Recovery Best Practices

1. **Always Create Backups**: Maintain copies of original data before processing
2. **Log Everything**: Enable comprehensive logging for troubleshooting
3. **Validate Early**: Use preview tools to catch issues before upload
4. **Implement Checkpoints**: Save progress at regular intervals
5. **Monitor Resources**: Ensure sufficient disk space and memory
6. **Test Recovery Procedures**: Regularly test recovery processes
7. **Document Errors**: Maintain error logs for pattern analysis

## Recovery Documentation and Reporting

### Error Report Generation
```bash
# Generate comprehensive error report
generate_error_report() {
    local log_file=$1
    local output_file="error_report_$(date +%Y%m%d_%H%M%S).html"
    
    echo "<html><body>" > $output_file
    echo "<h1>O-Nakala Core Error Report</h1>" >> $output_file
    echo "<h2>Error Summary</h2>" >> $output_file
    grep -i "error\|failed" $log_file | sort | uniq -c >> $output_file
    echo "<h2>Recovery Actions</h2>" >> $output_file
    grep -i "recovery\|retry" $log_file >> $output_file
    echo "</body></html>" >> $output_file
    
    echo "Error report generated: $output_file"
}
```

### Recovery Success Metrics
- **Mean Time to Recovery (MTTR)**: Target <2 hours
- **Recovery Success Rate**: Target >95%
- **Data Loss Prevention**: Target 0% data loss
- **Error Recurrence Rate**: Target <5%

This comprehensive error recovery guide ensures that O-Nakala Core workflows can handle failures gracefully and recover quickly with minimal data loss and user intervention.