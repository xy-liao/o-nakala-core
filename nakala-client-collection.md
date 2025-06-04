# Nakala Client Collection Script

A Python script for managing collections on the Nakala platform.

## Main Features:

1. **Create collection from upload output**: Uses the `output.csv` file from your upload script to automatically create a collection with all successfully uploaded data items.

2. **Create collection from data ID list**: Allows manual specification of data IDs for collection creation.

3. **Comprehensive metadata support**: Handles title, description, and keywords with proper Nakala metadata formatting.

4. **Error handling and retry logic**: Implements robust error handling with automatic retries for failed API calls.

## Usage Examples:

```bash
# Create collection from upload output
python nakala-client-collection.py \
    --api-key "your-api-key" \
    --title "My Bird Collection" \
    --description "A collection of bird photographs" \
    --keywords "birds,wildlife,photography" \
    --status private \
    --from-upload-output output.csv

# Create collection from specific data IDs
python nakala-client-collection.py \
    --api-key "your-api-key" \
    --title "Selected Images" \
    --description "Curated selection of images" \
    --keywords "selection,curated" \
    --status public \
    --data-ids "10.34847/nkl.f1c8y3w0,10.34847/nkl.3bdeo0xj"
```

## Integration with Your Workflow:

The script is designed to work seamlessly with your existing upload script. After running `nakala-client-upload.py`, you can immediately use the generated `output.csv` to create collections:

```bash
# Step 1: Upload data
python nakala-client-upload.py --api-key "your-api-key" --dataset dataset.csv --image-dir img/

# Step 2: Create collection from uploaded data
python nakala-client-collection.py --api-key "your-api-key" --title "Birds Collection" --from-upload-output output.csv
```

## Command Line Arguments:

- `--api-key`: (Required) Your Nakala API key
- `--api-url`: (Optional) Nakala API URL (default: https://apitest.nakala.fr)
- `--title`: (Required) Collection title
- `--description`: (Optional) Collection description
- `--keywords`: (Optional) Comma-separated keywords for the collection
- `--status`: (Optional) Collection status (private or public, default: private)
- `--from-upload-output`: Path to upload output CSV file (mutually exclusive with --data-ids)
- `--data-ids`: Comma-separated list of data IDs (mutually exclusive with --from-upload-output)

## Output:

The script provides detailed logging information and returns:
- Collection ID upon successful creation
- Error messages if creation fails
- Log file: `nakala_collection.log`

## Example Success Output:
```
Found 3 successfully uploaded data items
Successfully created collection: 10.34847/nkl.ddb6fj61
Collection 'Bird Collection' created successfully with ID: 10.34847/nkl.ddb6fj61
```

This approach gives you maximum flexibility while keeping the code modular and maintainable. Each script has a clear, focused responsibility, making them easier to test, debug, and extend.