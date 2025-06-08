# Development Tools

This directory contains development tools and auto-generated components.

## 📁 Contents

### `/nakala-python-client/`
- **Purpose**: Auto-generated OpenAPI client for NAKALA API
- **Source**: Generated from official NAKALA OpenAPI specification
- **Size**: ~2MB (100+ auto-generated files)
- **Usage**: Reference implementation, model validation, API testing

### Notes
- These tools are for development purposes
- Auto-generated code should not be manually modified
- Use O-Nakala Core's main client (`src/nakala_client/`) for production

## 🔄 Regenerating OpenAPI Client

If needed, regenerate the client using:
```bash
# Using OpenAPI Generator
openapi-generator generate \
  -i https://apitest.nakala.fr/openapi.json \
  -g python \
  -o nakala-python-client/ \
  --package-name openapi_client
```

## 🎯 Production Usage

For production applications, use the main O-Nakala Core client:
```python
from nakala_client.upload import NakalaUpload
from nakala_client.collection import NakalaCollection
from nakala_client.curator import NakalaCurator
```