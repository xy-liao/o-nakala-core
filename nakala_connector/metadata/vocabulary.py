"""
Vocabulary and validation utilities for Nakala metadata.

This module provides functionality for loading and validating against
Nakala's controlled vocabularies and metadata schemas.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Union, Any
from urllib.parse import urlparse

import requests
from pydantic import BaseModel, HttpUrl, field_validator, ValidationError

# Default vocabulary files
DEFAULT_VOCABULARY_FILES = {
    "licenses": "licenses.json",
    "languages": "languages.json",
    "resource_types": "resource_types.json",
    "subjects": "subjects.json",
    "formats": "formats.json"
}

class VocabularyTerm(BaseModel):
    """A term in a controlled vocabulary."""
    uri: Optional[HttpUrl] = None
    pref_label: Dict[str, str] = {}
    alt_label: Dict[str, List[str]] = {}
    definition: Dict[str, str] = {}
    broader: List[HttpUrl] = []
    narrower: List[HttpUrl] = []
    related: List[HttpUrl] = []
    in_scheme: Optional[HttpUrl] = None
    top_concept_of: Optional[HttpUrl] = None
    
    @field_validator('pref_label', 'alt_label', 'definition', mode='before')
    @classmethod
    def ensure_dict_str_str(cls, v):
        if v is None:
            return {}
        if not isinstance(v, dict):
            raise ValueError("Must be a dictionary")
        return v
    
    @field_validator('broader', 'narrower', 'related', mode='before')
    @classmethod
    def ensure_list_of_uris(cls, v):
        if v is None:
            return []
        if not isinstance(v, list):
            return [v]
        return v


class Vocabulary:
    """A controlled vocabulary for Nakala metadata."""
    
    def __init__(self, name: str, terms: Dict[str, VocabularyTerm] = None):
        self.name = name
        self.terms = terms or {}
        self.uri_index = {}
        self.label_index = {}
        
        # Build indexes
        for term_id, term in self.terms.items():
            # Index by URI if available
            if term.uri:
                self.uri_index[str(term.uri)] = term_id
            
            # Index by prefLabel
            for lang, label in term.pref_label.items():
                lang_key = f"{lang}:{label.lower()}"
                self.label_index[lang_key] = term_id
            
            # Index by altLabel
            for lang, labels in term.alt_label.items():
                for label in labels:
                    lang_key = f"{lang}:{label.lower()}"
                    self.label_index[lang_key] = term_id
    
    def get_term(self, term_id: str) -> Optional[VocabularyTerm]:
        """Get a term by its ID."""
        return self.terms.get(term_id)
    
    def get_term_by_uri(self, uri: str) -> Optional[VocabularyTerm]:
        """Get a term by its URI."""
        term_id = self.uri_index.get(uri)
        if term_id:
            return self.terms.get(term_id)
        return None
    
    def get_term_by_label(self, label: str, lang: str = "en") -> Optional[VocabularyTerm]:
        """Get a term by its label in a specific language."""
        lang_key = f"{lang}:{label.lower()}"
        term_id = self.label_index.get(lang_key)
        if term_id:
            return self.terms.get(term_id)
        return None
    
    def search(self, query: str, lang: str = "en") -> List[VocabularyTerm]:
        """Search for terms matching a query."""
        query = query.lower()
        results = []
        
        for term_id, term in self.terms.items():
            # Check prefLabels
            for term_lang, label in term.pref_label.items():
                if term_lang.startswith(lang) and query in label.lower():
                    results.append(term)
                    break
            
            # Check altLabels if not already found
            else:
                for term_lang, labels in term.alt_label.items():
                    if term_lang.startswith(lang):
                        if any(query in label.lower() for label in labels):
                            results.append(term)
                            break
        
        return results


class VocabularyRegistry:
    """Registry for managing multiple controlled vocabularies."""
    
    def __init__(self, vocabularies_dir: Optional[str] = None):
        self.vocabularies: Dict[str, Vocabulary] = {}
        self.vocabularies_dir = vocabularies_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "vocabularies"
        )
    
    def load_vocabulary(self, name: str, force_reload: bool = False) -> Optional[Vocabulary]:
        """Load a vocabulary by name."""
        if name in self.vocabularies and not force_reload:
            return self.vocabularies[name]
        
        vocab_file = os.path.join(self.vocabularies_dir, f"{name}.json")
        if not os.path.exists(vocab_file):
            return None
        
        try:
            with open(vocab_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            terms = {}
            for term_id, term_data in data.get('terms', {}).items():
                try:
                    terms[term_id] = VocabularyTerm(**term_data)
                except ValidationError as e:
                    print(f"Warning: Error loading term {term_id} in vocabulary {name}: {e}")
            
            vocabulary = Vocabulary(name, terms)
            self.vocabularies[name] = vocabulary
            return vocabulary
            
        except Exception as e:
            print(f"Error loading vocabulary {name}: {e}")
            return None
    
    def get_vocabulary(self, name: str) -> Optional[Vocabulary]:
        """Get a loaded vocabulary by name."""
        return self.vocabularies.get(name)
    
    def get_term(self, vocab_name: str, term_id: str) -> Optional[VocabularyTerm]:
        """Get a term from a specific vocabulary."""
        vocab = self.get_vocabulary(vocab_name)
        if not vocab:
            vocab = self.load_vocabulary(vocab_name)
        
        if vocab:
            return vocab.get_term(term_id)
        return None
    
    def search_terms(self, query: str, vocab_names: Optional[List[str]] = None, lang: str = "en") -> Dict[str, List[VocabularyTerm]]:
        """Search for terms across multiple vocabularies."""
        results = {}
        
        if not vocab_names:
            vocab_names = list(self.vocabularies.keys())
        
        for name in vocab_names:
            vocab = self.get_vocabulary(name)
            if not vocab:
                vocab = self.load_vocabulary(name)
            
            if vocab:
                matches = vocab.search(query, lang)
                if matches:
                    results[name] = matches
        
        return results


# Global registry instance
_vocabulary_registry = VocabularyRegistry()


def load_vocabulary(name: str, force_reload: bool = False) -> Optional[Vocabulary]:
    """Load a vocabulary by name."""
    return _vocabulary_registry.load_vocabulary(name, force_reload)


def get_vocabulary(name: str) -> Optional[Vocabulary]:
    """Get a loaded vocabulary by name."""
    return _vocabulary_registry.get_vocabulary(name)


def get_term(vocab_name: str, term_id: str) -> Optional[VocabularyTerm]:
    """Get a term from a specific vocabulary."""
    return _vocabulary_registry.get_term(vocab_name, term_id)


def search_terms(query: str, vocab_names: Optional[List[str]] = None, lang: str = "en") -> Dict[str, List[VocabularyTerm]]:
    """Search for terms across multiple vocabularies."""
    return _vocabulary_registry.search_terms(query, vocab_names, lang)


def validate_against_vocabulary(value: str, vocabulary_name: str, lang: str = "en") -> bool:
    """
    Validate that a value exists in the specified vocabulary.
    
    Args:
        value: The value to validate
        vocabulary_name: Name of the vocabulary to validate against
        lang: Language code for label matching
        
    Returns:
        bool: True if the value is valid, False otherwise
    """
    if not value:
        return False
    
    vocab = get_vocabulary(vocabulary_name)
    if not vocab:
        return False
    
    # Check if the value is a term ID
    if value in vocab.terms:
        return True
    
    # Check if the value is a URI
    if value.startswith(('http://', 'https://')):
        term = vocab.get_term_by_uri(value)
        if term:
            return True
    
    # Check if the value matches a label
    term = vocab.get_term_by_label(value, lang)
    if term:
        return True
    
    return False


def get_controlled_terms(vocabulary_name: str, lang: str = "en") -> List[Dict[str, Any]]:
    """
    Get a list of controlled terms from a vocabulary.
    
    Args:
        vocabulary_name: Name of the vocabulary
        lang: Preferred language for labels
        
    Returns:
        List of term dictionaries with id, label, and uri
    """
    vocab = get_vocabulary(vocabulary_name)
    if not vocab:
        return []
    
    terms = []
    for term_id, term in vocab.terms.items():
        # Get the preferred label in the requested language
        label = None
        if term.pref_label:
            # Try exact language match first
            if lang in term.pref_label:
                label = term.pref_label[lang]
            # Fall back to any language
            elif term.pref_label:
                label = next(iter(term.pref_label.values()))
        
        # Fall back to term ID if no label
        if not label:
            label = term_id
        
        terms.append({
            'id': term_id,
            'label': label,
            'uri': str(term.uri) if term.uri else None
        })
    
    # Sort terms by label
    return sorted(terms, key=lambda x: x['label'])
