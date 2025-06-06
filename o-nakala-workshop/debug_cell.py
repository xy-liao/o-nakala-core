# DEBUG CELL - Add this to your notebook for troubleshooting
# Copy and paste this into a new cell if you encounter path issues

from pathlib import Path

print("🔍 PATH DEBUGGING")
print("=" * 50)

# Current location
print(f"📁 Current directory: {Path.cwd()}")
print(f"📁 Parent directory: {Path.cwd().parent}")

# Check scripts with absolute paths
scripts = ["nakala-client-upload-v2.py", "nakala-client-collection-v2.py", "nakala-curator.py"]
print(f"\n📜 SCRIPT CHECK:")
for script in scripts:
    path = Path("..").resolve() / script
    status = "✅" if path.exists() else "❌"
    print(f"{status} {script}: {path}")

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

# Check API key
try:
    print(f"\n🔑 API KEY: {API_KEY[:8]}..." if API_KEY != "YOUR_API_KEY_HERE" else "\n🔑 API KEY: Not set")
except NameError:
    print(f"\n🔑 API KEY: Variable not defined")

print(f"\n💡 If any ❌ appears above, that's the issue to fix!")