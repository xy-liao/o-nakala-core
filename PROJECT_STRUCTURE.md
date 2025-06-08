# O-Nakala Core Project Structure

## 📋 Overview

O-Nakala Core is organized as a comprehensive Python library and CLI toolkit for research data management with the NAKALA repository. The project follows modern Python packaging standards and provides multiple interfaces for different user needs.

## 🏗️ Directory Structure

```
o-nakala-core/
├── 📁 src/nakala_client/           # Main Python library
│   ├── cli/                        # Command-line interfaces
│   ├── auth/                       # Authentication & SSO system
│   ├── common/                     # Shared utilities and config
│   └── *.py                        # Core modules (upload, collection, curator)
├── 📁 examples/                    # Usage examples and datasets
│   ├── sample_dataset/             # Complete 14-file example
│   ├── simple-dataset/             # Minimal example (4 images)
│   └── workflow_documentation/     # Process documentation
├── 📁 docs/                        # User documentation
│   └── user-guides/                # Step-by-step guides
├── 📁 web/                         # Web interface
├── 📁 tools/                       # Development tools
│   └── nakala-python-client/       # Auto-generated OpenAPI client
├── 📁 o-nakala-workshop/           # Jupyter workshop materials
├── 📁 api/                         # API reference materials
└── 📁 config/                      # Configuration templates
```

## 🎯 Core Components

### Main Library (`src/nakala_client/`)

#### Command-Line Interfaces (`cli/`)
- `upload.py` - Data upload with metadata
- `collection.py` - Collection creation and management
- `curator.py` - Advanced metadata curation
- `user_info.py` - User account management

#### Core Modules
- `upload.py` - Upload functionality
- `collection.py` - Collection management
- `curator.py` - Metadata curation
- `vocabulary.py` - Vocabulary management
- `ml_engine.py` - Machine learning features
- `web_api.py` - Web API layer

#### Authentication System (`auth/`)
- `sso_provider.py` - SAML/OAuth SSO integration
- `institutional_auth.py` - Institution-specific authentication
- `auth_middleware.py` - Request authentication
- `user_manager.py` - User profile management
- `session_manager.py` - Session handling

### Examples and Testing (`examples/`)

#### Complete Example (`sample_dataset/`)
- **14 research files** across 5 categories
- **Metadata configurations** for upload and collections
- **Workshop exercise files** for training
- **Documentation** and usage guides

#### Simple Example (`simple-dataset/`)
- **4 bird images** for quick testing
- **Basic configuration** for getting started
- **Minimal metadata** requirements

#### Workflow Documentation (`workflow_documentation/`)
- **Process guides** for each workflow phase
- **Success metrics** and validation results
- **CSV format examples** and templates

### User Documentation (`docs/`)
- **User guides** - Step-by-step instructions
- **API reference** - Technical documentation
- **Troubleshooting** - Common issues and solutions
- **Field reference** - Metadata field specifications

### Web Interface (`web/`)
- **Modern HTML5/CSS3/ES6** single-page application
- **Progressive Web App** features
- **Mobile-responsive** design
- **Real-time analytics** dashboard

### Workshop Materials (`o-nakala-workshop/`)
- **Jupyter notebook** with complete workflow
- **Interactive tutorials** for learning
- **Educational resources** for training

## 📦 Package Structure

### Installation Structure
```python
nakala_client/
├── __init__.py                    # Package initialization
├── upload.py                     # Upload functionality
├── collection.py                 # Collection management
├── curator.py                    # Metadata curation
├── cli/                          # Command-line tools
│   ├── upload.py                 # nakala-upload command
│   ├── collection.py             # nakala-collection command
│   ├── curator.py                # nakala-curator command
│   └── user_info.py              # nakala-user-info command
└── common/                       # Shared utilities
    ├── config.py                 # Configuration management
    ├── utils.py                  # Helper functions
    └── exceptions.py             # Custom exceptions
```

### CLI Entry Points
- `nakala-upload` → `src.nakala_client.cli.upload:main`
- `nakala-collection` → `src.nakala_client.cli.collection:main`
- `nakala-curator` → `src.nakala_client.cli.curator:main`
- `nakala-user-info` → `src.nakala_client.cli.user_info:main`

## 🔧 Configuration Files

### Python Packaging
- `pyproject.toml` - Modern Python packaging configuration
- `setup.py` - Legacy setup script for compatibility
- `requirements.txt` - Production dependencies

### Development
- `.gitignore` - Git ignore patterns
- `cleanup.py` - Project cleanup script
- `CLAUDE.md` - AI assistant instructions

### API and Vocabulary
- `api/nakala-apitest.json` - Test API configuration
- `api/nakala_metadata_vocabulary.json` - Metadata vocabulary definitions

## 🚀 Usage Patterns

### For Researchers
1. **Start with examples** - Use `examples/simple-dataset/` for first upload
2. **Progress to complete workflow** - Use `examples/sample_dataset/` for full features
3. **Customize for your data** - Modify CSV configurations for your research

### For Institutions
1. **Use authentication system** - Configure institutional SSO
2. **Deploy web interface** - Provide user-friendly access
3. **Customize policies** - Set institutional metadata requirements

### For Developers
1. **Core library** - Import `nakala_client` modules directly
2. **CLI tools** - Use command-line interfaces for automation
3. **Web API** - Build custom interfaces using `web_api.py`

## 📊 Project Metrics

### Codebase Statistics
- **Core modules**: 15+ Python modules
- **CLI tools**: 4 command-line interfaces
- **Authentication**: Complete SSO system with 5 providers
- **Documentation**: 20+ user guides and references
- **Examples**: 18 files across multiple categories
- **Tests**: Comprehensive validation with real API calls

### Features Implemented
- ✅ **Basic upload/collection workflows**
- ✅ **Advanced metadata curation**
- ✅ **Institutional authentication**
- ✅ **Web interface**
- ✅ **Machine learning features**
- ✅ **Workshop materials**
- ✅ **Comprehensive documentation**

## 🔄 Development Workflow

### Code Organization
1. **Feature modules** in `src/nakala_client/`
2. **CLI wrappers** in `src/nakala_client/cli/`
3. **Tests and examples** in `examples/`
4. **Documentation** in `docs/`

### Release Process
1. **Run cleanup** - `python cleanup.py`
2. **Update version** - `pyproject.toml`
3. **Test examples** - Validate with real API
4. **Build package** - `python -m build`

---

**Production-ready for institutional research data management workflows.**