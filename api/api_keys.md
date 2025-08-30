# NAKALA API Keys Guide

This guide helps you obtain and manage API keys for accessing the NAKALA research data repository through O-Nakala Core.

## Production Environment

### Getting Your Personal API Key

1. **Create NAKALA Account**
   - Visit [nakala.fr](https://nakala.fr)
   - Register using your institutional email address
   - Verify your email and complete profile setup

2. **Request API Access**
   - Contact your institution's NAKALA administrator
   - Or email nakala@huma-num.fr with your use case
   - API access is typically granted for legitimate research purposes

3. **Locate Your API Key**
   - Log into your NAKALA account
   - Navigate to "My Account" → "API Settings"
   - Copy your personal API key (treat this as confidential)

4. **Configure O-Nakala Core**
   ```bash
   export NAKALA_API_KEY="your-personal-api-key"
   export NAKALA_BASE_URL="https://api.nakala.fr"
   ```

## Test Environment

### Public Test API Key

For evaluation, development, and learning purposes, use the public test environment:

- **API URL**: `https://apitest.nakala.fr`
- **Test API Key**: `33170cfe-f53c-550b-5fb6-4814ce981293`
- **Status**: Active (verified August 2025)

### Test Environment Configuration

```bash
# Set test environment variables
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_BASE_URL="https://apitest.nakala.fr"

# Verify connection
o-nakala-user-info --api-key $NAKALA_API_KEY
```

### Test Environment Limitations

- **Data Persistence**: Test data may be periodically cleaned
- **Performance**: May be slower than production environment
- **Rate Limits**: More restrictive than production
- **Features**: Some advanced features may be disabled

## API Key Security

### Best Practices

- **Never commit API keys** to version control systems
- **Use environment variables** instead of hardcoding keys
- **Rotate keys regularly** in production environments
- **Limit key permissions** to minimum required scope

### Environment Variable Setup

Create a `.env` file in your project (add to `.gitignore`):

```bash
# .env file (DO NOT COMMIT)
NAKALA_API_KEY=your-actual-api-key
NAKALA_BASE_URL=https://api.nakala.fr
```

Load environment variables:

```bash
# Using python-dotenv (recommended)
pip install python-dotenv

# In your Python code
from dotenv import load_dotenv
load_dotenv()

# Or manually in shell
source .env
```

## Troubleshooting

### Common Issues

**"Authentication failed" or 401 errors**
- Verify API key is correct and not expired
- Check you're using the right environment URL
- Ensure key has required permissions

**"Invalid API key format" errors**
- API keys should be UUID format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- Remove any extra spaces or characters
- Verify you copied the complete key

**Connection timeout errors**
- Check internet connectivity
- Verify NAKALA_BASE_URL is correct
- Try test environment to isolate issues

### Getting Help

- **Documentation**: [NAKALA User Guide](https://documentation.huma-num.fr/nakala/) (fallback: see local docs/ folder)
- **API Documentation**: [OAI/API Reference](https://documentation.huma-num.fr/nakala-API/) (fallback: test with working examples)
- **Technical Support**: nakala@huma-num.fr
- **O-Nakala Core Issues**: [GitHub Issues](https://github.com/xy-liao/o-nakala-core/issues)
- **Community**: NAKALA user forums and mailing lists

### Offline/Fallback Resources

If external NAKALA platform resources are unavailable:

1. **Account Creation Issues**: 
   - Contact your institution's digital humanities center
   - Try alternative academic repositories temporarily
   - Use test environment for development and learning

2. **API Documentation Unavailable**:
   - Use O-Nakala Core's built-in help: `o-nakala-upload --help`
   - Refer to working examples in `examples/sample_dataset/`
   - Test commands with `--validate-only` flag first

3. **Platform Maintenance**:
   - Test environment may remain available during production maintenance
   - Development work can continue using preview tools offline
   - Documentation and examples are included in this repository

## API Key Examples by Institution

### Common Institution Patterns

Most French academic institutions have established NAKALA access procedures:

- **CNRS**: Contact your laboratory's data manager
- **Universities**: Check with library or digital humanities center
- **EFEO**: Contact IT services for API access
- **BnF**: Special institutional access procedures

### Workshop and Training Keys

For workshops, training sessions, or classroom use:

- **Use test environment only**
- **Test key**: `33170cfe-f53c-550b-5fb6-4814ce981293`
- **No personal data**: Only use example/synthetic datasets
- **Temporary use**: Not for production research data

## Advanced Configuration

### Multiple Environment Management

```bash
# Production
export NAKALA_PROD_KEY="your-prod-key"
export NAKALA_PROD_URL="https://api.nakala.fr"

# Test
export NAKALA_TEST_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_TEST_URL="https://apitest.nakala.fr"

# Switch environments
alias nakala-prod='export NAKALA_API_KEY=$NAKALA_PROD_KEY && export NAKALA_BASE_URL=$NAKALA_PROD_URL'
alias nakala-test='export NAKALA_API_KEY=$NAKALA_TEST_KEY && export NAKALA_BASE_URL=$NAKALA_TEST_URL'
```

### Configuration File Support

O-Nakala Core supports configuration files for repeated workflows:

```json
{
  "api_key": "${NAKALA_API_KEY}",
  "api_url": "https://apitest.nakala.fr",
  "default_status": "pending",
  "default_language": "fr",
  "timeout": 300
}
```

Save as `nakala-config.json` and use with `--config` parameter.