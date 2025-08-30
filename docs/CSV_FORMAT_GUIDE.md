# CSV Format Guide: Complete Reference

**📍 You are here:** [START_HERE](../START_HERE.md) → [Getting Started](GETTING_STARTED.md) → CSV Format Guide

**⏱️ Time:** 10-20 minutes | **👥 Audience:** All users | **📈 Level:** Reference

This comprehensive guide covers CSV format requirements for all O-Nakala Core operations: uploads, collections, and curation.

## Quick Start: Minimum Viable CSV

### Basic Upload Format
```csv
file,status,type,title
data.pdf,pending,http://purl.org/coar/resource_type/c_6501,"Research Results"
code.py,pending,http://purl.org/coar/resource_type/c_5ce6,"Analysis Script"
```

**Required fields:** `file`, `status`, `type`, `title`  
**Common values:** See [Quick Values Reference](#quick-values-reference) below.

### Basic Collection Format
```csv
collection_name,description,rights,status
"Research Data 2024","My research collection","CC-BY-4.0",pending
```

**Required fields:** `collection_name`, `description`

## Complete Field Reference

### Upload CSV Fields (All Optional Except Required*)

| Field | Required* | Purpose | Example Values |
|-------|-----------|---------|----------------|
| **file** | ✅ | Path to file | `data/results.csv`, `documents/paper.pdf` |
| **status** | ✅ | Publication status | `pending`, `published` |
| **type** | ✅ | Resource type (COAR URI) | `http://purl.org/coar/resource_type/c_ddb1` |
| **title** | ✅ | Resource title | `"Survey Results 2024"` |
| **alternative** | | Alternative title | `"Complete Dataset"` |
| **creator** | | Author/creator | `"Smith,Jane;Doe,John"` |
| **contributor** | | Additional contributors | `"Wilson,Bob"` |
| **date** | | Creation/publication date | `2024-03-15` |
| **license** | | License identifier | `CC-BY-4.0`, `CC0-1.0` |
| **description** | | Detailed description | `"Survey results from 200 participants"` |
| **keywords** | | Subject keywords | `"survey;research;statistics"` |
| **language** | | Content language | `en`, `fr`, `zh` |
| **temporal** | | Time period covered | `2024`, `2020-2024` |
| **spatial** | | Geographic coverage | `"Paris, France"`, `"Global"` |
| **accessRights** | | Access level | `Open Access`, `Restricted` |
| **identifier** | | External identifier | DOI, URL, custom ID |
| **rights** | | Rights statement | Custom rights text |

### Collection CSV Fields

| Field | Required* | Purpose | Example Values |
|-------|-----------|---------|----------------|
| **collection_name** | ✅ | Collection identifier | `"Research Project 2024"` |
| **description** | ✅ | Collection description | `"Complete dataset and analysis"` |
| **keywords** | | Subject terms | `"research;data;analysis"` |
| **rights** | | Default license | `CC-BY-4.0` |
| **status** | | Collection status | `pending`, `published` |

## Field Format Specifications

### File Paths
- **Relative paths only**: `data/file.csv` ✅, `/home/user/file.csv` ❌
- **No spaces in paths**: `my data.csv` ❌, `my_data.csv` ✅
- **Cross-platform separators**: Use `/` (converted automatically)

### Creator and Contributor Format
```csv
# Single person
creator,contributor
"Smith,Jane",""

# Multiple people (semicolon-separated)
creator,contributor
"Smith,Jane;Doe,John","Wilson,Bob;Brown,Alice"

# With institutional affiliation (optional)
creator,contributor
"Smith,Jane (University of Paris)","Research Institute"
```

### Date Formats
```csv
# ISO 8601 format (preferred)
date,temporal
2024-03-15,2024

# Year only
date,temporal
2024,2024

# Date ranges
date,temporal
2024-03-15,2020-2024
```

### Keywords and Subject Terms
```csv
# Semicolon-separated, no spaces after semicolons
keywords
"research;data;analysis;statistics"

# Multiple languages (use language codes)
keywords
"en:research;data|fr:recherche;données"

# Avoid
keywords
"research, data, analysis"  # Commas not recommended
"research ; data"           # Spaces after semicolons
```

### Resource Types (COAR URIs)
Use standard COAR resource type URIs:

| Type | URI | Usage |
|------|-----|-------|
| **Dataset** | `http://purl.org/coar/resource_type/c_ddb1` | Data files, databases |
| **Text** | `http://purl.org/coar/resource_type/c_6501` | Articles, reports, documents |
| **Software** | `http://purl.org/coar/resource_type/c_5ce6` | Code, scripts, applications |
| **Image** | `http://purl.org/coar/resource_type/c_c513` | Photos, figures, diagrams |
| **Collection** | `http://purl.org/coar/resource_type/c_c513` | Multi-item collections |

> **💡 Resource type help**: Use `o-nakala-preview --csv your_file.csv --interactive` to get suggestions based on your content.

### License Identifiers
```csv
# Creative Commons (most common)
license
CC-BY-4.0        # Attribution required
CC-BY-SA-4.0     # Attribution + ShareAlike  
CC-BY-NC-4.0     # Attribution + NonCommercial
CC0-1.0          # Public domain

# Custom licenses
license
"Custom institutional license"
"All rights reserved"
```

## Quick Values Reference

### Common Status Values
- `pending` - Draft, not yet published
- `published` - Publicly accessible

### Common Access Rights
- `Open Access` - Freely available
- `Restricted` - Access limitations apply
- `Embargoed` - Delayed access

### Common Language Codes (ISO 639-1)
- `en` - English
- `fr` - French  
- `de` - German
- `es` - Spanish
- `zh` - Chinese
- `ja` - Japanese

## CSV Format Best Practices

### File Encoding and Structure
```csv
# Always use UTF-8 encoding
# Header row required
# Quoted fields for safety (especially with commas/semicolons in content)

file,status,type,title,description
"data/survey.csv",pending,http://purl.org/coar/resource_type/c_ddb1,"Survey Data","Results from 200 participants, March 2024"
```

### Handling Special Characters
```csv
# Quote fields containing commas, quotes, or newlines
description
"Data includes responses to questions: ""What is your age?"", ""Where do you live?"""

# Escape quotes with double quotes
title
"Analysis of ""Big Data"" in Healthcare"

# Handle newlines in descriptions  
description
"First line of description
Second line continues here"
```

### Empty Fields
```csv
# Leave empty fields blank or use empty quotes
file,creator,contributor,description
"data.csv","Smith,Jane","","Complete dataset"
"code.py","","Wilson,Bob",""
```

## Validation and Testing

### Preview Before Upload
```bash
# Always validate your CSV first
o-nakala-preview --csv your_data.csv --validate-only

# Interactive validation with suggestions
o-nakala-preview --csv your_data.csv --interactive

# Export validation report
o-nakala-preview --csv your_data.csv --json-output validation.json
```

### Common Validation Errors

#### File Path Issues
```csv
# ❌ Wrong - absolute paths
file
/home/user/data.csv

# ❌ Wrong - backslashes  
file
data\results.csv

# ✅ Correct - relative paths
file
data/results.csv
```

#### Missing Required Fields
```csv
# ❌ Wrong - missing required fields
file,title
data.csv,"My Data"

# ✅ Correct - all required fields
file,status,type,title
data.csv,pending,http://purl.org/coar/resource_type/c_ddb1,"My Data"
```

#### Invalid Resource Types
```csv
# ❌ Wrong - invalid URI
type
dataset

# ❌ Wrong - incomplete URI
type
c_ddb1

# ✅ Correct - complete COAR URI
type
http://purl.org/coar/resource_type/c_ddb1
```

## Templates and Examples

### Research Data Template
```csv
file,status,type,title,alternative,creator,contributor,date,license,description,keywords,language,temporal,spatial,accessRights
"data/survey_results.csv",pending,http://purl.org/coar/resource_type/c_ddb1,"Survey Results 2024","Complete Survey Dataset","Smith,Jane","Wilson,Bob","2024-03-15",CC-BY-4.0,"Survey results from 200 participants in March 2024","survey;research;statistics","en","2024","Paris, France","Open Access"
"code/analysis.py",pending,http://purl.org/coar/resource_type/c_5ce6,"Data Analysis Script","Survey Analysis Code","Smith,Jane","","2024-03-16",CC-BY-4.0,"Python script for analyzing survey results","python;analysis;statistics","en","2024","","Open Access"
```

### Multi-Format Collection Template
```csv
file,status,type,title,creator,date,license,description,keywords,language
"documents/paper.pdf",pending,http://purl.org/coar/resource_type/c_6501,"Research Paper","Smith,Jane","2024-03-20",CC-BY-4.0,"Final research paper based on survey results","paper;research;publication","en"
"images/figure1.png",pending,http://purl.org/coar/resource_type/c_c513,"Figure 1: Survey Demographics","Smith,Jane","2024-03-18",CC-BY-4.0,"Demographic breakdown of survey participants","figure;demographics;visualization","en"
"presentations/conference.pdf",pending,http://purl.org/coar/resource_type/c_6501,"Conference Presentation","Smith,Jane","2024-03-22",CC-BY-4.0,"Presentation for XYZ Conference 2024","presentation;conference;slides","en"
```

### Collection Organization Template
```csv
collection_name,description,keywords,rights,status
"Research Project 2024 - Complete Dataset","All materials from the 2024 research project including data, analysis, and publications","research;2024;complete","CC-BY-4.0","pending"
"Survey Data and Analysis","Raw survey data and analysis scripts","survey;data;analysis","CC-BY-4.0","pending"
"Publications and Presentations","Papers and presentations based on the research","publications;presentations;dissemination","CC-BY-4.0","pending"
```

## Advanced CSV Features

### Conditional Fields
Some fields have different requirements based on status:

```csv
# For published items, creator is typically required
file,status,type,title,creator
"data.csv",published,http://purl.org/coar/resource_type/c_ddb1,"Survey Data","Smith,Jane"

# For pending items, creator can be added later
file,status,type,title,creator
"draft.csv",pending,http://purl.org/coar/resource_type/c_ddb1,"Draft Analysis",""
```

### Cross-References Between Items
```csv
# Use identifier field to create relationships
file,status,type,title,identifier,description
"data.csv",pending,http://purl.org/coar/resource_type/c_ddb1,"Raw Data","dataset_001","Source data for analysis"
"analysis.py",pending,http://purl.org/coar/resource_type/c_5ce6,"Analysis Script","script_001","Processes dataset_001"
```

### Multilingual Metadata
```csv
# Use multiple rows for multilingual content
file,status,type,title,description,language
"document.pdf",pending,http://purl.org/coar/resource_type/c_6501,"English Title","English description","en"
"document.pdf",pending,http://purl.org/coar/resource_type/c_6501,"Titre Français","Description française","fr"
```

## Troubleshooting CSV Issues

### Encoding Problems
```bash
# Check file encoding
file -I your_file.csv

# Convert to UTF-8 if needed
iconv -f ISO-8859-1 -t UTF-8 your_file.csv > fixed_file.csv
```

### Excel Compatibility
```bash
# If editing in Excel, save as "CSV UTF-8"
# Avoid Excel's default CSV format which may use local encoding

# Alternative: Use LibreOffice Calc or Google Sheets
# Both handle UTF-8 CSV correctly by default
```

### Large CSV Files
```bash
# For files with 1000+ rows, consider splitting
split -l 500 large_file.csv batch_

# Process in batches for better error handling and progress tracking
```

---

## 🧭 Navigation

### ⬅️ Previous Steps
- [Getting Started](GETTING_STARTED.md) - Basic concepts and first upload

### ➡️ Next Steps  
- **Ready to upload**: [Upload Guide](user-guides/01-upload-guide.md)
- **Need examples**: [Sample Dataset](../examples/sample_dataset/)
- **Complex workflows**: [Complete Workflow Guide](user-guides/03-workflow-guide.md)

### 🔍 Related Resources
- [Field Reference](curator-field-reference.md) - Complete metadata field guide
- [Quick Reference](guides/quick-reference.md) - Essential commands
- [Troubleshooting](user-guides/05-troubleshooting.md) - CSV-specific issues

### 🆘 Need Help?
- **CSV validation**: Use `o-nakala-preview --csv file.csv --interactive`
- **Format issues**: [CSV troubleshooting section](user-guides/05-troubleshooting.md#csv-format-issues)
- **Examples**: Browse [templates](../examples/templates/) directory

---

*📍 **You are here:** [START_HERE](../START_HERE.md) → [Getting Started](GETTING_STARTED.md) → CSV Format Guide*

*Complete CSV format specifications for upload, collection, and curator endpoints. Last updated: August 2025*