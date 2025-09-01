"""
Comprehensive tests for common utilities
"""

import os
import tempfile
import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path

from o_nakala_core.common.utils import (
    NakalaCommonUtils,
    NakalaPathResolver,
    prepare_metadata,
    parse_multilingual_field,
)
from o_nakala_core.common.config import NakalaConfig
from o_nakala_core.common.exceptions import NakalaValidationError


class TestNakalaCommonUtils:
    """Test NakalaCommonUtils functionality."""

    @pytest.fixture
    def utils(self):
        """Create utils instance."""
        return NakalaCommonUtils()

    def test_utils_initialization(self, utils):
        """Test utils initialization."""
        assert utils is not None

    def test_prepare_nakala_metadata_basic(self, utils):
        """Test basic metadata preparation."""
        metadata_dict = {
            "title": "Test Dataset",
            "description": "A test dataset for testing",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
        }

        result = utils.prepare_nakala_metadata(metadata_dict)

        assert isinstance(result, list)
        assert len(result) >= 3

        # Check for title metadata
        title_meta = next(
            (m for m in result if "title" in m.get("propertyUri", "")), None
        )
        assert title_meta is not None
        assert title_meta["value"] == "Test Dataset"

        # Check for type metadata
        type_meta = next(
            (m for m in result if "type" in m.get("propertyUri", "")), None
        )
        assert type_meta is not None
        assert "coar" in type_meta["value"]

    def test_prepare_nakala_metadata_multilingual(self, utils):
        """Test metadata preparation with multilingual fields."""
        metadata_dict = {
            "title": "en:English Title|fr:Titre Français|es:Título Español",
            "description": "en:English description|fr:Description française",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
        }

        result = utils.prepare_nakala_metadata(metadata_dict)

        # Should have multiple entries for multilingual fields
        title_entries = [m for m in result if "title" in m.get("propertyUri", "")]
        assert len(title_entries) >= 3  # At least 3 languages

        # Check language codes
        languages = [entry.get("lang") for entry in title_entries if "lang" in entry]
        assert "en" in languages
        assert "fr" in languages
        assert "es" in languages

    def test_prepare_nakala_metadata_empty_input(self, utils):
        """Test metadata preparation with empty input."""
        result = utils.prepare_nakala_metadata({})
        assert isinstance(result, list)
        assert len(result) == 0

    def test_parse_multilingual_field_simple(self, utils):
        """Test parsing simple text field."""
        result = utils.parse_multilingual_field("Simple title")
        assert len(result) == 1
        assert result[0] == (None, "Simple title")

    def test_parse_multilingual_field_multilingual(self, utils):
        """Test parsing multilingual field."""
        multilingual = "en:English title|fr:Titre français|de:Deutscher Titel"
        result = utils.parse_multilingual_field(multilingual)

        assert len(result) == 3
        assert ("en", "English title") in result
        assert ("fr", "Titre français") in result
        assert ("de", "Deutscher Titel") in result

    def test_parse_multilingual_field_malformed(self, utils):
        """Test parsing malformed multilingual field."""
        # Missing colon
        result = utils.parse_multilingual_field("en English|fr French")
        # Should handle gracefully
        assert len(result) >= 1

    def test_parse_multilingual_field_empty(self, utils):
        """Test parsing empty field."""
        result = utils.parse_multilingual_field("")
        # Empty string returns empty list after filtering
        assert len(result) == 0


class TestNakalaPathResolver:
    """Test NakalaPathResolver functionality."""

    @pytest.fixture
    def mock_config(self):
        """Create mock configuration."""
        config = NakalaConfig(api_key="test-key")
        config.base_path = tempfile.gettempdir()
        return config

    @pytest.fixture
    def resolver(self, mock_config):
        """Create path resolver instance."""
        return NakalaPathResolver(mock_config.base_path)

    def test_resolver_initialization(self, resolver, mock_config):
        """Test resolver initialization."""
        # Path.resolve() might resolve symlinks, so compare normalized paths
        import os
        config_normalized = os.path.normpath(mock_config.base_path)
        resolver_normalized = os.path.normpath(str(resolver.base_path))
        
        # Try file comparison first, fall back to string comparison
        paths_equal = False
        try:
            paths_equal = os.path.samefile(config_normalized, resolver_normalized)
        except (OSError, ValueError):
            # If samefile fails, use string comparison
            paths_equal = (
                config_normalized in resolver_normalized
                or resolver_normalized in config_normalized
            )
        
        assert paths_equal

    def test_get_absolute_path(self, resolver):
        """Test getting absolute paths from relative."""
        rel_path = "relative/path/to/file.txt"
        result = resolver.get_absolute_path(rel_path)
        assert os.path.isabs(result)
        # Convert to normalized path components for Windows compatibility
        rel_normalized = os.path.normpath(rel_path)
        result_normalized = os.path.normpath(result)
        assert rel_normalized in result_normalized or rel_path.replace('/', os.sep) in result

    def test_get_relative_path(self, resolver):
        """Test getting relative paths."""
        # Create a path within the base directory
        test_file = resolver.base_path / "test" / "file.txt"
        result = resolver.get_relative_path(str(test_file))
        expected = "test/file.txt"
        assert expected in result or "test\\file.txt" in result  # Handle Windows paths

    def test_path_exists_check(self, resolver):
        """Test path existence checking."""
        # Test with base path (should exist)
        assert resolver.exists(".")

        # Test with non-existent path
        assert not resolver.exists("nonexistent/path/file.txt")


class TestStandaloneFunctions:
    """Test standalone utility functions."""

    def test_prepare_metadata_function(self):
        """Test standalone prepare_metadata function."""
        metadata_dict = {
            "title": "Test Function",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "description": "Testing standalone function",
        }

        result = prepare_metadata(metadata_dict)
        assert isinstance(result, list)
        assert len(result) >= 3

        # Check that it contains expected metadata
        properties = [item.get("propertyUri", "") for item in result]
        assert any("title" in prop for prop in properties)
        assert any("type" in prop for prop in properties)

    def test_parse_multilingual_field_function(self):
        """Test standalone parse_multilingual_field function."""
        # Test simple case
        result = parse_multilingual_field("Simple text")
        assert len(result) == 1
        assert result[0] == (None, "Simple text")

        # Test multilingual case
        result = parse_multilingual_field("en:Hello|fr:Bonjour|es:Hola")
        assert len(result) == 3
        assert ("en", "Hello") in result
        assert ("fr", "Bonjour") in result
        assert ("es", "Hola") in result

    def test_parse_multilingual_field_edge_cases(self):
        """Test edge cases for multilingual parsing."""
        # Empty string
        result = parse_multilingual_field("")
        assert len(result) == 0

        # Only separator
        result = parse_multilingual_field("|")
        assert len(result) == 2  # Two empty parts: (None, ''), (None, '')

        # Trailing separator
        result = parse_multilingual_field("en:English|fr:French|")
        assert len(result) >= 2
        assert ("en", "English") in result
        assert ("fr", "French") in result


class TestMetadataTransformation:
    """Test metadata transformation utilities."""

    def test_dublin_core_mapping(self):
        """Test Dublin Core metadata mapping."""
        utils = NakalaCommonUtils()

        # Test common Dublin Core fields
        metadata = {
            "title": "Test Resource",
            "creator": "Test Author",
            "subject": "Test Subject",
            "description": "Test Description",
            "publisher": "Test Publisher",
            "contributor": "Test Contributor",
            "date": "2025-01-01",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "format": "text/plain",
            "identifier": "test-id-123",
            "source": "Test Source",
            "language": "en",
            "relation": "Test Relation",
            "coverage": "Test Coverage",
            "rights": "Test Rights",
        }

        result = utils.prepare_nakala_metadata(metadata)

        # Should have entries for all provided fields
        property_uris = [item.get("propertyUri", "") for item in result]

        # Check that major Dublin Core elements are mapped
        assert any("title" in uri for uri in property_uris)
        assert any("creator" in uri for uri in property_uris)
        assert any("type" in uri for uri in property_uris)

    def test_custom_metadata_fields(self):
        """Test handling of custom metadata fields."""
        utils = NakalaCommonUtils()

        metadata = {
            "title": "Test Resource",
            "custom_field": "Custom Value",
            "nakala_specific": "Nakala Value",
        }

        result = utils.prepare_nakala_metadata(metadata)

        # Should handle custom fields gracefully
        assert isinstance(result, list)
        assert len(result) > 0

    def test_metadata_validation(self):
        """Test metadata validation."""
        utils = NakalaCommonUtils()

        # Test with required fields missing
        minimal_metadata = {"title": "Minimal Test"}

        # Should not crash with minimal metadata
        result = utils.prepare_nakala_metadata(minimal_metadata)
        assert isinstance(result, list)

        # Check that title is properly formatted
        title_meta = next(
            (m for m in result if "title" in m.get("propertyUri", "")), None
        )
        assert title_meta is not None
        assert title_meta["value"] == "Minimal Test"


class TestConfigurationIntegration:
    """Test integration with configuration system."""

    def test_utils_with_config(self):
        """Test utils integration with configuration."""
        config = NakalaConfig(api_key="test-key")
        utils = NakalaCommonUtils()

        # Test that utils can work with config
        metadata = {"title": "Config Test", "type": "dataset"}
        result = utils.prepare_nakala_metadata(metadata)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_path_resolver_integration(self):
        """Test path resolver integration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = NakalaConfig(api_key="test-key")
            config.base_path = temp_dir

            resolver = NakalaPathResolver(temp_dir)

            # Test resolving paths within the configured base
            test_path = "test/file.txt"
            resolved = resolver.get_absolute_path(test_path)

            assert os.path.isabs(resolved)
            # Use normalized paths for Windows compatibility
            temp_normalized = os.path.normpath(temp_dir)
            resolved_normalized = os.path.normpath(resolved)
            
            # Check if the temp directory is contained in the resolved path
            contains_base = temp_normalized in resolved_normalized
            
            # Fallback: check if the resolved path starts with the temp directory
            if not contains_base:
                try:
                    # Get the common path to check if they're related
                    common_path = os.path.commonpath([temp_normalized, resolved_normalized])
                    contains_base = os.path.normpath(common_path) == temp_normalized
                except (ValueError, OSError):
                    # On Windows, different drives can cause commonpath to fail
                    pass
            
            assert contains_base
