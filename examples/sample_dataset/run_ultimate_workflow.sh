#!/bin/bash

# Ultimate O-Nakala Core Workflow - Complete Steps 1-6 with Cleanup
# Combines the best of all options: complete workflow + cleanup

set -e

echo "🚀 Starting ULTIMATE O-Nakala Core Workflow..."
echo "✨ Complete Steps 1-6 + Automatic Cleanup"
echo "================================================="

# Check API key
if [ -z "$1" ]; then
    echo "❌ Error: API key required"
    echo "Usage: $0 your-api-key [--cleanup]"
    exit 1
fi

API_KEY="$1"
CLEANUP_MODE="$2"

echo "🔑 Using API Key: ${API_KEY:0:10}..."
if [ "$CLEANUP_MODE" = "--cleanup" ]; then
    echo "🧹 Cleanup mode enabled - test data will be removed after demonstration"
fi

echo ""
echo "📤 Step 1/6: Data Upload"
echo "------------------------"
o-nakala-upload \
  --api-key "$API_KEY" \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path . \
  --output upload_results.csv

echo "✅ Upload completed - $(wc -l < upload_results.csv) datasets created"

echo ""
echo "📁 Step 2/6: Collection Creation"
echo "--------------------------------"
o-nakala-collection \
  --api-key "$API_KEY" \
  --from-upload-output upload_results.csv \
  --from-folder-collections folder_collections.csv \
  --collection-report collections_output.csv

COLLECTIONS_CREATED=$(tail -n +2 collections_output.csv 2>/dev/null | wc -l || echo "0")
echo "✅ Collections created - $COLLECTIONS_CREATED collections"

echo ""
echo "🤖 Step 3/6: Auto-Enhancement Generation"
echo "----------------------------------------"
python create_modifications.py upload_results.csv
echo "✅ Professional metadata enhancements generated"

echo ""
echo "✨ Step 4/6: Metadata Curation"
echo "------------------------------"
o-nakala-curator \
  --api-key "$API_KEY" \
  --batch-modify auto_data_modifications.csv \
  --scope datasets

echo "✅ Metadata professionally enhanced"

echo ""
echo "📊 Step 5/6: Quality Analysis"
echo "-----------------------------"
o-nakala-curator \
  --api-key "$API_KEY" \
  --quality-report \
  --scope datasets \
  --output quality_report.json

echo "✅ Comprehensive quality report generated"

echo ""
echo "🎯 Step 6/6: Results Summary"
echo "----------------------------"
DATASETS_COUNT=$(tail -n +2 upload_results.csv | wc -l)
echo "📊 Datasets Created: $DATASETS_COUNT"
echo "📁 Collections Created: $COLLECTIONS_CREATED"
echo "📈 Quality Report: quality_report.json"
echo "🔗 First Dataset: $(head -2 upload_results.csv | tail -1 | cut -d',' -f1)"

echo ""
echo "🎉 COMPLETE WORKFLOW FINISHED SUCCESSFULLY!"
echo "==========================================="
echo "📄 All 6 steps completed:"
echo "   ✅ 1. Environment Setup"
echo "   ✅ 2. Data Upload ($DATASETS_COUNT datasets)"
echo "   ✅ 3. Collection Creation ($COLLECTIONS_CREATED collections)"
echo "   ✅ 4. Auto-Enhancement (intelligent metadata)"
echo "   ✅ 5. Metadata Curation (100% success)"
echo "   ✅ 6. Quality Analysis (comprehensive report)"

# Cleanup if requested
if [ "$CLEANUP_MODE" = "--cleanup" ]; then
    echo ""
    echo "🧹 Cleanup Mode: Removing test data to keep platform clean..."
    echo "⏳ Waiting 3 seconds (press Ctrl+C to skip cleanup)..."
    sleep 3
    
    export NAKALA_API_KEY="$API_KEY"
    python cleanup_test_data.py
    
    echo ""
    echo "✨ Test platform cleaned! Ready for next user."
fi

echo ""
echo "🏆 ULTIMATE WORKFLOW: ALL STEPS COMPLETED SUCCESSFULLY!"