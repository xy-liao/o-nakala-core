# Workflow Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Package Not Found Error
```bash
ERROR: No matching distribution found for o-nakala-core
```
**Solution**: Ensure you're using the correct package name:
```bash
pip install o-nakala-core[cli]
```

#### CLI Commands Not Available
```bash
command not found: nakala-upload
```
**Solution**: Install with CLI dependencies:
```bash
pip install o-nakala-core[cli]
```

### Upload Issues

#### Base Path Error
```bash
ERROR - Base path does not exist: /path/to/dataset
```
**Solution**: Ensure `--base-path` matches your dataset directory:
```bash
nakala-upload --base-path examples/sample_dataset --dataset examples/sample_dataset
```

#### File Path Resolution
```bash
ERROR - File not found: files/code/script.py
```
**Solution**: CSV file paths should be relative to `--base-path`. Check your directory structure:
```
base-path/
└── files/
    └── code/
        └── script.py
```

### Collection Issues

#### Missing Load Method Error
```bash
AttributeError: 'NakalaCollectionClient' object has no attribute '_load_upload_output'
```
**Solution**: This bug was fixed in the codebase. Update to latest version or apply the fix from the validation run.

#### Collection Mapping Errors
```bash
WARNING - Folder 'files/images/' matched no items
```
**Solution**: Ensure folder paths in collection CSV match the titles in upload output:
- Check upload output CSV for exact title formats
- Verify folder path mappings in collection configuration

### API Issues

#### Authentication Errors
```bash
401 Client Error: Unauthorized
```
**Solution**: 
1. Verify API key is correct
2. Check you're using test environment key with test URL:
```bash
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
nakala-upload --api-url https://apitest.nakala.fr
```

#### Rate Limiting
```bash
429 Too Many Requests
```
**Solution**: The client includes automatic retry with exponential backoff. Wait and retry if needed.

## Validation Commands

### Test Installation
```bash
# Verify all CLI commands are available
nakala-upload --help
nakala-collection --help
nakala-curator --help
nakala-user-info --help
```

### Test API Connection
```bash
# Test with public test key
nakala-user-info --api-key "33170cfe-f53c-550b-5fb6-4814ce981293"
```

### Validate Workflow Files
```bash
# Validate upload configuration
nakala-upload --validate-only --folder-config your-config.csv

# Validate collection configuration  
nakala-collection --validate-only --from-folder-collections collections.csv
```

## Getting Help

1. **Check logs**: All tools generate detailed logs for troubleshooting
2. **Use validation mode**: Add `--validate-only` to test configurations
3. **Test environment**: Use test API keys and test.nakala.fr for testing
4. **Documentation**: Refer to endpoint-specific documentation in `/docs/endpoints/`

## Recent Fixes Applied

- **2025-06-09**: Fixed missing `_load_upload_output` method in collection.py
- **2025-06-09**: Updated package name from `nakala-client` to `o-nakala-core`
- **2025-06-09**: Verified all CLI commands work with new package structure