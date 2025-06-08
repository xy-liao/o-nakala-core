# Troubleshooting Guide

## Common Issues and Solutions

### Upload Issues

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