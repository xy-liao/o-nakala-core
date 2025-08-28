# Collection Organization Guide

## Research Data Collections - Group and Organize Your Uploads

> **Purpose**: Learn how to create and manage collections to organize your research data  
> **Audience**: Researchers who have uploaded data and want to organize it logically  
> **Time**: 10-20 minutes depending on complexity  
> **Prerequisites**: Completed data upload, have `upload_results.csv` file

## Navigation

📋 **You are here**: Collection Guide (organizing your data)  
🔄 **Complete workflow** → [User Workflow Guide](03-workflow-guide.md)  
📤 **Need to upload first?** → [Upload Guide](01-upload-guide.md)  
🎯 **Enhance metadata** → [Curation Guide](04-curation-guide.md)

---

## What Are Collections?

**Collections** group related datasets together, making your research easier to discover and navigate.

**Think of collections as:**
- Digital folders that organize related research materials
- Thematic groupings (e.g., "2024 Field Study", "Interview Data")
- Hierarchical organization for complex projects

**Benefits:**
- **Better discovery**: Others can find all related materials together
- **Context**: Provide overarching descriptions for groups of data
- **Organization**: Logical structure for complex research projects
- **Navigation**: Easier browsing for users

---

## Quick Collection Creation

### From Your Upload Results
```bash
o-nakala-collection \
    --api-key "your-key" \
    --from-upload-output "upload_results.csv" \
    --from-folder-collections "folder_collections.csv"
```

**Replace `your-key`** with your actual NAKALA API key

<details>
<summary>📁 Setting Up Collection Configuration</summary>

### Create `folder_collections.csv`
This file defines how to group your uploaded items:

```csv
title,status,description,keywords,creator,data_items
"en:My Research Project|fr:Mon Projet de Recherche",private,"en:Complete research data from 2024 study|fr:Données complètes de l'étude 2024","research,data,2024","Smith, John","files/data/|files/code/"
"en:Interview Materials|fr:Matériel d'entretien",private,"en:Transcripts and recordings|fr:Transcriptions et enregistrements","interviews,qualitative","Smith, John","files/interviews/"
```

### Field Explanations
- **title**: Collection name (multilingual: `en:English|fr:Français`)
- **status**: `private` (default) or `public`
- **description**: What this collection contains
- **keywords**: Search terms, comma-separated
- **creator**: Who created this collection
- **data_items**: Which uploaded folders to include (pipe-separated)

</details>

<details>
<summary>🛠️ Manual Collection Creation</summary>

### Single Collection from Specific Items
```bash
o-nakala-collection \
    --api-key "your-key" \
    --title "My Research Collection" \
    --description "Important research materials" \
    --keywords "research,data,2024" \
    --status private \
    --data-ids "10.34847/nkl.abc123,10.34847/nkl.def456"
```

### Collection from All Upload Results
```bash
o-nakala-collection \
    --api-key "your-key" \
    --title "Complete Study Data" \
    --description "All data from the 2024 research study" \
    --keywords "research,complete,2024" \
    --from-upload-output "upload_results.csv"
```

</details>

---

## Collection Organization Strategies

### Strategy 1: By Research Phase
```
├── Data Collection Phase (raw data, field notes)
├── Analysis Phase (processed data, scripts)
└── Publication Phase (final datasets, figures)
```

### Strategy 2: By Data Type
```
├── Quantitative Data (surveys, measurements)
├── Qualitative Data (interviews, observations)
└── Mixed Methods (combined analyses)
```

### Strategy 3: By Topic/Theme
```
├── Climate Measurements (temperature, precipitation)
├── Soil Analysis (composition, samples)
└── Vegetation Survey (species, coverage)
```

---

## Working with Collection Results

### Understanding Your Output

After running collections, you'll get `collections_output.csv`:

```csv
collection_id,collection_title,status,data_items_count,creation_status
10.34847/nkl.abc123,"Research Data 2024",private,15,SUCCESS
10.34847/nkl.def456,"Interview Materials",private,8,SUCCESS
```

### What This Shows
- **collection_id**: Unique identifier for citing/sharing
- **collection_title**: Display name
- **data_items_count**: Number of datasets included
- **creation_status**: Whether creation succeeded

<details>
<summary>📊 Advanced Collection Management</summary>

### Generate Collection Report
```bash
o-nakala-collection \
    --api-key "your-key" \
    --from-folder-collections "folder_collections.csv" \
    --from-upload-output "upload_results.csv" \
    --collection-report "detailed_collections.csv"
```

### Collection Hierarchy Example
The system can create nested organization:

```
Research Project 2024
├── Data Collection
│   ├── Survey Responses (15 items)
│   └── Field Measurements (8 items)
├── Analysis Results
│   ├── Statistical Output (5 items)
│   └── Visualizations (12 items)
└── Documentation
    ├── Protocols (3 items)
    └── Reports (7 items)
```

### Troubleshooting Collection Issues

**"No matching data items found"**
- Check that folder paths in `data_items` match your upload structure
- Verify `upload_results.csv` contains the expected items

**"Collection creation failed"**
- Verify your API key is correct
- Check that required fields (title, creator) are provided
- Ensure data item IDs exist and are accessible

</details>

---

## Best Practices

### 1. **Descriptive Naming**
```bash
# Good
title: "en:Climate Study 2024 - Temperature Data|fr:Étude Climatique 2024 - Données de Température"

# Avoid
title: "data1"
```

### 2. **Logical Grouping**
- Group by research question, not just file type
- Consider how others will discover your work
- Balance detail with usability (not too many small collections)

### 3. **Multilingual Support**
- Provide both English and French titles/descriptions
- Use format: `en:English text|fr:Texte français`
- Include keywords in both languages

### 4. **Consistent Metadata**
- Use the same creator format across collections
- Apply consistent keyword vocabulary
- Maintain similar description patterns

---

## Next Steps

### ✅ **You've Organized Your Data**
Your research is now logically grouped and easier to discover!

### 🚀 **What's Next?**
- **Enhance metadata** → [Curation Guide](04-curation-guide.md)
- **Complete workflow** → [User Workflow Guide](03-workflow-guide.md)
- **Publish your data** → Change status from private to public
- **Share collections** → Send collection URLs to collaborators

### 📄 **Files Created**
- `collections_output.csv` - Details of created collections
- `nakala_collection.log` - Detailed operation logs

---

## Related Guides

📋 **Collection organization** (you completed this)  
📤 **Upload your data** → [Upload Guide](01-upload-guide.md)  
🔧 **Improve metadata** → [Curation Guide](04-curation-guide.md)  
🔄 **Complete workflow** → [User Workflow Guide](03-workflow-guide.md)  
❓ **Problems?** → [Troubleshooting](05-troubleshooting.md)

## 📚 Official NAKALA Resources

### **Collection Management**
- **[Official NAKALA Documentation](https://documentation.huma-num.fr/nakala/)** - Complete platform guide including collection management
- **[Collection Creation Guide](https://documentation.huma-num.fr/nakala/collection-creation-form/)** - Official collection creation documentation
- **[Metadata Standards](https://documentation.huma-num.fr/nakala-guide-de-description/)** - Dublin Core metadata specifications for collections

### **Platform Access**
- **[NAKALA Test Platform](https://test.nakala.fr)** - Practice collection creation safely
- **[NAKALA Production](https://nakala.fr)** - Live research data repository
- **[API Documentation](https://api.nakala.fr/doc)** - Collection management via API