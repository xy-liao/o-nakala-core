# CSV Field Testing Guide for O-Nakala Core

**Complete quality assurance guide for validating metadata CSV files before NAKALA upload**

## Introduction: Why Thorough Testing Matters

Metadata validation failures can halt research workflows and require time-consuming corrections. This guide provides systematic testing procedures to ensure perfect metadata quality before upload. By following these validation steps, researchers avoid:

- Upload failures due to invalid field formats
- Rejected submissions with unclear error messages
- Time lost debugging metadata issues during critical deadlines
- Incomplete metadata that doesn't meet repository standards

**Goal**: Achieve 100% upload success rate by validating every field comprehensively.

## Quick Validation Checklist (5-minute check)

Before diving into detailed testing, run this rapid validation:

### 1. File Structure Check
```bash
# Basic structure validation
o-nakala-preview --csv your_metadata.csv --validate-only

# Quick encoding check
file -I your_metadata.csv  # Should show "charset=utf-8"
```

### 2. Required Fields Verification
**Data Items Must Have:**
- ✅ `title` (multilingual recommended)
- ✅ `creator` or `author` (Surname,Givenname format)
- ✅ `type` (COAR resource type URI)
- ✅ `license` (valid license identifier)
- ✅ `date` (W3C-DTF format: YYYY-MM-DD)

**Collections Must Have:**
- ✅ `title` (multilingual recommended)
- ✅ `status` (private/public)

### 3. Critical Format Quick-Check
```bash
# Check for common format issues
grep -E "(^|,)fr:|en:" your_metadata.csv  # Multilingual format
grep -E "http://purl.org/coar/resource_type/" your_metadata.csv  # COAR types
grep -E "[0-9]{4}(-[0-9]{2})?(-[0-9]{2})?" your_metadata.csv  # Date format
```

**🚩 Red Flags**: Stop and fix immediately if found:
- Mixed encoding (non-UTF-8 characters display incorrectly)
- Missing required fields
- Invalid COAR URIs (not starting with http://purl.org/coar/resource_type/)
- Malformed dates (not YYYY, YYYY-MM, or YYYY-MM-DD format)

## Field-by-Field Testing Guide

### Required Fields (Critical Priority)

#### Title Field Testing

**Format Requirements:**
- Single language: `"Simple title"`
- Multilingual: `"fr:Titre français|en:English title"`
- Maximum 250 characters per language
- Minimum 3 characters

**Test Cases:**
```bash
# Create test CSV with various title formats
cat > title_test.csv << 'EOF'
file,title
test1.txt,"Simple English title"
test2.txt,"fr:Titre français|en:English title"  
test3.txt,"fr:Très long titre avec beaucoup de détails spécifiques|en:Very long title with many specific details"
test4.txt,"fr:Titre avec caractères spéciaux éàùç|en:Title with special chars"
test5.txt,"fr:Titre|en:English|es:Español"
EOF

# Validate with preview tool
o-nakala-preview --csv title_test.csv --validate-only
```

**Expected Results:**
- All formats should validate successfully
- Multilingual titles should create multiple metadata entries
- Special characters should be preserved

**Common Errors & Fixes:**
```bash
# ❌ WRONG: Missing language separator
title,"frTitre françaisenEnglish title"

# ✅ CORRECT: Proper multilingual format  
title,"fr:Titre français|en:English title"

# ❌ WRONG: Wrong separator
title,"fr:Français;en:English"

# ✅ CORRECT: Use pipe separator
title,"fr:Français|en:English"
```

#### Creator/Author Field Testing

**Format Requirements:**
- Single: `"Surname,Givenname"`
- Multiple: `"Surname1,Givenname1;Surname2,Givenname2"`
- Organization: `"Organization Name"` (no comma)

**Test Cases:**
```bash
# Create creator validation test
cat > creator_test.csv << 'EOF'
file,creator
test1.txt,"Dupont,Jean"
test2.txt,"Dupont,Jean;Smith,John"
test3.txt,"Einstein"
test4.txt,"Université de Strasbourg"
test5.txt,"García,José-María"
test6.txt,"van der Berg,Johannes"
EOF

# Validate creator parsing
o-nakala-preview --csv creator_test.csv --json-output creator_preview.json
```

**Validation Script:**
```bash
# Check creator format compliance
grep -E '^[^,]*,[^,]*$' creator_test.csv  # Single creator format
grep -E '^[^;]*;[^;]*$' creator_test.csv  # Multiple creators format
```

**Common Errors & Fixes:**
```bash
# ❌ WRONG: First name first
creator,"Jean Dupont"

# ✅ CORRECT: Surname first
creator,"Dupont,Jean"

# ❌ WRONG: Missing comma for person
creator,"Jean Dupont Smith"

# ✅ CORRECT: Use comma for individuals
creator,"Smith,Jean Dupont"
```

#### Type Field Testing (COAR Resource Types)

**Valid COAR URIs:**
- Dataset: `http://purl.org/coar/resource_type/c_ddb1`
- Software: `http://purl.org/coar/resource_type/c_5ce6`
- Text: `http://purl.org/coar/resource_type/c_18cf`
- Image: `http://purl.org/coar/resource_type/c_c513`
- Lecture: `http://purl.org/coar/resource_type/c_8544`

**Validation Test:**
```bash
# Create type validation test
cat > type_test.csv << 'EOF'
file,type
dataset.csv,"http://purl.org/coar/resource_type/c_ddb1"
script.py,"http://purl.org/coar/resource_type/c_5ce6"
paper.pdf,"http://purl.org/coar/resource_type/c_18cf"
image.jpg,"http://purl.org/coar/resource_type/c_c513"
EOF

# Verify COAR URI validity
grep -o "http://purl.org/coar/resource_type/c_[a-z0-9]*" type_test.csv
```

**Interactive Type Selection:**
```bash
# Use preview tool for suggestions
o-nakala-preview --csv type_test.csv --interactive
# Choose option 1: "Get COAR resource type suggestions"
# Enter content hint: "research data analysis scripts"
```

#### License Field Testing

**Common Valid Licenses:**
- Creative Commons: `CC-BY-4.0`, `CC-BY-SA-4.0`, `CC0-1.0`
- Open Source: `MIT`, `GPL-3.0`, `Apache-2.0`
- Rights Reserved: `All Rights Reserved`

**Test Cases:**
```bash
# License validation test
cat > license_test.csv << 'EOF'
file,license
test1.txt,"CC-BY-4.0"
test2.txt,"CC-BY-SA-4.0"
test3.txt,"MIT"
test4.txt,"All Rights Reserved"
EOF

o-nakala-preview --csv license_test.csv --validate-only
```

#### Date Field Testing

**Valid Formats (W3C-DTF):**
- Full date: `2024-03-21`
- Year-month: `2024-03`
- Year only: `2024`

**Test Cases:**
```bash
# Date format validation
cat > date_test.csv << 'EOF'
file,date
test1.txt,"2024-03-21"
test2.txt,"2024-03"
test3.txt,"2024"
test4.txt,"2023-12-31"
EOF

# Validate date parsing
o-nakala-preview --csv date_test.csv --validate-only

# Test invalid dates (should be caught)
cat > invalid_date_test.csv << 'EOF'
file,date
test1.txt,"21/03/2024"
test2.txt,"March 2024"
test3.txt,"invalid-date"
EOF
```

### Optional Fields (Recommended)

#### Description Field Testing

**Format Requirements:**
- Multilingual: `"fr:Description française|en:English description"`
- Minimum 10 characters recommended
- No maximum limit

**Content Quality Test:**
```bash
# Test description completeness
cat > description_test.csv << 'EOF'
file,description
test1.txt,"fr:Scripts pour l'analyse de données de recherche avec documentation complète|en:Scripts for research data analysis with complete documentation"
test2.txt,"fr:Jeu de données collectées lors d'enquêtes terrain 2023-2024|en:Dataset collected during field surveys 2023-2024"
EOF

# Check description length and quality
awk -F',' '{print length($2), $2}' description_test.csv
```

#### Keywords Field Testing

**Format Requirements:**
- Single language: `"keyword1;keyword2;keyword3"`
- Multilingual: `"fr:mot1;mot2;mot3|en:word1;word2;word3"`
- Maximum 10 keywords per language recommended

**Test Cases:**
```bash
# Keywords validation test
cat > keywords_test.csv << 'EOF'
file,keywords
test1.txt,"fr:recherche;données;analyse;statistiques|en:research;data;analysis;statistics"
test2.txt,"fr:code;python;traitement;automatisation|en:code;python;processing;automation"
EOF

# Count keywords per language
grep -o ';' keywords_test.csv | wc -l  # Count separators
```

#### Multilingual Field Testing

**Languages Support:**
- Primary: `fr` (French), `en` (English)
- Extended: `es` (Spanish), `de` (German), `it` (Italian)
- Any ISO 639-1 language code

**Comprehensive Multilingual Test:**
```bash
cat > multilingual_test.csv << 'EOF'
file,title,description,keywords
test1.txt,"fr:Données de recherche|en:Research Data|es:Datos de investigación","fr:Description détaillée|en:Detailed description|es:Descripción detallada","fr:données;recherche|en:data;research|es:datos;investigación"
EOF

o-nakala-preview --csv multilingual_test.csv --json-output multilingual_preview.json

# Verify language parsing in JSON output
jq '.preview_data.entries[0].generated_metadata[] | select(.lang != null) | {lang: .lang, value: .value}' multilingual_preview.json
```

## Common Error Patterns & Fixes

### 1. Encoding Issues

**Problem**: Non-UTF-8 characters display as question marks or boxes.

**Detection:**
```bash
# Check file encoding
file -I your_metadata.csv

# Find problematic characters
grep -P "[\x80-\xFF]" your_metadata.csv
```

**Solution:**
```bash
# Convert to UTF-8
iconv -f iso-8859-1 -t utf-8 your_metadata.csv > your_metadata_utf8.csv

# Or re-save in your CSV editor with UTF-8 encoding
```

### 2. Multilingual Format Errors

**Problem**: Multilingual fields not parsed correctly.

**Common Issues:**
```bash
# ❌ WRONG: Using semicolon separator
title,"fr:Français;en:English"

# ❌ WRONG: Missing colon after language code  
title,"frFrançais|enEnglish"

# ❌ WRONG: Using wrong pipe character
title,"fr:Français‖en:English"  # Using double vertical bar

# ✅ CORRECT: Proper format
title,"fr:Français|en:English"
```

**Validation Regex:**
```bash
# Check multilingual format compliance
grep -E '^[a-z]{2}:[^|]+(\|[a-z]{2}:[^|]+)*$' your_field_values
```

### 3. Creator Name Format Issues

**Problem**: Names not parsed into surname/givenname correctly.

**Detection & Fix:**
```bash
# Find names without commas (potential issues)
grep -v ',' creator_column | grep -v '^$'

# Check for multiple commas (usually wrong)
grep -E ',.*,' creator_column
```

### 4. COAR URI Validation Errors

**Problem**: Invalid or incomplete COAR resource type URIs.

**Validation:**
```bash
# Check for proper COAR URI format
grep -v "http://purl.org/coar/resource_type/c_[a-z0-9]\+" type_column

# Common incorrect patterns:
# ❌ "dataset" → ✅ "http://purl.org/coar/resource_type/c_ddb1"
# ❌ "text" → ✅ "http://purl.org/coar/resource_type/c_18cf"
```

## Advanced Testing Scenarios

### 1. Large Dataset Validation

**Performance Testing:**
```bash
# Test with large CSV file (1000+ entries)
time o-nakala-preview --csv large_dataset.csv --validate-only

# Memory usage monitoring
/usr/bin/time -v o-nakala-preview --csv large_dataset.csv --validate-only
```

**Batch Processing:**
```bash
# Split large CSV into smaller chunks for testing
split -l 100 large_dataset.csv chunk_

# Validate each chunk
for chunk in chunk_*; do
    echo "Validating $chunk..."
    o-nakala-preview --csv "$chunk" --validate-only
done
```

### 2. Edge Case Testing

**Special Characters and Unicode:**
```bash
cat > unicode_test.csv << 'EOF'
file,title,creator,description
test1.txt,"fr:Données avec accents éàùç|en:Data with accents","François,José-María","fr:Description avec « guillemets » et —tirets—|en:Description with quotes and dashes"
test2.txt,"fr:Caractères spéciaux ñáéíóú|en:Special characters","de Souza,João","fr:Texte avec symboles © ® ™|en:Text with symbols"
EOF

o-nakala-preview --csv unicode_test.csv --validate-only
```

**Empty and Null Values:**
```bash
cat > empty_fields_test.csv << 'EOF'
file,title,creator,description,keywords
test1.txt,"Valid Title","Dupont,Jean","","fr:mot1;mot2|en:word1;word2"
test2.txt,"Valid Title","","Valid description",""
test3.txt,"Valid Title","Dupont,Jean",,
EOF

# Should handle gracefully without errors
o-nakala-preview --csv empty_fields_test.csv --validate-only
```

### 3. Stress Testing

**Maximum Field Length Testing:**
```bash
# Generate very long field content
python3 << 'EOF'
import csv

# Create test with maximum length fields
long_title = "fr:" + "Very long title content " * 50 + "|en:" + "Very long English title " * 50
long_desc = "fr:" + "Extremely detailed French description. " * 100 + "|en:" + "Extremely detailed English description. " * 100

with open('stress_test.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file', 'title', 'description'])
    writer.writerow(['test.txt', long_title, long_desc])
EOF

o-nakala-preview --csv stress_test.csv --validate-only
```

## Automated Testing Approaches

### 1. Python Validation Script

Create a comprehensive validation script:

```python
#!/usr/bin/env python3
"""
Automated CSV metadata validation script for O-Nakala Core.
Performs comprehensive field-by-field validation with detailed reporting.
"""

import csv
import re
import sys
from pathlib import Path

def validate_csv_metadata(csv_file):
    """Comprehensive CSV metadata validation."""
    
    errors = []
    warnings = []
    info = []
    
    # Field validation patterns
    patterns = {
        'title': r'^.{3,250}$',  # 3-250 characters
        'multilingual': r'^([a-z]{2}:[^|]+(\|[a-z]{2}:[^|]+)*|[^|]+)$',
        'creator': r'^([^,]+,[^,]+|[^,;]+)(;([^,]+,[^,]+|[^,;]+))*$',
        'coar_uri': r'^http://purl\.org/coar/resource_type/c_[a-z0-9]+$',
        'date': r'^(\d{4}|\d{4}-\d{2}|\d{4}-\d{2}-\d{2})$',
        'license': r'^(CC-BY-4\.0|CC-BY-SA-4\.0|CC0-1\.0|MIT|GPL-3\.0|Apache-2\.0|All Rights Reserved)$'
    }
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                
                # Check required fields
                required_fields = ['title', 'creator', 'type', 'license', 'date']
                for field in required_fields:
                    if not row.get(field) or row[field].strip() == '':
                        errors.append(f"Row {row_num}: Missing required field '{field}'")
                
                # Validate title
                if row.get('title'):
                    if not re.match(patterns['title'], row['title']):
                        errors.append(f"Row {row_num}: Title length must be 3-250 characters")
                    
                    if '|' in row['title'] and not re.match(patterns['multilingual'], row['title']):
                        errors.append(f"Row {row_num}: Invalid multilingual title format")
                
                # Validate creator
                if row.get('creator') and not re.match(patterns['creator'], row['creator']):
                    errors.append(f"Row {row_num}: Invalid creator format (use 'Surname,Givenname')")
                
                # Validate COAR URI
                if row.get('type') and not re.match(patterns['coar_uri'], row['type']):
                    errors.append(f"Row {row_num}: Invalid COAR resource type URI")
                
                # Validate date
                if row.get('date') and not re.match(patterns['date'], row['date']):
                    errors.append(f"Row {row_num}: Invalid date format (use YYYY-MM-DD, YYYY-MM, or YYYY)")
                
                # Validate license
                if row.get('license') and not re.match(patterns['license'], row['license']):
                    warnings.append(f"Row {row_num}: Unusual license '{row['license']}' - verify validity")
    
    except UnicodeDecodeError:
        errors.append("File encoding error - ensure UTF-8 encoding")
    except Exception as e:
        errors.append(f"File processing error: {str(e)}")
    
    return errors, warnings, info

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 validate_csv.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    errors, warnings, info = validate_csv_metadata(csv_file)
    
    print(f"Validation Results for {csv_file}")
    print("=" * 50)
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  • {error}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  • {warning}")
    
    if not errors and not warnings:
        print("\n✅ All validation checks passed!")
    
    # Exit code for automation
    sys.exit(1 if errors else 0)
```

**Usage:**
```bash
# Save as validate_csv.py and make executable
python3 validate_csv.py your_metadata.csv

# Use in automation
if python3 validate_csv.py metadata.csv; then
    echo "Validation passed, proceeding with upload"
    o-nakala-upload --csv metadata.csv
else
    echo "Validation failed, fix errors before upload"
fi
```

### 2. Bash Validation Functions

```bash
#!/bin/bash
# CSV validation functions for shell scripts

validate_encoding() {
    local csv_file="$1"
    if ! file -I "$csv_file" | grep -q "charset=utf-8"; then
        echo "❌ ERROR: File is not UTF-8 encoded"
        return 1
    fi
    echo "✅ Encoding: UTF-8"
    return 0
}

validate_required_columns() {
    local csv_file="$1"
    local required_cols=("title" "creator" "type" "license" "date")
    
    header=$(head -n1 "$csv_file")
    
    for col in "${required_cols[@]}"; do
        if ! echo "$header" | grep -q "$col"; then
            echo "❌ ERROR: Missing required column '$col'"
            return 1
        fi
    done
    echo "✅ All required columns present"
    return 0
}

validate_coar_uris() {
    local csv_file="$1"
    local invalid_types
    
    invalid_types=$(awk -F',' 'NR>1 {print $3}' "$csv_file" | 
                   grep -v "^http://purl.org/coar/resource_type/c_" | 
                   grep -v "^$")
    
    if [[ -n "$invalid_types" ]]; then
        echo "❌ ERROR: Invalid COAR URIs found:"
        echo "$invalid_types"
        return 1
    fi
    echo "✅ All COAR URIs valid"
    return 0
}

# Main validation function
full_validation() {
    local csv_file="$1"
    local errors=0
    
    echo "Validating $csv_file..."
    echo "========================"
    
    validate_encoding "$csv_file" || ((errors++))
    validate_required_columns "$csv_file" || ((errors++))
    validate_coar_uris "$csv_file" || ((errors++))
    
    if [[ $errors -eq 0 ]]; then
        echo -e "\n🎉 All validations passed!"
        return 0
    else
        echo -e "\n💥 $errors validation errors found"
        return 1
    fi
}

# Usage: full_validation your_metadata.csv
```

### 3. Continuous Validation Pipeline

**Pre-commit Hook:**
```bash
#!/bin/bash
# .git/hooks/pre-commit
# Validates CSV files before commit

csv_files=$(git diff --cached --name-only | grep '\.csv$')

if [[ -n "$csv_files" ]]; then
    echo "Validating CSV files before commit..."
    
    for csv_file in $csv_files; do
        if [[ -f "$csv_file" ]]; then
            echo "Validating $csv_file..."
            o-nakala-preview --csv "$csv_file" --validate-only
            if [[ $? -ne 0 ]]; then
                echo "❌ Validation failed for $csv_file"
                echo "Fix validation errors before committing."
                exit 1
            fi
        fi
    done
    
    echo "✅ All CSV files validated successfully"
fi
```

## Quality Assurance Checklist

### Pre-Upload Final Checklist

Print this checklist and verify each item:

#### ✅ File Structure
- [ ] File is UTF-8 encoded
- [ ] CSV structure is valid (no malformed rows)
- [ ] All rows have same number of columns
- [ ] No empty rows in middle of data

#### ✅ Required Fields (Data Items)
- [ ] `title` present and 3+ characters
- [ ] `creator` in "Surname,Givenname" format
- [ ] `type` is valid COAR URI starting with "http://purl.org/coar/resource_type/"
- [ ] `license` is recognized license identifier
- [ ] `date` in W3C-DTF format (YYYY-MM-DD, YYYY-MM, or YYYY)

#### ✅ Required Fields (Collections)
- [ ] `title` present and meaningful
- [ ] `status` is "private" or "public"

#### ✅ Multilingual Fields
- [ ] Format follows "fr:French|en:English" pattern
- [ ] Language codes are ISO 639-1 standard
- [ ] No empty language segments
- [ ] Pipe separator (|) used correctly

#### ✅ Content Quality
- [ ] Titles are descriptive and meaningful
- [ ] Descriptions explain content purpose and methodology
- [ ] Keywords are relevant and specific
- [ ] Creator names are complete and accurate
- [ ] All multilingual content is properly translated

#### ✅ Technical Validation
- [ ] Preview tool validates without errors: `o-nakala-preview --csv file.csv --validate-only`
- [ ] Enhanced preview generates expected metadata: `o-nakala-preview --csv file.csv --enhance`
- [ ] JSON output is well-formed: `o-nakala-preview --csv file.csv --json-output preview.json`

### Pre-Production Testing

Before uploading to production NAKALA:

```bash
# 1. Test with NAKALA test environment first
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_API_URL="https://apitest.nakala.fr"

# 2. Small batch test (first 3 rows only)
head -n4 your_metadata.csv > test_batch.csv  # Header + 3 data rows

# 3. Upload test batch
o-nakala-upload \
  --api-key "$NAKALA_API_KEY" \
  --dataset test_batch.csv \
  --base-path "." \
  --mode folder \
  --output test_results.csv \
  --dry-run

# 4. Verify test results
if [[ $? -eq 0 ]]; then
    echo "✅ Test batch successful - ready for full upload"
else
    echo "❌ Test batch failed - review and fix errors"
fi
```

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: "Invalid multilingual format" Error

**Symptoms:**
```
❌ ERROR: Row 5: Invalid multilingual title format
```

**Diagnosis:**
```bash
# Check the problematic row
sed -n '5p' your_metadata.csv

# Look for common issues:
grep -E '[^|]*\|[^|]*' your_metadata.csv  # Check pipe separators
grep -E '[a-z]{2}:[^|]*' your_metadata.csv  # Check language codes
```

**Solutions:**
- Use `|` (pipe) not `;` (semicolon) to separate languages
- Ensure format is exactly `fr:French text|en:English text`
- No spaces around the pipe separator
- Check that language codes are lowercase

#### Issue: "Creator format validation failed"

**Symptoms:**
```
❌ ERROR: Row 3: Invalid creator format (use 'Surname,Givenname')
```

**Solutions:**
```bash
# Check creator format
# ❌ WRONG formats:
"Jean Dupont"              # → "Dupont,Jean"
"Dupont, Jean"             # → "Dupont,Jean" (no space after comma)
"Dr. Jean Dupont"          # → "Dupont,Jean" (no titles)

# ✅ CORRECT formats:
"Dupont,Jean"              # Single person
"Dupont,Jean;Smith,John"   # Multiple people
"CNRS"                     # Organization (no comma)
```

#### Issue: "COAR URI validation error"

**Symptoms:**
```
❌ ERROR: Invalid COAR resource type URI
```

**Quick Fix Reference:**
```bash
# Common content types → Correct COAR URIs:
"dataset"    → "http://purl.org/coar/resource_type/c_ddb1"
"software"   → "http://purl.org/coar/resource_type/c_5ce6"  
"text"       → "http://purl.org/coar/resource_type/c_18cf"
"image"      → "http://purl.org/coar/resource_type/c_c513"
"slides"     → "http://purl.org/coar/resource_type/c_8544"
```

#### Issue: "Encoding problems with special characters"

**Symptoms:** Special characters display as `�` or `?` in output.

**Solutions:**
```bash
# 1. Check current encoding
file -I your_metadata.csv

# 2. Convert to UTF-8 if needed
iconv -f iso-8859-1 -t utf-8 your_metadata.csv > your_metadata_utf8.csv

# 3. Verify in text editor
# - Open file in text editor
# - Check that accented characters display correctly
# - Save as UTF-8 if necessary
```

#### Issue: Performance problems with large CSV files

**Symptoms:** Validation takes very long or runs out of memory.

**Solutions:**
```bash
# 1. Split into smaller chunks
split -l 500 large_dataset.csv chunk_

# 2. Validate chunks separately  
for chunk in chunk_*; do
    o-nakala-preview --csv "$chunk" --validate-only
done

# 3. Use streaming validation (future enhancement)
# Monitor memory usage during validation
/usr/bin/time -v o-nakala-preview --csv large_dataset.csv --validate-only
```

### Emergency Fixes

#### Quick Multilingual Conversion

Convert single-language fields to multilingual:

```bash
# Convert English titles to bilingual
sed -i.bak 's/title,"\([^"]*\)"/title,"fr:\1|en:\1"/' your_metadata.csv
```

#### Bulk COAR URI Fix

Replace common type names with proper URIs:

```bash
# Fix common type values
sed -i.bak 's/type,"dataset"/type,"http:\/\/purl.org\/coar\/resource_type\/c_ddb1"/' your_metadata.csv
sed -i.bak 's/type,"software"/type,"http:\/\/purl.org\/coar\/resource_type\/c_5ce6"/' your_metadata.csv
sed -i.bak 's/type,"text"/type,"http:\/\/purl.org\/coar\/resource_type\/c_18cf"/' your_metadata.csv
```

#### Creator Format Normalization

```bash
# Fix "Firstname Lastname" to "Lastname,Firstname" format
# (Use carefully - verify results manually)
sed -i.bak -E 's/creator,"([A-Z][a-z]+) ([A-Z][a-z]+)"/creator,"\2,\1"/' your_metadata.csv
```

### Getting Help

When validation issues persist:

1. **Run comprehensive validation:**
   ```bash
   o-nakala-preview --csv your_metadata.csv --interactive
   # Choose option 3: "Validate field values in detail"
   ```

2. **Generate detailed error report:**
   ```bash
   o-nakala-preview --csv your_metadata.csv --json-output full_report.json
   # Review JSON for specific field issues
   ```

3. **Test with sample data:**
   ```bash
   # Compare your format with working sample
   o-nakala-preview --csv examples/sample_dataset/folder_data_items.csv --validate-only
   ```

4. **Check documentation:**
   - [Curator Field Reference](docs/curator-field-reference.md) - Complete field specifications
   - [Upload Guide](docs/user-guides/01-upload-guide.md) - Upload procedures
   - [Troubleshooting](docs/user-guides/05-troubleshooting.md) - Common issues

This comprehensive testing guide ensures your metadata meets all NAKALA requirements before upload. By following these validation procedures systematically, you can achieve 100% upload success rates and maintain high metadata quality standards for your research data repository.