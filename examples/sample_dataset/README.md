# Sample Dataset - Clean Research Data Repository (v2.5.1)

## 📋 Overview

**Clean sample research dataset** containing 14 files across 5 academic categories for testing O-Nakala Core workflows. This directory provides **pure data and configurations only** - all operational scripts have been moved to `../notebooks/` and temporary files removed.

**Preview your data** before upload using the enhanced preview tool:
```bash
o-nakala-preview --csv folder_data_items.csv --enhance --interactive
```

## 📂 Directory Structure (v2.5.1 Clean)

```
sample_dataset/
├── README.md                    # This file - data description
├── folder_collections.csv      # Collection configuration (ESSENTIAL)
├── folder_data_items.csv       # Dataset upload configuration (ESSENTIAL)
└── files/                      # Research data files (ESSENTIAL)
    ├── code/                   # Analysis scripts (R, Python)
    ├── data/                   # Research datasets (CSV)
    ├── documents/              # Academic documentation (Markdown)
    ├── images/                 # Research photographs (JPG)
    └── presentations/          # Meeting materials (Markdown)
```

### 📝 **Generated Files** (Not Included)
These files are created during workflow execution:
- `upload_results.csv`, `collections_output.csv` - Workflow output files
- `quality_report.json`, `creator_fixes_*.csv` - Analysis results

## 🗂️ Data Contents

### Research Files (14 total)

#### **Code** (2 files)
- `analysis_data_cleaning.R` - R script for data preprocessing
- `preprocess_data.py` - Python data cleaning utilities

#### **Data** (2 files)  
- `analysis_results_2023.csv` - Processed research results
- `raw_survey_data_2023.csv` - Original survey responses

#### **Documents** (4 files)
- `paper_analysis_methods.md` - Methodology documentation
- `paper_literature_review.md` - Literature review section
- `paper_results_discussion.md` - Results and discussion
- `study_protocol_v1.0.md` - Research protocol

#### **Images** (1 file)
- `site_photograph_1.jpg` - Research site documentation

#### **Presentations** (3 files)
- `conference_presentation_2023.md` - Academic conference slides
- `stakeholder_update_2023-06.md` - Project update for stakeholders  
- `team_meeting_2023-04.md` - Internal team meeting notes

### Configuration Files (2 files)

#### **folder_data_items.csv**
Defines how individual files are uploaded as datasets with metadata:
- File paths and titles
- Descriptions and keywords
- COAR resource types
- Multilingual metadata (French/English)

#### **folder_collections.csv**
Defines how datasets are organized into thematic collections:
- Collection titles and descriptions
- Grouping logic for related datasets
- Professional metadata structure

## 🎯 Usage with O-Nakala Workflows

### Data-Only Purpose
This directory contains **only data and configuration**:
- ✅ Sample research files to upload
- ✅ CSV configurations for workflows
- ✅ Documentation of data structure
- ❌ No operational scripts (moved to `../notebooks/`)
- ❌ No generated results files (created during workflow execution)

### Integration with Workflows
To use this data with O-Nakala workflows:

1. **Navigate to operations center**: `cd ../notebooks/`
2. **Run complete workflow**: `./run_workflow.sh your-api-key`
3. **Results are generated**: Output files created in appropriate locations

### Expected Processing Results
When processed through O-Nakala workflows, this dataset creates:
- **5 Datasets**: One per file category (code, data, documents, images, presentations)
- **3 Collections**: Thematically organized groupings
- **Complete metadata**: Professional multilingual descriptions and keywords

## 📊 Quality Metrics

- **Total Files**: 14
- **File Categories**: 5  
- **Collection Groups**: 3
- **Metadata Languages**: 2 (French/English)
- **COAR Resource Types**: 4 different types
- **Success Rate**: 100% (when processed with valid API key)

## 🔗 Related Resources

- **Operations Center**: `../notebooks/` - All workflow scripts and automation
- **Documentation**: `../workflow_documentation/` - Detailed guides and troubleshooting
- **Requirements**: `../requirements.txt` - Python dependencies for workflows

---

**Purpose**: Research data repository for O-Nakala workflow testing  
**Type**: Sample academic research files with metadata configurations  
**Maintenance**: Data-only directory - operations handled in `../notebooks/`