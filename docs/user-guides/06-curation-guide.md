# Curation Guide

**Version 2.4.3+ Feature** - Metadata curation with automated analysis and community features.

## 🔬 Overview

O-Nakala Core v2.4.3 provides metadata curation capabilities that help improve data quality through automated analysis, pattern recognition, and community knowledge integration.

## 🚀 Quick Start

### Installation with Curation Features
```bash
# Install with curation capabilities
pip install o-nakala-core[ml]

# Or complete installation
pip install o-nakala-core[cli,ml]
```

### Basic Curation Workflow
```bash
# Curator with automated features
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --scope all \
  --output quality_report.json

# The curator includes:
# - Pattern analysis
# - Community intelligence insights
# - Automatic relationship discovery
# - Smart field suggestions
```

## 🔧 Automated Features in Detail

### 1. Pattern Learning

The system discovers metadata patterns from your existing data and the broader NAKALA community.

**What it analyzes:**
- Field correlation patterns (e.g., certain keywords → specific licenses)
- Content type classification patterns
- User workflow patterns
- Temporal patterns in metadata evolution

**Automatic integration:**
- Patterns are analyzed in the background during curator operations
- No additional CLI commands needed
- Results improve over time as more data is processed

### 2. Community Intelligence

Leverages community knowledge to provide better metadata suggestions.

**Features:**
- Community pattern analysis across NAKALA users
- Best practice recommendations based on successful datasets
- Quality benchmarking against similar resources
- Trend analysis for emerging metadata standards

**Usage:**
```bash
# Quality reports now include community insights
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --scope collections
```

The quality report will include:
- Community comparison metrics
- Suggested improvements based on similar successful datasets
- Trend analysis for your field of research

### 3. Intelligent Pre-population

Context-aware metadata suggestions based on file content, user history, and community patterns.

**Auto-detection capabilities:**
- File type analysis → appropriate metadata schemas
- Content analysis → keyword and description suggestions
- User context → personalized field suggestions
- License recommendations based on content type and institution

**Integration:**
Pre-population works automatically during upload and curation workflows. The system analyzes:
- File names and extensions
- File content (when appropriate)
- User's previous metadata patterns
- Institutional context
- Community best practices

### 4. Relationship Discovery

Automatically finds connections between your resources and suggests relationships.

**Discovery types:**
- Content similarity analysis
- Temporal relationships (versions, updates)
- Thematic connections
- Citation and reference relationships
- Collection membership suggestions

**Automatic suggestions:**
The system suggests relationship metadata such as:
- `isPartOf` relationships for collection membership
- `references` for citation relationships  
- `isVersionOf` for version control
- `relation` for thematic connections

### 5. Predictive Analytics

AI-driven predictions for metadata field values and quality improvements.

**Predictions include:**
- Missing field suggestions
- Value corrections for consistency
- Quality score predictions
- Completion time estimates for metadata enhancement

## 🎯 Enhanced Workflow Example

### Traditional Workflow (v2.4.3)
```bash
# 1. Upload data
o-nakala-upload --api-key "$KEY" --dataset data.csv --mode csv

# 2. Create collections manually
o-nakala-collection --api-key "$KEY" --title "My Collection"

# 3. Manual quality check
o-nakala-curator --api-key "$KEY" --quality-report
```

### Automated Enhancement Workflow (v2.4.3)
```bash
# 1. Upload with intelligent pre-population
o-nakala-upload --api-key "$KEY" --dataset data.csv --mode csv
# → Automated system suggests metadata improvements during upload

# 2. Collections with relationship discovery
o-nakala-collection --api-key "$KEY" --from-upload-output results.csv
# → AI suggests collection relationships and optimizations

# 3. Intelligent quality analysis
o-nakala-curator --api-key "$KEY" --quality-report --scope all
# → AI provides:
#   - Community benchmarking
#   - Predictive quality scores
#   - Relationship suggestions
#   - Pattern-based improvements
```

## 📊 Understanding AI Output

### Quality Reports with AI Insights

The enhanced quality reports include new sections:

```json
{
  "ai_insights": {
    "pattern_analysis": {
      "discovered_patterns": 15,
      "confidence_score": 0.87,
      "suggestions": [...]
    },
    "community_comparison": {
      "percentile": 78,
      "similar_datasets": 142,
      "best_practices": [...]
    },
    "relationship_discovery": {
      "potential_relationships": 8,
      "confidence_scores": {...}
    },
    "predictive_scores": {
      "completeness_prediction": 0.92,
      "quality_forecast": "excellent"
    }
  }
}
```

### Auto-Generated Modifications

When AI features are enabled, the system can automatically generate suggested modifications:

```bash
# Enhanced auto-generation (created by create_modifications.py)
python create_modifications.py upload_results.csv

# The generated modifications now include:
# - Automated field improvements
# - Community-driven recommendations  
# - Relationship metadata additions
# - Predictive quality enhancements
```

## ⚙️ Configuration

### AI Feature Control

AI features are enabled by default when the `[ml]` package is installed. You can control specific features:

```python
from o_nakala_core.curator import NakalaCuratorClient, CuratorConfig

config = CuratorConfig(
    enable_ml_learning=True,          # Pattern learning
    enable_collaborative_intel=True,  # Community insights
    enable_prepopulation=True,        # Smart suggestions
    enable_relationship_discovery=True # Auto relationships
)

curator = NakalaCuratorClient(api_key="...", config=config)
```

### Performance Considerations

AI features add processing time but provide significant value:

- **Pattern learning**: ~2-5 seconds per operation
- **Community analysis**: ~1-3 seconds per operation  
- **Relationship discovery**: ~3-8 seconds per dataset
- **Predictive analytics**: ~1-2 seconds per prediction

For large datasets (>100 items), consider:
- Running AI analysis during off-peak hours
- Using batch operations for efficiency
- Caching results for repeated operations

## 🔍 Troubleshooting

### Common Issues

**"Enhancement dependencies not found""
```bash
# Install enhancement dependencies
pip install o-nakala-core[ml]
```

**"Pattern learning taking too long"**
```bash
# Disable enhancements for faster operation
o-nakala-curator --api-key "$KEY" --quality-report --no-ml
```

**"Community data unavailable"**
```bash
# Check internet connection - community analysis requires online access
# Fallback to local-only analysis if needed
```

### Performance Optimization

```bash
# For large datasets, use batch processing
o-nakala-curator \
  --api-key "$KEY" \
  --batch-modify modifications.csv \
  --batch-size 50 \
  --scope datasets

# Enable caching for repeated operations
export NAKALA_CACHE_ENABLED=true
export NAKALA_CACHE_TTL=3600  # 1 hour
```

## 🎓 Best Practices

### 1. Gradual Adoption
- Start with quality reports to see AI insights
- Review AI suggestions before applying modifications
- Use dry-run mode for initial testing

### 2. Community Contribution
- Your anonymized patterns contribute to community intelligence
- Better metadata from you improves suggestions for everyone
- Consider sharing successful patterns with the community

### 3. Iterative Improvement
- AI suggestions improve with usage
- Regular quality reports help track improvement trends
- Pattern confidence increases over time

### 4. Validation
- Always review AI-generated modifications
- Use `--dry-run` for testing AI suggestions
- Maintain human oversight for critical metadata

## 🔗 Related Documentation

- [Curator Field Reference](../curator-field-reference.md) - Complete field documentation
- [Workflow Guide](03-workflow-guide.md) - End-to-end processes
- [API Endpoints](../endpoints/) - Technical specifications
- [FAQ](05-faq.md) - Common questions

## 🚀 What's Next

Future AI enhancements planned:
- Natural language metadata generation
- Multi-language AI translation
- Image content analysis for automatic tagging
- Citation network analysis
- Automated research impact predictions

---

**The AI features represent a significant advancement in research data management, moving from manual curation to intelligent, community-driven metadata enhancement.**