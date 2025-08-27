"""
Researcher workflow validation tests.
Tests the complete workflow from CSV creation to NAKALA API submission,
simulating how researchers will actually use the system.
"""

import pytest
import csv
import tempfile
import json
from pathlib import Path
from typing import Dict, List, Any

from o_nakala_core.common.utils import NakalaCommonUtils


class TestResearcherWorkflowValidation:
    """Test complete researcher workflows from CSV to API."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    @pytest.fixture
    def sample_researcher_dataset(self):
        """Create a realistic dataset that a researcher might have."""
        return [
            {
                "file": "code/analysis_script.py",
                "status": "pending",
                "type": "http://purl.org/coar/resource_type/c_5ce6",
                "title": "fr:Script d'analyse des données|en:Data analysis script",
                "description": "fr:Script Python pour analyser les données de l'enquête|en:Python script to analyze survey data",
                "creator": "Martin,Sophie",
                "keywords": "fr:python;analyse;données|en:python;analysis;data",
                "language": "fr",
                "license": "CC-BY-4.0",
                "date": "2024-03-15",
            },
            {
                "file": "data/survey_results.csv",
                "status": "pending", 
                "type": "http://purl.org/coar/resource_type/c_ddb1",
                "title": "fr:Résultats d'enquête 2024|en:Survey results 2024",
                "description": "fr:Données brutes de l'enquête sociologique|en:Raw sociological survey data",
                "creator": "Martin,Sophie;Dubois,Pierre",
                "keywords": "fr:enquête;sociologie;données brutes|en:survey;sociology;raw data",
                "language": "fr",
                "license": "CC-BY-NC-4.0",
                "date": "2024-03-10",
            },
            {
                "file": "documents/methodology.pdf",
                "status": "pending",
                "type": "http://purl.org/coar/resource_type/c_18cf",
                "title": "fr:Méthodologie de recherche|en:Research methodology",
                "description": "fr:Document détaillant la méthodologie utilisée|en:Document detailing the methodology used",
                "creator": "Martin,Sophie",
                "keywords": "fr:méthodologie;recherche;sociologie|en:methodology;research;sociology",
                "language": "fr",
                "license": "CC-BY-4.0",
                "date": "2024-02-28",
            }
        ]

    @pytest.fixture
    def sample_researcher_collections(self):
        """Create realistic collections that a researcher might organize."""
        return [
            {
                "title": "fr:Enquête Sociologique 2024|en:Sociological Survey 2024",
                "status": "private",
                "description": "fr:Collection complète de l'enquête sociologique menée en 2024|en:Complete collection of the sociological survey conducted in 2024",
                "keywords": "fr:enquête;sociologie;2024;données|en:survey;sociology;2024;data",
                "language": "fr",
                "creator": "Martin,Sophie;Dubois,Pierre",
                "data_items": "code/analysis_script.py|data/survey_results.csv|documents/methodology.pdf"
            }
        ]

    def test_complete_data_items_workflow(self, utils, sample_researcher_dataset):
        """Test processing complete data items as a researcher would."""
        successful_conversions = 0
        total_metadata_entries = 0
        
        for i, data_item in enumerate(sample_researcher_dataset):
            # Convert CSV row to API metadata
            api_metadata = utils.prepare_nakala_metadata(data_item)
            
            # Validate conversion success
            assert isinstance(api_metadata, list), f"Data item {i} should produce list of metadata"
            assert len(api_metadata) > 0, f"Data item {i} should generate metadata entries"
            
            # Validate API structure
            for meta_item in api_metadata:
                assert "propertyUri" in meta_item, f"Data item {i} metadata missing propertyUri"
                assert "value" in meta_item, f"Data item {i} metadata missing value"
                # Note: typeUri is not always present (e.g., creator fields don't have it)
                # This is correct behavior for certain field types
                
                # Count successful entries
                total_metadata_entries += 1
            
            successful_conversions += 1
        
        # Validate overall success
        assert successful_conversions == len(sample_researcher_dataset), "All data items should convert successfully"
        assert total_metadata_entries >= len(sample_researcher_dataset) * 3, "Should generate substantial metadata"
        
        print(f"✅ Processed {successful_conversions} data items generating {total_metadata_entries} metadata entries")

    def test_complete_collections_workflow(self, utils, sample_researcher_collections):
        """Test processing complete collections as a researcher would."""
        for i, collection in enumerate(sample_researcher_collections):
            # Convert collection to API metadata
            api_metadata = utils.prepare_nakala_metadata(collection)
            
            # Validate conversion success
            assert isinstance(api_metadata, list), f"Collection {i} should produce list of metadata"
            assert len(api_metadata) > 0, f"Collection {i} should generate metadata entries"
            
            # Validate multilingual fields are handled
            title_entries = [m for m in api_metadata if "title" in m.get("propertyUri", "")]
            assert len(title_entries) >= 2, "Collection title should be multilingual"
            
            # Check for French and English
            languages = [entry.get("lang") for entry in title_entries]
            assert "fr" in languages, "Should have French title"
            assert "en" in languages, "Should have English title"

    def test_mixed_language_handling(self, utils):
        """Test handling of mixed language content as researchers might create."""
        mixed_language_data = {
            "title": "fr:Étude sur les réseaux sociaux|en:Study on social networks|es:Estudio sobre redes sociales",
            "description": "fr:Analyse des comportements sur les réseaux sociaux|en:Analysis of social media behaviors",
            "keywords": "fr:réseaux sociaux;comportement;analyse|en:social networks;behavior;analysis",
            "creator": "García,María;Müller,Hans;Smith,John",
            "type": "http://purl.org/coar/resource_type/c_ddb1"
        }
        
        result = utils.prepare_nakala_metadata(mixed_language_data)
        
        # Should handle multiple languages smoothly
        title_entries = [m for m in result if "title" in m.get("propertyUri", "")]
        assert len(title_entries) == 3, "Should have 3 language versions of title"
        
        # Check all languages are present
        languages = [entry.get("lang") for entry in title_entries]
        assert "fr" in languages
        assert "en" in languages  
        assert "es" in languages

    def test_incomplete_metadata_handling(self, utils):
        """Test how system handles incomplete metadata as researchers might provide."""
        incomplete_data_cases = [
            # Minimal metadata
            {"title": "Minimal Dataset", "type": "http://purl.org/coar/resource_type/c_ddb1"},
            # Missing type (common mistake)
            {"title": "Dataset without type", "creator": "Smith,John"},
            # Only title
            {"title": "Just a title"},
            # Empty optional fields
            {"title": "Test", "description": "", "keywords": "", "creator": "Smith,John"},
        ]
        
        for i, incomplete_data in enumerate(incomplete_data_cases):
            # Should handle gracefully without crashing
            result = utils.prepare_nakala_metadata(incomplete_data)
            assert isinstance(result, list), f"Incomplete case {i} should still produce list"
            
            # Should at least have some metadata if title is present
            if "title" in incomplete_data and incomplete_data["title"]:
                assert len(result) > 0, f"Case {i} with title should generate some metadata"

    def test_researcher_error_scenarios(self, utils):
        """Test common errors researchers might make in CSV files."""
        error_scenarios = [
            # Malformed multilingual field
            {"title": "fr:Français|en"},  # Missing English text
            # Invalid COAR type
            {"title": "Test", "type": "not-a-valid-uri"},
            # Malformed creator
            {"title": "Test", "creator": "Just a name without comma"},
            # Very long field values
            {"title": "Very " * 100 + " long title"},
        ]
        
        for i, error_case in enumerate(error_scenarios):
            # Should handle errors gracefully
            try:
                result = utils.prepare_nakala_metadata(error_case)
                assert isinstance(result, list), f"Error case {i} should not crash"
            except Exception as e:
                # If it does raise an exception, it should be informative
                assert len(str(e)) > 10, f"Error case {i} should have meaningful error message"

    def test_batch_processing_simulation(self, utils, sample_researcher_dataset):
        """Simulate batch processing of multiple files as a researcher would do."""
        batch_results = []
        
        # Process each item
        for data_item in sample_researcher_dataset:
            metadata = utils.prepare_nakala_metadata(data_item)
            batch_results.append({
                "source": data_item,
                "metadata": metadata,
                "success": len(metadata) > 0
            })
        
        # Validate batch processing
        successful_items = [r for r in batch_results if r["success"]]
        assert len(successful_items) == len(sample_researcher_dataset), "All items should process successfully in batch"
        
        # Validate consistency across batch
        for result in batch_results:
            metadata = result["metadata"]
            # Each should have proper structure
            for meta_item in metadata:
                assert "propertyUri" in meta_item
                assert "value" in meta_item
                # typeUri is optional for some field types like creator

    def test_api_ready_json_output(self, utils, sample_researcher_dataset):
        """Test that output is ready for NAKALA API consumption."""
        for data_item in sample_researcher_dataset:
            metadata = utils.prepare_nakala_metadata(data_item)
            
            # Should be JSON serializable
            json_str = json.dumps(metadata, ensure_ascii=False)
            assert len(json_str) > 0, "Should serialize to JSON"
            
            # Should deserialize correctly
            parsed_back = json.loads(json_str)
            assert parsed_back == metadata, "Should round-trip through JSON"
            
            # Validate API structure
            for meta_item in metadata:
                # Required fields for NAKALA API
                assert isinstance(meta_item.get("propertyUri"), str)
                assert meta_item.get("value") is not None
                # typeUri is optional for some field types like creator
                
                # Optional fields should be correct types if present
                if "lang" in meta_item:
                    assert isinstance(meta_item["lang"], str)

    def test_field_validation_edge_cases(self, utils):
        """Test edge cases in field validation that researchers might encounter."""
        edge_cases = [
            # Unicode characters
            {"title": "fr:Données avec accents éàùçî|en:Data with unicode ñáéí"},
            # Special characters
            {"description": "Contains « quotes » and —dashes— and [brackets]"},
            # Numbers in text fields
            {"keywords": "fr:année 2024;étude 123|en:year 2024;study 123"},
            # Mixed separators (semicolon and comma)
            {"creator": "Dupont,Jean;Martin;Smith,John"},
            # Very short fields
            {"title": "A", "description": "B"},
            # Whitespace handling
            {"title": "  fr: Titre avec espaces  |  en: Title with spaces  "},
        ]
        
        for i, edge_case in enumerate(edge_cases):
            try:
                result = utils.prepare_nakala_metadata(edge_case)
                assert isinstance(result, list), f"Edge case {i} should produce list"
                
                # Should handle Unicode and special characters
                if result:
                    json.dumps(result, ensure_ascii=False)  # Should not fail
                    
            except Exception as e:
                pytest.fail(f"Edge case {i} should not crash: {e}")


class TestResearcherCSVCreationGuidance:
    """Test guidance and validation for researchers creating CSV files."""

    @pytest.fixture
    def utils(self):
        return NakalaCommonUtils()

    def test_required_vs_optional_fields(self, utils):
        """Test what fields are truly required vs optional."""
        # Minimal required set
        minimal_valid = {"title": "Minimal Dataset"}
        result = utils.prepare_nakala_metadata(minimal_valid)
        assert len(result) > 0, "Minimal valid data should work"
        
        # Recommended set for good metadata
        recommended = {
            "title": "fr:Jeu de données recommandé|en:Recommended dataset",
            "description": "fr:Description complète|en:Complete description", 
            "creator": "Researcher,Jane",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "license": "CC-BY-4.0",
            "keywords": "fr:recherche;données|en:research;data"
        }
        result = utils.prepare_nakala_metadata(recommended)
        assert len(result) >= 6, "Recommended set should generate comprehensive metadata"

    def test_multilingual_field_patterns(self, utils):
        """Test different multilingual patterns researchers might use."""
        patterns = [
            # Standard pattern
            "fr:Texte français|en:English text",
            # Three languages
            "fr:Français|en:English|de:Deutsch", 
            # Single language
            "fr:Seulement en français",
            # No language codes
            "Plain text without language codes",
            # Mixed
            "fr:Français|Plain English|de:Deutsch",
        ]
        
        for pattern in patterns:
            metadata = {"title": pattern}
            result = utils.prepare_nakala_metadata(metadata)
            assert len(result) > 0, f"Pattern '{pattern}' should work"

    def test_creator_field_patterns(self, utils):
        """Test different creator field patterns researchers might use."""
        creator_patterns = [
            # Standard academic format
            "Dupont,Jean",
            # Multiple creators
            "Dupont,Jean;Martin,Sophie",
            # Organization
            "Université de Strasbourg",
            # Mixed
            "Dupont,Jean;Université de Strasbourg;Smith,John",
            # With spaces
            "Van Der Berg,Jan;De La Cruz,Maria",
        ]
        
        for pattern in creator_patterns:
            metadata = {"creator": pattern}
            result = utils.prepare_nakala_metadata(metadata)
            creator_entries = [m for m in result if "creator" in m.get("propertyUri", "")]
            assert len(creator_entries) > 0, f"Creator pattern '{pattern}' should generate entries"


class TestCSVFileProcessing:
    """Test processing actual CSV files as researchers would create them."""

    def test_create_and_process_temporary_csv(self):
        """Test creating and processing a CSV file like a researcher would."""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'file', 'title', 'creator', 'description', 'type', 'keywords', 'license'
            ])
            
            # Write data rows
            writer.writerow([
                'data/results.csv',
                'fr:Résultats de recherche|en:Research results',
                'Dupont,Jean',
                'fr:Données de l\'expérience|en:Experiment data',
                'http://purl.org/coar/resource_type/c_ddb1',
                'fr:expérience;données|en:experiment;data',
                'CC-BY-4.0'
            ])
            
            writer.writerow([
                'code/analysis.py',
                'fr:Script d\'analyse|en:Analysis script',
                'Dupont,Jean;Martin,Sophie',
                'fr:Code pour analyser les résultats|en:Code to analyze results',
                'http://purl.org/coar/resource_type/c_5ce6',
                'fr:python;analyse|en:python;analysis',
                'MIT'
            ])
            
            csv_path = f.name
        
        try:
            # Read and process the CSV
            utils = NakalaCommonUtils()
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            assert len(rows) == 2, "Should have 2 data rows"
            
            # Process each row
            for i, row in enumerate(rows):
                metadata = utils.prepare_nakala_metadata(row)
                assert len(metadata) > 0, f"Row {i} should generate metadata"
                
                # Validate multilingual titles are handled
                title_entries = [m for m in metadata if "title" in m.get("propertyUri", "")]
                assert len(title_entries) >= 2, f"Row {i} should have multilingual titles"
                
        finally:
            # Cleanup
            Path(csv_path).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])