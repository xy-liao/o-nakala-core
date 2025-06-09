#!/usr/bin/env python3
"""
Curator Endpoint CSV Validator

Validates CSV files for Curator endpoint against transformation logic and API requirements.
"""

import argparse
import sys
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json
import re

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nakala_client.common.utils import NakalaCommonUtils


class CuratorCSVValidator:
    """Validates CSV files for Curator endpoint."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
        # Curator-specific field mappings (subset of the 280+ mappings)
        self.CURATOR_FIELD_MAPPINGS = {
            "new_title": {
                "property_uri": "http://nakala.fr/terms#title",
                "format": "multilingual",
                "required": False
            },
            "new_description": {
                "property_uri": "http://purl.org/dc/terms/description",
                "format": "multilingual", 
                "required": False
            },
            "new_keywords": {
                "property_uri": "http://purl.org/dc/terms/subject",
                "format": "multilingual",
                "required": False
            },
            "new_creator": {
                "property_uri": "http://nakala.fr/terms#creator",
                "format": "semicolon_split",
                "required": False
            },
            "new_contributor": {
                "property_uri": "http://purl.org/dc/terms/contributor",
                "format": "array",
                "required": False
            },
            "new_publisher": {
                "property_uri": "http://purl.org/dc/terms/publisher",
                "format": "multilingual",
                "required": False
            },
            "new_rights": {
                "property_uri": "http://purl.org/dc/terms/rights",
                "format": "rights_list",
                "required": False
            },
            "new_status": {
                "property_uri": "http://nakala.fr/terms#status",
                "format": "string",
                "required": False
            },
            "new_language": {
                "property_uri": "http://purl.org/dc/terms/language",
                "format": "string",
                "required": False
            },
            "new_coverage": {
                "property_uri": "http://purl.org/dc/terms/coverage",
                "format": "multilingual",
                "required": False
            },
            "new_relation": {
                "property_uri": "http://purl.org/dc/terms/relation",
                "format": "multilingual",
                "required": False
            },
            "new_source": {
                "property_uri": "http://purl.org/dc/terms/source",
                "format": "multilingual",
                "required": False
            },
            "new_alternative": {
                "property_uri": "http://purl.org/dc/terms/alternative",
                "format": "multilingual",
                "required": False
            },
            "new_format": {
                "property_uri": "http://purl.org/dc/terms/format",
                "format": "string",
                "required": False
            },
            "new_identifier": {
                "property_uri": "http://purl.org/dc/terms/identifier",
                "format": "string",
                "required": False
            }
        }
        
    def validate_csv_file(self, csv_path: Path) -> Dict[str, Any]:
        """
        Validate a CSV file for Curator endpoint.
        
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
        # Required columns for curator modifications
        required_columns = ['id', 'action']
        
        # Check required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            self.errors.append(f"Missing required columns: {missing_columns}")
        
        # Check for empty DataFrame
        if df.empty:
            self.errors.append("CSV file is empty")
            return
        
        # Validate modification columns (new_ prefix)
        modification_columns = [col for col in df.columns if col.startswith('new_')]
        if not modification_columns:
            self.warnings.append("No modification fields (new_*) found - no changes will be applied")
        
        # Validate column names
        valid_columns = {'id', 'action'} | set(self.CURATOR_FIELD_MAPPINGS.keys())
        
        # Add current_ columns (for template exports)
        current_columns = {col.replace('new_', 'current_') for col in self.CURATOR_FIELD_MAPPINGS.keys()}
        valid_columns.update(current_columns)
        
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
            
            # Validate modification content
            self._validate_modification_content(row, row_num)
    
    def _validate_required_fields(self, row: pd.Series, row_num: int):
        """Validate required fields for each row."""
        # Check id field
        resource_id = row.get('id')
        if pd.isna(resource_id) or not str(resource_id).strip():
            self.errors.append(f"Row {row_num}: Missing or empty resource ID")
        elif not self._is_valid_nakala_id(str(resource_id).strip()):
            self.errors.append(f"Row {row_num}: Invalid NAKALA identifier format: '{resource_id}'")
        
        # Check action field
        action = row.get('action')
        if pd.isna(action) or str(action).strip() != 'modify':
            self.errors.append(f"Row {row_num}: Invalid action '{action}' - must be 'modify'")
    
    def _validate_field_formats(self, row: pd.Series, row_num: int):
        """Validate specific field formats."""
        # Validate new_language format
        language = row.get('new_language')
        if pd.notna(language) and str(language).strip():
            lang_str = str(language).strip()
            if len(lang_str) > 3:
                self.warnings.append(f"Row {row_num}: Language code '{lang_str}' should be ≤ 3 characters")
        
        # Validate new_rights format
        rights = row.get('new_rights')
        if pd.notna(rights) and str(rights).strip():
            rights_str = str(rights).strip()
            self._validate_rights_format(rights_str, row_num)
        
        # Validate new_status format
        status = row.get('new_status')
        if pd.notna(status) and str(status).strip():
            status_str = str(status).strip()
            if status_str not in ['pending', 'published', 'private']:
                self.errors.append(f"Row {row_num}: Invalid status '{status_str}' - must be 'pending', 'published', or 'private'")
    
    def _validate_rights_format(self, rights_str: str, row_num: int):
        """Validate rights field format."""
        for right_entry in rights_str.split(';'):
            right_entry = right_entry.strip()
            if ',' not in right_entry:
                self.errors.append(f"Row {row_num}: Rights entry '{right_entry}' must be in format 'group_id,ROLE_NAME'")
            else:
                group_id, role = right_entry.split(',', 1)
                group_id = group_id.strip()
                role = role.strip()
                
                if not group_id:
                    self.errors.append(f"Row {row_num}: Empty group ID in rights entry '{right_entry}'")
                
                valid_roles = ['ROLE_OWNER', 'ROLE_ADMIN', 'ROLE_EDITOR', 'ROLE_READER']
                if role not in valid_roles:
                    self.warnings.append(f"Row {row_num}: Unknown role '{role}' - valid roles: {valid_roles}")
    
    def _validate_multilingual_formats(self, row: pd.Series, row_num: int):
        """Validate multilingual field formats."""
        multilingual_fields = [field for field in self.CURATOR_FIELD_MAPPINGS.keys() 
                              if self.CURATOR_FIELD_MAPPINGS[field]['format'] == 'multilingual']
        
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
    
    def _validate_modification_content(self, row: pd.Series, row_num: int):
        """Validate that at least one modification field has content."""
        modification_fields = [col for col in row.index if col.startswith('new_')]
        has_modifications = False
        
        for field in modification_fields:
            value = row.get(field)
            if pd.notna(value) and str(value).strip():
                has_modifications = True
                break
        
        if not has_modifications:
            self.warnings.append(f"Row {row_num}: No modification fields have content - no changes will be applied")
    
    def _test_transformation(self, df: pd.DataFrame):
        """Test actual transformation logic."""
        try:
            for index, row in df.iterrows():
                row_num = index + 2
                row_dict = row.to_dict()
                
                # Remove NaN values
                row_dict = {k: v for k, v in row_dict.items() if pd.notna(v)}
                
                # Test curator-specific transformation
                try:
                    metadata_entries = []
                    modification_count = 0
                    
                    # Process modification fields
                    for field, value in row_dict.items():
                        if field.startswith('new_') and field in self.CURATOR_FIELD_MAPPINGS:
                            field_config = self.CURATOR_FIELD_MAPPINGS[field]
                            
                            # Process based on format type
                            if field_config['format'] == 'multilingual':
                                entries = self._process_multilingual_field(value, field_config['property_uri'])
                                metadata_entries.extend(entries)
                                modification_count += len(entries)
                            
                            elif field_config['format'] == 'semicolon_split':
                                entries = self._process_semicolon_split_field(value, field_config['property_uri'])
                                metadata_entries.extend(entries)
                                modification_count += len(entries)
                            
                            elif field_config['format'] == 'array':
                                entries = self._process_array_field(value, field_config['property_uri'])
                                metadata_entries.extend(entries)
                                modification_count += len(entries)
                            
                            elif field_config['format'] == 'rights_list':
                                # Rights don't go in metadata, they go in rights array
                                modification_count += 1
                            
                            elif field_config['format'] == 'string':
                                if field == 'new_status':
                                    # Status doesn't go in metadata
                                    modification_count += 1
                                else:
                                    entry = {
                                        "propertyUri": field_config['property_uri'],
                                        "value": str(value),
                                        "typeUri": "http://www.w3.org/2001/XMLSchema#string"
                                    }
                                    metadata_entries.append(entry)
                                    modification_count += 1
                    
                    if modification_count > 0:
                        self.info.append(f"Row {row_num}: Generated {len(metadata_entries)} metadata entries ({modification_count} total modifications)")
                    else:
                        self.warnings.append(f"Row {row_num}: No modifications processed")
                        
                    # Validate generated metadata structure
                    for meta in metadata_entries:
                        if not isinstance(meta, dict):
                            self.errors.append(f"Row {row_num}: Invalid metadata structure")
                            continue
                        
                        # Check required keys
                        required_keys = ['propertyUri', 'value']
                        missing_keys = [key for key in required_keys if key not in meta]
                        if missing_keys:
                            self.errors.append(
                                f"Row {row_num}: Metadata missing keys: {missing_keys}"
                            )
                
                except Exception as e:
                    self.errors.append(f"Row {row_num}: Transformation failed - {str(e)}")
                    
        except Exception as e:
            self.errors.append(f"Transformation testing failed: {str(e)}")
    
    def _process_multilingual_field(self, value: str, property_uri: str) -> List[Dict[str, Any]]:
        """Process multilingual field value."""
        entries = []
        value_str = str(value).strip()
        
        if '|' in value_str:
            # Multilingual format
            parts = value_str.split('|')
            for part in parts:
                if ':' in part:
                    lang, text = part.split(':', 1)
                    entries.append({
                        "propertyUri": property_uri,
                        "value": text.strip(),
                        "lang": lang.strip(),
                        "typeUri": "http://www.w3.org/2001/XMLSchema#string"
                    })
        else:
            # Single language
            entries.append({
                "propertyUri": property_uri,
                "value": value_str,
                "lang": "und",
                "typeUri": "http://www.w3.org/2001/XMLSchema#string"
            })
        
        return entries
    
    def _process_semicolon_split_field(self, value: str, property_uri: str) -> List[Dict[str, Any]]:
        """Process semicolon-separated field value."""
        entries = []
        items = str(value).split(';')
        
        for item in items:
            item = item.strip()
            if item:
                entries.append({
                    "propertyUri": property_uri,
                    "value": item,
                    "typeUri": "http://www.w3.org/2001/XMLSchema#string"
                })
        
        return entries
    
    def _process_array_field(self, value: str, property_uri: str) -> List[Dict[str, Any]]:
        """Process array field value."""
        entries = []
        value_str = str(value).strip()
        
        if '|' in value_str:
            # Multilingual array
            parts = value_str.split('|')
            for part in parts:
                if ':' in part:
                    lang, text = part.split(':', 1)
                    items = text.split(';')
                    item_objects = [{"name": item.strip()} for item in items if item.strip()]
                    entries.append({
                        "propertyUri": property_uri,
                        "value": item_objects,
                        "lang": lang.strip()
                    })
        else:
            # Simple array
            items = value_str.split(';')
            item_objects = [{"name": item.strip()} for item in items if item.strip()]
            entries.append({
                "propertyUri": property_uri,
                "value": item_objects
            })
        
        return entries
    
    def _is_valid_nakala_id(self, identifier: str) -> bool:
        """Check if identifier is valid NAKALA format."""
        # Pattern for NAKALA identifiers
        pattern = r'^((10\.34847/nkl\.|11280/)[a-z0-9]{8})(\\.v([0-9]+))?$'
        return bool(re.match(pattern, identifier))
    
    def generate_report(self, validation_result: Dict[str, Any]) -> str:
        """Generate human-readable validation report."""
        report = "# Curator CSV Validation Report\n\n"
        
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
            report += "- Fix all errors before attempting batch modification\n"
            report += "- Check required fields: id, action\n"
            report += "- Validate NAKALA identifier formats\n"
            report += "- Ensure at least one new_* field has content per row\n"
        elif validation_result['warnings']:
            report += "## Recommendations\n"
            report += "- Review warnings for potential improvements\n"
            report += "- Consider fixing format issues for better compatibility\n"
            report += "- Verify multilingual syntax and rights formats\n"
        else:
            report += "## Result\n"
            report += "✅ CSV is ready for curator batch modification!\n"
        
        return report


def main():
    parser = argparse.ArgumentParser(description="Validate Curator endpoint CSV files")
    parser.add_argument("csv_file", help="Path to CSV file to validate")
    parser.add_argument("--report", help="Generate report file")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    # Validate CSV file
    validator = CuratorCSVValidator()
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