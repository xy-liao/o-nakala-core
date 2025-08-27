"""
Quality Analysis Operations

Handles quality analysis and reporting for NAKALA workflow,
corresponding to Step 6 of the ultimate workflow.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Literal
import logging
import time
from o_nakala_core import NakalaCuratorClient, NakalaConfig, NakalaError

class QualityAnalyzer:
    """Handles quality analysis and reporting operations."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize quality analyzer.
        
        Args:
            config: Configuration dictionary from WorkflowConfig
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.base_path = Path(config['base_path'])
        self.quality_report_file = self.base_path / 'quality_report.json'
    
    def generate_quality_report(self, scope: Literal["datasets", "collections", "all"] = "datasets",
                              output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive quality analysis report.
        
        Args:
            scope: Analysis scope ('datasets', 'collections', or 'all')
            output_file: Custom output file path (optional)
            
        Returns:
            Dict with quality analysis results
        """
        self.logger.info("📊 Generating quality analysis report...")
        
        # Use custom output file or default
        if output_file:
            report_file = Path(output_file)
        else:
            report_file = self.quality_report_file
        
        # Create curator client and execute quality analysis
        start_time = time.time()
        try:
            config = NakalaConfig(
                api_url=self.config.get('api_url', 'https://apitest.nakala.fr'),
                api_key=self.config['api_key']
            )
            curator_client = NakalaCuratorClient(config)
            
            self.logger.info(f"Generating quality report for scope: {scope}")
            
            # Generate real quality report using curator client
            quality_data = curator_client.generate_quality_report(scope=scope)
            
            execution_time = time.time() - start_time
            
            # Save report to file
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(quality_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info("✅ Quality analysis completed successfully")
            return self._process_quality_results(report_file, execution_time, scope)
                
        except Exception as e:
            error_msg = f"Quality analysis failed: {e}"
            self.logger.error(error_msg)
            raise NakalaError(error_msg)
    
    def _process_quality_results(self, report_file: Path, execution_time: float, 
                               scope: str) -> Dict[str, Any]:
        """Process and analyze quality report results."""
        if not report_file.exists():
            raise FileNotFoundError(f"Quality report file not found: {report_file}")
        
        try:
            # Load quality report
            with open(report_file, 'r', encoding='utf-8') as f:
                quality_data = json.load(f)
            
            # Extract key statistics
            stats = self._extract_quality_statistics(quality_data, scope, execution_time)
            
            # Display summary
            self._display_quality_summary(stats, quality_data)
            
            return {
                'stats': stats,
                'quality_data': quality_data,
                'report_file': str(report_file),
                'success': True
            }
            
        except Exception as e:
            self.logger.error(f"Error processing quality results: {e}")
            raise
    
    def _extract_quality_statistics(self, quality_data: Dict[str, Any], 
                                  scope: str, execution_time: float) -> Dict[str, Any]:
        """Extract key statistics from quality report."""
        stats = {
            'scope': scope,
            'execution_time': execution_time,
            'analysis_timestamp': quality_data.get('generated_at', quality_data.get('analysis_info', {}).get('timestamp', 'Unknown')),
            'items_analyzed': 0,
            'overall_quality_score': 0.0,
            'issues_found': 0,
            'recommendations_count': 0
        }
        
        # Extract statistics from quality report
        if 'overall_statistics' in quality_data:
            overall_stats = quality_data['overall_statistics']
            stats['items_analyzed'] = overall_stats.get('total_items_analyzed', 0)
            stats['overall_quality_score'] = overall_stats.get('overall_quality_score', 0.0)
            stats['issues_found'] = overall_stats.get('items_with_issues', 0)
            stats['recommendations_count'] = overall_stats.get('recommendations_count', 0)
        else:
            # Fallback to legacy format
            if 'summary' in quality_data:
                summary = quality_data['summary']
                total_collections = summary.get('total_collections', 0)
                total_datasets = summary.get('total_datasets', 0)
                stats['items_analyzed'] = total_collections + total_datasets
            
            stats['overall_quality_score'] = quality_data.get('overall_quality_score', 0.0)
            
            collections_analysis = quality_data.get('collections_analysis', {})
            datasets_analysis = quality_data.get('datasets_analysis', {})
            stats['issues_found'] = (
                collections_analysis.get('items_with_errors', 0) + 
                datasets_analysis.get('items_with_errors', 0)
            )
        
        if 'recommendations' in quality_data and not stats.get('recommendations_count'):
            stats['recommendations_count'] = len(quality_data['recommendations'])
        
        # Extract issue categories
        if 'issues' in quality_data:
            stats['issue_categories'] = {}
            for issue in quality_data['issues']:
                category = issue.get('category', 'Unknown')
                stats['issue_categories'][category] = stats['issue_categories'].get(category, 0) + 1
        
        return stats
    
    def _display_quality_summary(self, stats: Dict[str, Any], quality_data: Dict[str, Any]):
        """Display quality analysis summary."""
        print("\n📊 Quality Analysis Summary")
        print("=" * 50)
        print(f"Scope: {stats['scope'].upper()}")
        print(f"Items Analyzed: {stats['items_analyzed']}")
        print(f"Overall Quality Score: {stats['overall_quality_score']:.2f}")
        print(f"Issues Found: {stats['issues_found']}")
        print(f"Recommendations: {stats['recommendations_count']}")
        print(f"Analysis Time: {stats['execution_time']:.2f} seconds")
        
        # Display issue categories if available
        if 'issue_categories' in stats and stats['issue_categories']:
            print("\n📋 Issue Categories:")
            for category, count in stats['issue_categories'].items():
                print(f"  - {category}: {count}")
        
        # Display top recommendations if available
        if 'recommendations' in quality_data and quality_data['recommendations']:
            print("\n💡 Top Recommendations:")
            for i, rec in enumerate(quality_data['recommendations'][:3], 1):
                # Handle both string and dict recommendations
                if isinstance(rec, str):
                    print(f"  {i}. {rec}")
                else:
                    print(f"  {i}. {rec.get('description', str(rec))}")
        
        print("=" * 50)
    
    def get_quality_report(self) -> Optional[Dict[str, Any]]:
        """Get quality report data as dictionary."""
        if self.quality_report_file.exists():
            try:
                with open(self.quality_report_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error reading quality report: {e}")
                return None
        return None
    
    def verify_quality_analysis(self) -> bool:
        """Verify quality analysis was completed successfully."""
        if not self.quality_report_file.exists():
            self.logger.warning("Quality report file not found")
            return False
        
        try:
            quality_data = self.get_quality_report()
            if not quality_data:
                self.logger.warning("Quality report file is empty or invalid")
                return False
            
            # Basic validation of report structure
            required_keys = ['analysis_info', 'overall_statistics']  # Updated required structure
            if not all(key in quality_data for key in required_keys):
                self.logger.warning("Quality report missing required structure")
                return False
            
            self.logger.info("✅ Quality analysis verification successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying quality analysis: {e}")
            return False
    
    def analyze_quality_trends(self) -> Optional[Dict[str, Any]]:
        """Analyze quality trends and patterns from the report."""
        quality_data = self.get_quality_report()
        if not quality_data:
            return None
        
        trends = {
            'metadata_completeness': 'Unknown',
            'common_issues': [],
            'improvement_areas': [],
            'strengths': []
        }
        
        try:
            # Analyze metadata completeness based on errors
            total_items = quality_data.get('summary', {}).get('total_collections', 0) + quality_data.get('summary', {}).get('total_datasets', 0)
            total_errors = quality_data.get('collections_analysis', {}).get('items_with_errors', 0) + quality_data.get('datasets_analysis', {}).get('items_with_errors', 0)
            
            if total_items > 0:
                error_rate = (total_errors / total_items) * 100
                if error_rate < 20:
                    trends['metadata_completeness'] = 'Excellent'
                elif error_rate < 40:
                    trends['metadata_completeness'] = 'Good'
                elif error_rate < 60:
                    trends['metadata_completeness'] = 'Fair'
                else:
                    trends['metadata_completeness'] = 'Needs Improvement'
            
            # Identify common issues from validation details
            issue_counts = {}
            
            # Process collections analysis
            if 'collections_analysis' in quality_data and 'validation_details' in quality_data['collections_analysis']:
                for item in quality_data['collections_analysis']['validation_details']:
                    for error in item.get('errors', []):
                        issue_counts[error] = issue_counts.get(error, 0) + 1
            
            # Process datasets analysis
            if 'datasets_analysis' in quality_data and 'validation_details' in quality_data['datasets_analysis']:
                for item in quality_data['datasets_analysis']['validation_details']:
                    for error in item.get('errors', []):
                        issue_counts[error] = issue_counts.get(error, 0) + 1
            
            # Get top 3 most common issues
            trends['common_issues'] = sorted(
                issue_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:3]
            
            # Extract improvement recommendations
            if 'recommendations' in quality_data:
                trends['improvement_areas'] = quality_data['recommendations'][:5]
            
            return trends
            
        except Exception as e:
            self.logger.error(f"Error analyzing quality trends: {e}")
            return trends
    
    def export_quality_summary(self, output_file: Optional[str] = None) -> str:
        """
        Export quality analysis summary to CSV format.
        
        Args:
            output_file: Output CSV file path (optional)
            
        Returns:
            Path to exported summary file
        """
        quality_data = self.get_quality_report()
        if not quality_data:
            raise ValueError("No quality report data available")
        
        # Determine output file
        if output_file:
            summary_file = Path(output_file)
        else:
            summary_file = self.base_path / 'quality_summary.csv'
        
        try:
            # Create summary data for CSV export
            summary_records = []
            
            if 'items' in quality_data:
                for item in quality_data['items']:
                    record = {
                        'item_id': item.get('id', 'Unknown'),
                        'item_type': item.get('type', 'Unknown'),
                        'quality_score': item.get('score', 0.0),
                        'issues_count': len(item.get('issues', [])),
                        'metadata_completeness': item.get('metadata_completeness', 0.0)
                    }
                    summary_records.append(record)
            
            # Export to CSV
            if summary_records:
                df = pd.DataFrame(summary_records)
                df.to_csv(summary_file, index=False)
                self.logger.info(f"Quality summary exported to: {summary_file}")
            else:
                self.logger.warning("No item-level data available for export")
            
            return str(summary_file)
            
        except Exception as e:
            self.logger.error(f"Error exporting quality summary: {e}")
            raise
    
