# Complete Metadata Management System Design

## 🎯 **Vision: Truly Complete Metadata Management**

Transform the complex NAKALA API into an intuitive, guided experience where users can create complete, valid metadata without deep API knowledge or manual field lookup.

---

## 🏗️ **System Architecture Overview**

### **Core Components**

1. **🔍 Dynamic Field Discovery Engine**
2. **📝 Intelligent Template Generator**  
3. **🤖 Pre-population Assistant**
4. **🎮 Interactive Metadata Builder**
5. **🔧 Technical Integration Helper**
6. **✅ Real-time Validation Engine**

---

## 🔍 **Component 1: Dynamic Field Discovery Engine**

### **Purpose**
Automatically discover and maintain current NAKALA API capabilities, vocabularies, and validation rules.

### **Implementation**

#### **Vocabulary Discovery Service**
```python
class NakalaVocabularyService:
    def __init__(self, api_client):
        self.api = api_client
        self.cache = {}
        
    async def discover_vocabularies(self):
        """Fetch all available vocabularies and cache them."""
        vocabularies = {
            'properties': await self.api.get('/vocabularies/properties'),
            'languages': await self.api.get('/vocabularies/languages'),
            'licenses': await self.api.get('/vocabularies/licenses'),
            'datatypes': await self.api.get('/vocabularies/datatypes'),
            'countries': await self.api.get('/vocabularies/countryCodes'),
            'statuses': await self.api.get('/vocabularies/dataStatuses'),
            'collection_statuses': await self.api.get('/vocabularies/collectionStatuses')
        }
        self.cache = vocabularies
        return vocabularies
    
    def get_field_schema(self, property_uri):
        """Get validation schema for a specific field."""
        # Implementation based on property URI
        pass
```

#### **Schema Generator**
```python
class MetadataSchemaGenerator:
    def generate_field_schema(self, property_uri):
        """Generate JSON Schema for a specific metadata field."""
        return {
            "type": "object",
            "properties": {
                "propertyUri": {"const": property_uri},
                "value": self._get_value_schema(property_uri),
                "lang": self._get_language_schema(),
                "typeUri": self._get_type_schema(property_uri)
            },
            "required": ["propertyUri", "value"]
        }
```

---

## 📝 **Component 2: Intelligent Template Generator**

### **Purpose**
Create context-aware metadata templates with validation, examples, and smart defaults.

### **Template Types**

#### **Basic Template Structure**
```python
class MetadataTemplate:
    def __init__(self, resource_type, context=None):
        self.resource_type = resource_type
        self.context = context or {}
        self.fields = {}
        self.validation_rules = {}
        self.examples = {}
        
    def add_field(self, field_name, config):
        """Add field with validation and examples."""
        self.fields[field_name] = {
            'property_uri': config['property_uri'],
            'required': config.get('required', False),
            'multilingual': config.get('multilingual', False),
            'data_type': config.get('data_type', 'string'),
            'controlled_vocabulary': config.get('vocabulary'),
            'validation_pattern': config.get('pattern'),
            'examples': config.get('examples', []),
            'help_text': config.get('help_text', '')
        }
```

#### **Dynamic Template Generation**
```python
class DynamicTemplateGenerator:
    def __init__(self, vocabulary_service, schema_generator):
        self.vocab = vocabulary_service
        self.schema = schema_generator
        
    async def generate_template(self, resource_type, user_context=None):
        """Generate template based on resource type and user context."""
        
        # Get required fields for resource type
        required_fields = await self._get_required_fields(resource_type)
        
        # Get recommended fields based on context
        recommended_fields = await self._get_recommended_fields(resource_type, user_context)
        
        # Get vocabularies for validation
        vocabularies = await self.vocab.discover_vocabularies()
        
        template = MetadataTemplate(resource_type, user_context)
        
        for field_uri in required_fields + recommended_fields:
            field_config = await self._build_field_config(field_uri, vocabularies)
            template.add_field(field_uri, field_config)
            
        return template
```

---

## 🤖 **Component 3: Pre-population Assistant**

### **Purpose**
Intelligently pre-populate metadata templates with existing data, user information, and contextual suggestions.

### **Data Sources**

#### **User Context Service**
```python
class UserContextService:
    async def get_user_profile(self, api_key):
        """Get user information for auto-population."""
        return {
            'name': await self._get_user_name(),
            'affiliation': await self._get_user_affiliation(),
            'orcid': await self._get_user_orcid(),
            'default_language': await self._get_user_language(),
            'recent_projects': await self._get_recent_collections(),
            'common_keywords': await self._analyze_user_keywords(),
            'preferred_licenses': await self._analyze_user_licenses()
        }
```

#### **Relationship Discovery Service**
```python
class RelationshipDiscoveryService:
    async def suggest_relations(self, current_metadata, user_context):
        """Suggest related resources based on content similarity."""
        
        # Search for similar resources
        similar_resources = await self.api.search({
            'query': current_metadata.get('title', ''),
            'filters': {
                'user': user_context['user_id'],
                'type': 'similar'
            }
        })
        
        # Generate relationship suggestions
        suggestions = []
        for resource in similar_resources:
            suggestions.append({
                'identifier': resource['identifier'],
                'title': resource['title'],
                'suggested_relation': self._analyze_relationship_type(current_metadata, resource),
                'confidence': self._calculate_confidence(current_metadata, resource)
            })
            
        return suggestions
```

#### **File Metadata Integration**
```python
class FileMetadataService:
    async def extract_file_metadata(self, uploaded_files):
        """Extract technical metadata from uploaded files."""
        metadata = []
        
        for file_upload in uploaded_files:
            file_info = {
                'name': file_upload['name'],
                'sha1': file_upload['sha1'],
                'size': file_upload['size'],
                'mime_type': file_upload['mimeType'],
                'technical_metadata': await self._extract_technical_metadata(file_upload),
                'suggested_description': await self._generate_file_description(file_upload)
            }
            
            # IIIF metadata for images
            if file_upload['mimeType'].startswith('image/'):
                file_info['iiif_metadata'] = await self._get_iiif_metadata(file_upload['sha1'])
                
            metadata.append(file_info)
            
        return metadata
```

---

## 🎮 **Component 4: Interactive Metadata Builder**

### **Purpose**
Provide step-by-step guided metadata creation with real-time validation and smart suggestions.

### **User Interface Components**

#### **Wizard-Style Form Builder**
```python
class MetadataWizard:
    def __init__(self, template, pre_population_service):
        self.template = template
        self.pre_pop = pre_population_service
        self.current_step = 0
        self.metadata = {}
        self.validation_errors = {}
        
    async def start_wizard(self, user_context):
        """Initialize wizard with pre-populated data."""
        self.metadata = await self.pre_pop.pre_populate_template(
            self.template, user_context
        )
        return self._get_current_step()
        
    def _get_current_step(self):
        """Get current step configuration."""
        steps = [
            {'name': 'basic_info', 'fields': ['title', 'description', 'type']},
            {'name': 'creators', 'fields': ['creator', 'contributor']},
            {'name': 'content', 'fields': ['keywords', 'language', 'license']},
            {'name': 'coverage', 'fields': ['temporal', 'spatial']},
            {'name': 'relations', 'fields': ['isPartOf', 'relation', 'source']},
            {'name': 'technical', 'fields': ['format', 'identifier']},
            {'name': 'rights', 'fields': ['rights', 'accessRights', 'embargo']}
        ]
        return steps[self.current_step]
```

#### **Real-time Validation Engine**
```python
class RealTimeValidator:
    def __init__(self, schema_generator, vocabulary_service):
        self.schema = schema_generator
        self.vocab = vocabulary_service
        
    async def validate_field(self, field_name, value, context=None):
        """Validate single field in real-time."""
        field_schema = await self.schema.get_field_schema(field_name)
        
        # Basic format validation
        validation_result = self._validate_format(value, field_schema)
        
        # Vocabulary validation
        if field_schema.get('controlled_vocabulary'):
            vocab_validation = await self._validate_vocabulary(value, field_schema['vocabulary'])
            validation_result.update(vocab_validation)
            
        # Contextual validation
        if context:
            context_validation = await self._validate_context(field_name, value, context)
            validation_result.update(context_validation)
            
        return validation_result
        
    async def suggest_corrections(self, field_name, invalid_value):
        """Suggest corrections for invalid values."""
        suggestions = []
        
        # Fuzzy matching against vocabularies
        if self._has_vocabulary(field_name):
            vocab_suggestions = await self._fuzzy_match_vocabulary(field_name, invalid_value)
            suggestions.extend(vocab_suggestions)
            
        # Format corrections
        format_suggestions = self._suggest_format_corrections(field_name, invalid_value)
        suggestions.extend(format_suggestions)
        
        return suggestions
```

---

## 🔧 **Component 5: Technical Integration Helper**

### **Purpose**
Handle complex technical operations like file upload orchestration, IIIF integration, and SHA1 calculation.

### **Integration Services**

#### **File Upload Orchestrator**
```python
class FileUploadOrchestrator:
    async def upload_with_metadata(self, files, metadata_template):
        """Coordinate file upload with metadata creation."""
        
        # Step 1: Upload files and get SHA1 identifiers
        upload_results = []
        for file in files:
            result = await self.api.post('/datas/uploads', files={'file': file})
            upload_results.append(result)
            
        # Step 2: Extract technical metadata
        file_metadata = await self.file_service.extract_file_metadata(upload_results)
        
        # Step 3: Update metadata template with file information
        metadata_template.add_files(file_metadata)
        
        # Step 4: Create data record with files and metadata
        final_metadata = await self._prepare_final_metadata(metadata_template)
        data_record = await self.api.post('/datas', json=final_metadata)
        
        return {
            'data_record': data_record,
            'files': upload_results,
            'metadata': final_metadata
        }
```

#### **IIIF Integration Service**
```python
class IIIFIntegrationService:
    async def enhance_image_metadata(self, data_identifier, file_identifier):
        """Add IIIF metadata to image resources."""
        
        # Get IIIF info
        iiif_info = await self.api.get(f'/iiif/{data_identifier}/{file_identifier}/info.json')
        
        # Generate technical metadata
        technical_metadata = {
            'width': iiif_info['width'],
            'height': iiif_info['height'],
            'profile': iiif_info['profile'],
            'formats': iiif_info.get('preferredFormats', []),
            'iiif_service': f"{self.api.base_url}/iiif/{data_identifier}/{file_identifier}"
        }
        
        return technical_metadata
```

---

## ✅ **Component 6: Real-time Validation Engine**

### **Purpose**
Provide comprehensive validation with intelligent error messages and correction suggestions.

### **Validation Layers**

#### **Multi-layer Validation**
```python
class ComprehensiveValidator:
    def __init__(self):
        self.validators = [
            FormatValidator(),
            VocabularyValidator(), 
            RelationshipValidator(),
            BusinessRuleValidator(),
            QualityValidator()
        ]
        
    async def validate_complete_metadata(self, metadata):
        """Run all validation layers."""
        results = {
            'errors': [],
            'warnings': [],
            'suggestions': [],
            'quality_score': 0
        }
        
        for validator in self.validators:
            layer_result = await validator.validate(metadata)
            results['errors'].extend(layer_result.get('errors', []))
            results['warnings'].extend(layer_result.get('warnings', []))
            results['suggestions'].extend(layer_result.get('suggestions', []))
            
        results['quality_score'] = self._calculate_quality_score(metadata, results)
        return results
```

---

## 🎯 **Implementation Strategy**

### **Phase 1: Foundation (Months 1-2)**
- Build Dynamic Field Discovery Engine
- Implement basic Template Generator
- Create vocabulary caching system
- Establish API abstraction layer

### **Phase 2: Intelligence (Months 3-4)**  
- Develop Pre-population Assistant
- Build User Context Service
- Implement relationship discovery
- Add file metadata extraction

### **Phase 3: User Experience (Months 5-6)**
- Create Interactive Metadata Builder
- Build wizard-style interface
- Implement real-time validation
- Add smart suggestions engine

### **Phase 4: Integration (Months 7-8)**
- Build Technical Integration Helper
- Implement file upload orchestration
- Add IIIF integration
- Create comprehensive validation

### **Phase 5: Enhancement (Months 9-10)**
- Add quality scoring system
- Implement advanced relationship mapping
- Build metadata analytics
- Create export/import tools

---

## 📊 **Success Metrics**

### **User Experience Metrics**
- **Metadata Completion Time**: Target 50% reduction
- **Validation Error Rate**: Target <5% on first submission
- **User Satisfaction**: Target >90% positive feedback
- **Template Reuse Rate**: Target >70% of users reuse templates

### **Technical Quality Metrics**
- **Metadata Completeness**: Target >95% required fields filled
- **Relationship Accuracy**: Target >90% suggested relationships accepted
- **File Integration Success**: Target >99% successful file-metadata linking
- **API Performance**: Target <2s response time for template generation

### **System Adoption Metrics**
- **Feature Usage**: Track usage of each component
- **Error Reduction**: Measure API error rate improvement
- **Workflow Efficiency**: Time from data upload to publication
- **Community Feedback**: User-reported improvements and requests

---

## 🛠️ **Technical Requirements**

### **Backend Requirements**
- **Python 3.9+** with async/await support
- **Caching layer** (Redis) for vocabulary data
- **Database** (PostgreSQL) for user contexts and templates
- **Message queue** (Celery) for background processing
- **API client** with rate limiting and retry logic

### **Frontend Requirements**
- **React/Vue.js** for interactive forms
- **Real-time validation** with WebSocket connections
- **File upload** with progress tracking
- **Responsive design** for mobile/tablet use
- **Accessibility** compliance (WCAG 2.1)

### **Integration Requirements**
- **NAKALA API** full integration
- **ORCID API** for author lookup
- **Vocabulary services** (LCSH, MeSH, etc.)
- **Geographic services** (GeoNames) for spatial data
- **Citation services** for reference formatting

---

## 🎉 **Expected Outcomes**

### **For Users**
- **Intuitive metadata creation** without API knowledge
- **Intelligent suggestions** based on context and history  
- **Real-time validation** preventing submission errors
- **Rich templates** with examples and guidance
- **Automated technical metadata** handling

### **For Institutions**
- **Improved metadata quality** across all submissions
- **Reduced support burden** through self-service capabilities
- **Better discoverability** of research outputs
- **Compliance assurance** with metadata standards
- **Workflow standardization** across departments

### **For the Platform**
- **Higher quality metadata** in the repository
- **Reduced API errors** through better validation
- **Improved user adoption** of advanced features
- **Better integration** between components
- **Enhanced research discoverability**

---

**This comprehensive system transforms NAKALA's powerful but complex API into an intuitive, guided experience that enables users to create complete, high-quality metadata without requiring deep technical knowledge.**