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

## 🎯 Workflow Processing

### Data Upload Results
When processed through O-Nakala Core, this dataset creates:

- **5 Datasets**: One for each file category (code, data, documents, images, presentations)
- **3 Collections**: Thematically organized groupings
  - "Code and Data Collection" - Technical files
  - "Documents Collection" - Research documentation
  - "Multimedia Collection" - Images and presentations

### Success Metrics
- **14 files** successfully uploaded
- **100% success rate** in processing
- **Multilingual metadata** support (French/English)
- **COAR resource types** properly assigned

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

### 1. Basic Upload Workflow
```bash
# Set up environment
export NAKALA_API_KEY="your_test_api_key"
export PYTHONPATH=/path/to/o-nakala-core

# Upload dataset
o-nakala-upload \
  --api-key "$NAKALA_API_KEY" \
  --dataset folder_data_items.csv \
  --mode folder \
  --output upload_results.csv

# Create collections
o-nakala-collection \
  --api-key "$NAKALA_API_KEY" \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv
```

### 2. Quality Analysis
```bash
# Run quality report
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --verbose
```

### 3. Batch Modifications
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

## 📊 Expected Results

### Upload Output
- Creates persistent identifiers (DOIs) for each dataset
- Generates upload results CSV with collection mappings
- Processes all 14 files successfully

### Collection Organization
- Groups related datasets thematically
- Maintains multilingual metadata
- Supports complex relationship mapping

### Quality Metrics
- 100% metadata completeness for core fields
- Proper COAR resource type assignments
- Multilingual support validation

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
- [O-Nakala API Documentation](../../api/guide_description.md) - API reference
- [Troubleshooting Guide](../../docs/user-guides/troubleshooting.md) - Common issues

---

**Total Files**: 14  
**Categories**: 5  
**Collections**: 3  
**Workshop Exercises**: 6  
**Success Rate**: 100%