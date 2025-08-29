# 📁 Complete Researcher Workflow Guide
## From Folder-Based Files to NAKALA Repository

*A comprehensive step-by-step guide for researchers to upload, create, organize, and curate their folder-based research data in NAKALA.*

---

## 🎯 **Overview: The Complete Research Data Cycle**

This guide walks you through the complete 8-step workflow to transform your local folder structure into a well-organized, curated NAKALA repository. Perfect for researchers with mixed content (code, data, documents, images, presentations).

### **What You'll Achieve:**
- ✅ **Upload**: All files uploaded as individual datasets
- ✅ **Create**: Proper metadata for each file type
- ✅ **Organize**: Logical collections grouping related materials
- ✅ **Curate**: Quality validation, metadata enhancement, and publication-ready content

---

## 📂 **Prerequisites: Prepare Your Folder Structure**

### **1. Organize Your Research Files**
```
your_research_project/
├── code/
│   ├── analysis_script.py
│   ├── data_processing.R
│   └── visualization.ipynb
├── data/
│   ├── survey_results.csv
│   ├── experiment_data.xlsx
│   └── cleaned_dataset.json
├── documents/
│   ├── methodology.pdf
│   ├── literature_review.md
│   └── research_protocol.docx
├── images/
│   ├── diagram_1.png
│   ├── site_photo.jpg
│   └── chart_results.svg
└── presentations/
    ├── conference_talk.pptx
    ├── poster_session.pdf
    └── team_update.md
```

### **2. Install O-Nakala-Core**
```bash
pip install o-nakala-core==2.4.3
```

### **3. Set Up Environment**
```bash
# For testing (public test environment)
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_BASE_URL="https://apitest.nakala.fr"

# For production (use your personal API key)
export NAKALA_API_KEY="your-personal-api-key"
export NAKALA_BASE_URL="https://api.nakala.fr"
```

---

## 🚀 **Step-by-Step Workflow**

### **Phase 1: Preparation & Planning** 

#### **Step 1: Create Metadata CSV Files**

Create two CSV files to describe your content:

**A. `folder_data_items.csv` - Describe individual files**

```csv
file,status,type,title,alternative,creator,contributor,date,license,description,keywords,language,temporal,spatial,accessRights,identifier,rights
code/analysis_script.py,pending,http://purl.org/coar/resource_type/c_5ce6,"fr:Script d'analyse Python|en:Python Analysis Script","fr:Code d'analyse|en:Analysis Code","Dupont,Jean","","2024-03-15",CC-BY-4.0,"fr:Script pour l'analyse statistique des données|en:Script for statistical data analysis","fr:python;analyse;statistiques|en:python;analysis;statistics",fr,2024,"fr:Laboratoire Paris|en:Paris Lab",Open Access,,
data/survey_results.csv,pending,http://purl.org/coar/resource_type/c_ddb1,"fr:Résultats d'enquête sociologique|en:Sociological Survey Results","fr:Données d'enquête|en:Survey Data","Dupont,Jean;Martin,Sophie","","2024-02-28",CC-BY-NC-4.0,"fr:Données brutes de l'enquête menée en 2024|en:Raw data from 2024 survey","fr:enquête;sociologie;données|en:survey;sociology;data",fr,2024,"fr:France métropolitaine|en:Metropolitan France",Open Access,,
documents/methodology.pdf,pending,http://purl.org/coar/resource_type/c_18cf,"fr:Méthodologie de recherche|en:Research Methodology","fr:Document méthodologique|en:Methodology Document","Dupont,Jean","","2024-01-15",CC-BY-4.0,"fr:Document détaillant la méthodologie de recherche utilisée|en:Document detailing research methodology used","fr:méthodologie;recherche;protocole|en:methodology;research;protocol",fr,2024,"fr:Université de Strasbourg|en:University of Strasbourg",Open Access,,
```

**B. `folder_collections.csv` - Organize files into collections**

```csv
title,status,description,keywords,language,creator,data_items
"fr:Collection Code et Analyses|en:Code and Analysis Collection",private,"fr:Collection regroupant tous les scripts et codes d'analyse|en:Collection grouping all analysis scripts and code","fr:code;analyse;programmation|en:code;analysis;programming",fr,"Dupont,Jean;Martin,Sophie","code/analysis_script.py"
"fr:Collection Données de Recherche|en:Research Data Collection",private,"fr:Collection de toutes les données collectées et traitées|en:Collection of all collected and processed data","fr:données;recherche;enquête|en:data;research;survey",fr,"Dupont,Jean;Martin,Sophie","data/survey_results.csv"
"fr:Collection Documentation|en:Documentation Collection",private,"fr:Documentation complète du projet de recherche|en:Complete research project documentation","fr:documentation;méthodologie;recherche|en:documentation;methodology;research",fr,"Dupont,Jean;Martin,Sophie","documents/methodology.pdf"
```

#### **Step 2: Preview and Validate Your Metadata**

Use the preview tool to validate your CSV files:

```bash
# Preview and validate your data items
o-nakala-preview --csv folder_data_items.csv --interactive

# Preview your collections
o-nakala-preview --csv folder_collections.csv --validate-only
```

**What to look for:**
- ✅ All required fields present (title, type)
- ✅ Multilingual format correct (`fr:French|en:English`)
- ✅ COAR resource types valid
- ✅ Creator format correct (`Surname,Firstname`)

#### **Step 3: Get COAR Resource Type Suggestions**

If unsure about resource types, use the interactive assistant:

```bash
o-nakala-preview --csv folder_data_items.csv --interactive
# Choose option 1: Get COAR resource type suggestions
# Enter content hints like: "python analysis script"
```

**Common COAR Types:**
- **Dataset**: `http://purl.org/coar/resource_type/c_ddb1`
- **Software**: `http://purl.org/coar/resource_type/c_5ce6` 
- **Text**: `http://purl.org/coar/resource_type/c_18cf`
- **Image**: `http://purl.org/coar/resource_type/c_c513`
- **Presentation**: `http://purl.org/coar/resource_type/c_8544`

### **Phase 2: Upload & Create**

#### **Step 4: Upload Files and Create Datasets**

Upload all your files with metadata:

```bash
o-nakala-upload \
  --api-key "$NAKALA_API_KEY" \
  --dataset folder_data_items.csv \
  --base-path . \
  --mode folder \
  --output upload_results.csv
```

**Expected Output:**
```
📤 Upload Progress:
✅ code/analysis_script.py → Dataset ID: 10.34847/nkl.xxxxx
✅ data/survey_results.csv → Dataset ID: 10.34847/nkl.yyyyy  
✅ documents/methodology.pdf → Dataset ID: 10.34847/nkl.zzzzz

📊 Summary: 3 files uploaded, 3 datasets created
```

### **Phase 3: Organize**

#### **Step 5: Create Collections**

Organize your datasets into logical collections:

```bash
o-nakala-collection \
  --api-key "$NAKALA_API_KEY" \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv \
  --collection-report collections_output.csv
```

**Expected Output:**
```
📁 Collection Creation:
✅ Code and Analysis Collection → Collection ID: 10.34847/nkl.coll1
✅ Research Data Collection → Collection ID: 10.34847/nkl.coll2
✅ Documentation Collection → Collection ID: 10.34847/nkl.coll3

📊 Summary: 3 collections created, 3 datasets organized
```

### **Phase 4: Curate**

#### **Step 6: Quality Analysis and Validation**

Run comprehensive quality analysis:

```bash
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --scope all \
  --output quality_report.json
```

**Quality Report Analysis:**
- 📊 **Metadata Completeness**: Percentage of required fields filled
- 🔗 **Relationship Validation**: Collection-dataset associations
- 📝 **Content Analysis**: Multilingual metadata quality
- ⚠️ **Issues Identified**: Missing creators, invalid dates, etc.

#### **Step 7: Fix Validation Issues**

Address any quality issues found:

```bash
# Create fixes file based on quality report
echo "id,action,property,value,lang" > validation_fixes.csv
echo "10.34847/nkl.xxxxx,add_metadata,creator,Dupont Jean,en" >> validation_fixes.csv

# Apply fixes
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify validation_fixes.csv \
  --scope datasets
```

#### **Step 8: Enhance Metadata (Optional)**

Add enhanced metadata based on content analysis:

```bash
# Generate metadata enhancements
echo "id,action,property,value,lang" > metadata_enhancements.csv
echo "10.34847/nkl.xxxxx,add_metadata,subject,Data Science,en" >> metadata_enhancements.csv
echo "10.34847/nkl.xxxxx,add_metadata,subject,Science des Données,fr" >> metadata_enhancements.csv

# Apply enhancements
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify metadata_enhancements.csv \
  --scope datasets
```

---

## 🎯 **Complete Automated Workflow**

For experienced researchers, use the complete automated workflow:

```bash
# Clone the example workflow
git clone https://github.com/your-org/o-nakala-core
cd o-nakala-core/examples/notebooks

# Run complete 8-step workflow
./run_workflow.sh YOUR_API_KEY

# With cleanup (removes test data after completion)
./run_workflow.sh YOUR_API_KEY --cleanup
```

**The automated workflow performs:**
1. **Data Upload** - All files → NAKALA datasets
2. **Collection Creation** - Organize datasets into collections
3. **Metadata Enhancement** - Automated improvements
4. **Quality Analysis** - Comprehensive validation
5. **Validation Fixes** - Automatic issue resolution
6. **Dataset Curation** - Metadata refinement
7. **Collection Curation** - Collection-level improvements
8. **Publication Management** - Rights and publication status

---

## 📊 **Monitoring Your Progress**

### **Check User Information and Statistics**
```bash
o-nakala-user-info \
  --api-key "$NAKALA_API_KEY" \
  --collections-only
```

### **View Quality Metrics**
```bash
# Generate detailed quality report
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --scope all \
  --detailed-analysis \
  --output comprehensive_quality.json
```

### **Export Final Results**
```bash
# List all your datasets
o-nakala-user-info \
  --api-key "$NAKALA_API_KEY" \
  --datasets-only \
  --export-csv my_datasets.csv

# List all your collections  
o-nakala-user-info \
  --api-key "$NAKALA_API_KEY" \
  --collections-only \
  --export-csv my_collections.csv
```

---

## ✅ **Success Checklist**

After completing the workflow, verify:

### **Upload Success:**
- [ ] All files uploaded without errors
- [ ] Each file has a unique dataset ID
- [ ] File checksums validated
- [ ] Metadata correctly associated

### **Organization Success:**
- [ ] Collections created as planned  
- [ ] Datasets properly grouped in collections
- [ ] Collection metadata complete
- [ ] Hierarchical structure preserved

### **Quality Success:**
- [ ] All required metadata fields present
- [ ] Multilingual content properly formatted
- [ ] COAR resource types correctly assigned
- [ ] Creator information complete
- [ ] No validation errors in quality report

### **Curation Success:**
- [ ] Metadata enhanced with relevant keywords
- [ ] Descriptions complete and bilingual
- [ ] Publication status set appropriately
- [ ] Access rights configured correctly

---

## 🚨 **Common Issues and Solutions**

### **Issue: CSV Validation Fails**
**Solution:**
```bash
# Use preview tool to identify issues
o-nakala-preview --csv folder_data_items.csv --interactive
# Fix issues shown in validation report
# Re-run preview to confirm fixes
```

### **Issue: Multilingual Format Errors**
**Solution:**
```bash
# Correct format: "fr:French text|en:English text"
# Wrong: "French text|English text" 
# Use the assistant to generate templates
```

### **Issue: COAR Type Not Recognized**
**Solution:**
```bash
# Get valid COAR types
o-nakala-preview --csv folder_data_items.csv --interactive
# Choose option 1 for COAR suggestions
# Use exact URIs provided
```

### **Issue: Upload Fails for Large Files**
**Solution:**
```bash
# For files >100MB, use chunked upload
o-nakala-upload \
  --dataset folder_data_items.csv \
  --base-path . \
  --chunk-size 50MB \
  --retry-attempts 3
```

### **Issue: Quality Report Shows Issues**
**Solution:**
```bash
# Review quality_report.json
# Create fixes CSV file
# Apply fixes with curator tool
# Re-run quality analysis to verify
```

---

## 📚 **Advanced Workflows**

### **For Large Research Projects (100+ files)**
```bash
# Use batch processing
o-nakala-upload \
  --dataset folder_data_items.csv \
  --base-path . \
  --parallel-workers 4 \
  --batch-size 10 \
  --output upload_results.csv
```

### **For Collaborative Research Teams**
```bash
# Set up shared collections with proper rights
o-nakala-collection \
  --from-upload-output upload_results.csv \
  --collaborative-mode \
  --default-rights "group:research_team:editor"
```

### **For Long-term Research Projects**
```bash
# Enable versioning and history tracking
o-nakala-upload \
  --dataset folder_data_items.csv \
  --enable-versioning \
  --version-strategy "semantic" \
  --backup-previous
```

---

## 🏆 **Best Practices for Research Data**

### **1. Metadata Quality:**
- ✅ Always provide bilingual titles and descriptions
- ✅ Use controlled vocabularies for keywords  
- ✅ Include temporal and spatial information
- ✅ Provide complete creator information

### **2. File Organization:**
- ✅ Group related files in logical collections
- ✅ Use descriptive file names
- ✅ Include README files for complex datasets
- ✅ Maintain consistent folder structure

### **3. Quality Assurance:**
- ✅ Always run quality analysis before publication
- ✅ Fix all validation errors
- ✅ Enhance metadata with relevant keywords
- ✅ Test metadata preview before upload

### **4. Long-term Preservation:**
- ✅ Use open file formats when possible
- ✅ Include methodology documentation
- ✅ Set appropriate access rights
- ✅ Plan for data updates and versioning

---

## 💡 **Quick Start for Common Research Scenarios**

### **Scenario 1: Psychology Research with Survey Data**
```bash
# Copy template
cp examples/sample_dataset/folder_data_items.csv folder_data_items.csv
# Edit with your file paths and metadata
# Run workflow
./run_workflow.sh YOUR_API_KEY
```

### **Scenario 2: Computational Research with Code and Results**
```bash
# Use software-focused template
cp examples/sample_dataset/folder_data_items.csv folder_data_items.csv
# Ensure code files use COAR type c_5ce6
# Include algorithm descriptions
```

### **Scenario 3: Historical Research with Documents and Images**
```bash
# Use humanities template
cp examples/sample_dataset/folder_data_items.csv folder_data_items.csv
# Include temporal metadata for historical periods
# Use multilingual descriptions for international research
```

---

## 📞 **Getting Help**

- **Documentation**: `/docs/` directory
- **Examples**: `/examples/` directory  
- **Sample Dataset**: `/examples/sample_dataset/`
- **API Reference**: `/docs/endpoints/` directory
- **Community**: GitHub Discussions
- **Issues**: GitHub Issues

## 📚 Official NAKALA Resources for Researchers

### **Getting Started**
- **[Official NAKALA Documentation](https://documentation.huma-num.fr/nakala/)** - Complete researcher guide
- **[Getting Started with NAKALA](https://documentation.huma-num.fr/nakala/)** - Official first steps
- **[Data Preparation Guide](https://documentation.huma-num.fr/nakala-preparer-ses-donnees/)** - How to prepare your research data

### **Research Data Management**
- **[Data Deposit Process](https://documentation.huma-num.fr/nakala/)** - Official deposit workflow
- **[Collection Management](https://documentation.huma-num.fr/nakala/)** - Organize your research data
- **[Metadata Best Practices](https://documentation.huma-num.fr/nakala-guide-de-description/)** - Dublin Core for research data

### **Platform Access**
- **[NAKALA Test Platform](https://test.nakala.fr)** - Safe environment for testing your workflow
- **[NAKALA Production](https://nakala.fr)** - Live research data repository
- **[API Documentation](https://api.nakala.fr/doc)** - Advanced automation tools

---

**🎉 Congratulations!** You've successfully transformed your folder-based research files into a well-organized, curated NAKALA repository. Your research data is now discoverable, preservable, and ready for sharing with the global research community.