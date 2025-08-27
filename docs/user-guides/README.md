# O-Nakala Core User Guides

## 🧭 Navigation & Quick Access

### **📋 User Guide Index**

| Guide | Purpose | Time | Best For |
|-------|---------|------|----------|
| **[01-Upload Guide](01-upload-guide.md)** | First dataset upload | 15 min | New users, single files |
| **[02-Collection Guide](02-collection-guide.md)** | Organize data into collections | 30 min | Data organization |
| **[03-Workflow Guide](03-workflow-guide.md)** | Complete research workflow | 60 min | Full projects |
| **[04-Curation Guide](04-curation-guide.md)** | Metadata enhancement | 45 min | Quality improvement |
| **[05-Troubleshooting](05-troubleshooting.md)** | Problem solving | As needed | When stuck |

### **🎯 Choose Your Workflow**

Different workflows serve different needs. Pick the one that matches your situation:

| Workflow Type | Steps | Time | Purpose | Best For |
|---------------|-------|------|---------|----------|
| **[Quick Start](01-upload-guide.md)** | 3 essential | 10-15 min | First upload | New users, single files |
| **[User Workflow](03-workflow-guide.md)** | 6 complete | 45-90 min | Full data management | Research projects |
| **[Feature Demo](../../examples/notebooks/workflow_notebook.ipynb)** | 8 operations | 20 min | Explore capabilities | Evaluators, learning |

## User-Focused Guides (Practical Steps)

### Essential Workflows
- **[User Workflow Guide](03-workflow-guide.md)** - Complete 6-step research data management
- **[Upload Guide](01-upload-guide.md)** - Single operation focus  
- **[Collection Guide](02-collection-guide.md)** - Organizing your data

### Specialized Tasks  
- **[Curation Guide](04-curation-guide.md)** - Metadata enhancement and quality management

### Support Resources
- **[Troubleshooting](05-troubleshooting.md)** - Problem solving and common issues

## Demo & Learning Resources (Feature Exploration)

### Interactive Demonstrations
- **[Feature Demonstration Notebook](../../examples/notebooks/workflow_notebook.ipynb)** - Complete capability showcase
- **API Examples** - Available in `examples/` directory

### Technical References
- **[Endpoint Documentation](../endpoints/)** - API specifications
- **[Field Reference](../curator-field-reference.md)** - Complete metadata field guide

## Quick Decision Guide

### "I need to..."

**Upload my first dataset** → [Upload Guide](01-upload-guide.md)  
**Manage a complete research project** → [User Workflow Guide](03-workflow-guide.md)  
**See what this tool can do** → [Feature Demonstration](../../examples/notebooks/workflow_notebook.ipynb)  
**Improve my metadata** → [Curation Guide](04-curation-guide.md)  
**Organize existing data** → [Collection Guide](02-collection-guide.md)  
**Fix a problem** → [Troubleshooting](05-troubleshooting.md)  
**Understand field requirements** → [Field Reference](../curator-field-reference.md)

### "I am a..."

**Researcher with data to publish** → Start with [User Workflow Guide](03-workflow-guide.md)  
**New user exploring options** → Try [Feature Demonstration](../../examples/notebooks/workflow_notebook.ipynb)  
**Developer integrating o-nakala-core** → Check [API Documentation](../endpoints/)  
**Data manager with many files** → Use [User Workflow Guide](03-workflow-guide.md) + [Curation Guide](04-curation-guide.md)

## Documentation Philosophy

### **O-Nakala Core vs Official NAKALA Docs**

**Important**: O-Nakala Core uses **user-friendly CSV formats** that differ from the official NAKALA API. This is intentional design for ease of use.

| Format | Official NAKALA API | O-Nakala Core |
|--------|-------------------|---------------|
| **Creators** | `[{"givenname": "Jean", "surname": "Dupont"}]` | `"Dupont,Jean"` |
| **Multilingual** | Multiple API calls | `"fr:Titre\|en:Title"` |
| **Why Different?** | Raw API power | User-friendly simplicity |

**You get both**: Simple CSV input **AND** full API compliance through automatic conversion.

### User-Focused vs Demo Content

**User Guides** (what you need to accomplish your work):
- Action-oriented language ("Upload your data", "Improve metadata")
- Practical time estimates and clear outcomes
- Progressive disclosure (quick start → detailed options)
- Troubleshooting and real-world tips

**Demo Content** (exploring what's possible):
- Feature-oriented language ("Demonstrates ML capabilities")
- Technical details and integration points exposed
- Comprehensive capability showcase
- Development and evaluation focus

Both types serve important but different purposes. User guides help you get work done; demos help you understand what's available.