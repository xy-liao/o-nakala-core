# Local Testing Guide - NAKALA Workshop

**🎯 Goal**: Test the workshop notebook locally while maintaining compatibility for future PyPI publication.

## 🚀 Quick Setup (Recommended)

### Step 1: Install in Development Mode
```bash
cd o-nakala-workshop
pip install -e ../
```

### Step 2: Test Installation
```bash
python test_local_setup.py
```

### Step 3: Run Workshop
```bash
jupyter lab NAKALA_Complete_Workflow.ipynb
```

## 🔧 Detailed Setup Options

### Option A: Development Installation (Best for Testing)
```bash
# From workshop directory
cd o-nakala-workshop

# Install nakala-client in editable mode
pip install -e ../

# This creates a link to your source code
# Changes in ../src/nakala_client/ are immediately available
```

**Benefits:**
- ✅ Immediate code changes reflected
- ✅ PyPI-compatible imports work
- ✅ CLI commands available
- ✅ Future-proof

### Option B: Direct Path Method (Fallback)
```bash
# The notebook automatically adds parent directory to Python path
# No installation required, but less clean
```

**Benefits:**
- ✅ No installation needed
- ✅ Works immediately
- ⚠️ Less PyPI-compatible

## 📊 Import Compatibility Matrix

| Method | Current Status | PyPI Ready | Workshop Works |
|--------|----------------|------------|----------------|
| `pip install -e ../` | ✅ Works | ✅ Yes | ✅ Perfect |
| Path manipulation | ✅ Works | ⚠️ Needs change | ✅ Good |
| `pip install nakala-client` | ❌ Not published | ✅ Future | ✅ Perfect |

## 🧪 Testing Your Setup

### Quick Test
```python
# Test 1: Import check
try:
    from nakala_client.common.config import NakalaConfig
    print("✅ PyPI-style imports work")
except ImportError:
    print("⚠️ Using fallback method")

# Test 2: CLI check  
import subprocess
result = subprocess.run(["nakala-upload", "--help"], capture_output=True)
print("✅ CLI available" if result.returncode == 0 else "⚠️ CLI not available")
```

### Comprehensive Test
```bash
python test_local_setup.py
```

## 📝 Workshop Notebook Behavior

The notebook automatically detects your setup and adapts:

### Scenario 1: Development Installation
```python
# Notebook uses:
from nakala_client.upload import NakalaUploader
uploader = NakalaUploader(config)
result = uploader.upload_folder(...)
```

### Scenario 2: Fallback Mode
```python
# Notebook uses:
subprocess.run(["python", "../nakala-client-upload-v2.py", ...])
```

## 🔄 Migration Path to PyPI

### Current (Local Testing)
```bash
cd o-nakala-workshop
pip install -e ../                    # Development install
jupyter lab NAKALA_Complete_Workflow.ipynb
```

### Future (After PyPI Publication)
```bash
cd o-nakala-workshop  
pip install nakala-client[workshop]   # PyPI install
jupyter lab NAKALA_Complete_Workflow.ipynb
```

**The notebook code remains exactly the same!** 🎉

## 🐛 Troubleshooting

### Issue: Import Errors
```bash
# Solution: Reinstall in development mode
pip uninstall nakala-client
pip install -e ../
```

### Issue: CLI Commands Not Found
```bash
# Check installation
pip show nakala-client

# If not found, reinstall
pip install -e ../
```

### Issue: Module Not Found in Jupyter
```python
# In notebook, restart kernel after installation
# Kernel → Restart & Clear Output
```

### Issue: Changes Not Reflected
```bash
# Development install should auto-reload
# If not working, reinstall:
pip install -e ../ --force-reinstall
```

## 🎯 Recommended Workflow

### For Your Colleagues (Testing)
1. **Clone repository** (when you share it)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Install nakala-client**: `pip install -e ../`
4. **Test setup**: `python test_local_setup.py`
5. **Run workshop**: `jupyter lab NAKALA_Complete_Workflow.ipynb`

### For Future Users (Post-PyPI)
1. **Install package**: `pip install nakala-client[workshop]`
2. **Download workshop**: `git clone` or download zip
3. **Run workshop**: `jupyter lab NAKALA_Complete_Workflow.ipynb`

## 💡 Pro Tips

### Development Efficiency
- **Use development install** for testing code changes
- **Keep workshop directory clean** - no src code modifications needed
- **Test both import methods** to ensure compatibility

### Future Compatibility  
- **Import statements** are already PyPI-ready
- **CLI commands** work identically
- **Configuration patterns** match PyPI standards

### Sharing with Colleagues
```bash
# Package everything for sharing
tar -czf nakala-workshop.tar.gz o-nakala-core/
```

They just need:
```bash
tar -xzf nakala-workshop.tar.gz
cd o-nakala-core/o-nakala-workshop
pip install -e ../
jupyter lab NAKALA_Complete_Workflow.ipynb
```

---

**🎉 You're all set for local testing with future PyPI compatibility!**