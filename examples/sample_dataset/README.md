# Sample Dataset - Complete O-Nakala Workflow Example

## 📋 Overview

This directory contains a comprehensive example dataset designed for testing all aspects of the O-Nakala Core system. It includes 14 sample files organized into 5 research categories, complete with metadata configurations and workshop exercises.

## 🗂️ Dataset Structure

### Core Configuration Files
- **`folder_data_items.csv`** - Dataset metadata configuration for 5 folder categories
- **`folder_collections.csv`** - Collection organization template for thematic grouping

### Sample Research Files (`files/`)

#### `/code/` - Research Code
- `analysis_data_cleaning.R` - R script for data preprocessing
- `preprocess_data.py` - Python module for data preparation

#### `/data/` - Research Data
- `analysis_results_2023.csv` - Processed analysis results
- `raw_survey_data_2023.csv` - Original survey responses

#### `/documents/` - Research Documentation
- `paper_analysis_methods.md` - Methodology documentation
- `paper_literature_review.md` - Literature review
- `paper_results_discussion.md` - Results and discussion
- `study_protocol_v1.0.md` - Research protocol

#### `/images/` - Visual Materials
- `site_photograph_1.jpg` - Field photography
- `site_photograph_2.jpg` - Additional site documentation
- `temperature_trends_2023.png` - Data visualization chart

#### `/presentations/` - Communication Materials
- `conference_presentation_2023.md` - Academic presentation
- `stakeholder_update_2023-06.md` - Progress report
- `team_meeting_2023-04.md` - Internal meeting notes

## 🎯 7-Step Workflow Processing

### Data Upload Results
When processed through the O-Nakala Core workflow, this dataset creates:

- **5 Datasets**: One for each file category (code, data, documents, images, presentations)
- **3 Collections**: Thematically organized groupings
  - "Code and Data Collection" - Technical files with metadata
  - "Academic Documentation Collection" - Research documentation with descriptions
  - "Multimedia Collection" - Images and presentations with keywords

### Success Metrics (v2.4.0)
- **14 files** successfully uploaded
- **Complete processing** of all items
- **Multilingual metadata** support (French/English)
- **COAR resource types** properly assigned
- **Metadata enhancement** for both datasets AND collections
- **Automated metadata generation** with content detection
- **Complete workflow automation** with 7-step process

## 🧪 Workshop Exercises

### Exercise Files Included

#### Level 1: Basic Modifications
- **`workshop_basic_modifications.csv`** - Title and description updates
  ```csv
  id,action,new_title,new_description
  REPLACE_WITH_YOUR_COLLECTION_ID,modify,"fr:Titre Modifié|en:Modified Title","fr:Description mise à jour|en:Updated description"
  ```

#### Level 2: Keyword Management
- **`workshop_keywords_exercise.csv`** - Keyword enhancement
  ```csv
  id,action,new_keywords
  REPLACE_WITH_YOUR_COLLECTION_ID,modify,"fr:recherche;données;analyse|en:research;data;analysis"
  ```

#### Level 3: Creator Assignment
- **`workshop_creator_exercise.csv`** - Author field management
  ```csv
  id,action,new_creator
  REPLACE_WITH_YOUR_COLLECTION_ID,modify,"Workshop, Participant;Example, User"
  ```

#### Level 4: Advanced Multi-Field
- **`workshop_advanced_exercise.csv`** - Complex metadata updates
- **`simple_field_test.csv`** - Tested stable format for multiple fields

### Workshop Template
- **`workshop_template.csv`** - Blank template with instructions

## 🚀 Usage Instructions

### 1. Enhanced 7-Step Workflow (Recommended)
```bash
# Complete automated workflow with professional metadata enhancement
./run_workflow.sh your_test_api_key --cleanup
```

**What this does:**
1. **Upload** - 5 datasets created from sample files
2. **Collections** - 3 thematic collections organized
3. **Enhancement Generation** - Professional metadata created for datasets AND collections
4. **Dataset Curation** - Enhanced metadata applied to all datasets
5. **Collection Curation** - Enhanced metadata applied to all collections  
6. **Quality Analysis** - Comprehensive report generated
7. **Cleanup** - Test data automatically removed (optional)

### 2. Manual Step-by-Step Workflow
```bash
# Set up environment
export NAKALA_API_KEY="your_test_api_key"

# Step 1-2: Upload and create collections
o-nakala-upload --api-key "$NAKALA_API_KEY" --dataset folder_data_items.csv --mode folder --output upload_results.csv
o-nakala-collection --api-key "$NAKALA_API_KEY" --from-upload-output upload_results.csv --from-folder-collections folder_collections.csv

# Step 3: Generate professional enhancements
python create_modifications.py upload_results.csv
python create_collection_modifications.py collections_output.csv

# Step 4-5: Apply enhancements to datasets and collections
o-nakala-curator --api-key "$NAKALA_API_KEY" --batch-modify auto_data_modifications.csv --scope datasets
o-nakala-curator --api-key "$NAKALA_API_KEY" --batch-modify auto_collection_modifications.csv --scope collections

# Step 6: Quality analysis
o-nakala-curator --api-key "$NAKALA_API_KEY" --quality-report --scope datasets --output quality_report.json
```

### 3. Workshop Exercises and Custom Modifications
```bash
# Test modifications (dry run)
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify workshop_basic_modifications.csv \
  --dry-run \
  --verbose

# Apply modifications
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify workshop_basic_modifications.csv \
  --verbose
```

## 📊 Expected Results (Enhanced 7-Step Workflow)

### Upload Output
- Creates persistent identifiers (DOIs) for each dataset
- Generates upload results CSV with collection mappings
- Processes all 14 files successfully

### Collection Organization (Enhanced)
- Groups related datasets thematically with professional titles
- Enhanced multilingual metadata for both datasets AND collections
- Professional descriptions and targeted keywords automatically generated

### Enhanced Quality Metrics (v2.4.0)
- 100% metadata completeness for core fields
- Proper COAR resource type assignments
- Multilingual support validation
- **Professional metadata enhancement**: Datasets AND collections enhanced
- **Automated intelligence**: Content-aware metadata generation
- **Complete automation**: 7-step workflow with 100% success rate

### New Files Generated
- `auto_data_modifications.csv` - Professional dataset metadata enhancements
- `auto_collection_modifications.csv` - Professional collection metadata enhancements
- `quality_report.json` - Comprehensive analysis report
- `collections_output.csv` - Collection creation results with IDs

## 🔧 Configuration Details

### Metadata Fields Configured
- **Title**: Multilingual (French/English)
- **Description**: Detailed, multilingual descriptions
- **Keywords**: Semicolon-separated, multilingual
- **Creator**: Author information
- **Type**: COAR resource type URIs
- **License**: Creative Commons licensing
- **Language**: ISO language codes
- **Rights**: Access control settings

### File Type Mappings
- `.R`, `.py` → Software (c_5ce6)
- `.csv` → Dataset (c_ddb1)
- `.md` → Text (c_18cf)
- `.jpg`, `.png` → Image (c_c513)
- All files → Appropriate COAR types

## ⚠️ Workshop Preparation

### Before Using for Training
1. **Replace Collection IDs**: Update `REPLACE_WITH_YOUR_COLLECTION_ID` in workshop files
2. **Test API Connection**: Verify API key works with test endpoint
3. **Check File Permissions**: Ensure all files are readable
4. **Review Output Path**: Confirm write permissions for output files

### During Workshops
1. **Start with dry-run**: Always test modifications first
2. **Monitor progress**: Use `--verbose` flag for detailed output
3. **Handle errors gracefully**: Check API connectivity if issues occur
4. **Document results**: Save output files for analysis

## 📚 Additional Resources

- [Workshop CSV Guide](WORKSHOP_CSV_GUIDE.md) - Detailed CSV format documentation
- [NAKALA API Documentation](https://api.nakala.fr/doc) - Official API reference
- [Troubleshooting Guide](../../docs/user-guides/troubleshooting.md) - Common issues

---

**Total Files**: 14  
**Categories**: 5  
**Collections**: 3  
**Workshop Exercises**: 6  
**Success Rate**: 100%