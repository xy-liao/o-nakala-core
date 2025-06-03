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
    TemporalCoverage,
    SpatialCoverage,
    Relation,
    Rights,
    License
)

from .vocabulary import (
    VocabularyTerm,
    Vocabulary,
    VocabularyRegistry,
    load_vocabulary,
    get_vocabulary,
    validate_against_vocabulary,
    get_controlled_terms
)

from .validators import (
    validate_metadata,
    validate_metadata_structure,
    validate_metadata_entry,
    validate_metadata_value,
    is_valid_uri,
    is_valid_date,
    is_valid_language_code
)

__all__ = [
    'MetadataValue',
    'MetadataEntry',
    'MetadataBuilder',
    'Creator',
    'Contributor',
    'Subject',
    'TemporalCoverage',
    'SpatialCoverage',
    'Relation',
    'Rights',
    'License',
    'VocabularyTerm',
    'Vocabulary',
    'VocabularyRegistry',
    'load_vocabulary',
    'get_vocabulary',
    'validate_against_vocabulary',
    'get_controlled_terms',
    'validate_metadata',
    'validate_metadata_structure',
    'validate_metadata_entry',
    'validate_metadata_value',
    'is_valid_uri',
    'is_valid_date',
    'is_valid_language_code'
]
