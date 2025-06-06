# Project Consolidation Plan

## 🎯 **Goal**: Clean, professional project ready for GitHub public + PyPI publication

## 📊 **Current Issues**

### **1. Script Redundancy** 
- ❌ **v1.0 Legacy Scripts**: `nakala-client-upload.py` (23KB), `nakala-client-collection.py` (27KB)
- ❌ **v2.0 Thin Wrappers**: `nakala-client-upload-v2.py` (533 bytes), `nakala-client-collection-v2.py` (545 bytes)
- ✅ **Solution**: Remove both, use CLI entry points from setup.py

### **2. Documentation Mess**
- ❌ **3 Doc Structures**: `docs/`, `docs_organized/`, multiple READMEs
- ✅ **Solution**: Keep `docs_organized/`, remove `docs/`, single root README.md

### **3. Dataset Duplication**
- ❌ **3 Copies**: Root, docs, workshop
- ✅ **Solution**: Keep workshop copy, symlink others or remove

### **4. Output File Clutter**
- ❌ **Files Everywhere**: `*.csv`, `*.log`, `*.json` in root
- ✅ **Solution**: Move to `.gitignore` or archive

### **5. Complex CLI Architecture**
- ❌ **Wrapper Scripts**: v2.py files call src/nakala_client/
- ✅ **Solution**: Direct CLI entry points via setup.py

## 🚀 **Consolidation Steps**

### **Phase 1: Remove Legacy Scripts** ✅
```bash
# Remove v1.0 legacy
rm nakala-client-upload.py
rm nakala-client-collection.py

# Remove v2.0 wrappers (replaced by setup.py entry points)
rm nakala-client-upload-v2.py  
rm nakala-client-collection-v2.py
rm nakala-user-info.py

# Keep only essential
# nakala-curator.py (main functionality)
```

### **Phase 2: Clean Documentation** 📚
```bash
# Remove old docs
rm -rf docs/

# Keep organized docs as main docs
mv docs_organized/ docs/

# Clean up duplicate READMEs
# Keep only: README.md (root), docs/README.md
```

### **Phase 3: Dataset Cleanup** 🗂️
```bash
# Remove duplicates
rm -rf sample_dataset/           # Keep workshop version
rm -rf simple-dataset/          # Move to docs/examples/

# Consolidate in docs/examples/
mv o-nakala-workshop/data/sample_dataset/ docs/examples/
ln -s docs/examples/sample_dataset/ o-nakala-workshop/data/sample_dataset
```

### **Phase 4: Output Cleanup** 🧹
```bash
# Move output files
mkdir -p archive/
mv *.csv *.json *.log archive/ 2>/dev/null || true
mv output_archive/ archive/legacy/
mv test_workflow_output/ archive/test/

# Update .gitignore
echo "archive/" >> .gitignore
```

### **Phase 5: CLI Modernization** ⚙️
```bash
# Test CLI entry points work
nakala-upload --help
nakala-collection --help  
nakala-curator --help

# Verify no wrapper scripts needed
```

## 📦 **Post-Consolidation Structure**

```
nakala-client/                     # Clean project root
├── README.md                      # Single comprehensive README
├── LICENSE                        # MIT license
├── setup.py                       # Package configuration
├── pyproject.toml                 # Modern packaging
├── src/nakala_client/             # Main package
│   ├── upload.py                  # Core modules
│   ├── collection.py
│   ├── curator.py
│   ├── cli/                       # CLI entry points
│   └── common/                    # Shared utilities
├── docs/                          # Consolidated documentation
│   ├── README.md
│   ├── user-guides/              # User documentation
│   ├── developer/                 # Developer docs
│   └── examples/                  # Sample datasets
├── o-nakala-workshop/             # Workshop materials
│   ├── NAKALA_Complete_Workflow.ipynb
│   └── data/ -> ../docs/examples/ # Symlink to examples
├── tests/                         # Test suite
└── archive/                       # Historical materials (gitignored)
```

## ✅ **Benefits After Consolidation**

### **For Users**
- **Simple Installation**: `pip install nakala-client`
- **Clean CLI**: `nakala-upload`, `nakala-collection`, `nakala-curator`
- **Clear Documentation**: Single docs/ structure
- **Professional Appearance**: No clutter, clear purpose

### **For Developers**  
- **Maintainable Code**: No duplicate scripts
- **Standard Structure**: Follows Python packaging best practices
- **Easy Testing**: Clear separation of concerns
- **CI/CD Ready**: Clean structure for automated testing

### **For Publication**
- **GitHub Ready**: Professional, clean repository
- **PyPI Ready**: Standard package structure
- **Documentation Ready**: Organized, comprehensive docs
- **User Ready**: Clear examples and tutorials

## 🎯 **Success Criteria**

✅ **Repository Cleanliness**: No duplicate files, clear structure  
✅ **CLI Functionality**: All commands work via setup.py entry points  
✅ **Documentation Quality**: Single, comprehensive docs structure  
✅ **Workshop Integrity**: Workshop materials work seamlessly  
✅ **PyPI Readiness**: Package builds and installs correctly  

## ⏱️ **Estimated Time**

- **Script Cleanup**: 30 minutes
- **Documentation Consolidation**: 1 hour  
- **Dataset Organization**: 30 minutes
- **Testing & Validation**: 1 hour
- **Total**: ~3 hours for complete consolidation

## 🚨 **Risk Mitigation**

- **Backup**: Create git branch before consolidation
- **Testing**: Verify all functionality after each phase
- **Rollback Plan**: Keep archive/ for recovery if needed
- **Documentation**: Update README with new structure

---

**📝 Note**: This consolidation makes the project 10x more professional and ready for public release.