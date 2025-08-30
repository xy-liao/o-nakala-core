# O-Nakala Core Troubleshooting Guide

## 🚨 Common Issues and Solutions

### Upload Issues

#### "Folder config is required for folder mode"

**Problem**: You're trying to use folder mode without specifying the folder configuration file.

**Solution**: 
```bash
# ❌ Incorrect - missing --folder-config
o-nakala-upload --api-key YOUR_KEY --dataset folder_data_items.csv --mode folder

# ✅ Correct - includes --folder-config
o-nakala-upload --api-key YOUR_KEY --dataset folder_data_items.csv --mode folder --folder-config folder_data_items.csv --base-path .
```

**Key points**:
- Folder mode requires both `--dataset` and `--folder-config` parameters
- Usually these point to the same CSV file when using folder structure
- Always specify `--base-path` to set the root directory for file resolution

#### "No such file or directory" when changing directories

**Problem**: The script tries to navigate to a directory that doesn't exist relative to your current location.

**Solution**:
```bash
# Check your current directory
pwd

# Make sure you're in the project root
cd /path/to/o-nakala-core

# Then run the commands
cd examples/sample_dataset
o-nakala-upload --api-key YOUR_KEY ...
```

**Alternative**: Use absolute paths instead of relative paths:
```bash
o-nakala-upload --api-key YOUR_KEY --dataset /full/path/to/folder_data_items.csv --base-path /full/path/to/examples/sample_dataset
```

#### Folder Path Issues
- **Problem**: "No folders found to process" warning
- **Solution**: 
  1. Verify the base path in `--dataset` parameter points to the directory containing your `files` folder
  2. Check folder paths in `folder_data_items.csv` match actual directory structure
  3. Ensure folder paths use forward slashes (/) and match case exactly
  4. Example correct structure:
     ```
     sample_dataset/
     ├── files/
     │   ├── code/
     │   ├── data/
     │   └── documents/
     ├── folder_data_items.csv
     └── folder_collections.csv
     ```

#### File Not Found Errors
- **Problem**: Script cannot find files to upload
- **Solution**: 
  1. Verify folder structure matches configuration
  2. Check file paths in CSV configuration
  3. Ensure proper permissions on files
  4. Use absolute paths if needed

#### MIME Type Issues
- **Problem**: Files rejected due to incorrect MIME type
- **Solution**:
  1. Verify file extensions are correct
  2. Check file format is supported
  3. Use dynamic MIME type detection
  4. Add custom MIME type mapping if needed

#### Upload Failures
- **Problem**: Files fail to upload
- **Solution**:
  1. Check API key validity
  2. Verify network connection
  3. Check file size limits
  4. Review error logs for details

### Collection Issues

#### "Item [ID] not found in datasets or collections"

**Problem**: The collection IDs in your modification CSV file are outdated or incorrect.

**Solution**:
1. Check the `collections_output.csv` file created during collection creation
2. Update your `collection_modifications.csv` with the correct collection IDs
3. Example:
   ```csv
   # OLD (from example)
   10.34847/nkl.adfc67q4,modify,"Description..."
   
   # NEW (from your collections_output.csv)
   10.34847/nkl.6fbdsyv0,modify,"Description..."
   ```

**Prevention**: Always use the most recent collection IDs from your workflow outputs.

#### Collection Mapping Issues
- **Problem**: Collections not matching expected folder structure
- **Solution**:
  1. Check collection mapping diagnostics in logs
  2. Verify folder paths in `folder_collections.csv`
  3. Ensure data items were successfully uploaded
  4. Review the mapping output:
     ```json
     {
       "folder": {
         "code": {
           "path": "files/code",
           "matches": [
             {
               "title": "fr:Fichiers de code|en:Code Files",
               "id": "10.34847/nkl.xxxxx"
             }
           ]
         }
       },
       "matched_items": ["fr:Fichiers de code|en:Code Files"],
       "unmatched_folders": []
     }
     ```

#### Empty Collections
- **Problem**: Collections created but no items added
- **Solution**:
  1. Check output.csv for successful uploads
  2. Verify data IDs in collection creation
  3. Check rights and permissions
  4. Review collection configuration
  5. Check collection mapping diagnostics for unmatched folders

#### Metadata Problems
- **Problem**: Metadata not appearing correctly
- **Solution**:
  1. Verify metadata format in CSV
  2. Check multilingual syntax (fr|en format)
  3. Validate required fields
  4. Review metadata templates

#### Collection Relationship Issues
- **Problem**: Collection relationships not properly established
- **Solution**:
  1. Verify relation types in folder_collections.csv
  2. Check collection IDs exist
  3. Ensure proper relation syntax
  4. Review collection hierarchy

#### Folder-Based Collection Issues
- **Problem**: Collections not matching folder structure
- **Solution**:
  1. Verify folder_collections.csv configuration
  2. Check folder paths match data items
  3. Ensure proper folder hierarchy
  4. Review collection mapping

### API Issues

#### Authentication Failures
- **Problem**: API requests rejected
- **Solution**:
  1. Verify API key is correct
  2. Check API key permissions
  3. Ensure proper headers
  4. Check API endpoint URL

#### Rate Limiting
- **Problem**: Too many requests
- **Solution**:
  1. Implement retry with backoff
  2. Reduce concurrent requests
  3. Batch operations when possible
  4. Monitor API limits

### Environment Issues

#### Package Import Errors

**Problem**: Cannot import `o_nakala_core` or getting import errors.

**Solution**:
```bash
# Clean installation
pip uninstall o-nakala-core
pip install -e ".[dev,cli,ml]"

# Verify installation
python -c "import o_nakala_core; print(f'Version: {o_nakala_core.__version__}')"
o-nakala-upload --help
```

#### CLI Commands Not Found

**Problem**: Commands like `o-nakala-upload` are not recognized.

**Solution**:
```bash
# Ensure you're in the right virtual environment
source .venv/bin/activate  # or your venv path

# Reinstall with CLI support
pip install -e ".[cli]"

# Verify CLI commands are available
which o-nakala-upload
o-nakala-upload --help
```

### API Issues

#### Authentication Errors (401/403)

**Problem**: API key is invalid or expired.

**Solution**:
```bash
# Test API connection
export NAKALA_API_KEY="your-test-key"
o-nakala-user-info --api-key "$NAKALA_API_KEY"

# Use the validated test key for testing
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
```

#### Rate Limiting or Connection Errors

**Problem**: Too many requests or network issues.

**Solution**:
- Wait a few minutes and retry
- Check your internet connection
- Use the test environment: `--api-url https://apitest.nakala.fr`

### Workflow Issues

#### File Path Resolution Problems

**Problem**: Files are not found even though they exist.

**Solution**:
```bash
# Always use absolute paths or ensure you're in the correct directory
cd examples/sample_dataset

# Verify files exist
ls -la folder_data_items.csv
ls -la files/

# Use correct relative paths
o-nakala-upload --base-path . --dataset folder_data_items.csv
```

#### CSV Format Issues

**Problem**: CSV files have formatting problems.

**Solution**:
- Ensure proper UTF-8 encoding
- Check for unescaped quotes in multilingual fields
- Use proper delimiter (comma)
- Example of correct multilingual format:
  ```csv
  title,description
  "Test Title","fr:Description française|en:English description"
  ```

## 🔧 Diagnostic Commands

### Environment Check
```bash
# Check Python and pip
python --version
pip --version

# Check virtual environment
which python
which pip

# Check package installation
pip list | grep nakala
python -c "import o_nakala_core; print(o_nakala_core.__file__)"
```

### CLI Check
```bash
# Test all CLI commands
o-nakala-upload --help
o-nakala-collection --help
o-nakala-curator --help
o-nakala-user-info --help
```

### API Check
```bash
# Test API connection
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
o-nakala-user-info --api-key "$NAKALA_API_KEY" --collections-only
```

### File Structure Check
```bash
# Verify directory structure
find examples/sample_dataset -name "*.csv" -type f
find examples/sample_dataset/files -type f | head -10
```

## 📋 Pre-flight Checklist

Before running workflows, verify:

- [ ] Virtual environment is activated
- [ ] Package is installed: `pip list | grep o-nakala-core`
- [ ] CLI commands work: `o-nakala-upload --help`
- [ ] API key is set: `echo $NAKALA_API_KEY`
- [ ] You're in the correct directory: `pwd`
- [ ] Required files exist: `ls -la *.csv`
- [ ] Base path is correct: `ls -la files/`

## 🆘 Getting Help

### Log Analysis
```bash
# Check detailed logs
tail -f nakala_upload.log
tail -f o_nakala_core.log
```

### Enable Debug Logging
```bash
o-nakala-upload --log-level DEBUG --api-key YOUR_KEY ...
```

### Validation Mode
```bash
# Test without uploading
o-nakala-upload --validate-only --api-key YOUR_KEY --dataset your_file.csv --mode csv
```

### Community Support

1. **Check existing issues**: Review solved problems in the repository
2. **Create detailed bug reports**: Include error messages, log files, and steps to reproduce
3. **Use validation tools**: Always validate CSV files before uploading

## Debugging Tips

### Enhanced Error Handling (V2 Features)
- **Pre-validation**: Payloads are validated before API calls to catch common errors early
- **Detailed Error Parsing**: API error responses are parsed to provide specific guidance
- **Debug Logging**: Set `--log-level DEBUG` to see request payloads for failed API calls
- **Metadata Validation**: Common metadata format issues are detected and explained

### Log Files
- Check `nakala_upload.log` for upload issues
- Check `nakala_collection.log` for collection issues
- Review `collections_output.csv` for collection creation status
- Use `--log-level DEBUG` for detailed request/response logging
- Look for specific error messages and guidance
- Check timestamps for correlation

### Common Error Messages

#### "Invalid status private"
- **Cause**: Status value not accepted by API
- **Fix**: Use valid status values (e.g., "pending", "public")

#### "File not found"
- **Cause**: Incorrect file path or permissions
- **Fix**: Verify file exists and is accessible

#### "Invalid metadata format" / "nakala:creator must be an array" (RESOLVED ✅)
- **Status**: ✅ **FIXED** - Creator fields now fully supported
- **Solution**: Use `new_creator` or `new_author` fields in batch modifications
- **Example**: 
  ```csv
  id,action,new_creator
  10.34847/nkl.collection1,modify,"Smith, John;Doe, Jane"
  ```
- **Note**: Both individual and multiple creators (semicolon-separated) are supported

#### "metadata field must not have lang attribute"
- **Cause**: System fields like date/license cannot have language attributes
- **Fix**: Remove language attributes from system fields (date, license, type URIs)
- **Note**: Only descriptive fields like title/description should have language attributes

#### "Dataset payload validation failed"
- **Cause**: Pre-validation caught structural issues before API call
- **Fix**: Check the specific validation error messages in logs for guidance

#### "Invalid collection relation"
- **Cause**: Collection relationship syntax incorrect
- **Fix**: Verify relation format in folder_collections.csv

## Best Practices

### Prevention
1. Validate configurations before upload
2. Test with small datasets first
3. Use consistent naming conventions
4. Keep detailed logs
5. Verify folder structure matches collection design

### Recovery
1. Use collections_output.csv to track progress
2. Implement proper error handling
3. Keep backup of configurations
4. Document successful workflows
5. Maintain collection relationship documentation

## 📚 Official NAKALA Help Resources

### **Technical Support**
- **[Official NAKALA Documentation](https://documentation.huma-num.fr/nakala/)** - Complete troubleshooting guide
- **[NAKALA User Manual](https://documentation.huma-num.fr/nakala/)** - Step-by-step problem resolution
- **[NAKALA Support](https://documentation.huma-num.fr/nakala/)** - Official technical support

### **API Debugging**
- **[Test API Documentation](https://apitest.nakala.fr/doc)** - Interactive debugging and testing
- **[Production API Documentation](https://api.nakala.fr/doc)** - Live API troubleshooting
- **[API Error Codes](https://api.nakala.fr/doc)** - HTTP status codes and response formats for API errors

### **Safe Testing Environment**
- **[NAKALA Test Platform](https://test.nakala.fr)** - Debug issues safely with test accounts (password: IamTesting2020)
- **[Test Data Guidelines](https://documentation.huma-num.fr/nakala/)** - Best practices for testing

---

**Last Updated**: 2025-08-30  
**O-Nakala Core Version**: v2.5.1 