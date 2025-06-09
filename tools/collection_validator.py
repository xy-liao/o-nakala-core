#!/usr/bin/env python3
"""
Collection Endpoint CSV Validator

Validates CSV files for Collection endpoint against transformation logic and API requirements.
"""

import argparse
import sys
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nakala_client.common.utils import NakalaCommonUtils


class CollectionCSVValidator:
    """Validates CSV files for Collection endpoint."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
    def validate_csv_file(self, csv_path: Path) -> Dict[str, Any]:
        """
        Validate a CSV file for Collection endpoint.
        
        Args:
            csv_path: Path to CSV file
            
        Returns:
            Validation result dictionary
        """
        self.errors = []
        self.warnings = []
        self.info = []
        
        try:
            # Load and parse CSV
            df = pd.read_csv(csv_path)
            self.info.append(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
            
            # Validate structure
            self._validate_csv_structure(df)
            
            # Validate content
            self._validate_csv_content(df)
            
            # Test transformation
            self._test_transformation(df)
            
            return {
                "valid": len(self.errors) == 0,
                "errors": self.errors,
                "warnings": self.warnings,
                "info": self.info
            }
            
        except Exception as e:
            self.errors.append(f"Failed to validate CSV: {str(e)}")
            return {
                "valid": False,
                "errors": self.errors,
                "warnings": self.warnings,
                "info": self.info
            }
    
    def _validate_csv_structure(self, df: pd.DataFrame):
        """Validate CSV structure requirements."""
        # Required columns for collections
        required_columns = ['title', 'status', 'data_items']
        
        # Check required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            self.errors.append(f"Missing required columns: {missing_columns}")
        
        # Check for empty DataFrame
        if df.empty:
            self.errors.append("CSV file is empty")
            return
        
        # Validate column names
        valid_columns = set(NakalaCommonUtils.PROPERTY_URIS.keys()) | {
            'title', 'status', 'data_items', 'alternative', 'keywords',
            'rights', 'date', 'coverage', 'relation', 'source', 'language',
            'temporal', 'spatial'
        }
        
        invalid_columns = [col for col in df.columns if col not in valid_columns]
        if invalid_columns:
            self.warnings.append(f"Unknown columns (will be ignored): {invalid_columns}")
    
    def _validate_csv_content(self, df: pd.DataFrame):
        """Validate CSV content and values."""
        for index, row in df.iterrows():
            row_num = index + 2  # +2 for 1-based indexing and header row
            
            # Validate required fields
            self._validate_required_fields(row, row_num)
            
            # Validate field formats
            self._validate_field_formats(row, row_num)
            
            # Validate multilingual formats
            self._validate_multilingual_formats(row, row_num)
    
    def _validate_required_fields(self, row: pd.Series, row_num: int):
        """Validate required fields for each row."""
        # Check title field
        title = row.get('title')
        if pd.isna(title) or not str(title).strip():
            self.errors.append(f"Row {row_num}: Missing or empty title")
        
        # Check status field
        status = row.get('status')
        if pd.isna(status) or str(status).strip() not in ['pending', 'published', 'private']:
            self.errors.append(f"Row {row_num}: Invalid status '{status}' - must be 'pending', 'published', or 'private'")
        
        # Check data_items field
        data_items = row.get('data_items')
        if pd.isna(data_items) or not str(data_items).strip():
            self.errors.append(f"Row {row_num}: Missing or empty data_items field")
    
    def _validate_field_formats(self, row: pd.Series, row_num: int):
        """Validate specific field formats."""
        # Validate date format
        date_value = row.get('date')
        if pd.notna(date_value) and str(date_value).strip():
            date_str = str(date_value).strip()
            if not self._is_valid_date_format(date_str):
                self.warnings.append(f"Row {row_num}: Date '{date_str}' should be in ISO format (YYYY-MM-DD)")
        
        # Validate language codes
        language = row.get('language')
        if pd.notna(language) and str(language).strip():
            lang_str = str(language).strip()
            if len(lang_str) > 3:
                self.warnings.append(f"Row {row_num}: Language code '{lang_str}' should be ≤ 3 characters")
        
        # Validate rights format
        rights = row.get('rights')
        if pd.notna(rights) and str(rights).strip():
            rights_str = str(rights).strip()
            if ',' not in rights_str:
                self.warnings.append(f"Row {row_num}: Rights should be in format 'group_id,ROLE_NAME'")
        
        # Validate data_items patterns
        data_items = row.get('data_items')
        if pd.notna(data_items) and str(data_items).strip():
            patterns = str(data_items).strip().split('|')
            for pattern in patterns:
                pattern = pattern.strip()
                if not pattern:
                    self.warnings.append(f"Row {row_num}: Empty pattern in data_items")
                elif not self._is_valid_folder_pattern(pattern):
                    self.warnings.append(f"Row {row_num}: Pattern '{pattern}' may not match typical folder structures")
    
    def _validate_multilingual_formats(self, row: pd.Series, row_num: int):
        """Validate multilingual field formats."""
        multilingual_fields = ['title', 'description', 'keywords', 'contributor', 'publisher', 'coverage', 'relation', 'source']
        
        for field in multilingual_fields:
            value = row.get(field)
            if pd.notna(value) and str(value).strip():
                value_str = str(value).strip()
                if '|' in value_str:
                    # Validate multilingual format
                    parts = value_str.split('|')
                    for part in parts:
                        if ':' not in part:
                            self.warnings.append(
                                f"Row {row_num}, Field '{field}': Multilingual part '{part}' missing language code"
                            )
                        else:
                            lang, text = part.split(':', 1)
                            if not lang.strip():
                                self.warnings.append(
                                    f"Row {row_num}, Field '{field}': Empty language code in '{part}'"
                                )
                            if not text.strip():
                                self.warnings.append(
                                    f"Row {row_num}, Field '{field}': Empty text in '{part}'"
                                )
    
    def _test_transformation(self, df: pd.DataFrame):
        """Test actual transformation logic."""
        try:
            for index, row in df.iterrows():
                row_num = index + 2
                row_dict = row.to_dict()
                
                # Remove NaN values
                row_dict = {k: v for k, v in row_dict.items() if pd.notna(v)}
                
                # Test metadata preparation using collection-specific fields
                try:
                    # Prepare metadata dict similar to collection processing
                    metadata_dict = {}
                    collection_fields = ['title', 'description', 'keywords', 'creator', 'contributor', 'publisher', 'coverage', 'relation', 'source', 'language', 'date']
                    
                    for field in collection_fields:
                        if field in row_dict and row_dict[field]:
                            metadata_dict[field] = str(row_dict[field])
                    
                    if metadata_dict:
                        metadata = NakalaCommonUtils.prepare_nakala_metadata(metadata_dict)
                        if not metadata:
                            self.warnings.append(f"Row {row_num}: No metadata generated")
                        else:
                            self.info.append(f"Row {row_num}: Generated {len(metadata)} metadata entries")
                            
                            # Validate generated metadata structure
                            for meta in metadata:
                                if not isinstance(meta, dict):
                                    self.errors.append(f"Row {row_num}: Invalid metadata structure")
                                    continue
                                
                                # Check required keys (typeUri is optional for creator/contributor arrays)
                                required_keys = ['propertyUri', 'value']
                                missing_keys = [key for key in required_keys if key not in meta]
                                if missing_keys:
                                    self.errors.append(
                                        f"Row {row_num}: Metadata missing keys: {missing_keys}"
                                    )
                    else:
                        self.warnings.append(f"Row {row_num}: No metadata fields to transform")
                
                except Exception as e:
                    self.errors.append(f"Row {row_num}: Transformation failed - {str(e)}")
                    
        except Exception as e:
            self.errors.append(f"Transformation testing failed: {str(e)}")
    
    def _is_valid_date_format(self, date_str: str) -> bool:
        """Check if date string is in valid ISO format."""
        import re
        # Basic check for YYYY-MM-DD format or ranges
        pattern = r'^(\d{4}(-\d{2}(-\d{2})?)?(/\d{4}(-\d{2}(-\d{2})?)?)?)$'
        return bool(re.match(pattern, date_str))
    
    def _is_valid_folder_pattern(self, pattern: str) -> bool:
        """Check if folder pattern looks reasonable."""
        # Basic check for common folder patterns
        common_patterns = [
            'files/', 'data/', 'code/', 'documents/', 'images/', 'results/',
            'src/', 'scripts/', 'analysis/', 'raw/', 'processed/', 'output/'
        ]
        
        # Check if pattern contains common folder keywords
        pattern_lower = pattern.lower()
        return any(common in pattern_lower for common in common_patterns) or len(pattern) >= 3
    
    def generate_report(self, validation_result: Dict[str, Any]) -> str:
        """Generate human-readable validation report."""
        report = "# Collection CSV Validation Report\n\n"
        
        # Status
        status = "✅ VALID" if validation_result["valid"] else "❌ INVALID"
        report += f"**Status**: {status}\n"
        report += f"**Errors**: {len(validation_result['errors'])}\n"
        report += f"**Warnings**: {len(validation_result['warnings'])}\n\n"
        
        # Info
        if validation_result['info']:
            report += "## Information\n"
            for info in validation_result['info']:
                report += f"- ℹ️ {info}\n"
            report += "\n"
        
        # Errors
        if validation_result['errors']:
            report += "## Errors\n"
            for error in validation_result['errors']:
                report += f"- ❌ {error}\n"
            report += "\n"
        
        # Warnings
        if validation_result['warnings']:
            report += "## Warnings\n"
            for warning in validation_result['warnings']:
                report += f"- ⚠️ {warning}\n"
            report += "\n"
        
        # Recommendations
        if validation_result['errors']:
            report += "## Recommendations\n"
            report += "- Fix all errors before attempting collection creation\n"
            report += "- Check required fields: title, status, data_items\n"
            report += "- Validate multilingual syntax and folder patterns\n"
        elif validation_result['warnings']:
            report += "## Recommendations\n"
            report += "- Review warnings for potential improvements\n"
            report += "- Consider fixing format issues for better compatibility\n"
        else:
            report += "## Result\n"
            report += "✅ CSV is ready for collection creation!\n"
        
        return report


def main():
    parser = argparse.ArgumentParser(description="Validate Collection endpoint CSV files")
    parser.add_argument("csv_file", help="Path to CSV file to validate")
    parser.add_argument("--report", help="Generate report file")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    # Validate CSV file
    validator = CollectionCSVValidator()
    result = validator.validate_csv_file(Path(args.csv_file))
    
    if args.json:
        # JSON output
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        print(validator.generate_report(result))
    
    # Generate report file if requested
    if args.report:
        report = validator.generate_report(result)
        with open(args.report, 'w') as f:
            f.write(report)
        print(f"\nReport saved to {args.report}")
    
    # Exit with error code if validation failed
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()