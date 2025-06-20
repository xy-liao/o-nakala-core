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

### **Step 4: Test Complete Workflow v2.2.0** (2 minutes)

```bash
# Navigate to sample dataset directory
cd examples/sample_dataset

# Test upload validation with folder mode (v2.2.0 validated)
o-nakala-upload \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path . \
  --validate-only

# Test collection validation (v2.2.0 validated)
o-nakala-collection \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --from-folder-collections folder_collections.csv \
  --validate-only
```

**🎉 Success!** If both commands complete without errors, you're ready to use O-Nakala Core.

---

## **Production Workflow Example**

### **Upload Research Data**

```bash
# Upload your research files
python -m src.o_nakala_core.upload \
  --api-key "$NAKALA_API_KEY" \
  --dataset "your_data/folder_data_items.csv" \
  --base-path "your_data" \
  --mode "folder" \
  --output "upload_results.csv"
```

### **Create Collections**

```bash
# Organize uploads into collections
python -m src.o_nakala_core.collection \
  --api-key "$NAKALA_API_KEY" \
  --from-folder-collections "your_data/collections.csv" \
  --from-upload-output "upload_results.csv" \
  --collection-report "collections_output.csv"
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