#!/bin/bash
set -e

# Complete O-Nakala Core Workflow with Optional Cleanup
# Usage: ./run_workflow_with_cleanup.sh YOUR_API_KEY [--cleanup]

if [ -z "$1" ]; then
    echo "❌ Usage: $0 YOUR_API_KEY [--cleanup]"
    echo "Example: $0 33170cfe-f53c-550b-5fb6-4814ce981293"
    echo "         $0 33170cfe-f53c-550b-5fb6-4814ce981293 --cleanup"
    echo ""
    echo "Options:"
    echo "  --cleanup    Automatically cleanup test data after demonstration"
    exit 1
fi

API_KEY="$1"
CLEANUP_MODE="$2"

echo "🚀 Starting O-Nakala Core Complete Workflow..."
echo "🔑 Using API Key: ${API_KEY:0:8}..."

if [ "$CLEANUP_MODE" = "--cleanup" ]; then
    echo "🧹 Cleanup mode enabled - test data will be removed after demonstration"
fi

echo ""

# Step 1: Upload datasets
echo "📤 Step 1/4: Uploading datasets..."
o-nakala-upload \
  --api-key "$API_KEY" \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path . \
  --output upload_results.csv

# Step 2: Generate modifications
echo ""
echo "🤖 Step 2/4: Auto-generating metadata enhancements..."
python create_modifications.py upload_results.csv

# Step 3: Apply enhancements  
echo ""
echo "✨ Step 3/4: Applying metadata enhancements..."
o-nakala-curator \
  --api-key "$API_KEY" \
  --batch-modify auto_data_modifications.csv \
  --scope datasets

# Step 4: Generate quality report
echo ""
echo "📊 Step 4/4: Generating quality report..."
o-nakala-curator \
  --api-key "$API_KEY" \
  --quality-report \
  --scope datasets \
  --output quality_report.json

echo ""
echo "✅ Complete workflow finished successfully!"
echo "📋 Results:"
echo "   - upload_results.csv: Dataset identifiers" 
echo "   - auto_data_modifications.csv: Applied enhancements"
echo "   - quality_report.json: Comprehensive analysis"
echo ""
echo "🎯 Summary:"
DATASET_COUNT=$(tail -n +2 upload_results.csv | wc -l | tr -d ' ')
echo "   - ${DATASET_COUNT} datasets uploaded and enhanced"
echo "   - 100% automation achieved"
echo "   - All metadata professionally improved"
echo "   - Quality analysis completed"
echo ""
echo "🔗 First dataset ID: $(head -2 upload_results.csv | tail -1 | cut -d',' -f1)"
echo "🌐 Test in browser: https://test.nakala.fr/$(head -2 upload_results.csv | tail -1 | cut -d',' -f1)"

# Optional cleanup
if [ "$CLEANUP_MODE" = "--cleanup" ]; then
    echo ""
    echo "🧹 Cleanup Mode: Removing test data to keep platform clean..."
    echo "⏳ Waiting 3 seconds (press Ctrl+C to skip cleanup)..."
    sleep 3
    
    python cleanup_test_data.py "$API_KEY" --force
    
    echo ""
    echo "✨ Test platform cleaned! Ready for next user."
else
    echo ""
    echo "💡 To clean up test data later, run:"
    echo "   python cleanup_test_data.py $API_KEY"
    echo ""
    echo "🌍 Being considerate: Cleanup helps keep the test platform tidy for everyone!"
fi