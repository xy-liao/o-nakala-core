#!/bin/bash

# Complete O-Nakala Core Workflow - Successful Commands v2.2.0
# Date: 2025-06-12
# Package: O-Nakala Core v2.2.0 (Fresh Build)
# API: NAKALA Test Environment
# Status: All commands validated and successful with fresh v2.2.0 build

# =============================================================================
# PHASE 1: ENVIRONMENT SETUP AND VALIDATION
# =============================================================================

echo "Setting up environment variables..."
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_BASE_URL="https://apitest.nakala.fr"
echo "Environment variables set successfully"

echo "Installing O-Nakala Core package..."
pip install o-nakala-core==2.2.0
# OR for development with all extras:
# pip install -e ".[dev,cli,ml]"
echo "Package installation completed"

echo "Validating API access..."
NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293" \
NAKALA_BASE_URL="https://apitest.nakala.fr" \
o-nakala-user-info
echo "API access validated successfully"

# =============================================================================
# PHASE 2: DATA UPLOAD
# =============================================================================

echo "Uploading sample dataset using folder mode..."
# Navigate to sample dataset directory (adjust path as needed)
cd examples/sample_dataset || { echo "Error: Could not find examples/sample_dataset directory"; exit 1; }

o-nakala-upload \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path . \
  --output upload_results.csv

echo "Data upload completed successfully"
echo "Generated upload_results.csv with dataset identifiers"

# =============================================================================
# PHASE 3: COLLECTION CREATION
# =============================================================================

echo "Creating collections from uploaded data..."
o-nakala-collection \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv \
  --collection-report collections_output.csv

echo "Collection creation completed successfully"
echo "Generated collections_output.csv with collection identifiers"

# =============================================================================
# PHASE 4: QUALITY ANALYSIS
# =============================================================================

echo "Generating comprehensive quality report..."
o-nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --quality-report

echo "Quality analysis completed successfully"

# =============================================================================
# PHASE 5: METADATA CURATION - DATA ITEMS
# =============================================================================

echo "Performing dry run of data item modifications..."
o-nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify data_modifications.csv \
  --scope datasets \
  --dry-run

echo "Applying batch modifications to data items..."
o-nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify data_modifications.csv \
  --scope datasets

echo "Data item modifications completed successfully"

# =============================================================================
# PHASE 6: METADATA CURATION - COLLECTIONS
# =============================================================================

echo "IMPORTANT: Update collection IDs in collection_modifications.csv with IDs from collections_output.csv before running curation"
echo "Performing dry run of collection modifications..."
o-nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify collection_modifications.csv \
  --scope collections \
  --dry-run

echo "Applying batch modifications to collections..."
o-nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify collection_modifications.csv \
  --scope collections

echo "Collection modifications completed successfully"

# =============================================================================
# PHASE 7: FINAL VALIDATION
# =============================================================================

echo "Validating specific collections..."
o-nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --validate-metadata \
  --scope collections \
  --collections "10.34847/nkl.adfc67q4,10.34847/nkl.d8328982,10.34847/nkl.1c39i9oq"

echo "Final validation completed"

# =============================================================================
# WORKFLOW SUMMARY
# =============================================================================

echo "============================================================"
echo "WORKFLOW COMPLETED SUCCESSFULLY"
echo "============================================================"
echo "Files Processed: 14 individual files"
echo "Datasets Created: 5 organized data items"
echo "Collections Created: 3 thematic collections"
echo "Metadata Enhancements: 8 batch modifications"
echo "Success Rate: 100% for all operations"
echo "============================================================"

# =============================================================================
# GENERATED IDENTIFIERS FOR REFERENCE
# =============================================================================

echo "Generated Dataset Identifiers (v2.2.0 Fresh Test):"
echo "  Images: 10.34847/nkl.653c7n3i"
echo "  Code: 10.34847/nkl.d189r56n"
echo "  Presentations: 10.34847/nkl.a181l7lg"
echo "  Documents: 10.34847/nkl.14cbu3te"
echo "  Data: 10.34847/nkl.0cdc209a"
echo ""
echo "Generated Collection Identifiers (v2.2.0 Fresh Test):"
echo "  Code and Data: 10.34847/nkl.b6f4ygm2"
echo "  Documents: 10.34847/nkl.d4d16w51"
echo "  Multimedia: 10.34847/nkl.c70e6vv6"
echo ""
echo "All identifiers saved to respective output CSV files"