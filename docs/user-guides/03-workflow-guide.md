# User Workflow Guide

## Research Data Management - 6 Essential Steps

> **Purpose**: Complete workflow for uploading, organizing, and managing your research data in NAKALA  
> **Audience**: Researchers, data managers, digital humanities practitioners  
> **Time**: 45-90 minutes depending on dataset size  
> **Prerequisites**: NAKALA API key, organized files and metadata

## Workflow Navigation

📋 **You are here**: User Workflow Guide (practical steps)  
🔬 **Want to explore features?** → [Feature Demonstration Notebook](../../examples/notebooks/workflow_notebook.ipynb)  
⚡ **Just getting started?** → [Upload Guide](01-upload-guide.md) for single operations  
🎯 **Need help with specific tools?** → [Curation Guide](04-curation-guide.md)

---

## Step 1: Organize Your Data and Metadata

**What you'll do**: Set up your files and prepare metadata information for upload  
**Why**: Proper organization ensures smooth upload and makes your data discoverable  
**Time**: 15-30 minutes  
**You'll have**: Organized files and complete metadata ready for NAKALA

### Quick Instructions
1. Create a clear folder structure (e.g., `files/code`, `files/data`, `files/documents`)
2. Prepare two CSV files:
   - `folder_data_items.csv` - describes your individual files/datasets  
   - `folder_collections.csv` - describes how to group your data
3. Verify file paths in your CSV match your actual folder structure

<details>
<summary>📋 Detailed Organization Guide</summary>

### Folder Structure Example
```
my_research_project/
├── files/
│   ├── data/           # Raw data files
│   ├── code/           # Scripts and analysis code  
│   ├── documents/      # Papers, reports
│   └── images/         # Figures, photos
├── folder_data_items.csv
└── folder_collections.csv
```

### CSV Preparation Tips
- **Required fields**: title, description, creator, license, type
- **Multilingual format**: `en:English title|fr:Titre français`
- **File paths**: Must match your actual folder structure exactly
- **Validation**: Check that all files referenced in CSV actually exist

</details>

<details>
<summary>🔧 Troubleshooting Common Issues</summary>

- **File not found errors**: Check file paths in CSV match folder structure
- **Special characters**: Avoid spaces and special characters in file names
- **Large files**: Consider splitting very large datasets into smaller parts
- **Metadata quality**: Use descriptive titles and keywords for better discoverability

</details>

## Step 2: Upload Your Data to NAKALA

**What you'll do**: Upload your organized files and metadata to the NAKALA repository  
**Why**: Makes your research data accessible, citable, and preservable  
**Time**: 5-15 minutes depending on file size  
**You'll have**: All your data uploaded with unique identifiers and metadata

### Quick Upload
```bash
o-nakala-upload \
    --api-key "your-key" \
    --dataset "folder_data_items.csv" \
    --base-path "your_project_folder" \
    --mode folder \
    --output "upload_results.csv"
```

**Replace `your-key`** with your actual NAKALA API key  
**Replace `your_project_folder`** with your folder name

<details>
<summary>📤 Complete Upload Options</summary>

### Full Command with All Parameters
```bash
o-nakala-upload \
    --api-key "$NAKALA_API_KEY" \
    --dataset "folder_data_items.csv" \
    --base-path "sample_dataset" \
    --mode folder \
    --folder-config "folder_data_items.csv" \
    --output "upload_results.csv" \
    --validate-only  # Test without uploading
```

### Parameter Explanation
- `--dataset`: Your metadata CSV file
- `--base-path`: Directory containing your files
- `--mode folder`: Upload organized by folder structure
- `--output`: File to save upload results (default: upload_results.csv)
- `--validate-only`: Check everything without actually uploading

</details>

<details>
<summary>⚡ Upload Tips & Troubleshooting</summary>

### Before Upload
- **Test first**: Use `--validate-only` to check for errors
- **Check API key**: Verify your NAKALA API key is correct
- **File size**: Large files may take longer - be patient

### Common Issues
- **Authentication failed**: Check your API key
- **File not found**: Verify paths in CSV match actual files
- **Network timeout**: Try smaller batches for large datasets
- **Metadata errors**: Check required fields are complete

### After Upload
- Check `upload_results.csv` for successful uploads
- Note the identifier for each uploaded item
- Failed uploads will show error messages

</details>

## Step 3: Organize Data into Collections

**What you'll do**: Group your uploaded items into thematic collections  
**Why**: Collections make your research easier to discover and navigate  
**Time**: 5-10 minutes  
**You'll have**: Organized collections with your uploaded datasets properly grouped

### Quick Collection Setup
```bash
o-nakala-collection \
    --api-key "your-key" \
    --from-upload-output "upload_results.csv" \
    --from-folder-collections "folder_collections.csv"
```

<details>
<summary>📁 Collection Organization Details</summary>

### Full Command
```bash
o-nakala-collection \
    --api-key "your-key" \
    --from-folder-collections "folder_collections.csv" \
    --from-upload-output "upload_results.csv" \
    --collection-report "collections_output.csv"
```

### What Collections Do
- **Group related items**: Put similar data together
- **Add context**: Provide descriptions for groups of data
- **Improve discovery**: Make it easier for others to find related materials
- **Create hierarchy**: Organize complex research projects

### Collection Examples
- "2024 Field Study Data" - all data from a specific research period
- "Interview Transcripts" - all interview-related materials  
- "Statistical Analysis" - code, data, and results from analysis

</details>

## Step 4: Improve Your Metadata

**What you'll do**: Generate templates to enhance titles, descriptions, and keywords  
**Why**: Better metadata makes your research more discoverable and professional  
**Time**: 10-20 minutes (5 min to generate, 10-15 min to edit)  
**You'll have**: Professional, enhanced metadata for all your items

### Quick Template Generation
```bash
# Create template for your uploaded items
o-nakala-curator \
    --api-key "your-key" \
    --export-template "my_improvements.csv" \
    --scope datasets
```

Then edit `my_improvements.csv` to add better titles, descriptions, and keywords.

<details>
<summary>✨ Metadata Enhancement Guide</summary>

### Generate Templates for Everything
```bash
# For your uploaded datasets
o-nakala-curator \
    --api-key "your-key" \
    --export-template "data_modifications.csv" \
    --scope datasets

# For your collections  
o-nakala-curator \
    --api-key "your-key" \
    --export-template "collection_modifications.csv" \
    --scope collections
```

### What to Improve in Your CSV
- **Titles**: Make them descriptive and searchable
- **Descriptions**: Add context, methodology, significance
- **Keywords**: Include research terms, topics, methods
- **Language tags**: Use proper language codes (en, fr, etc.)

### Enhancement Examples
```csv
# Before
title: "data.csv"
description: "some data"

# After  
new_title: "en:Climate Survey Data 2024|fr:Données d'enquête climatique 2024"
new_description: "en:Temperature and precipitation measurements from 15 weather stations across France, collected monthly from January to December 2024 for climate change research."
```

</details>

## Step 5: Apply Your Improvements

**What you'll do**: Update your items with the enhanced metadata you created  
**Why**: Apply all your improvements to make data more professional and discoverable  
**Time**: 5-10 minutes  
**You'll have**: All your items updated with enhanced metadata

### Safe Application (Always Test First!)
```bash
# 1. Test your changes first (no actual changes made)
o-nakala-curator \
    --api-key "your-key" \
    --batch-modify "my_improvements.csv" \
    --dry-run

# 2. If test looks good, apply the changes
o-nakala-curator \
    --api-key "your-key" \
    --batch-modify "my_improvements.csv"
```

<details>
<summary>🔧 Advanced Application Options</summary>

### Apply Different Types of Modifications
```bash
# Apply dataset improvements
o-nakala-curator \
    --api-key "your-key" \
    --batch-modify "data_modifications.csv"

# Apply collection improvements  
o-nakala-curator \
    --api-key "your-key" \
    --batch-modify "collection_modifications.csv"

# Process in smaller batches for large datasets
o-nakala-curator \
    --api-key "your-key" \
    --batch-modify "modifications.csv" \
    --batch-size 10
```

### Safety Features
- **Dry run**: Always test with `--dry-run` first
- **Validation**: System checks your changes before applying
- **Rollback**: Keep backup of original metadata if needed
- **Batch processing**: Large updates are processed safely in chunks

</details>

## Step 6: Verify Everything is Ready

**What you'll do**: Generate a quality report to check your data is ready for publication  
**Why**: Ensure everything is complete, consistent, and meets NAKALA standards  
**Time**: 2-5 minutes  
**You'll have**: A quality report showing what's ready and what needs attention

### Quick Quality Check
```bash
o-nakala-curator \
    --api-key "your-key" \
    --quality-report \
    --scope all \
    --output "my_quality_report.json"
```

Then review `my_quality_report.json` to see your data quality status.

<details>
<summary>📊 Understanding Your Quality Report</summary>

### What the Report Shows
- **Completeness**: Are all required fields filled?
- **Consistency**: Do similar items have similar metadata?  
- **Standards**: Does everything meet NAKALA requirements?
- **Recommendations**: What could be improved?

### Quality Report Structure
```json
{
  "summary": {
    "total_items": 25,
    "validation_errors": 2,
    "missing_required_fields": 1,
    "overall_score": 85.2
  },
  "recommendations": [
    "Add description to 1 item",
    "Check language codes in 2 items"
  ]
}
```

### Next Steps Based on Report
- **Score 90+**: Excellent! Ready for publication
- **Score 75-89**: Good quality, minor improvements recommended  
- **Score 60-74**: Some issues to address before publication
- **Score <60**: Significant improvements needed

</details>

---

## 🎉 Workflow Complete - What You've Accomplished

**Congratulations!** You've successfully managed your research data in NAKALA. Here's what you now have:

### ✅ Your Results
- **Uploaded data**: All files stored securely with unique identifiers
- **Organized collections**: Data grouped logically for easy discovery  
- **Enhanced metadata**: Professional titles, descriptions, and keywords
- **Quality verified**: Reports confirm your data meets standards
- **Publication ready**: Data can be made public when you're ready

### 📄 Files Generated During Workflow
- `upload_results.csv` - Details of all uploaded items
- `collections_output.csv` - Information about created collections  
- `my_quality_report.json` - Quality analysis and recommendations
- `my_improvements.csv` - Your metadata enhancements

### 🚀 Next Steps (Optional)
- **Make data public**: Change status from private to public in NAKALA interface
- **Get DOIs**: Assign permanent identifiers for citation
- **Share collections**: Send collection links to collaborators
- **Monitor usage**: Check access statistics in NAKALA

## Quick Reference - 6 Essential Steps

| Step | What You Do | Time | Result |
|------|-------------|------|--------|
| 1. **Organize** | Set up files and metadata | 15-30 min | Ready for upload |
| 2. **Upload** | Send data to NAKALA | 5-15 min | Data stored with IDs |
| 3. **Collect** | Group items into collections | 5-10 min | Organized data |
| 4. **Enhance** | Improve metadata quality | 10-20 min | Professional metadata |
| 5. **Apply** | Update all improvements | 5-10 min | Enhanced data |
| 6. **Verify** | Check quality and completeness | 2-5 min | Publication ready |

**Total Time**: 45-90 minutes for complete research data management

---

## Related Guides

📋 **You completed**: User Workflow Guide  
🔬 **Explore more features**: [Feature Demonstration Notebook](../../examples/notebooks/workflow_notebook.ipynb)  
🎯 **Specific help**: [Upload Guide](01-upload-guide.md) • [Collection Guide](02-collection-guide.md) • [Curation Guide](04-curation-guide.md)  
❓ **Questions?**: [Troubleshooting](05-troubleshooting.md)

## Common Workflows

### 1. Folder-Based Collection Creation
```bash
# Create collections based on folder structure
o-nakala-collection \
    --api-key "your-key" \
    --from-folder-collections "folder_collections.csv" \
    --from-upload-output "output.csv" \
    --collection-report "collections_output.csv"
```

The script will provide detailed collection mapping diagnostics showing:
- Which folders were matched
- Which data items were included
- Any unmatched folders
- Collection creation status

### 2. Single Collection Creation
```bash
# Create a single collection
o-nakala-collection \
    --api-key "your-key" \
    --title "fr:Collection Title|en:Collection Title" \
    --description "fr:Description|en:Description" \
    --keywords "fr:keywords|en:keywords" \
    --from-upload-output output.csv
```

### 3. Multilingual Dataset Upload and Collection
```bash
# Upload dataset with multilingual metadata
o-nakala-upload \
    --mode folder \
    --dataset "multilingual_dataset/" \
    --folder-config "folder_data_items.csv" \
    --api-key "your-key"

# Create collections with multilingual metadata
o-nakala-collection \
    --api-key "your-key" \
    --from-folder-collections "folder_collections.csv" \
    --from-upload-output "output.csv"
```

## Best Practices

### Data Organization
1. Use consistent folder structure:
   ```
   project/
   ├── files/
   │   ├── code/
   │   ├── data/
   │   ├── documents/
   │   ├── images/
   │   └── presentations/
   ├── folder_data_items.csv
   └── folder_collections.csv
   ```
2. Include comprehensive metadata in both French and English
3. Validate files before upload
4. Use appropriate file formats

### Metadata Management
1. Include multilingual descriptions (fr|en format)
2. Add relevant keywords in both languages
3. Specify proper licenses (CC-BY-4.0, CC-BY-NC-4.0, etc.)
4. Document authorship and contributions
5. Include coverage and relations

### Collection Organization
1. Create logical hierarchies based on content type
2. Use descriptive bilingual titles
3. Include relevant multilingual keywords
4. Set appropriate access rights
5. Maintain consistent metadata across collections

### Collection Relationships
1. Define clear relationships between collections
2. Use appropriate relation types
3. Document project associations
4. Maintain consistent coverage information
5. Link related collections through metadata

## 📚 Official NAKALA Resources

### **Complete Workflow Documentation**
- **[Official NAKALA Documentation](https://documentation.huma-num.fr/nakala/)** - Comprehensive platform guide
- **[Getting Started with NAKALA](https://documentation.huma-num.fr/nakala/getting-started/)** - Official workflow introduction
- **[Data Preparation Guide](https://documentation.huma-num.fr/nakala-preparer-ses-donnees/)** - Prepare your research data properly

### **Detailed Processes**
- **[Data Deposit Form](https://documentation.huma-num.fr/nakala/data-deposit-form/)** - Official deposit process
- **[Collection Creation Form](https://documentation.huma-num.fr/nakala/collection-creation-form/)** - Official collection workflow
- **[Metadata Description Guide](https://documentation.huma-num.fr/nakala-guide-de-description/)** - Complete metadata specifications

### **API & Advanced Usage**
- **[Test API Documentation](https://apitest.nakala.fr/doc)** - Interactive API testing
- **[Production API Documentation](https://api.nakala.fr/doc)** - Live API reference
- **[NAKALA Test Platform](https://test.nakala.fr)** - Safe environment for testing workflows
- **[NAKALA Production](https://nakala.fr)** - Live research data repository 