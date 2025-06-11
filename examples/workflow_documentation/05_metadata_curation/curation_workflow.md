# Metadata Curation Workflow

## Overview
This phase demonstrates systematic metadata enhancement using batch modification techniques to address quality issues and improve discoverability of datasets and collections.

> **📚 Documentation Reference**: For complete Curator endpoint documentation, CSV format specifications, and field transformations, see [Curator Endpoint Documentation](../../../docs/endpoints/curator-endpoint/README.md).

## Validation Status
**CSV File**: `data_modifications.csv` ✅ **VALIDATED**  
**Validation Tool**: `tools/curator_validator.py`  
**Result**: 100% valid, generates 4 metadata entries per row (4 total modifications)

## Curation Strategy

### Two-Phase Approach
1. **Data Item Enhancement** - Enrich dataset metadata with keywords and relations
2. **Collection Enhancement** - Improve collection descriptions and discoverability

### Target Improvements
- Enhanced multilingual keywords for better search visibility
- Detailed relationship documentation between datasets and research context
- Expanded descriptions with comprehensive academic context
- Improved collection-level metadata organization

## Phase 1: Data Item Curation

### Modification Configuration Analysis

#### data_modifications.csv Structure
```csv
id,action,new_keywords,new_relation
10.34847/nkl.bf0fxt5e,modify,"fr:images;photographie;recherche;visualisation|en:images;photography;research;visualization","fr:Relatif au projet de recherche principal|en:Related to main research project"
10.34847/nkl.181eqe75,modify,"fr:code;programmation;analyse;traitement|en:code;programming;analysis;processing","fr:Scripts d'analyse des données de l'étude|en:Data analysis scripts for the study"
10.34847/nkl.9edeiw5z,modify,"fr:présentations;communication;conférence;diffusion|en:presentations;communication;conference;dissemination","fr:Matériel de présentation du projet|en:Project presentation materials"
10.34847/nkl.2b617444,modify,"fr:documentation;papiers;méthodologie;protocole|en:documentation;papers;methodology;protocol","fr:Documentation méthodologique complète|en:Complete methodological documentation"
10.34847/nkl.5f40fo9t,modify,"fr:données;résultats;enquête;analyse|en:data;results;survey;analysis","fr:Données primaires de l'enquête 2023|en:Primary survey data from 2023"
```

### Enhancement Strategy
- **Keyword Expansion**: Domain-specific terms in both French and English
- **Relationship Context**: Clear connections to research project context
- **Academic Terminology**: Proper scholarly vocabulary for discoverability
- **Temporal Context**: Specific references to study timeframes and scope

### Data Item Modification Commands

#### Dry Run Validation
```bash
o-nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify data_modifications.csv \
  --scope datasets \
  --dry-run
```

**Dry Run Results:**
```
Batch modification simulation:
  Total processed: 5
  Successful: 5
  Failed: 0
  Skipped: 0
  Success rate: 100.0%
```

#### Production Application
```bash
o-nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify data_modifications.csv \
  --scope datasets
```

**Application Results:**
```
Batch modification completed:
  Total processed: 5
  Successful: 5
  Failed: 0
  Skipped: 0
  Success rate: 100.0%

Successfully applied changes to:
- 10.34847/nkl.bf0fxt5e (Images)
- 10.34847/nkl.181eqe75 (Code)
- 10.34847/nkl.9edeiw5z (Presentations)
- 10.34847/nkl.2b617444 (Documents)
- 10.34847/nkl.5f40fo9t (Data)
```

## Phase 2: Collection Curation

### Collection Enhancement Configuration

#### collection_modifications.csv Structure
```csv
id,action,new_description,new_keywords
10.34847/nkl.adfc67q4,modify,"fr:Collection regroupant les scripts de code et les données associées pour l'analyse de recherche. Cette collection contient les outils développés et les jeux de données utilisés dans le cadre du projet.|en:Collection containing code scripts and associated data for research analysis. This collection includes the tools developed and datasets used in the project framework.","fr:code;données;analyse;recherche;scripts;traitement|en:code;data;analysis;research;scripts;processing"
10.34847/nkl.d8328982,modify,"fr:Collection complète de documents de recherche incluant les protocoles d'étude, les analyses méthodologiques, les revues de littérature et les discussions de résultats.|en:Complete collection of research documents including study protocols, methodological analyses, literature reviews, and results discussions.","fr:documents;recherche;méthodologie;protocole;littérature;résultats|en:documents;research;methodology;protocol;literature;results"
10.34847/nkl.1c39i9oq,modify,"fr:Collection multimédia rassemblant les images de terrain, les graphiques de données et les matériaux de présentation du projet de recherche.|en:Multimedia collection bringing together field images, data graphics, and research project presentation materials.","fr:multimédia;images;graphiques;présentations;visuel;communication|en:multimedia;images;graphics;presentations;visual;communication"
```

### Collection Modification Commands

#### Dry Run Validation
```bash
o-nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify collection_modifications.csv \
  --scope collections \
  --dry-run
```

**Dry Run Results:**
```
Batch modification simulation:
  Total processed: 3
  Successful: 3
  Failed: 0
  Skipped: 0
  Success rate: 100.0%
```

#### Production Application
```bash
o-nakala-curator \
  --api-key "33170cfe-f53c-550b-5fb6-4814ce981293" \
  --batch-modify collection_modifications.csv \
  --scope collections
```

**Application Results:**
```
Batch modification completed:
  Total processed: 3
  Successful: 3
  Failed: 0
  Skipped: 0
  Success rate: 100.0%

Successfully applied changes to:
- 10.34847/nkl.adfc67q4 (Code and Data Collection)
- 10.34847/nkl.d8328982 (Documents Collection)
- 10.34847/nkl.1c39i9oq (Multimedia Collection)
```

## Curation Impact Analysis

### Metadata Enhancement Summary

#### Data Items Enhanced
| Dataset | Content Type | Keywords Added | Relation Context |
|---------|-------------|----------------|------------------|
| nkl.bf0fxt5e | Images | 8 multilingual terms | Research project connection |
| nkl.181eqe75 | Code | 8 multilingual terms | Data analysis context |
| nkl.9edeiw5z | Presentations | 8 multilingual terms | Project presentation materials |
| nkl.2b617444 | Documents | 8 multilingual terms | Methodological documentation |
| nkl.5f40fo9t | Data | 8 multilingual terms | Primary survey data context |

#### Collections Enhanced
| Collection | Enhancement Type | Description Length | Keywords Added |
|-----------|------------------|-------------------|----------------|
| Code and Data | Detailed description | 150+ characters | 12 multilingual terms |
| Documents | Comprehensive overview | 140+ characters | 12 multilingual terms |
| Multimedia | Context-rich description | 130+ characters | 12 multilingual terms |

### Quality Improvements Achieved

#### ✅ Discoverability Enhancements
1. **Keyword Coverage**: 40+ new multilingual search terms added
2. **Context Documentation**: Clear project relationships established
3. **Academic Terminology**: Proper scholarly vocabulary integrated
4. **Bilingual Access**: Complete French/English metadata coverage

#### ✅ Research Context
1. **Project Integration**: Clear connections to research workflow
2. **Temporal Context**: Specific study timeframes documented
3. **Methodological Links**: Research protocol connections established
4. **Data Lineage**: Origin and purpose clearly documented

## Technical Implementation Notes

### CSV Format Requirements
- **Column Names**: Must use 'new_' prefix for modification fields
- **Action Values**: Must specify 'modify' (not 'update')
- **Multilingual Format**: `fr:text|en:text` pattern required
- **Field Validation**: Only supported fields accepted by curator

### Supported Modification Fields
**Data Items:**
- `new_keywords`, `new_relation`, `new_description`, `new_title`
- `new_author`, `new_contributor`, `new_license`, `new_type`
- `new_date`, `new_language`, `new_temporal`, `new_spatial`

**Collections:**
- `new_description`, `new_keywords`, `new_title`
- **Note**: `new_creator` field not supported via batch modifications

### Best Practices Demonstrated

#### ✅ Effective Patterns
1. **Dry Run Testing**: Always validate modifications before application
2. **Incremental Enhancement**: Focus on specific field improvements
3. **Multilingual Consistency**: Maintain language balance throughout
4. **Academic Standards**: Use appropriate scholarly terminology
5. **Relationship Documentation**: Clear context and purpose statements

#### 🔧 Technical Considerations
- **Field Limitations**: Some collection fields require different modification approaches
- **Validation Requirements**: All modifications must pass NAKALA validation
- **Batch Size**: Large modifications may require chunking
- **Error Handling**: Failed modifications are clearly reported and tracked

## Attempted Advanced Modifications

### Creator Field Challenge
```csv
id,action,new_creator
10.34847/nkl.adfc67q4,modify,"Doe,John;Smith,Jane"
```

**Result**: Field not supported for batch collection modifications
**Alternative**: Creator fields may require different API endpoints or manual updates

## Quality Validation

### Post-Curation Assessment
After applying all modifications, the enhanced metadata provides:
- **Improved Search Coverage**: Expanded keyword vocabulary
- **Better Academic Context**: Clear research project relationships
- **Enhanced Discoverability**: Multilingual access points
- **Professional Presentation**: Comprehensive descriptions

### Success Metrics
- **100% Application Success**: All planned modifications applied successfully
- **Zero Data Loss**: Original metadata preserved while adding enhancements
- **Comprehensive Coverage**: All target datasets and collections improved
- **Multilingual Integrity**: Language balance maintained throughout

## Next Steps
The curation process concludes with [final validation](../06_validation_and_results/final_validation.md) to confirm improvements and document the complete workflow outcomes.