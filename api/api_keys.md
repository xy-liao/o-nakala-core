# NAKALA API Keys for Testing

**📖 PUBLIC TEST KEYS**: These are public API keys for the NAKALA test environment (https://apitest.nakala.fr) - safe to use for workshops and documentation.

## Available Test Accounts

| Account | Username | Password | API Key | Purpose | Status |
|---------|----------|----------|---------|---------|--------|
| Test 1 | tnakala | IamTesting2020 | 01234567-89ab-cdef-0123-456789abcdef | Basic testing | ⚠️ Untested |
| **Test 2** | **unakala1** | **IamTesting2020** | **33170cfe-f53c-550b-5fb6-4814ce981293** | **Full workflow** | **✅ VALIDATED** |
| Test 3 | unakala2 | IamTesting2020 | f41f5957-d396-3bb9-ce35-a4692773f636 | Collection testing | ⚠️ Untested |
| Test 4 | unakala3 | IamTesting2020 | aae99aba-476e-4ff2-2886-0aaf1bfa6fd2 | Curation testing | ⚠️ Untested |

## Getting Your API Key

1. **Create Account**: Register at https://apitest.nakala.fr
2. **Generate API Key**: Go to Profile → API Keys → Generate New Key
3. **Use in Scripts**: Replace `YOUR_API_KEY_HERE` with your actual key

## Workshop Quick Start

**RECOMMENDED**: Use the validated Test 2 key for reliable workflow testing:

```bash
# Validated key for complete workflow
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_API_URL="https://apitest.nakala.fr"

# Test complete workflow
python -m src.nakala_client.upload \
  --api-key "$NAKALA_API_KEY" \
  --api-url "$NAKALA_API_URL" \
  --dataset "examples/sample_dataset/folder_data_items.csv" \
  --base-path "examples/sample_dataset" \
  --mode "folder" \
  --validate-only
```

## Validation Status (2025-06-10)

**Key `33170cfe-f53c-550b-5fb6-4814ce981293` successfully tested for:**
- ✅ **Upload workflow**: 5 datasets created (14 files)
- ✅ **Collection creation**: 3 collections created automatically
- ✅ **Curator modifications**: 5 metadata enhancements applied
- ✅ **End-to-end workflow**: Complete 3-step process validated
- ✅ **Error handling**: Graceful failure handling
- ✅ **Multilingual support**: French/English metadata confirmed

## Security Notes

- ✅ **Test Keys**: These are public test environment keys - safe to share
- ⚠️ **Production Keys**: Never share production API keys
- 🔐 **Personal Keys**: For production, create your own at https://nakala.fr
- 🧪 **Test Environment**: These keys only work on https://apitest.nakala.fr

## Creating Your Own API Key

For production use or personal projects:

1. **Register**: Create account at https://nakala.fr (production) or https://apitest.nakala.fr (test)
2. **Generate Key**: Profile → API Keys → Generate New Key
3. **Environment Variable**: `export NAKALA_API_KEY="your-personal-key"`