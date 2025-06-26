# O-Nakala Core Quick Start Guide

## 🚀 **5-Minute Setup**

Get O-Nakala Core working in under 5 minutes with our validated test environment.

### **Step 1: Install** (1 minute)

```bash
# Clone the repository
git clone https://github.com/xy-liao/o-nakala-core.git
cd o-nakala-core

# Install with all features
pip install -e ".[dev,cli,ml]"
```

### **Step 2: Configure Environment** (1 minute)

```bash
# Set up validated test API key
export NAKALA_API_KEY="33170cfe-f53c-550b-5fb6-4814ce981293"
export NAKALA_API_URL="https://apitest.nakala.fr"
```

### **Step 3: Validate Setup** (1 minute)

```bash
# Quick validation test
python -c "
from src.o_nakala_core.upload import NakalaUploadClient
from src.o_nakala_core.common.config import NakalaConfig

config = NakalaConfig(
    api_key='33170cfe-f53c-550b-5fb6-4814ce981293',
    api_url='https://apitest.nakala.fr',
    base_path='examples/sample_dataset'
)

client = NakalaUploadClient(config)
print('✅ O-Nakala Core is ready!')
"
```

### **Step 4: Test Enhanced 7-Step Workflow v2.4.0** (2 minutes)

```bash
# Navigate to sample dataset directory
cd examples/sample_dataset

# Run complete 7-step workflow with automatic cleanup
./run_workflow.sh 33170cfe-f53c-550b-5fb6-4814ce981293 --cleanup

# OR test validation only (without actual upload)
o-nakala-upload \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path . \
  --validate-only
```

**🎉 Success!** The workflow creates 5 datasets + 3 collections with metadata enhancement and automatically cleans up test data.

### **What the 7-Step Workflow Does:**
1. **Upload** - 5 datasets from sample files
2. **Collections** - 3 thematic collections created 
3. **Enhancement** - Metadata generated for datasets AND collections
4. **Dataset Curation** - Updated titles, descriptions, keywords applied
5. **Collection Curation** - Metadata applied to collections
6. **Quality Analysis** - Comprehensive report generated
7. **Cleanup** - Test data automatically removed (with `--cleanup`)

---

## **Production Workflow Example (7 Steps)**

### **Complete Workflow**

```bash
# Step 1-2: Upload datasets and create collections
o-nakala-upload \
  --api-key "$NAKALA_API_KEY" \
  --dataset "your_data/folder_data_items.csv" \
  --base-path "your_data" \
  --mode "folder" \
  --output "upload_results.csv"

o-nakala-collection \
  --api-key "$NAKALA_API_KEY" \
  --from-folder-collections "your_data/collections.csv" \
  --from-upload-output "upload_results.csv" \
  --collection-report "collections_output.csv"

# Step 3: Generate metadata enhancements
python create_modifications.py upload_results.csv
python create_collection_modifications.py collections_output.csv

# Step 4-5: Apply metadata to datasets and collections
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify auto_data_modifications.csv \
  --scope datasets

o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify auto_collection_modifications.csv \
  --scope collections

# Step 6: Generate quality report
o-nakala-curator \
  --api-key "$NAKALA_API_KEY" \
  --quality-report \
  --scope datasets \
  --output "quality_report.json"
```

### **Enhance Metadata**

```bash
# Apply metadata improvements
python -m src.o_nakala_core.curator \
  --api-key "$NAKALA_API_KEY" \
  --batch-modify "your_data/modifications.csv" \
  --output "curation_results.csv"
```

---

## **Key Features Validated**

✅ **Multi-format Upload**: Images, documents, code, data files  
✅ **Smart Collections**: Automatic organization from folder patterns  
✅ **Multilingual Metadata**: French/English support  
✅ **Batch Operations**: Process multiple items efficiently  
✅ **Error Recovery**: Robust error handling and validation  
✅ **CLI & Python API**: Use from command line or Python scripts  

---

## **Next Steps**

- **📖 Full Documentation**: [README.md](README.md)
- **🔧 Development Setup**: [docs/DEVELOPMENT_ENVIRONMENT.md](docs/DEVELOPMENT_ENVIRONMENT.md)
- **📋 Workflow Examples**: [examples/workflow_documentation/](examples/workflow_documentation/)
- **🧪 API Reference**: [api/](api/)

---

## **Support**

- **🐛 Issues**: [GitHub Issues](https://github.com/xy-liao/o-nakala-core/issues)
- **📚 NAKALA Docs**: [nakala.fr/documentation](https://nakala.fr/documentation)
- **💬 Questions**: Check existing issues or create a new one

---

**Ready to manage your research data like a pro!** 🎓