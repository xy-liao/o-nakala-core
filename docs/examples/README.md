# 📖 O-Nakala Core Examples

## Overview

This directory contains practical examples for extending O-Nakala Core with custom properties, workflows, and institutional configurations.

## Quick Start Examples

### 🎯 **Basic Custom Field Mapping**
**File**: [`custom-field-mapping.py`](custom-field-mapping.py)  
**Purpose**: Simple example showing how to add custom research properties  
**Time**: 5 minutes  
**Use Case**: Individual researcher with specific metadata needs

```bash
PYTHONPATH=src python docs/examples/custom-field-mapping.py
```

**What it demonstrates:**
- Adding custom properties like `funding_agency`, `ethics_approval`
- Mixing NAKALA, Dublin Core, and custom ontology properties
- Handling multilingual custom fields
- Processing COAR types not in predefined suggestions

### 🏛️ **Institutional Workflow** 
**File**: [`institutional-workflow.py`](institutional-workflow.py)  
**Purpose**: Complete institutional solution with enhanced validation  
**Time**: 15 minutes  
**Use Case**: Research institutions, labs, or collaborative projects

```bash
PYTHONPATH=src python docs/examples/institutional-workflow.py
```

**What it demonstrates:**
- 21 custom research-specific properties
- Enhanced validation with custom field mapping
- CSV template generation for different research domains
- Professional-grade metadata processing pipeline

## CSV Templates

### Available Templates

| Template | Description | Use Case | Fields |
|----------|-------------|----------|---------|
| `research-study.csv` | General research study | Social sciences, surveys | 15+ fields |
| `clinical-trial.csv` | Clinical research data | Medical research | 12+ fields |
| `humanities-project.csv` | Humanities research | History, literature, culture | 10+ fields |

### Creating Custom Templates

```python
from docs.examples.institutional_workflow import CustomResearchMetadata

processor = CustomResearchMetadata()

# Create template for your domain
processor.create_custom_csv_template(
    "my_research_template.csv", 
    "research_study"  # or "clinical_trial"
)
```

## Extension Patterns

### Pattern 1: Simple Property Addition
```python
custom_mapping = {
    "title": "http://nakala.fr/terms#title",
    "my_field": "http://myinstitution.org/terms#my_field"
}
```

### Pattern 2: Ontology Integration
```python
# Using existing ontologies
"methodology": "http://purl.org/spar/pwo/methodology",
"funding": "http://purl.org/cerif/frapo/funds",
"location": "http://www.w3.org/2003/01/geo/wgs84_pos#"
```

### Pattern 3: Multi-Institutional Collaboration
```python
# Shared namespace for consortium
"consortium_id": "http://research-consortium.org/terms#project_id",
"partner_institution": "http://research-consortium.org/terms#partner",
"work_package": "http://research-consortium.org/terms#work_package"
```

## Integration with Preview Tool

### Basic Integration
```python
from o_nakala_core.common.utils import NakalaCommonUtils

utils = NakalaCommonUtils()
result = utils.prepare_nakala_metadata(your_data, custom_mapping)
```

### Enhanced Integration  
```python
from docs.examples.institutional_workflow import CustomResearchMetadata

processor = CustomResearchMetadata()
results = processor.validate_and_preview_csv("your_data.csv")
```

## Testing Your Extensions

```bash
# Test basic extension
PYTHONPATH=src python -c "
from docs.examples.custom_field_mapping import *
extended_metadata_processing()
"

# Test institutional workflow  
PYTHONPATH=src python docs/examples/institutional-workflow.py

# Run comprehensive validation
PYTHONPATH=src python -m pytest tests/unit/csv_validation/ -v
```

## Common Use Cases & Solutions

### **Use Case 1: Adding Grant Information**
```python
grant_fields = {
    "funding_agency": "http://research.org/funding#agency",
    "grant_number": "http://research.org/funding#grant_number", 
    "grant_period": "http://research.org/funding#period",
    "budget": "http://research.org/funding#budget_allocated"
}
```

### **Use Case 2: Clinical Research Metadata**
```python
clinical_fields = {
    "trial_registration": "http://clinical.org/terms#trial_registration",
    "primary_outcome": "http://clinical.org/terms#primary_outcome",
    "intervention": "http://clinical.org/terms#intervention",
    "adverse_events": "http://clinical.org/terms#adverse_events"
}
```

### **Use Case 3: Digital Humanities**
```python
humanities_fields = {
    "historical_period": "http://humanities.org/temporal#period",
    "cultural_context": "http://humanities.org/context#cultural",
    "manuscript_source": "http://humanities.org/source#manuscript",
    "transcription_method": "http://humanities.org/method#transcription"
}
```

## Best Practices

### ✅ **Property URI Design**
- Use established ontologies when possible (Dublin Core, FOAF, etc.)
- Create institution namespace: `http://yourinstitution.edu/terms#`
- Use descriptive, consistent naming conventions

### ✅ **Multilingual Support**
```python
# Always support multilingual values
"title": "fr:Titre français|en:English title",
"methodology": "fr:Méthodologie qualitative|en:Qualitative methodology"
```

### ✅ **Data Type Handling**
```python
# Let the system handle type inference or specify explicitly
date_fields = ["date", "created", "embargo_date"]  # Auto: XSD date
uri_fields = ["type", "identifier", "related_work"]  # Auto: XSD anyURI
```

### ✅ **Testing & Validation**
- Always test custom mappings with preview tool
- Validate with actual NAKALA API in test environment
- Use comprehensive test framework for production

## Next Steps

1. **Try Basic Example**: Run `custom-field-mapping.py`
2. **Customize for Your Domain**: Modify property mappings
3. **Create Templates**: Generate CSV templates for your team
4. **Integrate with Workflow**: Use in complete upload/organize/curate cycle
5. **Scale Institutionally**: Deploy `institutional-workflow.py` for team use

---

*For questions or contributions, see main repository documentation.*