# Endpoint and Field Improvement Plan

## 🎯 Objective

Ensure every NAKALA API endpoint and every metadata field is **well-handled, documented, and demonstrated** in O-Nakala Core, addressing the insufficient official documentation in `/api/`.

## 📋 Current State Analysis

### **Official API Documentation Gaps**
- `/api/guide_description.md` - Basic overview, lacks transformation details
- `/api/nakala-apitest.json` - Raw OpenAPI spec, not user-friendly
- `/api/nakala_metadata_vocabulary.json` - Vocabulary list without usage examples
- `/api/api_keys.md` - Simple key information

### **Missing Critical Documentation**
1. **Field-by-field transformation rules** for each endpoint
2. **Complete CSV format specifications** with validation
3. **Error handling and troubleshooting** for transformation issues
4. **Working examples** for every supported field combination
5. **Interactive validation tools** for CSV format checking

## 🚀 Systematic Improvement Strategy

### **Phase 1: Endpoint Documentation (Priority: High)**

#### **1.1 Upload Endpoint** (`/datas` - POST)
**Target**: `docs/endpoints/upload-endpoint.md`

**Coverage Required**:
- CSV format specifications for folder mode vs file mode
- Field transformation rules for each metadata field
- Multilingual format examples and validation
- File organization patterns and requirements
- Error scenarios and troubleshooting
- Complete working examples

**Implementation**:
```
docs/endpoints/upload-endpoint/
├── README.md                    # Overview and quick start
├── csv-format-specification.md # Complete CSV format rules
├── field-transformations.md    # Field-by-field transformation
├── examples/                   # Working examples
│   ├── basic-upload.csv
│   ├── multilingual-upload.csv
│   ├── complex-metadata.csv
│   └── error-examples.csv
└── troubleshooting.md          # Common issues and solutions
```

#### **1.2 Collection Endpoint** (`/collections` - POST)
**Target**: `docs/endpoints/collection-endpoint.md`

**Coverage Required**:
- Collection metadata structure and requirements
- Relationship mapping between datasets and collections
- Collection organization patterns
- Rights and access control configuration
- Thematic grouping strategies

#### **1.3 Curator Endpoint** (Batch Operations)
**Target**: `docs/endpoints/curator-endpoint.md`

**Coverage Required**:
- Batch modification CSV formats (creation vs modification modes)
- Quality analysis and reporting features
- Metadata enhancement strategies
- ML-powered curation capabilities
- Advanced batch processing patterns

### **Phase 2: Field Documentation (Priority: High)**

#### **2.1 Core Dublin Core Fields**
**Target**: `docs/fields/dublin-core/`

Fields to document:
- `title` - Multilingual support, required for all resources
- `description` - Long-form descriptions, HTML support
- `creator` - Author/creator information, person vs organization
- `contributor` - Additional contributors, institutional affiliations
- `publisher` - Publishing organization information
- `date` - Date formats and validation rules
- `type` - COAR resource types, URI validation
- `language` - ISO language codes, multilingual resource handling
- `identifier` - External identifiers, DOI integration
- `rights` - License and access rights, complex permissions
- `relation` - Resource relationships, linking strategies
- `source` - Source information and provenance
- `coverage` - Spatial and temporal coverage

#### **2.2 NAKALA-Specific Fields**
**Target**: `docs/fields/nakala-specific/`

Fields to document:
- `keywords`/`subject` - Keyword arrays, vocabulary integration
- `alternative` - Alternative titles and names
- `temporal` - Temporal coverage specific formats
- `spatial` - Geographic coverage and coordinates
- `accessRights` - Access control and embargo settings

#### **2.3 Field Documentation Template**
Each field documented with:
```markdown
# Field Name: [field]

## Overview
- **Property URI**: http://example.com/terms#field
- **Required**: Yes/No
- **Multilingual**: Yes/No
- **Array Support**: Yes/No
- **Data Type**: String/URI/Date

## CSV Format
### Simple Format
```csv
field
"Simple value"
```

### Multilingual Format
```csv
field
"fr:Valeur française|en:English value"
```

### Array Format (if applicable)
```csv
field
"value1;value2;value3"
```

## JSON Transformation
### Input CSV
### Output JSON
### Transformation Logic

## Validation Rules
- Format requirements
- Vocabulary constraints
- Length limits
- Special characters

## Common Errors
- Error message examples
- Troubleshooting steps
- Fix recommendations

## Examples
- Basic examples
- Complex examples
- Edge cases
```

### **Phase 3: Interactive Tools (Priority: Medium)**

#### **3.1 CSV Validation Tools**
**Target**: `tools/csv-validator/`

Features:
- Field format validation
- Multilingual syntax checking
- Array format verification
- NAKALA API compatibility testing
- Error reporting with suggestions

#### **3.2 JSON Preview Tools**
**Target**: `tools/json-preview/`

Features:
- CSV to JSON transformation preview
- Metadata structure visualization
- Field mapping demonstration
- API payload preview

#### **3.3 Interactive Examples**
**Target**: `examples/interactive/`

Features:
- Web-based CSV builder
- Step-by-step transformation demos
- Field-by-field examples
- Error scenario simulations

## 📊 Implementation Roadmap

### **Week 1: Upload Endpoint Documentation**
- [ ] Complete upload endpoint analysis
- [ ] Document all CSV format variations
- [ ] Create comprehensive examples
- [ ] Test all examples with real API

### **Week 2: Collection Endpoint Documentation**
- [ ] Collection metadata structure analysis
- [ ] Relationship mapping documentation
- [ ] Collection organization examples
- [ ] Rights configuration guide

### **Week 3: Curator Endpoint Documentation**
- [ ] Batch modification format analysis
- [ ] Quality analysis feature documentation
- [ ] ML curation capabilities overview
- [ ] Advanced processing examples

### **Week 4: Core Field Documentation**
- [ ] Dublin Core fields (13 fields)
- [ ] NAKALA-specific fields (5 fields)
- [ ] Field validation rules
- [ ] Transformation examples per field

### **Week 5: Advanced Field Documentation**
- [ ] Complex field combinations
- [ ] Edge case handling
- [ ] Error scenarios and solutions
- [ ] Best practices documentation

### **Week 6: Interactive Tools Development**
- [ ] CSV validation tool
- [ ] JSON preview functionality
- [ ] Interactive examples
- [ ] Web-based demonstrations

## 🎯 Success Metrics

### **Documentation Quality**
- [ ] Every endpoint has comprehensive documentation
- [ ] Every field has complete transformation rules
- [ ] All examples tested with real API
- [ ] Zero ambiguity in format specifications

### **User Experience**
- [ ] Clear error messages for all validation failures
- [ ] Step-by-step guidance for complex formats
- [ ] Interactive tools for format validation
- [ ] Comprehensive troubleshooting guides

### **Developer Experience**
- [ ] Complete API reference beyond official docs
- [ ] Field-by-field implementation guides
- [ ] Transformation logic documentation
- [ ] Extension and customization guidance

## 📁 New Documentation Structure

```
docs/
├── endpoints/                          # Endpoint-specific documentation
│   ├── upload-endpoint/
│   │   ├── README.md
│   │   ├── csv-format-specification.md
│   │   ├── field-transformations.md
│   │   ├── examples/
│   │   └── troubleshooting.md
│   ├── collection-endpoint/
│   │   ├── README.md
│   │   ├── metadata-structure.md
│   │   ├── relationship-mapping.md
│   │   ├── examples/
│   │   └── troubleshooting.md
│   └── curator-endpoint/
│       ├── README.md
│       ├── batch-operations.md
│       ├── quality-analysis.md
│       ├── examples/
│       └── troubleshooting.md
├── fields/                             # Field-by-field documentation
│   ├── dublin-core/
│   │   ├── title.md
│   │   ├── description.md
│   │   ├── creator.md
│   │   └── ...
│   ├── nakala-specific/
│   │   ├── keywords.md
│   │   ├── temporal.md
│   │   └── ...
│   └── field-reference-complete.md
├── transformations/                    # Transformation documentation
│   ├── csv-to-json-guide.md
│   ├── multilingual-formats.md
│   ├── array-processing.md
│   └── validation-rules.md
└── tools/                             # Tool documentation
    ├── csv-validator.md
    ├── json-preview.md
    └── interactive-examples.md
```

## 🔧 Implementation Priority

### **Immediate (Week 1)**
1. **Upload endpoint documentation** - Most commonly used
2. **Core field documentation** - title, description, creator, keywords
3. **Basic CSV format specification** - Foundation for all endpoints

### **Short-term (Weeks 2-3)**
1. **Collection endpoint documentation** - Second most important
2. **Curator endpoint documentation** - Advanced features
3. **Complete field coverage** - All Dublin Core and NAKALA fields

### **Medium-term (Weeks 4-6)**
1. **Interactive validation tools** - Improve user experience
2. **Comprehensive error handling** - Better troubleshooting
3. **Advanced examples** - Complex use cases and edge cases

---

**Goal**: Transform O-Nakala Core from a functional system to a **comprehensively documented, user-friendly, and developer-ready** platform that surpasses the official NAKALA documentation in clarity and completeness.