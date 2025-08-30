# Navigation Template

<!-- This template provides consistent navigation elements for all documentation files -->
<!-- Copy the relevant sections to each documentation file -->

## Standard Navigation Header
```markdown
**📍 You are here:** [START_HERE](../START_HERE.md) → [Getting Started](GETTING_STARTED.md) → Current Guide

**⏱️ Time:** X minutes | **👥 Audience:** Your target audience | **📈 Level:** Beginner/Intermediate/Advanced
```

## Progressive Disclosure Sections

### For Basic Guides
```markdown
## What You'll Learn
- ✅ Key outcome 1
- ✅ Key outcome 2  
- ✅ Key outcome 3

## Prerequisites
- [ ] Previous guide completed OR basic knowledge requirement
- [ ] Tools installed and configured
- [ ] Time available (X minutes)

## Next Steps After This Guide
**If successful, you'll be ready for:**
- 🎯 **Next logical step**: [Link to next guide](link)
- 🔧 **Advanced topics**: [Link to advanced guide](link)
- 🚨 **If issues**: [Troubleshooting Guide](link)
```

### For Advanced Guides  
```markdown
## Before Starting This Advanced Guide
**Required foundation:**
- ✅ [Basic Guide](link) completed successfully
- ✅ [Intermediate Guide](link) concepts understood
- ✅ X uploads performed without errors

**If you haven't completed the prerequisites:**
→ Start with [Getting Started Guide](GETTING_STARTED.md)

## Advanced Topics Covered
This guide covers complex scenarios that require solid foundational knowledge.
```

### For Reference Documentation
```markdown
## How to Use This Reference
- 🔍 **Finding specific information**: Use Ctrl+F / Cmd+F to search
- 📋 **Copy-paste ready**: All code examples are production-tested
- 🔗 **Cross-references**: Links to related concepts and examples

## Context and Background
**This reference supports:**
- [Workflow Guide](link) - Implementation context
- [Getting Started](link) - Basic usage patterns  
- [Troubleshooting](link) - Error resolution
```

## Standard Footer Navigation
```markdown
---

## 🧭 Navigation

### ⬅️ Previous Steps
- [Previous Guide Title](link) - Brief description

### ➡️ Next Steps  
- **Recommended next**: [Next Guide Title](link) - Brief description
- **Alternative path**: [Alternative Guide](link) - Brief description

### 🔍 Related Resources
- [Quick Reference](link) - Essential commands
- [Troubleshooting](link) - Problem solving
- [Examples](link) - Working code and data

### 🆘 Need Help?
- **Quick issues**: [Troubleshooting Guide](user-guides/05-troubleshooting.md)
- **Community support**: [GitHub Issues](https://github.com/xy-liao/o-nakala-core/issues)
- **Start over**: [Navigation Guide](../START_HERE.md)

---

*📍 **You are here:** [START_HERE](../START_HERE.md) → [Section] → Current Guide*
```

## Content Organization Patterns

### Learning Progression Pattern
```markdown
## 📚 Learning Path: [Topic Name]

### Foundation (Required First)
1. **[Guide 1](link)** (15 min) - Basic concepts and setup
2. **[Guide 2](link)** (20 min) - First practical application

### Development (Choose Your Path)  
- **Research Focus**: [Research Workflow](link) (45 min)
- **Technical Focus**: [API Integration](link) (60 min)
- **Management Focus**: [Quality Assurance](link) (30 min)

### Advanced (After Foundation + One Development Path)
- **[Advanced Guide 1](link)** (90 min) - Complex scenarios
- **[Advanced Guide 2](link)** (120 min) - Expert techniques
```

### Decision Tree Pattern
```markdown
## 🤔 Choose Your Path

**I need to...**
- ✅ **Upload files quickly** → [Quick Upload Guide](link) (10 min)
- ⚙️ **Set up systematic workflow** → [Complete Workflow](link) (60 min)  
- 🏛️ **Deploy for multiple users** → [Institutional Setup](link) (120 min)
- 🚨 **Solve a specific problem** → [Troubleshooting](link) (as needed)

**I am a...**
- 🎓 **Researcher** → [Research Workflow Path](#research-path)
- 🔧 **Data Manager** → [Data Management Path](#data-management-path)
- 💻 **Developer** → [Technical Integration Path](#technical-path)
- 🏛️ **Administrator** → [Institutional Deployment Path](#institutional-path)
```

### Context Awareness Pattern
```markdown
## 💡 Context: When to Use This Guide

**Use this guide when:**
- ✅ You have [specific prerequisite condition]
- ✅ You need to [specific outcome]
- ✅ You're comfortable with [specific skill level]

**Don't use this guide if:**
- ❌ You haven't completed [prerequisite guide]
- ❌ You're looking for [different outcome] - see [alternative guide] instead
- ❌ You need [simpler/more complex approach] - see [level-appropriate guide]

**After this guide, you'll be able to:**
- [Specific capability 1]
- [Specific capability 2]
- [Specific capability 3]
```

## Cross-Reference Standards

### Inline References
```markdown
<!-- For concepts introduced elsewhere -->
For API key setup, see the [complete setup guide](../api/api_keys.md).

<!-- For commands explained in detail elsewhere -->  
The `o-nakala-preview` command ([full reference](CSV_FORMAT_GUIDE.md#essential-commands)) validates your data before upload.

<!-- For troubleshooting -->
If you encounter errors, check the [troubleshooting section](user-guides/05-troubleshooting.md#upload-errors) for solutions.
```

### Section References
```markdown
### See Also
- **[Related Concept](link)** - Brief explanation of relevance
- **[Alternative Approach](link)** - When to choose this instead
- **[Deep Dive](link)** - More detailed exploration of this topic

### Prerequisites Review
If any of these concepts are unfamiliar, review them first:
- **[Basic Concept](link)** - Foundation knowledge needed
- **[Tool Setup](link)** - Required configuration
- **[Sample Data](link)** - Practice materials
```

## Standard Section Templates

### Installation Section
```markdown
## Installation

### System Requirements
- **Python**: 3.9+ ([installation guide](https://python.org))
- **Operating System**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Disk Space**: 500MB for installation + workspace

### Quick Install
\`\`\`bash
pip install o-nakala-core[cli,ml]
\`\`\`

### Development Install  
\`\`\`bash
git clone https://github.com/xy-liao/o-nakala-core.git
cd o-nakala-core
pip install -e ".[dev,cli,ml]"
\`\`\`

### Verify Installation
\`\`\`bash
o-nakala-preview --version
# Should output: o-nakala-core X.X.X
\`\`\`

**Issues with installation?** See [installation troubleshooting](user-guides/05-troubleshooting.md#installation-issues).
```

### Example Section
```markdown
## Working Example

### Sample Data
\`\`\`bash
# Use provided sample dataset
cd examples/sample_dataset
ls folder_data_items.csv  # Main metadata file
ls files/                 # Sample research files
\`\`\`

### Step-by-Step Execution
\`\`\`bash
# 1. Preview (always do this first)
o-nakala-preview --csv folder_data_items.csv --interactive

# 2. Upload  
o-nakala-upload --dataset folder_data_items.csv --output results.csv

# 3. Verify
grep -c "success" results.csv
\`\`\`

### Expected Outcomes
After successful execution:
- ✅ All files uploaded to NAKALA
- ✅ Results saved in `results.csv`  
- ✅ Ready for collection organization

**Don't see expected results?** Check the [troubleshooting guide](user-guides/05-troubleshooting.md).
```

This navigation template provides consistent, user-friendly navigation patterns that implement progressive disclosure and help users find their next steps efficiently.