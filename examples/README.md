# O-Nakala Core Examples

This directory contains example datasets, configurations, and workflows for learning and testing the O-Nakala Core system.

## 📁 Directory Structure

### `/sample_dataset/` - Complete Example Dataset
- **Purpose**: Comprehensive example with 14 files across 5 categories
- **Use case**: Full workflow testing, workshop training, API validation
- **Contents**:
  - `folder_data_items.csv` - Dataset metadata configuration
  - `folder_collections.csv` - Collection organization configuration
  - `files/` - Sample research files (images, code, documents, data, presentations)
  - Workshop exercise files for batch modifications

### `/simple-dataset/` - Minimal Example
- **Purpose**: Quick start example with image files
- **Use case**: Basic upload testing, simple workflows
- **Contents**: 4 bird images with basic configuration

### `/workflow_documentation/` - Process Documentation
- **Purpose**: Documented workflows and success metrics
- **Use case**: Understanding system capabilities and performance
- **Contents**: Workflow guides, success reports, process documentation

## 🚀 Quick Start

### 1. Basic Upload Test
```bash
cd simple-dataset
python -m src.o_nakala_core.cli.upload \
  --api-key YOUR_API_KEY \
  --dataset . \
  --mode folder
```

### 2. Complete Workflow Test
```bash
cd sample_dataset
# Upload data
python -m src.o_nakala_core.cli.upload \
  --api-key YOUR_API_KEY \
  --dataset folder_data_items.csv \
  --mode folder \
  --output upload_results.csv

# Create collections
python -m src.o_nakala_core.cli.collection \
  --api-key YOUR_API_KEY \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv
```

### 3. Workshop Exercises
```bash
cd sample_dataset
# Use provided workshop CSV files for batch modification exercises
python -m src.o_nakala_core.cli.curator \
  --api-key YOUR_API_KEY \
  --batch-modify workshop_basic_modifications.csv \
  --dry-run
```

## 📚 File Types Included

### Research Data Examples
- **Code**: R scripts, Python modules
- **Data**: CSV datasets, analysis results
- **Documents**: Markdown papers, protocols, literature reviews
- **Images**: Photographs, charts, visualizations
- **Presentations**: Conference talks, stakeholder updates

### Configuration Examples
- **Upload configurations**: Metadata templates for different file types
- **Collection configurations**: Thematic organization patterns
- **Batch modification templates**: Field update examples

## 🎓 Educational Use

### For Workshops
1. **Level 1**: Use `simple-dataset` for basic concepts
2. **Level 2**: Use `sample_dataset` for complete workflows
3. **Level 3**: Use workshop CSV files for advanced metadata management

### For Development
1. **Testing**: Use examples to validate code changes
2. **Debugging**: Sample data for reproducing issues
3. **Documentation**: Examples for user guides and tutorials

## 🔧 Configuration Files

### Essential Files (DO NOT MODIFY)
- `folder_data_items.csv` - Core dataset configuration
- `folder_collections.csv` - Collection organization template
- `files/` directory structure - Sample research data

### Workshop Files (MODIFY FOR EXERCISES)
- `workshop_basic_modifications.csv` - Title/description updates
- `workshop_keywords_exercise.csv` - Keyword management
- `workshop_creator_exercise.csv` - Author assignment
- `workshop_advanced_exercise.csv` - Multi-field updates

## ⚠️ Important Notes

### API Keys
- Never commit real API keys to the repository
- Use test API keys for workshop exercises
- Set `NAKALA_API_KEY` environment variable for security

### File Modifications
- Sample files in `files/` are for reference only
- Workshop CSV files can be modified for exercises
- Always use `--dry-run` before applying batch modifications

### Data Persistence
- Uploads to test API are temporary
- Production uploads require institutional credentials
- Workshop data is cleaned up periodically

## 📖 Related Documentation

- [User Guides](../docs/user-guides/) - Step-by-step instructions
- [API Reference](../api/) - NAKALA API documentation
- [Troubleshooting](../docs/user-guides/troubleshooting.md) - Common issues and solutions

## 🤝 Contributing Examples

To add new examples:
1. Follow the existing directory structure
2. Include README documentation
3. Provide both simple and complex variations
4. Test with real API before submitting
5. Update this README with new examples

---

**Ready for workshops, development, and production workflows.**