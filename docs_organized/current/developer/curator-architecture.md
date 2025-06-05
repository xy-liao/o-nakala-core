# Nakala Curator Architecture

The Nakala Curator provides comprehensive data curation and quality management tools for digital humanities researchers and data managers working with large collections in Nakala.

## Architecture Overview

### Core Components

1. **NakalaUserInfoClient** (`src/nakala_client/user_info.py`)
   - Retrieves user profile information
   - Lists collections, datasets, and group permissions
   - Provides summary statistics and export capabilities

2. **NakalaCuratorClient** (`src/nakala_client/curator.py`)
   - Main curator functionality for batch operations
   - Metadata validation and quality assessment
   - Duplicate detection and batch modifications
   - Quality reporting and recommendations

3. **Supporting Classes**
   - `CuratorConfig`: Extended configuration for curator operations
   - `BatchModificationResult`: Container for batch operation results
   - `NakalaMetadataValidator`: Metadata validation logic
   - `NakalaDuplicateDetector`: Duplicate detection algorithms

## Key Features

### 1. User Information Management
```python
from nakala_client import NakalaUserInfoClient, NakalaConfig

config = NakalaConfig(api_key="your-key")
client = NakalaUserInfoClient(config)

# Get complete user profile
profile = client.get_complete_user_profile()
client.print_summary(profile)
```

### 2. Metadata Validation
- Validates required fields (title, creator, description)
- Checks controlled vocabulary compliance
- Provides quality suggestions and recommendations
- Batch validation for large datasets

### 3. Duplicate Detection
- Text-based similarity analysis using Jaccard similarity
- Configurable similarity thresholds
- Cross-collection duplicate detection
- Detailed similarity reports

### 4. Batch Modifications
- Safe batch metadata updates with validation
- Dry-run mode for testing changes
- Comprehensive error handling and rollback
- Progress tracking and detailed logging

### 5. Quality Reporting
- Overall quality score calculation
- Detailed validation reports by item
- Actionable recommendations for improvement
- Export capabilities for further analysis

## Usage Patterns

### Command Line Interface

#### Get User Information
```bash
# Basic user info summary
./nakala-user-info.py

# Export complete profile
./nakala-user-info.py --output user_profile.json

# Get only collections
./nakala-user-info.py --collections-only
```

#### Quality Assessment
```bash
# Generate quality report
./nakala-curator.py --quality-report --output quality_report.json

# Validate metadata for all collections
./nakala-curator.py --validate-metadata --scope collections

# Detect duplicates in specific collections
./nakala-curator.py --detect-duplicates --collections col1,col2,col3
```

#### Batch Modifications
```bash
# Export modification template
./nakala-curator.py --export-template modifications.csv

# Apply modifications (dry run first)
./nakala-curator.py --batch-modify modifications.csv --dry-run

# Apply modifications for real
./nakala-curator.py --batch-modify modifications.csv
```

### Python API

#### Basic Usage
```python
from nakala_client import NakalaCuratorClient, CuratorConfig

# Create configuration
config = CuratorConfig(
    api_key="your-api-key",
    batch_size=50,
    dry_run_default=True
)

# Initialize curator
curator = NakalaCuratorClient(config)

# Generate quality report
report = curator.generate_quality_report()
print(f"Quality score: {report['overall_quality_score']:.1f}%")
```

#### Batch Operations
```python
# Prepare modifications
modifications = [
    {
        'id': 'dataset-123',
        'changes': {
            'title': 'Updated Dataset Title',
            'description': 'Enhanced description with more details'
        }
    }
]

# Apply with validation
result = curator.batch_modify_metadata(modifications, dry_run=False)
summary = result.get_summary()
print(f"Success rate: {summary['success_rate']:.1f}%")
```

## Configuration Options

### CuratorConfig Parameters

```python
config = CuratorConfig(
    # API settings
    api_key="your-key",
    api_url="https://apitest.nakala.fr",
    
    # Batch processing
    batch_size=50,                          # Items per batch
    concurrent_operations=3,                # Parallel operations
    validation_batch_size=100,              # Validation batch size
    
    # Safety settings
    skip_existing=True,                     # Skip existing items
    validate_before_modification=True,      # Pre-modification validation
    backup_before_changes=True,             # Backup before changes
    require_confirmation=True,              # Require user confirmation
    dry_run_default=True,                   # Default to dry run mode
    
    # Quality settings
    duplicate_threshold=0.85,               # Similarity threshold (0-1)
    max_modifications_per_batch=100,        # Safety limit per batch
)
```

## Safety Features

### 1. Validation Pipeline
- Pre-modification metadata validation
- Required field checking
- Controlled vocabulary validation
- Custom validation rules

### 2. Dry Run Mode
- Test modifications without applying changes
- Preview results and potential issues
- Safety-first approach for batch operations

### 3. Batch Processing
- Configurable batch sizes to avoid API limits
- Error isolation - failures don't stop entire operation
- Detailed logging and progress tracking

### 4. Rollback Protection
- Backup metadata before modifications
- Detailed operation logs for troubleshooting
- Confirmation prompts for destructive operations

## Integration with Existing V2.0 Architecture

The curator architecture builds on the solid V2.0 foundation:

- **Common Utilities**: Leverages existing `NakalaConfig`, error handling, and logging
- **API Client**: Uses the same OpenAPI client library and patterns
- **Configuration**: Extends the existing configuration system
- **Error Handling**: Consistent exception handling across all modules

## Best Practices

### 1. Always Start with Dry Runs
```bash
# Test your modifications first
./nakala-curator.py --batch-modify changes.csv --dry-run
```

### 2. Validate Before Modifying
```bash
# Check data quality first
./nakala-curator.py --quality-report
./nakala-curator.py --validate-metadata
```

### 3. Use Appropriate Batch Sizes
- Start with small batches (10-50 items)
- Monitor API response times
- Adjust based on operation complexity

### 4. Monitor and Log
- Enable verbose logging for troubleshooting
- Review operation results carefully
- Keep backups of original data

## Future Enhancements

1. **Advanced Duplicate Detection**
   - Machine learning-based similarity
   - Fuzzy string matching
   - Image and file content analysis

2. **Workflow Integration**
   - Integration with institutional workflows
   - Automated quality checks
   - Scheduled maintenance operations

3. **Collaborative Curation**
   - Multi-user editing workflows
   - Change approval processes
   - Conflict resolution tools

4. **Advanced Analytics**
   - Usage pattern analysis
   - Quality trend tracking
   - Performance optimization recommendations