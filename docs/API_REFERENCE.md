# API Reference: Complete O-Nakala Core Guide

**📍 You are here:** [START_HERE](../START_HERE.md) → [Getting Started](GETTING_STARTED.md) → API Reference

**⏱️ Time:** 30-60 minutes | **👥 Audience:** Developers, Technical Users | **📈 Level:** Technical Reference

This comprehensive guide covers all O-Nakala Core API functionality for Python integration.

## Quick Navigation
- [Upload Operations](#upload-operations) - Create datasets from files
- [Collection Operations](#collection-operations) - Organize data into collections  
- [Curator Operations](#curator-operations) - Quality management and metadata enhancement
- [User Operations](#user-operations) - Account and permission management
- [Python API](#python-api) - Integration and automation
- [CLI Reference](#cli-reference) - Command-line interface

---

## Upload Operations

### Overview
The Upload operations (`o-nakala-upload`) transform files with metadata into NAKALA datasets. Supports both organized folder structures and explicit file lists.

### Upload Modes

#### Folder Mode (Recommended)
**Best for:** Research projects with organized file structures

```bash
# Upload sample dataset using folder configuration
o-nakala-upload \
  --api-key "$NAKALA_API_KEY" \
  --dataset examples/sample_dataset/folder_data_items.csv \
  --mode folder \
  --base-path examples/sample_dataset \
  --output upload_results.csv
```

**How it works:**
- Each CSV row maps a folder path to metadata
- All files in the folder become one dataset
- Automatic file discovery and organization
- Supports complex research data structures

**Example:** 14 files in 5 categories → 5 datasets

#### CSV Mode
**Best for:** Explicit file control and individual datasets

```bash
# Upload individual files with metadata
o-nakala-upload \
  --api-key "$NAKALA_API_KEY" \
  --dataset my_datasets.csv \
  --mode csv \
  --output results.csv
```

**How it works:**
- Each CSV row specifies one file
- Direct file-to-dataset mapping
- Manual file specification required
- Fine-grained control over metadata

### Upload Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--api-key` | ✅ | NAKALA API authentication key | `$NAKALA_API_KEY` |
| `--dataset` | ✅ | Path to CSV metadata file | `data_items.csv` |
| `--mode` | | Upload mode: folder or csv | `folder` (default) |
| `--base-path` | | Base directory for file paths | `./data` |
| `--output` | | Results output file | `results.csv` |
| `--timeout` | | Request timeout in seconds | `300` |
| `--max-retries` | | Maximum retry attempts | `3` |
| `--verbose` | | Detailed output logging | Flag |

### CSV Format for Uploads

#### Required Fields
```csv
file,status,type,title
data/results.csv,pending,http://purl.org/coar/resource_type/c_ddb1,"Research Results"
```

#### Complete Format
```csv
file,status,type,title,alternative,creator,contributor,date,license,description,keywords,language,temporal,spatial,accessRights,identifier,rights
```

> **📖 Complete CSV specification:** [CSV Format Guide](CSV_FORMAT_GUIDE.md)

### Upload Response Format

**Success Response:**
```csv
file,nakala_id,status,upload_date,metadata_count
data.csv,10.34847/nkl.abc123,success,2024-03-15T10:30:00,15
```

**Error Response:**
```csv
file,nakala_id,status,upload_date,error_message
bad_file.csv,,error,2024-03-15T10:30:00,"File not found: bad_file.csv"
```

### Common Upload Errors

| Error Type | Cause | Solution |
|------------|-------|----------|
| File not found | Path issues, permissions | Check file paths, use `--validate-files` |
| Metadata validation | Missing required fields | Use `o-nakala-preview --validate` |
| API timeout | Large files, slow connection | Increase `--timeout`, reduce batch size |
| Authentication | Invalid API key | Verify API key and environment |

---

## Collection Operations

### Overview
Collection operations (`o-nakala-collection`) organize uploaded datasets into logical collections using folder pattern matching or explicit assignment.

### Collection Workflow
```
Upload Data Items → Generate Upload Report → Create Collections CSV → Run Collection Creation → Organized Collections
```

### Collection Modes

#### Folder Pattern Mode (Recommended)
**Use case:** Automatic dataset organization based on folder structures

```bash
# Create collections from upload results
o-nakala-collection \
  --api-key "$NAKALA_API_KEY" \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv
```

**Collection CSV Format:**
```csv
collection_name,description,keywords,rights,status
"Research Data 2024","Complete research dataset collection","research;2024;data","CC-BY-4.0","pending"
```

#### Explicit ID Mode (Advanced)
**Use case:** Precise control over collection membership

```bash
# Create collections with specific dataset IDs
o-nakala-collection \
  --api-key "$NAKALA_API_KEY" \
  --from-ids dataset_ids.csv \
  --collection-config collection_config.csv
```

### Collection Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--api-key` | ✅ | NAKALA API authentication key | `$NAKALA_API_KEY` |
| `--from-upload-output` | | Use upload results as source | `upload_results.csv` |
| `--from-folder-collections` | | Collection definitions | `collections.csv` |
| `--from-ids` | | Explicit dataset IDs | `ids.csv` |
| `--collection-config` | | Collection metadata | `config.csv` |
| `--output` | | Results output file | `collection_results.csv` |

### Collection Patterns

#### Folder Pattern Matching
```csv
# Pattern examples
data_items,collection_name
"files/code/",,"Code Collection"
"files/data/|files/results/","Data and Results Collection"
"files/images/","Image Collection"
```

#### Collection Hierarchy
```csv
# Parent-child relationships
collection_name,parent_collection,description
"Project 2024","","Main project collection"
"Data Subset","Project 2024","Subset of main project"
"Analysis Results","Project 2024","Analysis outputs"
```

---

## Curator Operations

### Overview
Curator operations (`o-nakala-curator`) provide quality management, metadata enhancement, and validation tools for maintaining high-quality NAKALA repositories.

### Quality Analysis

#### Quality Reports
```bash
# Generate comprehensive quality report
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --scope all \
  --output quality_report.csv
```

#### Scope Options
- `all` - All user data
- `collections` - Collection-level analysis
- `recent` - Recently uploaded items
- `failed` - Items with validation issues

### Metadata Enhancement

#### Completeness Analysis
```bash
# Analyze metadata completeness
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --completeness-check \
  --threshold 80 \
  --output completeness_report.csv
```

#### Field Validation
```bash
# Validate specific metadata fields
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --validate-fields \
  --fields creator,title,description \
  --output validation_report.csv
```

### Curator Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--api-key` | ✅ | NAKALA API authentication key | `$NAKALA_API_KEY` |
| `--quality-report` | | Generate quality analysis | Flag |
| `--completeness-check` | | Check metadata completeness | Flag |
| `--validate-fields` | | Validate specific fields | Flag |
| `--scope` | | Analysis scope | `all`, `collections`, `recent` |
| `--threshold` | | Quality threshold (%) | `80` |
| `--output` | | Results output file | `report.csv` |

### Quality Metrics

#### Completeness Scoring
```
Excellent (90-100%): All recommended fields present
Good (70-89%): Core fields present, some optional missing  
Adequate (50-69%): Required fields present, many optional missing
Poor (<50%): Missing required or core fields
```

#### Field Priority Levels
- **Critical:** title, creator, type, status
- **Important:** description, date, license, keywords
- **Recommended:** alternative, contributor, temporal, spatial
- **Optional:** identifier, rights, accessRights

---

## User Operations

### Overview
User operations (`o-nakala-user-info`) provide account information, permission management, and usage statistics.

### Account Information
```bash
# Get complete user profile
o-nakala-user-info \
  --api-key "$NAKALA_API_KEY" \
  --profile
```

### Data Overview
```bash
# List all collections
o-nakala-user-info \
  --api-key "$NAKALA_API_KEY" \
  --collections-only

# List recent uploads
o-nakala-user-info \
  --api-key "$NAKALA_API_KEY" \
  --recent-uploads \
  --days 7
```

### Usage Statistics
```bash
# Generate usage report
o-nakala-user-info \
  --api-key "$NAKALA_API_KEY" \
  --usage-stats \
  --format json \
  --output usage_report.json
```

---

## Python API

### Installation and Setup
```python
# Install with Python API support
pip install o-nakala-core[api,cli]

from o_nakala_core import NakalaUserInfoClient, NakalaCuratorClient
```

### Upload Operations
```python
# Import from specific modules
from o_nakala_core.upload import NakalaUploadClient
from o_nakala_core.collection import NakalaCollectionClient

# Initialize uploader
uploader = NakalaUploadClient(
    api_key="your-api-key",
    api_url="https://api.nakala.fr"  # or test environment
)

# Upload from CSV
results = uploader.upload_from_csv(
    csv_file="data_items.csv",
    mode="folder",
    base_path="./data"
)

# Check results
for result in results:
    print(f"File: {result['file']}, Status: {result['status']}")
```

### Collection Management
```python
from o_nakala_core import NakalaCollection

# Initialize collection manager
collections = NakalaCollectionClient(api_key="your-api-key")

# Create collections from upload results
collection_results = collections.create_from_upload(
    upload_results=results,
    collection_config="collections.csv"
)

# List user collections
user_collections = collections.list_collections()
```

### Quality Management
```python
from o_nakala_core import NakalaCurator

# Initialize curator
curator = NakalaCurator(api_key="your-api-key")

# Generate quality report
quality_report = curator.generate_quality_report(
    scope="all",
    include_suggestions=True
)

# Check completeness
completeness = curator.check_completeness(
    threshold=80,
    fields=["title", "creator", "description"]
)
```

### Error Handling
```python
from o_nakala_core.exceptions import NakalaError, NakalaAPIError

try:
    results = uploader.upload_from_csv("data.csv")
except NakalaAPIError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
except NakalaError as e:
    print(f"General Error: {e}")
```

---

## CLI Reference

### Command Overview
| Command | Purpose | Documentation |
|---------|---------|---------------|
| `o-nakala-preview` | Validate and preview before upload | [Preview Guide](#preview-operations) |
| `o-nakala-upload` | Upload files to NAKALA | [Upload Operations](#upload-operations) |
| `o-nakala-collection` | Create and manage collections | [Collection Operations](#collection-operations) |
| `o-nakala-curator` | Quality management and validation | [Curator Operations](#curator-operations) |
| `o-nakala-user-info` | Account and usage information | [User Operations](#user-operations) |

### Preview Operations
```bash
# Interactive validation and preview
o-nakala-preview --csv your_data.csv --interactive

# Quick validation only
o-nakala-preview --csv your_data.csv --validate-only

# Export detailed preview
o-nakala-preview --csv your_data.csv --json-output preview.json

# Validate file accessibility
o-nakala-preview --csv your_data.csv --validate-files
```

### Global Parameters
All commands support these common parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--api-key` | NAKALA API key | `$NAKALA_API_KEY` |
| `--api-url` | NAKALA API endpoint | `https://api.nakala.fr` |
| `--timeout` | Request timeout (seconds) | `300` |
| `--verbose` | Detailed logging | Flag |
| `--help` | Command help | Flag |

### Environment Variables
```bash
# Set default API configuration
export NAKALA_API_KEY="your-api-key"
export NAKALA_API_URL="https://api.nakala.fr"
export NAKALA_TIMEOUT=300
```

---

## Integration Patterns

### Batch Processing
```python
# Process large datasets in chunks
def batch_upload(csv_file, batch_size=50):
    df = pd.read_csv(csv_file)
    batches = [df[i:i+batch_size] for i in range(0, len(df), batch_size)]
    
    results = []
    for i, batch in enumerate(batches):
        batch_file = f"batch_{i}.csv"
        batch.to_csv(batch_file, index=False)
        
        batch_results = uploader.upload_from_csv(batch_file)
        results.extend(batch_results)
        
        # Rate limiting
        time.sleep(30)
    
    return results
```

### Automated Workflows
```python
# Complete automated workflow
def automated_research_workflow(project_dir):
    # 1. Validate and preview
    preview = preview_tool.validate_directory(project_dir)
    if not preview.valid:
        raise ValueError("Validation failed")
    
    # 2. Upload files
    upload_results = uploader.upload_from_csv(
        f"{project_dir}/data_items.csv"
    )
    
    # 3. Create collections
    collections = collection_manager.create_from_upload(upload_results)
    
    # 4. Quality check
    quality_report = curator.generate_quality_report()
    
    # 5. Return summary
    return {
        'uploaded': len(upload_results),
        'collections': len(collections),
        'quality_score': quality_report.average_score
    }
```

### Error Recovery
```python
# Robust upload with retry logic
def resilient_upload(csv_file, max_retries=3):
    for attempt in range(max_retries):
        try:
            results = uploader.upload_from_csv(csv_file)
            return results
        except NakalaAPIError as e:
            if e.status_code == 503 and attempt < max_retries - 1:
                # Server overloaded, wait and retry
                time.sleep(60 * (attempt + 1))
                continue
            raise
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(30)
                continue
            raise
```

---

## Advanced Configuration

### Custom Metadata Transformation
```python
# Custom field mapping
field_mappings = {
    'custom_title': 'title',
    'author_name': 'creator', 
    'subject_terms': 'keywords'
}

uploader.set_field_mappings(field_mappings)
```

### Validation Rules
```python
# Custom validation rules
validation_rules = {
    'title': {'required': True, 'min_length': 5},
    'creator': {'required': True, 'format': 'LastName,FirstName'},
    'keywords': {'separator': ';', 'min_count': 3}
}

preview_tool.set_validation_rules(validation_rules)
```

### Performance Tuning
```python
# Optimize for large uploads
uploader.configure(
    chunk_size=1024*1024*10,  # 10MB chunks
    parallel_uploads=3,        # Concurrent uploads
    retry_backoff=2.0,        # Exponential backoff
    connection_pool_size=10    # HTTP connection pool
)
```

---

## 🧭 Navigation

### ⬅️ Previous Steps
- [Getting Started](GETTING_STARTED.md) - Basic setup and concepts
- [CSV Format Guide](CSV_FORMAT_GUIDE.md) - Metadata format reference

### ➡️ Next Steps  
- **Implementation**: [User Workflow Guides](user-guides/) - Step-by-step processes
- **Advanced Usage**: [Feature Showcase](guides/feature-showcase.md) - Explore capabilities
- **Production**: [Best Practices](../examples/workflow_documentation/best-practices.md) - Enterprise deployment

### 🔍 Related Resources
- [Field Reference](curator-field-reference.md) - Complete metadata specification
- [Troubleshooting](user-guides/05-troubleshooting.md) - Common issues and solutions
- [Examples](../examples/) - Working code and data samples

### 🆘 Need Help?
- **API issues**: Check [troubleshooting section](user-guides/05-troubleshooting.md#api-errors)
- **Python integration**: Review [examples directory](../examples/)
- **Community support**: [GitHub Issues](https://github.com/xy-liao/o-nakala-core/issues)

---

*📍 **You are here:** [START_HERE](../START_HERE.md) → [Getting Started](GETTING_STARTED.md) → API Reference*

*Complete technical specification for O-Nakala Core integration. Last updated: August 2025*