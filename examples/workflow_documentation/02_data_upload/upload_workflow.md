# Data Upload Workflow

## Overview
This phase demonstrates the batch upload of research files organized by content type using O-Nakala Core's folder mode functionality.

> **📚 Documentation Reference**: For complete Upload endpoint documentation, CSV format specifications, and field transformations, see [Upload Endpoint Documentation](../../../docs/endpoints/upload-endpoint/README.md).

## Validation Status
**CSV File**: `folder_data_items.csv` ✅ **VALIDATED**  
**Validation Tool**: `tools/upload_validator.py`  
**Result**: 100% valid, generates 14 metadata entries per row

## Source Data Structure
The sample dataset contains 14 files organized into 5 content categories:

```
sample_dataset/files/
├── code/                    # 2 files
│   ├── analysis_data_cleaning.R
│   └── preprocess_data.py
├── data/                    # 2 files
│   ├── analysis_results_2023.csv
│   └── raw_survey_data_2023.csv
├── documents/               # 4 files
│   ├── paper_analysis_methods.md
│   ├── paper_literature_review.md
│   ├── paper_results_discussion.md
│   └── study_protocol_v1.0.md
├── images/                  # 3 files
│   ├── site_photograph_1.jpg
│   ├── site_photograph_2.jpg
│   └── temperature_trends_2023.png
└── presentations/           # 3 files
    ├── conference_presentation_2023.md
    ├── stakeholder_update_2023-06.md
    └── team_meeting_2023-04.md
```

## Configuration File Analysis

### folder_data_items.csv
This file defines the metadata for each folder/dataset:

```csv
file,status,type,title,alternative,author,contributor,date,license,description,keywords,language,temporal,spatial,accessRights,identifier,rights
files/code/,pending,http://purl.org/coar/resource_type/c_5ce6,fr:Fichiers de code|en:Code Files,...
files/data/,pending,http://purl.org/coar/resource_type/c_ddb1,fr:Données de recherche|en:Research Data,...
files/documents/,pending,http://purl.org/coar/resource_type/c_18cf,fr:Documents de recherche|en:Research Documents,...
files/images/,pending,http://purl.org/coar/resource_type/c_c513,fr:Collection d'images|en:Image Collection,...
files/presentations/,pending,http://purl.org/coar/resource_type/c_18cf,fr:Matériaux de présentation|en:Presentation Materials,...
```

### Key Features
- **Multilingual Support**: Titles and descriptions in French and English
- **COAR Resource Types**: Proper academic resource type classification
- **Structured Metadata**: Complete Dublin Core compatible fields
- **Access Rights**: Open Access with CC-BY-4.0 licensing

## Upload Command

### Successful Execution
```bash
cd /Users/syl/Documents/GitHub/o-nakala-core/examples/sample_dataset

nakala-upload \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --dataset folder_data_items.csv \
  --mode folder \
  --folder-config folder_data_items.csv \
  --base-path .
```

### Parameters Explained
- `--dataset`: CSV configuration file defining folder metadata
- `--mode folder`: Process directories as individual datasets
- `--folder-config`: Same file used for folder definitions
- `--base-path .`: Current directory as base for relative paths

## Upload Results

### Processing Log
```
2025-06-08 00:09:45,637 - Successfully uploaded: temperature_trends_2023.png
2025-06-08 00:09:46,369 - Successfully uploaded: site_photograph_2.jpg
2025-06-08 00:09:46,449 - Successfully uploaded: site_photograph_1.jpg
2025-06-08 00:09:49,638 - Successfully created dataset: 10.34847/nkl.bf0fxt5e
2025-06-08 00:09:49,727 - Successfully uploaded: preprocess_data.py
2025-06-08 00:09:49,857 - Successfully uploaded: analysis_data_cleaning.R
2025-06-08 00:09:50,026 - Successfully created dataset: 10.34847/nkl.181eqe75
2025-06-08 00:09:50,107 - Successfully uploaded: team_meeting_2023-04.md
2025-06-08 00:09:50,187 - Successfully uploaded: conference_presentation_2023.md
2025-06-08 00:09:50,269 - Successfully uploaded: stakeholder_update_2023-06.md
2025-06-08 00:09:50,443 - Successfully created dataset: 10.34847/nkl.9edeiw5z
2025-06-08 00:09:50,518 - Successfully uploaded: paper_literature_review.md
2025-06-08 00:09:50,608 - Successfully uploaded: study_protocol_v1.0.md
2025-06-08 00:09:50,695 - Successfully uploaded: paper_analysis_methods.md
2025-06-08 00:09:50,777 - Successfully uploaded: paper_results_discussion.md
2025-06-08 00:09:50,980 - Successfully created dataset: 10.34847/nkl.2b617444
2025-06-08 00:09:51,058 - Successfully uploaded: analysis_results_2023.csv
2025-06-08 00:09:51,141 - Successfully uploaded: raw_survey_data_2023.csv
2025-06-08 00:09:51,326 - Successfully created dataset: 10.34847/nkl.5f40fo9t
2025-06-08 00:09:51,327 - Upload process completed successfully
```

### Generated Identifiers
| Content Type | Dataset ID | Files Count |
|-------------|------------|-------------|
| Images | 10.34847/nkl.bf0fxt5e | 3 |
| Code | 10.34847/nkl.181eqe75 | 2 |
| Presentations | 10.34847/nkl.9edeiw5z | 3 |
| Documents | 10.34847/nkl.2b617444 | 4 |
| Data | 10.34847/nkl.5f40fo9t | 2 |

## Output File Structure

### upload_output.csv
The upload process generates a comprehensive output file tracking all created datasets:

```csv
identifier,files,title,status,response
10.34847/nkl.bf0fxt5e,"temperature_trends_2023.png,adc83b19e793491b1c6ea0fd8b46cd9f32e592fc,site_photograph_2.jpg,f5b02aa456a714d4daf81199e0e58eb6a84b504d,site_photograph_1.jpg,0cd7534987b9d695281c77ffa715172bedfb0e3c",fr:Collection d'images|en:Image Collection,OK,"{""code"": 201, ""message"": ""Data created"", ""payload"": {""id"": ""10.34847/nkl.bf0fxt5e""}}"
```

### Key Information Captured
- **Dataset Identifiers**: Persistent DOI-style identifiers
- **File Inventory**: Complete list of uploaded files with checksums
- **Metadata**: Preserved multilingual titles and descriptions
- **API Responses**: Success confirmation with HTTP status codes

## Best Practices Demonstrated

### ✅ Successful Patterns
1. **Organized File Structure**: Clear folder hierarchy by content type
2. **Comprehensive Metadata**: Complete Dublin Core fields with multilingual support
3. **Proper Resource Types**: COAR vocabulary for academic compatibility
4. **Consistent Licensing**: Open Access CC-BY-4.0 throughout
5. **Validation**: Immediate feedback on upload success/failure

### 🔧 Configuration Tips
- Use relative paths in CSV for portability
- Include both French and English metadata for international accessibility
- Specify appropriate COAR resource types for academic discoverability
- Maintain consistent licensing and access rights policies

## Troubleshooting Notes

### Common Issues Resolved
1. **Base Path Configuration**: Must specify `--base-path .` when using relative paths
2. **Folder Config Required**: `--folder-config` parameter is mandatory for folder mode
3. **CSV Format**: File paths in CSV must match actual directory structure

## Next Steps
The generated `upload_output.csv` file will be used in the next phase for [collection creation](../03_collection_creation/collection_workflow.md).