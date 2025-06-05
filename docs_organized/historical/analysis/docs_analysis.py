#!/usr/bin/env python3
"""
Documentation Analysis and Categorization Script

Analyzes all markdown files and categorizes them by type, purpose, and timeline.
"""

import os
import re
from datetime import datetime
from pathlib import Path

def analyze_doc_content(file_path):
    """Analyze document content to determine its category and purpose."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract first few lines for analysis
        lines = content.split('\n')[:10]
        first_content = '\n'.join(lines).lower()
        
        # Determine category based on content, filename, and path
        filename = os.path.basename(file_path).lower()
        filepath = str(file_path).lower()
        
        # Timeline indicators
        timeline = "unknown"
        if any(indicator in first_content for indicator in ['v2', 'version 2', '2.0', 'complete', 'final']):
            timeline = "current"
        elif any(indicator in first_content for indicator in ['v1', 'version 1', '1.0', 'legacy', 'old']):
            timeline = "legacy"
        elif any(indicator in first_content for indicator in ['draft', 'plan', 'proposal', 'todo']):
            timeline = "planning"
        elif any(indicator in first_content for indicator in ['analysis', 'review', 'assessment']):
            timeline = "analysis"
        elif 'claude.md' in filename or 'readme' in filename:
            timeline = "current"
        
        # Type categorization
        doc_type = "unknown"
        audience = "unknown"
        
        # User documentation
        if any(keyword in filepath for keyword in ['user-guide', 'guide', 'tutorial', 'faq', 'troubleshooting']):
            doc_type = "user_guide"
            audience = "users"
        elif any(keyword in first_content for keyword in ['user', 'how to', 'tutorial', 'guide']):
            doc_type = "user_guide" 
            audience = "users"
            
        # Developer documentation
        elif any(keyword in filepath for keyword in ['implementation', 'architecture', 'api', 'development']):
            doc_type = "developer_doc"
            audience = "developers"
        elif any(keyword in first_content for keyword in ['implementation', 'architecture', 'api', 'development', 'code']):
            doc_type = "developer_doc"
            audience = "developers"
            
        # Analysis/Research documentation
        elif any(keyword in filepath for keyword in ['analysis', 'review', 'assessment', 'comparison']):
            doc_type = "analysis"
            audience = "developers"
        elif any(keyword in first_content for keyword in ['analysis', 'review', 'assessment', 'comparison']):
            doc_type = "analysis"
            audience = "developers"
            
        # Planning documentation
        elif any(keyword in filepath for keyword in ['plan', 'timeline', 'roadmap']):
            doc_type = "planning"
            audience = "developers"
        elif any(keyword in first_content for keyword in ['plan', 'timeline', 'roadmap', 'todo']):
            doc_type = "planning"
            audience = "developers"
            
        # Reference documentation
        elif any(keyword in filepath for keyword in ['api', 'reference', 'spec']):
            doc_type = "reference"
            audience = "developers"
            
        # Project status/reports
        elif any(keyword in filename for keyword in ['status', 'report', 'results', 'completion']):
            doc_type = "project_report"
            audience = "stakeholders"
        elif any(keyword in first_content for keyword in ['status', 'report', 'results', 'summary', 'completion']):
            doc_type = "project_report"
            audience = "stakeholders"
            
        # Examples/samples
        elif 'sample' in filepath or 'example' in filepath:
            doc_type = "example"
            audience = "users"
            
        # Auto-generated docs
        elif 'nakala-python-client' in filepath:
            doc_type = "auto_generated"
            audience = "developers"
            
        # Main project docs
        elif filename in ['claude.md', 'readme.md']:
            doc_type = "main_doc"
            audience = "all"
            
        # Estimate importance
        importance = "medium"
        if filename in ['claude.md', 'readme.md'] or 'completion' in filename or 'status' in filename:
            importance = "high"
        elif doc_type in ['user_guide', 'main_doc']:
            importance = "high"
        elif timeline == "current" and doc_type in ['developer_doc', 'project_report']:
            importance = "high"
        elif timeline == "legacy" or doc_type == "auto_generated":
            importance = "low"
        elif doc_type in ['analysis', 'planning'] and timeline != "current":
            importance = "low"
            
        return {
            'path': file_path,
            'filename': filename,
            'type': doc_type,
            'audience': audience,
            'timeline': timeline,
            'importance': importance,
            'size_lines': len(content.split('\n')),
            'size_chars': len(content)
        }
        
    except Exception as e:
        return {
            'path': file_path,
            'filename': os.path.basename(file_path),
            'type': 'error',
            'audience': 'unknown',
            'timeline': 'unknown',
            'importance': 'low',
            'error': str(e),
            'size_lines': 0,
            'size_chars': 0
        }

def main():
    """Analyze all markdown documentation."""
    print("📚 Analyzing Documentation Structure...")
    print("=" * 60)
    
    # Find all markdown files
    md_files = []
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        if any(skip in root for skip in ['venv', '.git', '__pycache__', '.pytest_cache']):
            continue
            
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    # Analyze each file
    analyzed_docs = []
    for md_file in md_files:
        analysis = analyze_doc_content(md_file)
        analyzed_docs.append(analysis)
    
    # Categorize and display results
    categories = {}
    for doc in analyzed_docs:
        key = f"{doc['type']}_{doc['timeline']}"
        if key not in categories:
            categories[key] = []
        categories[key].append(doc)
    
    # Display analysis
    print("\n📊 Documentation Analysis Results:")
    print("-" * 40)
    
    total_docs = len(analyzed_docs)
    print(f"Total markdown files found: {total_docs}")
    
    # Group by type and timeline
    type_counts = {}
    timeline_counts = {}
    importance_counts = {}
    
    for doc in analyzed_docs:
        # Count by type
        doc_type = doc['type']
        if doc_type not in type_counts:
            type_counts[doc_type] = 0
        type_counts[doc_type] += 1
        
        # Count by timeline
        timeline = doc['timeline']
        if timeline not in timeline_counts:
            timeline_counts[timeline] = 0
        timeline_counts[timeline] += 1
        
        # Count by importance
        importance = doc['importance']
        if importance not in importance_counts:
            importance_counts[importance] = 0
        importance_counts[importance] += 1
    
    print(f"\nBy Type:")
    for doc_type, count in sorted(type_counts.items()):
        print(f"  {doc_type}: {count}")
    
    print(f"\nBy Timeline:")
    for timeline, count in sorted(timeline_counts.items()):
        print(f"  {timeline}: {count}")
    
    print(f"\nBy Importance:")
    for importance, count in sorted(importance_counts.items()):
        print(f"  {importance}: {count}")
    
    # Recommendations for organization
    print(f"\n🗂️  Organizational Recommendations:")
    print("-" * 40)
    
    # High importance current docs
    current_important = [doc for doc in analyzed_docs 
                        if doc['importance'] == 'high' and doc['timeline'] == 'current']
    
    print(f"📌 Keep in main docs/ (High importance, current): {len(current_important)}")
    for doc in current_important[:5]:  # Show first 5
        print(f"   • {doc['filename']} ({doc['type']})")
    
    # User guides
    user_guides = [doc for doc in analyzed_docs if doc['type'] == 'user_guide']
    print(f"\n👥 User documentation: {len(user_guides)}")
    
    # Developer docs
    dev_docs = [doc for doc in analyzed_docs if doc['audience'] == 'developers' and doc['timeline'] == 'current']
    print(f"\n👨‍💻 Developer documentation (current): {len(dev_docs)}")
    
    # Archive candidates
    archive_candidates = [doc for doc in analyzed_docs 
                         if doc['importance'] == 'low' or doc['timeline'] in ['legacy', 'planning']]
    print(f"\n📦 Archive candidates (low importance/legacy): {len(archive_candidates)}")
    
    # Auto-generated docs
    auto_gen = [doc for doc in analyzed_docs if doc['type'] == 'auto_generated']
    print(f"\n🤖 Auto-generated docs (keep separate): {len(auto_gen)}")
    
    # Generate reorganization plan
    print(f"\n📋 Reorganization Plan:")
    print("-" * 40)
    
    reorganization = {
        'keep_main': [doc for doc in analyzed_docs if doc['importance'] == 'high' and doc['timeline'] == 'current' and doc['type'] in ['main_doc', 'project_report']],
        'move_to_users': [doc for doc in analyzed_docs if doc['type'] == 'user_guide'],
        'move_to_dev': [doc for doc in analyzed_docs if doc['audience'] == 'developers' and doc['timeline'] == 'current' and doc['type'] in ['developer_doc', 'reference']],
        'archive_historical': [doc for doc in analyzed_docs if doc['timeline'] in ['analysis', 'planning'] and doc['importance'] != 'high'],
        'archive_legacy': [doc for doc in analyzed_docs if doc['timeline'] == 'legacy' or doc['importance'] == 'low'],
        'keep_auto_generated': [doc for doc in analyzed_docs if doc['type'] == 'auto_generated'],
        'examples': [doc for doc in analyzed_docs if doc['type'] == 'example']
    }
    
    for category, docs in reorganization.items():
        if docs:
            print(f"\n{category.replace('_', ' ').title()}: {len(docs)} files")
            for doc in docs[:3]:  # Show first 3 examples
                rel_path = doc['path'].replace('./', '')
                print(f"   • {rel_path}")
            if len(docs) > 3:
                print(f"   ... and {len(docs) - 3} more")
    
    # Save analysis results
    import json
    with open('documentation_analysis.json', 'w') as f:
        json.dump({
            'analysis_date': datetime.now().isoformat(),
            'total_files': total_docs,
            'categorization': type_counts,
            'timeline_distribution': timeline_counts,
            'importance_distribution': importance_counts,
            'reorganization_plan': {k: [doc['path'] for doc in v] for k, v in reorganization.items()},
            'detailed_analysis': analyzed_docs
        }, f, indent=2, default=str)
    
    print(f"\n💾 Detailed analysis saved to: documentation_analysis.json")

if __name__ == '__main__':
    main()