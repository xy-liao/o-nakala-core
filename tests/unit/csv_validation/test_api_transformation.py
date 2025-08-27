"""
CSV-to-API transformation accuracy tests.
Validates that CSV fields are correctly transformed to NAKALA API-ready JSON metadata.
"""

import pytest
import json
from typing import Dict, Any, List

from o_nakala_core.common.utils import NakalaCommonUtils


class TestCSVToAPITransformation:
    """Test accurate transformation from CSV format to NAKALA API JSON format."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    def test_simple_field_transformation(self, utils):
        """Test transformation of simple fields to API format."""
        csv_data = {
            "title": "Test Dataset",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "creator": "Dupont,Jean"
        }
        
        result = utils.prepare_nakala_metadata(csv_data)
        
        # Verify API structure
        assert isinstance(result, list), "Result should be a list of metadata objects"
        
        for item in result:
            # Each metadata item should have required API fields
            assert "propertyUri" in item, "Each metadata item must have propertyUri"
            assert "value" in item, "Each metadata item must have value"
            # Note: typeUri is not present for all field types (e.g., creator fields)

    def test_multilingual_field_transformation(self, utils):
        """Test that multilingual CSV fields transform correctly to API format."""
        csv_data = {
            "title": "fr:Titre français|en:English title",
            "description": "fr:Description en français|en:English description"
        }
        
        result = utils.prepare_nakala_metadata(csv_data)
        
        # Find title entries
        title_entries = [m for m in result if "title" in m.get("propertyUri", "")]
        assert len(title_entries) == 2, "Should have 2 title entries (French and English)"
        
        # Verify French entry
        french_title = next((e for e in title_entries if e.get("lang") == "fr"), None)
        assert french_title is not None, "French title entry should exist"
        assert french_title["value"] == "Titre français", "French title value should be correct"
        assert french_title["lang"] == "fr", "French entry should have lang='fr'"
        
        # Verify English entry
        english_title = next((e for e in title_entries if e.get("lang") == "en"), None)
        assert english_title is not None, "English title entry should exist"
        assert english_title["value"] == "English title", "English title value should be correct"
        assert english_title["lang"] == "en", "English entry should have lang='en'"

    def test_creator_field_transformation(self, utils):
        """Test that creator fields transform to correct API format."""
        test_cases = [
            # Single creator with surname, firstname
            ("Dupont,Jean", "Jean Dupont should be parsed correctly"),
            # Multiple creators
            ("Dupont,Jean;Smith,John", "Multiple creators should be parsed"),
            # Organization name
            ("Université de Strasbourg", "Organization names should be handled"),
        ]
        
        for creator_value, description in test_cases:
            csv_data = {"creator": creator_value}
            result = utils.prepare_nakala_metadata(csv_data)
            
            creator_entries = [m for m in result if "creator" in m.get("propertyUri", "")]
            assert len(creator_entries) >= 1, f"{description} - should generate creator entries"
            
            creator_entry = creator_entries[0]
            assert "value" in creator_entry, f"{description} - creator should have value field"

    def test_keywords_multivalued_transformation(self, utils):
        """Test that semicolon-separated keywords transform correctly."""
        csv_data = {
            "keywords": "fr:mot1;mot2;mot3|en:word1;word2;word3"
        }
        
        result = utils.prepare_nakala_metadata(csv_data)
        
        # Keywords are likely mapped to subject
        keyword_entries = [m for m in result if any(term in m.get("propertyUri", "") for term in ["subject", "keyword"])]
        assert len(keyword_entries) >= 1, "Keywords should generate subject/keyword entries"

    def test_coar_type_preservation(self, utils):
        """Test that COAR resource type URIs are preserved correctly."""
        coar_types = [
            "http://purl.org/coar/resource_type/c_ddb1",  # dataset
            "http://purl.org/coar/resource_type/c_5ce6",  # software
            "http://purl.org/coar/resource_type/c_c513",  # image
            "http://purl.org/coar/resource_type/c_18cf",  # text
        ]
        
        for coar_type in coar_types:
            csv_data = {"type": coar_type}
            result = utils.prepare_nakala_metadata(csv_data)
            
            type_entries = [m for m in result if "type" in m.get("propertyUri", "")]
            assert len(type_entries) >= 1, f"Type {coar_type} should generate entries"
            
            type_entry = type_entries[0]
            assert coar_type in str(type_entry.get("value", "")), f"COAR type {coar_type} should be preserved"

    def test_dublin_core_field_mapping(self, utils):
        """Test that Dublin Core fields map to correct property URIs."""
        dublin_core_fields = {
            "spatial": "test spatial value",
            "temporal": "test temporal value", 
            "alternative": "test alternative title",
            "accessRights": "Open Access",
            "contributor": "Test Contributor",
        }
        
        result = utils.prepare_nakala_metadata(dublin_core_fields)
        
        # Verify each Dublin Core field generates appropriate metadata
        for field, value in dublin_core_fields.items():
            matching_entries = [m for m in result if field.lower() in m.get("propertyUri", "").lower()]
            assert len(matching_entries) >= 1, f"Dublin Core field '{field}' should generate metadata entries"

    def test_api_json_structure_validity(self, utils):
        """Test that generated metadata has valid JSON structure for API."""
        csv_data = {
            "title": "fr:Jeu de données test|en:Test dataset",
            "creator": "Dupont,Jean;Smith,John",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "description": "fr:Description du jeu de données|en:Dataset description",
            "license": "CC-BY-4.0",
            "date": "2024-03-21",
            "language": "fr",
        }
        
        result = utils.prepare_nakala_metadata(csv_data)
        
        # Test JSON serialization (should not fail)
        json_str = json.dumps(result, ensure_ascii=False)
        assert len(json_str) > 0, "Should be able to serialize to JSON"
        
        # Test JSON deserialization
        parsed_back = json.loads(json_str)
        assert parsed_back == result, "Should deserialize back to original structure"

    def test_empty_field_handling(self, utils):
        """Test that empty CSV fields don't break API transformation."""
        csv_data = {
            "title": "Valid Title",
            "creator": "",  # Empty
            "description": "",  # Empty
            "contributor": "",  # Empty
            "rights": "",  # Empty
        }
        
        result = utils.prepare_nakala_metadata(csv_data)
        
        # Should still generate valid metadata
        assert isinstance(result, list)
        
        # Should at least have title
        title_entries = [m for m in result if "title" in m.get("propertyUri", "")]
        assert len(title_entries) >= 1, "Should still have title metadata"

    def test_field_order_independence(self, utils):
        """Test that field order in CSV doesn't affect API transformation."""
        csv_data_1 = {
            "title": "Test Dataset",
            "creator": "Dupont,Jean",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
        }
        
        csv_data_2 = {
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "creator": "Dupont,Jean",
            "title": "Test Dataset",
        }
        
        result_1 = utils.prepare_nakala_metadata(csv_data_1)
        result_2 = utils.prepare_nakala_metadata(csv_data_2)
        
        # Should have same number of metadata entries
        assert len(result_1) == len(result_2), "Field order shouldn't affect result count"
        
        # Should contain same property URIs
        uris_1 = set(m.get("propertyUri") for m in result_1)
        uris_2 = set(m.get("propertyUri") for m in result_2)
        assert uris_1 == uris_2, "Field order shouldn't affect property URIs generated"


class TestAPIMetadataStructure:
    """Test the structure of generated API metadata."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    def test_required_metadata_fields(self, utils):
        """Test that all metadata entries have required fields for NAKALA API."""
        csv_data = {
            "title": "Test Resource",
            "type": "http://purl.org/coar/resource_type/c_ddb1"
        }
        
        result = utils.prepare_nakala_metadata(csv_data)
        
        required_fields = ["propertyUri", "value"]
        
        for item in result:
            for field in required_fields:
                assert field in item, f"Metadata item missing required field: {field}"
                assert item[field] is not None, f"Required field '{field}' should not be None"
            
            # typeUri is optional for some field types
            if "typeUri" in item:
                assert item["typeUri"] is not None, "typeUri should not be None if present"

    def test_optional_metadata_fields(self, utils):
        """Test handling of optional metadata fields like lang."""
        csv_data = {
            "title": "fr:Titre français|en:English title"
        }
        
        result = utils.prepare_nakala_metadata(csv_data)
        title_entries = [m for m in result if "title" in m.get("propertyUri", "")]
        
        # Should have lang field for multilingual entries
        for entry in title_entries:
            if "lang" in entry:
                assert isinstance(entry["lang"], str), "Lang field should be string"
                assert len(entry["lang"]) >= 2, "Language code should be meaningful"

    def test_metadata_value_types(self, utils):
        """Test that metadata values have correct types."""
        csv_data = {
            "title": "String Title",
            "creator": "Dupont,Jean",
            "date": "2024-03-21",
        }
        
        result = utils.prepare_nakala_metadata(csv_data)
        
        for item in result:
            value = item.get("value")
            # Value can be string, list, or dict depending on the field
            assert value is not None, "Value should not be None"
            assert isinstance(value, (str, list, dict)), "Value should be string, list, or dict"

    def test_property_uri_validity(self, utils):
        """Test that all property URIs are valid HTTP URIs."""
        csv_data = {
            "title": "Test",
            "creator": "Test Creator",
            "description": "Test Description",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
        }
        
        result = utils.prepare_nakala_metadata(csv_data)
        
        for item in result:
            property_uri = item.get("propertyUri", "")
            assert property_uri.startswith("http://"), f"Property URI should be HTTP URL: {property_uri}"
            assert len(property_uri) > 10, f"Property URI should be meaningful: {property_uri}"


class TestTransformationConsistency:
    """Test consistency of transformations across multiple runs."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    def test_transformation_deterministic(self, utils):
        """Test that same input produces same output consistently."""
        csv_data = {
            "title": "fr:Titre|en:Title",
            "creator": "Dupont,Jean",
            "type": "http://purl.org/coar/resource_type/c_ddb1"
        }
        
        # Run transformation multiple times
        results = [utils.prepare_nakala_metadata(csv_data) for _ in range(5)]
        
        # All results should be identical
        first_result = results[0]
        for i, result in enumerate(results[1:], 1):
            assert len(result) == len(first_result), f"Run {i} has different number of items"
            
            # Compare each metadata item
            for j, (item1, item2) in enumerate(zip(first_result, result)):
                assert item1.get("propertyUri") == item2.get("propertyUri"), f"Run {i}, item {j}: propertyUri differs"
                assert item1.get("value") == item2.get("value"), f"Run {i}, item {j}: value differs"

    def test_batch_processing_consistency(self, utils):
        """Test that batch processing multiple rows gives consistent results."""
        csv_rows = [
            {"title": "Dataset 1", "creator": "Author 1"},
            {"title": "Dataset 2", "creator": "Author 2"},
            {"title": "Dataset 3", "creator": "Author 3"},
        ]
        
        # Process individually
        individual_results = [utils.prepare_nakala_metadata(row) for row in csv_rows]
        
        # Each should have consistent structure
        for i, result in enumerate(individual_results):
            assert isinstance(result, list), f"Row {i} should produce list"
            assert len(result) > 0, f"Row {i} should have metadata entries"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])