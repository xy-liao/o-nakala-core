# Django NAKALA Web Application Development Prompt

## Project Overview

Build a comprehensive Django web application that provides a user-friendly interface for the NAKALA research data repository API. This application should simplify data management, collection creation, and metadata curation for researchers and institutions working with digital humanities, historical research, and cultural heritage digitization.

## Available Resources

You have access to:
- Complete OpenAPI specification: `nakala-apitest.json` (Swagger 2.0 format)
- NAKALA API metadata vocabulary: `nakala_metadata_vocabulary.json`
- Official documentation guide: `guide_description.md`
- API keys configuration: `api_keys.md`

## Target Application Features

### 1. Core API Integration
- **Authentication Management**: Secure API key storage and rotation
- **Multi-environment Support**: Test (apitest.nakala.fr) and Production (api.nakala.fr) environments
- **API Client**: Auto-generated or hand-crafted client based on OpenAPI spec
- **Rate Limiting**: Built-in request throttling and retry logic
- **Error Handling**: Comprehensive error management with user-friendly messages

### 2. Data Management Interface
- **Upload Workflow**: Drag-and-drop file upload with progress tracking
- **Metadata Editor**: Rich form interface for Dublin Core qualified metadata
- **Bulk Operations**: CSV-based batch upload and modification
- **File Preview**: Support for images, documents, and other research data
- **Validation Engine**: Pre-upload validation with detailed feedback
- **Version Control**: Track data item versions and changes

### 3. Collection Management
- **Visual Collection Builder**: Drag-and-drop interface for organizing datasets
- **Folder-based Collections**: Import collections from directory structures
- **Metadata Inheritance**: Automatic metadata propagation from collections to items
- **Relationship Mapping**: Visual interface for DataCite RelationType relationships
- **Status Management**: Private/public collection lifecycle management

### 4. Metadata Curation Tools
- **Quality Assessment Dashboard**: Automated metadata quality scoring
- **Duplicate Detection**: Content-based similarity analysis with visual comparison
- **Batch Editor**: Spreadsheet-like interface for bulk metadata modifications
- **Controlled Vocabularies**: Integration with RAMEAU, Pactols, GEMET, LCSH, etc.
- **FAIR Compliance**: Built-in FAIR principles validation and recommendations

### 5. Search and Discovery
- **Advanced Search**: Multi-faceted search across authors, subjects, dates, types
- **Visual Filters**: Interactive filter interface with autocomplete
- **Citation Generator**: Automatic citation formatting in multiple styles
- **Export Tools**: Multiple format export (CSV, JSON, XML, BibTeX)
- **OAI-PMH Integration**: Harvest and display external repository data

### 6. User Experience Features
- **Dashboard**: Personalized overview of user's data and collections
- **Progress Tracking**: Real-time status updates for long-running operations
- **Notification System**: Email and in-app notifications for important events
- **Responsive Design**: Mobile-friendly interface for field researchers
- **Accessibility**: WCAG 2.1 AA compliance for inclusive access
- **Internationalization**: French/English bilingual interface

## Technical Architecture Requirements

### Backend (Django)
- **Django 4.2+ LTS**: Long-term support version for stability
- **Django REST Framework**: API endpoints for frontend interaction
- **Celery**: Asynchronous task processing for uploads and curation
- **Redis**: Task queue and caching layer
- **PostgreSQL**: Primary database with full-text search capabilities
- **File Storage**: Configurable local/S3/MinIO storage backends
- **Security**: CSRF protection, rate limiting, input validation

### Frontend
- **Django Templates**: Server-side rendering with progressive enhancement
- **Alpine.js/HTMX**: Lightweight JavaScript for interactivity
- **Bootstrap 5**: Responsive CSS framework
- **File Upload**: Chunked upload with progress bars
- **Data Visualization**: Chart.js for analytics and quality metrics
- **Rich Text Editor**: TinyMCE for metadata descriptions

### API Integration Architecture
```python
# Suggested structure
nakala_web/
├── settings/
│   ├── base.py           # Common settings
│   ├── development.py    # Dev-specific settings
│   └── production.py     # Production settings
├── apps/
│   ├── core/            # Base models and utilities
│   ├── api_client/      # NAKALA API integration
│   ├── data_management/ # Upload and data workflows
│   ├── collections/     # Collection management
│   ├── curation/        # Quality and duplicate tools
│   ├── search/          # Search and discovery
│   └── users/           # User management and profiles
├── templates/           # Django templates
├── static/              # CSS, JS, images
├── media/               # User uploaded files
└── locale/              # Internationalization files
```

### Database Schema Considerations
- **API Key Management**: Encrypted storage with environment-specific keys
- **Metadata Caching**: Local cache of NAKALA metadata for performance
- **User Preferences**: Customizable default metadata, languages, licenses
- **Audit Trail**: Complete history of user actions and API calls
- **Batch Operations**: Track long-running operations with status updates

## Development Priorities

### Phase 1: Foundation (MVP)
1. Django project setup with proper configuration
2. NAKALA API client integration
3. Basic authentication and user management
4. Simple upload interface
5. Essential metadata forms
6. Basic collection creation

### Phase 2: Core Features
1. Advanced metadata editor with Dublin Core qualified fields
2. Bulk upload with CSV configuration
3. Collection management interface
4. File preview and validation
5. Basic search functionality
6. User dashboard

### Phase 3: Advanced Features
1. Metadata curation tools
2. Quality assessment dashboard
3. Duplicate detection
4. Batch modification interface
5. Advanced search and filters
6. Citation and export tools

### Phase 4: Polish and Production
1. Performance optimization
2. Security hardening
3. Accessibility compliance
4. Comprehensive testing
5. Documentation
6. Deployment configuration

## Key Integration Points

### NAKALA API Endpoints (Priority Order)
1. **Authentication**: User info and API key validation
2. **Data Upload**: File upload and metadata creation
3. **Collections**: Collection CRUD operations
4. **Search**: Author and data search endpoints
5. **Vocabularies**: Controlled vocabulary endpoints
6. **Metadata**: Retrieval and modification
7. **Relations**: Data relationship management

### Metadata Standards Integration
- **Dublin Core Qualified**: Complete DC terms implementation
- **DataCite**: RelationType for inter-data relationships
- **Controlled Vocabularies**: RAMEAU, Pactols, GEMET, LCSH integration
- **FAIR Principles**: Built-in compliance checking
- **Language Support**: RFC5646 language codes
- **Geographic Data**: TGN, ISO3166, coordinate systems

### File Management Strategy
- **Chunked Upload**: Handle large research datasets
- **MIME Detection**: Automatic file type recognition
- **Thumbnail Generation**: Preview for images and documents
- **Virus Scanning**: Security check for uploaded files
- **Backup Strategy**: Redundant storage for critical data
- **Cleanup Jobs**: Automatic removal of orphaned files

## User Interface Guidelines

### Design Principles
- **Research-Focused**: Optimize for academic workflows
- **Data-Dense**: Efficiently display complex metadata
- **Progressive Disclosure**: Show basic options first, advanced on demand
- **Consistency**: Align with NAKALA's visual language where possible
- **Performance**: Fast loading even with large datasets

### Accessibility Requirements
- **Keyboard Navigation**: Full functionality without mouse
- **Screen Reader Support**: Proper ARIA labels and structure
- **Color Contrast**: WCAG AA compliant color schemes
- **Text Scaling**: Support up to 200% zoom
- **Alternative Text**: Descriptive alt text for all images

### Responsive Considerations
- **Mobile-First**: Primary interface works on tablets/phones
- **Touch-Friendly**: Appropriate touch targets and gestures
- **Offline Capability**: Basic functionality when connectivity is poor
- **Progressive Web App**: Consider PWA features for field work

## Quality Assurance Strategy

### Testing Framework
- **Unit Tests**: pytest for backend logic
- **Integration Tests**: Test API client thoroughly
- **End-to-End Tests**: Selenium for critical user journeys
- **Performance Tests**: Load testing for bulk operations
- **Security Tests**: Penetration testing for production readiness

### Documentation Requirements
- **API Documentation**: Complete endpoint documentation
- **User Guide**: Step-by-step workflows for researchers
- **Developer Documentation**: Setup and contribution guidelines
- **Deployment Guide**: Production deployment instructions
- **Troubleshooting**: Common issues and solutions

## Deployment and DevOps

### Development Environment
- **Docker Compose**: Containerized development stack
- **Environment Variables**: .env configuration management
- **Database Migrations**: Proper migration strategy
- **Static Assets**: Efficient asset compilation and serving
- **Background Tasks**: Celery worker configuration

### Production Considerations
- **Load Balancing**: Handle multiple concurrent users
- **Database Optimization**: Query optimization and indexing
- **Caching Strategy**: Redis for session and data caching
- **Monitoring**: Application performance monitoring
- **Backup Strategy**: Automated database and file backups
- **Security**: SSL, security headers, input validation

## Success Metrics

### User Experience Metrics
- **Task Completion Rate**: Successful upload/collection creation rate
- **Time to First Upload**: How quickly new users can upload data
- **Error Recovery**: How well users recover from validation errors
- **User Retention**: Return usage patterns
- **Feature Adoption**: Which advanced features are actually used

### Technical Performance Metrics
- **API Response Times**: Monitor NAKALA API performance
- **Upload Success Rate**: Track failed uploads and causes
- **Database Performance**: Query optimization opportunities
- **Error Rates**: Application and API error tracking
- **Security Incidents**: Track and respond to security issues

## Getting Started

1. **Environment Setup**: Create Django project with recommended structure
2. **API Integration**: Implement NAKALA API client based on OpenAPI spec
3. **Authentication**: Set up user authentication and API key management
4. **Basic Models**: Create core models for data, collections, and metadata
5. **MVP Interface**: Build minimal viable upload and collection interface
6. **Iterative Development**: Add features incrementally based on user feedback

Remember to prioritize user research and feedback throughout development. The goal is to make NAKALA's powerful API accessible to researchers who may not be comfortable with command-line tools or API integration.