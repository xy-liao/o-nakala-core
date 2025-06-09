# Collection CSV Format Specification

## 🎯 Overview

This specification defines the **complete CSV format** for Collection endpoint processing. Collections organize existing datasets into logical groups using **folder pattern matching** and **Dublin Core metadata**.

## 📋 Required CSV Structure

### **Column Header Format**
```csv
title,status,description,keywords,language,creator,contributor,publisher,date,rights,coverage,relation,source,data_items
```

### **Encoding Requirements**
- **Character Encoding**: UTF-8 (required for multilingual content)
- **Delimiter**: Comma (`,`)
- **Quote Character**: Double quote (`"`) for fields containing commas or multilingual syntax
- **Line Endings**: Unix LF (`\n`) or Windows CRLF (`\r\n`)

## 🔧 Field Specifications

### **Required Fields**

#### **`title`** *(Required)*
**Purpose**: Collection name and primary identifier
**Format**: Text string or multilingual format
**Validation**: 
- ✅ Non-empty string required
- ✅ Supports multilingual syntax: `"lang:text|lang:text"`
- ❌ Cannot be null or empty

**Examples**:
```csv
title
"Research Code Collection"
"fr:Collection de code|en:Code Collection"
"Dataset Repository"
```

#### **`status`** *(Required)*
**Purpose**: Collection visibility and publication status
**Format**: Controlled vocabulary
**Validation**:
- ✅ Must be exactly: `published`, `pending`, or `private`
- ❌ Case sensitive
- ❌ No other values accepted

**Examples**:
```csv
status
published
pending
private
```

#### **`data_items`** *(Required)*
**Purpose**: Folder patterns for automatic dataset inclusion
**Format**: Pipe-separated folder patterns
**Validation**:
- ✅ Non-empty string required
- ✅ Multiple patterns separated by `|`
- ✅ Matches against uploaded dataset titles

**Examples**:
```csv
data_items
"files/code/"
"files/data/|files/results/"
"code|programming|scripts"
```

### **Optional Metadata Fields**

#### **`description`** *(Optional)*
**Purpose**: Detailed collection description
**Format**: Text string or multilingual format
**Property URI**: `http://purl.org/dc/terms/description`
**Validation**:
- ✅ Empty allowed
- ✅ Supports multilingual syntax
- ✅ No length restrictions

**Examples**:
```csv
description
"Collection of research analysis code"
"fr:Collection de données de recherche|en:Research data collection"
""
```

#### **`keywords`** *(Optional)*
**Purpose**: Subject keywords for discovery
**Format**: Semicolon-separated terms (can be multilingual)
**Property URI**: `http://purl.org/dc/terms/subject`
**Validation**:
- ✅ Semicolon-separated terms
- ✅ Supports multilingual terms
- ✅ Empty allowed

**Examples**:
```csv
keywords
"research;data;analysis"
"fr:recherche;données|en:research;data"
"programming;python;scripts;automation"
```

#### **`creator`** *(Optional)*
**Purpose**: Collection creator(s)
**Format**: Semicolon-separated person names (Surname, Givenname format)
**Property URI**: `http://nakala.fr/terms#creator`
**Validation**:
- ✅ Format: "Surname, Givenname"
- ✅ Multiple creators separated by semicolon
- ✅ Simple names allowed if comma format not possible

**Examples**:
```csv
creator
"Smith, John"
"Smith, John;Doe, Jane;Wilson, Sarah"
"Research Team"
```

#### **`contributor`** *(Optional)*
**Purpose**: Additional contributors or institutions
**Format**: Semicolon-separated names (supports multilingual)
**Property URI**: `http://purl.org/dc/terms/contributor`
**Validation**:
- ✅ Institutional names allowed
- ✅ Supports multilingual format
- ✅ Multiple contributors separated by semicolon

**Examples**:
```csv
contributor
"University Research Lab"
"fr:CNRS;Université de Paris|en:CNRS;University of Paris"
"Data Analysis Team;Statistics Department"
```

#### **`publisher`** *(Optional)*
**Purpose**: Publishing institution or organization
**Format**: Text string or multilingual format
**Property URI**: `http://purl.org/dc/terms/publisher`

**Examples**:
```csv
publisher
"Research Institute"
"fr:Institut de Recherche|en:Research Institute"
```

#### **`language`** *(Optional)*
**Purpose**: Primary language of collection content
**Format**: ISO 639-1/639-2 language code
**Property URI**: `http://purl.org/dc/terms/language`
**Validation**:
- ✅ 2-3 character language codes preferred
- ✅ Examples: `fr`, `en`, `de`, `spa`, `fra`

**Examples**:
```csv
language
fr
en
multilingual
```

#### **`date`** *(Optional)*
**Purpose**: Collection creation or coverage date
**Format**: ISO 8601 date format (YYYY-MM-DD)
**Property URI**: `http://nakala.fr/terms#created`
**Validation**:
- ✅ ISO format: YYYY-MM-DD
- ✅ Date ranges: YYYY-MM-DD/YYYY-MM-DD
- ⚠️ Other formats accepted but not recommended

**Examples**:
```csv
date
2023-06-09
2023-01-01/2023-12-31
2023
```

#### **`coverage`** *(Optional)*
**Purpose**: Temporal or spatial coverage
**Format**: Text description (supports multilingual)
**Property URI**: `http://purl.org/dc/terms/coverage`

**Examples**:
```csv
coverage
"2020-2023"
"fr:France|en:France" 
"European Union"
```

#### **`relation`** *(Optional)*
**Purpose**: Related resources or collections
**Format**: URLs or identifiers (supports multilingual descriptions)
**Property URI**: `http://purl.org/dc/terms/relation`

**Examples**:
```csv
relation
"https://doi.org/10.1234/related.collection"
"Related Project Dataset"
```

#### **`source`** *(Optional)*
**Purpose**: Source information or provenance
**Format**: Text description or URLs (supports multilingual)
**Property URI**: `http://purl.org/dc/terms/source`

**Examples**:
```csv
source
"Derived from National Survey 2023"
"https://example.org/original-data"
```

#### **`rights`** *(Optional)*
**Purpose**: Access rights configuration  
**Format**: `group_id,ROLE_NAME` format
**Validation**:
- ✅ Format: "group_id,ROLE_NAME"
- ✅ Multiple rights separated by semicolon
- ✅ Valid roles: OWNER, ADMIN, EDITOR, READER

**Examples**:
```csv
rights
"de0f2a9b-a198-48a4-8074-db5120187a16,ROLE_READER"
"group1,ROLE_EDITOR;group2,ROLE_READER"
```

## 🌐 Multilingual Format Specification

### **Syntax**: `"lang:text|lang:text"`

#### **Single Language**
```csv
title
"Research Collection"
```

#### **Multiple Languages**
```csv
title
"fr:Collection de recherche|en:Research Collection"
```

#### **Complex Multilingual with Keywords**
```csv
keywords
"fr:recherche;données;analyse|en:research;data;analysis"
```

### **Language Code Guidelines**
- **ISO 639-1**: Preferred 2-letter codes (`fr`, `en`, `de`)
- **ISO 639-2**: 3-letter codes accepted (`fra`, `eng`, `deu`)
- **Undefined**: Use `und` if language unknown
- **Mixed content**: Use primary language code

## 📊 Validation Rules

### **Structural Validation**
- ✅ **Required columns**: `title`, `status`, `data_items` must be present
- ✅ **Column order**: Flexible (any order acceptable)
- ✅ **Extra columns**: Ignored during processing
- ✅ **Empty rows**: Skipped automatically

### **Content Validation**
- ✅ **Non-empty required fields**: title, status, data_items
- ✅ **Valid status values**: published/pending/private only
- ✅ **Pattern format**: data_items must contain folder patterns
- ✅ **Multilingual syntax**: Proper lang:text|lang:text format

### **Data Type Validation**
- ✅ **Text fields**: UTF-8 encoded strings
- ✅ **Date fields**: ISO 8601 format validation
- ✅ **Rights format**: group_id,ROLE validation
- ✅ **Language codes**: ISO 639 format checking

## 🎯 Complete Example

```csv
title,status,description,keywords,language,creator,contributor,publisher,date,rights,coverage,relation,source,data_items
"fr:Collection de code|en:Code Collection",published,"fr:Scripts d'analyse|en:Analysis scripts","fr:code;programmation|en:code;programming",fr,"Smith, John","fr:Laboratoire de recherche|en:Research Lab","fr:Institut|en:Institute",2023-06-09,"de0f2a9b-a198-48a4-8074-db5120187a16,ROLE_READER","2023","https://related.project","Original research","files/code/"
"Dataset Repository",published,"Research data collection","data;research;analysis",en,"Doe, Jane;Wilson, Sarah","Data Team","University",2023-05-15,"","2023-01/2023-12","","Survey data","files/data/|files/results/"
"Documentation",pending,"Project documentation","documentation;reports",en,"Project Team","","Research Institute",2023-06-01,"","","","","files/documents/"
```

## 🚨 Common Format Issues

### **Issue: Malformed Multilingual Syntax**
```csv
# ❌ Incorrect
title
"french text - english text"

# ✅ Correct  
title
"fr:french text|en:english text"
```

### **Issue: Invalid Status Values**
```csv
# ❌ Incorrect
status
draft
active

# ✅ Correct
status
pending
published
```

### **Issue: Missing Required Fields**
```csv
# ❌ Missing title
,published,,,,"files/code/"

# ✅ Complete
"Code Collection",published,,,,"files/code/"
```

### **Issue: Incorrect Rights Format**
```csv
# ❌ Incorrect
rights
"READER:group_id"

# ✅ Correct
rights
"group_id,ROLE_READER"
```

## 🔗 Related Resources

- **[Field Transformations](./field-transformations.md)** - How CSV fields map to JSON
- **[Examples](./examples/)** - Working CSV examples
- **[Validation Tools](./validation/)** - CSV validation utilities
- **[Dublin Core Specification](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)** - Metadata standards

---

**Specification Version**: 1.0  
**Last Updated**: 2025-06-09  
**NAKALA API Compatibility**: v2024