# Environment Setup and Authentication

## Overview
This phase establishes the necessary environment configuration and validates API access to the NAKALA test platform.

## Prerequisites
- Python 3.9+ installed
- Git repository cloned
- Access to NAKALA test API key

## Environment Configuration

### 1. API Key Setup
```bash
# Set NAKALA test API key (provided in api/api_keys.md)
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"

# Set API endpoint to test environment
export NAKALA_BASE_URL="https://apitest.nakala.fr"

# Verify environment variables
echo "API Key: $NAKALA_API_KEY"
echo "Base URL: $NAKALA_BASE_URL"
```

### 2. Package Installation

#### Option A: From PyPI (Recommended)
```bash
# Install stable release with CLI tools
pip install o-nakala-core[cli]

# Verify installation
nakala-upload --help
nakala-collection --help
nakala-curator --help
nakala-user-info --help
```

#### Option B: From Source (Development)
```bash
# Navigate to project root
cd /Users/syl/Documents/GitHub/o-nakala-core

# Install in development mode with all dependencies
pip install -e .[cli]

# Verify installation
nakala-upload --help
nakala-collection --help
nakala-curator --help
nakala-user-info --help
```

## Validation

### API Access Test
```bash
# Test API connectivity and authentication
NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293" \
NAKALA_BASE_URL="https://apitest.nakala.fr" \
nakala-user-info
```

**Expected Output:**
```
============================================================
NAKALA USER PROFILE SUMMARY
============================================================

User Information:
  Name: Utilisateur Nakala #1
  Email: nakala@huma-num.fr
  Institution: N/A
  User ID: c7e9bb15-6b4e-4e09-b234-ae7b13ac1f3b
  Status: 

Resource Summary:
  Collections: 187
  Datasets: 572
  Groups: 0

Collections by Status:
  private: 107
  public: 80

Datasets by Status:
  published: 288
  pending: 284
```

## Security Notes

### Test Environment
- ✅ **Safe for testing**: Test API keys are public and designed for development
- ✅ **Isolated data**: Test environment is separate from production
- ✅ **No impact**: Operations do not affect production repositories

### Production Considerations
- ⚠️ **Personal API Keys**: Never commit production API keys to version control
- ⚠️ **Environment Variables**: Use `.env` files for local development
- ⚠️ **CI/CD**: Use secure environment variable injection for automated workflows

## Troubleshooting

### Common Issues
1. **Authentication Errors (401/403)**
   - Verify API key is correctly set
   - Check API endpoint URL
   - Ensure test environment access

2. **Network Connectivity**
   - Verify internet connection
   - Check firewall settings
   - Test API endpoint accessibility

3. **Package Installation Issues**
   - Update pip: `pip install --upgrade pip`
   - Use virtual environment for isolation
   - Check Python version compatibility (3.9+)

## Next Steps
Once environment is validated, proceed to [02_data_upload](../02_data_upload/upload_workflow.md) to begin the data upload process.