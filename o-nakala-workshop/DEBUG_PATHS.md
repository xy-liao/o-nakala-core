# Debug Path Issues - Quick Reference

## 🔍 Current Path Structure
```
o-nakala-core/                          # Main project directory
├── nakala-client-upload-v2.py          # CLI scripts here
├── nakala-client-collection-v2.py
├── nakala-curator.py
├── src/nakala_client/                  # Package source
└── o-nakala-workshop/                  # Workshop directory (we are here)
    ├── NAKALA_Complete_Workflow.ipynb
    └── data/sample_dataset/
```

## 🧪 Debug Commands

### Check Current Location
```python
from pathlib import Path
print(f"Current directory: {Path.cwd()}")
print(f"Parent directory: {Path.cwd().parent}")
```

### Check Script Paths
```python
scripts = [
    "nakala-client-upload-v2.py",
    "nakala-client-collection-v2.py", 
    "nakala-curator.py"
]

for script in scripts:
    script_path = Path("..") / script
    print(f"{script}: {script_path.resolve()} - Exists: {script_path.exists()}")
```

### Check Data Paths
```python
data_dir = Path("data/sample_dataset")
csv_files = ["folder_data_items.csv", "folder_collections.csv"]

print(f"Data directory: {data_dir.resolve()} - Exists: {data_dir.exists()}")
for csv in csv_files:
    csv_path = data_dir / csv
    print(f"{csv}: {csv_path.resolve()} - Exists: {csv_path.exists()}")
```

## 🔧 Common Fixes

### If Scripts Not Found
```bash
# Make sure you're in the workshop directory
cd o-nakala-workshop

# Check parent directory has the scripts
ls ../nakala-*.py
```

### If Package Not Found
```bash
# Install in development mode
pip install -e ../

# Check installation
pip show nakala-client
```

### If API Key Issues
```python
# Use a public test key for immediate testing
API_KEY = "f41f5957-d396-3bb9-ce35-a4692773f636"  # unakala2 test account
```

## 🎯 Quick Test Cell

Add this cell to your notebook for debugging:

```python
# DEBUG: Check all paths and requirements
from pathlib import Path

print("🔍 PATH DEBUGGING")
print("=" * 50)

# Current location
print(f"📁 Current directory: {Path.cwd()}")
print(f"📁 Parent directory: {Path.cwd().parent}")

# Check scripts
scripts = ["nakala-client-upload-v2.py", "nakala-client-collection-v2.py", "nakala-curator.py"]
print(f"\n📜 SCRIPT CHECK:")
for script in scripts:
    path = Path("..") / script
    status = "✅" if path.exists() else "❌"
    print(f"{status} {script}: {path.resolve()}")

# Check data
print(f"\n📊 DATA CHECK:")
data_dir = Path("data/sample_dataset")
print(f"📁 Data directory: {data_dir.resolve()} - {'✅' if data_dir.exists() else '❌'}")

csv_files = ["folder_data_items.csv", "folder_collections.csv"]
for csv in csv_files:
    path = data_dir / csv
    status = "✅" if path.exists() else "❌"
    print(f"{status} {csv}: {path.resolve()}")

# Check package
try:
    import nakala_client
    print(f"\n📦 PACKAGE CHECK:")
    print(f"✅ nakala_client: {nakala_client.__file__}")
except ImportError:
    print(f"\n📦 PACKAGE CHECK:")
    print(f"❌ nakala_client not installed - run: pip install -e ../")

print(f"\n🔑 API KEY: {API_KEY[:8]}..." if API_KEY != "YOUR_API_KEY_HERE" else "\n🔑 API KEY: Not set")
```