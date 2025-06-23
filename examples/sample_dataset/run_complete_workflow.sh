#!/bin/bash
set -e

# Complete O-Nakala Core Workflow - One Script Execution
# Usage: ./run_complete_workflow.sh YOUR_API_KEY

if [ -z "$1" ]; then
    echo "❌ Usage: $0 YOUR_API_KEY"
    echo "Example: $0 33170cfe-f53c-550b-5fb6-4814ce981293"
    exit 1
fi

API_KEY="$1"
echo "🚀 Starting O-Nakala Core Complete Workflow..."
echo "🔑 Using API Key: ${API_KEY:0:8}..."

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
echo "🤖 Step 2/4: Auto-generating metadata enhancements..."
python create_modifications.py upload_results.csv

# Step 3: Apply enhancements  
echo "✨ Step 3/4: Applying metadata enhancements..."
o-nakala-curator \
  --api-key "$API_KEY" \
  --batch-modify auto_data_modifications.csv \
  --scope datasets

# Step 4: Generate quality report
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