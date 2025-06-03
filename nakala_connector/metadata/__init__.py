"""
Metadata handling for Nakala API.

This module provides classes and utilities for working with Nakala metadata,
including validation, transformation, and serialization of metadata according
to Nakala's metadata schema and controlled vocabularies.
"""

from .models import (
    MetadataValue,
    MetadataEntry,
    MetadataBuilder,
    Creator,
    Contributor,
    Subject,
    Coverage,
    TemporalCoverage,
    SpatialCoverage,
    Relation,
    Rights,
    License
)

from .vocabulary import (
    load_vocabulary,
    validate_against_vocabulary,
    get_controlled_terms
)

from .validators import (
    validate_metadata,
    validate_metadata_entry,
    validate_metadata_value
)

__all__ = [
    'MetadataValue',
    'MetadataEntry',
    'MetadataBuilder',
    'Creator',
    'Contributor',
    'Subject',
    'Coverage',
    'TemporalCoverage',
    'SpatialCoverage',
    'Relation',
    'Rights',
    'License',
    'load_vocabulary',
    'validate_against_vocabulary',
    'get_controlled_terms',
    'validate_metadata',
    'validate_metadata_entry',
    'validate_metadata_value',
]
