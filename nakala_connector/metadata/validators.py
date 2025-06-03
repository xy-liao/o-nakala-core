"""
Metadata validation for Nakala API.

This module provides validation functions for Nakala metadata,
ensuring it conforms to the Nakala metadata schema and controlled vocabularies.
"""

import json
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Union, Tuple
from urllib.parse import urlparse

from pydantic import ValidationError

from .vocabulary import validate_against_vocabulary, get_controlled_terms
from .models import (
    MetadataValue,
    MetadataEntry,
    Creator,
    Contributor,
    Subject,
    TemporalCoverage,
    SpatialCoverage,
    Relation,
    Rights,
    License
)

# Required metadata fields
REQUIRED_FIELDS = [
    {
        "property_uri": "http://nakala.fr/terms#title",
        "description": "Resource title",
        "required": True,
        "multiple": False,
        "type": "string"
    },
    {
        "property_uri": "http://purl.org/dc/terms/creator",
        "description": "Resource creator(s)",
        "required": True,
        "multiple": True,
        "type": "object"
    },
    {
        "property_uri": "http://purl.org/dc/terms/type",
        "description": "Resource type",
        "required": True,
        "multiple": False,
        "type": "string",
        "vocabulary": "resource_types"
    },
    {
        "property_uri": "http://purl.org/dc/terms/rights",
        "description": "Rights information",
        "required": True,
        "multiple": False,
        "type": "object"
    }
]

# Common validation functions
def is_valid_uri(uri: str) -> bool:
    """Check if a string is a valid URI."""
    try:
        result = urlparse(uri)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def is_valid_date(date_str: str) -> bool:
    """Check if a string is a valid date in YYYY-MM-DD format."""
    try:
        if isinstance(date_str, (date, datetime)):
            return True
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False

def is_valid_language_code(lang: str) -> bool:
    """Check if a string is a valid language code (ISO 639-1 or 639-3)."""
    if not lang or not isinstance(lang, str):
        return False
    return len(lang) in (2, 3) and lang.isalpha()

def validate_metadata_value(value: Any, field_spec: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a single metadata value against a field specification.
    
    Args:
        value: The value to validate
        field_spec: Field specification from REQUIRED_FIELDS
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check required field
    if field_spec.get('required') and value is None:
        errors.append(f"Field '{field_spec['property_uri']}' is required")
        return False, errors
    
    # Skip further validation if value is None and field is not required
    if value is None:
        return True, []
    
    # Check type
    expected_type = field_spec.get('type', 'string')
    
    if expected_type == 'string':
        if not isinstance(value, str):
            errors.append(f"Expected string for field '{field_spec['property_uri']}', got {type(value).__name__}")
    elif expected_type == 'object':
        if not isinstance(value, dict):
            errors.append(f"Expected object for field '{field_spec['property_uri']}', got {type(value).__name__}")
    elif expected_type == 'array':
        if not isinstance(value, (list, tuple)):
            errors.append(f"Expected array for field '{field_spec['property_uri']}', got {type(value).__name__}")
    elif expected_type == 'number':
        if not isinstance(value, (int, float)):
            errors.append(f"Expected number for field '{field_spec['property_uri']}', got {type(value).__name__}")
    elif expected_type == 'boolean':
        if not isinstance(value, bool):
            errors.append(f"Expected boolean for field '{field_spec['property_uri']}', got {type(value).__name__}")
    elif expected_type == 'date':
        if not is_valid_date(value):
            errors.append(f"Invalid date format for field '{field_spec['property_uri']}'. Expected YYYY-MM-DD")
    elif expected_type == 'uri':
        if not is_valid_uri(value):
            errors.append(f"Invalid URI for field '{field_spec['property_uri']}'")
    
    # Check against controlled vocabulary if specified
    if 'vocabulary' in field_spec and isinstance(value, str):
        if not validate_against_vocabulary(value, field_spec['vocabulary']):
            errors.append(
                f"Value '{value}' is not a valid term in the {field_spec['vocabulary']} vocabulary "
                f"for field '{field_spec['property_uri']}'"
            )
    
    return len(errors) == 0, errors

def validate_metadata_entry(entry: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a single metadata entry.
    
    Args:
        entry: Metadata entry to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check required fields
    if 'propertyUri' not in entry:
        errors.append("Missing required field 'propertyUri' in metadata entry")
        return False, errors
    
    if 'values' not in entry or not entry['values']:
        errors.append(f"Missing or empty 'values' in metadata entry for {entry['propertyUri']}")
        return False, errors
    
    # Find matching field specification
    field_spec = next(
        (f for f in REQUIRED_FIELDS if f['property_uri'] == entry['propertyUri']),
        None
    )
    
    if not field_spec:
        # Unknown field, but we'll allow it
        return True, []
    
    # Validate each value
    for i, value in enumerate(entry['values']):
        if not field_spec.get('multiple', True) and i > 0:
            errors.append(f"Field {entry['propertyUri']} does not allow multiple values")
            break
            
        is_valid, value_errors = validate_metadata_value(value, field_spec)
        if not is_valid:
            errors.extend(value_errors)
    
    return len(errors) == 0, errors

def validate_metadata(metadata: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate Nakala metadata against the schema.
    
    Args:
        metadata: Metadata dictionary to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check top-level required fields
    if 'status' not in metadata:
        errors.append("Missing required field 'status' in metadata")
    
    if 'metas' not in metadata or not metadata['metas']:
        errors.append("Missing or empty 'metas' in metadata")
    else:
        # Check for required fields
        required_fields = {f['property_uri']: f for f in REQUIRED_FIELDS if f.get('required', False)}
        found_fields = set()
        
        for entry in metadata['metas']:
            if 'propertyUri' in entry and entry['propertyUri'] in required_fields:
                found_fields.add(entry['propertyUri'])
            
            # Validate the entry
            is_valid, entry_errors = validate_metadata_entry(entry)
            if not is_valid:
                errors.extend(entry_errors)
        
        # Check for missing required fields
        missing_fields = set(required_fields.keys()) - found_fields
        for field_uri in missing_fields:
            errors.append(f"Missing required field: {field_uri}")
    
    # Validate rights if present
    if 'rights' in metadata and metadata['rights']:
        try:
            # Try to parse as a Rights object
            Rights.model_validate(metadata['rights'])
        except ValidationError as e:
            errors.append(f"Invalid rights format: {str(e)}")
    
    # Validate files if present
    if 'files' in metadata and metadata['files']:
        if not isinstance(metadata['files'], list):
            errors.append("'files' must be an array")
        else:
            for i, file_info in enumerate(metadata['files']):
                if not isinstance(file_info, dict):
                    errors.append(f"File at index {i} must be an object")
                elif 'sha1' not in file_info:
                    errors.append(f"File at index {i} is missing required 'sha1' field")
    
    return len(errors) == 0, errors


def validate_metadata_structure(metadata: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate the basic structure of Nakala metadata.
    
    This is a lighter check than validate_metadata and doesn't validate
    against controlled vocabularies or specific field requirements.
    
    Args:
        metadata: Metadata dictionary to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    if not isinstance(metadata, dict):
        return False, ["Metadata must be a JSON object"]
    
    # Check top-level fields
    if 'status' not in metadata:
        errors.append("Missing required field 'status'")
    
    if 'metas' not in metadata:
        errors.append("Missing required field 'metas'")
    elif not isinstance(metadata['metas'], list):
        errors.append("'metas' must be an array")
    
    # Check each metadata entry
    if 'metas' in metadata and isinstance(metadata['metas'], list):
        for i, entry in enumerate(metadata['metas']):
            if not isinstance(entry, dict):
                errors.append(f"Metadata entry at index {i} must be an object")
                continue
            
            if 'propertyUri' not in entry:
                errors.append(f"Metadata entry at index {i} is missing 'propertyUri'")
            
            if 'values' not in entry:
                errors.append(f"Metadata entry at index {i} is missing 'values'")
            elif not isinstance(entry['values'], list):
                errors.append(f"'values' in metadata entry at index {i} must be an array")
    
    # Check rights if present
    if 'rights' in metadata and metadata['rights'] is not None:
        if not isinstance(metadata['rights'], dict):
            errors.append("'rights' must be an object")
    
    # Check files if present
    if 'files' in metadata and metadata['files'] is not None:
        if not isinstance(metadata['files'], list):
            errors.append("'files' must be an array")
    
    return len(errors) == 0, errors
