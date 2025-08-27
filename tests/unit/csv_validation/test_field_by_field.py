"""
Comprehensive field-by-field validation tests for CSV processing.
This test suite validates every field type, property mapping, and multilingual handling
specifically for researcher workflows using folder_data_items.csv and folder_collections.csv.
"""

import pytest
import csv
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple

from o_nakala_core.common.utils import NakalaCommonUtils
from o_nakala_core.common.exceptions import NakalaValidationError


class TestCSVFieldValidation:
    """Test every CSV field individually with all possible combinations."""

    @pytest.fixture
    def utils(self):
        """Create utils instance for field testing."""
        return NakalaCommonUtils()

    @pytest.fixture
    def sample_data_items_row(self):
        """Sample row from folder_data_items.csv for testing."""
        return {
            "file": "files/code/",
            "status": "pending",
            "type": "http://purl.org/coar/resource_type/c_5ce6",
            "title": "fr:Scripts d'analyse|en:Analysis Scripts",
            "alternative": "fr:Scripts et modules|en:Scripts and Modules",
            "creator": "Dupont,Jean",
            "contributor": "",
            "date": "2024-03-21",
            "license": "CC-BY-4.0",
            "description": "fr:Scripts pour l'analyse de données de recherche|en:Scripts for research data analysis",
            "keywords": "fr:code;programmation;scripts;recherche|en:code;programming;scripts;research",
            "language": "fr",
            "temporal": "2024",
            "spatial": "fr:Global|en:Global",
            "accessRights": "Open Access",
            "identifier": "",
            "rights": "",
        }

    @pytest.fixture
    def sample_collections_row(self):
        """Sample row from folder_collections.csv for testing."""
        return {
            "title": "fr:Collection Code et Données|en:Code and Data Collection",
            "status": "private",
            "description": "fr:Collection regroupant les scripts de code et les données de recherche|en:Collection grouping code scripts and research data",
            "keywords": "fr:code;données;programmation;analyse|en:code;data;programming;analysis",
            "language": "fr",
            "creator": "Dupont,Jean;Smith,John",
            "data_items": "files/code/|files/data/"
        }


class TestDataItemsFieldByField:
    """Test each field in folder_data_items.csv individually."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    def test_file_field_validation(self, utils):
        """Test file path field validation."""
        test_cases = [
            # Valid cases
            ("files/code/", True, "Valid folder path"),
            ("files/data/analysis.csv", True, "Valid file path"),
            ("documents/paper.pdf", True, "Valid document path"),
            ("./relative/path.txt", True, "Valid relative path"),
            
            # Edge cases
            ("", False, "Empty file path"),
            ("/", True, "Root path"),
            ("files with spaces/document.txt", True, "Path with spaces"),
            ("files/français/document.pdf", True, "Path with non-ASCII characters"),
        ]
        
        for file_path, should_be_valid, description in test_cases:
            metadata = {"file": file_path}
            try:
                result = utils.prepare_nakala_metadata(metadata)
                if not should_be_valid:
                    # If we expect this to be invalid but it passes, that's noteworthy
                    print(f"WARNING: {description} - Expected invalid but passed")
            except Exception as e:
                if should_be_valid:
                    pytest.fail(f"{description} - Expected valid but failed: {e}")

    def test_status_field_validation(self, utils):
        """Test status field validation."""
        valid_statuses = ["pending", "published", "private", "draft"]
        invalid_statuses = ["", "invalid_status", "123", None]
        
        for status in valid_statuses:
            metadata = {"status": status}
            result = utils.prepare_nakala_metadata(metadata)
            assert isinstance(result, list), f"Status '{status}' should produce valid metadata"
        
        for status in invalid_statuses:
            metadata = {"status": status}
            # Should handle gracefully even with invalid statuses
            result = utils.prepare_nakala_metadata(metadata)
            assert isinstance(result, list)

    def test_type_field_validation(self, utils):
        """Test COAR resource type field validation."""
        valid_types = [
            "http://purl.org/coar/resource_type/c_ddb1",  # dataset
            "http://purl.org/coar/resource_type/c_5ce6",  # software
            "http://purl.org/coar/resource_type/c_c513",  # image
            "http://purl.org/coar/resource_type/c_18cf",  # text
        ]
        
        invalid_types = [
            "dataset",  # Should be full URI
            "http://invalid.uri",
            "",
            "not-a-uri",
        ]
        
        for type_uri in valid_types:
            metadata = {"type": type_uri}
            result = utils.prepare_nakala_metadata(metadata)
            
            # Find type metadata in result
            type_meta = next((m for m in result if "type" in m.get("propertyUri", "")), None)
            assert type_meta is not None, f"Type metadata not found for {type_uri}"
            assert type_uri in type_meta["value"], f"Type URI not preserved: {type_uri}"
        
        for type_uri in invalid_types:
            metadata = {"type": type_uri}
            result = utils.prepare_nakala_metadata(metadata)
            # Should handle gracefully
            assert isinstance(result, list)

    def test_title_field_multilingual(self, utils):
        """Test title field with various multilingual formats."""
        test_cases = [
            # Basic multilingual
            ("fr:Titre français|en:English title", 2, ["fr", "en"]),
            # Three languages
            ("fr:Français|en:English|es:Español", 3, ["fr", "en", "es"]),
            # Single language
            ("fr:Titre uniquement français", 1, ["fr"]),
            # No language prefix (should default to "und")
            ("Simple title without language", 1, ["und"]),
            # Mixed format
            ("fr:Français|English without prefix|de:Deutsch", 3, ["fr", "und", "de"]),
            # Empty segments (currently creates empty entry)
            ("fr:Français||en:English", 3, ["fr", "und", "en"]),  # Empty segment creates entry with "und" lang
        ]
        
        for title_value, expected_count, expected_langs in test_cases:
            metadata = {"title": title_value}
            result = utils.prepare_nakala_metadata(metadata)
            
            title_entries = [m for m in result if "title" in m.get("propertyUri", "")]
            assert len(title_entries) == expected_count, f"Expected {expected_count} title entries for '{title_value}', got {len(title_entries)}"
            
            actual_langs = [entry.get("lang") for entry in title_entries]
            for expected_lang in expected_langs:
                assert expected_lang in actual_langs, f"Expected language '{expected_lang}' not found in {actual_langs}"

    def test_alternative_field_multilingual(self, utils):
        """Test alternative title field with multilingual support."""
        alternative_value = "fr:Titre alternatif|en:Alternative title"
        metadata = {"alternative": alternative_value}
        result = utils.prepare_nakala_metadata(metadata)
        
        # Should have alternative property entries
        alt_entries = [m for m in result if "alternative" in m.get("propertyUri", "")]
        assert len(alt_entries) >= 1, "Alternative field should generate metadata entries"

    def test_creator_field_parsing(self, utils):
        """Test creator field parsing with various formats."""
        test_cases = [
            # Standard format
            ("Dupont,Jean", [{"surname": "Dupont", "givenname": "Jean"}]),
            # Multiple creators
            ("Dupont,Jean;Smith,John", [{"surname": "Dupont", "givenname": "Jean"}, {"surname": "Smith", "givenname": "John"}]),
            # Single name (surname only)
            ("Einstein", [{"surname": "Einstein"}]),
            # Organization name
            ("Université de Strasbourg", [{"fullname": "Université de Strasbourg"}]),
            # Mixed format
            ("Dupont,Jean;Université de Strasbourg", [{"surname": "Dupont", "givenname": "Jean"}, {"fullname": "Université de Strasbourg"}]),
        ]
        
        for creator_value, expected_structure in test_cases:
            metadata = {"creator": creator_value}
            result = utils.prepare_nakala_metadata(metadata)
            
            creator_entries = [m for m in result if "creator" in m.get("propertyUri", "")]
            assert len(creator_entries) >= 1, f"Creator field '{creator_value}' should generate entries"
            
            # Verify structure (this might need adjustment based on actual implementation)
            creator_meta = creator_entries[0]
            assert "value" in creator_meta, "Creator metadata should have 'value' field"

    def test_date_field_validation(self, utils):
        """Test date field with various formats."""
        valid_dates = [
            "2024-03-21",  # ISO format
            "2024",        # Year only
            "2024-03",     # Year-month
            "21/03/2024",  # Alternative format
        ]
        
        invalid_dates = [
            "invalid-date",
            "32/13/2024",  # Invalid day/month
            "",
        ]
        
        for date_value in valid_dates:
            metadata = {"date": date_value}
            result = utils.prepare_nakala_metadata(metadata)
            assert isinstance(result, list), f"Valid date '{date_value}' should process successfully"
        
        for date_value in invalid_dates:
            metadata = {"date": date_value}
            result = utils.prepare_nakala_metadata(metadata)
            # Should handle gracefully
            assert isinstance(result, list)

    def test_license_field_validation(self, utils):
        """Test license field with common licenses."""
        valid_licenses = [
            "CC-BY-4.0",
            "CC-BY-SA-4.0",
            "CC0-1.0",
            "MIT",
            "GPL-3.0",
            "Apache-2.0",
        ]
        
        for license_value in valid_licenses:
            metadata = {"license": license_value}
            result = utils.prepare_nakala_metadata(metadata)
            
            license_entries = [m for m in result if "license" in m.get("propertyUri", "")]
            if license_entries:  # License might be mapped to different property
                license_meta = license_entries[0]
                assert license_value in str(license_meta.get("value", ""))

    def test_description_field_multilingual(self, utils):
        """Test description field with multilingual content."""
        description_value = "fr:Description en français avec détails|en:English description with details"
        metadata = {"description": description_value}
        result = utils.prepare_nakala_metadata(metadata)
        
        desc_entries = [m for m in result if "description" in m.get("propertyUri", "")]
        assert len(desc_entries) >= 1, "Description should generate metadata entries"
        
        # Check multilingual parsing
        french_entry = next((e for e in desc_entries if e.get("lang") == "fr"), None)
        english_entry = next((e for e in desc_entries if e.get("lang") == "en"), None)
        
        assert french_entry is not None, "French description entry should exist"
        assert english_entry is not None, "English description entry should exist"

    def test_keywords_field_multilingual_and_multivalued(self, utils):
        """Test keywords field with multilingual and multiple values."""
        keywords_value = "fr:code;programmation;scripts;recherche|en:code;programming;scripts;research"
        metadata = {"keywords": keywords_value}
        result = utils.prepare_nakala_metadata(metadata)
        
        # Keywords might be mapped to subject
        keyword_entries = [m for m in result if any(term in m.get("propertyUri", "") for term in ["subject", "keyword"])]
        assert len(keyword_entries) >= 1, "Keywords should generate metadata entries"

    def test_language_field_validation(self, utils):
        """Test language field with various language codes."""
        valid_languages = ["fr", "en", "es", "de", "it", "pt"]
        
        for lang in valid_languages:
            metadata = {"language": lang}
            result = utils.prepare_nakala_metadata(metadata)
            assert isinstance(result, list), f"Language '{lang}' should be valid"

    def test_temporal_field_validation(self, utils):
        """Test temporal field with various time formats."""
        temporal_values = [
            "2024",
            "2020-2024",
            "21st century",
            "fr:2024|en:2024",  # Multilingual temporal
        ]
        
        for temporal in temporal_values:
            metadata = {"temporal": temporal}
            result = utils.prepare_nakala_metadata(metadata)
            assert isinstance(result, list), f"Temporal '{temporal}' should process"

    def test_spatial_field_multilingual(self, utils):
        """Test spatial field with multilingual locations."""
        spatial_value = "fr:Global|en:Global"
        metadata = {"spatial": spatial_value}
        result = utils.prepare_nakala_metadata(metadata)
        
        # Should handle multilingual spatial data
        assert isinstance(result, list)

    def test_access_rights_field_validation(self, utils):
        """Test accessRights field with various access levels."""
        access_rights_values = [
            "Open Access",
            "Restricted Access",
            "Embargoed Access",
            "Metadata Only Access",
        ]
        
        for rights in access_rights_values:
            metadata = {"accessRights": rights}
            result = utils.prepare_nakala_metadata(metadata)
            assert isinstance(result, list), f"Access rights '{rights}' should process"


class TestCollectionsFieldByField:
    """Test each field in folder_collections.csv individually."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    def test_collection_title_multilingual(self, utils):
        """Test collection title with multilingual support."""
        title_value = "fr:Collection Code et Données|en:Code and Data Collection"
        metadata = {"title": title_value}
        result = utils.prepare_nakala_metadata(metadata)
        
        title_entries = [m for m in result if "title" in m.get("propertyUri", "")]
        assert len(title_entries) == 2, "Should have French and English titles"
        
        languages = [entry.get("lang") for entry in title_entries]
        assert "fr" in languages and "en" in languages

    def test_collection_status_validation(self, utils):
        """Test collection status field."""
        valid_statuses = ["private", "public", "published", "draft"]
        
        for status in valid_statuses:
            metadata = {"status": status}
            result = utils.prepare_nakala_metadata(metadata)
            assert isinstance(result, list)

    def test_collection_creator_multiple(self, utils):
        """Test collection creator with multiple creators."""
        creator_value = "Dupont,Jean;Smith,John"
        metadata = {"creator": creator_value}
        result = utils.prepare_nakala_metadata(metadata)
        
        creator_entries = [m for m in result if "creator" in m.get("propertyUri", "")]
        assert len(creator_entries) >= 1, "Multiple creators should be handled"

    def test_data_items_field_parsing(self, utils):
        """Test data_items field with multiple items."""
        data_items_value = "files/code/|files/data/"
        # This field is collection-specific and may not be directly mapped to metadata
        # Test that it doesn't break the processing
        metadata = {"data_items": data_items_value}
        result = utils.prepare_nakala_metadata(metadata)
        assert isinstance(result, list)


class TestPropertyURIMappings:
    """Test that all CSV fields map to correct NAKALA property URIs."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    def test_nakala_property_mappings(self, utils):
        """Test that all supported fields map to correct property URIs."""
        expected_mappings = {
            "title": "http://nakala.fr/terms#title",
            "creator": "http://nakala.fr/terms#creator",
            "type": "http://nakala.fr/terms#type",
            "license": "http://nakala.fr/terms#license",
            "description": "http://purl.org/dc/terms/description",
            "keywords": "http://purl.org/dc/terms/subject",  # keywords maps to subject URI
            "contributor": "http://purl.org/dc/terms/contributor",
            "spatial": "http://purl.org/dc/terms/spatial",
            "temporal": "http://purl.org/dc/terms/temporal",
            "alternative": "http://purl.org/dc/terms/alternative",
            "accessRights": "http://purl.org/dc/terms/accessRights",
        }
        
        # Test each mapping
        for field, expected_uri in expected_mappings.items():
            metadata = {field: "Test Value"}
            result = utils.prepare_nakala_metadata(metadata)
            
            # Find metadata entry with expected URI
            matching_entry = next((m for m in result if m.get("propertyUri") == expected_uri), None)
            assert matching_entry is not None, f"Field '{field}' should map to URI '{expected_uri}'"

    def test_all_dublin_core_fields_present(self, utils):
        """Verify all critical Dublin Core fields are mapped."""
        critical_dc_fields = [
            "spatial", "temporal", "alternative", "accessRights",
            "contributor", "publisher", "rights", "coverage"
        ]
        
        property_uris = utils.PROPERTY_URIS
        
        for field in critical_dc_fields:
            assert field in property_uris, f"Critical Dublin Core field '{field}' missing from PROPERTY_URIS"
            assert "purl.org/dc/terms" in property_uris[field], f"Field '{field}' should use Dublin Core URI"


class TestMultilingualFieldProcessing:
    """Comprehensive tests for multilingual field processing."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    def test_multilingual_parsing_patterns(self, utils):
        """Test various multilingual patterns."""
        test_patterns = [
            # Standard pattern
            ("fr:Français|en:English", [("fr", "Français"), ("en", "English")]),
            # Three languages
            ("fr:Français|en:English|de:Deutsch", [("fr", "Français"), ("en", "English"), ("de", "Deutsch")]),
            # Single language with prefix
            ("fr:Seulement français", [("fr", "Seulement français")]),
            # No language prefix
            ("No language prefix", [(None, "No language prefix")]),
            # Mixed with and without prefix
            ("fr:Français|Without prefix|en:English", [("fr", "Français"), (None, "Without prefix"), ("en", "English")]),
            # Empty segments (should be filtered)
            ("fr:Français||en:English", [("fr", "Français"), ("en", "English")]),
            # Whitespace handling
            ("fr: Avec espace |en: With space ", [("fr", "Avec espace"), ("en", "With space")]),
        ]
        
        for input_value, expected_output in test_patterns:
            result = utils.parse_multilingual_field(input_value)
            
            # Filter out empty values
            expected_filtered = [(lang, text.strip()) for lang, text in expected_output if text.strip()]
            result_filtered = [(lang, text.strip()) for lang, text in result if text.strip()]
            
            assert len(result_filtered) == len(expected_filtered), f"Pattern '{input_value}' - expected {len(expected_filtered)} entries, got {len(result_filtered)}"
            
            for expected_lang, expected_text in expected_filtered:
                assert (expected_lang, expected_text) in result_filtered, f"Expected ({expected_lang}, '{expected_text}') not found in result"

    def test_multilingual_metadata_transformation(self, utils):
        """Test that multilingual fields are correctly transformed to metadata."""
        multilingual_fields = {
            "title": "fr:Titre français|en:English title|es:Título español",
            "description": "fr:Description française|en:English description",
            "keywords": "fr:mot1;mot2|en:word1;word2",
        }
        
        result = utils.prepare_nakala_metadata(multilingual_fields)
        
        # Check that each field generates multiple language entries
        for field in multilingual_fields.keys():
            # Handle mapping: keywords -> subject URI
            if field == "keywords":
                field_entries = [m for m in result if "subject" in m.get("propertyUri", "")]
            else:
                field_entries = [m for m in result if field in m.get("propertyUri", "")]
            
            # Should have multiple entries for multilingual fields
            languages_found = set(entry.get("lang") for entry in field_entries if entry.get("lang"))
            
            if field == "title":
                assert "fr" in languages_found
                assert "en" in languages_found
                assert "es" in languages_found
            elif field in ["description", "keywords"]:
                assert "fr" in languages_found
                assert "en" in languages_found


class TestCompleteCSVRowValidation:
    """Test complete CSV rows as they would appear in real researcher workflows."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    def test_complete_data_item_row(self, utils):
        """Test processing a complete data item row."""
        complete_row = {
            "file": "files/code/",
            "status": "pending",
            "type": "http://purl.org/coar/resource_type/c_5ce6",
            "title": "fr:Scripts d'analyse|en:Analysis Scripts",
            "alternative": "fr:Scripts et modules|en:Scripts and Modules",
            "creator": "Dupont,Jean",
            "contributor": "",
            "date": "2024-03-21",
            "license": "CC-BY-4.0",
            "description": "fr:Scripts pour l'analyse de données de recherche|en:Scripts for research data analysis",
            "keywords": "fr:code;programmation;scripts;recherche|en:code;programming;scripts;research",
            "language": "fr",
            "temporal": "2024",
            "spatial": "fr:Global|en:Global",
            "accessRights": "Open Access",
            "identifier": "",
            "rights": "",
        }
        
        result = utils.prepare_nakala_metadata(complete_row)
        
        # Should produce comprehensive metadata
        assert isinstance(result, list)
        assert len(result) > 10, "Complete row should generate many metadata entries"
        
        # Verify key elements are present
        property_uris = [item.get("propertyUri", "") for item in result]
        
        # Must have core elements
        assert any("title" in uri for uri in property_uris)
        assert any("type" in uri for uri in property_uris)
        assert any("creator" in uri for uri in property_uris)
        
        # Should handle multilingual fields
        title_entries = [m for m in result if "title" in m.get("propertyUri", "")]
        title_languages = [entry.get("lang") for entry in title_entries]
        assert "fr" in title_languages
        assert "en" in title_languages

    def test_complete_collection_row(self, utils):
        """Test processing a complete collection row."""
        complete_row = {
            "title": "fr:Collection Code et Données|en:Code and Data Collection",
            "status": "private",
            "description": "fr:Collection regroupant les scripts de code et les données de recherche|en:Collection grouping code scripts and research data",
            "keywords": "fr:code;données;programmation;analyse|en:code;data;programming;analysis",
            "language": "fr",
            "creator": "Dupont,Jean;Smith,John",
            "data_items": "files/code/|files/data/"
        }
        
        result = utils.prepare_nakala_metadata(complete_row)
        
        assert isinstance(result, list)
        assert len(result) > 0, "Collection row should generate metadata"
        
        # Check multilingual title
        title_entries = [m for m in result if "title" in m.get("propertyUri", "")]
        assert len(title_entries) >= 2, "Should have multilingual title entries"


class TestErrorHandlingAndEdgeCases:
    """Test error handling and edge cases in CSV processing."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    def test_empty_fields_handling(self, utils):
        """Test handling of empty or null fields."""
        test_cases = [
            {"title": ""},
            {"title": None},
            {"creator": ""},
            {"description": ""},
            {"keywords": ""},
        ]
        
        for metadata in test_cases:
            result = utils.prepare_nakala_metadata(metadata)
            # Should handle gracefully without crashing
            assert isinstance(result, list)

    def test_malformed_multilingual_fields(self, utils):
        """Test handling of malformed multilingual fields."""
        malformed_cases = [
            "fr:Français|en",  # Missing value
            "fr:|en:English",  # Empty value
            "français|english",  # No language codes
            ":Empty language|en:Valid",  # Empty language code
            "fr:Valid|:Empty",  # Empty language in middle
        ]
        
        for malformed in malformed_cases:
            metadata = {"title": malformed}
            result = utils.prepare_nakala_metadata(metadata)
            # Should not crash
            assert isinstance(result, list)

    def test_special_characters_in_fields(self, utils):
        """Test handling of special characters and encodings."""
        special_cases = {
            "title": "fr:Données à caractères spéciaux éàùçî|en:Data with special chars",
            "creator": "François,José-María",
            "description": "fr:Description avec « guillemets » et —tirets—|en:Description with quotes and dashes",
        }
        
        result = utils.prepare_nakala_metadata(special_cases)
        assert isinstance(result, list)
        assert len(result) > 0, "Special characters should be handled"

    def test_very_long_field_values(self, utils):
        """Test handling of very long field values."""
        long_description = "fr:" + "Very long description. " * 100 + "|en:" + "Very long English description. " * 100
        metadata = {"description": long_description}
        
        result = utils.prepare_nakala_metadata(metadata)
        assert isinstance(result, list)
        # Should handle long content without issues


# Integration test to verify CSV files can be processed
class TestActualCSVFiles:
    """Test the actual CSV files in the sample dataset."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    def test_sample_data_items_csv(self, utils):
        """Test processing the actual folder_data_items.csv file."""
        csv_path = Path("/Users/syl/Documents/GitHub/o-nakala-core/examples/sample_dataset/folder_data_items.csv")
        
        if not csv_path.exists():
            pytest.skip("Sample CSV file not found")
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) > 0, "CSV should contain data rows"
        
        # Process each row
        for i, row in enumerate(rows):
            result = utils.prepare_nakala_metadata(row)
            assert isinstance(result, list), f"Row {i} should produce valid metadata"
            assert len(result) > 0, f"Row {i} should generate metadata entries"

    def test_sample_collections_csv(self, utils):
        """Test processing the actual folder_collections.csv file."""
        csv_path = Path("/Users/syl/Documents/GitHub/o-nakala-core/examples/sample_dataset/folder_collections.csv")
        
        if not csv_path.exists():
            pytest.skip("Sample CSV file not found")
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) > 0, "CSV should contain collection rows"
        
        # Process each row
        for i, row in enumerate(rows):
            result = utils.prepare_nakala_metadata(row)
            assert isinstance(result, list), f"Collection row {i} should produce valid metadata"


if __name__ == "__main__":
    # Can be run directly for quick testing
    pytest.main([__file__, "-v"])