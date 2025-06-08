/**
 * O-Nakala Core Template Designer
 * Visual Drag-and-Drop Template Creation Interface
 */

class TemplateDesigner {
    constructor() {
        this.currentTemplate = {
            name: '',
            description: '',
            resource_type: 'dataset',
            fields: [],
            sections: []
        };
        this.selectedField = null;
        this.draggedElement = null;
        this.fieldCounter = 0;
        
        // Field definitions from NAKALA vocabulary
        this.fieldDefinitions = this.initializeFieldDefinitions();
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupDragAndDrop();
        this.setupSortable();
        this.updateStats();
    }
    
    initializeFieldDefinitions() {
        return {
            title: {
                name: 'Title',
                property_uri: 'http://nakala.fr/terms#title',
                data_type: 'string',
                required: true,
                multilingual: true,
                icon: 'fas fa-heading',
                help_text: 'The main title or name of the resource',
                examples: ['Research Dataset 2023', 'Historical Documents Collection']
            },
            creator: {
                name: 'Creator',
                property_uri: 'http://purl.org/dc/terms/creator',
                data_type: 'string',
                required: false,
                multilingual: false,
                icon: 'fas fa-user',
                help_text: 'The person or organization responsible for creating the resource',
                examples: ['John Doe', 'University of Paris', 'Research Team Alpha']
            },
            description: {
                name: 'Description',
                property_uri: 'http://purl.org/dc/terms/description',
                data_type: 'text',
                required: true,
                multilingual: true,
                icon: 'fas fa-align-left',
                help_text: 'A detailed description of the resource content and purpose',
                examples: ['This dataset contains...', 'Collection of historical documents from...']
            },
            subject: {
                name: 'Subject',
                property_uri: 'http://purl.org/dc/terms/subject',
                data_type: 'string',
                required: false,
                multilingual: true,
                icon: 'fas fa-tags',
                help_text: 'Keywords or topics that describe the resource content',
                examples: ['History', 'Digital Humanities', 'Medieval Studies']
            },
            license: {
                name: 'License',
                property_uri: 'http://purl.org/dc/terms/license',
                data_type: 'uri',
                required: true,
                multilingual: false,
                icon: 'fas fa-certificate',
                help_text: 'Legal license governing the use of this resource',
                examples: ['CC BY 4.0', 'CC BY-SA 4.0', 'Custom License']
            },
            rights: {
                name: 'Rights',
                property_uri: 'http://purl.org/dc/terms/rights',
                data_type: 'string',
                required: false,
                multilingual: true,
                icon: 'fas fa-key',
                help_text: 'Rights statement or copyright information',
                examples: ['© 2023 University', 'Public Domain', 'All rights reserved']
            },
            accessRights: {
                name: 'Access Rights',
                property_uri: 'http://purl.org/dc/terms/accessRights',
                data_type: 'string',
                required: false,
                multilingual: false,
                icon: 'fas fa-lock',
                help_text: 'Information about access restrictions or permissions',
                examples: ['Open Access', 'Restricted', 'Embargoed until 2025']
            },
            format: {
                name: 'Format',
                property_uri: 'http://purl.org/dc/terms/format',
                data_type: 'string',
                required: false,
                multilingual: false,
                icon: 'fas fa-file-alt',
                help_text: 'File format, physical medium, or dimensions of the resource',
                examples: ['CSV', 'PDF', 'JPEG', 'application/json']
            },
            extent: {
                name: 'Extent',
                property_uri: 'http://purl.org/dc/terms/extent',
                data_type: 'string',
                required: false,
                multilingual: false,
                icon: 'fas fa-ruler',
                help_text: 'Size or duration of the resource',
                examples: ['1.2 MB', '45 pages', '2 hours', '1000 records']
            },
            language: {
                name: 'Language',
                property_uri: 'http://purl.org/dc/terms/language',
                data_type: 'string',
                required: false,
                multilingual: false,
                icon: 'fas fa-language',
                help_text: 'Language(s) of the resource content',
                examples: ['French', 'English', 'fr', 'en', 'Multi-language']
            },
            date: {
                name: 'Date',
                property_uri: 'http://purl.org/dc/terms/date',
                data_type: 'date',
                required: false,
                multilingual: false,
                icon: 'fas fa-calendar',
                help_text: 'Date associated with the resource (creation, publication, etc.)',
                examples: ['2023-06-08', '2023', '1850-1900']
            },
            spatial: {
                name: 'Spatial Coverage',
                property_uri: 'http://purl.org/dc/terms/spatial',
                data_type: 'string',
                required: false,
                multilingual: false,
                icon: 'fas fa-globe',
                help_text: 'Geographic location or region covered by the resource',
                examples: ['Paris, France', 'Europe', 'Latitude: 48.8566, Longitude: 2.3522']
            },
            temporal: {
                name: 'Temporal Coverage',
                property_uri: 'http://purl.org/dc/terms/temporal',
                data_type: 'string',
                required: false,
                multilingual: false,
                icon: 'fas fa-clock',
                help_text: 'Time period covered by the resource content',
                examples: ['19th century', '1850-1900', 'Medieval period']
            }
        };
    }
    
    setupEventListeners() {
        // Template info changes
        document.getElementById('templateName').addEventListener('input', (e) => {
            this.currentTemplate.name = e.target.value;
            this.updateStats();
        });
        
        document.getElementById('templateType').addEventListener('change', (e) => {
            this.currentTemplate.resource_type = e.target.value;
        });
        
        // Navigation buttons
        document.getElementById('previewBtn').addEventListener('click', () => this.showPreview());
        document.getElementById('exportBtn').addEventListener('click', () => this.exportTemplate());
        document.getElementById('saveBtn').addEventListener('click', () => this.saveTemplate());
        
        // Canvas tools
        document.getElementById('clearAllBtn').addEventListener('click', () => this.clearAll());
        document.getElementById('addSectionBtn').addEventListener('click', () => this.addSection());
        
        // Field search
        document.getElementById('fieldSearch').addEventListener('input', (e) => {
            this.filterFields(e.target.value);
        });
        
        // Preview modal tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchPreviewTab(e.target.dataset.tab);
            });
        });
    }
    
    setupDragAndDrop() {
        const dropZone = document.getElementById('designCanvas');
        
        // Setup drag events for field items
        document.querySelectorAll('.field-item').forEach(item => {
            item.addEventListener('dragstart', (e) => {
                this.draggedElement = {
                    type: 'field',
                    fieldType: e.target.dataset.fieldType
                };
                e.target.classList.add('dragging');
            });
            
            item.addEventListener('dragend', (e) => {
                e.target.classList.remove('dragging');
                this.draggedElement = null;
            });
        });
        
        // Setup drop zone
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });
        
        dropZone.addEventListener('dragleave', (e) => {
            if (!dropZone.contains(e.relatedTarget)) {
                dropZone.classList.remove('drag-over');
            }
        });
        
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            
            if (this.draggedElement && this.draggedElement.type === 'field') {
                this.addFieldToCanvas(this.draggedElement.fieldType);
            }
        });
    }
    
    setupSortable() {
        // Will be implemented when fields are added to canvas
    }
    
    addFieldToCanvas(fieldType) {
        const fieldDef = this.fieldDefinitions[fieldType];
        if (!fieldDef) return;
        
        // Create field object
        const field = {
            id: `field_${++this.fieldCounter}`,
            type: fieldType,
            name: fieldDef.name,
            property_uri: fieldDef.property_uri,
            data_type: fieldDef.data_type,
            required: fieldDef.required,
            multilingual: fieldDef.multilingual,
            help_text: fieldDef.help_text,
            examples: fieldDef.examples,
            default_value: '',
            validation_rules: [],
            custom_properties: {}
        };
        
        // Add to template
        this.currentTemplate.fields.push(field);
        
        // Render the field
        this.renderTemplate();
        this.updateStats();
        
        // Select the newly added field
        setTimeout(() => {
            this.selectField(field.id);
        }, 100);
        
        this.showToast(`Added ${fieldDef.name} field`, 'success');
    }
    
    renderTemplate() {
        const canvas = document.getElementById('designCanvas');
        
        if (this.currentTemplate.fields.length === 0) {
            // Show placeholder
            canvas.innerHTML = `
                <div class="drop-placeholder">
                    <i class="fas fa-mouse-pointer"></i>
                    <h3>Start designing your template</h3>
                    <p>Drag fields from the library to build your metadata template</p>
                    <div class="placeholder-actions">
                        <button class="placeholder-btn" onclick="templateDesigner.addQuickTemplate('basic')">
                            <i class="fas fa-bolt"></i> Basic Template
                        </button>
                        <button class="placeholder-btn" onclick="templateDesigner.addQuickTemplate('research')">
                            <i class="fas fa-microscope"></i> Research Template
                        </button>
                        <button class="placeholder-btn" onclick="templateDesigner.addQuickTemplate('collection')">
                            <i class="fas fa-archive"></i> Collection Template
                        </button>
                    </div>
                </div>
            `;
            return;
        }
        
        // Render fields
        const fieldsHtml = this.currentTemplate.fields.map(field => {
            const fieldDef = this.fieldDefinitions[field.type];
            if (!fieldDef) return '';
            
            return `
                <div class="designed-field ${this.selectedField === field.id ? 'selected' : ''}" 
                     data-field-id="${field.id}" 
                     onclick="templateDesigner.selectField('${field.id}')">
                    <div class="field-drag-handle">
                        <i class="fas fa-grip-vertical"></i>
                    </div>
                    <div class="designed-field-icon">
                        <i class="${fieldDef.icon}"></i>
                    </div>
                    <div class="designed-field-content">
                        <div class="designed-field-name">${field.name}</div>
                        <div class="designed-field-uri">${field.property_uri}</div>
                    </div>
                    <div class="designed-field-badges">
                        <span class="field-badge ${field.required ? 'required' : 'optional'}">
                            ${field.required ? 'Required' : 'Optional'}
                        </span>
                        ${field.multilingual ? '<span class="field-badge multilingual">Multilingual</span>' : ''}
                    </div>
                    <div class="designed-field-actions">
                        <button class="field-action-btn" onclick="templateDesigner.duplicateField('${field.id}')" title="Duplicate">
                            <i class="fas fa-copy"></i>
                        </button>
                        <button class="field-action-btn danger" onclick="templateDesigner.removeField('${field.id}')" title="Remove">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
        }).join('');
        
        canvas.innerHTML = `
            <div class="template-fields" id="templateFields">
                ${fieldsHtml}
            </div>
        `;
        
        // Setup sortable for reordering
        this.setupFieldSorting();
    }
    
    setupFieldSorting() {
        const container = document.getElementById('templateFields');
        if (!container) return;
        
        new Sortable(container, {
            animation: 150,
            ghostClass: 'dragging',
            onEnd: (evt) => {
                // Update field order in template
                const oldIndex = evt.oldIndex;
                const newIndex = evt.newIndex;
                
                if (oldIndex !== newIndex) {
                    const field = this.currentTemplate.fields.splice(oldIndex, 1)[0];
                    this.currentTemplate.fields.splice(newIndex, 0, field);
                    this.showToast('Field order updated', 'success');
                }
            }
        });
    }
    
    selectField(fieldId) {
        this.selectedField = fieldId;
        this.renderTemplate();
        this.renderProperties();
    }
    
    renderProperties() {
        const propertiesContent = document.getElementById('propertiesContent');
        
        if (!this.selectedField) {
            propertiesContent.innerHTML = `
                <div class="no-selection">
                    <i class="fas fa-hand-pointer"></i>
                    <p>Select a field to edit its properties</p>
                </div>
            `;
            return;
        }
        
        const field = this.currentTemplate.fields.find(f => f.id === this.selectedField);
        if (!field) return;
        
        const fieldDef = this.fieldDefinitions[field.type];
        
        propertiesContent.innerHTML = `
            <div class="property-form">
                <div class="property-group">
                    <label class="property-label">Field Name</label>
                    <input type="text" class="property-input" id="prop_name" value="${field.name}">
                </div>
                
                <div class="property-group">
                    <label class="property-label">Property URI</label>
                    <input type="text" class="property-input" id="prop_uri" value="${field.property_uri}">
                </div>
                
                <div class="property-group">
                    <label class="property-label">Data Type</label>
                    <select class="property-select" id="prop_datatype">
                        <option value="string" ${field.data_type === 'string' ? 'selected' : ''}>String</option>
                        <option value="text" ${field.data_type === 'text' ? 'selected' : ''}>Text</option>
                        <option value="uri" ${field.data_type === 'uri' ? 'selected' : ''}>URI</option>
                        <option value="date" ${field.data_type === 'date' ? 'selected' : ''}>Date</option>
                        <option value="number" ${field.data_type === 'number' ? 'selected' : ''}>Number</option>
                    </select>
                </div>
                
                <div class="property-group">
                    <label class="property-checkbox">
                        <input type="checkbox" id="prop_required" ${field.required ? 'checked' : ''}>
                        Required field
                    </label>
                </div>
                
                <div class="property-group">
                    <label class="property-checkbox">
                        <input type="checkbox" id="prop_multilingual" ${field.multilingual ? 'checked' : ''}>
                        Multilingual support
                    </label>
                </div>
                
                <div class="property-group">
                    <label class="property-label">Help Text</label>
                    <textarea class="property-input property-textarea" id="prop_help" placeholder="Enter helpful guidance for users...">${field.help_text || ''}</textarea>
                </div>
                
                <div class="property-group">
                    <label class="property-label">Default Value</label>
                    <input type="text" class="property-input" id="prop_default" value="${field.default_value || ''}" placeholder="Optional default value">
                </div>
                
                <div class="property-group">
                    <label class="property-label">Examples (one per line)</label>
                    <textarea class="property-input property-textarea" id="prop_examples" placeholder="Enter example values...">${(field.examples || []).join('\\n')}</textarea>
                </div>
            </div>
        `;
        
        // Setup property change listeners
        this.setupPropertyListeners(field);
    }
    
    setupPropertyListeners(field) {
        const updateField = () => {
            field.name = document.getElementById('prop_name').value;
            field.property_uri = document.getElementById('prop_uri').value;
            field.data_type = document.getElementById('prop_datatype').value;
            field.required = document.getElementById('prop_required').checked;
            field.multilingual = document.getElementById('prop_multilingual').checked;
            field.help_text = document.getElementById('prop_help').value;
            field.default_value = document.getElementById('prop_default').value;
            
            const examplesText = document.getElementById('prop_examples').value;
            field.examples = examplesText ? examplesText.split('\\n').filter(e => e.trim()) : [];
            
            this.renderTemplate();
            this.updateStats();
        };
        
        // Add listeners to all property inputs
        document.querySelectorAll('.property-input, .property-select, input[type="checkbox"]').forEach(input => {
            input.addEventListener('change', updateField);
            input.addEventListener('input', updateField);
        });
    }
    
    removeField(fieldId) {
        if (confirm('Are you sure you want to remove this field?')) {
            this.currentTemplate.fields = this.currentTemplate.fields.filter(f => f.id !== fieldId);
            
            if (this.selectedField === fieldId) {
                this.selectedField = null;
            }
            
            this.renderTemplate();
            this.renderProperties();
            this.updateStats();
            this.showToast('Field removed', 'success');
        }
    }
    
    duplicateField(fieldId) {
        const field = this.currentTemplate.fields.find(f => f.id === fieldId);
        if (!field) return;
        
        const duplicatedField = {
            ...field,
            id: `field_${++this.fieldCounter}`,
            name: field.name + ' (Copy)'
        };
        
        // Insert after the original field
        const index = this.currentTemplate.fields.indexOf(field);
        this.currentTemplate.fields.splice(index + 1, 0, duplicatedField);
        
        this.renderTemplate();
        this.updateStats();
        this.selectField(duplicatedField.id);
        this.showToast('Field duplicated', 'success');
    }
    
    addQuickTemplate(templateType) {
        let fieldsToAdd = [];
        
        switch (templateType) {
            case 'basic':
                fieldsToAdd = ['title', 'creator', 'description', 'license'];
                break;
            case 'research':
                fieldsToAdd = ['title', 'creator', 'description', 'subject', 'date', 'language', 'license', 'rights'];
                break;
            case 'collection':
                fieldsToAdd = ['title', 'creator', 'description', 'subject', 'extent', 'license', 'accessRights'];
                break;
        }
        
        fieldsToAdd.forEach(fieldType => {
            this.addFieldToCanvas(fieldType);
        });
        
        // Update template name
        const nameInput = document.getElementById('templateName');
        if (!nameInput.value) {
            nameInput.value = `${templateType.charAt(0).toUpperCase() + templateType.slice(1)} Template`;
            this.currentTemplate.name = nameInput.value;
        }
        
        this.showToast(`${templateType} template created with ${fieldsToAdd.length} fields`, 'success');
    }
    
    clearAll() {
        if (confirm('Are you sure you want to clear all fields? This cannot be undone.')) {
            this.currentTemplate.fields = [];
            this.selectedField = null;
            this.renderTemplate();
            this.renderProperties();
            this.updateStats();
            this.showToast('Template cleared', 'success');
        }
    }
    
    addSection() {
        // Future enhancement: Add section grouping
        this.showToast('Section functionality coming soon!', 'info');
    }
    
    updateStats() {
        const totalFields = this.currentTemplate.fields.length;
        const requiredFields = this.currentTemplate.fields.filter(f => f.required).length;
        
        document.getElementById('fieldCount').textContent = totalFields;
        document.getElementById('requiredCount').textContent = requiredFields;
    }
    
    filterFields(searchTerm) {
        const term = searchTerm.toLowerCase();
        
        document.querySelectorAll('.field-item').forEach(item => {
            const fieldName = item.querySelector('.field-name').textContent.toLowerCase();
            const fieldType = item.dataset.fieldType;
            const fieldDef = this.fieldDefinitions[fieldType];
            const helpText = fieldDef ? fieldDef.help_text.toLowerCase() : '';
            
            const matches = fieldName.includes(term) || helpText.includes(term);
            item.style.display = matches ? 'flex' : 'none';
        });
    }
    
    showPreview() {
        const modal = document.getElementById('previewModal');
        modal.classList.add('show');
        
        // Default to visual tab
        this.switchPreviewTab('visual');
    }
    
    switchPreviewTab(tabType) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabType}"]`).classList.add('active');
        
        // Update content
        const content = document.getElementById('previewContent');
        
        switch (tabType) {
            case 'visual':
                content.innerHTML = this.generateVisualPreview();
                break;
            case 'json':
                content.innerHTML = this.generateJsonPreview();
                break;
            case 'csv':
                content.innerHTML = this.generateCsvPreview();
                break;
        }
    }
    
    generateVisualPreview() {
        const fieldsHtml = this.currentTemplate.fields.map(field => {
            const fieldDef = this.fieldDefinitions[field.type];
            return `
                <div class="preview-field">
                    <div class="preview-field-header">
                        <span class="preview-field-name">
                            <i class="${fieldDef.icon}"></i> ${field.name}
                        </span>
                        <span class="preview-field-meta">
                            ${field.required ? 'Required' : 'Optional'} • 
                            ${field.data_type} • 
                            ${field.multilingual ? 'Multilingual' : 'Monolingual'}
                        </span>
                    </div>
                    <div class="preview-field-uri">${field.property_uri}</div>
                    ${field.help_text ? `<div class="preview-field-help">${field.help_text}</div>` : ''}
                    ${field.examples && field.examples.length > 0 ? 
                        `<div class="preview-field-examples"><strong>Examples:</strong> ${field.examples.join(', ')}</div>` : ''}
                </div>
            `;
        }).join('');
        
        return `
            <div class="preview-visual">
                <div class="preview-header">
                    <h3>${this.currentTemplate.name || 'Untitled Template'}</h3>
                    <p><strong>Type:</strong> ${this.currentTemplate.resource_type}</p>
                    <p><strong>Fields:</strong> ${this.currentTemplate.fields.length} total, ${this.currentTemplate.fields.filter(f => f.required).length} required</p>
                </div>
                ${fieldsHtml}
            </div>
        `;
    }
    
    generateJsonPreview() {
        const templateJson = {
            name: this.currentTemplate.name || 'Untitled Template',
            description: this.currentTemplate.description || '',
            resource_type: this.currentTemplate.resource_type,
            fields: this.currentTemplate.fields.map(field => ({
                name: field.name,
                property_uri: field.property_uri,
                data_type: field.data_type,
                required: field.required,
                multilingual: field.multilingual,
                help_text: field.help_text,
                examples: field.examples,
                default_value: field.default_value
            }))
        };
        
        return `<pre class="preview-code">${JSON.stringify(templateJson, null, 2)}</pre>`;
    }
    
    generateCsvPreview() {
        const headers = ['field_name', 'property_uri', 'data_type', 'required', 'multilingual', 'help_text', 'examples', 'default_value'];
        const rows = this.currentTemplate.fields.map(field => [
            field.name,
            field.property_uri,
            field.data_type,
            field.required ? 'true' : 'false',
            field.multilingual ? 'true' : 'false',
            field.help_text || '',
            (field.examples || []).join('; '),
            field.default_value || ''
        ]);
        
        const csvContent = [headers, ...rows]
            .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
            .join('\\n');
        
        return `<pre class="preview-code">${csvContent}</pre>`;
    }
    
    exportTemplate() {
        if (this.currentTemplate.fields.length === 0) {
            this.showToast('Add some fields before exporting', 'error');
            return;
        }
        
        const templateJson = {
            name: this.currentTemplate.name || 'Untitled Template',
            description: this.currentTemplate.description || '',
            resource_type: this.currentTemplate.resource_type,
            created_date: new Date().toISOString(),
            fields: this.currentTemplate.fields.map(field => ({
                name: field.name,
                property_uri: field.property_uri,
                data_type: field.data_type,
                required: field.required,
                multilingual: field.multilingual,
                help_text: field.help_text,
                examples: field.examples,
                default_value: field.default_value
            }))
        };
        
        // Export as JSON
        const blob = new Blob([JSON.stringify(templateJson, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${(this.currentTemplate.name || 'template').replace(/\\s+/g, '_')}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showToast('Template exported successfully!', 'success');
    }
    
    saveTemplate() {
        if (this.currentTemplate.fields.length === 0) {
            this.showToast('Add some fields before saving', 'error');
            return;
        }
        
        if (!this.currentTemplate.name) {
            this.showToast('Please enter a template name', 'error');
            return;
        }
        
        // In a real application, this would save to a server
        // For now, we'll save to localStorage
        const savedTemplates = JSON.parse(localStorage.getItem('nakala_templates') || '[]');
        
        const templateToSave = {
            ...this.currentTemplate,
            id: Date.now().toString(),
            created_date: new Date().toISOString(),
            updated_date: new Date().toISOString()
        };
        
        savedTemplates.push(templateToSave);
        localStorage.setItem('nakala_templates', JSON.stringify(savedTemplates));
        
        this.showToast('Template saved successfully!', 'success');
    }
    
    showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }
}

// Global functions for button clicks
function closePreview() {
    document.getElementById('previewModal').classList.remove('show');
}

// Initialize the designer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.templateDesigner = new TemplateDesigner();
});

// Additional styles for dynamic elements
const additionalStyles = `
<style>
.preview-field-help {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    font-style: italic;
}

.preview-field-examples {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    padding: 0.5rem;
    background: var(--background-color);
    border-radius: var(--radius);
}

.preview-header {
    padding: 1rem;
    background: var(--primary-color);
    color: white;
    border-radius: var(--radius);
    margin-bottom: 1.5rem;
}

.preview-header h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.25rem;
}

.preview-header p {
    margin: 0.25rem 0;
    opacity: 0.9;
}

.dragging {
    opacity: 0.5;
    transform: rotate(2deg);
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', additionalStyles);