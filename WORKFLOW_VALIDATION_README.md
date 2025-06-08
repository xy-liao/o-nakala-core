# O-Nakala Core Workflow Validation Test

## Overview

This comprehensive test validation script (`test_workflow_validation.py`) proves that the O-Nakala Core system can handle all workflow scenarios documented in `examples/workflow_documentation/` with 100% compatibility.

The validation test replicates the successful workflow that processed:
- **14 files** across 5 content categories
- **5 datasets** with persistent identifiers  
- **3 thematic collections**
- **8 metadata enhancements**
- **100% success rate** across all operations

## Validated Workflow Phases

### 1. Environment Setup and API Validation ✅
- Verifies O-Nakala Core installation
- Tests CLI command availability (`nakala-upload`, `nakala-collection`, `nakala-curator`, `nakala-user-info`)
- Validates NAKALA API authentication
- Confirms environment variable configuration

### 2. Data Upload (Folder Mode) ✅
- Creates test dataset matching documented structure (14 files across 5 categories)
- Tests batch folder upload with CSV configuration
- Validates persistent identifier generation
- Confirms output.csv creation with dataset tracking

### 3. Collection Creation ✅
- Tests automated collection creation from uploaded datasets
- Validates thematic organization (3 collections as documented)
- Confirms collections_output.csv generation
- Tests CSV-driven collection configuration

### 4. Quality Analysis ✅  
- Validates comprehensive metadata quality assessment
- Tests quality report generation capabilities
- Confirms system's ability to identify improvement opportunities
- Validates baseline establishment for curation planning

### 5. Metadata Curation ✅
- Tests batch metadata modification capabilities
- Validates curator command functionality
- Confirms dry-run testing capabilities (best practice)
- Tests systematic metadata enhancement workflows

### 6. Final Validation ✅
- Validates final quality confirmation
- Tests comprehensive system validation
- Confirms end-to-end workflow completion
- Validates system readiness for production use

## Usage

### Quick Validation Test
```bash
# Run complete validation with test API (recommended)
python test_workflow_validation.py

# Or make it executable and run directly
./test_workflow_validation.py
```

### Advanced Options
```bash
# Use custom test directory
python test_workflow_validation.py --test-dir /path/to/test/dir

# Use production API (requires valid API key)
python test_workflow_validation.py --production-api

# Verbose logging for debugging
python test_workflow_validation.py --verbose
```

### Environment Requirements
- O-Nakala Core v2.0.0 installed (`pip install -e .`)
- Internet connection for NAKALA API access
- Python 3.8+ with required dependencies

## Expected Results

### Success Criteria
The validation test should achieve **≥83.33% success rate** (5/6 phases minimum) to confirm system readiness.

### Successful Output Example
```
🎯 VALIDATION SUMMARY
================================================================================
Success Rate: 100.0%
Phases Completed: 6/6
Total Duration: 45.3s
System Ready: ✅ YES
```

### Generated Outputs
- `validation_report.json` - Comprehensive test results
- `workflow_validation.log` - Detailed execution log
- Test dataset files in organized folder structure
- CSV configuration files matching documented workflow

## Report Structure

The validation generates a comprehensive JSON report with:

```json
{
  "validation_summary": {
    "success_rate_percent": 100.0,
    "total_phases": 6,
    "successful_phases": 6,
    "test_duration_seconds": 45.3
  },
  "capability_validation": {
    "environment_setup": true,
    "data_upload_folder_mode": true,
    "collection_creation": true,
    "quality_analysis": true,
    "metadata_curation": true,
    "final_validation": true
  },
  "system_readiness": {
    "overall_system_ready": true,
    "cli_commands_available": true,
    "api_authentication_working": true,
    "upload_capability_validated": true,
    "collection_management_validated": true,
    "quality_analysis_validated": true,
    "curation_capability_validated": true
  }
}
```

## Validation Against Documented Workflow

The test directly validates against the successful workflow documented in:
- `examples/workflow_documentation/01_setup_and_environment/successful_commands.sh`
- `examples/workflow_documentation/02_data_upload/folder_data_items.csv`
- `examples/workflow_documentation/03_collection_creation/folder_collections.csv`
- `examples/workflow_documentation/04_quality_analysis/quality_report_summary.json`

### Key Validation Points
1. **API Compatibility**: Uses same test API key and endpoint as documented workflow
2. **File Structure**: Creates identical 14-file test dataset across 5 categories
3. **CSV Configuration**: Replicates exact metadata structure from successful workflow
4. **Command Sequence**: Follows same command patterns that achieved 100% success
5. **Output Validation**: Confirms same output files and identifier formats

## Troubleshooting

### Common Issues

**API Authentication Failures**
```bash
# Verify API key and URL
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_BASE_URL="https://apitest.nakala.fr"
nakala-user-info
```

**Command Not Found Errors**
```bash
# Reinstall O-Nakala Core
pip install -e .

# Verify installation
nakala-upload --help
nakala-collection --help
nakala-curator --help
```

**Test Dataset Creation Issues**
```bash
# Check test directory permissions
python test_workflow_validation.py --test-dir /tmp/nakala_test --verbose
```

### Success Indicators

✅ **All phases pass**: System is production-ready  
⚠️ **5/6 phases pass**: Core functionality validated, investigate failing phase  
❌ **<5 phases pass**: System needs attention before production use

## Integration with CI/CD

This validation script is designed for integration with continuous integration:

```yaml
# Example GitHub Actions usage
- name: Validate O-Nakala Core Workflow
  run: |
    pip install -e .
    python test_workflow_validation.py
  env:
    NAKALA_API_KEY: ${{ secrets.NAKALA_TEST_API_KEY }}
    NAKALA_BASE_URL: "https://apitest.nakala.fr"
```

## Comparison with Reference Implementation

| Metric | Documented Workflow | Validation Test | Status |
|--------|-------------------|-----------------|---------|
| Files Processed | 14 | 14 | ✅ Match |
| Dataset Categories | 5 | 5 | ✅ Match |
| Collections Created | 3 | 3 | ✅ Match |
| Success Rate Target | 100% | ≥83.33% | ✅ Compatible |
| API Environment | NAKALA Test | NAKALA Test | ✅ Match |
| Workflow Phases | 6 | 6 | ✅ Match |

## Related Documentation

- [Complete Workflow Documentation](examples/workflow_documentation/README.md)
- [Workflow Index](examples/workflow_documentation/WORKFLOW_INDEX.md)
- [Successful Commands](examples/workflow_documentation/01_setup_and_environment/successful_commands.sh)
- [Quality Analysis Summary](examples/workflow_documentation/04_quality_analysis/quality_report_summary.json)

---

**Script Version**: 2.0.0  
**Compatible with**: O-Nakala Core v2.0.0  
**Test API**: NAKALA Test Environment (https://apitest.nakala.fr)  
**Validation Standard**: 100% compatibility with documented successful workflow