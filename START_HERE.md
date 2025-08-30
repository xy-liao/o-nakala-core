# 🚀 Start Here: O-Nakala Core Navigation Guide

*📍 **You are here:** Main Navigation → START_HERE.md*

**Welcome to O-Nakala Core!** This single page helps you find exactly what you need based on your role and goals.

## 🎯 Quick Decision Tree

### → **I'm completely new to NAKALA**
**Goal**: Understand what NAKALA is and get my first upload working  
**Time**: 15-30 minutes  
**Path**: [Getting Started Guide](#getting-started-guide) → [First Upload](#first-upload) → [Basic Workflow](#basic-workflow)

### → **I need to upload research data now**
**Goal**: Get files uploaded to NAKALA repository quickly  
**Time**: 5-15 minutes  
**Path**: [Quick Upload](#quick-upload) → [Essential Commands](#essential-commands)

### → **I'm setting up a complete research workflow**
**Goal**: Organize files, create collections, ensure quality  
**Time**: 30-60 minutes  
**Path**: [Complete Workflow](#complete-workflow) → [Collection Management](#collection-management) → [Quality Assurance](#quality-assurance)

### → **I'm implementing for my institution**
**Goal**: Multi-user setup, security, scaling  
**Time**: 2-4 hours  
**Path**: [Institutional Deployment](#institutional-deployment) → [Multi-User Setup](#multi-user-setup) → [Security & Compliance](#security-compliance)

### → **I need to solve a specific problem**
**Goal**: Find solution to error or issue  
**Time**: 5-10 minutes  
**Path**: [Troubleshooting](#troubleshooting) → [Error Recovery](#error-recovery) → [Support](#support)

---

## 📋 Learning Paths by Role

### 🎓 **Digital Humanities Researcher**
*"I have research files and want them preserved in NAKALA"*

#### Path: Research Data → Repository
1. **[Getting Started](docs/GETTING_STARTED.md)** (20 min) - Installation and first steps
2. **[Research Workflow Guide](docs/guides/researcher-workflow-guide.md)** (45 min) - Folder-to-repository process
3. **[Collection Organization](docs/user-guides/02-collection-guide.md)** (15 min) - Organize your data
4. **[Quality Validation](docs/user-guides/04-curation-guide.md)** (20 min) - Ensure quality

**Success milestone**: Upload 5-10 research files with proper metadata and collections

### 🔧 **Data Manager/Librarian**
*"I need reliable workflows for processing multiple datasets"*

#### Path: Workflows → Quality → Scale
1. **[Complete Workflow Guide](docs/user-guides/03-workflow-guide.md)** (60 min) - Systematic 6-step process
2. **[CSV Field Testing](docs/guides/csv-field-testing.md)** (30 min) - Comprehensive validation
3. **[Best Practices](examples/workflow_documentation/best-practices.md)** (45 min) - Production lessons
4. **[Quality Assurance](examples/workflow_documentation/quality-assurance.md)** (30 min) - QA procedures

**Success milestone**: Process 50+ files with <5% error rate and complete quality reports

### 💻 **Developer/Technical Staff**
*"I need to integrate O-Nakala Core into existing systems"*

#### Path: API → Integration → Automation
1. **[API Documentation](docs/API_REFERENCE.md)** (30 min) - Complete API reference
2. **[Python Integration Examples](docs/examples/)** (45 min) - Code examples and patterns
3. **[Extending Preview Tool](docs/guides/extending-preview-tool.md)** (60 min) - Customization
4. **[Institutional Setup](examples/workflow_documentation/institutional-setup.md)** (120 min) - Enterprise deployment

**Success milestone**: Automated workflow processing 100+ files with monitoring and error recovery

### 🏛️ **Institution Administrator**
*"I need to deploy this for multiple users securely and efficiently"*

#### Path: Planning → Deployment → Management
1. **[Institutional Setup](examples/workflow_documentation/institutional-setup.md)** (120 min) - Multi-user deployment
2. **[Security & Compliance](examples/workflow_documentation/institutional-setup.md#security-and-compliance)** (60 min) - Enterprise security
3. **[Case Studies](examples/workflow_documentation/)** (60 min) - Learn from real implementations
4. **[Monitoring & Maintenance](examples/workflow_documentation/institutional-setup.md#monitoring-and-maintenance)** (45 min) - Ongoing operations

**Success milestone**: 10+ users successfully uploading with centralized monitoring and quality control

---

## ⚡ Quick Access Links

### Getting Started Guide
**New to O-Nakala Core? Start here.**
- **Installation**: `pip install o-nakala-core[cli]`
- **API Key Setup**: [Get your NAKALA API key](api/api_keys.md)
- **First Commands**: Preview → Upload → Organize

**→ [Full Getting Started Guide](docs/GETTING_STARTED.md)**

### First Upload
**Get your first files uploaded successfully.**
```bash
# 1. Preview your data first
o-nakala-preview --csv your_data.csv --interactive

# 2. Upload with confidence
o-nakala-upload --dataset your_data.csv --api-key $NAKALA_API_KEY

# 3. Organize into collections
o-nakala-collection --from-upload-output results.csv
```

**→ [Detailed Upload Guide](docs/user-guides/01-upload-guide.md)**

### Quick Upload
**For experienced users who need fast upload.**
```bash
# All-in-one command  
o-nakala-upload --csv data.csv --mode folder --folder-config data.csv --base-path ./files --output results.csv --api-key $NAKALA_API_KEY && o-nakala-collection --from-upload-output results.csv
```

**→ [Quick Reference](docs/CSV_FORMAT_GUIDE.md#essential-commands)**

### Essential Commands
```bash
# Preview and validate
o-nakala-preview --csv data.csv --interactive

# Upload files  
o-nakala-upload --dataset data.csv --mode folder --folder-config data.csv --base-path ./ --output results.csv

# Create collections
o-nakala-collection --from-upload-output results.csv

# Quality check
o-nakala-curator --quality-report --scope all

# User info
o-nakala-user-info --api-key $NAKALA_API_KEY --collections-only
```

### Complete Workflow
**Systematic 6-step process for reliable results.**
1. **Prepare**: Organize files and create metadata CSV
2. **Preview**: Validate using `o-nakala-preview --interactive`
3. **Upload**: Execute with `o-nakala-upload`
4. **Organize**: Create collections with `o-nakala-collection`
5. **Quality**: Validate with `o-nakala-curator`
6. **Publish**: Update status and verify access

**→ [Complete Workflow Guide](docs/user-guides/03-workflow-guide.md)**

### Collection Management
- **Organize uploads**: Group related data logically
- **Hierarchical structure**: Create meaningful collections
- **Metadata enhancement**: Improve discoverability

**→ [Collection Guide](docs/user-guides/02-collection-guide.md)**

### Quality Assurance
- **Metadata validation**: Ensure completeness and accuracy
- **Error detection**: Catch issues early with preview tools
- **Quality metrics**: Track and improve data quality

**→ [Quality Assurance Guide](examples/workflow_documentation/quality-assurance.md)**

### Institutional Deployment
- **Multi-user setup**: Configure for team collaboration
- **Security policies**: Implement access control and audit logging
- **Scaling strategies**: Handle growing data volumes

**→ [Institutional Setup Guide](examples/workflow_documentation/institutional-setup.md)**

### Multi-User Setup
- **Role-based access**: Configure permissions by user type
- **Shared workflows**: Standardize processes across teams
- **Central management**: Monitor and maintain system health

**→ [Multi-User Configuration](examples/workflow_documentation/institutional-setup.md#multi-user-environment)**

### Security & Compliance
- **API key management**: Secure credential handling
- **Audit logging**: Track all system activity
- **Data governance**: Implement retention and backup policies

**→ [Security Guidelines](examples/workflow_documentation/institutional-setup.md#security-and-compliance)**

### Troubleshooting
**Common issues and solutions.**
- **Upload failures**: Network, permission, metadata issues
- **Validation errors**: CSV format and field problems
- **API connectivity**: Authentication and timeout problems

**→ [Troubleshooting Guide](docs/user-guides/05-troubleshooting.md)**

### Error Recovery
**Recover from workflow failures.**
- **Resume interrupted uploads**: Continue where you left off
- **Fix metadata issues**: Correct and retry failed items
- **Quality recovery**: Restore data integrity

**→ [Error Recovery Guide](examples/workflow_documentation/error-recovery.md)**

### Support
**Get help when you need it.**
- **Documentation**: Complete guides and references
- **Examples**: Working code and configuration samples
- **Community**: GitHub issues and discussions

**→ [Support Resources](#support-resources)**

---

## 📚 Complete Documentation Structure

### Core User Guides
| Guide | Purpose | Time | Audience |
|-------|---------|------|----------|
| [Getting Started](docs/GETTING_STARTED.md) | First-time setup and basic usage | 20 min | Everyone |
| [Upload Guide](docs/user-guides/01-upload-guide.md) | Single upload operations | 15 min | All users |
| [Collection Guide](docs/user-guides/02-collection-guide.md) | Data organization | 15 min | All users |
| [Workflow Guide](docs/user-guides/03-workflow-guide.md) | Complete systematic process | 60 min | Regular users |
| [Troubleshooting](docs/user-guides/05-troubleshooting.md) | Problem solving | As needed | All users |

### Advanced Guides
| Guide | Purpose | Time | Audience |
|-------|---------|------|----------|
| [Researcher Workflow](docs/guides/researcher-workflow-guide.md) | Academic research focus | 45 min | Researchers |
| [Feature Showcase](docs/guides/feature-showcase.md) | Explore all capabilities | 30 min | All levels |
| [CSV Field Testing](docs/guides/csv-field-testing.md) | Comprehensive validation | 30 min | Data managers |
| [Extending Preview Tool](docs/guides/extending-preview-tool.md) | Customization | 60 min | Developers |

### Technical Reference
| Resource | Purpose | Audience |
|----------|---------|----------|
| [API Documentation](docs/API_REFERENCE.md) | Complete API reference | Developers |
| [Field Reference](docs/curator-field-reference.md) | Metadata field guide | Data managers |
| [Quick Reference](docs/CSV_FORMAT_GUIDE.md#essential-commands) | Essential commands | Experienced users |

### Production Deployment
| Resource | Purpose | Time | Audience |
|----------|---------|------|----------|
| [Best Practices](examples/workflow_documentation/best-practices.md) | Production lessons | 45 min | All users |
| [Quality Assurance](examples/workflow_documentation/quality-assurance.md) | QA procedures | 30 min | Data managers |
| [Institutional Setup](examples/workflow_documentation/institutional-setup.md) | Multi-user deployment | 120 min | Administrators |
| [Case Studies](examples/workflow_documentation/) | Real-world examples | 60 min | All levels |

### Examples and Templates
| Resource | Purpose | Audience |
|----------|---------|----------|
| [Sample Dataset](examples/sample_dataset/) | Working example data | All users |
| [Interactive Notebook](examples/notebooks/) | Hands-on tutorial | All users |
| [CSV Templates](examples/templates/) | Ready-to-use formats | All users |
| [Code Examples](docs/examples/) | Integration patterns | Developers |

---

## 🆘 Support Resources

### Quick Help
- **Common Commands**: See [CSV Format Guide](docs/CSV_FORMAT_GUIDE.md#essential-commands)
- **Error Messages**: Check [Troubleshooting](docs/user-guides/05-troubleshooting.md)
- **CSV Issues**: Use [Field Testing Guide](docs/guides/csv-field-testing.md)

### Community Support
- **GitHub Issues**: [Report bugs and request features](https://github.com/xy-liao/o-nakala-core/issues)
- **Documentation**: [Complete project documentation](https://github.com/xy-liao/o-nakala-core)
- **NAKALA Platform**: [Official NAKALA support](https://nakala.fr)

### Professional Support
- **API Documentation**: [NAKALA API reference](https://api.nakala.fr/doc)
- **Platform Guides**: [Official NAKALA documentation](https://documentation.huma-num.fr/nakala/)
- **Institutional Setup**: Professional implementation services available

---

**🎯 Choose your path above and start your O-Nakala Core journey!**

*Complete navigation guide for all O-Nakala Core documentation and resources.*