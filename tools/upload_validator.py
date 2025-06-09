#!/usr/bin/env python3
"""
Upload Endpoint CSV Validator

Validates CSV files for Upload endpoint against transformation logic and API requirements.
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


class UploadCSVValidator:
    """Validates CSV files for Upload endpoint."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
    def validate_csv_file(self, csv_path: Path, mode: str = "auto") -> Dict[str, Any]:
        """
        Validate a CSV file for Upload endpoint.
        
        Args:
            csv_path: Path to CSV file
            mode: Upload mode ('folder', 'csv', or 'auto')
            
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
            
            # Detect mode if auto
            if mode == "auto":
                mode = self._detect_csv_mode(df)
                self.info.append(f"Auto-detected mode: {mode}")
            
            # Validate structure
            self._validate_csv_structure(df, mode)
            
            # Validate content
            self._validate_csv_content(df, mode)
            
            # Test transformation
            self._test_transformation(df, mode)
            
            return {
                "valid": len(self.errors) == 0,
                "mode": mode,
                "errors": self.errors,
                "warnings": self.warnings,
                "info": self.info
            }
            
        except Exception as e:
            self.errors.append(f"Failed to validate CSV: {str(e)}")
            return {
                "valid": False,
                "mode": mode,
                "errors": self.errors,
                "warnings": self.warnings,
                "info": self.info
            }
    
    def _detect_csv_mode(self, df: pd.DataFrame) -> str:
        """Detect CSV mode based on column structure."""
        if 'file' in df.columns:
            return 'folder'
        elif 'files' in df.columns:
            return 'csv'
        else:
            self.warnings.append("Cannot detect mode - missing 'file' or 'files' column")
            return 'folder'  # Default to folder mode
    
    def _validate_csv_structure(self, df: pd.DataFrame, mode: str):
        """Validate CSV structure requirements."""
        required_columns = {
            'folder': ['file', 'status', 'type', 'title'],
            'csv': ['files', 'status', 'type', 'title']
        }
        
        # Check required columns
        required = required_columns.get(mode, required_columns['folder'])
        missing_columns = [col for col in required if col not in df.columns]
        
        if missing_columns:
            self.errors.append(f"Missing required columns for {mode} mode: {missing_columns}")
        
        # Check for empty DataFrame
        if df.empty:
            self.errors.append("CSV file is empty")
            return
        
        # Validate column names  
        valid_columns = set(NakalaCommonUtils.PROPERTY_URIS.keys()) | {
            'file', 'files', 'status', 'alternative', 'author', 
            'accessRights', 'temporal', 'spatial', 'keywords', 'rights',
            'date'  # Maps to created property URI
        }
        
        invalid_columns = [col for col in df.columns if col not in valid_columns]
        if invalid_columns:
            self.warnings.append(f"Unknown columns (will be ignored): {invalid_columns}")
    
    def _validate_csv_content(self, df: pd.DataFrame, mode: str):
        """Validate CSV content and values."""
        for index, row in df.iterrows():
            row_num = index + 2  # +2 for 1-based indexing and header row
            
            # Validate required fields
            self._validate_required_fields(row, row_num, mode)
            
            # Validate field formats
            self._validate_field_formats(row, row_num)
            
            # Validate multilingual formats
            self._validate_multilingual_formats(row, row_num)
    
    def _validate_required_fields(self, row: pd.Series, row_num: int, mode: str):
        """Validate required fields for each row."""
        file_field = 'file' if mode == 'folder' else 'files'
        
        # Check file/files field
        if pd.isna(row.get(file_field)) or not str(row.get(file_field)).strip():
            self.errors.append(f"Row {row_num}: Missing or empty '{file_field}' field")
        
        # Check status field
        status = row.get('status')
        if pd.isna(status) or str(status).strip() not in ['pending', 'published']:
            self.errors.append(f"Row {row_num}: Invalid status '{status}' - must be 'pending' or 'published'")
        
        # Check type field
        type_value = row.get('type')
        if pd.isna(type_value) or not str(type_value).strip():
            self.errors.append(f"Row {row_num}: Missing type field")
        elif not str(type_value).startswith('http'):
            self.warnings.append(f"Row {row_num}: Type should be a full URI starting with 'http'")
        
        # Check title field
        title = row.get('title')
        if pd.isna(title) or not str(title).strip():
            self.errors.append(f"Row {row_num}: Missing or empty title")
    
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
    
    def _validate_multilingual_formats(self, row: pd.Series, row_num: int):
        """Validate multilingual field formats."""
        multilingual_fields = ['title', 'description', 'keywords', 'contributor']
        
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
    
    def _test_transformation(self, df: pd.DataFrame, mode: str):
        """Test actual transformation logic."""
        try:
            for index, row in df.iterrows():
                row_num = index + 2
                row_dict = row.to_dict()
                
                # Remove NaN values
                row_dict = {k: v for k, v in row_dict.items() if pd.notna(v)}
                
                # Test metadata preparation
                try:
                    metadata = NakalaCommonUtils.prepare_nakala_metadata(row_dict)
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
                            
                            # Warn if typeUri missing but not for creator/contributor arrays
                            if 'typeUri' not in meta and not isinstance(meta.get('value'), list):
                                self.warnings.append(
                                    f"Row {row_num}: Metadata entry missing typeUri for '{meta.get('propertyUri', 'unknown')}'"
                                )
                
                except Exception as e:
                    self.errors.append(f"Row {row_num}: Transformation failed - {str(e)}")
                    
        except Exception as e:
            self.errors.append(f"Transformation testing failed: {str(e)}")
    
    def _is_valid_date_format(self, date_str: str) -> bool:
        """Check if date string is in valid ISO format."""
        import re
        # Basic check for YYYY-MM-DD format
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return bool(re.match(pattern, date_str))
    
    def generate_report(self, validation_result: Dict[str, Any]) -> str:
        """Generate human-readable validation report."""
        report = "# Upload CSV Validation Report\n\n"
        
        # Status
        status = "✅ VALID" if validation_result["valid"] else "❌ INVALID"
        report += f"**Status**: {status}\n"
        report += f"**Mode**: {validation_result['mode']}\n"
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
            report += "- Fix all errors before attempting upload\n"
            report += "- Check field formats and required columns\n"
            report += "- Validate multilingual syntax\n"
        elif validation_result['warnings']:
            report += "## Recommendations\n"
            report += "- Review warnings for potential improvements\n"
            report += "- Consider fixing format issues for better compatibility\n"
        else:
            report += "## Result\n"
            report += "✅ CSV is ready for upload!\n"
        
        return report


def main():
    parser = argparse.ArgumentParser(description="Validate Upload endpoint CSV files")
    parser.add_argument("csv_file", help="Path to CSV file to validate")
    parser.add_argument("--mode", choices=['folder', 'csv', 'auto'], default='auto',
                       help="Upload mode (default: auto-detect)")
    parser.add_argument("--report", help="Generate report file")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    # Validate CSV file
    validator = UploadCSVValidator()
    result = validator.validate_csv_file(Path(args.csv_file), args.mode)
    
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