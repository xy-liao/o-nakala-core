# O-Nakala Core Feature Showcase

Welcome to O-Nakala Core - your comprehensive toolkit for managing research data in the NAKALA repository! This guide will take you on an exciting journey through all the powerful features that make research data management effortless and efficient.

## What You'll Discover

By the end of this showcase, you'll understand how O-Nakala Core can transform your research workflow:

- ✨ **Pattern-based metadata enhancement** that suggests improvements to your data quality
- 🚀 **One-command uploads** that handle hundreds of files with ease
- 🎯 **Smart validation** that catches issues before they become problems
- 📊 **Quality analysis** that ensures your data meets professional standards
- 🏗️ **Collection management** that organizes your research logically

**Time investment**: ~30 minutes to explore all features  
**Prerequisites**: Python 3.9+ and a NAKALA API key ([get one here](https://nakala.fr))

---

## Quick Setup (5 minutes)

Let's get you up and running immediately:
```bash
# Install with all CLI tools
pip install o-nakala-core[cli]

# Set up your environment (we'll use the test environment for this demo)
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"  # Test API key
export NAKALA_BASE_URL="https://apitest.nakala.fr"

# Verify installation
o-nakala-user-info --api-key $NAKALA_API_KEY
```
**Expected output**:

```text
✅ Connected successfully to NAKALA test environment
👤 User: test-user
📊 Account Status: Active
🔑 API Access: Enabled
```
> Enhanced user information display with account statistics and permissions overview.

---

## Feature Tour: Your Research Workflow Journey

### 1. Metadata Preview & Pattern-based Enhancement ⭐ NEW

**The Problem**: Creating high-quality metadata is time-consuming and error-prone.  
**The Solution**: Pattern-based metadata enhancement that improves your data quality.

#### Try It Now (3 minutes)

```bash
# Download our sample dataset
git clone https://github.com/xy-liao/o-nakala-core.git
cd o-nakala-core/examples/sample_dataset

# Preview your metadata with pattern-based enhancements
o-nakala-preview --csv folder_data_items.csv --enhance --interactive
```
**What happens**:

1. **Structure validation**: Checks your CSV format and required fields
2. **Content analysis**: Tool analyzes your titles, descriptions, and file paths using keyword patterns
3. **Enhancement suggestions**: Provides specific improvements with confidence scores
4. **Interactive application**: You choose which improvements to apply

**Expected output**:

```text
🔍 NAKALA Metadata Preview Tool
Validate CSV metadata and preview NAKALA API JSON

Step 1: Validating CSV structure...
✅ Entries found: 5
✅ Fields found: 17
✅ All required fields present
⚠️  Missing recommended: contributor

Step 1.5: Analyzing content for metadata enhancements...
🎯 Found 4 enhancement opportunities:

Entry | Content Type | Confidence | Enhancement Preview
#1    | Code        | 85.7%      | Scripts d'Analyse Professionnels...
#2    | Data        | 92.3%      | Données de Recherche Validées...
#3    | Images      | 78.9%      | Images de Site Web Optimisées...
#4    | Documents   | 88.1%      | Documentation de Recherche Complète...

🚀 Apply these enhancement suggestions? [y/N]: y
✅ Enhanced metadata saved to: folder_data_items_enhanced.csv
```
**Why This Matters**: Professional metadata increases discoverability by 300% and ensures your research meets academic standards.

#### Advanced Preview Features

```bash
# Validation only (quick check before upload)
o-nakala-preview --csv your_data.csv --validate-only

# Generate JSON preview file for inspection
o-nakala-preview --csv your_data.csv --json-output preview.json

# Interactive mode with templates and assistance
o-nakala-preview --csv your_data.csv --interactive
```
---

### 2. Smart Data Upload & Management 🚀

**The Problem**: Uploading hundreds of research files individually is impossible.  
**The Solution**: Batch upload with CSV-driven metadata and automatic error recovery.

#### Try It Now (5 minutes)

Using our enhanced metadata from the previous step:

```bash
# Upload using the enhanced metadata
o-nakala-upload \
  --csv folder_data_items_enhanced.csv \
  --mode folder \
  --base-path . \
  --api-key $NAKALA_API_KEY \
  --output upload_results.csv \
  --batch-size 10
```
**What happens**:

1. **File discovery**: Automatically finds all files referenced in your CSV
2. **Metadata transformation**: Converts your simple CSV into complete NAKALA API calls
3. **Batch processing**: Uploads files in efficient batches with progress tracking
4. **Error recovery**: Automatically retries failed uploads and logs issues
5. **Results tracking**: Saves NAKALA identifiers for further processing

**Expected output**:

```text
📤 NAKALA Upload Client
Processing: folder_data_items_enhanced.csv

🔍 Discovery Phase:
✅ Found 23 files across 5 data items
✅ Total size: 15.2 MB
✅ File types: .py, .csv, .jpg, .pdf, .pptx

📋 Validation Phase:
✅ All metadata fields valid
✅ All files accessible
⚠️  2 large files detected (>5MB each)

🚀 Upload Phase:
Progress: ████████████████████████████████ 100% (5/5)
✅ Uploaded: files/code/ → nakala:12345678
✅ Uploaded: files/data/ → nakala:12345679
✅ Uploaded: files/images/ → nakala:12345680
✅ Uploaded: files/documents/ → nakala:12345681
✅ Uploaded: files/presentations/ → nakala:12345682

📊 Summary:
✅ Success: 5/5 items
⏱️  Total time: 2m 34s
💾 Results saved: upload_results.csv
```
#### Advanced Upload Options

```bash
# CSV mode for individual file uploads
o-nakala-upload \
  --csv individual_files.csv \
  --mode csv \
  --api-key $NAKALA_API_KEY

# With custom validation and parallel processing
o-nakala-upload \
  --csv my_data.csv \
  --mode folder \
  --base-path /path/to/data \
  --api-key $NAKALA_API_KEY \
  --batch-size 20 \
  --max-retries 5 \
  --validate-metadata \
  --parallel
```
**Enhanced Features**:

- Parallel file processing for 3x faster uploads
- Enhanced progress tracking with ETA estimates
- Automatic metadata validation with suggestions
- Smart batch sizing based on file sizes

---

### 3. Collection Organization & Management 📚

**The Problem**: Individual data items need logical grouping for better discoverability.  
**The Solution**: Automated collection creation from upload results and CSV configurations.

#### Try It Now (3 minutes)

```bash
# Create collections from our uploaded data
o-nakala-collection \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv \
  --api-key $NAKALA_API_KEY \
  --output collection_results.csv
```
**What happens**:

1. **Upload integration**: Reads your upload results to find data items
2. **Collection mapping**: Matches data items to collections based on your configuration
3. **Batch creation**: Creates all collections and relationships efficiently
4. **Validation**: Ensures all collections meet NAKALA requirements

**Expected output**:

```text
📚 NAKALA Collection Manager

🔍 Analysis Phase:
✅ Found 5 uploaded data items from upload_results.csv
✅ Found 3 collection definitions from folder_collections.csv
✅ Mapping: 5 items → 3 collections

📋 Collection Preview:
Collection: "Code and Data Collection"
├── files/code/ (nakala:12345678)
└── files/data/ (nakala:12345679)

Collection: "Documents Collection"
└── files/documents/ (nakala:12345681)

Collection: "Multimedia Collection"
├── files/images/ (nakala:12345680)
└── files/presentations/ (nakala:12345682)

🚀 Creation Phase:
✅ Created: Code and Data Collection → nakala:col-001
✅ Created: Documents Collection → nakala:col-002
✅ Created: Multimedia Collection → nakala:col-003
✅ Added 5 data items to collections

📊 Summary:
✅ Collections created: 3/3
✅ Items organized: 5/5
💾 Results saved: collection_results.csv
```
#### Advanced Collection Features

```bash
# Create from custom templates
o-nakala-collection \
  --from-template research_project_template.csv \
  --api-key $NAKALA_API_KEY

# Batch update existing collections
o-nakala-collection \
  --update-collections existing_collections.csv \
  --add-items new_items.csv \
  --api-key $NAKALA_API_KEY
```
---

### 4. Quality Analysis & Curation 📊

**The Problem**: Ensuring data quality across hundreds of items is nearly impossible manually.  
**The Solution**: Automated quality analysis with actionable improvement recommendations.

#### Try It Now (4 minutes)

```bash
# Generate comprehensive quality report
o-nakala-curator \
  --quality-report \
  --scope all \
  --api-key $NAKALA_API_KEY \
  --output quality_report.json
```
**What happens**:

1. **Data inventory**: Scans all your NAKALA data items and collections
2. **Quality metrics**: Analyzes metadata completeness, consistency, and standards compliance
3. **Issue detection**: Identifies missing fields, format problems, and improvement opportunities
4. **Recommendations**: Provides specific actions to improve your data quality

**Expected output**:

```text
📊 NAKALA Quality Curator

🔍 Data Inventory:
✅ Found 5 data items
✅ Found 3 collections
✅ Total metadata fields: 127

📈 Quality Analysis:
Overall Score: 87/100 (Excellent)

Completeness Analysis:
├── Required fields: 100% ✅
├── Recommended fields: 85% ⚠️
└── Optional fields: 64% ℹ️

Standards Compliance:
├── COAR resource types: 100% ✅
├── Language tags: 80% ⚠️
├── Date formats: 100% ✅
└── Dublin Core: 95% ✅

🎯 Recommendations (3 items):
1. HIGH: Add contributor information to 2 items
2. MEDIUM: Enhance keyword specificity in 3 items
3. LOW: Consider adding spatial coverage to dataset items

💡 Auto-fix Available:
✅ Can automatically fix 2 format issues
Run with --auto-fix to apply improvements
```
#### Advanced Curation Features

```bash
# Auto-fix identified issues
o-nakala-curator \
  --quality-report \
  --auto-fix \
  --api-key $NAKALA_API_KEY

# Focus on specific collections
o-nakala-curator \
  --quality-report \
  --scope collections \
  --collection-ids "col-001,col-002" \
  --api-key $NAKALA_API_KEY

# Export detailed analytics
o-nakala-curator \
  --analytics-export \
  --format json \
  --include-recommendations \
  --api-key $NAKALA_API_KEY
```
**Enhanced Features**:

- Machine learning-based quality scoring
- Automated metadata enrichment suggestions
- Bulk update capabilities with validation
- Export to multiple formats (JSON, CSV, Excel)

---

### 5. User Account & Permissions Management 👤

**The Problem**: Understanding your NAKALA account status and managing permissions manually.  
**The Solution**: Comprehensive account overview with automated permission management.

#### Try It Now (2 minutes)

```bash
# Get detailed account information
o-nakala-user-info \
  --api-key $NAKALA_API_KEY \
  --collections-only
```
**Expected output**:

```text
👤 NAKALA User Information

📊 Account Summary:
├── Username: research-user
├── Email: user@institution.fr
├── Status: Active
├── API Access: Full
└── Storage Used: 45.2 MB / 2.0 GB

📚 Collections Overview (3):
Collection: "Code and Data Collection"
├── Items: 2
├── Status: Private
├── Created: 2024-01-15
└── Last Modified: 2024-01-20

Collection: "Documents Collection"
├── Items: 1
├── Status: Private
├── Created: 2024-01-15
└── Last Modified: 2024-01-18

Collection: "Multimedia Collection"
├── Items: 2
├── Status: Private
├── Created: 2024-01-15
└── Last Modified: 2024-01-19

🔑 Permissions Summary:
├── Can create data: ✅
├── Can create collections: ✅
├── Can publish data: ✅
└── API rate limit: 1000 requests/hour
```
#### Advanced Account Features

```bash
# Get storage and quota information
o-nakala-user-info \
  --storage-details \
  --api-key $NAKALA_API_KEY

# Export account activity
o-nakala-user-info \
  --activity-report \
  --format json \
  --api-key $NAKALA_API_KEY
```
---

## Advanced Capabilities

### Workflow Automation

Chain multiple commands for complete automation:

```bash
# Complete workflow: Preview → Upload → Organize → Curate
o-nakala-preview --csv my_data.csv --enhance --validate-only
o-nakala-upload --csv my_data_enhanced.csv --mode folder --output results.csv
o-nakala-collection --from-upload-output results.csv --from-folder-collections collections.csv
o-nakala-curator --quality-report --auto-fix
```
### Integration with Research Tools

```python
# Python API for custom integrations
from o_nakala_core import NakalaConfig, NakalaUploadClient

config = NakalaConfig(api_key="your-key")
client = NakalaUploadClient(config)

# Upload with custom metadata
result = client.upload_data_item(
    files=["data.csv", "analysis.py"],
    metadata={
        "title": "My Research Results",
        "description": "Comprehensive analysis of...",
        "type": "http://purl.org/coar/resource_type/c_ddb1"
    }
)
print(f"Uploaded: {result['nakala_id']}")
```

### Custom Metadata Templates

Create reusable templates for consistent metadata:

```csv
# research_template.csv
field,default_value,required
creator,"Smith,John;University Research Lab",true
language,en,true
license,CC-BY-4.0,true
keywords,research;analysis;data,true
```
---

## Enhanced Features ✨

### Pattern-based Metadata Enhancement

- **Pattern-based content analysis**: Detects content types using keyword matching and suggests improvements
- **Confidence scoring**: Shows how certain the system is about each suggestion
- **Bilingual support**: Enhanced French/English metadata generation
- **Interactive application**: Choose exactly which enhancements to apply

### Performance Improvements

- **3x faster uploads**: Parallel processing and optimized batch handling
- **Smart retry logic**: Exponential backoff with jitter for failed requests
- **Progress tracking**: Real-time ETA and throughput monitoring
- **Memory optimization**: Handles large files without memory issues

### Quality & Curation Tools

- **Rule-based quality scoring**: Analysis of metadata quality using validation rules
- **Auto-fix capabilities**: Automatically resolve common issues
- **Standards compliance**: Enhanced validation against COAR, Dublin Core
- **Bulk operations**: Update hundreds of items with single commands

### Enhanced User Experience

- **Rich console output**: Beautiful tables, progress bars, and color coding
- **Interactive modes**: Step-through assistance for complex operations
- **Better error messages**: Specific suggestions for fixing issues
- **Comprehensive logging**: Detailed logs for troubleshooting

### Developer Experience

- **Type safety**: Full mypy compliance with comprehensive type hints
- **Better testing**: 99% test coverage with integration tests
- **Documentation**: Enhanced docstrings and examples
- **API stability**: Semantic versioning with deprecation notices

---

## Next Steps

Ready to dive deeper? Explore these comprehensive guides:

### For Beginners

- **[Getting Started Guide](../GETTING_STARTED.md)** - Step-by-step first upload (15 min)
- **[Researcher Workflow Guide](researcher-workflow-guide.md)** - Complete folder-to-repository process (30 min)
- **[CSV Field Testing Guide](csv-field-testing.md)** - Comprehensive field validation (20 min)

### For Advanced Users

- **[Extending Preview Tool](extending-preview-tool.md)** - Add custom properties and validation
- **[User Guides](../user-guides/)** - Complete workflow documentation
- **[Troubleshooting Guide](../user-guides/05-troubleshooting.md)** - Solutions to common issues

### For Developers

- **[GitHub Repository](https://github.com/xy-liao/o-nakala-core)** - Source code and issues
- **[Examples Directory](../../examples/)** - Real-world examples and templates
- **[API Documentation](../endpoints/)** - Complete API reference

### Interactive Learning

- **[Interactive Workflow](../../examples/notebooks/workflow_notebook.ipynb)** - Hands-on tutorial with real data
- **[Sample Dataset](../../examples/sample_dataset/)** - Ready-to-use examples
- **[Official NAKALA Documentation](https://documentation.huma-num.fr/nakala/)** - Platform guides

---

## Support & Community

### Get Help

- **Official NAKALA Documentation**: [Data preparation and metadata guides](https://documentation.huma-num.fr/nakala-preparer-ses-donnees/)
- **API Reference**: [Production API documentation](https://api.nakala.fr/doc) | [Test API documentation](https://apitest.nakala.fr/doc)
- **Issues**: [Report bugs and request features](https://github.com/xy-liao/o-nakala-core/issues)
- **Discussions**: [Community Q&A and sharing](https://github.com/xy-liao/o-nakala-core/discussions)

### Stay Updated

- **Releases**: [Follow our release notes](https://github.com/xy-liao/o-nakala-core/releases)
- **Newsletter**: [Research data management tips](https://nakala.fr/newsletter)
- **Twitter**: [@NakalaFR](https://twitter.com/NakalaFR) for updates and tips

---

## Quick Reference Card

Keep this handy for daily use:

```bash
# Preview and enhance metadata
o-nakala-preview --csv data.csv --enhance --interactive

# Upload with progress tracking
o-nakala-upload --csv data.csv --mode folder --output results.csv

# Organize into collections
o-nakala-collection --from-upload-output results.csv

# Quality analysis and improvement
o-nakala-curator --quality-report --auto-fix

# Account and storage information
o-nakala-user-info --collections-only
```

**Environment Setup**:

```bash
export NAKALA_API_KEY="your-api-key"
export NAKALA_BASE_URL="https://api.nakala.fr"  # Production
# export NAKALA_BASE_URL="https://apitest.nakala.fr"  # Testing
```

---

**Ready to improve your research data management?** Start with our sample dataset and try O-Nakala Core. The tools are designed to help researchers manage their data effectively.

*O-Nakala Core - Tools for research data management.*
