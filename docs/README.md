# O-Nakala-Core Documentation

🎉 **V2.0 Development Complete** - Production-ready client with enhanced features!

## 📋 CURRENT STATUS: V2.0 COMPLETE WITH REAL CURATION VALIDATED

**⚠️ DOCUMENTATION HAS BEEN REORGANIZED** - See [`../docs_organized/`](../docs_organized/) for the new organized structure.

**Current Status**: All workflows validated with real API calls, curation successfully applied to live data.

## Overview

The O-Nakala-Core project provides a comprehensive suite of tools for interacting with the Nakala API platform. V2.0 development is complete with improved consistency, error handling, and extensibility while maintaining 100% backward compatibility.

## 🚀 What's New in v2.0

### Key Improvements
- **Unified Architecture**: Common utilities shared across all client modules
- **Better Error Handling**: Comprehensive validation and error reporting
- **Enhanced Logging**: Detailed diagnostics and progress tracking
- **Backward Compatibility**: Original scripts remain functional
- **Extensible Design**: Foundation for new client modules

### Available Client Modules

#### ✅ **Implemented (v2.0)**
- **Upload Client** (`nakala-client-upload-v2.py`) - Upload datasets with files and metadata
- **Collection Client** (`nakala-client-collection-v2.py`) - Create and manage collections

#### 🔄 **Legacy (v1.0 - Still Functional)**
- `nakala-client-upload.py` - Original upload script
- `nakala-client-collection.py` - Original collection script

#### 📋 **Planned for Future Development**
- **Search Client** - Advanced search and retrieval operations
- **Curator Client** - Data curation and quality management
- **Metadata Client** - Metadata manipulation and validation

## Quick Start Guide

### 1. Installation

```bash
# Clone the repository
git clone [repository-url]
cd o-nakala-core

# Install dependencies
pip install -r requirements-new.txt

# Install in development mode (recommended)
pip install -e .
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit with your API credentials
nano .env
```

### 3. Basic Usage

#### Upload Datasets
```bash
python nakala-client-upload-v2.py \
  --api-key YOUR_KEY \
  --dataset sample_dataset/folder_data_items.csv \
  --folder-config sample_dataset/folder_data_items.csv \
  --mode folder
```

#### Create Collections
```bash
python nakala-client-collection-v2.py \
  --api-key YOUR_KEY \
  --from-folder-collections sample_dataset/folder_collections.csv \
  --from-upload-output output.csv
```

## Documentation Structure

### 📋 **User Guides**
- [Upload Guide](user-guides/01-upload-guide.md) - Complete upload workflow
- [Collection Guide](user-guides/02-collection-guide.md) - Collection management
- [Workflow Guide](user-guides/03-workflow-guide.md) - End-to-end examples
- [V2.0 Migration Guide](user-guides/04-v2-migration-guide.md) - Upgrading from v1.0

### 🔧 **Technical Documentation**
- [API Implementation Notes](implementation/01-api-implementation-notes.md) - Technical details
- [Architecture Overview](implementation/02-architecture-overview.md) - V2.0 system design
- [Common Utilities Reference](implementation/03-common-utilities.md) - Shared components

### 📊 **Analysis & Design**
- [API Client Analysis](analysis/01-api-client-analysis.md) - Design decisions
- [Folder Dataset Analysis](analysis/02-folder-dataset-analysis.md) - Dataset organization
- [V2.0 Design Review](analysis/03-v2-design-review.md) - Architecture improvements

### 🆘 **Support Resources**
- [Troubleshooting Guide](troubleshooting.md) - Common issues and solutions
- [FAQ](user-guides/05-faq.md) - Frequently asked questions
- [Development Timeline](development_timeline.md) - Project history

## Project Structure

```
o-nakala-core/
├── src/nakala_client/           # V2.0 Package Structure
│   ├── __init__.py             # Package initialization
│   ├── upload.py               # Upload module (v2.0)
│   ├── collection.py           # Collection module (v2.0)
│   └── common/                 # Shared utilities
│       ├── __init__.py
│       ├── utils.py            # Common functions
│       ├── config.py           # Configuration management
│       └── exceptions.py       # Custom exceptions
├── nakala-client-*-v2.py       # V2.0 CLI scripts
├── nakala-client-*.py          # V1.0 CLI scripts (legacy)
├── config/                     # Configuration templates
├── docs/                       # Documentation
├── sample_dataset/             # Example datasets
└── requirements-new.txt        # V2.0 dependencies
```

## Getting Help

### For Users
1. Check the [Troubleshooting Guide](troubleshooting.md) for common issues
2. Review the relevant [User Guide](user-guides/) for your task
3. Check the [FAQ](user-guides/05-faq.md) for quick answers

### For Developers
1. Review the [Architecture Overview](implementation/02-architecture-overview.md)
2. Check the [Common Utilities Reference](implementation/03-common-utilities.md)
3. See [Development Timeline](development_timeline.md) for project context

### For Migration from V1.0
1. Read the [V2.0 Migration Guide](user-guides/04-v2-migration-guide.md)
2. Test with your existing datasets using v2.0 scripts
3. Both versions remain functional during transition

## Contributing

When contributing to the project:
1. Follow the v2.0 architecture patterns in `src/nakala_client/common/`
2. Update relevant documentation in the `docs/` directory
3. Add comprehensive error handling and logging
4. Maintain backward compatibility where possible
5. Include tests and examples for new features

## Support

- **Documentation Issues**: Update the relevant guide or create a new one
- **Technical Issues**: Check implementation notes and error logs
- **Feature Requests**: Review the planned client modules roadmap
- **Bug Reports**: Include detailed logs and reproduction steps