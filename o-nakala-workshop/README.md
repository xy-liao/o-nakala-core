# NAKALA Complete Workflow Workshop

**🎯 Objective:** Interactive hands-on workshop for learning the complete NAKALA research data management workflow.

## 📋 Workshop Overview

This workshop teaches you to:
- Upload research datasets to NAKALA repository
- Create and organize thematic collections  
- Perform data curation and quality analysis
- Generate comprehensive workflow reports

**⏱️ Duration:** ~30 minutes  
**👥 Target Audience:** Researchers, data managers, digital humanities practitioners

## 🚀 Quick Start

**⚡ For immediate 5-minute start:** See the **[Quick Start Guide](../docs_organized/current/QUICK_START.md)**

### Prerequisites

1. **NAKALA Test Account**
   - Sign up at https://apitest.nakala.fr
   - Generate an API key from your profile

2. **Python Environment**
   - Python 3.8 or higher
   - Jupyter Notebook or JupyterLab
   - Required packages (see requirements.txt)

### Setup Instructions

#### Local Testing (Current)
1. **Navigate to Workshop Directory**
   ```bash
   cd o-nakala-workshop
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install NAKALA Client (Development Mode)**
   ```bash
   pip install -e ../
   ```

4. **Test Setup (Optional)**
   ```bash
   python test_local_setup.py
   ```

5. **Launch Jupyter**
   ```bash
   jupyter lab NAKALA_Complete_Workflow.ipynb
   ```

6. **Configure API Key**
   - Open the notebook
   - Replace `YOUR_API_KEY_HERE` with your API key (or use public test keys)
   - Follow the step-by-step instructions

#### Future Setup (After PyPI Publication)
```bash
pip install nakala-client[workshop]
git clone https://github.com/efeo/o-nakala-core.git
cd o-nakala-core/o-nakala-workshop
jupyter lab NAKALA_Complete_Workflow.ipynb
```

## 📁 Workshop Structure

```
o-nakala-workshop/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── NAKALA_Complete_Workflow.ipynb      # Main workshop notebook
├── config/                             # Configuration templates
├── data/                               # Workshop datasets
│   └── sample_dataset/                 # Sample research data
│       ├── folder_data_items.csv       # Upload configuration
│       ├── folder_collections.csv      # Collection configuration
│       └── files/                      # Research files by type
│           ├── images/                 # Site photographs, charts
│           ├── code/                   # Analysis scripts (R, Python)
│           ├── data/                   # Research datasets (CSV)
│           ├── documents/              # Papers, protocols
│           └── presentations/          # Meeting materials
└── outputs/                            # Generated workshop results
```

## 🎓 Learning Outcomes

By completing this workshop, you will:

1. **Master NAKALA API Operations**
   - Understand authentication and configuration
   - Use validation mode for testing
   - Handle errors and troubleshooting

2. **Organize Research Data Effectively**
   - Structure folders by content type
   - Create meaningful metadata
   - Manage multilingual descriptions

3. **Build Collections Strategically**
   - Group related datasets thematically
   - Configure collection metadata
   - Control visibility and access

4. **Perform Data Curation**
   - Assess metadata quality
   - Identify improvement opportunities
   - Generate actionable recommendations

5. **Automate Workflows**
   - Use CLI tools programmatically
   - Create repeatable processes
   - Generate comprehensive reports

## 📊 Workshop Phases

### Phase 1: Data Upload (10 minutes)
- **Validation**: Test configuration without uploading
- **Upload**: Create 5 data items with 14 research files
- **Analysis**: Review upload results and identifiers

### Phase 2: Collection Creation (5 minutes)
- **Organization**: Create 3 thematic collections
- **Assignment**: Automatically group data by content type
- **Verification**: Confirm collection structure

### Phase 3: Curation Analysis (10 minutes)
- **Quality Assessment**: Analyze metadata completeness
- **Recommendations**: Receive improvement suggestions
- **Reporting**: Generate quality scores and insights

### Phase 4: Report Generation (5 minutes)
- **Documentation**: Create comprehensive workshop report
- **Summary**: Review all accomplished tasks
- **Next Steps**: Plan future data management activities

## 🛠️ Technical Details

### NAKALA v2.0 Architecture
- **Unified CLI Tools**: Modern command-line interface
- **Configuration Management**: Environment-based settings
- **Error Handling**: Comprehensive validation and retry logic
- **Output Formats**: CSV reports and JSON analytics

### Supported Content Types
- **Images**: PNG, JPG (site photographs, charts)
- **Code**: Python, R (analysis scripts)
- **Data**: CSV (research datasets)
- **Documents**: Markdown (papers, protocols)
- **Presentations**: Markdown (meeting materials)

### API Environment
- **Test Environment**: https://apitest.nakala.fr (workshop default)
- **Production**: https://api.nakala.fr (for real deployments)

## 🔧 Troubleshooting

### Common Issues

**❌ API Key Error**
```
Solution: Verify your API key is correct and active
Check: Account status at https://apitest.nakala.fr
```

**❌ File Not Found**
```
Solution: Ensure you're in the workshop directory
Run: pwd to verify current location
```

**❌ Permission Error**
```
Solution: Check file permissions and API quotas
Verify: Account limits in NAKALA interface
```

**❌ Import Error**
```
Solution: Install missing dependencies
Run: pip install -r requirements.txt
```

### Getting Help

1. **Check Error Messages**: Read the detailed output in notebook cells
2. **Validate Configuration**: Use `--validate-only` flags for testing
3. **Review Logs**: Examine the generated output files
4. **Consult Documentation**: Visit https://documentation.nakala.fr/

## 🌟 Advanced Features

After completing the basic workshop, explore:

### Batch Operations
- Upload hundreds of files efficiently
- Bulk metadata modifications
- Automated duplicate detection

### Quality Management
- Metadata validation rules
- Content similarity analysis
- Automated enhancement suggestions

### Workflow Integration
- CI/CD pipeline integration
- Scheduled data synchronization
- API-driven research workflows

## 📚 Additional Resources

### Documentation
- **NAKALA Official Docs**: https://documentation.nakala.fr/
- **API Reference**: https://api.nakala.fr/swagger-ui/
- **User Guides**: ../docs_organized/current/user-guides/

### Example Datasets
- **Simple Dataset**: ../simple-dataset/ (basic example)
- **Sample Dataset**: data/sample_dataset/ (workshop data)
- **Large Dataset**: ../examples/ (advanced scenarios)

### Related Tools
- **Collection Management**: nakala-client-collection-v2.py
- **Upload Tools**: nakala-client-upload-v2.py  
- **Curation Suite**: nakala-curator.py

## 🎉 Workshop Completion

Upon successful completion, you'll have:

✅ **5 Data Items** uploaded to NAKALA  
✅ **3 Collections** organized thematically  
✅ **Quality Reports** with actionable insights  
✅ **Complete Documentation** of your workflow  
✅ **Practical Skills** for real research projects  

## 🚀 Next Steps After Workshop

1. **Apply to Real Data**: Use your own research datasets
2. **Enhance Metadata**: Implement curation recommendations
3. **Share Collections**: Make your work publicly available
4. **Automate Processes**: Integrate tools into research workflows
5. **Collaborate**: Share techniques with your research team

---

**📧 Questions?** Contact your workshop instructor or consult the documentation.

**🎓 Ready to start?** Open `NAKALA_Complete_Workflow.ipynb` and begin your journey!