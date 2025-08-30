# Institutional Setup Guide

This guide provides comprehensive instructions for deploying O-Nakala Core in institutional environments, supporting multi-user workflows, shared resources, and enterprise-level research data management.

## Overview

Institutional deployment of O-Nakala Core requires careful consideration of user management, resource sharing, security policies, and workflow standardization across research teams and departments.

## Pre-Deployment Planning

### Infrastructure Assessment

#### System Requirements
```bash
# Minimum server specifications
CPU: 4 cores (8+ cores recommended)
RAM: 8GB (16GB+ recommended for large datasets)
Storage: 1TB SSD (expandable for data staging)
Network: 100Mbps+ dedicated bandwidth
OS: Ubuntu 20.04 LTS or CentOS 8+ (recommended)
```

#### Network Configuration
- **Firewall Rules**: Allow HTTPS (443) outbound to NAKALA API endpoints
- **Proxy Configuration**: Configure institutional proxy if required
- **DNS Resolution**: Ensure access to `api.nakala.fr` and `apitest.nakala.fr`
- **SSL Certificates**: Configure institutional certificates if required

### User Access Planning

#### Role-Based Access Model
```
┌─────────────────┬──────────────────┬─────────────────────┐
│ Role            │ Permissions      │ NAKALA Access       │
├─────────────────┼──────────────────┼─────────────────────┤
│ Administrator   │ All operations   │ Master API key      │
│ Data Manager    │ Upload, organize │ Project API keys    │
│ Researcher      │ Upload only      │ Limited API keys    │
│ Read-Only       │ Preview, report  │ No API access       │
└─────────────────┴──────────────────┴─────────────────────┘
```

## Central Installation and Configuration

### System-Wide Installation

#### Production Environment Setup
```bash
# Create dedicated service user
sudo useradd -m -s /bin/bash nakala-service
sudo usermod -aG docker nakala-service  # If using Docker

# Install Python environment
sudo apt update
sudo apt install python3.9 python3-pip python3-venv
sudo -u nakala-service python3 -m venv /opt/nakala-core/venv

# Install O-Nakala Core with all features
sudo -u nakala-service /opt/nakala-core/venv/bin/pip install "o-nakala-core[cli,ml,dev]"

# Create global configuration directory
sudo mkdir -p /etc/nakala-core
sudo chown nakala-service:nakala-service /etc/nakala-core
```

#### Shared Configuration Management
```bash
# Global configuration file
cat > /etc/nakala-core/global.conf << EOF
[DEFAULT]
api_url = https://api.nakala.fr
timeout = 300
max_retries = 5
log_level = INFO

[INSTITUTION]
name = Your Institution Name
contact = data-manager@institution.edu
default_license = CC-BY-4.0
metadata_standards = dublin_core

[STORAGE]
staging_directory = /var/lib/nakala-core/staging
backup_directory = /var/lib/nakala-core/backups
log_directory = /var/log/nakala-core

[SECURITY]
api_key_rotation_days = 90
require_ssl = true
audit_logging = true
EOF
```

### Multi-User Environment

#### User Directory Structure
```bash
# Create standardized user structure
create_user_environment() {
    local username=$1
    local user_dir="/home/$username/nakala-workspace"
    
    sudo -u $username mkdir -p $user_dir/{projects,templates,logs,backups}
    
    # Link to shared templates and tools
    sudo -u $username ln -s /opt/nakala-core/templates $user_dir/shared-templates
    sudo -u $username ln -s /opt/nakala-core/scripts $user_dir/shared-scripts
    
    # Create user configuration
    sudo -u $username cat > $user_dir/.nakala-config << EOF
[USER]
name = $username
email = $username@institution.edu
default_project = $user_dir/projects/current

[PREFERENCES]
preview_mode = interactive
output_format = csv
backup_before_upload = true
EOF
}
```

#### API Key Management
```bash
# Centralized API key distribution
distribute_api_key() {
    local username=$1
    local api_key=$2
    local key_file="/home/$username/.nakala-api-key"
    
    echo "$api_key" | sudo -u $username tee $key_file
    sudo chmod 600 $key_file
    sudo chown $username:$username $key_file
    
    # Add to user's environment
    sudo -u $username echo "export NAKALA_API_KEY=\$(cat ~/.nakala-api-key)" >> /home/$username/.bashrc
}
```

## Workflow Standardization

### Institutional Templates

#### Standardized CSV Templates
```bash
# Create institutional metadata templates
mkdir -p /opt/nakala-core/templates/institutional

# Basic research data template
cat > /opt/nakala-core/templates/institutional/research_data.csv << EOF
file,status,type,title,alternative,creator,contributor,date,license,description,keywords,language,temporal,spatial,accessRights,identifier,rights
# Template for research data deposits at [Institution Name]
# Creator format: "Last,First" 
# Date format: YYYY-MM-DD
# License: Use institutional standard licenses
# Keywords: Use institutional controlled vocabulary
EOF

# Thesis and dissertation template
cat > /opt/nakala-core/templates/institutional/thesis.csv << EOF
file,status,type,title,alternative,creator,contributor,date,license,description,keywords,language,temporal,spatial,accessRights,identifier,rights
# Template for thesis and dissertation deposits
# Type: Use http://purl.org/coar/resource_type/c_db06 for doctoral thesis
# Include advisor in contributor field
# Use institutional thesis metadata standards
EOF
```

#### Collection Organization Standards
```bash
# Institutional collection naming convention
cat > /opt/nakala-core/templates/institutional/collections.csv << EOF
collection_name,description,keywords,rights,status
"[Department] - [Year] - [Project Name]","Description following institutional standards","departmental;keywords;here","CC-BY-4.0",pending
# Examples:
# "History - 2024 - Medieval Manuscripts","Digital collection of medieval manuscript analysis","history;medieval;manuscripts;paleography","CC-BY-4.0",pending
# "Biology - 2024 - Species Documentation","Research data supporting species classification study","biology;taxonomy;species;classification","CC0-1.0",pending
EOF
```

### Automated Workflow Scripts

#### Institutional Upload Script
```bash
#!/bin/bash
# institutional_upload.sh - Standardized institutional upload process

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="/etc/nakala-core/global.conf"
LOG_DIR="/var/log/nakala-core"

# Source institutional configuration
source $CONFIG_FILE

usage() {
    echo "Usage: $0 -p PROJECT_DIR -u USERNAME [-t] [-v]"
    echo "  -p PROJECT_DIR  Path to project directory"
    echo "  -u USERNAME     Institutional username"  
    echo "  -t              Use test environment"
    echo "  -v              Verbose output"
    exit 1
}

# Parse command line arguments
while getopts "p:u:tv" opt; do
    case $opt in
        p) PROJECT_DIR="$OPTARG" ;;
        u) USERNAME="$OPTARG" ;;
        t) USE_TEST=true ;;
        v) VERBOSE=true ;;
        *) usage ;;
    esac
done

# Validate required parameters
[[ -z "$PROJECT_DIR" || -z "$USERNAME" ]] && usage

# Set environment
if [[ "$USE_TEST" == true ]]; then
    export NAKALA_API_URL="https://apitest.nakala.fr"
else
    export NAKALA_API_URL="https://api.nakala.fr"
fi

# Load user API key
export NAKALA_API_KEY=$(sudo -u $USERNAME cat /home/$USERNAME/.nakala-api-key)

# Create timestamped log
LOG_FILE="$LOG_DIR/upload_${USERNAME}_$(date +%Y%m%d_%H%M%S).log"
exec 1> >(tee -a "$LOG_FILE")
exec 2>&1

echo "=== Institutional O-Nakala Upload ==="
echo "User: $USERNAME"
echo "Project: $PROJECT_DIR"
echo "Environment: $NAKALA_API_URL"
echo "Timestamp: $(date)"
echo "========================================"

# Stage 1: Pre-upload validation
echo "Stage 1: Pre-upload validation"
cd "$PROJECT_DIR"

if [[ ! -f "folder_data_items.csv" ]]; then
    echo "ERROR: Missing folder_data_items.csv"
    exit 1
fi

# Validate using preview tool
echo "Validating metadata and files..."
o-nakala-preview --csv folder_data_items.csv --validate-only

# Stage 2: Upload execution
echo "Stage 2: Upload execution"
UPLOAD_OUTPUT="upload_results_$(date +%Y%m%d_%H%M%S).csv"

o-nakala-upload \
    --dataset folder_data_items.csv \
    --mode folder \
    --base-path . \
    --output "$UPLOAD_OUTPUT" \
    --timeout 300 \
    --max-retries 3 \
    ${VERBOSE:+--verbose}

# Stage 3: Collection creation (if configured)
if [[ -f "folder_collections.csv" ]]; then
    echo "Stage 3: Collection creation"
    o-nakala-collection \
        --from-upload-output "$UPLOAD_OUTPUT" \
        --from-folder-collections folder_collections.csv
fi

# Stage 4: Quality report
echo "Stage 4: Quality assurance"
QA_OUTPUT="quality_report_$(date +%Y%m%d_%H%M%S).csv"
o-nakala-curator \
    --quality-report \
    --scope recent \
    --output "$QA_OUTPUT"

# Stage 5: Summary report
echo "Stage 5: Upload summary"
SUCCESS_COUNT=$(grep -c "success" "$UPLOAD_OUTPUT" || echo "0")
TOTAL_COUNT=$(tail -n +2 folder_data_items.csv | wc -l)
echo "Upload completed: $SUCCESS_COUNT/$TOTAL_COUNT files successful"

# Archive results
ARCHIVE_DIR="nakala_archives/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$ARCHIVE_DIR"
cp "$UPLOAD_OUTPUT" "$QA_OUTPUT" "$LOG_FILE" "$ARCHIVE_DIR/"

echo "Results archived to: $ARCHIVE_DIR"
echo "Upload process completed successfully"
```

## Security and Compliance

### Access Control Implementation

#### LDAP/AD Integration
```python
# ldap_auth.py - LDAP integration for institutional authentication
import ldap
from functools import wraps

def authenticate_user(username, password):
    """Authenticate user against institutional LDAP"""
    ldap_server = "ldap://directory.institution.edu"
    base_dn = "ou=People,dc=institution,dc=edu"
    
    try:
        conn = ldap.initialize(ldap_server)
        user_dn = f"uid={username},{base_dn}"
        conn.simple_bind_s(user_dn, password)
        return True
    except ldap.INVALID_CREDENTIALS:
        return False
    except Exception as e:
        logger.error(f"LDAP authentication error: {e}")
        return False

def require_institutional_auth(f):
    """Decorator for functions requiring institutional authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Implementation depends on your web framework
        # This is a conceptual example
        pass
    return decorated_function
```

#### Audit Logging
```bash
# Setup audit logging
mkdir -p /var/log/nakala-core/audit
chown nakala-service:nakala-service /var/log/nakala-core/audit
chmod 750 /var/log/nakala-core/audit

# Audit log rotation
cat > /etc/logrotate.d/nakala-core << EOF
/var/log/nakala-core/*.log {
    daily
    missingok
    rotate 90
    compress
    delaycompress
    copytruncate
    create 644 nakala-service nakala-service
}
EOF
```

### Data Governance

#### Retention and Backup Policies
```bash
#!/bin/bash
# backup_policy.sh - Institutional backup management

BACKUP_BASE="/var/lib/nakala-core/backups"
RETENTION_DAYS=365

# Daily backup of user projects
daily_backup() {
    for user_home in /home/*/nakala-workspace; do
        username=$(basename $(dirname $user_home))
        backup_dir="$BACKUP_BASE/daily/$username/$(date +%Y%m%d)"
        
        mkdir -p "$backup_dir"
        rsync -av --exclude='*.tmp' --exclude='.cache' "$user_home/" "$backup_dir/"
    done
}

# Cleanup old backups
cleanup_backups() {
    find "$BACKUP_BASE/daily" -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \;
}

# Archive completed projects
archive_projects() {
    local archive_dir="$BACKUP_BASE/archived/$(date +%Y)"
    mkdir -p "$archive_dir"
    
    # Move completed projects to archive
    find /home/*/nakala-workspace/projects -name "*.completed" -exec mv {} "$archive_dir/" \;
}

# Execute backup procedures
daily_backup
cleanup_backups
archive_projects
```

## Monitoring and Maintenance

### System Monitoring

#### Health Check Dashboard
```python
# health_dashboard.py - System health monitoring
import subprocess
import json
from datetime import datetime, timedelta

def check_system_health():
    """Comprehensive system health check"""
    health_status = {
        'timestamp': datetime.now().isoformat(),
        'status': 'healthy',
        'checks': {}
    }
    
    # Check disk space
    disk_result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
    disk_usage = disk_result.stdout.split('\n')[1].split()[4].rstrip('%')
    health_status['checks']['disk_usage'] = {
        'status': 'warning' if int(disk_usage) > 80 else 'ok',
        'value': f"{disk_usage}%"
    }
    
    # Check API connectivity
    api_result = subprocess.run([
        'curl', '-f', '-H', f'X-API-KEY: {test_api_key}',
        'https://apitest.nakala.fr/users/me'
    ], capture_output=True, text=True)
    health_status['checks']['api_connectivity'] = {
        'status': 'ok' if api_result.returncode == 0 else 'error',
        'response_time': 'measured in actual implementation'
    }
    
    # Check recent uploads
    log_result = subprocess.run([
        'grep', '-c', 'success', '/var/log/nakala-core/upload_*.log'
    ], capture_output=True, text=True)
    success_count = log_result.stdout.strip() if log_result.returncode == 0 else '0'
    health_status['checks']['recent_uploads'] = {
        'status': 'ok',
        'successful_uploads_24h': success_count
    }
    
    return health_status

def generate_health_report():
    """Generate daily health report"""
    health = check_system_health()
    
    with open(f"/var/log/nakala-core/health_{datetime.now().strftime('%Y%m%d')}.json", 'w') as f:
        json.dump(health, f, indent=2)
    
    # Send alerts if needed
    if health['status'] != 'healthy':
        send_alert(health)

def send_alert(health_status):
    """Send alert to administrators"""
    # Implementation depends on institutional alerting system
    pass
```

#### Performance Monitoring
```bash
# performance_monitor.sh - Track system performance
#!/bin/bash

METRICS_FILE="/var/log/nakala-core/performance_$(date +%Y%m%d).csv"

# Initialize metrics file if it doesn't exist
if [[ ! -f "$METRICS_FILE" ]]; then
    echo "timestamp,cpu_usage,memory_usage,disk_io,network_io,active_uploads" > "$METRICS_FILE"
fi

# Collect metrics
timestamp=$(date +%Y-%m-%d_%H:%M:%S)
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
memory_usage=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')
disk_io=$(iostat -d 1 1 | tail -n +4 | awk '{sum+=$4} END {print sum}')
network_io=$(cat /proc/net/dev | grep eth0 | awk '{print $10}')  # Adjust interface name
active_uploads=$(pgrep -f "o-nakala-upload" | wc -l)

# Log metrics
echo "$timestamp,$cpu_usage,$memory_usage,$disk_io,$network_io,$active_uploads" >> "$METRICS_FILE"

# Generate weekly performance report
if [[ $(date +%u) -eq 1 ]]; then  # Monday
    python3 /opt/nakala-core/scripts/generate_performance_report.py
fi
```

## User Training and Documentation

### Training Program Structure

#### Level 1: Basic User Training (2 hours)
- NAKALA platform introduction
- O-Nakala Core installation and setup
- Basic upload workflows
- Metadata best practices
- Troubleshooting common issues

#### Level 2: Advanced User Training (4 hours)  
- Complex workflow design
- Collection organization strategies
- Quality assurance procedures
- Batch processing techniques
- Integration with research workflows

#### Level 3: Administrator Training (8 hours)
- System installation and configuration
- Multi-user environment management
- Security and compliance procedures
- Monitoring and maintenance
- Troubleshooting and support

### Self-Service Resources

#### Institutional Documentation Portal
```bash
# Create documentation website
mkdir -p /var/www/nakala-docs
cd /var/www/nakala-docs

# Copy and customize documentation
cp -r /opt/nakala-core/docs/* ./
sed -i 's/your-institution.edu/'"$(hostname -d)"'/g' ./*.md

# Setup web server (nginx example)
cat > /etc/nginx/sites-available/nakala-docs << EOF
server {
    listen 80;
    server_name nakala-docs.institution.edu;
    root /var/www/nakala-docs;
    index index.html README.md;
    
    location ~ \.md$ {
        add_header Content-Type text/plain;
    }
}
EOF
```

## Scaling and Growth Management

### Capacity Planning

#### User Growth Projection
```python
# capacity_planning.py - Predict resource needs
def calculate_resource_needs(current_users, growth_rate, file_size_avg, files_per_user):
    """Calculate infrastructure needs for user growth"""
    projected_users = {
        '6_months': current_users * (1 + growth_rate * 0.5),
        '1_year': current_users * (1 + growth_rate),
        '2_years': current_users * (1 + growth_rate) ** 2
    }
    
    storage_needs = {}
    bandwidth_needs = {}
    
    for period, users in projected_users.items():
        total_files = users * files_per_user
        storage_gb = (total_files * file_size_avg) / (1024**3)
        monthly_bandwidth_gb = (total_files * file_size_avg * 1.5) / (1024**3)  # 1.5x for transfers
        
        storage_needs[period] = storage_gb
        bandwidth_needs[period] = monthly_bandwidth_gb
    
    return {
        'users': projected_users,
        'storage_gb': storage_needs,
        'bandwidth_gb': bandwidth_needs
    }

# Example usage
current_capacity = calculate_resource_needs(
    current_users=50,
    growth_rate=0.3,  # 30% annual growth
    file_size_avg=10 * 1024 * 1024,  # 10MB average file
    files_per_user=100
)

print(json.dumps(current_capacity, indent=2))
```

### Institutional Integration

#### Research Information Systems Integration
```python
# ris_integration.py - Research Information System integration
class RISIntegrator:
    """Integrate O-Nakala Core with institutional research systems"""
    
    def __init__(self, ris_api_url, nakala_config):
        self.ris_api = ris_api_url
        self.nakala_config = nakala_config
    
    def sync_project_metadata(self, project_id):
        """Sync project metadata from RIS to NAKALA"""
        # Fetch project details from RIS
        project_data = self.fetch_ris_project(project_id)
        
        # Transform to NAKALA metadata format
        nakala_metadata = self.transform_metadata(project_data)
        
        # Create or update NAKALA collection
        return self.update_nakala_collection(nakala_metadata)
    
    def fetch_ris_project(self, project_id):
        """Fetch project data from research information system"""
        # Implementation specific to institutional RIS
        pass
    
    def transform_metadata(self, project_data):
        """Transform RIS metadata to NAKALA format"""
        return {
            'title': project_data.get('title'),
            'creators': [f"{p['last_name']},{p['first_name']}" for p in project_data.get('investigators', [])],
            'description': project_data.get('abstract'),
            'keywords': ';'.join(project_data.get('keywords', [])),
            'funding': project_data.get('funding_source'),
            'institutional_id': project_data.get('project_id')
        }
```

This comprehensive institutional setup guide provides the foundation for deploying O-Nakala Core in enterprise environments, supporting multiple users, maintaining security standards, and scaling with institutional growth.