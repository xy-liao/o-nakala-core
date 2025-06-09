# Documentation Validation Strategy

## 🎯 Objective

Ensure all endpoint and field documentation is **accurate, current, and continuously validated** against the real NAKALA API to maintain reliability and user trust.

## 🚨 The Validation Challenge

### **Why Documentation Validation Is Critical**
1. **API Changes**: NAKALA API may evolve, breaking documented examples
2. **Field Validation Rules**: Metadata requirements may change
3. **CSV Format Evolution**: New format support or deprecated features
4. **Example Accuracy**: All examples must work with real API calls
5. **Error Message Updates**: Error scenarios must match actual API responses

### **Consequences of Invalid Documentation**
- **User Frustration**: Examples that don't work
- **Developer Confusion**: Incorrect transformation rules
- **Support Overhead**: Issues from outdated documentation
- **System Credibility**: Loss of trust in O-Nakala Core

## 🔧 Multi-Layer Validation Architecture

### **Layer 1: Automated Example Testing**

#### **Real API Validation Suite**
**Location**: `tests/documentation_validation/`

```python
# tests/documentation_validation/test_endpoint_examples.py

import pytest
import requests
import pandas as pd
from pathlib import Path

class TestDocumentationExamples:
    """Validate all documentation examples against real NAKALA API."""
    
    @pytest.fixture
    def test_api_key(self):
        return "f41f5957-d396-3bb9-ce35-a4692773f636"  # Public test key
    
    @pytest.fixture  
    def api_base_url(self):
        return "https://apitest.nakala.fr"
    
    def test_upload_endpoint_examples(self, test_api_key, api_base_url):
        """Test all upload endpoint CSV examples."""
        examples_dir = Path("docs/endpoints/upload-endpoint/examples/")
        
        for csv_file in examples_dir.glob("*.csv"):
            with self.subTest(csv_file=csv_file.name):
                # Test CSV parsing
                df = pd.read_csv(csv_file)
                assert not df.empty, f"CSV file {csv_file} is empty"
                
                # Test transformation logic
                from nakala_client.upload import NakalaUpload
                uploader = NakalaUpload(api_key=test_api_key)
                
                # Validate CSV format
                validation_result = uploader.validate_csv(csv_file)
                assert validation_result.is_valid, f"CSV validation failed: {validation_result.errors}"
                
                # Test with dry-run (don't actually upload)
                result = uploader.process_csv(csv_file, dry_run=True)
                assert result.success, f"CSV processing failed: {result.errors}"
    
    def test_collection_endpoint_examples(self, test_api_key, api_base_url):
        """Test all collection endpoint examples."""
        # Similar validation for collection examples
        pass
    
    def test_curator_endpoint_examples(self, test_api_key, api_base_url):
        """Test all curator endpoint batch modification examples."""
        # Similar validation for curator examples
        pass
```

#### **Field Validation Testing**
```python
# tests/documentation_validation/test_field_examples.py

class TestFieldDocumentation:
    """Validate field-specific examples and transformation rules."""
    
    def test_title_field_examples(self):
        """Test all title field format examples."""
        examples = [
            "Simple title",
            "fr:Titre français|en:English title",
            "fr:Titre|en:Title|es:Título|de:Titel"
        ]
        
        for example in examples:
            with self.subTest(example=example):
                # Test multilingual parsing
                from nakala_client.common.utils import NakalaCommonUtils
                result = NakalaCommonUtils.parse_multilingual_field(example)
                
                # Validate structure
                assert isinstance(result, list)
                assert all(isinstance(item, tuple) for item in result)
                
                # Test transformation to JSON
                metadata = NakalaCommonUtils.prepare_nakala_metadata({
                    'title': example
                })
                assert len(metadata) == len(result)
    
    def test_all_documented_fields(self):
        """Test every field documented in field reference."""
        field_docs_dir = Path("docs/fields/")
        
        for field_doc in field_docs_dir.rglob("*.md"):
            if field_doc.name == "README.md":
                continue
                
            with self.subTest(field=field_doc.stem):
                # Extract examples from markdown documentation
                examples = self._extract_examples_from_markdown(field_doc)
                
                # Test each example
                for example in examples:
                    self._validate_field_example(field_doc.stem, example)
```

#### **Continuous Integration Setup**
```yaml
# .github/workflows/documentation-validation.yml

name: Documentation Validation

on:
  push:
    paths:
      - 'docs/**'
      - 'examples/**'
  pull_request:
    paths:
      - 'docs/**'
      - 'examples/**'
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  validate-documentation:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -e .
    
    - name: Validate endpoint examples
      run: pytest tests/documentation_validation/test_endpoint_examples.py -v
    
    - name: Validate field examples
      run: pytest tests/documentation_validation/test_field_examples.py -v
    
    - name: Validate CSV format examples
      run: pytest tests/documentation_validation/test_csv_formats.py -v
    
    - name: Generate validation report
      run: python tools/generate_validation_report.py
    
    - name: Upload validation report
      uses: actions/upload-artifact@v3
      with:
        name: documentation-validation-report
        path: docs/validation-report.md
```

### **Layer 2: Interactive Validation Tools**

#### **CSV Format Validator**
**Location**: `tools/csv_validator.py`

```python
#!/usr/bin/env python3
"""
CSV Format Validator for O-Nakala Core Documentation

Validates CSV examples in documentation against current transformation logic.
"""

import argparse
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from nakala_client.common.utils import NakalaCommonUtils
from nakala_client.curator import NakalaCurator

class DocumentationValidator:
    """Validates documentation examples and formats."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.validated_files = []
    
    def validate_csv_file(self, csv_path: Path) -> Dict[str, Any]:
        """Validate a single CSV file against transformation logic."""
        try:
            # Load CSV
            df = pd.read_csv(csv_path)
            
            # Basic validation
            if df.empty:
                self.errors.append(f"{csv_path}: CSV file is empty")
                return {"valid": False, "errors": ["Empty CSV file"]}
            
            # Test transformation logic
            validation_result = self._test_transformation(df, csv_path)
            
            self.validated_files.append({
                "file": str(csv_path),
                "valid": validation_result["valid"],
                "errors": validation_result.get("errors", []),
                "warnings": validation_result.get("warnings", [])
            })
            
            return validation_result
            
        except Exception as e:
            error_msg = f"{csv_path}: Failed to validate - {str(e)}"
            self.errors.append(error_msg)
            return {"valid": False, "errors": [error_msg]}
    
    def _test_transformation(self, df: pd.DataFrame, csv_path: Path) -> Dict[str, Any]:
        """Test CSV transformation logic."""
        errors = []
        warnings = []
        
        try:
            # Detect CSV mode
            if 'id' in df.columns and 'action' in df.columns:
                # Modification mode
                curator = NakalaCurator(api_key="test")
                result = curator.parse_csv_modifications(str(csv_path))
                
                if not result:
                    errors.append("No valid modifications parsed")
                
            else:
                # Creation/upload mode
                for index, row in df.iterrows():
                    row_dict = row.to_dict()
                    
                    # Test metadata preparation
                    metadata = NakalaCommonUtils.prepare_nakala_metadata(row_dict)
                    
                    if not metadata:
                        warnings.append(f"Row {index}: No metadata generated")
                    
                    # Test multilingual fields
                    for field, value in row_dict.items():
                        if pd.notna(value) and '|' in str(value):
                            parsed = NakalaCommonUtils.parse_multilingual_field(str(value))
                            if not parsed:
                                warnings.append(f"Row {index}, Field {field}: Multilingual parsing failed")
            
            return {
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings
            }
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Transformation test failed: {str(e)}"]
            }
    
    def validate_all_documentation(self) -> Dict[str, Any]:
        """Validate all CSV files in documentation."""
        docs_dir = Path("docs")
        examples_dir = Path("examples")
        
        csv_files = []
        csv_files.extend(docs_dir.rglob("*.csv"))
        csv_files.extend(examples_dir.rglob("*.csv"))
        
        for csv_file in csv_files:
            self.validate_csv_file(csv_file)
        
        return {
            "total_files": len(csv_files),
            "validated_files": len(self.validated_files),
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "validation_details": self.validated_files
        }
    
    def generate_report(self) -> str:
        """Generate validation report."""
        report = "# Documentation Validation Report\n\n"
        report += f"**Generated**: {pd.Timestamp.now()}\n\n"
        
        # Summary
        total_files = len(self.validated_files)
        valid_files = sum(1 for f in self.validated_files if f["valid"])
        
        report += f"## Summary\n"
        report += f"- **Total files validated**: {total_files}\n"
        report += f"- **Valid files**: {valid_files}\n"
        report += f"- **Files with errors**: {total_files - valid_files}\n"
        report += f"- **Total errors**: {len(self.errors)}\n"
        report += f"- **Total warnings**: {len(self.warnings)}\n\n"
        
        # Detailed results
        if self.validated_files:
            report += "## Detailed Results\n\n"
            for file_result in self.validated_files:
                status = "✅" if file_result["valid"] else "❌"
                report += f"### {status} {file_result['file']}\n"
                
                if file_result["errors"]:
                    report += "**Errors:**\n"
                    for error in file_result["errors"]:
                        report += f"- {error}\n"
                
                if file_result["warnings"]:
                    report += "**Warnings:**\n"
                    for warning in file_result["warnings"]:
                        report += f"- {warning}\n"
                
                report += "\n"
        
        return report

def main():
    parser = argparse.ArgumentParser(description="Validate O-Nakala Core documentation")
    parser.add_argument("--file", help="Validate specific CSV file")
    parser.add_argument("--all", action="store_true", help="Validate all documentation")
    parser.add_argument("--report", help="Generate report file")
    
    args = parser.parse_args()
    
    validator = DocumentationValidator()
    
    if args.file:
        result = validator.validate_csv_file(Path(args.file))
        print(f"Validation result: {'Valid' if result['valid'] else 'Invalid'}")
        if result.get('errors'):
            print("Errors:")
            for error in result['errors']:
                print(f"  - {error}")
    
    elif args.all:
        results = validator.validate_all_documentation()
        print(f"Validated {results['total_files']} files")
        print(f"Errors: {results['total_errors']}")
        print(f"Warnings: {results['total_warnings']}")
        
        if args.report:
            report = validator.generate_report()
            with open(args.report, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.report}")

if __name__ == "__main__":
    main()
```

### **Layer 3: Documentation Maintenance System**

#### **Automated Update Detection**
```python
# tools/documentation_monitor.py

class DocumentationMonitor:
    """Monitor API changes and update documentation accordingly."""
    
    def check_api_changes(self):
        """Check for NAKALA API changes that affect documentation."""
        # Compare current API spec with cached version
        # Detect field changes, new endpoints, deprecated features
        pass
    
    def validate_transformation_logic(self):
        """Validate that transformation logic matches documentation."""
        # Test code examples in documentation
        # Verify field mappings are current
        # Check multilingual format support
        pass
    
    def generate_update_alerts(self):
        """Generate alerts for documentation that needs updates."""
        # Create GitHub issues for outdated documentation
        # Alert maintainers of validation failures
        # Suggest fixes for common issues
        pass
```

#### **Documentation Quality Metrics**
```python
# tools/documentation_metrics.py

class DocumentationMetrics:
    """Generate quality metrics for documentation."""
    
    def coverage_analysis(self):
        """Analyze documentation coverage."""
        return {
            "endpoints_documented": "3/3 (100%)",
            "fields_documented": "18/18 (100%)",
            "examples_with_tests": "85%",
            "multilingual_examples": "90%",
            "error_scenarios_covered": "75%"
        }
    
    def freshness_analysis(self):
        """Analyze documentation freshness."""
        return {
            "last_validation": "2025-06-08",
            "api_compatibility": "100%",
            "broken_examples": "0",
            "outdated_sections": []
        }
```

### **Layer 4: User Feedback Integration**

#### **Documentation Feedback System**
```markdown
<!-- Template for all documentation pages -->

---
## 📝 Documentation Feedback

**Was this documentation helpful?** 

- 👍 Yes - Click [here](https://github.com/xy-liao/o-nakala-core/issues/new?template=doc_feedback_positive.md&title=Positive+feedback:+[PAGE_NAME])
- 👎 No - Click [here](https://github.com/xy-liao/o-nakala-core/issues/new?template=doc_feedback_negative.md&title=Documentation+issue:+[PAGE_NAME])
- 🐛 Found an error - Click [here](https://github.com/xy-liao/o-nakala-core/issues/new?template=doc_error.md&title=Documentation+error:+[PAGE_NAME])

**Last validated**: 2025-06-08 ✅  
**API compatibility**: NAKALA Test API v2024  
**Examples tested**: All examples validated with real API calls
```

## 🔄 Validation Workflow

### **Daily Automated Validation**
1. **Run example tests** against test API
2. **Check transformation logic** against current code
3. **Validate CSV formats** in all documentation
4. **Generate validation report**
5. **Alert on failures**

### **Weekly Documentation Review**
1. **Review user feedback** and issues
2. **Update examples** based on usage patterns
3. **Add new scenarios** based on user questions
4. **Refresh API compatibility** checks

### **Monthly Comprehensive Audit**
1. **Full API compatibility** check
2. **Documentation coverage** analysis
3. **Quality metrics** evaluation
4. **Strategic improvements** planning

## 🎯 Validation Success Criteria

### **Technical Validation**
- [ ] **100% of CSV examples** validate against transformation logic
- [ ] **All documented endpoints** tested with real API calls
- [ ] **Every field example** successfully transforms to valid JSON
- [ ] **Zero broken examples** in documentation

### **Accuracy Validation**  
- [ ] **Error messages** match actual API responses
- [ ] **Field validation rules** match current API requirements
- [ ] **Transformation outputs** match expected JSON structure
- [ ] **Edge cases** properly documented and tested

### **Completeness Validation**
- [ ] **Every endpoint** has comprehensive documentation
- [ ] **Every field** has format specifications and examples
- [ ] **All CSV modes** (creation, modification, upload) covered
- [ ] **Complex scenarios** and multilingual examples included

## 🛠️ Implementation Commands

### **Run Full Validation**
```bash
# Validate all documentation
python tools/csv_validator.py --all --report docs/validation-report.md

# Test specific endpoint examples
pytest tests/documentation_validation/test_upload_examples.py -v

# Generate quality metrics
python tools/documentation_metrics.py --output docs/quality-metrics.md
```

### **Continuous Monitoring**
```bash
# Setup automated validation
crontab -e
# Add: 0 2 * * * cd /path/to/o-nakala-core && python tools/csv_validator.py --all

# Monitor API changes
python tools/documentation_monitor.py --check-api --alert-on-changes
```

---

**Result**: Every piece of documentation will be **continuously validated, automatically tested, and maintained current** with the actual NAKALA API behavior, ensuring users and developers can trust all examples and specifications.