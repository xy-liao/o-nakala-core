# Curator CSV Format Specification

## 🎯 Overview

This specification defines the **complete CSV format** for Curator endpoint batch modification operations. The Curator uses a specialized CSV format with `new_` prefixed fields to modify existing NAKALA resources while preserving unmodified metadata.

## 📋 Required CSV Structure

### **Column Header Format**
```csv
id,action,new_title,new_description,new_keywords,new_creator,new_contributor,new_rights,new_status
```

### **Encoding Requirements**
- **Character Encoding**: UTF-8 (required for multilingual content)
- **Delimiter**: Comma (`,`)
- **Quote Character**: Double quote (`"`) for fields containing commas or multilingual syntax
- **Line Endings**: Unix LF (`\n`) or Windows CRLF (`\r\n`)

## 🔧 Field Specifications

### **Required Fields**

#### **`id`** *(Required)*
**Purpose**: NAKALA resource identifier for modification target
**Format**: NAKALA identifier format
**Validation**: 
- ✅ Must be valid NAKALA identifier: `10.34847/nkl.xxxxxxxx` or `11280/xxxxxxxx`
- ✅ Resource must exist and be accessible
- ❌ Cannot be empty or invalid format

**Examples**:
```csv
id
10.34847/nkl.abc12345
11280/def67890
10.34847/nkl.ghi09876.v2
```

#### **`action`** *(Required)*
**Purpose**: Specifies the operation type for curator processing
**Format**: Controlled vocabulary  
**Validation**:
- ✅ Must be exactly: `modify`
- ❌ No other values currently supported
- ❌ Case sensitive

**Examples**:
```csv
action
modify
```

### **Modification Fields (new_* prefix)**

All modification fields use the `new_` prefix to distinguish them from current values. Only fields with non-empty values in the CSV will be modified on the target resource.

#### **`new_title`** *(Optional)*
**Purpose**: Update resource title
**Format**: Text string or multilingual format
**Property URI**: `http://nakala.fr/terms#title`
**Validation**:
- ✅ Supports multilingual syntax: `"lang:text|lang:text"`
- ✅ Empty allowed (no modification)
- ✅ Will replace existing title completely

**Examples**:
```csv
new_title
"Updated Research Dataset"
"fr:Données de recherche mises à jour|en:Updated Research Dataset"
""
```

#### **`new_description`** *(Optional)*
**Purpose**: Update resource description  
**Format**: Text string or multilingual format
**Property URI**: `http://purl.org/dc/terms/description`
**Validation**:
- ✅ Supports multilingual syntax
- ✅ Empty allowed (no modification)
- ✅ No length restrictions

**Examples**:
```csv
new_description
"Enhanced description with additional context"
"fr:Description améliorée|en:Enhanced description"
""
```

#### **`new_keywords`** *(Optional)*
**Purpose**: Update subject keywords
**Format**: Semicolon-separated terms (can be multilingual)
**Property URI**: `http://purl.org/dc/terms/subject`
**Validation**:
- ✅ Semicolon-separated terms: `"term1;term2;term3"`
- ✅ Supports multilingual terms: `"fr:terme1;terme2|en:term1;term2"`
- ✅ Empty allowed (no modification)
- ✅ Replaces all existing keywords

**Examples**:
```csv
new_keywords
"research;data;analysis;updated"
"fr:recherche;données;analyse|en:research;data;analysis"
""
```

#### **`new_creator`** *(Optional)*
**Purpose**: Update resource creator(s)
**Format**: Semicolon-separated person names
**Property URI**: `http://nakala.fr/terms#creator`
**Processing**: `semicolon_split` format
**Validation**:
- ✅ Format: "Surname, Givenname" preferred
- ✅ Multiple creators: `"Creator1;Creator2;Creator3"`
- ✅ Simple names allowed if comma format not possible
- ✅ Empty allowed (no modification)

**Examples**:
```csv
new_creator
"Smith, John"
"Smith, John;Doe, Jane;Wilson, Sarah"
"Research Team Alpha"
""
```

#### **`new_contributor`** *(Optional)*
**Purpose**: Update additional contributors
**Format**: Semicolon-separated names (supports multilingual)
**Property URI**: `http://purl.org/dc/terms/contributor`
**Processing**: `array` format
**Validation**:
- ✅ Institutional names allowed
- ✅ Supports multilingual format
- ✅ Multiple contributors separated by semicolon

**Examples**:
```csv
new_contributor
"University Research Lab"
"fr:CNRS;Université de Paris|en:CNRS;University of Paris"
"Data Team;Statistics Department"
""
```

#### **`new_rights`** *(Optional)*
**Purpose**: Update access rights configuration
**Format**: `group_id,ROLE_NAME` format
**Processing**: `rights_list` format
**Validation**:
- ✅ Format: "group_id,ROLE_NAME"
- ✅ Multiple rights: `"group1,ROLE_READER;group2,ROLE_EDITOR"`
- ✅ Valid roles: OWNER, ADMIN, EDITOR, READER
- ✅ Empty allowed (no modification)

**Examples**:
```csv
new_rights
"de0f2a9b-a198-48a4-8074-db5120187a16,ROLE_READER"
"group1,ROLE_EDITOR;group2,ROLE_READER"
""
```

#### **`new_status`** *(Optional)*
**Purpose**: Update publication status
**Format**: Controlled vocabulary
**Property URI**: `http://nakala.fr/terms#status`
**Validation**:
- ✅ Valid values: `published`, `pending`, `private`
- ✅ Empty allowed (no modification)
- ❌ Case sensitive

**Examples**:
```csv
new_status
published
pending
private
""
```

#### **`new_language`** *(Optional)*
**Purpose**: Update primary language
**Format**: ISO 639-1/639-2 language code
**Property URI**: `http://purl.org/dc/terms/language`
**Validation**:
- ✅ 2-3 character language codes
- ✅ Examples: `fr`, `en`, `de`, `spa`

**Examples**:
```csv
new_language
fr
en
multilingual
""
```

### **Extended Dublin Core Fields**

#### **`new_publisher`** *(Optional)*
**Purpose**: Update publisher information
**Property URI**: `http://purl.org/dc/terms/publisher`
**Format**: Text string (supports multilingual)

#### **`new_coverage`** *(Optional)*  
**Purpose**: Update temporal or spatial coverage
**Property URI**: `http://purl.org/dc/terms/coverage`
**Format**: Text description (supports multilingual)

#### **`new_relation`** *(Optional)*
**Purpose**: Update related resources
**Property URI**: `http://purl.org/dc/terms/relation`
**Format**: URLs or identifiers (supports multilingual descriptions)

#### **`new_source`** *(Optional)*
**Purpose**: Update source information
**Property URI**: `http://purl.org/dc/terms/source`
**Format**: Text description or URLs (supports multilingual)

#### **`new_alternative`** *(Optional)*
**Purpose**: Update alternative titles
**Property URI**: `http://purl.org/dc/terms/alternative`
**Format**: Text string (supports multilingual)

#### **`new_format`** *(Optional)*
**Purpose**: Update format information
**Property URI**: `http://purl.org/dc/terms/format`
**Format**: MIME type or format description

#### **`new_identifier`** *(Optional)*
**Purpose**: Update additional identifiers
**Property URI**: `http://purl.org/dc/terms/identifier`
**Format**: Identifier strings

## 🌐 Multilingual Format Specification

### **Syntax**: `"lang:text|lang:text"`

#### **Single Language Update**
```csv
new_title
"Updated Title"
```

#### **Multilingual Update**
```csv
new_title
"fr:Titre mis à jour|en:Updated Title"
```

#### **Complex Multilingual with Keywords**
```csv
new_keywords
"fr:recherche;données;mise à jour|en:research;data;update"
```

### **Language Processing Logic**
1. **Parse existing**: Read current multilingual metadata
2. **Parse new**: Extract language-specific updates from CSV
3. **Merge**: Replace specified languages, preserve others
4. **Generate**: Create updated metadata entries

## 📊 Validation Rules

### **Structural Validation**
- ✅ **Required columns**: `id` and `action` must be present
- ✅ **Column order**: Flexible (any order acceptable)
- ✅ **Modification fields**: At least one `new_*` field should have content
- ✅ **Empty rows**: Skipped automatically

### **Content Validation**
- ✅ **Valid identifiers**: NAKALA ID format compliance
- ✅ **Valid action**: Must be `modify`
- ✅ **Resource existence**: Target resources must be accessible
- ✅ **Multilingual syntax**: Proper lang:text|lang:text format

### **Permission Validation**
- ✅ **Modification rights**: User must have edit permissions on target resources
- ✅ **Rights format**: Access rights must follow group_id,ROLE format
- ✅ **Status transitions**: Status changes must be valid

## 🎯 Complete Example

```csv
id,action,new_title,new_description,new_keywords,new_creator,new_contributor,new_rights,new_status,new_language
10.34847/nkl.abc12345,modify,"fr:Données de recherche améliorées|en:Enhanced Research Data","fr:Description mise à jour avec contexte|en:Updated description with context","fr:recherche;données;amélioré|en:research;data;enhanced","Smith, John;Doe, Jane","fr:Laboratoire de recherche|en:Research Laboratory","de0f2a9b-a198-48a4-8074-db5120187a16,ROLE_READER",published,fr
10.34847/nkl.def67890,modify,"Updated Dataset Title","Enhanced description for better discoverability","data;analysis;improved","Wilson, Sarah","Data Analysis Team","","pending",en
11280/ghi09876,modify,"","New description only","","","","group123,ROLE_EDITOR","",""
```

## 🚨 Common Format Issues

### **Issue: Invalid Identifier Format**
```csv
# ❌ Incorrect
id
abc123
nakala.123

# ✅ Correct
id
10.34847/nkl.abc12345
11280/def67890
```

### **Issue: Invalid Action Value**
```csv
# ❌ Incorrect
action
update
edit

# ✅ Correct
action
modify
```

### **Issue: Malformed Multilingual Syntax**
```csv
# ❌ Incorrect
new_title
"french text - english text"

# ✅ Correct
new_title
"fr:french text|en:english text"
```

### **Issue: Incorrect Rights Format**
```csv
# ❌ Incorrect
new_rights
"READER:group_id"
"group_id=READER"

# ✅ Correct
new_rights
"group_id,ROLE_READER"
```

### **Issue: No Modification Fields**
```csv
# ❌ Incorrect - no modifications specified
id,action
10.34847/nkl.abc123,modify

# ✅ Correct - at least one modification field
id,action,new_title
10.34847/nkl.abc123,modify,"Updated Title"
```

## 🔄 Processing Behavior

### **Selective Modification**
- **Empty fields**: Ignored (no modification applied)
- **Non-empty fields**: Replace existing metadata completely
- **Missing fields**: Current metadata preserved unchanged

### **Multilingual Merging**
- **Specified languages**: Updated with new values
- **Unspecified languages**: Preserved from existing metadata
- **Language removal**: Not supported (use empty language code)

### **Array Field Handling**
- **Keywords**: Replaced entirely (not merged)
- **Creators**: Replaced entirely with new list
- **Contributors**: Replaced entirely with new list

## 🔗 Related Resources

- **[Field Transformations](./field-transformations.md)** - How CSV fields map to JSON
- **[Examples](../../../examples/sample_dataset/)** - Working curator CSV examples
- **[Validation Tools](./validation/)** - CSV validation utilities
- **[Curator Code Reference](../../src/o_nakala_core/curator.py)** - Implementation details

---

**Specification Version**: 1.0  
**Last Updated**: 2025-06-09  
**NAKALA API Compatibility**: v2024  
**Field Mapping Reference**: 280+ mappings in `CSV_FIELD_MAPPINGS`