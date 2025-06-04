# Troubleshooting Guide

## Common Issues and Solutions

### Upload Issues

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

#### Empty Collections
- **Problem**: Collections created but no items added
- **Solution**:
  1. Check output.csv for successful uploads
  2. Verify data IDs in collection creation
  3. Check rights and permissions
  4. Review collection configuration

#### Metadata Problems
- **Problem**: Metadata not appearing correctly
- **Solution**:
  1. Verify metadata format in CSV
  2. Check multilingual syntax
  3. Validate required fields
  4. Review metadata templates

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

### Log Files
- Check `nakala_upload.log` for upload issues
- Review `nakala_collection.log` for collection problems
- Look for specific error messages
- Check timestamps for correlation

### Common Error Messages

#### "Invalid status private"
- **Cause**: Status value not accepted by API
- **Fix**: Use valid status values (e.g., "pending", "public")

#### "File not found"
- **Cause**: Incorrect file path or permissions
- **Fix**: Verify file exists and is accessible

#### "Invalid metadata format"
- **Cause**: Metadata structure doesn't match requirements
- **Fix**: Check metadata format in configuration

## Best Practices

### Prevention
1. Validate configurations before upload
2. Test with small datasets first
3. Use consistent naming conventions
4. Keep detailed logs

### Recovery
1. Use output.csv to track progress
2. Implement proper error handling
3. Keep backup of configurations
4. Document successful workflows 