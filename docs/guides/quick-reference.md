# Quick Reference: O-Nakala Core v2.5.0

## 🚀 Essential Commands

### **NEW: Preview First (Recommended)**
```bash
# Interactive validation and preview
o-nakala-preview --csv your_data.csv --interactive

# Quick validation only
o-nakala-preview --csv your_data.csv --validate-only

# Export detailed preview
o-nakala-preview --csv your_data.csv --json-output preview.json
```

### **Enhanced Upload (Same Commands, Better Results)**
```bash
# Basic upload (now 65% richer metadata)
o-nakala-upload --csv data.csv --api-key $API_KEY

# Folder mode with enhanced metadata
o-nakala-upload --dataset folder_data.csv --mode folder --base-path ./files --api-key $API_KEY

# With output tracking
o-nakala-upload --csv data.csv --api-key $API_KEY --output results.csv
```

### **Collections & Management**
```bash
# Create collections from uploads
o-nakala-collection --from-upload-output results.csv --api-key $API_KEY

# Quality analysis with enhanced validation
o-nakala-curator --quality-report --api-key $API_KEY

# User information
o-nakala-user-info --api-key $API_KEY --collections-only
```

## 📝 CSV Format Guide

### **Required Fields**
```csv
file,title,type
data.csv,"Research Data",http://purl.org/coar/resource_type/c_ddb1
```

### **Recommended Complete Format**
```csv
file,title,creator,description,type,date,keywords,language,temporal,spatial,license
data.csv,"fr:Données de recherche|en:Research Data","Dupont,Jean","fr:Analyse des résultats|en:Results analysis",http://purl.org/coar/resource_type/c_ddb1,2024,"fr:recherche;données|en:research;data",fr,2024,"fr:Global|en:Global",CC-BY-4.0
```

### **All Supported Fields (v2.5.0 Complete)**
| Field | Description | Example | v2.5.0 Status |
|-------|-------------|---------|----------------|
| `title` | Resource title | `"fr:Titre|en:Title"` | ✅ Enhanced |
| `creator` | Author/Creator | `"Dupont,Jean"` | ✅ Enhanced |
| `description` | Detailed description | `"fr:Description|en:Description"` | ✅ Enhanced |
| `type` | COAR resource type | `http://purl.org/coar/resource_type/c_ddb1` | ✅ Enhanced |
| `date` | Publication date | `2024` or `2024-03-21` | ✅ Enhanced |
| `keywords` | Subject keywords | `"fr:mot-clé;recherche|en:keyword;research"` | ✅ Enhanced |
| `language` | Primary language | `fr`, `en`, `fr,en` | ✅ Enhanced |
| `license` | License | `CC-BY-4.0`, `All rights reserved` | ✅ Enhanced |
| `rights` | Rights statement | Custom rights text | ✅ Enhanced |
| `contributor` | Additional contributors | `"Martin,Paul"` | ✅ Enhanced |
| `accessRights` | Access level | `Open Access`, `Restricted` | ✅ Enhanced |
| **`spatial`** | **Geographic coverage** | **`"fr:France|en:France"`** | **🆕 Fixed in v2.5.0** |
| **`temporal`** | **Time period** | **`"2020-2024"`, `"Medieval"`** | **🆕 Fixed in v2.5.0** |
| **`alternative`** | **Alternative title** | **`"fr:Titre alt|en:Alt title"`** | **🆕 Fixed in v2.5.0** |
| **`identifier`** | **Resource ID** | **`"DOI:10.1234/example"`** | **🆕 Fixed in v2.5.0** |

## 🎯 COAR Resource Types (Copy-Paste Ready)

### **Common Types**
```csv
# Dataset
type,http://purl.org/coar/resource_type/c_ddb1

# Software/Code  
type,http://purl.org/coar/resource_type/c_5ce6

# Text/Document
type,http://purl.org/coar/resource_type/c_18cf

# Image
type,http://purl.org/coar/resource_type/c_c513

# Presentation/Lecture
type,http://purl.org/coar/resource_type/c_8544
```

### **Get Suggestions Interactively**
```bash
o-nakala-preview --csv data.csv --interactive
# Choose option 1: COAR resource type suggestions
# Enter content description for smart recommendations
```

## 💡 Quick Templates

### **Research Paper**
```csv
file,title,creator,description,type,date,keywords,language
paper.pdf,"fr:Article de recherche|en:Research paper","Smith,Jane","fr:Analyse détaillée|en:Detailed analysis",http://purl.org/coar/resource_type/c_18cf,2024,"fr:recherche;analyse|en:research;analysis",fr
```

### **Dataset**
```csv
file,title,creator,description,type,temporal,spatial,license
data.csv,"fr:Jeu de données|en:Dataset","Smith,Jane","fr:Données de l'enquête|en:Survey data",http://purl.org/coar/resource_type/c_ddb1,2024,"fr:France|en:France",CC-BY-4.0
```

### **Code/Software**
```csv
file,title,creator,description,type,date,keywords
scripts/,"fr:Scripts d'analyse|en:Analysis scripts","Smith,Jane","fr:Code Python pour analyse|en:Python analysis code",http://purl.org/coar/resource_type/c_5ce6,2024,"fr:code;python|en:code;python"
```

## 🔧 Workflow Patterns

### **Pattern 1: Quick Upload**
```bash
# For urgent/simple uploads
o-nakala-upload --csv data.csv --api-key $API_KEY
```

### **Pattern 2: Validated Upload (Recommended)**  
```bash
# Best practice workflow
o-nakala-preview --csv data.csv --validate-only
o-nakala-upload --csv data.csv --api-key $API_KEY
```

### **Pattern 3: Interactive Workflow**
```bash
# For complex/new metadata
o-nakala-preview --csv data.csv --interactive
# Use menu options to improve metadata
o-nakala-upload --csv data.csv --api-key $API_KEY
```

### **Pattern 4: Team Collaboration**
```bash
# Generate preview for team review
o-nakala-preview --csv project_data.csv --json-output team_review.json
# Share team_review.json, gather feedback, improve CSV
o-nakala-upload --csv project_data_final.csv --api-key $API_KEY
```

### **Pattern 5: Batch Processing**
```bash
# Validate all files first
for csv_file in *.csv; do
    o-nakala-preview --csv "$csv_file" --validate-only
done

# Upload only if all validate
for csv_file in *.csv; do
    o-nakala-upload --csv "$csv_file" --api-key $API_KEY
done
```

## ⚡ Installation & Setup

### **Install v2.5.0**
```bash
# Complete installation with preview tool
pip install o-nakala-core[cli,ml]==2.5.0

# Verify preview tool works
o-nakala-preview --help
```

### **Environment Setup**
```bash
# Set API key (get from api/api_keys.md for testing)
export NAKALA_API_KEY="your-api-key"

# Optional: Set environment (defaults to test)
export NAKALA_BASE_URL="https://apitest.nakala.fr"  # Test
export NAKALA_BASE_URL="https://api.nakala.fr"     # Production
```

## 🚨 Troubleshooting

### **Common Issues & Quick Fixes**

| Problem | Solution |
|---------|----------|
| `o-nakala-preview` not found | `pip install o-nakala-core[cli]==2.5.0` |
| Invalid COAR resource type | Use interactive preview: choose option 1 |
| Date format errors | Use `YYYY` or `YYYY-MM-DD` format |
| Bilingual format issues | Use `"fr:Français|en:English"` pattern |
| Missing required fields | Preview tool shows exactly what's missing |
| Upload fails after preview passes | Check API key and network connection |

### **Validation Commands**
```bash
# Quick health check
o-nakala-preview --csv data.csv --validate-only

# Detailed validation with suggestions  
o-nakala-preview --csv data.csv --interactive

# Check specific field formats
python -c "from o_nakala_core.common.utils import NakalaCommonUtils; print(NakalaCommonUtils().PROPERTY_URIS.keys())"
```

## 📊 Version Comparison

### **What's Better in v2.5.0**
| Aspect | Before v2.5.0 | v2.5.0 | Improvement |
|--------|---------------|--------|-------------|
| **Metadata Fields** | ~65 entries | 107 entries | +65% |
| **Dublin Core** | 11/15 fields | 15/15 fields | Complete |
| **Error Prevention** | After upload | Before upload | Proactive |
| **Resource Types** | Manual lookup | Interactive suggestions | User-friendly |
| **Team Workflow** | Individual only | Collaborative preview | Team-ready |

### **Rescue Mission Completed**
These fields were **lost in previous versions** and are **rescued in v2.5.0**:
- ✅ `spatial` - Geographic coverage now preserved
- ✅ `temporal` - Time periods now captured  
- ✅ `alternative` - Alternative titles now included
- ✅ `identifier` - DOIs and URIs now linked

## 🎉 Success Indicators

### **You're Using v2.5.0 Successfully When:**
- [ ] Preview tool shows 15/15 Dublin Core fields for complete data
- [ ] Upload success rate is 90%+ (vs ~60% previously)
- [ ] You can see spatial/temporal metadata in NAKALA after upload
- [ ] Interactive suggestions help improve your metadata quality
- [ ] Team can collaborate using JSON preview exports

### **Next Steps**
- Explore all interactive preview features
- Generate metadata templates for your research domain  
- Set up collaborative workflows with your team
- Consider upgrading existing datasets that lost spatial/temporal data

---

**Quick Start Command:**
```bash
o-nakala-preview --csv your_data.csv --interactive
```

**This single command transforms your NAKALA workflow from guesswork to confidence!** 🚀