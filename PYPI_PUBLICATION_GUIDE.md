# PyPI Publication Guide for NAKALA Client

## 🎯 Overview

This guide outlines the steps to publish the `nakala-client` package to PyPI, enabling users to install it via `pip install nakala-client` instead of relying on subprocess calls and local scripts.

## ✅ Current Status

### Completed Preparations:
- ✅ **Package Structure**: Modern `src/` layout with proper `__init__.py` files
- ✅ **CLI Entry Points**: Created `src/nakala_client/cli/` modules with proper entry points
- ✅ **setup.py**: Updated with correct console scripts configuration
- ✅ **pyproject.toml**: Modern packaging configuration with all dependencies
- ✅ **Workshop Integration**: Updated notebook to use direct imports with fallback
- ✅ **Requirements**: Updated workshop requirements for PyPI compatibility

### Package Structure:
```
src/nakala_client/
├── __init__.py              # Package initialization
├── upload.py               # Core upload functionality
├── collection.py           # Core collection functionality  
├── curator.py              # Core curation functionality
├── user_info.py           # User information functionality
├── cli/                    # CLI wrapper modules
│   ├── __init__.py
│   ├── upload.py          # CLI: nakala-upload
│   ├── collection.py      # CLI: nakala-collection
│   ├── curator.py         # CLI: nakala-curator
│   └── user_info.py       # CLI: nakala-user-info
└── common/                 # Shared utilities
    ├── __init__.py
    ├── config.py          # Configuration management
    ├── utils.py           # Common utilities
    └── exceptions.py      # Custom exceptions
```

## 🚀 Publication Steps

### 1. Pre-Publication Testing

```bash
# Test local installation
pip install -e .

# Verify CLI commands work
nakala-upload --help
nakala-collection --help
nakala-curator --help
nakala-user-info --help

# Test workshop notebook
cd o-nakala-workshop
jupyter lab NAKALA_Complete_Workflow.ipynb
```

### 2. Build Package

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Verify contents
tar -tzf dist/nakala-client-2.0.0.tar.gz
```

### 3. Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ nakala-client
```

### 4. Publish to PyPI

```bash
# Upload to production PyPI
twine upload dist/*

# Verify installation
pip install nakala-client
```

## 📦 Package Benefits After Publication

### For Users:
```bash
# Simple installation
pip install nakala-client

# With workshop dependencies
pip install nakala-client[workshop]

# Direct CLI usage
nakala-upload --api-key YOUR_KEY --dataset data.csv
```

### For Workshop:
```python
# Direct imports (no subprocess needed)
from nakala_client import NakalaUploader, NakalaCollectionManager

# Clean API usage
uploader = NakalaUploader(api_key="key", api_url="url")
result = uploader.upload_folder(dataset_csv="data.csv")
```

### For Developers:
```python
# Professional API access
from nakala_client.common import NakalaConfig
from nakala_client.upload import NakalaUploader

config = NakalaConfig(api_key="key")
uploader = NakalaUploader(config)
```

## 🔧 Workshop Improvements After PyPI

### Before (Subprocess approach):
```python
upload_cmd = [
    "python", str(PARENT_DIR / "nakala-client-upload-v2.py"),
    "--api-url", API_URL,
    "--api-key", API_KEY,
    # ... many parameters
]
result = subprocess.run(upload_cmd, capture_output=True, text=True)
```

### After (Direct API approach):
```python
uploader = NakalaUploader(api_key=API_KEY, api_url=API_URL)
result = uploader.upload_folder(
    dataset_csv=data_items_csv,
    base_path=DATA_DIR,
    validate_only=True
)
```

## 🌟 Additional Benefits

### 1. **Cloud Compatibility**
- Works in Google Colab, Binder, etc.
- No file path dependencies
- Standard Python packaging

### 2. **Version Management**
- Semantic versioning
- Easy updates: `pip install --upgrade nakala-client`
- Dependency resolution

### 3. **Professional Distribution**
- Standard Python packaging practices
- Automatic dependency installation
- Better error handling and debugging

### 4. **Enhanced Workshop Experience**
- Faster setup (one `pip install` command)
- More reliable execution
- Better error messages
- Cross-platform compatibility

## 📋 Checklist for Publication

### Pre-Publication:
- [ ] Test all CLI commands work
- [ ] Verify import structure
- [ ] Run workshop notebook end-to-end
- [ ] Update version numbers
- [ ] Write comprehensive README
- [ ] Add proper LICENSE file

### Publication:
- [ ] Build package locally
- [ ] Test on TestPyPI
- [ ] Verify installation from TestPyPI
- [ ] Upload to production PyPI
- [ ] Test final installation

### Post-Publication:
- [ ] Update workshop documentation
- [ ] Create installation guides
- [ ] Tag GitHub release
- [ ] Update project README
- [ ] Announce to users

## 🎯 Recommendation

**Strongly recommend proceeding with PyPI publication** because:

1. **Eliminates subprocess complexity** in workshop
2. **Improves user experience** significantly  
3. **Follows Python best practices**
4. **Enables cloud notebook compatibility**
5. **Provides professional distribution**

The current setup is already PyPI-ready with both modern `pyproject.toml` and backward-compatible `setup.py` configurations.