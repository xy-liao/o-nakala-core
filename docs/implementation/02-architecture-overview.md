KEY') or
            self._load_from_file() or
            self._prompt_for_key()
        )
```

### Input Validation

```python
# Comprehensive input validation
def validate_upload_data(data: Dict) -> None:
    """Validate upload data against security and format requirements"""
    
    # File path validation (prevent directory traversal)
    if '..' in data.get('file_path', ''):
        raise SecurityError("Invalid file path detected")
    
    # Metadata validation (prevent injection)
    for field in ['title', 'description']:
        if field in data:
            validate_text_field(data[field])
    
    # File size validation
    if data.get('file_size', 0) > MAX_FILE_SIZE:
        raise ValidationError(f"File too large: {data['file_size']} bytes")
```

## 🧪 Testing Architecture

### Unit Testing Structure

```python
# tests/test_common_utils.py
import pytest
from nakala_client.common.utils import prepare_metadata
from nakala_client.common.exceptions import MetadataValidationError

class TestMetadataPreparation:
    def test_prepare_basic_metadata(self):
        data = {'title': 'Test', 'author': 'John Doe'}
        result = prepare_metadata(data)
        assert len(result) == 2
        assert result[0]['propertyUri'] == 'http://nakala.fr/terms#title'
    
    def test_multilingual_field_parsing(self):
        data = {'title_en': 'English Title', 'title_fr': 'Titre Français'}
        result = prepare_metadata(data)
        # Verify multilingual handling
        
    def test_invalid_metadata_raises_error(self):
        with pytest.raises(MetadataValidationError):
            prepare_metadata({'invalid_field': 'value'})
```

### Integration Testing

```python
# tests/test_integration.py
class TestUploadIntegration:
    def test_full_upload_workflow(self, test_config, sample_dataset):
        """Test complete upload workflow with test API"""
        uploader = NakalaUploader(test_config)
        result = uploader.process_dataset_csv(sample_dataset)
        
        assert result['status'] == 'success'
        assert 'identifier' in result
        
    def test_error_recovery(self, test_config, invalid_dataset):
        """Test error handling and recovery"""
        uploader = NakalaUploader(test_config)
        
        with pytest.raises(FileValidationError):
            uploader.process_dataset_csv(invalid_dataset)
```

## 📈 Performance Architecture

### Concurrent Processing

```python
# Configurable concurrency for file uploads
from concurrent.futures import ThreadPoolExecutor

class ConcurrentUploader:
    def __init__(self, config: UploadConfig):
        self.config = config
        self.max_workers = config.concurrent_uploads
    
    def upload_files_concurrently(self, files: List[Path]) -> List[Dict]:
        """Upload multiple files concurrently with error handling"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.upload_file, f): f for f in files}
            results = []
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Upload failed: {e}")
                    results.append({'error': str(e)})
            
            return results
```

### Batch Processing

```python
# Efficient batch processing for large datasets
class BatchProcessor:
    def __init__(self, config: UploadConfig):
        self.batch_size = config.batch_size
    
    def process_in_batches(self, datasets: List[Dict]) -> Iterator[List[Dict]]:
        """Process datasets in configurable batches"""
        for i in range(0, len(datasets), self.batch_size):
            batch = datasets[i:i + self.batch_size]
            yield self.process_batch(batch)
```

## 🔄 Migration Strategy

### Backward Compatibility

The v2.0 architecture maintains full backward compatibility:

```python
# v1.0 scripts remain functional
# v2.0 scripts provide same CLI interface
# Configuration files work with both versions
# Output formats are identical
```

### Gradual Migration Path

1. **Phase 1**: Run v1.0 and v2.0 in parallel
2. **Phase 2**: Test v2.0 with existing workflows
3. **Phase 3**: Migrate non-critical workflows to v2.0
4. **Phase 4**: Migrate critical workflows after validation
5. **Phase 5**: Deprecate v1.0 (optional)

## 🎯 Future Extensions

The architecture is designed to support:

### Planned Client Modules
- **Search Client**: Advanced search and filtering
- **Curator Client**: Data quality and curation tools
- **Metadata Client**: Metadata validation and transformation
- **Analytics Client**: Usage analytics and reporting

### Integration Possibilities
- **Web Interface**: Django/Flask web frontend
- **REST API**: API server for remote access
- **CLI Tools**: Enhanced command-line utilities
- **Workflow Orchestration**: Integration with workflow systems

## 📋 Benefits of V2.0 Architecture

### For Users
- **Better Error Messages**: Clear, actionable error information
- **Progress Tracking**: Detailed logging of operations
- **Validation**: Early detection of problems before API calls
- **Reliability**: Improved error recovery and retry mechanisms

### For Developers
- **Code Reuse**: Common utilities reduce duplication
- **Consistency**: Standardized patterns across modules
- **Extensibility**: Easy addition of new functionality
- **Maintainability**: Clear separation of concerns

### For Operations
- **Monitoring**: Structured logging for operational visibility
- **Configuration**: Centralized configuration management
- **Deployment**: Package-based installation and distribution
- **Testing**: Comprehensive test coverage and validation

This architecture provides a solid foundation for current needs while supporting future growth and enhancement of the Nakala client ecosystem.