# NAKALA Client Documentation

Complete documentation for the NAKALA Python client library.

## 📚 User Guides

### [🚀 Quick Start](../README.md#quick-start)
Get up and running in 5 minutes with installation and basic usage.

### [📤 Upload Guide](user-guides/01-upload-guide.md)
Complete guide to uploading research data and datasets.

### [📚 Collection Guide](user-guides/02-collection-guide.md)
Learn how to organize datasets into thematic collections.

### [📋 Workflow Guide](user-guides/03-workflow-guide.md)
End-to-end workflows for digital humanities research.

### [🔧 Migration Guide](user-guides/04-v2-migration-guide.md)
Migrating from v1.0 to v2.0 (if using legacy scripts).

### [❓ FAQ](user-guides/05-faq.md)
Frequently asked questions and troubleshooting.

### [🛠️ Troubleshooting](user-guides/troubleshooting.md)
Common issues and solutions.

## 🔧 Curator Documentation

### [📋 Curator Field Reference](curator-field-reference.md)
Complete field reference for data curation with all supported fields, formats, and examples.

### [🔗 Property URI Mapping](property-uri-mapping.md)
Detailed mapping between CSV fields and NAKALA/Dublin Core property URIs.

## 📁 Examples

### [Sample Dataset](../examples/sample_dataset/)
Complete example with academic research data including:
- Multi-language metadata configuration
- Folder-based organization (code, data, documents, images, presentations)
- Collection definitions

### [Simple Dataset](../examples/simple-dataset/)
Minimal example for quick testing with bird images.

## 🎓 Interactive Learning

### [Workshop](../o-nakala-workshop/)
Hands-on Jupyter notebook covering the complete workflow:
- Data upload (5 datasets, 14 files)
- Collection creation (3 thematic collections)
- Quality curation and analysis

```bash
cd o-nakala-workshop
pip install -r requirements.txt
jupyter lab NAKALA_Complete_Workflow.ipynb
```

## 🔧 CLI Reference

### Core Commands

```bash
# Upload data
nakala-upload --help

# Manage collections  
nakala-collection --help

# Data curation
nakala-curator --help

# Show complete field reference
nakala-curator --list-fields

# Account information
nakala-user-info --help
```

### Environment Setup

```bash
# Required
export NAKALA_API_KEY="your-api-key"

# Optional (defaults to test environment)
export NAKALA_BASE_URL="https://apitest.nakala.fr"
```

## 🌐 External Resources

- **[NAKALA Platform](https://nakala.fr)** - Main repository platform
- **[Test Environment](https://apitest.nakala.fr)** - Safe testing environment
- **[API Documentation](https://api.nakala.fr/swagger-ui/)** - Complete API reference
- **[xy-liao/o-nakala-core](https://github.com/xy-liao/o-nakala-core)** - Project repository

## 🚀 Quick Examples

### Complete Workflow
```bash
# 1. Upload datasets
nakala-upload \
  --api-url "https://apitest.nakala.fr" \
  --api-key "YOUR_KEY" \
  --mode folder \
  --dataset "../examples/sample_dataset/folder_data_items.csv" \
  --base-path "../examples/sample_dataset"

# 2. Create collections
nakala-collection \
  --api-url "https://apitest.nakala.fr" \
  --api-key "YOUR_KEY" \
  --from-upload-output "upload_results.csv"

# 3. Analyze quality
nakala-curator \
  --api-url "https://apitest.nakala.fr" \
  --api-key "YOUR_KEY" \
  --quality-report \
  --output "quality_report.json"
```

---

**📖 Need help?** Start with the [User Guides](user-guides/) or try the [Interactive Workshop](../o-nakala-workshop/).