# Getting Started with O-Nakala Core

**Transform your research files into a professionally managed NAKALA repository in 15 minutes.**

This guide covers installation, first upload, and essential concepts. For role-specific paths, see [START_HERE.md](../START_HERE.md).

## What is NAKALA?

NAKALA is a French research data repository operated by Huma-Num, providing persistent identifiers, professional metadata standards, and long-term preservation for academic research. O-Nakala Core makes NAKALA accessible through simple command-line tools and Python integration.

## Prerequisites (5 minutes)

### 1. Python Environment
```bash
# Check Python version (3.9+ required)
python --version

# Create virtual environment (recommended)
python -m venv nakala-env
source nakala-env/bin/activate  # Windows: nakala-env\Scripts\activate
```

### 2. Installation
```bash
# Install with all features
pip install o-nakala-core[cli,ml]

# Verify installation
o-nakala-preview --help
```

### 3. NAKALA Account & API Key
1. Visit [nakala.fr](https://nakala.fr) and create an account
2. Generate an API key in your profile settings
3. For testing, use the public test environment

**Test Environment Setup:**
```bash
# Use test API key for learning
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_API_URL="https://apitest.nakala.fr"
```

**Production Environment:**
```bash
# Use your personal API key
export NAKALA_API_KEY="your-personal-api-key"
export NAKALA_API_URL="https://api.nakala.fr"
```

> **📖 Detailed API key setup**: [api/api_keys.md](../api/api_keys.md)

## Your First Successful Upload (10 minutes)

### Step 1: Get Sample Data
```bash
# Clone or download the sample dataset
cd examples/sample_dataset
ls
# You'll see: folder_data_items.csv, folder_collections.csv, files/
```

### Step 2: Preview Before Upload ⭐
**This is the game-changer that prevents 90% of upload failures.**

```bash
# Interactive validation - catches issues before upload
o-nakala-preview --csv folder_data_items.csv --interactive
```

**What the preview shows you:**
- ✅ Exact JSON metadata that NAKALA will receive
- ✅ File accessibility validation  
- ✅ Resource type suggestions for your content
- ✅ Metadata completeness analysis
- ✅ Common issues and fixes

### Step 3: Upload with Confidence
```bash
# Upload files to NAKALA
o-nakala-upload \
  --dataset folder_data_items.csv \
  --mode folder \
  --base-path . \
  --output upload_results.csv \
  --api-key $NAKALA_API_KEY
```

### Step 4: Organize into Collections
```bash
# Create logical collections
o-nakala-collection \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv \
  --api-key $NAKALA_API_KEY
```

### Step 5: Verify Success
```bash
# Check upload results
grep -c "success" upload_results.csv
echo "Successful uploads: $(grep -c success upload_results.csv)"

# View your data in NAKALA
o-nakala-user-info --api-key $NAKALA_API_KEY --collections-only
```

**🎉 Success!** You've uploaded research data with professional metadata, organized it into collections, and can now access it via persistent identifiers.

## Essential Commands Reference

### Preview and Validation
```bash
# Interactive preview (recommended for all users)
o-nakala-preview --csv your_data.csv --interactive

# Quick validation only  
o-nakala-preview --csv your_data.csv --validate-only

# Export preview for analysis
o-nakala-preview --csv your_data.csv --json-output preview.json
```

### File Upload
```bash
# Basic upload
o-nakala-upload --dataset data.csv --api-key $NAKALA_API_KEY

# Folder mode (files in subdirectories)
o-nakala-upload --dataset data.csv --mode folder --base-path ./files

# With result tracking
o-nakala-upload --dataset data.csv --output results.csv --api-key $NAKALA_API_KEY
```

### Collection Management
```bash
# Create from upload results
o-nakala-collection --from-upload-output results.csv --api-key $NAKALA_API_KEY

# Create from collection CSV
o-nakala-collection --from-folder-collections collections.csv --api-key $NAKALA_API_KEY
```

### Quality and Information
```bash
# Quality analysis
o-nakala-curator --quality-report --scope all --api-key $NAKALA_API_KEY

# User account information
o-nakala-user-info --api-key $NAKALA_API_KEY --collections-only
```

## Understanding Your Data Structure

### CSV Metadata Format
**Minimum required fields:**
```csv
file,status,type,title
data.pdf,pending,http://purl.org/coar/resource_type/c_6501,"My Research Document"
```

**Complete format (recommended):**
```csv
file,status,type,title,alternative,creator,contributor,date,license,description,keywords,language,temporal,spatial,accessRights,identifier,rights
```

### File Organization Best Practices
```
your_project/
├── data/              # Research data files
├── documents/         # Papers, reports, documentation  
├── code/             # Analysis scripts and software
├── images/           # Figures, photographs, diagrams
├── folder_data_items.csv      # Main metadata file
└── folder_collections.csv     # Collection organization
```

### Resource Types (COAR Standards)
Use these URIs in the `type` field:
- **Dataset**: `http://purl.org/coar/resource_type/c_ddb1`
- **Text/Article**: `http://purl.org/coar/resource_type/c_6501`  
- **Software**: `http://purl.org/coar/resource_type/c_5ce6`
- **Image**: `http://purl.org/coar/resource_type/c_c513`

> **📖 Complete field reference**: [curator-field-reference.md](curator-field-reference.md)

## Next Steps by Role

### 🎓 **Research-Focused Users**
- **[Research Workflow Guide](guides/researcher-workflow-guide.md)** - Complete folder-to-repository process
- **[Collection Organization](user-guides/02-collection-guide.md)** - Organize your research data

### 🔧 **Data Managers**  
- **[Complete Workflow](user-guides/03-workflow-guide.md)** - 6-step systematic process
- **[Quality Assurance](../examples/workflow_documentation/quality-assurance.md)** - Production-level QA

### 💻 **Developers**
- **[API Documentation](API_REFERENCE.md)** - Python integration and automation
- **[Extending Preview Tool](guides/extending-preview-tool.md)** - Customization and extension

### 🏛️ **Institutions**
- **[Institutional Setup](../examples/workflow_documentation/institutional-setup.md)** - Multi-user deployment
- **[Case Studies](examples/workflow_documentation/)** - Real-world implementation examples

## Common Issues and Solutions

### Upload Failures
```bash
# Check file permissions
ls -la your_files/
chmod 644 your_files/*  # Fix permission issues

# Validate before upload
o-nakala-preview --csv your_data.csv --validate-files
```

### Metadata Errors
```bash
# Use interactive preview to catch issues
o-nakala-preview --csv your_data.csv --interactive

# Check CSV format
head -5 your_data.csv  # Verify header and first few rows
```

### API Connectivity  
```bash
# Test API connection
curl -H "X-API-KEY: $NAKALA_API_KEY" $NAKALA_API_URL/users/me

# Check environment variables
echo $NAKALA_API_KEY
echo $NAKALA_API_URL
```

> **📖 Complete troubleshooting**: [user-guides/05-troubleshooting.md](user-guides/05-troubleshooting.md)

## Key Concepts to Remember

### Preview-First Workflow ⭐
**Always preview before upload.** The preview tool prevents 90% of failures and shows you exactly what NAKALA will receive.

### Metadata Quality Matters
Rich metadata makes your research discoverable and citable. O-Nakala Core helps you create professional-quality metadata effortlessly.

### Collections Provide Organization
Group related files into logical collections. This makes your research more navigable and professionally presented.

### Quality Assurance is Built-In
Use the curator tools to validate metadata completeness and maintain high-quality repositories.

## Support Resources

### Quick Help
- **Commands not working?** Check [troubleshooting guide](user-guides/05-troubleshooting.md)
- **CSV issues?** Use the [interactive preview](guides/csv-field-testing.md)
- **Need examples?** Browse [sample dataset](examples/sample_dataset/)

### Community Support
- **GitHub Issues**: [Report bugs](https://github.com/xy-liao/o-nakala-core/issues)
- **Documentation**: [Complete guides](https://github.com/xy-liao/o-nakala-core)
- **NAKALA Platform**: [Official support](https://nakala.fr)

### Advanced Resources
- **API Reference**: [NAKALA API docs](https://api.nakala.fr/doc)
- **Field Specifications**: [Metadata standards](curator-field-reference.md)
- **Best Practices**: [Production lessons](../examples/workflow_documentation/best-practices.md)

---

**🎯 You're ready to start!** This guide gave you the foundation. Choose your next step from the [role-specific paths above](#next-steps-by-role) or return to the [navigation guide](../START_HERE.md) for more options.

*Updated for O-Nakala Core v2.5.1 - Last revised: August 2025*