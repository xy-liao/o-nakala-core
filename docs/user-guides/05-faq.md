# Frequently Asked Questions (FAQ)

## General Questions

### Q: What is the difference between v1.0 and v2.0 scripts?

**A:** V2.0 provides significant improvements while maintaining full backward compatibility:

- **Better Error Handling**: More detailed error messages and recovery options
- **Enhanced Logging**: Structured logging with timestamps and context
- **Shared Architecture**: Common utilities for consistency across modules  
- **Validation**: Input validation before API calls to catch issues early
- **Extensibility**: Foundation for adding new client modules

Both versions work simultaneously - you can migrate gradually at your own pace.

### Q: Do I need to change my existing CSV files or configuration?

**A:** No! All existing files work unchanged with both v1.0 and v2.0:
- CSV datasets remain the same format
- Configuration files are compatible
- CLI arguments are identical
- Output formats are unchanged

### Q: Which API endpoint should I use for testing?

**A:** Use the test environment for development:
- **Test API**: `https://apitest.nakala.fr`
- **Production API**: `https://nakala.fr` (use only for final production uploads)

Always test thoroughly on the test environment before using production.

## Upload Questions

### Q: How do I handle large file uploads?

**A:** For large files:

1. **Check file size limits**: Nakala has size restrictions per file
2. **Monitor upload progress**: V2.0 provides detailed progress logging
3. **Handle timeouts**: Use retry mechanisms for network issues
4. **Split large datasets**: Process in smaller batches if needed

```bash
# Example for large datasets
nakala-upload --batch-size 10 --retry-attempts 3
```

### Q: What file formats are supported?

**A:** Nakala supports most common formats:
- **Images**: JPG, PNG, TIFF, GIF
- **Documents**: PDF, DOC, DOCX, TXT
- **Data**: CSV, JSON, XML
- **Audio/Video**: MP3, MP4, AVI
- **Archives**: ZIP, TAR

Check the specific requirements in your Nakala instance configuration.

### Q: How do I handle failed uploads?

**A:** V2.0 provides better error recovery:

1. **Check the logs**: Detailed error messages explain the issue
2. **Validate inputs**: Run with `--validate-only` flag first
3. **Retry mechanism**: V2.0 includes automatic retry for network issues
4. **Resume uploads**: Fix issues and re-run - already uploaded files are skipped

```bash
# Validate before uploading
nakala-upload --validate-only dataset.csv

# Upload with detailed logging
nakala-upload --debug dataset.csv
```

## Collection Questions

### Q: How do I organize data into collections?

**A:** Use the hierarchical collection system:

1. **Create collections first**: Use the collection script to create containers
2. **Upload data**: Upload your datasets with the upload script  
3. **Link data to collections**: Use the collection script to associate data

```bash
# Step 1: Create collections
nakala-collection --from-folder-collections collections.csv

# Step 2: Upload data
nakala-upload --dataset data.csv

# Step 3: Link data to collections  
nakala-collection --from-upload-output output.csv
```

### Q: Can I add data to existing collections?

**A:** Yes, in several ways:

1. **Via collection script**: Add new data to existing collections
2. **Via upload script**: Specify collection IDs in your dataset CSV
3. **Via Nakala web interface**: Manual addition through the GUI

### Q: How do I handle collection permissions?

**A:** Set permissions in your CSV configuration:
- **ROLE_READER**: Can view the collection
- **ROLE_EDITOR**: Can modify collection content
- **ROLE_ADMIN**: Can manage collection and permissions
- **ROLE_OWNER**: Full control over the collection

## Authentication Questions

### Q: How do I get an API key?

**A:** 
1. **Register** on the Nakala platform (test or production)
2. **Access your profile** settings
3. **Generate API key** in the API section
4. **Store securely** in your `.env` file

### Q: My API key isn't working. What should I check?

**A:** Common issues:

1. **Wrong environment**: Test keys don't work on production endpoints
2. **Expired key**: Generate a new key if it's old
3. **Wrong format**: API keys are UUIDs (e.g., `12345678-1234-1234-1234-123456789abc`)
4. **Environment file**: Check your `.env` file is loaded correctly

```bash
# Test your API key
python -c "import os; print(os.getenv('NAKALA_API_KEY'))"
```

## Metadata Questions

### Q: Which metadata fields are required?

**A:** Nakala requires these core fields:
- **type**: Resource type (from COAR vocabulary)
- **title**: Resource title (multilingual support)
- **creator**: Author information
- **created**: Creation date
- **license**: Usage license

### Q: How do I handle multilingual metadata?

**A:** Use language codes in your CSV:

```csv
title_en,title_fr,description_en,description_fr
"Bird Photos","Photos d'Oiseaux","Collection of bird photographs","Collection de photographies d'oiseaux"
```

### Q: What date formats are supported?

**A:** Use ISO date formats:
- **Full date**: `2024-01-15`
- **Year-month**: `2024-01`
- **Year only**: `2024`

## Technical Questions

### Q: How do I run the scripts programmatically?

**A:** Import the modules directly:

```python
from nakala_client.upload import upload_dataset
from nakala_client.collection import create_collections

# Use the modules in your code
result = upload_dataset(config, dataset_file)
collections = create_collections(config, collection_file)
```

### Q: Can I customize the logging?

**A:** Yes, configure logging levels:

```bash
# Minimal logging
nakala-upload --log-level WARNING dataset.csv

# Detailed logging  
nakala-upload --log-level DEBUG dataset.csv

# Custom log file (output goes to logs/)
nakala-upload --log-level INFO dataset.csv
```

### Q: How do I handle proxy or firewall issues?

**A:** Configure network settings:

```bash
# Set proxy in environment
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# Or in your code
import os
os.environ['HTTP_PROXY'] = 'http://proxy.example.com:8080'
```

## Error Troubleshooting

### Q: "File not found" errors

**A:** Check these common issues:
1. **Path separators**: Use forward slashes `/` or proper escaping
2. **Working directory**: Run scripts from the correct location
3. **File permissions**: Ensure files are readable
4. **Relative paths**: Use absolute paths if relative paths fail

### Q: "API connection" errors

**A:** Network troubleshooting:
1. **Internet connection**: Test basic connectivity
2. **API endpoint**: Verify the correct URL (test vs production)
3. **Firewall**: Check if the API URL is accessible
4. **Proxy settings**: Configure proxy if needed

### Q: "Invalid metadata" errors

**A:** Validation issues:
1. **Required fields**: Ensure all mandatory fields are present
2. **Format validation**: Check date formats, URLs, etc.
3. **Vocabulary terms**: Use valid terms from Nakala vocabularies
4. **File size**: Check file size limits

### Q: "Permission denied" errors

**A:** Authorization issues:
1. **API key**: Verify key is correct and active
2. **Collection access**: Check permissions on target collections
3. **User roles**: Ensure your user has necessary permissions
4. **Expired session**: Try generating a new API key

## Getting More Help

### Immediate Help
1. **Check logs**: V2.0 provides detailed error logging
2. **Run validation**: Use `--validate-only` to check inputs
3. **Test environment**: Always test on the test API first

### Documentation
1. **User Guides**: Check the specific guide for your task
2. **Troubleshooting**: Review the troubleshooting guide
3. **Implementation Notes**: Technical details for advanced users

### Support Resources
1. **Error logs**: Include full error logs when reporting issues
2. **Sample data**: Provide minimal examples that reproduce issues
3. **Environment**: Specify OS, Python version, and package versions

Remember: The v2.0 scripts provide much better error messages that usually explain exactly what needs to be fixed!