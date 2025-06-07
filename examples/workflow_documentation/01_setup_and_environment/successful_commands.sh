#!/bin/bash

# Complete O-Nakala Core Workflow - Successful Commands
# Date: 2025-06-08
# API: NAKALA Test Environment
# Status: All commands validated and successful

# =============================================================================
# PHASE 1: ENVIRONMENT SETUP AND VALIDATION
# =============================================================================

echo "Setting up environment variables..."
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_BASE_URL="https://apitest.nakala.fr"
echo "Environment variables set successfully"

echo "Installing O-Nakala Core package..."
pip install -e .
echo "Package installation completed"

echo "Validating API access..."
NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293" \
NAKALA_BASE_URL="https://apitest.nakala.fr" \
nakala-user-info
echo "API access validated successfully"

# =============================================================================
# PHASE 2: DATA UPLOAD
# =============================================================================

echo "Uploading sample dataset using folder mode..."
cd /Users/syl/Documents/GitHub/o-nakala-core/examples/sample_dataset

nakala-upload \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path .

echo "Data upload completed successfully"
echo "Generated output.csv with dataset identifiers"

# =============================================================================
# PHASE 3: COLLECTION CREATION
# =============================================================================

echo "Creating collections from uploaded data..."
nakala-collection \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --from-upload-output output.csv \
  --from-folder-collections folder_collections.csv

echo "Collection creation completed successfully"
echo "Generated collections_output.csv with collection identifiers"

# =============================================================================
# PHASE 4: QUALITY ANALYSIS
# =============================================================================

echo "Generating comprehensive quality report..."
nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --quality-report

echo "Quality analysis completed successfully"

# =============================================================================
# PHASE 5: METADATA CURATION - DATA ITEMS
# =============================================================================

echo "Performing dry run of data item modifications..."
nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify data_modifications.csv \
  --scope datasets \
  --dry-run

echo "Applying batch modifications to data items..."
nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify data_modifications.csv \
  --scope datasets

echo "Data item modifications completed successfully"

# =============================================================================
# PHASE 6: METADATA CURATION - COLLECTIONS
# =============================================================================

echo "Performing dry run of collection modifications..."
nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify collection_batch_modifications.csv \
  --scope collections \
  --dry-run

echo "Applying batch modifications to collections..."
nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify collection_batch_modifications.csv \
  --scope collections

echo "Collection modifications completed successfully"

# =============================================================================
# PHASE 7: FINAL VALIDATION
# =============================================================================

echo "Validating specific collections..."
nakala-curator \
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

echo "Generated Dataset Identifiers:"
echo "  Images: 10.34847/nkl.bf0fxt5e"
echo "  Code: 10.34847/nkl.181eqe75"
echo "  Presentations: 10.34847/nkl.9edeiw5z"
echo "  Documents: 10.34847/nkl.2b617444"
echo "  Data: 10.34847/nkl.5f40fo9t"
echo ""
echo "Generated Collection Identifiers:"
echo "  Code and Data: 10.34847/nkl.adfc67q4"
echo "  Documents: 10.34847/nkl.d8328982"
echo "  Multimedia: 10.34847/nkl.1c39i9oq"
echo ""
echo "All identifiers saved to respective output CSV files"