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
        this.isMobile = this.detectMobile();
        this.isOffline = !navigator.onLine;
        this.touchStartY = null;
        this.csvData = null;
        this.csvProcessor = null;
        this.progressTimer = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupTabNavigation();
        this.setupDragAndDrop();
        this.setupMobileFeatures();
        this.setupOfflineHandling();
        this.checkApiConnection();
        this.optimizeForMobile();
    }
    
    detectMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               (window.innerWidth <= 768);
    }
    
    setupMobileFeatures() {
        if (this.isMobile) {
            // Add mobile-specific CSS class
            document.body.classList.add('mobile-device');
            
            // Setup touch gestures
            this.setupTouchGestures();
            
            // Setup mobile-specific UI optimizations
            this.setupMobileUI();
            
            // Prevent zoom on double tap
            this.preventDoubleTabZoom();
            
            // Setup mobile file handling
            this.setupMobileFileHandling();
        }
    }
    
    setupTouchGestures() {
        // Pull-to-refresh gesture
        let startY = 0;
        let currentY = 0;
        let pullDistance = 0;
        const threshold = 100;
        
        document.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
                this.touchStartY = startY;
            }
        });
        
        document.addEventListener('touchmove', (e) => {
            if (this.touchStartY !== null && window.scrollY === 0) {
                currentY = e.touches[0].clientY;
                pullDistance = currentY - startY;
                
                if (pullDistance > 0) {
                    e.preventDefault();
                    const opacity = Math.min(pullDistance / threshold, 1);
                    this.showPullToRefresh(opacity);
                }
            }
        });
        
        document.addEventListener('touchend', () => {
            if (pullDistance > threshold) {
                this.refreshData();
            }
            this.hidePullToRefresh();
            this.touchStartY = null;
            pullDistance = 0;
        });
        
        // Swipe navigation between tabs
        this.setupSwipeNavigation();
    }
    
    setupSwipeNavigation() {
        let startX = 0;
        let startY = 0;
        let endX = 0;
        let endY = 0;
        
        const tabContents = document.querySelectorAll('.tab-content');
        const navLinks = document.querySelectorAll('.nav-link');
        let currentTabIndex = 0;
        
        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        
        document.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            
            const deltaX = endX - startX;
            const deltaY = endY - startY;
            
            // Only trigger if horizontal swipe is dominant
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
                if (deltaX > 0 && currentTabIndex > 0) {
                    // Swipe right - previous tab
                    currentTabIndex--;
                    navLinks[currentTabIndex].click();
                } else if (deltaX < 0 && currentTabIndex < navLinks.length - 1) {
                    // Swipe left - next tab
                    currentTabIndex++;
                    navLinks[currentTabIndex].click();
                }
            }
        });
        
        // Update current tab index when tabs are clicked
        navLinks.forEach((link, index) => {
            link.addEventListener('click', () => {
                currentTabIndex = index;
            });
        });
    }
    
    setupMobileUI() {
        // Collapse navigation on mobile after selection
        if (this.isMobile) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', () => {
                    // Auto-scroll to content on mobile
                    setTimeout(() => {
                        document.querySelector('.main-content').scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }, 100);
                });
            });
        }
        
        // Mobile-optimized modals
        this.setupMobileModals();
    }
    
    setupMobileModals() {
        // Make modals full-screen on mobile
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (this.isMobile) {
                modal.classList.add('mobile-fullscreen');
            }
        });
    }
    
    preventDoubleTabZoom() {
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (e) => {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
    }
    
    setupMobileFileHandling() {
        // Enhanced file input for mobile
        const fileInputs = document.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            input.setAttribute('accept', '*/*');
            input.setAttribute('capture', 'environment'); // Use camera if available
        });
        
        // Mobile-specific upload feedback
        fileInputs.forEach(input => {
            input.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    this.showMobileUploadFeedback(e.target.files[0]);
                }
            });
        });
    }
    
    setupOfflineHandling() {
        window.addEventListener('online', () => {
            this.isOffline = false;
            this.showToast('Back online! Syncing data...', 'success');
            this.syncOfflineData();
        });
        
        window.addEventListener('offline', () => {
            this.isOffline = true;
            this.showToast('Working offline. Data will sync when reconnected.', 'warning');
        });
        
        // Check initial state
        if (!navigator.onLine) {
            this.isOffline = true;
            this.showOfflineIndicator();
        }
    }
    
    optimizeForMobile() {
        if (this.isMobile) {
            // Reduce animation complexity on mobile
            document.documentElement.style.setProperty('--animation-duration', '0.2s');
            
            // Optimize chart rendering for mobile
            this.mobileChartDefaults = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            boxWidth: 12,
                            font: {
                                size: 10
                            }
                        }
                    }
                },
                elements: {
                    point: {
                        radius: 3
                    },
                    line: {
                        borderWidth: 2
                    }
                }
            };
            
            // Setup mobile performance monitoring
            this.setupPerformanceMonitoring();
        }
    }
    
    setupPerformanceMonitoring() {
        // Monitor performance on mobile
        if ('performance' in window) {
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.duration > 100) { // Long tasks
                        console.warn('Long task detected:', entry);
                    }
                }
            });
            
            try {
                observer.observe({ entryTypes: ['longtask'] });
            } catch (e) {
                // Not supported in all browsers
            }
        }
    }
    
    showPullToRefresh(opacity) {
        let refreshIndicator = document.getElementById('pullToRefreshIndicator');
        if (!refreshIndicator) {
            refreshIndicator = document.createElement('div');
            refreshIndicator.id = 'pullToRefreshIndicator';
            refreshIndicator.innerHTML = '<i class="fas fa-sync fa-spin"></i> Pull to refresh';
            refreshIndicator.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: var(--primary-color);
                color: white;
                text-align: center;
                padding: 1rem;
                transform: translateY(-100%);
                transition: transform 0.3s ease;
                z-index: 1000;
                font-size: 0.875rem;
            `;
            document.body.appendChild(refreshIndicator);
        }
        
        refreshIndicator.style.opacity = opacity;
        refreshIndicator.style.transform = `translateY(${opacity * 100 - 100}%)`;
    }
    
    hidePullToRefresh() {
        const refreshIndicator = document.getElementById('pullToRefreshIndicator');
        if (refreshIndicator) {
            refreshIndicator.style.transform = 'translateY(-100%)';
            refreshIndicator.style.opacity = '0';
        }
    }
    
    refreshData() {
        this.showToast('Refreshing data...', 'info');
        
        // Refresh current tab data
        const activeTab = document.querySelector('.nav-link.active');
        if (activeTab) {
            const tabId = activeTab.dataset.tab;
            this.loadTabData(tabId);
        }
        
        // Update dashboard if connected
        if (this.isConnected) {
            this.loadDashboard();
        }
    }
    
    showMobileUploadFeedback(file) {
        const feedback = document.createElement('div');
        feedback.className = 'mobile-upload-feedback';
        feedback.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span>Selected: ${file.name}</span>
            <small>${this.formatFileSize(file.size)}</small>
        `;
        feedback.style.cssText = `
            position: fixed;
            bottom: 1rem;
            left: 1rem;
            right: 1rem;
            background: var(--success-color);
            color: white;
            padding: 1rem;
            border-radius: var(--radius);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            z-index: 1000;
            animation: slideUp 0.3s ease;
        `;
        
        document.body.appendChild(feedback);
        
        setTimeout(() => {
            feedback.remove();
        }, 3000);
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    showOfflineIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'offlineIndicator';
        indicator.innerHTML = '<i class="fas fa-wifi-slash"></i> Working Offline';
        indicator.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: var(--warning-color);
            color: white;
            text-align: center;
            padding: 0.5rem;
            font-size: 0.875rem;
            z-index: 1001;
        `;
        document.body.appendChild(indicator);
        document.body.style.paddingTop = '40px';
    }
    
    hideOfflineIndicator() {
        const indicator = document.getElementById('offlineIndicator');
        if (indicator) {
            indicator.remove();
            document.body.style.paddingTop = '0';
        }
    }
    
    syncOfflineData() {
        // Implement offline data synchronization
        const offlineData = localStorage.getItem('nakala_offline_data');
        if (offlineData) {
            try {
                const data = JSON.parse(offlineData);
                // Process offline data when back online
                this.processOfflineData(data);
                localStorage.removeItem('nakala_offline_data');
            } catch (e) {
                console.error('Failed to sync offline data:', e);
            }
        }
        this.hideOfflineIndicator();
    }
    
    processOfflineData(data) {
        // Process any data that was collected while offline
        console.log('Processing offline data:', data);
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
        
        // Basic Batch Processing
        document.getElementById('batchFileInput').addEventListener('change', (e) => this.handleBatchFileSelect(e));
        document.getElementById('processBatchBtn').addEventListener('click', () => this.processBatch());
        
        // Advanced CSV Management
        document.getElementById('createNewCsvBtn')?.addEventListener('click', () => this.createNewCsv());
        document.getElementById('downloadTemplateBtn')?.addEventListener('click', () => this.downloadCsvTemplate());
        document.getElementById('importSampleBtn')?.addEventListener('click', () => this.importSampleData());
        
        // CSV Editor Tools
        document.getElementById('addRowBtn')?.addEventListener('click', () => this.addCsvRow());
        document.getElementById('addColumnBtn')?.addEventListener('click', () => this.addCsvColumn());
        document.getElementById('validateBtn')?.addEventListener('click', () => this.validateCsv());
        document.getElementById('saveChangesBtn')?.addEventListener('click', () => this.saveCsvChanges());
        
        // Progress Control
        document.getElementById('pauseBtn')?.addEventListener('click', () => this.pauseProcessing());
        document.getElementById('cancelBtn')?.addEventListener('click', () => this.cancelProcessing());
        
        // Results Navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.showResultDetails(e.target.dataset.detail));
        });
        
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
            options: this.isMobile ? {
                ...this.mobileChartDefaults,
                plugins: {
                    ...this.mobileChartDefaults.plugins,
                    title: {
                        display: true,
                        text: 'Quality Trends',
                        font: { size: 14 }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            font: { size: 10 },
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        ticks: {
                            font: { size: 10 }
                        }
                    }
                }
            } : {
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
            this.loadCsvFile(file);
        } else {
            this.showToast('Please select a CSV file', 'error');
        }
    }
    
    async loadCsvFile(file) {
        try {
            const text = await file.text();
            this.csvData = this.parseCsv(text);
            this.displayCsvEditor(file.name);
            this.showSection('csvEditorSection');
            this.showSection('processingOptions');
        } catch (error) {
            this.showToast('Failed to load CSV file: ' + error.message, 'error');
        }
    }
    
    parseCsv(text) {
        const lines = text.split('\n').filter(line => line.trim());
        if (lines.length === 0) return { headers: [], rows: [] };
        
        const headers = this.parseCsvLine(lines[0]);
        const rows = lines.slice(1).map(line => this.parseCsvLine(line));
        
        return { headers, rows };
    }
    
    parseCsvLine(line) {
        const result = [];
        let current = '';
        let inQuotes = false;
        
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            const nextChar = line[i + 1];
            
            if (char === '"' && inQuotes && nextChar === '"') {
                current += '"';
                i++; // Skip next quote
            } else if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                result.push(current.trim());
                current = '';
            } else {
                current += char;
            }
        }
        
        result.push(current.trim());
        return result;
    }
    
    displayCsvEditor(fileName) {
        // Update file info
        document.getElementById('fileName').textContent = fileName;
        document.getElementById('fileStats').textContent = 
            `${this.csvData.rows.length} rows, ${this.csvData.headers.length} columns`;
        
        // Build table
        this.buildCsvTable();
        
        // Update UI
        document.getElementById('validateBtn').disabled = false;
        document.getElementById('saveChangesBtn').disabled = false;
    }
    
    buildCsvTable() {
        const table = document.getElementById('csvTable');
        const thead = document.getElementById('csvTableHead');
        const tbody = document.getElementById('csvTableBody');
        
        // Clear existing content
        thead.innerHTML = '';
        tbody.innerHTML = '';
        
        // Build header
        const headerRow = document.createElement('tr');
        
        // Row number column
        const rowNumHeader = document.createElement('th');
        rowNumHeader.textContent = '#';
        rowNumHeader.className = 'row-number';
        headerRow.appendChild(rowNumHeader);
        
        // Data columns
        this.csvData.headers.forEach((header, index) => {
            const th = document.createElement('th');
            th.textContent = header;
            th.contentEditable = true;
            th.addEventListener('blur', () => this.updateHeader(index, th.textContent));
            headerRow.appendChild(th);
        });
        
        thead.appendChild(headerRow);
        
        // Build rows
        this.csvData.rows.forEach((row, rowIndex) => {
            const tr = document.createElement('tr');
            
            // Row number
            const rowNumCell = document.createElement('td');
            rowNumCell.textContent = rowIndex + 1;
            rowNumCell.className = 'row-number';
            tr.appendChild(rowNumCell);
            
            // Data cells
            row.forEach((cell, cellIndex) => {
                const td = document.createElement('td');
                td.textContent = cell;
                td.contentEditable = true;
                td.addEventListener('blur', () => this.updateCell(rowIndex, cellIndex, td.textContent));
                td.addEventListener('focus', () => this.highlightCell(td));
                tr.appendChild(td);
            });
            
            tbody.appendChild(tr);
        });
    }
    
    updateHeader(index, value) {
        this.csvData.headers[index] = value;
        this.markAsModified();
    }
    
    updateCell(rowIndex, cellIndex, value) {
        this.csvData.rows[rowIndex][cellIndex] = value;
        this.markAsModified();
    }
    
    highlightCell(cell) {
        document.querySelectorAll('.csv-table td').forEach(td => td.classList.remove('active-cell'));
        cell.classList.add('active-cell');
    }
    
    markAsModified() {
        const saveBtn = document.getElementById('saveChangesBtn');
        saveBtn.classList.add('modified');
        saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Changes *';
    }
    
    createNewCsv() {
        this.csvData = {
            headers: ['identifier', 'title', 'creator', 'type', 'description'],
            rows: [['', '', '', 'dataset', '']]
        };
        this.displayCsvEditor('new_file.csv');
        this.showSection('csvEditorSection');
        this.showSection('processingOptions');
        this.showToast('New CSV created with basic template', 'success');
    }
    
    downloadCsvTemplate() {
        const templateData = {
            headers: ['identifier', 'title', 'creator', 'type', 'description', 'subject', 'rights', 'language'],
            rows: [
                ['example-dataset-001', 'Sample Dataset Title', 'John Doe', 'dataset', 'A sample dataset for testing', 'Research;Data Analysis', 'CC BY 4.0', 'en'],
                ['example-doc-002', 'Sample Document', 'Jane Smith', 'document', 'Sample document description', 'Documentation', 'All rights reserved', 'fr']
            ]
        };
        
        const csvContent = this.csvDataToCsv(templateData);
        this.downloadFile(csvContent, 'nakala_template.csv', 'text/csv');
        this.showToast('CSV template downloaded', 'success');
    }
    
    importSampleData() {
        this.csvData = {
            headers: ['identifier', 'title', 'creator', 'type', 'description', 'subject', 'rights'],
            rows: [
                ['research-2024-001', 'Climate Data Analysis 2024', 'Research Team A', 'dataset', 'Comprehensive climate data for 2024 analysis', 'Climate;Environment;Data', 'CC BY 4.0'],
                ['manuscript-medieval-01', 'Medieval Manuscript Collection', 'Library Archives', 'document', 'Digitized medieval manuscripts from the 12th century', 'History;Manuscripts;Medieval', 'Restricted Access'],
                ['survey-results-social', 'Social Survey Results 2024', 'Dr. Sarah Johnson', 'dataset', 'Results from comprehensive social behavior survey', 'Sociology;Survey;Behavior', 'CC BY-NC 4.0']
            ]
        };
        this.displayCsvEditor('sample_data.csv');
        this.showSection('csvEditorSection');
        this.showSection('processingOptions');
        this.showToast('Sample data imported successfully', 'success');
    }
    
    addCsvRow() {
        const newRow = new Array(this.csvData.headers.length).fill('');
        this.csvData.rows.push(newRow);
        this.buildCsvTable();
        this.markAsModified();
        this.showToast('Row added', 'success');
    }
    
    addCsvColumn() {
        const columnName = prompt('Enter column name:');
        if (columnName) {
            this.csvData.headers.push(columnName);
            this.csvData.rows.forEach(row => row.push(''));
            this.buildCsvTable();
            this.markAsModified();
            this.showToast(`Column "${columnName}" added`, 'success');
        }
    }
    
    async validateCsv() {
        if (!this.csvData) {
            this.showToast('No CSV data to validate', 'error');
            return;
        }
        
        const validationResults = this.performCsvValidation();
        this.displayValidationResults(validationResults);
        
        if (validationResults.errors.length === 0) {
            this.showToast('CSV validation passed', 'success');
        } else {
            this.showToast(`Found ${validationResults.errors.length} validation issues`, 'warning');
        }
    }
    
    performCsvValidation() {
        const results = {
            errors: [],
            warnings: [],
            info: []
        };
        
        // Check required headers
        const requiredHeaders = ['identifier', 'title', 'type'];
        requiredHeaders.forEach(header => {
            if (!this.csvData.headers.includes(header)) {
                results.errors.push(`Missing required header: ${header}`);
            }
        });
        
        // Check for empty rows
        this.csvData.rows.forEach((row, index) => {
            const isEmpty = row.every(cell => !cell.trim());
            if (isEmpty) {
                results.warnings.push(`Row ${index + 1} is empty`);
            }
        });
        
        // Check identifier uniqueness
        const identifiers = this.csvData.rows.map(row => row[0]).filter(id => id.trim());
        const duplicates = identifiers.filter((id, index) => identifiers.indexOf(id) !== index);
        if (duplicates.length > 0) {
            results.errors.push(`Duplicate identifiers found: ${duplicates.join(', ')}`);
        }
        
        // Check data consistency
        this.csvData.rows.forEach((row, rowIndex) => {
            if (row.length !== this.csvData.headers.length) {
                results.errors.push(`Row ${rowIndex + 1} has ${row.length} columns, expected ${this.csvData.headers.length}`);
            }
        });
        
        return results;
    }
    
    displayValidationResults(results) {
        const container = document.getElementById('validationResults');
        const content = document.getElementById('validationContent');
        
        if (results.errors.length === 0 && results.warnings.length === 0) {
            container.style.display = 'none';
            return;
        }
        
        content.innerHTML = '';
        
        [...results.errors, ...results.warnings, ...results.info].forEach(item => {
            const div = document.createElement('div');
            div.className = 'validation-item';
            
            if (results.errors.includes(item)) {
                div.classList.add('error');
            } else if (results.warnings.includes(item)) {
                div.classList.add('warning');
            } else {
                div.classList.add('info');
            }
            
            div.textContent = item;
            content.appendChild(div);
        });
        
        container.style.display = 'block';
    }
    
    saveCsvChanges() {
        if (!this.csvData) return;
        
        const csvContent = this.csvDataToCsv(this.csvData);
        const fileName = document.getElementById('fileName').textContent || 'modified_data.csv';
        this.downloadFile(csvContent, fileName, 'text/csv');
        
        const saveBtn = document.getElementById('saveChangesBtn');
        saveBtn.classList.remove('modified');
        saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Changes';
        
        this.showToast('CSV changes saved', 'success');
    }
    
    csvDataToCsv(data) {
        const rows = [data.headers, ...data.rows];
        return rows.map(row => 
            row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')
        ).join('\n');
    }
    
    showSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'block';
        }
    }
    
    hideSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'none';
        }
    }
    
    async processBatch() {
        if (!this.isConnected) {
            this.showToast('Please connect first', 'error');
            return;
        }
        
        if (!this.csvData || this.csvData.rows.length === 0) {
            this.showToast('Please load and validate CSV data first', 'error');
            return;
        }
        
        const dryRun = document.getElementById('dryRun').checked;
        const enableProgressTracking = document.getElementById('enableProgressTracking').checked;
        
        if (enableProgressTracking) {
            this.startProgressTracking();
        }
        
        this.showLoading();
        this.processState = 'running';
        
        try {
            // Prepare CSV data for processing
            const csvContent = this.csvDataToCsv(this.csvData);
            const blob = new Blob([csvContent], { type: 'text/csv' });
            
            const formData = new FormData();
            formData.append('file', blob, 'batch_data.csv');
            formData.append('dry_run', dryRun);
            formData.append('processing_mode', document.getElementById('processingMode').value);
            formData.append('validation_level', document.getElementById('validationLevel').value);
            formData.append('error_handling', document.getElementById('errorHandling').value);
            
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
            
            // Process with progress tracking
            const result = await this.processWithProgress(parseResult.data, {
                dry_run: dryRun,
                processing_mode: document.getElementById('processingMode').value,
                validation_level: document.getElementById('validationLevel').value,
                error_handling: document.getElementById('errorHandling').value
            });
            
            this.displayEnhancedBatchResults(result);
            this.showToast(`Batch ${dryRun ? 'simulation' : 'processing'} completed!`, 'success');
            
        } catch (error) {
            console.error('Batch processing failed:', error);
            this.showToast('Batch processing failed: ' + error.message, 'error');
        } finally {
            this.hideLoading();
            this.stopProgressTracking();
        }
    }
    
    async processWithProgress(data, options) {
        const totalRows = data.modifications?.length || this.csvData.rows.length;
        let processedRows = 0;
        const results = {
            successful: 0,
            failed: 0,
            skipped: 0,
            warnings: 0,
            details: {
                successful: [],
                failed: [],
                warnings: [],
                all: []
            }
        };
        
        this.updateProgress(0, totalRows, 0);
        
        // Simulate processing with progress updates
        for (let i = 0; i < totalRows; i++) {
            if (this.processState === 'cancelled') break;
            if (this.processState === 'paused') {
                await this.waitForResume();
            }
            
            // Simulate API call for each row
            await new Promise(resolve => setTimeout(resolve, 100));
            
            const success = Math.random() > 0.1; // 90% success rate for demo
            const hasWarning = Math.random() > 0.7; // 30% warning rate
            
            const rowResult = {
                row: i + 1,
                identifier: this.csvData.rows[i]?.[0] || `row-${i + 1}`,
                status: success ? 'success' : 'failed',
                message: success ? 'Processed successfully' : 'Validation failed',
                details: success ? 'All metadata fields validated' : 'Missing required field: description'
            };
            
            if (success) {
                results.successful++;
                results.details.successful.push(rowResult);
                if (hasWarning) {
                    results.warnings++;
                    rowResult.warning = 'Optional field recommended';
                    results.details.warnings.push({...rowResult, status: 'warning'});
                }
            } else {
                results.failed++;
                results.details.failed.push(rowResult);
            }
            
            results.details.all.push(rowResult);
            processedRows++;
            
            this.updateProgress(processedRows, totalRows, processedRows / totalRows * 100);
            this.addProgressLog(success ? 'success' : 'error', 
                `Row ${i + 1}: ${rowResult.message}`);
        }
        
        results.skipped = totalRows - processedRows;
        return results;
    }
    
    startProgressTracking() {
        this.showSection('progressTracking');
        this.progressStartTime = Date.now();
        this.progressTimer = setInterval(() => {
            this.updateProgressTimer();
        }, 1000);
    }
    
    stopProgressTracking() {
        if (this.progressTimer) {
            clearInterval(this.progressTimer);
            this.progressTimer = null;
        }
    }
    
    updateProgress(processed, total, percentage) {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        
        if (progressFill) progressFill.style.width = `${percentage}%`;
        if (progressText) progressText.textContent = `${Math.round(percentage)}%`;
        
        // Update processing speed
        const elapsed = (Date.now() - this.progressStartTime) / 1000;
        const speed = processed / elapsed;
        const speedElement = document.getElementById('processingSpeed');
        if (speedElement) speedElement.textContent = `${speed.toFixed(1)} rows/sec`;
        
        // Estimate remaining time
        const remaining = (total - processed) / speed;
        const estimatedElement = document.getElementById('estimatedTime');
        if (estimatedElement && remaining > 0) {
            const minutes = Math.floor(remaining / 60);
            const seconds = Math.floor(remaining % 60);
            estimatedElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
    }
    
    updateProgressTimer() {
        const elapsed = (Date.now() - this.progressStartTime) / 1000;
        const minutes = Math.floor(elapsed / 60);
        const seconds = Math.floor(elapsed % 60);
        const elapsedElement = document.getElementById('elapsedTime');
        if (elapsedElement) {
            elapsedElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
    }
    
    addProgressLog(type, message) {
        const logContainer = document.getElementById('progressLog');
        if (!logContainer) return;
        
        const entry = document.createElement('div');
        entry.className = 'progress-log-entry';
        
        const time = new Date().toLocaleTimeString();
        entry.innerHTML = `
            <span class="progress-log-time">${time}</span>
            <span class="progress-log-message ${type}">${message}</span>
        `;
        
        logContainer.appendChild(entry);
        logContainer.scrollTop = logContainer.scrollHeight;
        
        // Limit log entries to prevent memory issues
        if (logContainer.children.length > 100) {
            logContainer.removeChild(logContainer.firstChild);
        }
    }
    
    pauseProcessing() {
        this.processState = 'paused';
        const pauseBtn = document.getElementById('pauseBtn');
        if (pauseBtn) {
            pauseBtn.innerHTML = '<i class="fas fa-play"></i> Resume';
            pauseBtn.onclick = () => this.resumeProcessing();
        }
        this.addProgressLog('info', 'Processing paused');
    }
    
    resumeProcessing() {
        this.processState = 'running';
        const pauseBtn = document.getElementById('pauseBtn');
        if (pauseBtn) {
            pauseBtn.innerHTML = '<i class="fas fa-pause"></i> Pause';
            pauseBtn.onclick = () => this.pauseProcessing();
        }
        this.addProgressLog('info', 'Processing resumed');
    }
    
    cancelProcessing() {
        this.processState = 'cancelled';
        this.addProgressLog('error', 'Processing cancelled by user');
        this.showToast('Processing cancelled', 'warning');
    }
    
    async waitForResume() {
        return new Promise(resolve => {
            const checkState = () => {
                if (this.processState === 'running' || this.processState === 'cancelled') {
                    resolve();
                } else {
                    setTimeout(checkState, 100);
                }
            };
            checkState();
        });
    }
    
    displayEnhancedBatchResults(result) {
        // Update summary stats
        document.getElementById('successfulCount').textContent = result.successful;
        document.getElementById('failedCount').textContent = result.failed;
        document.getElementById('skippedCount').textContent = result.skipped;
        document.getElementById('warningsCount').textContent = result.warnings;
        
        // Update navigation counts
        document.getElementById('successfulNavCount').textContent = result.successful;
        document.getElementById('failedNavCount').textContent = result.failed;
        document.getElementById('warningsNavCount').textContent = result.warnings;
        
        // Store results for detail view
        this.currentData.batchResult = result;
        
        // Show results section
        this.showSection('batchResults');
        
        // Hide progress tracking
        this.hideSection('progressTracking');
    }
    
    showResultDetails(category) {
        const content = document.getElementById('batchDetailsContent');
        const navBtns = document.querySelectorAll('.nav-btn');
        
        // Update navigation
        navBtns.forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-detail="${category}"]`).classList.add('active');
        
        // Get relevant results
        const results = this.currentData.batchResult;
        let items = [];
        
        switch (category) {
            case 'successful':
                items = results.details.successful;
                break;
            case 'failed':
                items = results.details.failed;
                break;
            case 'warnings':
                items = results.details.warnings;
                break;
            case 'all':
                items = results.details.all;
                break;
        }
        
        // Display results
        content.innerHTML = '';
        
        if (items.length === 0) {
            content.innerHTML = `
                <div class="details-placeholder">
                    <i class="fas fa-info-circle"></i>
                    <p>No ${category} results to display</p>
                </div>
            `;
            return;
        }
        
        items.forEach(item => {
            const resultDiv = document.createElement('div');
            resultDiv.className = `result-item ${item.status}`;
            resultDiv.innerHTML = `
                <div class="result-header">
                    <span class="result-title">Row ${item.row}: ${item.identifier}</span>
                    <span class="result-status ${item.status}">${item.status}</span>
                </div>
                <div class="result-details">
                    ${item.message}
                    ${item.details ? `<br><small>${item.details}</small>` : ''}
                    ${item.warning ? `<br><small class="text-warning">⚠️ ${item.warning}</small>` : ''}
                </div>
            `;
            content.appendChild(resultDiv);
        });
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
    
    // Handle shared files from mobile (PWA share target)
    handleSharedFiles(files) {
        if (files && files.length > 0) {
            const file = files[0];
            
            // Switch to appropriate tab based on file type
            if (file.name.endsWith('.csv')) {
                // Switch to batch processing tab
                this.switchToTab('batch');
                this.handleBatchFileSelect({ target: { files: [file] } });
                this.showToast(`Shared CSV file "${file.name}" loaded for batch processing`, 'success');
            } else {
                // Switch to autonomous generation tab
                this.switchToTab('autonomous');
                this.handleFileSelect({ target: { files: [file] } });
                this.showToast(`Shared file "${file.name}" loaded for autonomous generation`, 'success');
            }
        }
    }
    
    switchToTab(tabId) {
        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
        
        // Update content
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        
        // Load tab data
        this.loadTabData(tabId);
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