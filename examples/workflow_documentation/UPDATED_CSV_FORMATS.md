# Updated CSV Formats for Workshop Exercises

## ✅ Tested and Working CSV Formats

**Updated:** 2025-06-08 after comprehensive API testing

### Upload Configuration Format
```csv
file,status,type,title,alternative,author,contributor,date,license,description,keywords,language,temporal,spatial,accessRights,identifier,rights
files/code/,pending,http://purl.org/coar/resource_type/c_5ce6,fr:Fichiers de code|en:Code Files,fr:Scripts et modules|en:Scripts and Modules,"Dupont,Jean","",2023-05-21,CC-BY-4.0,fr:Scripts pour l'analyse de données|en:Scripts for data analysis,fr:code;programmation;scripts|en:code;programming;scripts,fr,2023-01/2023-12,fr:Global|en:Global,Open Access,,"de0f2a9b-a198-48a4-8074-db5120187a16,ROLE_READER"
```

### Collection Configuration Format
```csv
title,status,description,keywords,language,creator,contributor,publisher,date,rights,coverage,relation,source,data_items
"fr:Collection de Code et Données|en:Code and Data Collection",private,"fr:Collection contenant des scripts et des données associées|en:Collection containing scripts and associated data","fr:code;données;analyse|en:code;data;analysis","fr:fr|en:en","fr:Doe,John;Smith,Jane|en:Doe,John;Smith,Jane","fr:Johnson,Robert;Williams,Emily|en:Johnson,Robert;Williams,Emily","fr:Université Paris 1|en:Université Paris 1","fr:2024-05-21|en:2024-05-21","fr:CC-BY-4.0|en:CC-BY-4.0","fr:Global|en:Global","fr:Lié à des projets de recherche|en:Related to research projects","fr:Données originales|en:Original data","files/code/|files/data/"
```

### Batch Modification Format (STABLE)

#### ✅ Working Format - Core Fields Only
```csv
id,action,new_title,new_description,new_keywords
10.34847/nkl.9d9601xz,modify,"fr:Collection de Code Mise à Jour|en:Updated Code Collection","fr:Collection mise à jour avec de nouvelles métadonnées|en:Collection updated with new metadata","fr:code;test;mise à jour|en:code;test;update"
```

#### ✅ Simple Creator Fix Format
```csv
id,action,new_creator
10.34847/nkl.9d9601xz,modify,"Doe, John;Smith, Jane"
```

#### ⚠️ Complex Modifications (May Cause API Errors)
Some fields cause API 500 errors when used with complex multilingual formats:
- `new_contributor` with multiple values
- `new_publisher` with multilingual format
- `new_source`, `new_relation` with complex content

### 🎯 Recommended Workshop Progression

#### Step 1: Basic Modifications (Always Works)
```csv
id,action,new_title,new_description
collection_id,modify,"fr:Nouveau Titre|en:New Title","fr:Nouvelle description|en:New description"
```

#### Step 2: Keyword Enhancement
```csv
id,action,new_keywords
collection_id,modify,"fr:mot-clé1;mot-clé2;mot-clé3|en:keyword1;keyword2;keyword3"
```

#### Step 3: Creator Assignment
```csv
id,action,new_creator
collection_id,modify,"Last, First;Another, Name"
```

### 📋 Field Support Status

| Field | Collections | Datasets | Notes |
|-------|-------------|----------|--------|
| `new_title` | ✅ | ✅ | Multilingual format supported |
| `new_description` | ✅ | ✅ | Multilingual format supported |
| `new_keywords` | ✅ | ✅ | Semicolon-separated, multilingual |
| `new_creator` | ✅ | ✅ | Simple comma-separated names |
| `new_contributor` | ⚠️ | ⚠️ | Simple values only, avoid complex formats |
| `new_publisher` | ⚠️ | ⚠️ | Simple values only |
| `new_language` | ✅ | ✅ | ISO language codes |
| `new_license` | ✅ | ✅ | Standard license identifiers |
| `new_relation` | ⚠️ | ⚠️ | Simple text only |
| `new_source` | ⚠️ | ⚠️ | Simple text only |

### 🔧 Troubleshooting Tips

#### API Error 500 (Array Given)
**Cause:** Complex field values being parsed as arrays
**Solution:** Simplify field values, avoid nested multilingual structures in contributor/publisher fields

#### Validation Errors
**Cause:** Missing required columns or invalid field names
**Solution:** Ensure CSV has: `id`, `action`, and at least one `new_*` field

#### Field Not Supported
**Cause:** Using unsupported field names
**Solution:** Check supported fields with: `nakala-curator --list-fields`

### 📚 Complete Working Example

```csv
id,action,new_title,new_description,new_keywords,new_creator
10.34847/nkl.example1,modify,"fr:Titre Amélioré|en:Enhanced Title","fr:Description complète et détaillée|en:Complete and detailed description","fr:recherche;données;analyse|en:research;data;analysis","Smith, Jane;Doe, John"
10.34847/nkl.example2,modify,"fr:Autre Collection|en:Another Collection","fr:Deuxième exemple de modification|en:Second modification example","fr:exemples;tests;validation|en:examples;tests;validation","Researcher, Lead"
```

### 🎓 Workshop Exercise Files

Use these files for hands-on workshop training:

1. **Basic Upload**: `folder_data_items.csv` (provided)
2. **Collection Creation**: `folder_collections.csv` (provided)
3. **Simple Modifications**: `simple_field_test.csv` (tested working)
4. **Creator Fixes**: `workshop_collection_fix_correct.csv` (tested working)

All files have been validated with real API calls and work reliably for workshop scenarios.