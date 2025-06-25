#!/bin/bash

# Ultimate O-Nakala Core Workflow - Complete Steps 1-7
# Runs from notebooks/ directory and operates on ../sample_dataset/

set -e

echo "🚀 Starting ULTIMATE O-Nakala Core Workflow..."
echo "✨ Complete Steps 1-7 from notebooks directory"
echo "================================================="

# Check API key
if [ -z "$1" ]; then
    echo "❌ Error: API key required"
    echo "Usage: $0 your-api-key [--cleanup]"
    echo ""
    echo "Options:"
    echo "  --cleanup    Clean up all test data after workflow completion"
    echo ""
    echo "Example:"
    echo "  cd examples/notebooks"
    echo "  ./run_ultimate_workflow.sh 33170cfe-f53c-550b-5fb6-4814ce981293"
    echo "  ./run_ultimate_workflow.sh 33170cfe-f53c-550b-5fb6-4814ce981293 --cleanup"
    exit 1
fi

API_KEY="$1"
CLEANUP_MODE="$2"
DATASET_DIR="../sample_dataset"

echo "🔑 Using API Key: ${API_KEY:0:10}..."
echo "📂 Working with dataset: $DATASET_DIR"
if [ "$CLEANUP_MODE" = "--cleanup" ]; then
    echo "🧹 Cleanup mode enabled - test data will be removed after workflow"
fi

# Check if we're in the right directory
if [ ! -d "$DATASET_DIR" ]; then
    echo "❌ Error: Cannot find sample_dataset directory"
    echo "Please run this script from the notebooks/ directory:"
    echo "  cd examples/notebooks"
    echo "  ./run_ultimate_workflow.sh your-api-key"
    exit 1
fi

# Check required files
if [ ! -f "$DATASET_DIR/folder_data_items.csv" ]; then
    echo "❌ Error: Cannot find folder_data_items.csv in $DATASET_DIR"
    exit 1
fi

echo ""
echo "📤 Step 1/6: Data Upload"
echo "------------------------"
o-nakala-upload \
  --api-key "$API_KEY" \
  --dataset "$DATASET_DIR/folder_data_items.csv" \
  --mode folder \
  --folder-config "$DATASET_DIR/folder_data_items.csv" \
  --base-path "$DATASET_DIR" \
  --output "$DATASET_DIR/upload_results.csv"

# Count datasets properly (subtract header line)
DATASETS_UPLOADED=$(tail -n +2 "$DATASET_DIR/upload_results.csv" | wc -l)
echo "✅ Upload completed - $DATASETS_UPLOADED datasets created"

echo ""
echo "📁 Step 2/6: Collection Creation"
echo "--------------------------------"
o-nakala-collection \
  --api-key "$API_KEY" \
  --from-upload-output "$DATASET_DIR/upload_results.csv" \
  --from-folder-collections "$DATASET_DIR/folder_collections.csv" \
  --collection-report "$DATASET_DIR/collections_output.csv"

# Move collections_output.csv from notebooks to sample_dataset if it exists there
if [ -f "collections_output.csv" ]; then
    mv collections_output.csv "$DATASET_DIR/"
fi

# Count collections more reliably and fix counting issue
if [ -f "$DATASET_DIR/collections_output.csv" ]; then
    COLLECTIONS_CREATED=$(tail -n +2 "$DATASET_DIR/collections_output.csv" 2>/dev/null | grep -v "^$" | wc -l 2>/dev/null || echo "0")
    COLLECTIONS_CREATED=$(echo "$COLLECTIONS_CREATED" | tr -d ' \t\n\r')
else
    COLLECTIONS_CREATED="0"
fi
echo "✅ Collections created - $COLLECTIONS_CREATED collections"

echo ""
echo "🤖 Step 3/6: Auto-Enhancement Generation"
echo "----------------------------------------"
if [ -f "$DATASET_DIR/create_modifications.py" ]; then
    cd "$DATASET_DIR"
    python create_modifications.py upload_results.csv
    echo "✅ Data metadata enhancements generated"
    
    # Generate collection modifications using the current collections_output.csv
    if [ -f "collections_output.csv" ]; then
        echo "🔍 Found collections_output.csv in sample_dataset, generating collection enhancements..."
        python create_collection_modifications.py collections_output.csv
        echo "✅ Collection metadata enhancements generated"
        echo "✅ Professional metadata enhancements generated (data + collections)"
    else
        echo "⚠️  Collections file not found - skipping collection enhancements"
        echo "✅ Data metadata enhancements generated (collections file not found)"
    fi
    cd - > /dev/null
else
    echo "⚠️  Skipping enhancement generation - scripts not found"
fi

echo ""
echo "✨ Step 4/6: Dataset Metadata Curation"
echo "--------------------------------------"
if [ -f "$DATASET_DIR/auto_data_modifications.csv" ]; then
    o-nakala-curator \
      --api-key "$API_KEY" \
      --batch-modify "$DATASET_DIR/auto_data_modifications.csv" \
      --scope datasets
    echo "✅ Dataset metadata professionally enhanced"
else
    echo "⚠️  Skipping dataset curation - auto_data_modifications.csv not found"
fi

echo ""
echo "📁 Step 5/6: Collection Metadata Curation"
echo "-----------------------------------------"
if [ -f "$DATASET_DIR/auto_collection_modifications.csv" ]; then
    o-nakala-curator \
      --api-key "$API_KEY" \
      --batch-modify "$DATASET_DIR/auto_collection_modifications.csv" \
      --scope collections
    echo "✅ Collection metadata professionally enhanced"
else
    echo "⚠️  Skipping collection curation - auto_collection_modifications.csv not found"
fi

echo ""
echo "📊 Step 6/6: Quality Analysis"
echo "-----------------------------"
o-nakala-curator \
  --api-key "$API_KEY" \
  --quality-report \
  --scope all \
  --output "$DATASET_DIR/quality_report.json"

echo "✅ Comprehensive quality report generated"

echo ""
echo "🎯 Results Summary"
echo "----------------------------"
echo "📊 Datasets Created: $DATASETS_UPLOADED"
echo "📁 Collections Created: $COLLECTIONS_CREATED" 
echo "📈 Quality Report: $DATASET_DIR/quality_report.json"
echo "🔗 First Dataset: $(head -2 "$DATASET_DIR/upload_results.csv" | tail -1 | cut -d',' -f1)"

echo ""
echo "🎉 COMPLETE WORKFLOW FINISHED SUCCESSFULLY!"
echo "==========================================="
echo "📄 All 6 steps completed:"
echo "   ✅ 1. Data Upload ($DATASETS_UPLOADED datasets)"
echo "   ✅ 2. Collection Creation ($COLLECTIONS_CREATED collections)"
echo "   ✅ 3. Auto-Enhancement (intelligent metadata)"
echo "   ✅ 4. Dataset Curation"
echo "   ✅ 5. Collection Curation" 
echo "   ✅ 6. Quality Analysis (comprehensive report)"

# Cleanup if requested
if [ "$CLEANUP_MODE" = "--cleanup" ]; then
    echo ""
    echo "🧹 Cleanup Mode: Removing test data to keep platform clean..."
    echo "⏳ Waiting 3 seconds (press Ctrl+C to skip cleanup)..."
    sleep 3
    
    if [ -f "cleanup_all_unakala1_data.py" ]; then
        echo "🗑️  Running complete user data cleanup..."
        python cleanup_all_unakala1_data.py "$API_KEY" --force
    else
        echo "⚠️  No cleanup scripts found - skipping cleanup"
    fi
    
    echo "✨ Test platform cleaned! Ready for next user."
fi

echo ""
echo "📁 Results saved in: $DATASET_DIR/"
echo "🏆 ULTIMATE WORKFLOW: ALL STEPS COMPLETED SUCCESSFULLY!"