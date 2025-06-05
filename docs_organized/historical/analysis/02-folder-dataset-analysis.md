# Analysis: Handling Folder-Based Datasets in Nakala Scripts

## Current Sample Dataset Structure
```
sample_dataset/
├── files/
│   ├── code/
│   ├── data/
│   ├── documents/
│   ├── images/
│   └── presentations/
├── folder_collections.csv
└── folder_data_items.csv
```

## Is This a Good Practice? **YES, but with modifications**

### ✅ **Advantages of Folder-Based Approach**

1. **Natural Organization**: Matches how researchers typically organize their data
2. **Semantic Grouping**: Files are grouped by type and purpose
3. **Scalability**: Can handle large datasets with many files
4. **Preservation of Context**: Maintains relationships between related files
5. **Research Best Practices**: Aligns with FAIR data principles
6. **Collection Management**: Supports hierarchical collection creation

### ✅ **Perfect for Digital Humanities**

- **Multi-format Projects**: Your field often works with diverse file types (texts, images, code, data)
- **Complex Relationships**: Folder structure preserves intellectual relationships
- **Collaborative Work**: Teams can easily understand and navigate the structure
- **Long-term Preservation**: Hierarchical organization aids in data management
- **Collection Organization**: Supports research-driven collection creation

## Recommended Implementation Strategy

### 🔄 **Hybrid Approach: Extend Current Scripts**

Rather than completely rewriting, extend your existing scripts to handle both:
1. **File-based datasets** (current CSV approach)
2. **Folder-based datasets** (new functionality)
3. **Collection creation** (based on folder structure)

### 📋 **Implementation Plan**

#### 1. **Enhanced Upload Script** (`nakala-client-upload.py`)

```python
# Add new command-line options
parser.add_argument('--mode', choices=['csv', 'folder'], default='csv',
                   help='Upload mode: csv (current) or folder (new)')
parser.add_argument('--folder-config', 
                   help='Path to folder configuration CSV (for folder mode)')
```

#### 2. **Folder Processing Logic**

- **Auto-detect file types** based on extensions and folder names
- **Generate metadata** based on folder structure and naming conventions
- **Batch upload** entire folders as logical units
- **Maintain folder relationships** in Nakala
- **Support multilingual metadata** (fr|en format)

#### 3. **Collection Management**

- **Automatic collection creation** based on folder hierarchy
- **Hierarchical collections** (parent/child relationships)
- **Bulk operations** for folder-based uploads
- **Collection relationship management**
- **Multilingual collection metadata**

## Proposed Extended Architecture

### 🏗️ **New Classes to Add**

```python
class FolderDatasetProcessor:
    """Handles folder-based dataset processing"""
    
class FileTypeDetector:
    """Detects and categorizes file types"""
    
class MetadataGenerator:
    """Generates metadata from folder structure"""
    
class HierarchicalCollectionManager:
    """Manages nested collection structures"""
    
class CollectionRelationshipManager:
    """Manages relationships between collections"""
```

### 📊 **Enhanced CSV Format**

Your `folder_data_items.csv` and `folder_collections.csv` show good structure:

**Advantages:**
- ✅ Multilingual support (fr:|en:)
- ✅ Proper metadata fields
- ✅ Rights management
- ✅ Semantic typing
- ✅ Collection relationships
- ✅ Hierarchical organization

**Suggestions:**
- Add file path mapping
- Include MIME type detection
- Add validation rules
- Enhance relationship definitions

## Implementation Recommendations

### 🎯 **Phase 1: Extend Current Scripts**

1. **Add folder mode** to existing scripts
2. **Maintain backward compatibility**
3. **Use existing error handling and retry logic**
4. **Leverage current metadata handling**
5. **Implement collection creation**

### 🎯 **Phase 2: Advanced Features**

1. **Automatic metadata extraction** from files
2. **Batch validation** before upload
3. **Progress tracking** for large folder uploads
4. **Resume capability** for interrupted uploads
5. **Collection relationship management**

### 🎯 **Phase 3: Integration**

1. **Collection hierarchies** matching folder structure
2. **Relationship preservation** between files
3. **Search optimization** based on folder organization
4. **Enhanced collection reporting**
5. **Multilingual collection support**

## Code Structure Suggestion

```python
# In nakala-client-upload.py
class NakalaUploader:
    def __init__(self, ...):
        # existing code
        self.mode = 'csv'  # default
    
    def process_dataset(self):
        if self.mode == 'csv':
            return self._process_csv_dataset()
        elif self.mode == 'folder':
            return self._process_folder_dataset()
    
    def _process_folder_dataset(self):
        # New folder processing logic
        pass

# In nakala-client-collection.py
class NakalaCollectionManager:
    def __init__(self, ...):
        # existing code
    
    def create_collections_from_folder(self):
        # New folder-based collection creation
        pass
```

## Alternative: Separate Script?

### 🤔 **Consider a Third Option**: `nakala-client-folder.py`

**Pros:**
- Clean separation of concerns
- Specialized for folder operations
- No complexity added to existing scripts

**Cons:**
- Code duplication
- Multiple tools to maintain
- Less integrated workflow
- Harder to maintain collection relationships

## Final Recommendation

### ✅ **Extend Existing Scripts** (Recommended)

**Why this approach works best:**

1. **Maintains ecosystem coherence**
2. **Leverages existing robust error handling**
3. **Preserves your excellent architecture**
4. **Supports both workflows seamlessly**
5. **Fits digital humanities research patterns**
6. **Better collection relationship management**

### 🚀 **Next Steps**

1. Start with `--mode folder` option in upload script
2. Add folder configuration CSV parsing
3. Implement batch file processing
4. Extend collection script for hierarchical collections
5. Add comprehensive logging for folder operations
6. Implement collection relationship management

Your folder-based approach is **excellent for digital humanities research** and extending your current well-designed scripts is the optimal path forward.