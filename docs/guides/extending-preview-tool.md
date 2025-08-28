# Extending the O-Nakala Core Preview Tool

**Version**: 2.5.0  
**Target Audience**: Intermediate developers and researchers  
**Goal**: Extend the preview tool with custom fields, COAR types, and templates

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites and Setup](#prerequisites-and-setup)
3. [Understanding Current Limitations](#understanding-current-limitations)
4. [Method 1: Custom Field Mapping (Simple)](#method-1-custom-field-mapping-simple)
5. [Method 2: Custom COAR Resource Types](#method-2-custom-coar-resource-types)
6. [Method 3: Custom Templates (Advanced)](#method-3-custom-templates-advanced)
7. [Complete Integration Example](#complete-integration-example)
8. [Troubleshooting Common Issues](#troubleshooting-common-issues)
9. [Best Practices and Recommendations](#best-practices-and-recommendations)
10. [Advanced Customization Techniques](#advanced-customization-techniques)

---

## Introduction

The O-Nakala Core preview tool (`o-nakala-preview`) is designed to validate CSV metadata files and generate JSON previews for NAKALA uploads. While the tool comes with predefined configurations, researchers often need to extend it with:

- **Custom metadata fields** beyond the standard Dublin Core and NAKALA properties
- **Specialized COAR resource types** not in the default 5-type suggestion list
- **Institutional templates** tailored to specific research domains
- **Custom validation rules** for domain-specific requirements

This guide shows you how to extend the preview tool systematically while maintaining compatibility with the NAKALA API.

### What Can Be Extended

The preview tool has three main extension points:

1. **Field Mappings**: Map custom CSV fields to any property URI
2. **COAR Types**: Use any valid COAR resource type URI (not limited to suggestions)
3. **Templates**: Create domain-specific CSV templates with custom fields

### Current Tool Capabilities

- ✅ **Validates CSV structure** and field values
- ✅ **Generates NAKALA JSON** preview with exact API payload format
- ✅ **Supports multilingual metadata** (`fr:|en:` format)
- ✅ **Pattern-based enhancement suggestions** (v2.5.0 feature)
- ✅ **Interactive assistance mode** with COAR suggestions
- ✅ **Extensible field mapping** system

---

## Prerequisites and Setup

### Required Installation

```bash
# Install O-Nakala Core v2.5.0+
pip install o-nakala-core>=2.5.0

# Verify installation
o-nakala-preview --help
```

### Environment Setup

```bash
# Set up NAKALA test environment (optional, for full workflow testing)
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"  # Test key
export NAKALA_API_URL="https://apitest.nakala.fr"
```

### Required Knowledge

- **Basic Python**: For writing custom field mappings and templates
- **CSV format**: Understanding of CSV structure and metadata organization
- **NAKALA concepts**: Familiarity with NAKALA metadata structure and COAR types
- **JSON/URI concepts**: Basic understanding of property URIs and JSON structure

### Development Environment

```bash
# Create development directory
mkdir nakala-custom-extensions
cd nakala-custom-extensions

# Copy existing examples as starting point
cp /path/to/o-nakala-core/docs/examples/custom-field-mapping.py ./
cp /path/to/o-nakala-core/docs/examples/institutional-workflow.py ./
```

---

## Understanding Current Limitations

### 1. Hardcoded COAR Type Suggestions (5 types)

The preview tool shows only 5 COAR types in interactive suggestions:

```python
# Current suggestions in ResearcherAssistant.suggest_coar_types()
suggestions = [
    {"uri": "http://purl.org/coar/resource_type/c_ddb1", "label": "Dataset"},
    {"uri": "http://purl.org/coar/resource_type/c_5ce6", "label": "Software"}, 
    {"uri": "http://purl.org/coar/resource_type/c_18cf", "label": "Text"},
    {"uri": "http://purl.org/coar/resource_type/c_c513", "label": "Image"},
    {"uri": "http://purl.org/coar/resource_type/c_8544", "label": "Lecture"}
]
```

**✅ SOLUTION**: Any valid COAR URI works in the `type` field - suggestions are just UI convenience.

### 2. Limited Property URI Mapping (63 fields)

The `NakalaCommonUtils.PROPERTY_URIS` dictionary contains 63 standard fields:

```python
PROPERTY_URIS = {
    "title": "http://nakala.fr/terms#title",
    "creator": "http://nakala.fr/terms#creator",
    # ... 61 more standard fields
}
```

**✅ SOLUTION**: Custom field mapping allows any property URI.

### 3. Template Limitations (3 types)

Interactive mode provides only 3 template types:

- `research_paper`
- `dataset` 
- `code`

**✅ SOLUTION**: Create custom template generation functions.

---

## Method 1: Custom Field Mapping (Simple)

This is the **recommended approach** for most researchers. It allows you to use any CSV field name and map it to any property URI.

### Step 1: Create Custom Field Mapping

Create a file `custom_mapping.py`:

```python
#!/usr/bin/env python3
"""
Custom Field Mapping for Research Project
Extends O-Nakala preview tool with domain-specific fields.
"""

from o_nakala_core.common.utils import NakalaCommonUtils

def get_anthropology_field_mapping():
    """Custom field mapping for anthropological research."""
    
    # Start with standard mappings
    base_mapping = {
        "title": "http://nakala.fr/terms#title",
        "creator": "http://nakala.fr/terms#creator",
        "type": "http://nakala.fr/terms#type",
        "description": "http://purl.org/dc/terms/description",
        "keywords": "http://purl.org/dc/terms/subject",
        "license": "http://nakala.fr/terms#license",
        "date": "http://nakala.fr/terms#created",
        "language": "http://purl.org/dc/terms/language",
    }
    
    # Add custom anthropology fields
    anthropology_fields = {
        # Research methodology fields
        "fieldwork_location": "http://anthro.org/fieldwork#location",
        "fieldwork_dates": "http://anthro.org/fieldwork#dates",
        "research_method": "http://anthro.org/methodology#method",
        "data_collection_technique": "http://anthro.org/methodology#technique",
        "participant_count": "http://anthro.org/study#participant_count",
        
        # Ethical and legal fields
        "ethics_approval": "http://ethics.org/approval#number",
        "consent_type": "http://ethics.org/consent#type", 
        "anonymization_level": "http://ethics.org/privacy#anonymization",
        
        # Cultural context fields
        "cultural_group": "http://anthro.org/context#group",
        "geographical_region": "http://purl.org/dc/terms/spatial",  # Reuse DC
        "historical_period": "http://purl.org/dc/terms/temporal",   # Reuse DC
        "language_group": "http://anthro.org/linguistics#group",
        
        # Administrative fields
        "funding_source": "http://research.org/funding#source",
        "project_code": "http://research.org/project#code",
        "institutional_affiliation": "http://research.org/affiliation#institution",
        "research_permit": "http://research.org/legal#permit_number",
    }
    
    # Merge mappings
    return {**base_mapping, **anthropology_fields}

def process_anthropology_csv(csv_file):
    """Process CSV with anthropology-specific field mapping."""
    
    # Get custom mapping
    custom_mapping = get_anthropology_field_mapping()
    
    # Process CSV data
    import csv
    utils = NakalaCommonUtils()
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader, 1):
            print(f"\n--- Entry {i} ---")
            
            # Generate metadata with custom mapping
            metadata = utils.prepare_nakala_metadata(row, custom_mapping)
            
            # Show results
            print(f"Original CSV fields: {list(row.keys())}")
            print(f"Generated metadata entries: {len(metadata)}")
            
            # Show custom fields processed
            custom_fields = [field for field in row.keys() 
                           if field in custom_mapping and row[field]]
            print(f"Custom fields processed: {custom_fields}")
            
            # Show sample metadata
            for meta in metadata[:3]:  # First 3 entries
                prop_uri = meta.get("propertyUri", "")
                value = meta.get("value", "")
                lang = meta.get("lang", "")
                
                # Identify custom vs standard
                if "anthro.org" in prop_uri or "ethics.org" in prop_uri:
                    category = "🔬 CUSTOM"
                elif "nakala.fr" in prop_uri:
                    category = "🏛️ NAKALA"
                elif "purl.org/dc" in prop_uri:
                    category = "📚 DUBLIN CORE"
                else:
                    category = "🔧 OTHER"
                
                lang_info = f" [{lang}]" if lang and lang != "und" else ""
                print(f"  {category}: {value}{lang_info}")

if __name__ == "__main__":
    # Example usage
    print("🧑‍🔬 Anthropology Field Mapping Demo")
    print("=" * 50)
    
    # Show available custom fields
    mapping = get_anthropology_field_mapping()
    custom_fields = [k for k, v in mapping.items() 
                    if "anthro.org" in v or "ethics.org" in v or "research.org" in v]
    
    print(f"\n📋 Available custom fields ({len(custom_fields)}):")
    for field in sorted(custom_fields):
        print(f"  • {field}: {mapping[field]}")
    
    print(f"\n💡 Usage:")
    print(f"  1. Add these fields to your CSV")
    print(f"  2. Use multilingual format: 'fr:French text|en:English text'")
    print(f"  3. Process with: process_anthropology_csv('your_file.csv')")
```

### Step 2: Create Custom CSV Template

Create `anthropology_template.csv`:

```csv
file,title,creator,type,description,keywords,license,fieldwork_location,research_method,ethics_approval,cultural_group,funding_source
data/interviews.csv,"fr:Entretiens ethnographiques|en:Ethnographic interviews","Researcher,Senior;Assistant,Research",http://purl.org/coar/resource_type/c_ddb1,"fr:Données d'entretiens collectées lors du terrain|en:Interview data collected during fieldwork","fr:ethnographie;entretiens;terrain|en:ethnography;interviews;fieldwork",CC-BY-4.0,"fr:Village de Montagne, Alpes|en:Mountain Village, Alps","fr:Entretiens semi-structurés|en:Semi-structured interviews",IRB-2024-ANTHRO-001,"fr:Communauté alpine|en:Alpine community","ANR-2024-ANTHRO-MOUNTAIN"
```

### Step 3: Process with Custom Mapping

```python
# Use your custom mapping
from custom_mapping import process_anthropology_csv
process_anthropology_csv("anthropology_template.csv")
```

### Step 4: Integrate with Preview Tool

```python
#!/usr/bin/env python3
"""
Enhanced preview with custom field mapping integration.
"""

import sys
import subprocess
from pathlib import Path
from custom_mapping import get_anthropology_field_mapping

def preview_with_custom_fields(csv_file):
    """Run preview tool, then show custom field analysis."""
    
    # Run standard preview tool
    print("🔍 Running standard preview...")
    result = subprocess.run([
        sys.executable, "-m", "o_nakala_core.cli.preview",
        "--csv", csv_file,
        "--enhance",
        "--json-output", f"{csv_file.replace('.csv', '_preview.json')}"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    # Add custom field analysis
    print("\n" + "="*60)
    print("🔬 CUSTOM FIELD ANALYSIS")
    print("="*60)
    
    custom_mapping = get_anthropology_field_mapping()
    
    import csv
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_fields = reader.fieldnames or []
    
    # Categorize fields
    standard_fields = ["title", "creator", "type", "description", "keywords", "license", "date", "language"]
    custom_fields = [f for f in all_fields if f not in standard_fields and f != "file"]
    recognized_custom = [f for f in custom_fields if f in custom_mapping]
    unrecognized = [f for f in custom_fields if f not in custom_mapping]
    
    print(f"📊 Field Analysis:")
    print(f"   • Total fields: {len(all_fields)}")
    print(f"   • Standard fields: {len(standard_fields)} ✅")
    print(f"   • Custom fields: {len(custom_fields)}")
    print(f"     - Recognized: {len(recognized_custom)} ✅")
    print(f"     - Unrecognized: {len(unrecognized)} ⚠️")
    
    if recognized_custom:
        print(f"\n🔬 Recognized custom fields:")
        for field in recognized_custom:
            print(f"   • {field} → {custom_mapping[field]}")
    
    if unrecognized:
        print(f"\n⚠️ Unrecognized fields (will be ignored):")
        for field in unrecognized:
            print(f"   • {field}")
        print(f"\n💡 Add these to your custom mapping to process them.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python enhanced_preview.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    preview_with_custom_fields(csv_file)
```

**Usage:**

```bash
# Create and process custom CSV
python custom_mapping.py

# Run enhanced preview
python enhanced_preview.py anthropology_template.csv
```

---

## Method 2: Custom COAR Resource Types

The preview tool accepts **any valid COAR resource type URI**, not just the 5 suggested types. This section shows how to use specialized COAR types.

### Understanding COAR Resource Types

COAR (Confederation of Open Access Repositories) provides a comprehensive vocabulary of resource types. The preview tool suggestions show only 5 common types, but the full COAR vocabulary contains 100+ types.

### Step 1: Find Specialized COAR Types

```python
#!/usr/bin/env python3
"""
COAR Resource Type Explorer
Find and validate COAR types for specialized content.
"""

def get_specialized_coar_types():
    """Extended COAR type catalog for research domains."""
    
    return {
        # Text variations
        "research_article": "http://purl.org/coar/resource_type/c_2df8fbb1",
        "review_article": "http://purl.org/coar/resource_type/c_dcae04bc", 
        "book_chapter": "http://purl.org/coar/resource_type/c_3248",
        "thesis": "http://purl.org/coar/resource_type/c_46ec",
        "technical_report": "http://purl.org/coar/resource_type/c_18gh",
        "working_paper": "http://purl.org/coar/resource_type/c_8042",
        "conference_paper": "http://purl.org/coar/resource_type/c_5794",
        
        # Data variations
        "research_data": "http://purl.org/coar/resource_type/c_ddb1",  # Standard dataset
        "survey_data": "http://purl.org/coar/resource_type/c_ddb1",
        "interview_data": "http://purl.org/coar/resource_type/c_ddb1",
        "experimental_data": "http://purl.org/coar/resource_type/c_ddb1",
        
        # Media variations
        "moving_image": "http://purl.org/coar/resource_type/c_8a7e",
        "sound": "http://purl.org/coar/resource_type/c_18cc",
        "still_image": "http://purl.org/coar/resource_type/c_ecc8",
        
        # Interactive resources
        "interactive_resource": "http://purl.org/coar/resource_type/c_e9a0",
        "website": "http://purl.org/coar/resource_type/c_7ad9",
        
        # Learning objects
        "learning_object": "http://purl.org/coar/resource_type/c_e059",
        "lecture": "http://purl.org/coar/resource_type/c_8544",
        
        # Special formats
        "cartographic_material": "http://purl.org/coar/resource_type/c_12cc",
        "musical_notation": "http://purl.org/coar/resource_type/c_18cw",
    }

def validate_coar_uri(uri):
    """Validate COAR URI format."""
    import re
    pattern = r'^http://purl\.org/coar/resource_type/c_[a-z0-9]+$'
    return bool(re.match(pattern, uri))

def suggest_coar_type(content_description):
    """Suggest COAR types based on content description."""
    
    coar_types = get_specialized_coar_types()
    description_lower = content_description.lower()
    
    suggestions = []
    
    # Keyword-based suggestions
    keyword_mapping = {
        "research_article": ["article", "research", "paper", "publication"],
        "thesis": ["thesis", "dissertation", "phd", "master"],
        "survey_data": ["survey", "questionnaire", "poll"],
        "interview_data": ["interview", "conversation", "oral"],
        "conference_paper": ["conference", "proceedings", "presentation"],
        "technical_report": ["report", "technical", "documentation"],
        "moving_image": ["video", "film", "movie", "recording"],
        "sound": ["audio", "music", "sound", "recording"],
        "still_image": ["image", "photo", "picture", "photograph"],
        "cartographic_material": ["map", "geographic", "spatial", "gis"],
    }
    
    for type_name, keywords in keyword_mapping.items():
        if any(keyword in description_lower for keyword in keywords):
            if type_name in coar_types:
                suggestions.append({
                    "name": type_name,
                    "uri": coar_types[type_name],
                    "keywords": keywords
                })
    
    return suggestions[:5]  # Top 5 suggestions

def create_coar_csv_examples():
    """Create CSV examples with specialized COAR types."""
    
    examples = [
        {
            "file": "thesis/phd_dissertation.pdf",
            "title": "fr:Intelligence artificielle en anthropologie|en:AI in Anthropology",
            "creator": "Doctoral,Student", 
            "type": "http://purl.org/coar/resource_type/c_46ec",  # Thesis
            "description": "fr:Dissertation doctorale|en:PhD dissertation",
        },
        {
            "file": "conference/presentation.pdf", 
            "title": "fr:Présentation de conférence|en:Conference presentation",
            "creator": "Professor,Senior",
            "type": "http://purl.org/coar/resource_type/c_5794",  # Conference paper
            "description": "fr:Communication en conférence|en:Conference communication",
        },
        {
            "file": "maps/field_sites.geojson",
            "title": "fr:Cartes des sites de terrain|en:Field site maps", 
            "creator": "Cartographer,Geographic",
            "type": "http://purl.org/coar/resource_type/c_12cc",  # Cartographic material
            "description": "fr:Données cartographiques GIS|en:GIS cartographic data",
        },
        {
            "file": "audio/interviews.mp3",
            "title": "fr:Enregistrements d'entretiens|en:Interview recordings",
            "creator": "Anthropologist,Field",
            "type": "http://purl.org/coar/resource_type/c_18cc",  # Sound
            "description": "fr:Enregistrements audio d'entretiens|en:Audio interview recordings",
        }
    ]
    
    # Create CSV
    import csv
    with open('specialized_coar_examples.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = examples[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(examples)
    
    print("✅ Created specialized_coar_examples.csv")
    return "specialized_coar_examples.csv"

if __name__ == "__main__":
    print("🏷️ COAR Resource Type Extension")
    print("=" * 50)
    
    # Show available specialized types
    coar_types = get_specialized_coar_types()
    print(f"\n📋 Available specialized COAR types ({len(coar_types)}):")
    for name, uri in list(coar_types.items())[:10]:  # Show first 10
        is_valid = validate_coar_uri(uri)
        status = "✅" if is_valid else "❌"
        print(f"  {status} {name}: {uri}")
    
    # Test content-based suggestions
    print(f"\n🎯 Content-based suggestions:")
    test_descriptions = [
        "PhD thesis on machine learning",
        "Audio recordings of interviews", 
        "Geographic maps of study sites",
        "Conference presentation slides"
    ]
    
    for desc in test_descriptions:
        suggestions = suggest_coar_type(desc)
        print(f"\n'{desc}':")
        for suggestion in suggestions:
            print(f"  → {suggestion['name']}: {suggestion['uri']}")
    
    # Create example CSV
    print(f"\n📝 Creating specialized examples...")
    csv_file = create_coar_csv_examples()
    print(f"💡 Test with: o-nakala-preview --csv {csv_file}")
```

### Step 2: Validate COAR Types

```python
#!/usr/bin/env python3
"""
COAR Type Validator for CSV files.
"""

import csv
import re
from typing import List, Dict, Any

def validate_coar_types_in_csv(csv_file: str) -> Dict[str, Any]:
    """Validate all COAR types in a CSV file."""
    
    results = {
        "valid_types": [],
        "invalid_types": [],
        "entries_analyzed": 0,
        "validation_errors": []
    }
    
    coar_pattern = r'^http://purl\.org/coar/resource_type/c_[a-z0-9]+$'
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader, 1):
                results["entries_analyzed"] += 1
                
                if 'type' not in row:
                    results["validation_errors"].append(f"Entry {i}: Missing 'type' field")
                    continue
                
                coar_uri = row['type']
                if not coar_uri:
                    results["validation_errors"].append(f"Entry {i}: Empty 'type' field")
                    continue
                
                if re.match(coar_pattern, coar_uri):
                    results["valid_types"].append({
                        "entry": i,
                        "uri": coar_uri,
                        "title": row.get('title', 'Untitled')[:50]
                    })
                else:
                    results["invalid_types"].append({
                        "entry": i,
                        "uri": coar_uri,
                        "title": row.get('title', 'Untitled')[:50],
                        "error": "Invalid COAR URI format"
                    })
    
    except Exception as e:
        results["validation_errors"].append(f"File error: {str(e)}")
    
    return results

def fix_coar_types_in_csv(csv_file: str, output_file: str = None) -> str:
    """Fix common COAR type errors in CSV file."""
    
    if output_file is None:
        output_file = csv_file.replace('.csv', '_fixed_coar.csv')
    
    # Common COAR type corrections
    corrections = {
        "dataset": "http://purl.org/coar/resource_type/c_ddb1",
        "text": "http://purl.org/coar/resource_type/c_18cf",
        "software": "http://purl.org/coar/resource_type/c_5ce6",
        "image": "http://purl.org/coar/resource_type/c_c513",
        "lecture": "http://purl.org/coar/resource_type/c_8544",
        "article": "http://purl.org/coar/resource_type/c_2df8fbb1",
        "thesis": "http://purl.org/coar/resource_type/c_46ec",
        "conference": "http://purl.org/coar/resource_type/c_5794",
    }
    
    corrections_made = 0
    
    try:
        # Read data
        rows = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            
            for row in reader:
                if 'type' in row and row['type']:
                    original_type = row['type']
                    
                    # Check if it needs correction
                    if not re.match(r'^http://purl\.org/coar/resource_type/c_[a-z0-9]+$', original_type):
                        # Try to find correction
                        type_lower = original_type.lower().strip()
                        if type_lower in corrections:
                            row['type'] = corrections[type_lower]
                            corrections_made += 1
                            print(f"Fixed: '{original_type}' → '{row['type']}'")
                
                rows.append(row)
        
        # Write corrected data
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✅ Fixed {corrections_made} COAR types")
        print(f"📁 Corrected file: {output_file}")
        
    except Exception as e:
        print(f"❌ Error fixing COAR types: {e}")
        return csv_file
    
    return output_file

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python coar_validator.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    print("🔍 COAR Type Validation")
    print("=" * 40)
    
    # Validate COAR types
    results = validate_coar_types_in_csv(csv_file)
    
    print(f"📊 Analysis Results:")
    print(f"   • Entries analyzed: {results['entries_analyzed']}")
    print(f"   • Valid COAR types: {len(results['valid_types'])}")
    print(f"   • Invalid COAR types: {len(results['invalid_types'])}")
    print(f"   • Validation errors: {len(results['validation_errors'])}")
    
    # Show invalid types
    if results['invalid_types']:
        print(f"\n❌ Invalid COAR types found:")
        for invalid in results['invalid_types']:
            print(f"   Entry {invalid['entry']}: {invalid['uri']}")
            print(f"     Title: {invalid['title']}")
        
        # Offer to fix
        if input(f"\n🔧 Fix invalid COAR types? (y/n): ").lower() == 'y':
            fixed_file = fix_coar_types_in_csv(csv_file)
            print(f"\n💡 Test corrected file with:")
            print(f"   o-nakala-preview --csv {fixed_file}")
    
    # Show validation errors
    if results['validation_errors']:
        print(f"\n⚠️ Validation errors:")
        for error in results['validation_errors']:
            print(f"   • {error}")
```

### Step 3: Integration with Preview Tool

Create a wrapper that validates COAR types before running the preview:

```python
#!/usr/bin/env python3
"""
Enhanced preview with COAR type validation and correction.
"""

import sys
import subprocess
from pathlib import Path
from coar_validator import validate_coar_types_in_csv, fix_coar_types_in_csv

def preview_with_coar_validation(csv_file):
    """Run preview with COAR type pre-validation."""
    
    print("🏷️ Step 1: COAR Type Validation")
    print("-" * 40)
    
    # Validate COAR types first
    validation_results = validate_coar_types_in_csv(csv_file)
    
    print(f"📊 COAR Validation Results:")
    print(f"   • Valid types: {len(validation_results['valid_types'])}")
    print(f"   • Invalid types: {len(validation_results['invalid_types'])}")
    
    # Fix invalid types if needed
    working_file = csv_file
    if validation_results['invalid_types']:
        print(f"\n🔧 Auto-fixing invalid COAR types...")
        working_file = fix_coar_types_in_csv(csv_file)
    
    # Run preview tool
    print(f"\n🔍 Step 2: Running Preview Tool")
    print("-" * 40)
    
    result = subprocess.run([
        sys.executable, "-m", "o_nakala_core.cli.preview", 
        "--csv", working_file,
        "--enhance",
        "--json-output", f"{working_file.replace('.csv', '_preview.json')}"
    ])
    
    if working_file != csv_file:
        print(f"\n💡 Files created:")
        print(f"   • COAR-corrected CSV: {working_file}")
        print(f"   • JSON preview: {working_file.replace('.csv', '_preview.json')}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python coar_preview.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    preview_with_coar_validation(csv_file)
```

---

## Method 3: Custom Templates (Advanced)

This method creates a comprehensive template generation system that extends the preview tool's interactive capabilities.

### Step 1: Create Template Generator

```python
#!/usr/bin/env python3
"""
Advanced Template Generator for O-Nakala Preview Tool
Extends the basic 3-template system with research domain templates.
"""

import csv
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

class CustomTemplateGenerator:
    """Advanced template generator for research domains."""
    
    def __init__(self):
        self.domain_templates = self._load_domain_templates()
    
    def _load_domain_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load comprehensive domain-specific templates."""
        
        return {
            "anthropology_fieldwork": {
                "name": "Anthropological Fieldwork Data",
                "description": "Template for anthropological field research data",
                "coar_type": "http://purl.org/coar/resource_type/c_ddb1",
                "fields": {
                    "title": "fr:Données de terrain ethnographique|en:Ethnographic fieldwork data",
                    "creator": "Anthropologist,Field;Assistant,Research",
                    "type": "http://purl.org/coar/resource_type/c_ddb1",
                    "description": "fr:Données collectées lors du travail de terrain ethnographique|en:Data collected during ethnographic fieldwork",
                    "keywords": "fr:anthropologie;ethnographie;terrain;données|en:anthropology;ethnography;fieldwork;data",
                    "license": "CC-BY-NC-4.0",
                    "language": "fr",
                    "fieldwork_location": "fr:Site de terrain|en:Field site",
                    "fieldwork_dates": "2024-03-01 to 2024-09-30", 
                    "research_method": "fr:Observation participante|en:Participant observation",
                    "ethics_approval": "IRB-2024-ANTHRO-001",
                    "cultural_group": "fr:Groupe culturel étudié|en:Cultural group studied",
                    "participant_count": "n=50",
                    "consent_type": "fr:Consentement éclairé écrit|en:Written informed consent"
                }
            },
            
            "linguistics_corpus": {
                "name": "Linguistic Corpus Data", 
                "description": "Template for linguistic corpus and language documentation",
                "coar_type": "http://purl.org/coar/resource_type/c_ddb1",
                "fields": {
                    "title": "fr:Corpus linguistique|en:Linguistic corpus",
                    "creator": "Linguist,Field;Native,Speaker", 
                    "type": "http://purl.org/coar/resource_type/c_ddb1",
                    "description": "fr:Corpus de données linguistiques pour analyse phonétique et syntaxique|en:Linguistic data corpus for phonetic and syntactic analysis",
                    "keywords": "fr:linguistique;corpus;analyse;phonétique|en:linguistics;corpus;analysis;phonetics",
                    "license": "CC-BY-SA-4.0",
                    "language_group": "fr:Famille linguistique|en:Language family",
                    "transcription_method": "fr:Transcription IPA|en:IPA transcription",
                    "audio_quality": "48kHz/24bit",
                    "speaker_demographics": "fr:Données démographiques des locuteurs|en:Speaker demographics",
                    "elicitation_method": "fr:Méthode d'élicitation|en:Elicitation method"
                }
            },
            
            "archaeological_survey": {
                "name": "Archaeological Survey Data",
                "description": "Template for archaeological survey and excavation data", 
                "coar_type": "http://purl.org/coar/resource_type/c_ddb1",
                "fields": {
                    "title": "fr:Données de prospection archéologique|en:Archaeological survey data",
                    "creator": "Archaeologist,Senior;Surveyor,Field",
                    "type": "http://purl.org/coar/resource_type/c_ddb1",
                    "description": "fr:Données de prospection et documentation de sites archéologiques|en:Survey data and documentation of archaeological sites",
                    "keywords": "fr:archéologie;prospection;sites;documentation|en:archaeology;survey;sites;documentation",
                    "license": "CC-BY-4.0",
                    "survey_method": "fr:Prospection systématique|en:Systematic survey",
                    "dating_method": "fr:Datation radiocarbone|en:Radiocarbon dating",
                    "site_coordinates": "GPS coordinates (WGS84)",
                    "excavation_permit": "PERMIT-2024-ARCH-001",
                    "stratigraphy": "fr:Description stratigraphique|en:Stratigraphic description",
                    "artifact_catalog": "fr:Catalogue des artifacts|en:Artifact catalog"
                }
            },
            
            "digital_humanities": {
                "name": "Digital Humanities Project",
                "description": "Template for digital humanities computational projects",
                "coar_type": "http://purl.org/coar/resource_type/c_5ce6", 
                "fields": {
                    "title": "fr:Projet de humanités numériques|en:Digital humanities project",
                    "creator": "Digital,Humanist;Developer,Research",
                    "type": "http://purl.org/coar/resource_type/c_5ce6",
                    "description": "fr:Projet computationnel pour l'analyse de sources historiques|en:Computational project for historical source analysis",
                    "keywords": "fr:humanités numériques;analyse;computation|en:digital humanities;analysis;computation",
                    "license": "MIT",
                    "programming_language": "Python 3.9+",
                    "dependencies": "pandas, numpy, nltk, spacy",
                    "data_format": "JSON, CSV, XML-TEI",
                    "analysis_method": "fr:Analyse de réseau textuel|en:Textual network analysis",
                    "historical_period": "fr:Période médiévale|en:Medieval period",
                    "source_corpus": "fr:Manuscrits médiévaux|en:Medieval manuscripts"
                }
            },
            
            "clinical_study": {
                "name": "Clinical Research Study",
                "description": "Template for clinical research and medical data",
                "coar_type": "http://purl.org/coar/resource_type/c_ddb1",
                "fields": {
                    "title": "fr:Étude clinique randomisée|en:Randomized clinical study", 
                    "creator": "Clinical,Researcher;Medical,Doctor",
                    "type": "http://purl.org/coar/resource_type/c_ddb1",
                    "description": "fr:Données d'étude clinique contrôlée randomisée|en:Randomized controlled clinical study data",
                    "keywords": "fr:clinique;étude;médical;randomisé|en:clinical;study;medical;randomized",
                    "license": "CC-BY-NC-4.0",
                    "ethics_approval": "IRB-2024-CLINICAL-001",
                    "study_design": "fr:Essai randomisé contrôlé|en:Randomized controlled trial",
                    "sample_size": "n=200",
                    "inclusion_criteria": "fr:Critères d'inclusion|en:Inclusion criteria",
                    "exclusion_criteria": "fr:Critères d'exclusion|en:Exclusion criteria",
                    "primary_outcome": "fr:Critère de jugement principal|en:Primary endpoint",
                    "statistical_method": "fr:Test t de Student|en:Student's t-test"
                }
            }
        }
    
    def list_available_templates(self) -> List[str]:
        """List all available template names."""
        return list(self.domain_templates.keys())
    
    def get_template_info(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a template."""
        return self.domain_templates.get(template_name)
    
    def generate_csv_template(self, template_name: str, output_file: str = None, num_examples: int = 1) -> str:
        """Generate CSV template file with examples."""
        
        if template_name not in self.domain_templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.domain_templates[template_name]
        
        if output_file is None:
            output_file = f"{template_name}_template.csv"
        
        # Create example data
        examples = []
        base_fields = template["fields"]
        
        for i in range(num_examples):
            example = base_fields.copy()
            # Add file field with example path
            example["file"] = f"data/{template_name}/example_{i+1}.csv"
            examples.append(example)
        
        # Write CSV
        if examples:
            fieldnames = examples[0].keys()
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(examples)
        
        print(f"✅ Generated template: {output_file}")
        print(f"📋 Template: {template['name']}")
        print(f"🔧 Fields: {len(base_fields)}")
        print(f"📊 Examples: {num_examples}")
        
        return output_file
    
    def generate_field_mapping(self, template_name: str) -> Dict[str, str]:
        """Generate custom field mapping for a template."""
        
        if template_name not in self.domain_templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.domain_templates[template_name]
        
        # Create field mapping
        mapping = {}
        
        # Standard fields
        standard_fields = {
            "title": "http://nakala.fr/terms#title",
            "creator": "http://nakala.fr/terms#creator", 
            "type": "http://nakala.fr/terms#type",
            "description": "http://purl.org/dc/terms/description",
            "keywords": "http://purl.org/dc/terms/subject",
            "license": "http://nakala.fr/terms#license",
            "language": "http://purl.org/dc/terms/language",
        }
        
        # Domain-specific field URI prefixes
        domain_prefixes = {
            "anthropology": "http://anthro.org/terms#",
            "linguistics": "http://linguistics.org/terms#", 
            "archaeological": "http://archaeology.org/terms#",
            "digital_humanities": "http://dh.org/terms#",
            "clinical": "http://clinical.org/terms#"
        }
        
        # Find appropriate prefix
        prefix = "http://research.org/terms#"  # Default
        for domain, domain_prefix in domain_prefixes.items():
            if domain in template_name:
                prefix = domain_prefix
                break
        
        # Map all fields
        for field in template["fields"].keys():
            if field in standard_fields:
                mapping[field] = standard_fields[field]
            else:
                mapping[field] = f"{prefix}{field}"
        
        return mapping
    
    def create_enhanced_preview_script(self, template_name: str, output_script: str = None) -> str:
        """Create a complete preview script for the template."""
        
        if output_script is None:
            output_script = f"{template_name}_preview.py"
        
        template = self.domain_templates[template_name]
        field_mapping = self.generate_field_mapping(template_name)
        
        script_content = f'''#!/usr/bin/env python3
"""
Enhanced Preview Script for {template['name']}
Auto-generated template integration with O-Nakala preview tool.
"""

import sys
import csv
import subprocess
from pathlib import Path
from o_nakala_core.common.utils import NakalaCommonUtils

def get_{template_name}_field_mapping():
    """Custom field mapping for {template['name']}."""
    return {repr(field_mapping)}

def process_{template_name}_csv(csv_file):
    """Process CSV with {template_name}-specific field mapping."""
    
    custom_mapping = get_{template_name}_field_mapping()
    utils = NakalaCommonUtils()
    
    print(f"🔬 Processing {{csv_file}} with {template['name']} mapping")
    print(f"📋 Custom fields available: {{len(custom_mapping)}}")
    
    # Analyze CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader, 1):
            # Generate metadata
            metadata = utils.prepare_nakala_metadata(row, custom_mapping)
            
            print(f"\\n--- Entry {{i}} ---")
            print(f"CSV fields: {{list(row.keys())}}")
            print(f"Metadata entries: {{len(metadata)}}")
            
            # Show domain-specific fields processed
            domain_fields = [field for field in row.keys() 
                           if field in custom_mapping and 
                           "{template_name.split('_')[0]}" in custom_mapping[field]]
            
            if domain_fields:
                print(f"Domain-specific fields: {{domain_fields}}")

def run_enhanced_preview(csv_file):
    """Run preview tool with pre and post processing."""
    
    print("🚀 Enhanced Preview for {template['name']}")
    print("=" * 60)
    
    # Step 1: Domain-specific analysis
    print("\\n1️⃣ Domain-Specific Field Analysis")
    process_{template_name}_csv(csv_file)
    
    # Step 2: Standard preview tool
    print("\\n2️⃣ Standard Preview Tool") 
    result = subprocess.run([
        sys.executable, "-m", "o_nakala_core.cli.preview",
        "--csv", csv_file,
        "--enhance", 
        "--interactive"
    ])
    
    print("\\n✅ Enhanced preview complete!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python {output_script} <csv_file>")
        print("\\n💡 Generate template CSV first with:")
        print(f"   python -c 'from custom_templates import CustomTemplateGenerator; g=CustomTemplateGenerator(); g.generate_csv_template(\"{template_name}\")'")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    run_enhanced_preview(csv_file)
'''
        
        with open(output_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"✅ Generated preview script: {output_script}")
        return output_script

def main():
    """Interactive template generation."""
    
    print("🎯 Custom Template Generator for O-Nakala Preview Tool")
    print("=" * 65)
    
    generator = CustomTemplateGenerator()
    templates = generator.list_available_templates()
    
    print(f"\\n📋 Available templates ({len(templates)}):")
    for i, template_name in enumerate(templates, 1):
        info = generator.get_template_info(template_name)
        print(f"  {i}. {template_name}: {info['name']}")
    
    # Interactive selection
    try:
        choice = input(f"\\n🎯 Select template (1-{len(templates)}): ")
        selected_idx = int(choice) - 1
        
        if 0 <= selected_idx < len(templates):
            template_name = templates[selected_idx]
            
            print(f"\\n🔧 Generating files for: {template_name}")
            
            # Generate CSV template
            csv_file = generator.generate_csv_template(template_name, num_examples=2)
            
            # Generate preview script  
            script_file = generator.create_enhanced_preview_script(template_name)
            
            print(f"\\n🎉 Files created:")
            print(f"   • CSV template: {csv_file}")
            print(f"   • Preview script: {script_file}")
            
            print(f"\\n💡 Usage:")
            print(f"   1. Edit CSV template: {csv_file}")
            print(f"   2. Run enhanced preview: python {script_file} {csv_file}")
            
        else:
            print("❌ Invalid selection")
            
    except (ValueError, KeyboardInterrupt):
        print("\\n⚠️ Operation cancelled")

if __name__ == "__main__":
    main()
```

### Step 2: Template Management System

```python
#!/usr/bin/env python3
"""
Template Management System
Organize and manage custom templates for different research domains.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional

class TemplateManager:
    """Manage custom templates with persistence and validation."""
    
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(exist_ok=True)
        
        # Template registry
        self.registry_file = self.template_dir / "template_registry.json"
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load template registry from disk."""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load registry: {e}")
        
        return {
            "templates": {},
            "categories": {},
            "created": [],
            "last_used": {}
        }
    
    def _save_registry(self):
        """Save template registry to disk."""
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, indent=2, ensure_ascii=False)
    
    def create_template(self, 
                       name: str, 
                       description: str,
                       category: str,
                       fields: Dict[str, str],
                       coar_type: str = "http://purl.org/coar/resource_type/c_ddb1") -> str:
        """Create a new custom template."""
        
        template_data = {
            "name": name,
            "description": description,
            "category": category,
            "coar_type": coar_type,
            "fields": fields,
            "created_date": "2024-03-15",  # Would use datetime.now()
            "version": "1.0"
        }
        
        # Save template file
        template_file = self.template_dir / f"{name.lower().replace(' ', '_')}.json"
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=2, ensure_ascii=False)
        
        # Update registry
        template_id = name.lower().replace(' ', '_')
        self.registry["templates"][template_id] = {
            "name": name,
            "description": description,
            "category": category,
            "file": str(template_file),
            "created": "2024-03-15"
        }
        
        # Update categories
        if category not in self.registry["categories"]:
            self.registry["categories"][category] = []
        self.registry["categories"][category].append(template_id)
        
        self.registry["created"].append(template_id)
        self._save_registry()
        
        print(f"✅ Created template: {name}")
        print(f"📁 Saved to: {template_file}")
        
        return str(template_file)
    
    def list_templates(self, category: str = None) -> List[Dict[str, Any]]:
        """List available templates, optionally filtered by category."""
        
        templates = []
        for template_id, info in self.registry["templates"].items():
            if category is None or info["category"] == category:
                templates.append({
                    "id": template_id,
                    **info
                })
        
        return templates
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get template data by ID."""
        
        if template_id not in self.registry["templates"]:
            return None
        
        template_info = self.registry["templates"][template_id]
        template_file = Path(template_info["file"])
        
        if not template_file.exists():
            print(f"Warning: Template file not found: {template_file}")
            return None
        
        with open(template_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_csv_from_template(self, template_id: str, output_file: str = None, num_examples: int = 1) -> str:
        """Generate CSV file from template."""
        
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        if output_file is None:
            output_file = f"{template_id}_example.csv"
        
        # Create example rows
        examples = []
        for i in range(num_examples):
            example = template["fields"].copy()
            example["file"] = f"data/{template_id}/example_{i+1}.csv"
            examples.append(example)
        
        # Write CSV
        if examples:
            fieldnames = examples[0].keys()
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(examples)
        
        # Update usage tracking
        self.registry["last_used"][template_id] = "2024-03-15"
        self._save_registry()
        
        print(f"✅ Generated CSV: {output_file}")
        print(f"📋 Template: {template['name']}")
        print(f"🔧 Fields: {len(template['fields'])}")
        
        return output_file
    
    def validate_template(self, template_id: str) -> Dict[str, Any]:
        """Validate template structure and field mappings."""
        
        template = self.get_template(template_id)
        if not template:
            return {"valid": False, "errors": ["Template not found"]}
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "field_analysis": {}
        }
        
        # Required fields check
        required_fields = ["name", "description", "fields", "coar_type"]
        for field in required_fields:
            if field not in template:
                validation_result["errors"].append(f"Missing required field: {field}")
                validation_result["valid"] = False
        
        # COAR type validation
        if "coar_type" in template:
            coar_uri = template["coar_type"]
            if not coar_uri.startswith("http://purl.org/coar/resource_type/"):
                validation_result["errors"].append(f"Invalid COAR type: {coar_uri}")
                validation_result["valid"] = False
        
        # Field analysis
        if "fields" in template:
            fields = template["fields"]
            
            # Check for required metadata fields
            essential_fields = ["title", "creator", "type", "description"]
            missing_essential = [f for f in essential_fields if f not in fields]
            
            if missing_essential:
                validation_result["warnings"].append(
                    f"Missing recommended fields: {missing_essential}"
                )
            
            # Field type analysis
            validation_result["field_analysis"] = {
                "total_fields": len(fields),
                "required_fields": len([f for f in essential_fields if f in fields]),
                "custom_fields": len([f for f in fields.keys() 
                                    if f not in ["title", "creator", "type", "description", 
                                               "keywords", "license", "date", "language"]])
            }
        
        return validation_result

def main():
    """Interactive template management."""
    
    print("🎛️ Template Management System")
    print("=" * 50)
    
    manager = TemplateManager()
    
    while True:
        print(f"\\n📋 Template Management Options:")
        print("1. List templates")
        print("2. Create new template") 
        print("3. Generate CSV from template")
        print("4. Validate template")
        print("5. Show template details")
        print("6. Exit")
        
        choice = input(f"\\n🎯 Select option (1-6): ").strip()
        
        if choice == "1":
            templates = manager.list_templates()
            if templates:
                print(f"\\n📚 Available templates ({len(templates)}):")
                for template in templates:
                    print(f"  • {template['id']}: {template['name']} ({template['category']})")
            else:
                print("\\n📭 No templates found")
        
        elif choice == "2":
            print(f"\\n🆕 Create New Template")
            name = input("Template name: ")
            description = input("Description: ")
            category = input("Category: ")
            
            print("\\nAdd fields (press Enter with empty name to finish):")
            fields = {}
            while True:
                field_name = input("Field name: ").strip()
                if not field_name:
                    break
                field_value = input(f"Default value for {field_name}: ")
                fields[field_name] = field_value
            
            if fields:
                manager.create_template(name, description, category, fields)
            else:
                print("❌ No fields provided")
        
        elif choice == "3":
            template_id = input("Template ID: ").strip()
            output_file = input("Output CSV file (optional): ").strip() or None
            
            try:
                csv_file = manager.generate_csv_from_template(template_id, output_file)
                print(f"\\n💡 Test with: o-nakala-preview --csv {csv_file}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "4":
            template_id = input("Template ID: ").strip()
            validation = manager.validate_template(template_id)
            
            print(f"\\n🔍 Validation Results:")
            print(f"Valid: {'✅' if validation['valid'] else '❌'}")
            
            if validation["errors"]:
                print(f"\\n❌ Errors:")
                for error in validation["errors"]:
                    print(f"  • {error}")
            
            if validation["warnings"]:
                print(f"\\n⚠️ Warnings:")
                for warning in validation["warnings"]:
                    print(f"  • {warning}")
            
            if "field_analysis" in validation:
                analysis = validation["field_analysis"]
                print(f"\\n📊 Field Analysis:")
                print(f"  • Total fields: {analysis['total_fields']}")
                print(f"  • Required fields: {analysis['required_fields']}")
                print(f"  • Custom fields: {analysis['custom_fields']}")
        
        elif choice == "5":
            template_id = input("Template ID: ").strip()
            template = manager.get_template(template_id)
            
            if template:
                print(f"\\n📄 Template Details:")
                print(f"Name: {template['name']}")
                print(f"Description: {template['description']}")
                print(f"Category: {template.get('category', 'Unknown')}")
                print(f"COAR Type: {template.get('coar_type', 'Not specified')}")
                print(f"Fields: {len(template.get('fields', {}))}")
                
                if template.get('fields'):
                    print(f"\\n🔧 Available Fields:")
                    for field, value in list(template['fields'].items())[:5]:
                        preview = str(value)[:40] + "..." if len(str(value)) > 40 else str(value)
                        print(f"  • {field}: {preview}")
                    
                    if len(template['fields']) > 5:
                        print(f"  ... and {len(template['fields']) - 5} more fields")
            else:
                print("❌ Template not found")
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
```

---

## Complete Integration Example

This section demonstrates how to integrate all three methods into a comprehensive workflow.

### Step 1: Complete Integration Script

Create `complete_integration.py`:

```python
#!/usr/bin/env python3
"""
Complete Integration Example: Custom Fields + COAR Types + Templates
Demonstrates comprehensive extension of O-Nakala preview tool.
"""

import sys
import csv
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import our custom modules
from custom_mapping import get_anthropology_field_mapping
from coar_validator import validate_coar_types_in_csv, fix_coar_types_in_csv  
from custom_templates import CustomTemplateGenerator

class IntegratedNakalaWorkflow:
    """Complete integrated workflow for custom NAKALA metadata processing."""
    
    def __init__(self):
        self.field_mapping = get_anthropology_field_mapping()
        self.template_generator = CustomTemplateGenerator()
        self.validation_results = {}
    
    def process_complete_workflow(self, 
                                csv_file: str, 
                                template_name: str = None,
                                fix_coar: bool = True,
                                run_preview: bool = True) -> Dict[str, Any]:
        """
        Complete workflow: validation, enhancement, preview.
        
        Args:
            csv_file: Input CSV file
            template_name: Optional template to validate against
            fix_coar: Whether to auto-fix COAR type errors
            run_preview: Whether to run the preview tool
            
        Returns:
            Complete workflow results
        """
        
        results = {
            "input_file": csv_file,
            "validation": {},
            "coar_analysis": {},
            "field_analysis": {},
            "template_match": {},
            "preview_results": {},
            "files_generated": [],
            "recommendations": []
        }
        
        print(f"🚀 Integrated NAKALA Workflow")
        print(f"=" * 60)
        print(f"📁 Processing: {csv_file}")
        
        # Step 1: Basic CSV validation
        print(f"\\n1️⃣ CSV Structure Validation")
        results["validation"] = self._validate_csv_structure(csv_file)
        
        # Step 2: COAR type analysis and correction
        print(f"\\n2️⃣ COAR Type Analysis") 
        results["coar_analysis"] = self._analyze_coar_types(csv_file, fix_coar)
        working_file = results["coar_analysis"].get("corrected_file", csv_file)
        
        # Step 3: Custom field analysis
        print(f"\\n3️⃣ Custom Field Analysis")
        results["field_analysis"] = self._analyze_custom_fields(working_file)
        
        # Step 4: Template matching (if specified)
        if template_name:
            print(f"\\n4️⃣ Template Validation")
            results["template_match"] = self._validate_against_template(working_file, template_name)
        
        # Step 5: Enhanced preview (if requested)
        if run_preview:
            print(f"\\n5️⃣ Enhanced Preview Generation")
            results["preview_results"] = self._run_enhanced_preview(working_file)
        
        # Step 6: Generate recommendations
        print(f"\\n6️⃣ Generating Recommendations")
        results["recommendations"] = self._generate_recommendations(results)
        
        # Summary
        self._print_workflow_summary(results)
        
        return results
    
    def _validate_csv_structure(self, csv_file: str) -> Dict[str, Any]:
        """Validate basic CSV structure."""
        
        validation = {
            "file_exists": False,
            "readable": False, 
            "entries_count": 0,
            "fields_found": [],
            "issues": []
        }
        
        try:
            if not Path(csv_file).exists():
                validation["issues"].append(f"File not found: {csv_file}")
                return validation
            
            validation["file_exists"] = True
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                validation["readable"] = True
                validation["fields_found"] = reader.fieldnames or []
                
                entries = list(reader)
                validation["entries_count"] = len(entries)
            
            print(f"   ✅ File structure valid")
            print(f"   📊 Entries: {validation['entries_count']}")
            print(f"   🔧 Fields: {len(validation['fields_found'])}")
            
        except Exception as e:
            validation["issues"].append(f"Error reading CSV: {str(e)}")
            print(f"   ❌ Validation failed: {e}")
        
        return validation
    
    def _analyze_coar_types(self, csv_file: str, fix_errors: bool = True) -> Dict[str, Any]:
        """Analyze and optionally fix COAR types."""
        
        coar_results = validate_coar_types_in_csv(csv_file)
        
        print(f"   📊 COAR Analysis:")
        print(f"      • Valid types: {len(coar_results['valid_types'])}")
        print(f"      • Invalid types: {len(coar_results['invalid_types'])}")
        
        if coar_results["invalid_types"] and fix_errors:
            print(f"   🔧 Auto-fixing invalid COAR types...")
            corrected_file = fix_coar_types_in_csv(csv_file)
            coar_results["corrected_file"] = corrected_file
            print(f"   ✅ Corrected file: {corrected_file}")
        else:
            coar_results["corrected_file"] = csv_file
        
        return coar_results
    
    def _analyze_custom_fields(self, csv_file: str) -> Dict[str, Any]:
        """Analyze custom field usage and mapping."""
        
        field_analysis = {
            "total_fields": 0,
            "standard_fields": [],
            "custom_fields": [],
            "mapped_custom_fields": [],
            "unmapped_fields": [],
            "field_coverage": 0.0
        }
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                all_fields = reader.fieldnames or []
            
            field_analysis["total_fields"] = len(all_fields)
            
            # Categorize fields
            standard_fields = ["title", "creator", "type", "description", "keywords", 
                             "license", "date", "language", "file"]
            
            field_analysis["standard_fields"] = [f for f in all_fields if f in standard_fields]
            field_analysis["custom_fields"] = [f for f in all_fields if f not in standard_fields]
            
            # Check mapping coverage
            field_analysis["mapped_custom_fields"] = [
                f for f in field_analysis["custom_fields"] 
                if f in self.field_mapping
            ]
            field_analysis["unmapped_fields"] = [
                f for f in field_analysis["custom_fields"]
                if f not in self.field_mapping
            ]
            
            if field_analysis["custom_fields"]:
                field_analysis["field_coverage"] = (
                    len(field_analysis["mapped_custom_fields"]) / 
                    len(field_analysis["custom_fields"]) * 100
                )
            
            print(f"   📊 Field Analysis:")
            print(f"      • Total fields: {field_analysis['total_fields']}")
            print(f"      • Standard fields: {len(field_analysis['standard_fields'])}")
            print(f"      • Custom fields: {len(field_analysis['custom_fields'])}")
            print(f"      • Mapped custom: {len(field_analysis['mapped_custom_fields'])}")
            print(f"      • Coverage: {field_analysis['field_coverage']:.1f}%")
            
        except Exception as e:
            field_analysis["error"] = str(e)
            print(f"   ❌ Field analysis failed: {e}")
        
        return field_analysis
    
    def _validate_against_template(self, csv_file: str, template_name: str) -> Dict[str, Any]:
        """Validate CSV against a specific template."""
        
        template_validation = {
            "template_name": template_name,
            "template_found": False,
            "field_matches": [],
            "missing_fields": [],
            "extra_fields": [],
            "match_percentage": 0.0
        }
        
        try:
            template_info = self.template_generator.get_template_info(template_name)
            if not template_info:
                template_validation["error"] = f"Template not found: {template_name}"
                print(f"   ❌ Template not found: {template_name}")
                return template_validation
            
            template_validation["template_found"] = True
            
            # Get CSV fields
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                csv_fields = set(reader.fieldnames or [])
            
            # Get template fields
            template_fields = set(template_info["fields"].keys())
            
            # Compare
            template_validation["field_matches"] = list(csv_fields & template_fields)
            template_validation["missing_fields"] = list(template_fields - csv_fields)
            template_validation["extra_fields"] = list(csv_fields - template_fields)
            
            if template_fields:
                template_validation["match_percentage"] = (
                    len(template_validation["field_matches"]) / len(template_fields) * 100
                )
            
            print(f"   📋 Template Validation ({template_name}):")
            print(f"      • Field matches: {len(template_validation['field_matches'])}")
            print(f"      • Missing fields: {len(template_validation['missing_fields'])}")
            print(f"      • Extra fields: {len(template_validation['extra_fields'])}")
            print(f"      • Match rate: {template_validation['match_percentage']:.1f}%")
            
        except Exception as e:
            template_validation["error"] = str(e)
            print(f"   ❌ Template validation failed: {e}")
        
        return template_validation
    
    def _run_enhanced_preview(self, csv_file: str) -> Dict[str, Any]:
        """Run the preview tool with enhancements."""
        
        preview_results = {
            "preview_file": None,
            "success": False,
            "command_output": "",
            "errors": []
        }
        
        try:
            # Generate preview file name
            preview_file = csv_file.replace('.csv', '_integrated_preview.json')
            
            # Run preview tool
            cmd = [
                sys.executable, "-m", "o_nakala_core.cli.preview",
                "--csv", csv_file,
                "--enhance",
                "--json-output", preview_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            preview_results["command_output"] = result.stdout
            preview_results["success"] = result.returncode == 0
            
            if result.returncode == 0:
                preview_results["preview_file"] = preview_file
                print(f"   ✅ Preview generated: {preview_file}")
            else:
                preview_results["errors"].append(f"Preview failed: {result.stderr}")
                print(f"   ❌ Preview failed: {result.stderr}")
            
        except subprocess.TimeoutExpired:
            preview_results["errors"].append("Preview timed out")
            print(f"   ⏱️ Preview timed out")
        except Exception as e:
            preview_results["errors"].append(f"Preview error: {str(e)}")
            print(f"   ❌ Preview error: {e}")
        
        return preview_results
    
    def _generate_recommendations(self, workflow_results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate recommendations based on workflow analysis."""
        
        recommendations = []
        
        # COAR type recommendations
        coar_analysis = workflow_results.get("coar_analysis", {})
        if coar_analysis.get("invalid_types"):
            recommendations.append({
                "type": "coar_types",
                "priority": "high",
                "issue": f"Found {len(coar_analysis['invalid_types'])} invalid COAR types",
                "action": "Use valid COAR resource type URIs",
                "example": "http://purl.org/coar/resource_type/c_ddb1"
            })
        
        # Field mapping recommendations  
        field_analysis = workflow_results.get("field_analysis", {})
        if field_analysis.get("unmapped_fields"):
            recommendations.append({
                "type": "field_mapping",
                "priority": "medium",
                "issue": f"{len(field_analysis['unmapped_fields'])} unmapped custom fields",
                "action": "Add custom field mappings for better processing",
                "example": "Add to custom_mapping.py"
            })
        
        # Template recommendations
        template_match = workflow_results.get("template_match", {})
        if template_match.get("missing_fields"):
            recommendations.append({
                "type": "template_compliance", 
                "priority": "medium",
                "issue": f"Missing {len(template_match['missing_fields'])} template fields",
                "action": "Add missing fields to improve template compliance",
                "example": f"Consider adding: {', '.join(template_match['missing_fields'][:3])}"
            })
        
        # Preview recommendations
        preview_results = workflow_results.get("preview_results", {})
        if not preview_results.get("success"):
            recommendations.append({
                "type": "preview_generation",
                "priority": "high", 
                "issue": "Preview generation failed",
                "action": "Fix CSV structure and field validation issues",
                "example": "Check for required fields: title, type"
            })
        
        return recommendations
    
    def _print_workflow_summary(self, results: Dict[str, Any]):
        """Print comprehensive workflow summary."""
        
        print(f"\\n" + "="*60)
        print(f"📊 WORKFLOW SUMMARY")
        print(f"="*60)
        
        # Overall status
        validation_ok = results["validation"].get("readable", False)
        coar_ok = len(results["coar_analysis"].get("invalid_types", [])) == 0
        preview_ok = results["preview_results"].get("success", False)
        
        overall_status = "✅ READY" if (validation_ok and coar_ok and preview_ok) else "⚠️ NEEDS ATTENTION"
        print(f"🎯 Overall Status: {overall_status}")
        
        # Key metrics
        print(f"\\n📈 Key Metrics:")
        print(f"   • Entries processed: {results['validation'].get('entries_count', 0)}")
        print(f"   • Fields found: {len(results['validation'].get('fields_found', []))}")
        print(f"   • Custom field coverage: {results['field_analysis'].get('field_coverage', 0):.1f}%")
        print(f"   • COAR types valid: {len(results['coar_analysis'].get('valid_types', []))}")
        
        # Recommendations
        recommendations = results.get("recommendations", [])
        if recommendations:
            print(f"\\n💡 Recommendations ({len(recommendations)}):")
            for rec in recommendations[:3]:  # Show top 3
                priority_icon = "🔴" if rec["priority"] == "high" else "🟡"
                print(f"   {priority_icon} {rec['issue']}")
                print(f"      → {rec['action']}")
        
        # Files generated
        files = []
        if results["coar_analysis"].get("corrected_file") != results["input_file"]:
            files.append(results["coar_analysis"]["corrected_file"])
        if results["preview_results"].get("preview_file"):
            files.append(results["preview_results"]["preview_file"])
        
        if files:
            print(f"\\n📁 Files Generated:")
            for file in files:
                print(f"   • {file}")
        
        # Next steps
        print(f"\\n🚀 Next Steps:")
        if overall_status == "✅ READY":
            print("   1. Review preview JSON file")
            print("   2. Upload with: o-nakala-upload --csv <file>")
            print("   3. Create collections as needed")
        else:
            print("   1. Address recommendations above")
            print("   2. Re-run workflow after fixes")
            print("   3. Validate preview before upload")

def main():
    """Interactive workflow execution."""
    
    if len(sys.argv) < 2:
        print("🚀 Integrated NAKALA Workflow")
        print("Usage: python complete_integration.py <csv_file> [template_name]")
        print("\\nExample:")
        print("  python complete_integration.py data.csv anthropology_fieldwork")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    template_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Run complete workflow
    workflow = IntegratedNakalaWorkflow()
    results = workflow.process_complete_workflow(
        csv_file=csv_file,
        template_name=template_name,
        fix_coar=True,
        run_preview=True
    )
    
    # Save results
    results_file = csv_file.replace('.csv', '_workflow_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\\n💾 Workflow results saved: {results_file}")

if __name__ == "__main__":
    main()
```

---

## Troubleshooting Common Issues

### Issue 1: "Unknown fields will be ignored" Warning

**Problem**: Preview tool shows warnings for custom fields.

**Solution**:
```python
# Create custom field mapping
custom_mapping = {
    "your_custom_field": "http://your-domain.org/terms#your_field",
    # ... other mappings
}

# Use with utils
from o_nakala_core.common.utils import NakalaCommonUtils
utils = NakalaCommonUtils()
metadata = utils.prepare_nakala_metadata(row_data, custom_mapping)
```

### Issue 2: COAR Type Validation Errors

**Problem**: "Invalid resource type URI" errors.

**Solution**:
```python
# Valid COAR URI format
valid_coar = "http://purl.org/coar/resource_type/c_ddb1"

# Invalid formats
invalid_examples = [
    "dataset",  # Plain text
    "http://example.com/dataset",  # Wrong domain
    "purl.org/coar/resource_type/c_ddb1"  # Missing http://
]

# Auto-correction
corrections = {
    "dataset": "http://purl.org/coar/resource_type/c_ddb1",
    "software": "http://purl.org/coar/resource_type/c_5ce6",
    "text": "http://purl.org/coar/resource_type/c_18cf"
}
```

### Issue 3: Multilingual Format Errors

**Problem**: Bilingual titles not recognized.

**Solution**:
```python
# Correct format
correct_title = "fr:Titre français|en:English title"

# Common errors
wrong_formats = [
    "Titre français|English title",  # Missing language codes
    "fr: Titre français | en: English title",  # Extra spaces
    "french:Titre français|english:English title"  # Wrong language codes
]

# Validation function
def validate_multilingual_format(value):
    if "|" in value:
        parts = value.split("|")
        for part in parts:
            if not part.strip().startswith(("fr:", "en:")):
                return False
    return True
```

### Issue 4: Template Field Mismatches

**Problem**: CSV fields don't match template expectations.

**Solution**:
```python
def validate_csv_against_template(csv_file, template_fields):
    """Validate CSV fields against template."""
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        csv_fields = set(reader.fieldnames or [])
    
    template_set = set(template_fields.keys())
    
    missing = template_set - csv_fields
    extra = csv_fields - template_set
    
    return {
        "missing_fields": list(missing),
        "extra_fields": list(extra),
        "match_rate": len(csv_fields & template_set) / len(template_set) * 100
    }
```

### Issue 5: Preview Generation Failures

**Problem**: Preview tool crashes or produces no output.

**Solution**:
```python
# Debug checklist
debug_steps = [
    "1. Check file exists and is readable",
    "2. Verify CSV has header row",
    "3. Check for required fields: title, type",
    "4. Validate COAR type URIs",
    "5. Check for encoding issues (use UTF-8)",
    "6. Verify no empty required fields"
]

def debug_csv_file(csv_file):
    """Debug common CSV issues."""
    
    issues = []
    
    # Check file existence
    if not Path(csv_file).exists():
        issues.append(f"File not found: {csv_file}")
        return issues
    
    # Check readability
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)
    except Exception as e:
        issues.append(f"Cannot read CSV: {e}")
        return issues
    
    # Check required fields
    if not fieldnames:
        issues.append("No header row found")
        return issues
    
    required = ["title", "type"]
    missing = [f for f in required if f not in fieldnames]
    if missing:
        issues.append(f"Missing required fields: {missing}")
    
    # Check data
    if not rows:
        issues.append("No data rows found")
    
    return issues
```

### Issue 6: Memory Issues with Large Files

**Problem**: Preview tool runs out of memory with large CSV files.

**Solution**:
```python
def process_large_csv_in_chunks(csv_file, chunk_size=100):
    """Process large CSV files in chunks."""
    
    import pandas as pd
    
    # Read in chunks
    chunk_results = []
    
    for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
        # Process chunk
        chunk_dict = chunk.to_dict('records')
        
        # Process each row in chunk
        for row in chunk_dict:
            # Your processing logic here
            metadata = utils.prepare_nakala_metadata(row, custom_mapping)
            chunk_results.append(metadata)
    
    return chunk_results
```

---

## Best Practices and Recommendations

### 1. Field Mapping Design

**Recommended Structure:**
```python
def create_hierarchical_field_mapping(domain):
    """Create well-structured field mapping."""
    
    # Base ontology URL
    base_url = f"http://{domain}.org/terms#"
    
    # Hierarchical organization
    mapping = {
        # Administrative metadata
        f"admin_project_code": f"{base_url}admin/project_code",
        f"admin_funding": f"{base_url}admin/funding_source",
        f"admin_ethics": f"{base_url}admin/ethics_approval",
        
        # Methodological metadata
        f"method_data_collection": f"{base_url}methodology/data_collection",
        f"method_analysis": f"{base_url}methodology/analysis_method",
        f"method_sampling": f"{base_url}methodology/sampling_strategy",
        
        # Content metadata
        f"content_subjects": f"{base_url}content/research_subjects", 
        f"content_location": f"{base_url}content/geographic_location",
        f"content_timeframe": f"{base_url}content/temporal_coverage"
    }
    
    return mapping
```

**Benefits:**
- Clear namespace organization
- Easy to extend and maintain
- Self-documenting field purposes
- Compatible with semantic web standards

### 2. Template Organization

**Recommended Structure:**
```
templates/
├── domains/
│   ├── anthropology/
│   │   ├── fieldwork.json
│   │   ├── interview_data.json
│   │   └── cultural_analysis.json
│   ├── linguistics/
│   │   ├── corpus_documentation.json
│   │   └── phonetic_analysis.json
│   └── archaeology/
│       ├── excavation_data.json
│       └── survey_results.json
├── institutional/
│   ├── university_template.json
│   └── research_center_template.json
└── generic/
    ├── basic_dataset.json
    └── simple_document.json
```

### 3. Version Control for Custom Extensions

**Recommended Approach:**
```python
class VersionedCustomMapping:
    """Version-controlled custom field mappings."""
    
    VERSION = "2.1.0"
    LAST_UPDATED = "2024-03-15"
    
    def __init__(self):
        self.version_history = {
            "1.0.0": "Initial anthropology mapping",
            "2.0.0": "Added linguistics and archaeology fields", 
            "2.1.0": "Enhanced institutional metadata"
        }
    
    def get_mapping(self, version=None):
        """Get field mapping for specific version."""
        if version is None:
            version = self.VERSION
        
        # Return appropriate mapping for version
        return self._get_mapping_for_version(version)
    
    def validate_compatibility(self, required_version):
        """Check if current version is compatible."""
        # Version comparison logic
        return self._compare_versions(self.VERSION, required_version)
```

### 4. Testing Custom Extensions

**Comprehensive Test Suite:**
```python
#!/usr/bin/env python3
"""
Test Suite for Custom Extensions
Validates field mappings, templates, and COAR types.
"""

import unittest
import csv
import tempfile
from pathlib import Path

class TestCustomExtensions(unittest.TestCase):
    """Test custom NAKALA extensions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = {
            "title": "fr:Test Title|en:Test Title", 
            "creator": "Test,Creator",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "custom_field": "Test value",
            "fieldwork_location": "fr:Site de test|en:Test site"
        }
    
    def test_custom_field_mapping(self):
        """Test custom field mapping functionality."""
        from custom_mapping import get_anthropology_field_mapping
        from o_nakala_core.common.utils import NakalaCommonUtils
        
        mapping = get_anthropology_field_mapping()
        utils = NakalaCommonUtils()
        
        # Test metadata generation
        metadata = utils.prepare_nakala_metadata(self.test_data, mapping)
        
        # Assertions
        self.assertIsInstance(metadata, list)
        self.assertGreater(len(metadata), 0)
        
        # Check custom field processing
        custom_entries = [m for m in metadata 
                         if "fieldwork_location" in m.get("propertyUri", "")]
        self.assertGreater(len(custom_entries), 0)
    
    def test_coar_type_validation(self):
        """Test COAR type validation."""
        from coar_validator import validate_coar_types_in_csv
        
        # Create test CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=self.test_data.keys())
            writer.writeheader()
            writer.writerow(self.test_data)
            test_file = f.name
        
        try:
            results = validate_coar_types_in_csv(test_file)
            
            # Assertions
            self.assertEqual(results["entries_analyzed"], 1)
            self.assertEqual(len(results["valid_types"]), 1)
            self.assertEqual(len(results["invalid_types"]), 0)
        
        finally:
            Path(test_file).unlink()
    
    def test_template_generation(self):
        """Test template generation."""
        from custom_templates import CustomTemplateGenerator
        
        generator = CustomTemplateGenerator()
        
        # Test template listing
        templates = generator.list_available_templates()
        self.assertIsInstance(templates, list)
        self.assertGreater(len(templates), 0)
        
        # Test template info
        template_name = templates[0]
        info = generator.get_template_info(template_name)
        self.assertIsInstance(info, dict)
        self.assertIn("fields", info)
    
    def test_multilingual_format(self):
        """Test multilingual format parsing."""
        from o_nakala_core.common.utils import NakalaCommonUtils
        
        test_values = [
            "fr:Français|en:English",
            "fr:Français seulement",
            "Simple text",
            "fr:Français|en:English|de:Deutsch"
        ]
        
        for value in test_values:
            result = NakalaCommonUtils.parse_multilingual_field(value)
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)

def run_integration_tests():
    """Run all integration tests."""
    
    print("🧪 Running Custom Extension Tests")
    print("=" * 50)
    
    # Run unittest suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCustomExtensions)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print(f"\\n📊 Test Results:")
    print(f"   • Tests run: {result.testsRun}")
    print(f"   • Failures: {len(result.failures)}")
    print(f"   • Errors: {len(result.errors)}")
    
    if result.failures or result.errors:
        print(f"\\n❌ Some tests failed - check implementation")
        return False
    else:
        print(f"\\n✅ All tests passed!")
        return True

if __name__ == "__main__":
    run_integration_tests()
```

### 5. Documentation and Maintenance

**Create comprehensive documentation:**
```python
def generate_extension_documentation(output_file="EXTENSIONS.md"):
    """Generate documentation for custom extensions."""
    
    doc_content = f"""# Custom NAKALA Extensions Documentation

## Field Mappings
    
### Available Custom Fields
{list_custom_fields()}

### COAR Type Mappings  
{list_coar_types()}

### Template Catalog
{list_available_templates()}

## Usage Examples
{generate_usage_examples()}

## Troubleshooting
{generate_troubleshooting_guide()}

---
Generated: {datetime.now().isoformat()}
Version: {get_extension_version()}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(doc_content)
    
    return output_file
```

---

## Advanced Customization Techniques

### 1. Dynamic Field Mapping Based on Content

```python
class ContentAwareFieldMapper:
    """Dynamically adjust field mappings based on content analysis."""
    
    def __init__(self):
        self.content_patterns = {
            "interview": {
                "indicators": ["interview", "conversation", "oral", "speaking"],
                "additional_mapping": {
                    "interview_type": "http://interview.org/terms#type",
                    "interviewer": "http://interview.org/terms#interviewer",
                    "interviewee": "http://interview.org/terms#interviewee"
                }
            },
            "survey": {
                "indicators": ["survey", "questionnaire", "poll", "responses"],
                "additional_mapping": {
                    "survey_method": "http://survey.org/terms#method",
                    "response_rate": "http://survey.org/terms#response_rate",
                    "sample_method": "http://survey.org/terms#sampling"
                }
            }
        }
    
    def analyze_content_type(self, csv_data):
        """Analyze content to determine best mapping."""
        
        # Combine all text fields for analysis
        all_text = " ".join([
            row.get("title", ""),
            row.get("description", ""),
            row.get("keywords", "")
            for row in csv_data
        ]).lower()
        
        # Score content patterns
        scores = {}
        for content_type, config in self.content_patterns.items():
            score = sum(1 for indicator in config["indicators"] 
                       if indicator in all_text)
            scores[content_type] = score
        
        # Return best match
        if scores and max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return None
    
    def get_enhanced_mapping(self, csv_data, base_mapping):
        """Get enhanced mapping based on content analysis."""
        
        content_type = self.analyze_content_type(csv_data)
        enhanced_mapping = base_mapping.copy()
        
        if content_type and content_type in self.content_patterns:
            additional_mapping = self.content_patterns[content_type]["additional_mapping"]
            enhanced_mapping.update(additional_mapping)
            
            print(f"🎯 Detected content type: {content_type}")
            print(f"🔧 Added {len(additional_mapping)} specialized fields")
        
        return enhanced_mapping
```

### 2. Institutional Branding and Compliance

```python
class InstitutionalCompliance:
    """Ensure metadata meets institutional requirements."""
    
    def __init__(self, institution_config):
        self.institution = institution_config
        self.required_fields = institution_config.get("required_fields", [])
        self.field_validators = institution_config.get("validators", {})
        self.branding_rules = institution_config.get("branding", {})
    
    def validate_institutional_compliance(self, metadata_entry):
        """Validate metadata against institutional requirements."""
        
        compliance_result = {
            "compliant": True,
            "issues": [],
            "warnings": [],
            "enhancements": []
        }
        
        # Check required fields
        for field in self.required_fields:
            if field not in metadata_entry or not metadata_entry[field]:
                compliance_result["issues"].append(f"Missing required field: {field}")
                compliance_result["compliant"] = False
        
        # Apply field validators
        for field, validator_config in self.field_validators.items():
            if field in metadata_entry:
                value = metadata_entry[field]
                
                # Pattern validation
                if "pattern" in validator_config:
                    import re
                    if not re.match(validator_config["pattern"], value):
                        compliance_result["issues"].append(
                            f"Field {field} doesn't match required pattern"
                        )
                        compliance_result["compliant"] = False
                
                # Length validation
                if "max_length" in validator_config:
                    if len(value) > validator_config["max_length"]:
                        compliance_result["warnings"].append(
                            f"Field {field} exceeds recommended length"
                        )
        
        # Apply branding enhancements
        if self.branding_rules:
            enhancements = self._apply_branding_rules(metadata_entry)
            compliance_result["enhancements"].extend(enhancements)
        
        return compliance_result
    
    def _apply_branding_rules(self, metadata_entry):
        """Apply institutional branding rules."""
        
        enhancements = []
        
        # Add institutional identifier
        if "add_institution_id" in self.branding_rules:
            institution_id = self.branding_rules["add_institution_id"]
            enhancements.append({
                "field": "institutional_identifier",
                "value": institution_id,
                "reason": "Institutional branding requirement"
            })
        
        # Standardize creator format
        if "creator_format" in self.branding_rules and "creator" in metadata_entry:
            format_rule = self.branding_rules["creator_format"]
            if format_rule == "surname_first":
                # Transform creator to surname-first format
                enhancements.append({
                    "field": "creator",
                    "transformation": "surname_first",
                    "reason": "Institutional creator format standard"
                })
        
        return enhancements

# Example institutional config
UNIVERSITY_CONFIG = {
    "name": "University of Example",
    "required_fields": ["title", "creator", "type", "institutional_code"],
    "validators": {
        "institutional_code": {
            "pattern": r"^UE-\d{4}-[A-Z]{3}$"
        },
        "title": {
            "max_length": 200
        }
    },
    "branding": {
        "add_institution_id": "university-of-example",
        "creator_format": "surname_first"
    }
}
```

### 3. Automated Quality Assessment

```python
class MetadataQualityAssessor:
    """Assess and improve metadata quality automatically."""
    
    def __init__(self):
        self.quality_metrics = {
            "completeness": {"weight": 0.4, "max_score": 100},
            "richness": {"weight": 0.3, "max_score": 100}, 
            "consistency": {"weight": 0.2, "max_score": 100},
            "standardization": {"weight": 0.1, "max_score": 100}
        }
    
    def assess_metadata_quality(self, csv_file):
        """Comprehensive metadata quality assessment."""
        
        assessment = {
            "overall_score": 0,
            "metric_scores": {},
            "recommendations": [],
            "strengths": [],
            "improvement_areas": []
        }
        
        # Load and analyze data
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            fieldnames = reader.fieldnames or []
        
        # Assess each quality metric
        assessment["metric_scores"]["completeness"] = self._assess_completeness(data, fieldnames)
        assessment["metric_scores"]["richness"] = self._assess_richness(data, fieldnames)
        assessment["metric_scores"]["consistency"] = self._assess_consistency(data)
        assessment["metric_scores"]["standardization"] = self._assess_standardization(data)
        
        # Calculate overall score
        total_score = 0
        for metric, score in assessment["metric_scores"].items():
            weight = self.quality_metrics[metric]["weight"]
            total_score += score * weight
        
        assessment["overall_score"] = round(total_score, 1)
        
        # Generate recommendations
        assessment["recommendations"] = self._generate_quality_recommendations(assessment["metric_scores"])
        
        return assessment
    
    def _assess_completeness(self, data, fieldnames):
        """Assess completeness of metadata."""
        
        if not data:
            return 0
        
        # Essential fields for good completeness
        essential_fields = ["title", "creator", "type", "description", "keywords"]
        present_essential = [f for f in essential_fields if f in fieldnames]
        
        # Calculate field coverage
        field_score = len(present_essential) / len(essential_fields) * 50
        
        # Calculate data density (non-empty values)
        total_cells = len(data) * len(fieldnames)
        filled_cells = sum(1 for row in data for field in fieldnames 
                          if row.get(field, "").strip())
        
        density_score = (filled_cells / total_cells) * 50 if total_cells > 0 else 0
        
        return min(field_score + density_score, 100)
    
    def _assess_richness(self, data, fieldnames):
        """Assess richness and depth of metadata."""
        
        richness_indicators = {
            "multilingual_fields": 0,
            "detailed_descriptions": 0,
            "rich_keywords": 0,
            "temporal_coverage": 0,
            "spatial_coverage": 0
        }
        
        for row in data:
            # Check for multilingual content
            for field_value in row.values():
                if "|" in field_value and ("fr:" in field_value or "en:" in field_value):
                    richness_indicators["multilingual_fields"] += 1
                    break
            
            # Check description richness
            desc = row.get("description", "")
            if len(desc.split()) > 10:  # More than 10 words
                richness_indicators["detailed_descriptions"] += 1
            
            # Check keyword richness  
            keywords = row.get("keywords", "")
            if ";" in keywords or "|" in keywords:  # Multiple keywords
                richness_indicators["rich_keywords"] += 1
            
            # Check for temporal/spatial data
            for field in fieldnames:
                if "temporal" in field.lower() or "date" in field.lower():
                    if row.get(field, "").strip():
                        richness_indicators["temporal_coverage"] += 1
                        break
                        
                if "spatial" in field.lower() or "location" in field.lower():
                    if row.get(field, "").strip():
                        richness_indicators["spatial_coverage"] += 1
                        break
        
        # Calculate richness score
        max_possible = len(data) * len(richness_indicators)
        actual_richness = sum(richness_indicators.values())
        
        return (actual_richness / max_possible) * 100 if max_possible > 0 else 0
    
    def _assess_consistency(self, data):
        """Assess consistency across entries."""
        
        if len(data) < 2:
            return 100  # Single entry is always consistent
        
        consistency_scores = []
        
        # Check creator format consistency
        creator_formats = set()
        for row in data:
            creator = row.get("creator", "")
            if creator:
                # Detect format (comma-separated vs. semicolon vs. other)
                if ";" in creator:
                    creator_formats.add("semicolon_separated")
                elif "," in creator:
                    creator_formats.add("comma_separated")
                else:
                    creator_formats.add("simple")
        
        creator_consistency = 100 if len(creator_formats) <= 1 else 50
        consistency_scores.append(creator_consistency)
        
        # Check date format consistency
        date_formats = set()
        for row in data:
            date = row.get("date", "")
            if date:
                if len(date) == 4 and date.isdigit():
                    date_formats.add("year_only")
                elif "-" in date:
                    date_formats.add("iso_format")
                else:
                    date_formats.add("other")
        
        date_consistency = 100 if len(date_formats) <= 1 else 50
        consistency_scores.append(date_consistency)
        
        return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 100
    
    def _assess_standardization(self, data):
        """Assess adherence to standards."""
        
        standardization_score = 0
        total_checks = 0
        
        for row in data:
            # COAR type standardization
            coar_type = row.get("type", "")
            if coar_type:
                total_checks += 1
                if coar_type.startswith("http://purl.org/coar/resource_type/"):
                    standardization_score += 1
            
            # License standardization
            license_field = row.get("license", "")
            if license_field:
                total_checks += 1
                standard_licenses = ["CC-BY-4.0", "CC-BY-SA-4.0", "CC-BY-NC-4.0", "CC0-1.0"]
                if any(std_license in license_field for std_license in standard_licenses):
                    standardization_score += 1
            
            # Language code standardization
            language = row.get("language", "")
            if language:
                total_checks += 1
                if language in ["fr", "en", "de", "es", "it"]:  # ISO 639-1 codes
                    standardization_score += 1
        
        return (standardization_score / total_checks) * 100 if total_checks > 0 else 100
    
    def _generate_quality_recommendations(self, metric_scores):
        """Generate specific recommendations based on scores."""
        
        recommendations = []
        
        if metric_scores["completeness"] < 70:
            recommendations.append({
                "priority": "high",
                "metric": "completeness",
                "issue": "Low metadata completeness",
                "action": "Add missing essential fields: title, creator, type, description",
                "impact": "Improves discoverability and usability"
            })
        
        if metric_scores["richness"] < 60:
            recommendations.append({
                "priority": "medium", 
                "metric": "richness",
                "issue": "Limited metadata richness",
                "action": "Add multilingual titles, detailed descriptions, multiple keywords",
                "impact": "Enhances metadata quality and international accessibility"
            })
        
        if metric_scores["consistency"] < 80:
            recommendations.append({
                "priority": "medium",
                "metric": "consistency", 
                "issue": "Inconsistent formatting across entries",
                "action": "Standardize creator format and date format across all entries",
                "impact": "Improves data quality and processing reliability"
            })
        
        if metric_scores["standardization"] < 75:
            recommendations.append({
                "priority": "high",
                "metric": "standardization",
                "issue": "Poor adherence to standards",
                "action": "Use valid COAR types, standard license codes, ISO language codes",
                "impact": "Ensures interoperability and compliance"
            })
        
        return recommendations
```

---

## Conclusion

This comprehensive guide provides you with the tools and knowledge to fully extend the O-Nakala Core preview tool. The three main extension methods - custom field mapping, COAR type extension, and custom templates - can be used independently or combined for maximum flexibility.

**Key Takeaways:**

1. **Custom Field Mapping** is the most practical approach for immediate needs
2. **COAR Type Extension** works seamlessly - any valid COAR URI is accepted
3. **Custom Templates** provide systematic, reusable solutions for research domains
4. **Integration workflows** ensure quality and consistency across all extensions
5. **Testing and validation** are essential for reliable production use

**Next Steps:**

1. Start with the custom field mapping approach for immediate needs
2. Develop domain-specific templates for your research area
3. Create institutional compliance tools if needed
4. Implement quality assessment for ongoing improvement
5. Share your extensions with the research community

**Files Referenced:**
- `/Users/syl/Documents/GitHub/o-nakala-core/docs/examples/custom-field-mapping.py`
- `/Users/syl/Documents/GitHub/o-nakala-core/docs/examples/institutional-workflow.py`
- `/Users/syl/Documents/GitHub/o-nakala-core/src/o_nakala_core/cli/preview.py`
- `/Users/syl/Documents/GitHub/o-nakala-core/src/o_nakala_core/common/utils.py`

The preview tool's extensible architecture ensures that your customizations remain compatible with future versions while providing the flexibility needed for specialized research workflows.