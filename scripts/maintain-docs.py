#!/usr/bin/env python3
"""
maintain-docs.py - Automated documentation maintenance tool

This script performs regular maintenance tasks for O-Nakala Core documentation:
- Updates cross-references when files move
- Validates navigation consistency
- Generates documentation metrics
- Identifies content gaps and opportunities
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple

class DocumentationMaintainer:
    """Automated documentation maintenance and quality assurance"""
    
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        self.md_files = list(self.root.rglob("*.md"))
        # Exclude generated and archived files
        self.md_files = [f for f in self.md_files 
                        if not any(part in str(f) for part in ['.git', 'node_modules', 'archived'])]
        
    def extract_links(self, file_path: Path) -> List[Tuple[str, str]]:
        """Extract all markdown links from a file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern matches [text](link)
        pattern = r'\[([^\]]*)\]\(([^)]*)\)'
        return re.findall(pattern, content)
    
    def build_link_graph(self) -> Dict[str, List[Dict]]:
        """Build a graph of all documentation links"""
        link_graph = {}
        
        for file_path in self.md_files:
            relative_path = str(file_path.relative_to(self.root))
            links = self.extract_links(file_path)
            
            # Filter internal links only
            internal_links = []
            for text, link in links:
                if not link.startswith(('http://', 'https://', 'mailto:')):
                    internal_links.append({
                        'text': text,
                        'target': link,
                        'resolved': self.resolve_link_path(file_path, link)
                    })
            
            link_graph[relative_path] = internal_links
        
        return link_graph
    
    def resolve_link_path(self, source_file: Path, link: str) -> Path:
        """Resolve a relative link to absolute path"""
        # Remove anchor
        file_part = link.split('#')[0]
        if not file_part:
            return source_file
            
        if file_part.startswith('/'):
            # Root relative
            return self.root / file_part.lstrip('/')
        else:
            # Relative to source file
            return (source_file.parent / file_part).resolve()
    
    def validate_links(self) -> Dict[str, List[str]]:
        """Validate all internal links and return broken ones"""
        broken_links = {}
        link_graph = self.build_link_graph()
        
        for file_path, links in link_graph.items():
            file_broken_links = []
            
            for link in links:
                resolved_path = link['resolved']
                if resolved_path.suffix == '.md' and not resolved_path.exists():
                    file_broken_links.append(f"{link['text']} -> {link['target']}")
            
            if file_broken_links:
                broken_links[file_path] = file_broken_links
        
        return broken_links
    
    def analyze_navigation_consistency(self) -> Dict[str, any]:
        """Analyze navigation structure consistency"""
        analysis = {
            'files_with_breadcrumbs': 0,
            'files_without_breadcrumbs': [],
            'start_here_references': 0,
            'navigation_patterns': {}
        }
        
        key_files = [
            'START_HERE.md',
            'docs/GETTING_STARTED.md', 
            'docs/API_REFERENCE.md',
            'docs/CSV_FORMAT_GUIDE.md'
        ]
        
        for file_path in self.md_files:
            relative_path = str(file_path.relative_to(self.root))
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for navigation breadcrumbs
            has_breadcrumbs = ('📍 You are here:' in content or 
                             'START_HERE' in content or
                             '⬅️ Previous Steps' in content)
            
            if relative_path in key_files:
                if has_breadcrumbs:
                    analysis['files_with_breadcrumbs'] += 1
                else:
                    analysis['files_without_breadcrumbs'].append(relative_path)
            
            # Count START_HERE references
            if 'START_HERE.md' in content:
                analysis['start_here_references'] += 1
            
            # Analyze navigation patterns
            nav_patterns = re.findall(r'(⬅️|➡️|🔍|🆘).*?\n', content)
            if nav_patterns:
                analysis['navigation_patterns'][relative_path] = len(nav_patterns)
        
        return analysis
    
    def generate_metrics(self) -> Dict[str, any]:
        """Generate comprehensive documentation metrics"""
        metrics = {
            'total_files': len(self.md_files),
            'total_words': 0,
            'total_lines': 0,
            'file_sizes': {},
            'heading_structure': {},
            'link_density': {},
            'last_updated': datetime.now().isoformat()
        }
        
        for file_path in self.md_files:
            relative_path = str(file_path.relative_to(self.root))
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Basic metrics
            word_count = len(content.split())
            line_count = len(lines)
            
            metrics['total_words'] += word_count
            metrics['total_lines'] += line_count
            metrics['file_sizes'][relative_path] = {
                'words': word_count,
                'lines': line_count
            }
            
            # Analyze heading structure
            headings = [line for line in lines if line.startswith('#')]
            metrics['heading_structure'][relative_path] = len(headings)
            
            # Calculate link density
            links = self.extract_links(file_path)
            link_density = len(links) / max(word_count, 1) * 100
            metrics['link_density'][relative_path] = round(link_density, 2)
        
        return metrics
    
    def identify_orphaned_files(self) -> List[str]:
        """Identify files that aren't linked from anywhere"""
        link_graph = self.build_link_graph()
        
        # Get all linked files
        linked_files = set()
        for links in link_graph.values():
            for link in links:
                if link['resolved'].suffix == '.md':
                    try:
                        linked_path = str(link['resolved'].relative_to(self.root))
                        linked_files.add(linked_path)
                    except ValueError:
                        # Path is outside root directory
                        pass
        
        # Find orphaned files
        all_files = {str(f.relative_to(self.root)) for f in self.md_files}
        
        # Exclude certain files that are naturally not linked
        exclude_patterns = [
            'README.md',  # Main entry point
            'START_HERE.md',  # Main navigation
            'CLAUDE.md',  # Development notes
            'examples/sample_dataset/files/',  # Sample data
            'archived/',  # Archived content
        ]
        
        orphaned = []
        for file_path in all_files:
            if file_path not in linked_files:
                if not any(pattern in file_path for pattern in exclude_patterns):
                    orphaned.append(file_path)
        
        return orphaned
    
    def suggest_improvements(self) -> Dict[str, List[str]]:
        """Suggest documentation improvements"""
        suggestions = {
            'structure': [],
            'content': [],
            'navigation': [],
            'maintenance': []
        }
        
        metrics = self.generate_metrics()
        broken_links = self.validate_links()
        orphaned = self.identify_orphaned_files()
        nav_analysis = self.analyze_navigation_consistency()
        
        # Structure suggestions
        large_files = [f for f, stats in metrics['file_sizes'].items() 
                      if stats['lines'] > 1000]
        if large_files:
            suggestions['structure'].append(f"Consider splitting large files: {', '.join(large_files[:3])}")
        
        # Content suggestions
        low_density_files = [f for f, density in metrics['link_density'].items() 
                           if density < 1.0 and metrics['file_sizes'][f]['words'] > 200]
        if low_density_files:
            suggestions['content'].append(f"Add more cross-references to: {', '.join(low_density_files[:3])}")
        
        # Navigation suggestions
        if nav_analysis['files_without_breadcrumbs']:
            suggestions['navigation'].append(f"Add breadcrumbs to: {', '.join(nav_analysis['files_without_breadcrumbs'])}")
        
        # Maintenance suggestions
        if broken_links:
            suggestions['maintenance'].append(f"Fix {len(broken_links)} files with broken links")
        
        if orphaned:
            suggestions['maintenance'].append(f"Review {len(orphaned)} orphaned files")
        
        return suggestions
    
    def generate_report(self) -> str:
        """Generate comprehensive maintenance report"""
        metrics = self.generate_metrics()
        broken_links = self.validate_links()
        orphaned = self.identify_orphaned_files()
        nav_analysis = self.analyze_navigation_consistency()
        suggestions = self.suggest_improvements()
        
        report = f"""# Documentation Maintenance Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Documentation Metrics
- **Total files**: {metrics['total_files']}
- **Total words**: {metrics['total_words']:,}
- **Total lines**: {metrics['total_lines']:,}
- **Average words per file**: {metrics['total_words'] // metrics['total_files']:,}

## 🔗 Link Health
- **Files with broken links**: {len(broken_links)}
- **Total broken links**: {sum(len(links) for links in broken_links.values())}
- **Orphaned files**: {len(orphaned)}

## 🧭 Navigation Analysis
- **Key files with breadcrumbs**: {nav_analysis['files_with_breadcrumbs']}/4
- **Files referencing START_HERE**: {nav_analysis['start_here_references']}
- **Files with navigation patterns**: {len(nav_analysis['navigation_patterns'])}

## ⚠️ Issues Found

### Broken Links
"""
        
        for file_path, links in broken_links.items():
            report += f"\n**{file_path}**:\n"
            for link in links:
                report += f"  - {link}\n"
        
        if not broken_links:
            report += "✅ No broken links found\n"
        
        report += "\n### Orphaned Files\n"
        for orphan in orphaned:
            report += f"- {orphan}\n"
        
        if not orphaned:
            report += "✅ No orphaned files found\n"
        
        report += "\n## 💡 Improvement Suggestions\n"
        for category, items in suggestions.items():
            if items:
                report += f"\n### {category.title()}\n"
                for item in items:
                    report += f"- {item}\n"
        
        report += "\n## 📈 Large Files (>500 lines)\n"
        large_files = [(f, stats['lines']) for f, stats in metrics['file_sizes'].items() 
                      if stats['lines'] > 500]
        large_files.sort(key=lambda x: x[1], reverse=True)
        
        for file_path, lines in large_files[:10]:
            report += f"- {file_path}: {lines} lines\n"
        
        return report
    
    def fix_broken_links(self, dry_run: bool = True) -> Dict[str, int]:
        """Attempt to fix broken links automatically"""
        results = {'fixed': 0, 'unfixable': 0}
        broken_links = self.validate_links()
        
        for file_path, links in broken_links.items():
            full_path = self.root / file_path
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            for link_text in links:
                # Try to find similar files
                link_target = link_text.split(' -> ')[1]
                target_name = Path(link_target).name
                
                # Look for files with similar names
                candidates = [f for f in self.md_files if f.name == target_name]
                
                if candidates:
                    # Calculate relative path from source to candidate
                    candidate = candidates[0]
                    try:
                        rel_path = os.path.relpath(candidate, full_path.parent)
                        content = content.replace(f"]({link_target})", f"]({rel_path})")
                        results['fixed'] += 1
                    except ValueError:
                        results['unfixable'] += 1
                else:
                    results['unfixable'] += 1
            
            # Write back if changes made and not dry run
            if content != original_content and not dry_run:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed links in {file_path}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Maintain O-Nakala Core documentation')
    parser.add_argument('--report', action='store_true', 
                       help='Generate maintenance report')
    parser.add_argument('--check-links', action='store_true',
                       help='Check for broken links')
    parser.add_argument('--fix-links', action='store_true',
                       help='Attempt to fix broken links')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without making changes')
    parser.add_argument('--output', type=str, default='maintenance-report.md',
                       help='Output file for reports')
    
    args = parser.parse_args()
    
    maintainer = DocumentationMaintainer()
    
    if args.check_links or not any([args.report, args.fix_links]):
        print("🔗 Checking documentation links...")
        broken_links = maintainer.validate_links()
        
        if broken_links:
            print(f"❌ Found broken links in {len(broken_links)} files:")
            for file_path, links in broken_links.items():
                print(f"  {file_path}:")
                for link in links:
                    print(f"    - {link}")
        else:
            print("✅ All links are valid")
    
    if args.fix_links:
        print("🔧 Attempting to fix broken links...")
        results = maintainer.fix_broken_links(dry_run=args.dry_run)
        
        if args.dry_run:
            print(f"Would fix {results['fixed']} links")
            print(f"Cannot fix {results['unfixable']} links")
        else:
            print(f"Fixed {results['fixed']} links")
            print(f"Could not fix {results['unfixable']} links")
    
    if args.report:
        print("📊 Generating maintenance report...")
        report = maintainer.generate_report()
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Report saved to {args.output}")
        
        # Print summary
        metrics = maintainer.generate_metrics()
        broken_links = maintainer.validate_links()
        orphaned = maintainer.identify_orphaned_files()
        
        print("\n📋 Quick Summary:")
        print(f"  📁 Total files: {metrics['total_files']}")
        print(f"  📝 Total words: {metrics['total_words']:,}")
        print(f"  🔗 Broken links: {sum(len(links) for links in broken_links.values())}")
        print(f"  👻 Orphaned files: {len(orphaned)}")

if __name__ == "__main__":
    main()