# O-Nakala Core

**🚀 [START HERE](START_HERE.md) for role-based navigation and quick setup**

A Python library and CLI toolkit for NAKALA research data repository workflows, designed for digital humanities and academic research teams.

## What is NAKALA?

NAKALA is a French research data repository platform operated by Huma-Num, designed for long-term preservation and sharing of academic research data. It serves French academic institutions including EFEO, BnF, and universities, providing a trusted environment for digital humanities and academic research data management.

## Why O-Nakala Core?

Managing research data through NAKALA's web interface can be time-consuming for large datasets. O-Nakala Core provides:
- **Batch upload capabilities** for hundreds of files with automated metadata
- **CSV-driven metadata management** for reproducible workflows
- **Quality validation and preview** before actual uploads
- **Complete Dublin Core support** with multilingual metadata
- **Automated collection organization** and curation tools

## Quick Access by Role

- **🎓 New to NAKALA**: [Getting Started Guide](docs/GETTING_STARTED.md) (15 min)
- **⚡ Need to upload now**: [Quick Upload Commands](docs/CSV_FORMAT_GUIDE.md#quick-start-minimum-viable-csv)
- **🔧 Setting up workflows**: [Complete Workflow Guide](docs/user-guides/03-workflow-guide.md)
- **💻 Developer integration**: [API Reference](docs/API_REFERENCE.md)
- **🏛️ Institutional deployment**: [Institutional Setup](examples/workflow_documentation/institutional-setup.md)
- **🚨 Having problems**: [Troubleshooting Guide](docs/user-guides/05-troubleshooting.md)

## Prerequisites

### NAKALA Account & API Access

1. **Create NAKALA Account**: Visit [nakala.fr](https://nakala.fr) and register
2. **Request API Access**: Contact your institution's NAKALA administrator
3. **Get API Key**: Find your API key in your NAKALA account settings

### For Testing & Evaluation

Use the public test environment to try O-Nakala Core:
- **Test API URL**: `https://apitest.nakala.fr`
- **Test API Key**: `33170cfe-f53c-550b-5fb6-4814ce981293`
- **Note**: Test data may be periodically cleaned

## Installation

```bash
# Complete installation with CLI tools (latest stable)
pip install o-nakala-core[cli]==2.5.1

# Core library only
pip install o-nakala-core

# Development installation from source
git clone https://github.com/xy-liao/o-nakala-core.git
cd o-nakala-core
pip install ".[cli,dev]"
```

### System Requirements

- **Python 3.9+** (tested through Python 3.13)
- Active NAKALA account with API access
- CSV files with research metadata

### Python 3.13 Users

For Python 3.13 compatibility, always use regular installation (not editable mode with `-e`):

```bash
# ✅ Correct (works on all Python versions including 3.13)
pip install ".[cli,dev]"

# ❌ Avoid (may fail on Python 3.13)
pip install -e ".[cli,dev]"
```

## Quick Start

### Python API
```python
from o_nakala_core import NakalaConfig, NakalaUserInfoClient

# Configure connection
config = NakalaConfig(api_key="your-api-key")

# Get user information
client = NakalaUserInfoClient(config)
user_info = client.get_user_info()
print(f"Connected as: {user_info['username']}")
```

### CLI Tools
```bash
# Set your API key
export NAKALA_API_KEY="your-api-key"

# Preview and validate metadata before upload
o-nakala-preview --csv your_data.csv --interactive

# Upload datasets from CSV
o-nakala-upload --csv your_data.csv --mode folder --folder-config your_data.csv --base-path ./ --api-key $NAKALA_API_KEY

# Create collections
o-nakala-collection --from-folder-collections collections.csv

# Quality analysis and curation
o-nakala-curator --quality-report --scope all
```

## CLI Commands

- **`o-nakala-upload`** - Batch upload datasets with CSV-driven metadata
- **`o-nakala-preview`** - Validate and preview metadata before upload
- **`o-nakala-collection`** - Create and manage thematic collections  
- **`o-nakala-curator`** - Metadata curation and quality analysis
- **`o-nakala-user-info`** - Account management and permissions

## Key Features

- **CSV-based workflows** for reproducible research data management
- **Metadata validation** with real-time feedback and suggestions
- **Complete Dublin Core support** for comprehensive metadata
- **Batch operations** for large-scale data uploads and collection management
- **Quality analysis** tools for metadata curation and enhancement
- **Multilingual metadata** support with French/English templates
- **Production-ready error handling** with comprehensive logging

## Basic Workflow

```bash
# 1. Prepare your data in CSV format
# See examples/sample_dataset/ for format reference

# 2. Validate metadata (recommended)
o-nakala-preview --csv folder_data_items.csv --interactive

# 3. Upload data
o-nakala-upload \
  --api-key $NAKALA_API_KEY \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path ./ \
  --output upload_results.csv

# 4. Create collections (optional)
o-nakala-collection \
  --api-key $NAKALA_API_KEY \
  --from-upload-output upload_results.csv \
  --from-folder-collections collections.csv

# 5. Quality check (recommended)
o-nakala-curator --api-key $NAKALA_API_KEY --quality-report
```

## CSV Format Examples

### Basic Research Data
**folder_data_items.csv**:
```csv
title,creator,description,type,file
"Research Analysis Scripts","Dupont,Jean","Python scripts for data analysis","http://purl.org/coar/resource_type/c_5ce6","code/analysis.py"
"Survey Results 2023","Martin,Claire","Raw survey data","http://purl.org/coar/resource_type/c_ddb1","data/survey.csv"
```

### Digital Humanities Project
```csv
title,creator,description,type,keywords,language,file
"Medieval Manuscript Transcription","Smith,Alice","Transcribed text from 14th century manuscript","http://purl.org/coar/resource_type/c_6501","medieval;manuscript;paleography","la","texts/manuscript_001.txt"
"Archaeological Site Photos","Jones,Bob","Excavation documentation photos","http://purl.org/coar/resource_type/c_c513","archaeology;excavation;photography","en","images/site_photos/"
```

### Scientific Research Dataset
```csv
title,creator,description,type,temporal,spatial,license,file
"Climate Data 2020-2024","Lab Team","Temperature and precipitation measurements","http://purl.org/coar/resource_type/c_ddb1","2020/2024","France","CC-BY-4.0","data/climate_measurements.csv"
"Research Protocol v2.1","Dr. Martin","Updated experimental protocol","http://purl.org/coar/resource_type/c_18cf","2024","Global","CC-BY-SA-4.0","protocols/experiment_v2.1.pdf"
```

The library automatically transforms simple CSV formats into complete NAKALA API metadata structures.

## Documentation Structure

Our streamlined documentation provides clear paths for every user type and experience level:

### 🚀 **Start Here**
- **[START_HERE.md](START_HERE.md)** - Role-based navigation to find exactly what you need
- **[Getting Started](docs/GETTING_STARTED.md)** - Installation, setup, and first successful upload

### 📚 **Learning Paths**
- **[Research Workflow](docs/guides/researcher-workflow-guide.md)** - Complete folder-to-repository process (45 min)
- **[Complete Workflow](docs/user-guides/03-workflow-guide.md)** - Systematic 6-step process (60 min)
- **[Feature Showcase](docs/guides/feature-showcase.md)** - Explore all capabilities (30 min)

### 🔧 **Technical Reference**
- **[API Reference](docs/API_REFERENCE.md)** - Complete API and Python integration guide
- **[CSV Format Guide](docs/CSV_FORMAT_GUIDE.md)** - Metadata format specifications
- **[Field Reference](docs/curator-field-reference.md)** - Complete metadata field guide

### 🏭 **Production Deployment**
- **[Best Practices](examples/workflow_documentation/best-practices.md)** - Production lessons learned
- **[Institutional Setup](examples/workflow_documentation/institutional-setup.md)** - Multi-user deployment
- **[Case Studies](examples/workflow_documentation/)** - Real-world implementation examples

## Environment Setup

```bash
# Required - Get API key from NAKALA platform
export NAKALA_API_KEY="your-api-key"

# Optional - Set environment (defaults to test)
export NAKALA_BASE_URL="https://apitest.nakala.fr"  # Test environment
# export NAKALA_BASE_URL="https://api.nakala.fr"     # Production
```

## Requirements

- Python 3.9+
- Active NAKALA account with API access
- CSV files with research metadata

## Troubleshooting

### Installation Issues

**Import Issues with Python 3.13+**: If you encounter `ModuleNotFoundError: No module named 'o_nakala_core'` after installation:

```bash
# ❌ This may fail on Python 3.13:
pip install -e ".[cli,dev]"

# ✅ Use this instead:
pip install ".[cli,dev]"
```

This is due to changes in Python 3.13's handling of editable installs with `.pth` files.

**CLI Commands Not Found**: If commands like `o-nakala-upload` are not available after installation:

```bash
# Ensure you installed CLI extras:
pip install o-nakala-core[cli]

# Or for development:
pip install ".[cli,dev]"

# Verify installation:
pip show o-nakala-core
```

### Upload Issues

**Missing `--folder-config` Parameter**: If you get validation errors about missing folder config:

```bash
# ❌ This will fail in folder mode:
o-nakala-upload --csv data.csv --mode folder

# ✅ Include required parameters:
o-nakala-upload --csv data.csv --mode folder --folder-config data.csv --base-path ./
```

**API Authentication Errors**: If you get 401/403 errors:

- Verify your API key is correct and active
- Check you're using the right environment (`apitest` vs `api`)
- Ensure your key has required permissions

```bash
# Test your connection:
o-nakala-user-info --api-key $NAKALA_API_KEY

# For testing, use the public test environment:
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_BASE_URL="https://apitest.nakala.fr"
```

**Path Resolution Errors**: If you encounter confusing path-related errors:

- Always use absolute paths when possible
- Ensure your `--base-path` directory exists and contains the referenced files
- Use `--validate-only` mode to test configuration without uploading

### CSV Format Issues

**Unknown Field Warnings**: The preview tool will show warnings for unrecognized fields, but they won't break uploads:

```
ℹ️  Unknown fields (will be ignored): custom_field, extra_column
```

**Missing Required Fields**: Essential fields must be present:

```
❌ Missing required fields: title, type
```

Required fields: `title`, `type`  
Recommended fields: `creator`, `description`, `keywords`

### Specific Error Codes and Solutions

**Error: `[VALIDATION_ERROR] Invalid configuration paths`**
- **Cause**: Missing or incorrect `--base-path` parameter
- **Solution**: Add `--base-path ./` for current directory or specify correct path
```bash
# ✅ Correct usage
o-nakala-upload --csv data.csv --mode folder --folder-config data.csv --base-path ./
```

**Error: `401 Unauthorized` or `403 Forbidden`**
- **Cause**: Invalid API key or insufficient permissions
- **Solution**: Verify API key and environment URL
```bash
# Test connection
o-nakala-user-info --api-key $NAKALA_API_KEY
# Check environment variables
echo $NAKALA_API_KEY && echo $NAKALA_BASE_URL
```

**Error: `FileNotFoundError` for referenced files**
- **Cause**: CSV references files that don't exist or are inaccessible
- **Solution**: Use preview tool to check file paths
```bash
o-nakala-preview --csv your_data.csv --validate-only
```

**Error: `ConnectionTimeout` or `RequestException`**
- **Cause**: Network connectivity issues or API downtime
- **Solution**: Check internet connection and try test environment
```bash
# Switch to test environment
export NAKALA_BASE_URL="https://apitest.nakala.fr"
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
```

### Platform Status and Alternatives

**If NAKALA platform is unavailable**:
- **Use test environment**: `https://apitest.nakala.fr` (often more stable)
- **Offline development**: Preview and validate CSV files without uploading
- **Alternative repositories**: Contact your institution for backup options
- **Working offline**: All validation and preview tools work without internet

**Emergency workflows**:
```bash
# Continue development without uploading
o-nakala-preview --csv your_data.csv --interactive

# Validate complete workflow offline
o-nakala-upload --dataset your_data.csv --validate-only --mode folder --base-path ./
```

### Getting Help

- **Full API Key Guide**: See `api/api_keys.md`
- **Sample Data**: Check `examples/sample_dataset/` for working examples  
- **Issues**: [GitHub Issues](https://github.com/xy-liao/o-nakala-core/issues)
- **NAKALA Platform**: [nakala.fr](https://nakala.fr) (primary) or use test environment as fallback

## Support

For issues, questions, and contributions:

- **Issues**: [GitHub Issues](https://github.com/xy-liao/o-nakala-core/issues)
- **Documentation**: [Project Repository](https://github.com/xy-liao/o-nakala-core)
- **NAKALA Platform**: [nakala.fr](https://nakala.fr)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please see the repository for development setup and contribution guidelines.

---

**Built for academic and research teams who need reliable, straightforward tools for research data management.**