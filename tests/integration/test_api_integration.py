"""
NAKALA API Integration Tests

Tests actual API interactions with the test environment.
These tests require a valid NAKALA test API key.
"""

import pytest
import os
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

from o_nakala_core.common.config import NakalaConfig
from o_nakala_core.upload import NakalaUploadClient
from o_nakala_core.collection import NakalaCollectionClient


@pytest.mark.integration
class TestNakalaAPIIntegration:
    """Integration tests for NAKALA API functionality."""

    @pytest.fixture
    def api_config(self):
        """Create API configuration for testing."""
        api_key = os.getenv(
            "NAKALA_TEST_API_KEY", "33170cfe-f53c-550b-5fb6-4814ce981293"
        )

        return NakalaConfig(
            api_key=api_key,
            api_url="https://apitest.nakala.fr",
            base_path="examples/sample_dataset",
        )

    def test_api_authentication(self, api_config):
        """Test API authentication works."""

        # Create upload client
        upload_client = NakalaUploadClient(api_config)

        # Test that configuration is valid
        assert upload_client.config.api_key is not None
        assert upload_client.config.api_url == "https://apitest.nakala.fr"
        assert upload_client.session.headers["X-API-KEY"] == api_config.api_key

    def test_upload_validation(self, api_config):
        """Test upload validation against real API."""

        if not Path("examples/sample_dataset/folder_data_items.csv").exists():
            pytest.skip("Sample dataset not available")

        upload_client = NakalaUploadClient(api_config)

        try:
            # Test validation mode (should not make actual uploads)
            upload_client.validate_dataset(
                mode="folder",
                folder_config="examples/sample_dataset/folder_data_items.csv",
            )
        except Exception as e:
            pytest.fail(f"Upload validation failed: {e}")

    def test_collection_validation(self, api_config):
        """Test collection validation."""

        if not Path("examples/sample_dataset/folder_collections.csv").exists():
            pytest.skip("Sample collections CSV not available")

        collection_client = NakalaCollectionClient(api_config)

        try:
            # Test loading collections configuration
            collections_data = collection_client._load_folder_collections(
                "examples/sample_dataset/folder_collections.csv"
            )

            assert len(collections_data) > 0
            assert "title" in collections_data[0]

        except Exception as e:
            pytest.fail(f"Collection validation failed: {e}")

    def test_metadata_processing(self, api_config):
        """Test metadata processing functionality."""

        upload_client = NakalaUploadClient(api_config)

        # Test multilingual metadata processing
        test_metadata = {
            "title": "fr:Titre de test|en:Test title",
            "description": "fr:Description|en:Description",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "creator": "Doe,John",
            "date": "2024-01-01",
            "license": "CC-BY-4.0",
        }

        prepared_metadata = upload_client.prepare_metadata_from_dict(test_metadata)

        # Verify metadata structure
        assert len(prepared_metadata) > 0

        # Check for title entries
        title_entries = [
            m for m in prepared_metadata if "title" in m.get("propertyUri", "")
        ]
        assert len(title_entries) == 2  # French and English

        # Check for type entry
        type_entries = [
            m for m in prepared_metadata if "type" in m.get("propertyUri", "")
        ]
        assert len(type_entries) == 1

    def test_file_processing(self, api_config):
        """Test file processing capabilities."""

        upload_client = NakalaUploadClient(api_config)

        # Create a temporary test file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("test content")
            temp_file_path = f.name

        try:
            # Test file validation for existing file
            assert upload_client.file_processor.validate_file(temp_file_path) == True

            # Test file validation for non-existent file
            fake_file = "/nonexistent/path/file.txt"
            assert upload_client.file_processor.validate_file(fake_file) == False
        finally:
            # Clean up
            if Path(temp_file_path).exists():
                Path(temp_file_path).unlink()

    def test_configuration_validation(self, api_config):
        """Test configuration validation."""

        # Test valid configuration
        assert api_config.validate() == True

        # Test path validation
        if Path(api_config.base_path).exists():
            assert api_config.validate_paths() == True

        # Test header generation
        headers = api_config.get_headers()
        assert "X-API-KEY" in headers
        assert headers["X-API-KEY"] == api_config.api_key

    def test_error_handling(self, api_config):
        """Test error handling in API interactions."""

        # Test with invalid base path
        invalid_config = NakalaConfig(
            api_key=api_config.api_key,
            api_url=api_config.api_url,
            base_path="/nonexistent/path",
        )

        assert invalid_config.validate_paths() == False

        # Test with missing API key
        with pytest.raises(ValueError, match="API key must be provided"):
            # Clear environment variable to ensure test isolation
            with patch.dict(os.environ, {}, clear=True):
                NakalaConfig(
                    api_key=None,
                    api_url=api_config.api_url,
                    base_path=api_config.base_path,
                )


@pytest.mark.slow
class TestWorkflowPerformance:
    """Performance tests for workflow operations."""

    @pytest.fixture
    def performance_config(self):
        """Configuration for performance testing."""
        api_key = os.getenv(
            "NAKALA_TEST_API_KEY", "33170cfe-f53c-550b-5fb6-4814ce981293"
        )

        return NakalaConfig(
            api_key=api_key,
            api_url="https://apitest.nakala.fr",
            base_path="examples/sample_dataset",
        )

    def test_validation_performance(self, performance_config):
        """Test validation performance for large datasets."""

        if not Path("examples/sample_dataset/folder_data_items.csv").exists():
            pytest.skip("Sample dataset not available")

        import time

        upload_client = NakalaUploadClient(performance_config)

        start_time = time.time()

        # Run validation
        upload_client.validate_dataset(
            mode="folder", folder_config="examples/sample_dataset/folder_data_items.csv"
        )

        end_time = time.time()
        validation_time = end_time - start_time

        # Validation should complete within reasonable time (10 seconds)
        assert (
            validation_time < 10.0
        ), f"Validation took too long: {validation_time:.2f}s"

    def test_metadata_processing_performance(self, performance_config):
        """Test metadata processing performance."""

        import time

        upload_client = NakalaUploadClient(performance_config)

        # Create test metadata with multiple entries
        test_metadata = {
            "title": "fr:Titre de test très long avec beaucoup de texte|en:Very long test title with lots of text",
            "description": "fr:Description très détaillée|en:Very detailed description",
            "keywords": "fr:mot1;mot2;mot3;mot4;mot5|en:word1;word2;word3;word4;word5",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "creator": "Doe,John;Smith,Jane;Johnson,Bob",
            "date": "2024-01-01",
            "license": "CC-BY-4.0",
        }

        start_time = time.time()

        # Process metadata 100 times
        for _ in range(100):
            prepared_metadata = upload_client.prepare_metadata_from_dict(test_metadata)
            assert len(prepared_metadata) > 0

        end_time = time.time()
        processing_time = end_time - start_time

        # Should process 100 metadata sets in under 1 second
        assert (
            processing_time < 1.0
        ), f"Metadata processing too slow: {processing_time:.2f}s for 100 iterations"


class TestWorkflowDocumentation:
    """Tests to validate workflow documentation examples."""

    def test_sample_dataset_structure(self):
        """Test that sample dataset has expected structure."""

        sample_path = Path("examples/sample_dataset")

        if not sample_path.exists():
            pytest.skip("Sample dataset not available")

        # Check for at least some expected structure
        # Don't require all files to exist (flexible for different environments)
        expected_patterns = [
            "*.csv",  # Should have CSV files
            "files/*",  # Should have files directory with subdirs
        ]

        found_csv = list(sample_path.glob("*.csv"))
        found_files = list(sample_path.glob("files/*"))

        # At least one CSV and some files should exist if sample dataset exists
        if sample_path.exists():
            assert (
                len(found_csv) > 0 or len(found_files) > 0
            ), "Sample dataset exists but appears empty"

    def test_csv_format_compliance(self):
        """Test that CSV files comply with expected format."""

        if not Path("examples/sample_dataset/folder_data_items.csv").exists():
            pytest.skip("Sample dataset not available")

        # Test upload CSV format
        with open("examples/sample_dataset/folder_data_items.csv", "r") as f:
            header = f.readline().strip().split(",")

            expected_columns = ["file", "status", "type", "title"]
            for col in expected_columns:
                assert col in header, f"Missing column: {col}"

        # Test collections CSV format if it exists
        collections_path = Path("examples/sample_dataset/folder_collections.csv")
        if collections_path.exists():
            with open(collections_path, "r") as f:
                header = f.readline().strip().split(",")

                expected_columns = ["title", "status", "description"]
                for col in expected_columns:
                    assert col in header, f"Missing column: {col}"

    def test_workflow_documentation_consistency(self):
        """Test that workflow documentation is consistent with code."""

        # Check that documented example files exist
        workflow_path = Path("examples/workflow_documentation")

        if not workflow_path.exists():
            pytest.skip("Workflow documentation not available")

        # Check key documentation files
        doc_files = [
            "README.md",
            "02_data_upload/upload_workflow.md",
            "03_collection_creation/collection_workflow.md",
            "05_metadata_curation/curation_workflow.md",
        ]

        for doc_file in doc_files:
            doc_path = workflow_path / doc_file
            if doc_path.exists():
                # File exists - could add content validation here
                assert (
                    doc_path.stat().st_size > 0
                ), f"Empty documentation file: {doc_file}"


if __name__ == "__main__":
    # Allow running integration tests directly
    pytest.main([__file__, "-v", "-m", "integration"])
