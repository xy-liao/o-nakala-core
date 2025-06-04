# Collection Workflow for Folder-Based Datasets

## ✅ **Perfect Workflow Design**

Your proposed workflow is **exactly right** for digital humanities research:

```
Step 1: Upload data items by folder
nakala-client-upload.py --mode folder → output.csv (with Nakala IDs)

Step 2: Create collections from uploaded items  
nakala-client-collection.py + folder_collections.csv → organized collections
```

## 🎯 **Why This Approach is Ideal**

### **1. Separation of Concerns**
- **Upload script**: Focuses on data preservation and technical upload
- **Collection script**: Focuses on intellectual organization and discovery

### **2. Flexibility for Research**
- Upload all data first (ensures preservation)
- Organize into multiple collections later (supports different research views)
- Modify collections without re-uploading data

### **3. Matches Your Sample Data Structure**
Looking at your `output.csv`, you have 5 data items uploaded by folder type:
- `10.34847/nkl.5ac8e116` (Images)
- `10.34847/nkl.bbeafl2j` (Code)  
- `10.34847/nkl.1bb1n159` (Presentations)
- `10.34847/nkl.2cfcmmd0` (Documents)
- `10.34847/nkl.ede83ze5` (Data)

Your `folder_collections.csv` defines 3 logical collections:
- "Code and Data Collection" (code + data items)
- "Documents Collection" (documents)
- "Multimedia Collection" (images + presentations)

## 🚀 **Enhanced Collection Script Implementation**

You need to extend `nakala-client-collection.py` to handle `folder_collections.csv`:

### **New Command-Line Option:**
```python
parser.add_argument('--from-folder-collections',
                   help='Path to folder collections CSV file')
```

### **New Method to Add:**
```python
def create_collections_from_folder_config(self, output_csv: str, folder_collections_csv: str):
    """Create collections based on folder collections configuration."""
    
    # 1. Read uploaded data items and map by folder type
    uploaded_items = {}
    with open(output_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['status'] == 'OK':
                # Extract folder type from title (e.g., "fr:Fichiers de code|en:Code Files")
                title = row['title']
                uploaded_items[title] = row['identifier']
    
    # 2. Read folder collections configuration
    with open(folder_collections_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for collection_config in reader:
            # 3. Create each collection
            self._create_single_collection_from_config(collection_config, uploaded_items)

def _create_single_collection_from_config(self, config: Dict, uploaded_items: Dict):
    """Create a single collection from folder configuration."""
    
    # Parse data items that should be in this collection
    data_item_folders = config['data_items'].split('|')
    collection_data_ids = []
    
    # Map folder paths to actual uploaded data IDs
    for folder_path in data_item_folders:
        # Find corresponding uploaded item
        for title, data_id in uploaded_items.items():
            if self._matches_folder_type(folder_path, title):
                collection_data_ids.append(data_id)
    
    if not collection_data_ids:
        logger.warning(f"No data items found for collection: {config['title']}")
        return
    
    # Prepare multilingual metadata
    metas = self._prepare_collection_metadata_from_config(config)
    
    # Create collection
    collection_data = {
        "status": config['status'],
        "datas": collection_data_ids,
        "metas": metas,
        "rights": []
    }
    
    result = self.create_collection(collection_data)
    logger.info(f"Created collection: {config['title']}")
```

## 📋 **Complete Workflow Example**

### **Step 1: Upload folder-based dataset**
```bash
python nakala-client-upload.py \
    --mode folder \
    --dataset sample_dataset/files \
    --folder-config sample_dataset/folder_data_items.csv \
    --api-key "your-key"
```
**Result**: `output.csv` with 5 data items

### **Step 2: Create collections from uploaded data**
```bash
python nakala-client-collection.py \
    --api-key "your-key" \
    --from-folder-collections sample_dataset/folder_collections.csv \
    --from-upload-output output.csv
```
**Result**: 3 collections created according to `folder_collections.csv`

## 🎯 **Expected Collections Created**

Based on your sample data:

### **Collection 1: "Code and Data Collection"**
- Contains: Code files + Data files
- Data IDs: `10.34847/nkl.bbeafl2j`, `10.34847/nkl.ede83ze5`
- Multilingual title: fr:Collection de Code et Données |en:Code and Data Collection

### **Collection 2: "Documents Collection"**  
- Contains: Documents
- Data IDs: `10.34847/nkl.2cfcmmd0`
- Multilingual title: fr:Collection de Documents|en:Documents Collection

### **Collection 3: "Multimedia Collection"**
- Contains: Images + Presentations  
- Data IDs: `10.34847/nkl.5ac8e116`, `10.34847/nkl.1bb1n159`
- Multilingual title: fr:Collection Multimédia|en:Multimedia Collection

## 🏆 **Benefits of This Approach**

### **For Digital Humanities Research:**
1. **Flexible Organization**: Same data can be in multiple collections
2. **Research-Driven**: Collections reflect intellectual organization, not just technical structure
3. **Multilingual Support**: Collections support international collaboration
4. **Preservation First**: Data is safely uploaded before organization

### **For Technical Management:**
1. **Robust Workflow**: Two-step process is more reliable
2. **Error Recovery**: Can recreate collections without re-uploading data
3. **Scalable**: Works for any size dataset
4. **Maintainable**: Clear separation of concerns

## 🚀 **Implementation Priority**

**High Priority Enhancement**: Add `--from-folder-collections` option to your collection script. This will complete your excellent folder-based workflow design.

Your approach is **perfect for digital humanities research workflows** - it separates data preservation (upload) from intellectual organization (collections), which is exactly how researchers think about their data!