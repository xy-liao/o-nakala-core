# CSV Templates

This directory contains ready-to-use CSV templates for O-Nakala Core operations.

## Available Templates

### Upload Templates
- **[basic_upload_template.csv](basic_upload_template.csv)** - Basic template for uploading files to NAKALA
- **[collection_template.csv](collection_template.csv)** - Template for creating collections

## Usage

1. Copy the appropriate template
2. Replace placeholder values with your data
3. Use with O-Nakala Core commands:

```bash
# Upload using template
o-nakala-upload --dataset your_filled_template.csv --mode folder

# Create collections using template  
o-nakala-collection --from-folder-collections your_collection_template.csv
```

## Field Reference

For complete field specifications, see:
- [Upload CSV Format](../../docs/endpoints/upload-endpoint/csv-format-specification.md)
- [Collection CSV Format](../../docs/endpoints/collection-endpoint/csv-format-specification.md)
- [Field Reference](../../docs/curator-field-reference.md)