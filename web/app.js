/**
 * O-Nakala Core Web Interface
 * AI-Driven Metadata Management Dashboard
 */

class NakalaWebApp {
    constructor() {
        this.apiKey = null;
        this.apiUrl = 'http://localhost:8000/api/v1';
        this.isConnected = false;
        this.currentData = {};
        this.charts = {}; // Store Chart.js instances
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupTabNavigation();
        this.setupDragAndDrop();
        this.checkApiConnection();
    }
    
    setupEventListeners() {
        // Connection
        document.getElementById('connectBtn').addEventListener('click', () => this.connect());
        document.getElementById('apiKey').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.connect();
        });
        
        // Autonomous Generation
        document.getElementById('fileInput').addEventListener('change', (e) => this.handleFileSelect(e));
        document.getElementById('generateBtn').addEventListener('click', () => this.generateAutonomous());
        document.getElementById('exportCsvBtn')?.addEventListener('click', () => this.exportAutonomousCsv());
        document.getElementById('exportReportBtn')?.addEventListener('click', () => this.exportAutonomousReport());
        
        // Templates
        document.getElementById('generateTemplateBtn').addEventListener('click', () => this.generateTemplate());
        document.getElementById('exportTemplateBtn')?.addEventListener('click', () => this.exportTemplate());
        document.getElementById('viewDocumentationBtn')?.addEventListener('click', () => this.viewDocumentation());
        
        // Analytics
        document.getElementById('runAnalysisBtn').addEventListener('click', () => this.runAnalysis());
        
        // Batch Processing
        document.getElementById('batchFileInput').addEventListener('change', (e) => this.handleBatchFileSelect(e));
        document.getElementById('processBatchBtn').addEventListener('click', () => this.processBatch());
        
        // Modal
        document.querySelector('.modal-close')?.addEventListener('click', () => this.closeModal());
        document.getElementById('modalOverlay').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) this.closeModal();
        });
    }
    
    setupTabNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        const tabContents = document.querySelectorAll('.tab-content');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const tabId = link.dataset.tab;
                
                // Update nav links
                navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
                
                // Update tab content
                tabContents.forEach(tab => tab.classList.remove('active'));
                document.getElementById(tabId).classList.add('active');
                
                // Load tab-specific data
                this.loadTabData(tabId);
            });
        });
    }
    
    setupDragAndDrop() {
        const uploadAreas = document.querySelectorAll('.upload-area');
        
        uploadAreas.forEach(area => {
            area.addEventListener('dragover', (e) => {
                e.preventDefault();
                area.classList.add('drag-over');
            });
            
            area.addEventListener('dragleave', () => {
                area.classList.remove('drag-over');
            });
            
            area.addEventListener('drop', (e) => {
                e.preventDefault();
                area.classList.remove('drag-over');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    const fileInput = area.querySelector('.file-input');
                    fileInput.files = files;
                    
                    if (area.id === 'uploadArea') {
                        this.handleFileSelect({ target: fileInput });
                    } else if (area.id === 'batchUploadArea') {
                        this.handleBatchFileSelect({ target: fileInput });
                    }
                }
            });
        });
    }
    
    async checkApiConnection() {
        try {
            const response = await fetch(`${this.apiUrl.replace('/api/v1', '')}/`);
            if (response.ok) {
                this.showToast('API server is running', 'success');
            }
        } catch (error) {
            this.showToast('API server not accessible. Please start the server.', 'error');
        }
    }
    
    async connect() {
        const apiKeyInput = document.getElementById('apiKey');
        const apiKey = apiKeyInput.value.trim();
        
        if (!apiKey) {
            this.showToast('Please enter an API key', 'error');
            return;
        }
        
        this.showLoading();
        
        try {
            // Test connection with a simple request
            const response = await this.makeRequest('/templates/generate', 'POST', {
                resource_type: 'dataset'
            }, apiKey);
            
            if (response.ok || response.status === 422) { // 422 is validation error, means auth worked
                this.apiKey = apiKey;
                this.isConnected = true;
                this.updateConnectionStatus(true);
                this.showToast('Connected successfully!', 'success');
                this.loadDashboard();
                this.startDashboardUpdates();
            } else {
                throw new Error('Connection failed');
            }
        } catch (error) {
            this.showToast('Connection failed. Please check your API key.', 'error');
            this.updateConnectionStatus(false);
            this.stopDashboardUpdates();
        } finally {
            this.hideLoading();
        }
    }
    
    updateConnectionStatus(connected) {
        const statusIndicator = document.querySelector('.status-indicator');
        const statusText = document.querySelector('.status-text');
        
        if (connected) {
            statusIndicator.classList.remove('disconnected');
            statusIndicator.classList.add('connected');
            statusText.textContent = 'Connected';
        } else {
            statusIndicator.classList.remove('connected');
            statusIndicator.classList.add('disconnected');
            statusText.textContent = 'Disconnected';
        }
    }
    
    async loadDashboard() {
        if (!this.isConnected) return;
        
        try {
            // Load dashboard stats (mock data for now)
            this.updateDashboardStats({
                healthScore: '75%',
                qualityScore: '82%',
                completenessScore: '68%',
                aiPredictions: '12'
            });
            
            // Add recent activity
            this.addActivity('Autonomous metadata generated', 'Just now');
            
        } catch (error) {
            console.error('Failed to load dashboard:', error);
        }
    }
    
    updateDashboardStats(stats) {
        document.getElementById('healthScore').textContent = stats.healthScore;
        document.getElementById('qualityScore').textContent = stats.qualityScore;
        document.getElementById('completenessScore').textContent = stats.completenessScore;
        document.getElementById('aiPredictions').textContent = stats.aiPredictions;
    }
    
    addActivity(title, time) {
        const activityList = document.getElementById('activityList');
        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';
        activityItem.innerHTML = `
            <div class="activity-icon"><i class="fas fa-robot"></i></div>
            <div class="activity-content">
                <div class="activity-title">${title}</div>
                <div class="activity-time">${time}</div>
            </div>
        `;
        activityList.insertBefore(activityItem, activityList.firstChild);
    }
    
    loadTabData(tabId) {
        // Load tab-specific data when switching tabs
        switch (tabId) {
            case 'dashboard':
                this.loadDashboard();
                break;
            case 'analytics':
                // Initialize empty charts if they haven't been created
                if (this.isConnected && !this.charts.quality) {
                    this.initializeEmptyCharts();
                }
                break;
            case 'autonomous':
                // Clear previous results when switching
                document.getElementById('resultsSection').style.display = 'none';
                break;
            case 'templates':
                // Clear previous template results
                document.getElementById('templateResults').style.display = 'none';
                break;
            case 'batch':
                // Clear previous batch results
                document.getElementById('batchResults').style.display = 'none';
                break;
        }
    }
    
    initializeEmptyCharts() {
        // Initialize charts with sample data for demo purposes
        this.createQualityChart([
            { timeframe: '1M', current_value: 0.70, predicted_value: 0.75 },
            { timeframe: '3M', current_value: 0.70, predicted_value: 0.78 },
            { timeframe: '6M', current_value: 0.70, predicted_value: 0.82 },
            { timeframe: '1Y', current_value: 0.70, predicted_value: 0.85 }
        ]);
        
        this.createCompletenessChart([
            { field_name: 'Title', current_rate: 0.95, predicted_rate: 0.98 },
            { field_name: 'Creator', current_rate: 0.85, predicted_rate: 0.90 },
            { field_name: 'Subject', current_rate: 0.60, predicted_rate: 0.75 },
            { field_name: 'Description', current_rate: 0.70, predicted_rate: 0.80 },
            { field_name: 'Rights', current_rate: 0.40, predicted_rate: 0.65 },
            { field_name: 'Format', current_rate: 0.90, predicted_rate: 0.95 }
        ]);
        
        this.createUsageChart([
            { metric: 'API Calls', predicted_value: 45 },
            { metric: 'File Uploads', predicted_value: 25 },
            { metric: 'Metadata Updates', predicted_value: 20 },
            { metric: 'Downloads', predicted_value: 35 },
            { metric: 'Template Usage', predicted_value: 15 }
        ]);
        
        this.createHealthChart(0.758);
    }
    
    startDashboardUpdates() {
        // Start real-time dashboard updates every 30 seconds
        if (this.dashboardTimer) {
            clearInterval(this.dashboardTimer);
        }
        
        this.dashboardTimer = setInterval(() => {
            if (this.isConnected) {
                this.updateDashboardRealtime();
            }
        }, 30000); // Update every 30 seconds
    }
    
    stopDashboardUpdates() {
        if (this.dashboardTimer) {
            clearInterval(this.dashboardTimer);
            this.dashboardTimer = null;
        }
    }
    
    updateDashboardRealtime() {
        // Simulate real-time data updates
        const healthScore = (Math.random() * 0.3 + 0.65).toFixed(1) + '%';
        const qualityScore = (Math.random() * 0.2 + 0.75).toFixed(1) + '%';
        const completenessScore = (Math.random() * 0.25 + 0.60).toFixed(1) + '%';
        const aiPredictions = Math.floor(Math.random() * 8 + 10);
        
        this.updateDashboardStats({
            healthScore,
            qualityScore,
            completenessScore,
            aiPredictions: aiPredictions.toString()
        });
        
        // Add activity notification
        const activities = [
            'Quality analysis completed',
            'New template generated',
            'Autonomous metadata updated',
            'Predictive report ready',
            'Batch processing completed'
        ];
        
        const randomActivity = activities[Math.floor(Math.random() * activities.length)];
        const timeAgo = Math.floor(Math.random() * 5 + 1) + ' min ago';
        this.addActivity(randomActivity, timeAgo);
    }
    
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            const generateBtn = document.getElementById('generateBtn');
            generateBtn.disabled = false;
            generateBtn.innerHTML = `<i class="fas fa-magic"></i> Generate Metadata for "${file.name}"`;
            
            this.currentData.selectedFile = file;
        }
    }
    
    async generateAutonomous() {
        if (!this.isConnected) {
            this.showToast('Please connect first', 'error');
            return;
        }
        
        const file = this.currentData.selectedFile;
        const resourceType = document.getElementById('resourceType').value;
        
        if (!file) {
            this.showToast('Please select a file first', 'error');
            return;
        }
        
        this.showLoading();
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('resource_type', resourceType);
            
            const response = await fetch(`${this.apiUrl}/autonomous/generate`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`
                },
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const result = await response.json();
            this.displayAutonomousResults(result);
            this.showToast('Autonomous metadata generated successfully!', 'success');
            
        } catch (error) {
            console.error('Autonomous generation failed:', error);
            this.showToast('Autonomous generation failed: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    displayAutonomousResults(result) {
        // Update stats badges
        document.getElementById('qualityBadge').textContent = `Quality: ${(result.quality_score * 100).toFixed(0)}%`;
        document.getElementById('completenessBadge').textContent = `Completeness: ${(result.completeness_score * 100).toFixed(0)}%`;
        
        const avgConfidence = Object.values(result.confidence_scores).reduce((a, b) => a + b, 0) / Object.keys(result.confidence_scores).length;
        document.getElementById('confidenceBadge').textContent = `Confidence: ${(avgConfidence * 100).toFixed(0)}%`;
        
        // Display generated metadata
        const metadataList = document.getElementById('metadataList');
        metadataList.innerHTML = '';
        
        Object.entries(result.generated_metadata).forEach(([field, value]) => {
            const confidence = result.confidence_scores[field] || 0;
            const item = document.createElement('div');
            item.className = 'metadata-item';
            item.innerHTML = `
                <div class="metadata-field">${field}</div>
                <div class="metadata-value" title="${value}">${value}</div>
                <div class="confidence-badge">${(confidence * 100).toFixed(0)}%</div>
            `;
            metadataList.appendChild(item);
        });
        
        // Display content analysis
        const analysisDetails = document.getElementById('analysisDetails');
        analysisDetails.innerHTML = `
            <div class="analysis-item">
                <strong>Content Type:</strong> ${result.content_analysis.content_type}
            </div>
            <div class="analysis-item">
                <strong>Detected Language:</strong> ${result.content_analysis.detected_language}
            </div>
            <div class="analysis-item">
                <strong>Detection Confidence:</strong> ${(result.content_analysis.confidence_score * 100).toFixed(0)}%
            </div>
            <div class="analysis-item">
                <strong>Processing Time:</strong> ${result.processing_time.toFixed(2)}s
            </div>
        `;
        
        // Display recommendations
        const recommendationsList = document.getElementById('recommendationsList');
        recommendationsList.innerHTML = '';
        
        result.recommendations.forEach(rec => {
            const item = document.createElement('div');
            item.className = 'recommendation-item';
            item.textContent = rec;
            recommendationsList.appendChild(item);
        });
        
        // Show results section
        document.getElementById('resultsSection').style.display = 'block';
        
        // Store results for export
        this.currentData.autonomousResult = result;
    }
    
    async generateTemplate() {
        if (!this.isConnected) {
            this.showToast('Please connect first', 'error');
            return;
        }
        
        const resourceType = document.getElementById('templateResourceType').value;
        const templateName = document.getElementById('templateName').value;
        const includeOptional = document.getElementById('includeOptional').checked;
        
        this.showLoading();
        
        try {
            const response = await this.makeRequest('/templates/generate', 'POST', {
                resource_type: resourceType,
                template_name: templateName || null,
                include_optional: includeOptional
            });
            
            const result = await response.json();
            this.displayTemplateResults(result);
            this.showToast('Template generated successfully!', 'success');
            
        } catch (error) {
            console.error('Template generation failed:', error);
            this.showToast('Template generation failed: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    displayTemplateResults(result) {
        // Display template info
        const templateInfo = document.getElementById('templateInfo');
        templateInfo.innerHTML = `
            <div class="template-stat">
                <strong>Name:</strong> ${result.template.name}
            </div>
            <div class="template-stat">
                <strong>Resource Type:</strong> ${result.template.resource_type}
            </div>
            <div class="template-stat">
                <strong>Total Fields:</strong> ${result.field_count}
            </div>
            <div class="template-stat">
                <strong>Required Fields:</strong> ${result.required_fields}
            </div>
        `;
        
        // Display fields
        const fieldsList = document.getElementById('fieldsList');
        fieldsList.innerHTML = '';
        
        result.template.fields.forEach(field => {
            const fieldItem = document.createElement('div');
            fieldItem.className = 'field-item';
            fieldItem.innerHTML = `
                <div class="field-header">
                    <span class="field-name">${field.name}</span>
                    ${field.required ? '<span class="required-badge">Required</span>' : ''}
                    ${field.multilingual ? '<span class="multilingual-badge">Multilingual</span>' : ''}
                </div>
                <div class="field-details">
                    <div class="field-uri">${field.property_uri}</div>
                    ${field.help_text ? `<div class="field-help">${field.help_text}</div>` : ''}
                    ${field.examples ? `<div class="field-examples">Examples: ${field.examples.join(', ')}</div>` : ''}
                </div>
            `;
            fieldsList.appendChild(fieldItem);
        });
        
        // Show results
        document.getElementById('templateResults').style.display = 'block';
        
        // Store for export
        this.currentData.templateResult = result;
    }
    
    async runAnalysis() {
        if (!this.isConnected) {
            this.showToast('Please connect first', 'error');
            return;
        }
        
        // Get selected timeframes
        const timeframes = Array.from(document.querySelectorAll('input[type="checkbox"][value]'))
            .filter(cb => cb.checked)
            .map(cb => cb.value);
        
        const includeQuality = document.getElementById('includeQuality').checked;
        const includeCompleteness = document.getElementById('includeCompleteness').checked;
        const includeUsage = document.getElementById('includeUsage').checked;
        
        this.showLoading();
        
        try {
            const response = await this.makeRequest('/analytics/predict', 'POST', {
                timeframes: timeframes.length > 0 ? timeframes : null,
                include_quality: includeQuality,
                include_completeness: includeCompleteness,
                include_usage: includeUsage
            });
            
            const result = await response.json();
            this.displayAnalyticsResults(result);
            this.showToast('Predictive analysis completed!', 'success');
            
        } catch (error) {
            console.error('Analytics failed:', error);
            this.showToast('Analytics failed: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    displayAnalyticsResults(result) {
        // Update overview stats
        document.getElementById('analyticsHealthScore').textContent = `${(result.health_score * 100).toFixed(0)}%`;
        document.getElementById('insightsCount').textContent = result.key_insights.length;
        document.getElementById('recommendationsCount').textContent = result.strategic_recommendations.length;
        
        // Create interactive charts
        this.createQualityChart(result.quality_predictions);
        this.createCompletenessChart(result.completeness_predictions);
        this.createUsageChart(result.usage_predictions);
        this.createHealthChart(result.health_score);
        
        // Display insights
        const insightsList = document.getElementById('keyInsightsList');
        insightsList.innerHTML = '';
        
        result.key_insights.forEach(insight => {
            const item = document.createElement('div');
            item.className = 'insight-item';
            item.textContent = insight;
            insightsList.appendChild(item);
        });
        
        // Display recommendations
        const recommendationsList = document.getElementById('strategicRecommendationsList');
        recommendationsList.innerHTML = '';
        
        result.strategic_recommendations.forEach(rec => {
            const item = document.createElement('div');
            item.className = 'recommendation-item';
            item.textContent = rec;
            recommendationsList.appendChild(item);
        });
        
        // Show results
        document.getElementById('analyticsResults').style.display = 'block';
        
        // Store for later use
        this.currentData.analyticsResult = result;
    }
    
    createQualityChart(qualityPredictions) {
        const ctx = document.getElementById('qualityChart');
        if (!ctx) return;
        
        // Destroy existing chart if it exists
        if (this.charts.quality) {
            this.charts.quality.destroy();
        }
        
        // Prepare data for line chart
        const labels = qualityPredictions.map(pred => pred.timeframe || '1M');
        const data = qualityPredictions.map(pred => (pred.predicted_value || pred.current_value || 0.75) * 100);
        const currentData = qualityPredictions.map(pred => (pred.current_value || 0.70) * 100);
        
        this.charts.quality = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Predicted Quality',
                    data: data,
                    borderColor: 'rgb(37, 99, 235)',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'Current Quality',
                    data: currentData,
                    borderColor: 'rgb(107, 114, 128)',
                    backgroundColor: 'rgba(107, 114, 128, 0.1)',
                    borderDash: [5, 5],
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Quality Trends Over Time'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }
    
    createCompletenessChart(completenessPredictions) {
        const ctx = document.getElementById('completenessChart');
        if (!ctx) return;
        
        if (this.charts.completeness) {
            this.charts.completeness.destroy();
        }
        
        // Prepare data for bar chart showing field completion rates
        const fields = completenessPredictions.slice(0, 8).map(pred => pred.field_name || 'Field');
        const currentRates = completenessPredictions.slice(0, 8).map(pred => (pred.current_rate || 0.6) * 100);
        const predictedRates = completenessPredictions.slice(0, 8).map(pred => (pred.predicted_rate || 0.75) * 100);
        
        this.charts.completeness = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: fields,
                datasets: [{
                    label: 'Current Rate',
                    data: currentRates,
                    backgroundColor: 'rgba(107, 114, 128, 0.7)',
                    borderColor: 'rgb(107, 114, 128)',
                    borderWidth: 1
                }, {
                    label: 'Predicted Rate',
                    data: predictedRates,
                    backgroundColor: 'rgba(34, 197, 94, 0.7)',
                    borderColor: 'rgb(34, 197, 94)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Field Completion Predictions'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }
    
    createUsageChart(usagePredictions) {
        const ctx = document.getElementById('usageChart');
        if (!ctx) return;
        
        if (this.charts.usage) {
            this.charts.usage.destroy();
        }
        
        // Create doughnut chart for usage distribution
        const metrics = usagePredictions.slice(0, 5).map(pred => pred.metric || 'Usage');
        const values = usagePredictions.slice(0, 5).map(pred => pred.predicted_value || Math.random() * 100);
        
        this.charts.usage = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: metrics,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        'rgba(37, 99, 235, 0.8)',
                        'rgba(34, 197, 94, 0.8)',
                        'rgba(251, 191, 36, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(168, 85, 247, 0.8)'
                    ],
                    borderColor: [
                        'rgb(37, 99, 235)',
                        'rgb(34, 197, 94)',
                        'rgb(251, 191, 36)',
                        'rgb(239, 68, 68)',
                        'rgb(168, 85, 247)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Usage Analytics Distribution'
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    createHealthChart(healthScore) {
        const ctx = document.getElementById('healthChart');
        if (!ctx) return;
        
        if (this.charts.health) {
            this.charts.health.destroy();
        }
        
        // Create gauge-like chart using doughnut
        const score = (healthScore || 0.75) * 100;
        const remaining = 100 - score;
        
        this.charts.health = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Health Score', 'Remaining'],
                datasets: [{
                    data: [score, remaining],
                    backgroundColor: [
                        score >= 80 ? 'rgba(34, 197, 94, 0.8)' : 
                        score >= 60 ? 'rgba(251, 191, 36, 0.8)' : 
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(229, 231, 235, 0.3)'
                    ],
                    borderColor: [
                        score >= 80 ? 'rgb(34, 197, 94)' : 
                        score >= 60 ? 'rgb(251, 191, 36)' : 
                        'rgb(239, 68, 68)',
                        'rgba(229, 231, 235, 0.8)'
                    ],
                    borderWidth: 2,
                    cutout: '70%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Repository Health Score'
                    },
                    legend: {
                        display: false
                    }
                }
            },
            plugins: [{
                afterDraw: function(chart) {
                    const ctx = chart.ctx;
                    const centerX = chart.width / 2;
                    const centerY = chart.height / 2;
                    
                    ctx.fillStyle = '#1f2937';
                    ctx.font = 'bold 24px Inter';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(score.toFixed(0) + '%', centerX, centerY);
                }
            }]
        });
    }
    
    handleBatchFileSelect(event) {
        const file = event.target.files[0];
        if (file && file.name.endsWith('.csv')) {
            const processBtn = document.getElementById('processBatchBtn');
            processBtn.disabled = false;
            processBtn.innerHTML = `<i class="fas fa-cogs"></i> Process "${file.name}"`;
            
            this.currentData.batchFile = file;
        } else {
            this.showToast('Please select a CSV file', 'error');
        }
    }
    
    async processBatch() {
        if (!this.isConnected) {
            this.showToast('Please connect first', 'error');
            return;
        }
        
        const file = this.currentData.batchFile;
        const dryRun = document.getElementById('dryRun').checked;
        
        if (!file) {
            this.showToast('Please select a CSV file first', 'error');
            return;
        }
        
        this.showLoading();
        
        try {
            // First parse the CSV
            const formData = new FormData();
            formData.append('file', file);
            
            const parseResponse = await fetch(`${this.apiUrl}/csv/parse`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`
                },
                body: formData
            });
            
            if (!parseResponse.ok) {
                throw new Error('Failed to parse CSV');
            }
            
            const parseResult = await parseResponse.json();
            
            // Then process the modifications
            const processResponse = await this.makeRequest('/batch/modify', 'POST', {
                modifications: parseResult.data.modifications,
                dry_run: dryRun
            });
            
            const result = await processResponse.json();
            this.displayBatchResults(result.data);
            this.showToast(`Batch ${dryRun ? 'simulation' : 'processing'} completed!`, 'success');
            
        } catch (error) {
            console.error('Batch processing failed:', error);
            this.showToast('Batch processing failed: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    displayBatchResults(result) {
        // Update summary stats
        document.getElementById('successfulCount').textContent = result.successful;
        document.getElementById('failedCount').textContent = result.failed;
        document.getElementById('skippedCount').textContent = result.skipped;
        
        // Show results
        document.getElementById('batchResults').style.display = 'block';
        
        // Store for detail view
        this.currentData.batchResult = result;
    }
    
    async makeRequest(endpoint, method = 'GET', data = null, apiKey = null) {
        const url = `${this.apiUrl}${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey || this.apiKey}`
            }
        };
        
        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return response;
    }
    
    showLoading() {
        document.getElementById('loadingOverlay').classList.add('show');
    }
    
    hideLoading() {
        document.getElementById('loadingOverlay').classList.remove('show');
    }
    
    showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        container.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }
    
    showModal(content) {
        document.getElementById('modalContent').innerHTML = content;
        document.getElementById('modalOverlay').classList.add('show');
    }
    
    closeModal() {
        document.getElementById('modalOverlay').classList.remove('show');
    }
    
    viewDocumentation() {
        if (this.currentData.templateResult) {
            this.showModal(`<pre>${this.currentData.templateResult.documentation}</pre>`);
        }
    }
    
    async exportAutonomousCsv() {
        if (!this.currentData.autonomousResult) {
            this.showToast('No autonomous result to export', 'error');
            return;
        }
        
        // Create CSV content
        const result = this.currentData.autonomousResult;
        const headers = ['field', 'value', 'confidence'];
        const rows = Object.entries(result.generated_metadata).map(([field, value]) => [
            field,
            value,
            (result.confidence_scores[field] * 100).toFixed(0) + '%'
        ]);
        
        const csvContent = [headers, ...rows]
            .map(row => row.map(cell => `"${cell}"`).join(','))
            .join('\n');
        
        this.downloadFile(csvContent, 'autonomous_metadata.csv', 'text/csv');
    }
    
    exportAutonomousReport() {
        if (!this.currentData.autonomousResult) {
            this.showToast('No autonomous result to export', 'error');
            return;
        }
        
        const result = this.currentData.autonomousResult;
        const report = `
O-Nakala Core - Autonomous Metadata Generation Report
Generated: ${new Date().toLocaleString()}

Content Analysis:
- Content Type: ${result.content_analysis.content_type}
- Detected Language: ${result.content_analysis.detected_language}
- Detection Confidence: ${(result.content_analysis.confidence_score * 100).toFixed(0)}%
- Processing Time: ${result.processing_time.toFixed(2)}s

Quality Metrics:
- Quality Score: ${(result.quality_score * 100).toFixed(0)}%
- Completeness Score: ${(result.completeness_score * 100).toFixed(0)}%

Generated Metadata:
${Object.entries(result.generated_metadata).map(([field, value]) => 
    `- ${field}: ${value} (${(result.confidence_scores[field] * 100).toFixed(0)}% confidence)`
).join('\n')}

Recommendations:
${result.recommendations.map(rec => `- ${rec}`).join('\n')}
        `.trim();
        
        this.downloadFile(report, 'autonomous_report.txt', 'text/plain');
    }
    
    async exportTemplate() {
        if (!this.currentData.templateResult) {
            this.showToast('No template to export', 'error');
            return;
        }
        
        try {
            const template = this.currentData.templateResult.template;
            
            // Create CSV headers
            const headers = ['field_name', 'property_uri', 'required', 'multilingual', 'data_type', 'help_text', 'examples'];
            
            // Convert template to CSV rows
            const rows = template.fields.map(field => [
                field.name,
                field.property_uri,
                field.required ? 'true' : 'false',
                field.multilingual ? 'true' : 'false',
                field.data_type || 'string',
                field.help_text || '',
                field.examples ? field.examples.join('; ') : ''
            ]);
            
            // Create CSV content
            const csvContent = [headers, ...rows]
                .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
                .join('\\n');
            
            this.downloadFile(csvContent, `template_${template.name.replace(/\\s+/g, '_')}.csv`, 'text/csv');
            this.showToast('Template exported successfully!', 'success');
            
        } catch (error) {
            console.error('Template export failed:', error);
            this.showToast('Template export failed: ' + error.message, 'error');
        }
    }
    
    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        // Add visual feedback
        this.addActivity(`Exported ${filename}`, 'Just now');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.nakalaApp = new NakalaWebApp();
});

// Add some additional CSS for dynamic elements
const additionalStyles = `
<style>
.confidence-badge {
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
    background: var(--primary-color);
    color: white;
    border-radius: 9999px;
    font-weight: 500;
}

.field-item {
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 1rem;
    margin-bottom: 0.75rem;
}

.field-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.field-name {
    font-weight: 600;
    color: var(--text-primary);
}

.required-badge {
    font-size: 0.75rem;
    padding: 0.125rem 0.5rem;
    background: var(--error-color);
    color: white;
    border-radius: 9999px;
}

.multilingual-badge {
    font-size: 0.75rem;
    padding: 0.125rem 0.5rem;
    background: var(--warning-color);
    color: white;
    border-radius: 9999px;
}

.field-details {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.field-uri {
    font-family: monospace;
    background: var(--background-color);
    padding: 0.25rem 0.5rem;
    border-radius: var(--radius);
    margin: 0.25rem 0;
}

.analysis-item {
    margin-bottom: 0.5rem;
    padding: 0.5rem;
    background: var(--background-color);
    border-radius: var(--radius);
}

.template-stat {
    margin-bottom: 0.5rem;
    padding: 0.5rem;
    background: var(--background-color);
    border-radius: var(--radius);
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', additionalStyles);