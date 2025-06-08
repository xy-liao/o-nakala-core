# O-Nakala Core Web Interface

Modern web dashboard for AI-driven metadata management with NAKALA repositories.

## 🎯 Features

### 📊 Interactive Dashboard
- **Real-time Analytics**: Live health scores, quality metrics, and AI predictions
- **Activity Monitoring**: Recent AI activities and system status
- **Intelligence Overview**: AI feature status and capabilities

### 🤖 Autonomous Generation
- **Drag & Drop Upload**: Support for all file types (CSV, JSON, PDF, images, code)
- **AI Content Analysis**: Automatic content type and language detection
- **Complete Metadata Generation**: 6+ metadata fields generated automatically
- **Quality Metrics**: Confidence scores, completeness rates, and recommendations
- **Export Options**: CSV export and detailed reports

### 📋 Intelligent Templates
- **Context-Aware Generation**: Templates based on resource type and user context
- **Field Intelligence**: Pre-populated fields with AI suggestions
- **Visual Preview**: Field details, requirements, and help text
- **Documentation**: Built-in template documentation and examples

### 📈 Predictive Analytics
- **Interactive Charts**: Quality trends, completeness predictions, usage analytics
- **Health Monitoring**: Repository health gauge with color-coded indicators
- **Forecasting**: 1-month to 1-year predictions with confidence intervals
- **Strategic Insights**: AI-driven recommendations and capacity planning

### 🔄 Batch Processing
- **CSV Management**: Upload and process modification CSVs
- **Dry Run Mode**: Preview changes before applying
- **Processing Summary**: Success/failure counts with detailed results
- **Visual Feedback**: Progress tracking and error reporting

## 🚀 Quick Start

### 1. Start the API Server

```bash
# Option 1: Using the launcher script
python start_web_server.py --port 8000

# Option 2: Direct FastAPI launch
cd src
python -m nakala_client.web_api --port 8000

# Option 3: Using uvicorn directly
uvicorn nakala_client.web_api:create_web_api --host 0.0.0.0 --port 8000
```

### 2. Open the Web Interface

Open `web/index.html` in your browser or serve it with a local server:

```bash
# Using Python's built-in server
cd web
python -m http.server 3000

# Using Node.js serve
npx serve .

# Using PHP
php -S localhost:3000
```

### 3. Connect to NAKALA

1. Enter your NAKALA API key in the connection form
2. Click "Connect" to authenticate
3. Start using the AI-driven features!

## 🔧 Configuration

### API Settings

The web interface connects to the O-Nakala Core API server by default at:
- **API URL**: `http://localhost:8000/api/v1`
- **Documentation**: `http://localhost:8000/docs`

To change the API URL, modify the `apiUrl` in `app.js`:

```javascript
this.apiUrl = 'http://your-server:8000/api/v1';
```

### NAKALA Environment

By default, the interface connects to the NAKALA test environment:
- **Test API**: `https://apitest.nakala.fr`
- **Production API**: `https://api.nakala.fr`

## 📱 Interface Sections

### Dashboard Tab
- **System Status**: Health, quality, and completeness scores
- **AI Features**: Current capabilities and status
- **Recent Activity**: Real-time AI activity feed

### Autonomous Generation Tab
- **File Upload**: Drag-and-drop or click to upload
- **Resource Type**: Dataset, document, image, code, collection
- **Results Display**: Generated metadata with confidence scores
- **Export Options**: CSV download and text reports

### Templates Tab
- **Generator Form**: Resource type and template options
- **Template Preview**: Field details and requirements
- **Export Functions**: CSV templates and documentation

### Analytics Tab
- **Configuration**: Timeframes and analysis types
- **Interactive Charts**: Quality trends and predictions
- **Insights**: Key findings and strategic recommendations

### Batch Processing Tab
- **CSV Upload**: Modification files for batch operations
- **Processing Options**: Dry run mode for testing
- **Results Summary**: Success/failure statistics

## 🎨 Customization

### Styling

The interface uses CSS variables for easy theming in `styles.css`:

```css
:root {
    --primary-color: #2563eb;
    --success-color: #059669;
    --warning-color: #d97706;
    --error-color: #dc2626;
    /* ... more variables */
}
```

### Charts

Charts are powered by Chart.js v4.4.0 with customizable themes and interactions. Modify chart configurations in `app.js`:

```javascript
createQualityChart(data) {
    // Customize chart type, colors, and options
}
```

### Features

Enable/disable features by modifying the `init()` method in `app.js`:

```javascript
init() {
    this.setupEventListeners();
    this.setupTabNavigation();
    this.setupDragAndDrop();
    // this.startDashboardUpdates(); // Disable real-time updates
}
```

## 🔍 Development

### File Structure

```
web/
├── index.html          # Main HTML structure
├── styles.css          # Complete styling system
├── app.js              # JavaScript application logic
├── README.md           # This documentation
└── assets/             # Images and other assets (future)
```

### Key Components

- **NakalaWebApp**: Main application class
- **Chart Integration**: Interactive analytics visualizations
- **Real-time Updates**: Dashboard data refresh system
- **File Handling**: Drag-and-drop and upload management
- **API Communication**: RESTful API integration

### Browser Support

- **Modern Browsers**: Chrome 60+, Firefox 60+, Safari 12+, Edge 79+
- **JavaScript**: ES6+ features (classes, async/await, fetch)
- **CSS**: Flexbox, Grid, CSS Variables
- **APIs**: FileReader, Blob, URL.createObjectURL

## 🐛 Troubleshooting

### Common Issues

**API Connection Failed**
- Ensure the API server is running on port 8000
- Check firewall settings and network connectivity
- Verify the API URL in `app.js`

**Charts Not Loading**
- Ensure Chart.js CDN is accessible
- Check browser console for JavaScript errors
- Verify canvas elements exist in HTML

**File Upload Issues**
- Check file size limits (default: no limit in web interface)
- Ensure proper file types are selected
- Verify API server has write permissions for temp files

**Authentication Problems**
- Use valid NAKALA API keys
- Test API key with direct NAKALA API calls
- Check API key format and permissions

### Debug Mode

Enable debug logging by modifying `app.js`:

```javascript
// Enable detailed console logging
const DEBUG = true;

if (DEBUG) {
    console.log('Debug info:', data);
}
```

## 🔐 Security Notes

### API Keys
- API keys are stored only in browser memory
- Keys are transmitted via HTTPS to the API server
- Never commit API keys to version control

### CORS Configuration
- Development: Allows all origins (`*`)
- Production: Configure specific allowed origins

### File Upload Security
- Files are processed server-side with validation
- Temporary files are automatically cleaned up
- No file execution on the server

## 📊 Performance

### Optimization Features
- **Lazy Loading**: Charts created only when needed
- **Resource Cleanup**: Chart instances destroyed when switching tabs
- **Efficient DOM Updates**: Minimal DOM manipulation
- **Caching**: API responses cached where appropriate

### Metrics
- **Initial Load**: <2 seconds on modern browsers
- **Chart Rendering**: <500ms for typical datasets
- **Real-time Updates**: 30-second intervals (configurable)
- **Memory Usage**: <50MB typical browser footprint

## 🚀 Future Enhancements

- **Mobile Responsive Design**: Optimized mobile interface
- **Offline Mode**: Service worker for offline functionality
- **Advanced Visualizations**: 3D charts and network diagrams
- **Collaborative Features**: Multi-user real-time collaboration
- **Plugin System**: Custom widget development
- **Export Formats**: PDF, Excel, and custom formats

---

**Built with**: HTML5, CSS3, JavaScript ES6+, Chart.js, FastAPI
**Compatible with**: O-Nakala Core v4.0+ API
**License**: Same as O-Nakala Core project