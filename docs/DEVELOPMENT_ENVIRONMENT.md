# Development Environment Setup

## Overview

This document provides comprehensive setup instructions for developing and testing O-Nakala Core, including API key configuration, test environment setup, and validation procedures.

## API Key Configuration

### Test Environment API Keys

O-Nakala Core supports both production and test environments. For development and testing, use the NAKALA test environment.

#### Available Test API Keys

**Primary Test Key (Validated Working)**
```bash
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_API_URL="https://apitest.nakala.fr"
```

This key has been validated for:
- ✅ File uploads (all formats)
- ✅ Dataset creation 
- ✅ Collection management
- ✅ Metadata modifications
- ✅ Full end-to-end workflow

**Alternative Test Keys**

Additional test keys are documented in `api/api_keys.md`. These keys have varying capabilities and may be useful for specific testing scenarios.

#### Environment Configuration

**Option 1: Environment Variables**
```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_API_URL="https://apitest.nakala.fr"
export NAKALA_BASE_PATH="examples/sample_dataset"
```

**Option 2: .env File**
```bash
# Create .env file in project root
echo "NAKALA_API_KEY=33170cfe-f53c-550b-5fb6-4814ce981293" > .env
echo "NAKALA_API_URL=https://apitest.nakala.fr" >> .env
echo "NAKALA_BASE_PATH=examples/sample_dataset" >> .env
```

**Option 3: Configuration File**
```python
from src.o_nakala_core.common.config import NakalaConfig

config = NakalaConfig(
    api_key="33170cfe-f53c-550b-5fb6-4814ce981293",
    api_url="https://apitest.nakala.fr",
    base_path="examples/sample_dataset"
)
```

## Development Setup

### Prerequisites

```bash
# Python 3.9+ required
python --version  # Should be 3.9+

# Install development dependencies
pip install -e ".[dev,cli,ml]"
```

### Quick Validation

Test your environment setup with this quick validation script:

```bash
# Create and run validation script
cat > validate_setup.py << 'EOF'
#!/usr/bin/env python3
"""Quick environment validation script."""

import os
from src.o_nakala_core.common.config import NakalaConfig
from src.o_nakala_core.upload import NakalaUploadClient

def main():
    print("🔍 Validating O-Nakala Core Development Environment")
    print("=" * 55)
    
    # Check API key
    api_key = os.getenv('NAKALA_API_KEY')
    if api_key:
        print(f"✅ API Key: {api_key[:8]}...{api_key[-8:]}")
    else:
        print("❌ API Key: Not configured")
        return False
    
    # Check API URL
    api_url = os.getenv('NAKALA_API_URL', 'https://apitest.nakala.fr')
    print(f"✅ API URL: {api_url}")
    
    # Test configuration
    try:
        config = NakalaConfig(
            api_key=api_key,
            api_url=api_url,
            base_path="examples/sample_dataset"
        )
        print("✅ Configuration: Valid")
    except Exception as e:
        print(f"❌ Configuration: {e}")
        return False
    
    # Test client creation
    try:
        client = NakalaUploadClient(config)
        print("✅ Upload Client: Created successfully")
    except Exception as e:
        print(f"❌ Upload Client: {e}")
        return False
    
    # Test sample dataset validation
    if os.path.exists("examples/sample_dataset/folder_data_items.csv"):
        try:
            client.validate_dataset(
                mode="folder",
                folder_config="examples/sample_dataset/folder_data_items.csv"
            )
            print("✅ Sample Dataset: Validation passed")
        except Exception as e:
            print(f"❌ Sample Dataset: {e}")
            return False
    else:
        print("⚠️  Sample Dataset: Not found (optional)")
    
    print("\n🎉 Environment validation successful!")
    return True

if __name__ == "__main__":
    main()
EOF

python validate_setup.py
```

## Testing

### Unit Tests

```bash
# Run all unit tests
python -m pytest tests/unit/ -v

# Run with coverage
python -m pytest tests/unit/ --cov=src/o_nakala_core --cov-report=term-missing

# Run specific test module
python -m pytest tests/unit/test_upload_comprehensive.py -v
```

### Integration Tests

```bash
# Run integration tests (requires API key)
python -m pytest tests/integration/ -v -m integration

# Run without API-dependent tests
python -m pytest tests/integration/ -v -m "not integration"

# Run performance tests
python -m pytest tests/integration/ -v -m slow
```

### End-to-End Workflow Test

Validate the complete workflow:

```bash
# Set environment
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"

# Run upload validation
python -m src.o_nakala_core.upload \
  --api-key "$NAKALA_API_KEY" \
  --api-url "https://apitest.nakala.fr" \
  --dataset "examples/sample_dataset/folder_data_items.csv" \
  --base-path "examples/sample_dataset" \
  --mode "folder" \
  --folder-config "examples/sample_dataset/folder_data_items.csv" \
  --validate-only

# Run collection validation
python -m src.o_nakala_core.collection \
  --api-key "$NAKALA_API_KEY" \
  --api-url "https://apitest.nakala.fr" \
  --from-folder-collections "examples/sample_dataset/folder_collections.csv" \
  --validate-only
```

## Code Quality

### Linting and Formatting

```bash
# Check code style
python -m flake8 src/ --max-line-length=100 --extend-ignore=E203,W503

# Format code
python -m black src/ tests/

# Type checking
python -m mypy src/ --ignore-missing-imports
```

### Current Quality Status

As of the last validation:
- ✅ **Test Coverage**: 17% (substantial improvement from 15%)
- ✅ **Import Issues**: Resolved (Path imports fixed)
- ✅ **Line Length**: 64% reduction in violations (from 44 to 16)
- ✅ **Core Functionality**: 100% working end-to-end

## Production vs. Test Environment

### Test Environment (Development)
- **URL**: `https://apitest.nakala.fr`
- **Purpose**: Development and testing
- **Data**: Not persistent, may be reset
- **Rate Limits**: More lenient
- **API Key**: Use provided test keys

### Production Environment
- **URL**: `https://api.nakala.fr`
- **Purpose**: Real research data
- **Data**: Persistent, backed up
- **Rate Limits**: Strict
- **API Key**: Personal API key required from NAKALA

## Common Development Workflows

### Adding New Features

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Develop with TDD**
   ```bash
   # Write tests first
   python -m pytest tests/unit/test_new_feature.py -v
   
   # Implement feature
   # Run tests to validate
   ```

3. **Validate Integration**
   ```bash
   # Test with real API
   python -m pytest tests/integration/ -v -k "new_feature"
   ```

4. **Check Code Quality**
   ```bash
   python -m flake8 src/
   python -m pytest --cov=src/o_nakala_core
   ```

### Debugging API Issues

```bash
# Enable debug logging
export NAKALA_LOG_LEVEL="DEBUG"

# Run with verbose output
python -m src.o_nakala_core.upload \
  --api-key "$NAKALA_API_KEY" \
  --log-level "DEBUG" \
  --validate-only

# Check API response headers
curl -H "X-API-KEY: $NAKALA_API_KEY" \
     -I "https://apitest.nakala.fr/datas"
```

## Troubleshooting

### Common Issues

**1. API Key Not Working**
```bash
# Verify key format
echo $NAKALA_API_KEY | wc -c  # Should be 37 characters

# Test key directly
curl -H "X-API-KEY: $NAKALA_API_KEY" \
     "https://apitest.nakala.fr/datas" \
     | jq .
```

**2. Import Errors**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install in development mode
pip install -e .
```

**3. Path Issues**
```bash
# Check file permissions
ls -la examples/sample_dataset/

# Verify base path
python -c "
from pathlib import Path
print(Path('examples/sample_dataset').resolve())
"
```

**4. Network Issues**
```bash
# Test connectivity
curl -I https://apitest.nakala.fr/

# Check proxy settings
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

## Best Practices

### API Usage
- Always use test environment for development
- Implement proper error handling
- Use validation mode before real operations
- Respect rate limits

### Code Quality
- Write tests before implementing features
- Follow PEP 8 style guidelines
- Use type hints where possible
- Document complex functions

### Version Control
- Use meaningful commit messages
- Keep feature branches focused
- Test before pushing
- Update documentation

## Support

### Documentation
- **Main README**: [README.md](../README.md)
- **API Specs**: [api/](../api/)
- **Examples**: [examples/](../examples/)
- **Workflow Docs**: [examples/workflow_documentation/](../examples/workflow_documentation/)

### Getting Help
- Check existing issues: [GitHub Issues](https://github.com/xy-liao/o-nakala-core/issues)
- Review test cases for examples
- Consult NAKALA official documentation

---

**Last Updated**: 2025-06-10  
**Validated With**: O-Nakala Core v2.1.2  
**Test Environment**: https://apitest.nakala.fr  
**Primary Test Key**: 33170cfe-f53c-550b-5fb6-4814ce981293