"""
Integration tests for the complete O-Nakala Core workflow.

Tests the end-to-end workflow: upload -> collection creation -> curator modifications
based on the successful workflow demonstrated in examples/workflow_documentation.
"""

import pytest
import os
import csv
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from o_nakala_core.upload import NakalaUploadClient
from o_nakala_core.collection import NakalaCollectionClient
from o_nakala_core.common.config import NakalaConfig


class TestEndToEndWorkflow:
    """Integration tests for complete workflow."""

    @pytest.fixture
    def test_config(self, temp_dataset_dir):
        """Create test configuration."""
        return NakalaConfig(
            api_key="test-key-123",
            api_url="https://apitest.nakala.fr",
            base_path=temp_dataset_dir,
            mode="folder",
        )

    @pytest.fixture
    def temp_dataset_dir(self):
        """Create temporary dataset directory structure."""
        temp_dir = tempfile.mkdtemp()

        # Create folder structure
        folders = [
            "files/code",
            "files/data",
            "files/documents",
            "files/images",
            "files/presentations",
        ]

        for folder in folders:
            folder_path = Path(temp_dir) / folder
            folder_path.mkdir(parents=True)

            # Create sample files
            if "code" in folder:
                (folder_path / "test_script.py").write_text("# Test script")
                (folder_path / "analysis.R").write_text("# R analysis")
            elif "data" in folder:
                (folder_path / "data.csv").write_text("id,value\n1,test")
            elif "documents" in folder:
                (folder_path / "paper.md").write_text("# Research Paper")
            elif "images" in folder:
                (folder_path / "image.jpg").write_bytes(b"fake image data")
            elif "presentations" in folder:
                (folder_path / "slides.md").write_text("# Presentation")

        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def folder_data_items_csv(self, temp_dataset_dir):
        """Create folder_data_items.csv for testing."""
        csv_path = Path(temp_dataset_dir) / "folder_data_items.csv"

        data = [
            [
                "file",
                "status",
                "type",
                "title",
                "alternative",
                "author",
                "contributor",
                "date",
                "license",
                "description",
                "keywords",
                "language",
                "temporal",
                "spatial",
                "accessRights",
                "identifier",
                "rights",
            ],
            [
                "files/code/",
                "pending",
                "http://purl.org/coar/resource_type/c_5ce6",
                "fr:Fichiers de code|en:Code Files",
                "",
                "Doe,John",
                "",
                "2024-01-01",
                "CC-BY-4.0",
                "fr:Scripts|en:Scripts",
                "fr:code|en:code",
                "fr",
                "2024",
                "Global",
                "Open Access",
                "",
                "test-group,ROLE_READER",
            ],
            [
                "files/data/",
                "pending",
                "http://purl.org/coar/resource_type/c_ddb1",
                "fr:Données|en:Data",
                "",
                "Doe,John",
                "",
                "2024-01-01",
                "CC-BY-4.0",
                "fr:Données test|en:Test data",
                "fr:données|en:data",
                "fr",
                "2024",
                "Global",
                "Open Access",
                "",
                "test-group,ROLE_READER",
            ],
        ]

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)

        return str(csv_path)

    @pytest.fixture
    def folder_collections_csv(self, temp_dataset_dir):
        """Create folder_collections.csv for testing."""
        csv_path = Path(temp_dataset_dir) / "folder_collections.csv"

        data = [
            [
                "title",
                "status",
                "description",
                "keywords",
                "language",
                "creator",
                "contributor",
                "publisher",
                "date",
                "rights",
                "coverage",
                "relation",
                "source",
                "data_items",
            ],
            [
                "fr:Collection Test|en:Test Collection",
                "private",
                "fr:Collection de test|en:Test collection",
                "fr:test|en:test",
                "fr",
                "Doe,John",
                "",
                "Test Org",
                "2024-01-01",
                "CC-BY-4.0",
                "Global",
                "Test relation",
                "Test source",
                "files/code/|files/data/",
            ],
        ]

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)

        return str(csv_path)

    @pytest.fixture
    def mock_api_responses(self):
        """Mock API responses for testing."""
        return {
            "upload_response": {
                "code": 201,
                "message": "Data created",
                "payload": {"id": "10.34847/nkl.test123"},
            },
            "collection_response": {
                "code": 201,
                "message": "Collection created",
                "payload": {"id": "10.34847/nkl.coll456"},
            },
            "data_item_response": {
                "identifier": "10.34847/nkl.test123",
                "metas": [
                    {
                        "propertyUri": "http://nakala.fr/terms#title",
                        "value": "Test Title",
                        "lang": "en",
                    }
                ],
            },
        }

    def test_upload_workflow(
        self, test_config, temp_dataset_dir, folder_data_items_csv, mock_api_responses
    ):
        """Test upload workflow with folder mode."""

        # Update config with temp directory
        test_config.base_path = temp_dataset_dir

        with patch("requests.Session") as mock_session:
            # Mock upload and dataset creation responses
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = mock_api_responses["upload_response"]
            mock_session.return_value.post.return_value = mock_response

            client = NakalaUploadClient(test_config)

            # Test validation mode
            client.validate_dataset(mode="folder", folder_config=folder_data_items_csv)

            # Test actual upload would work (mocked)
            assert client.file_processor is not None
            assert client.utils is not None

    def test_collection_creation_workflow(
        self, test_config, temp_dataset_dir, folder_collections_csv, mock_api_responses
    ):
        """Test collection creation from uploaded data."""

        # Create mock upload output
        upload_output_path = Path(temp_dataset_dir) / "upload_output.csv"
        upload_data = [
            ["identifier", "files", "title", "status", "response"],
            [
                "10.34847/nkl.test123",
                "test.py,hash123",
                "Code Files",
                "OK",
                json.dumps(mock_api_responses["upload_response"]),
            ],
            [
                "10.34847/nkl.test456",
                "data.csv,hash456",
                "Data Files",
                "OK",
                json.dumps(mock_api_responses["upload_response"]),
            ],
        ]

        with open(upload_output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(upload_data)

        with patch("requests.Session") as mock_session:
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = mock_api_responses["collection_response"]
            mock_session.return_value.post.return_value = mock_response

            client = NakalaCollectionClient(test_config)

            # Test loading upload output
            uploaded_items = client._load_upload_output(str(upload_output_path))
            assert len(uploaded_items) == 2
            assert uploaded_items[0]["identifier"] == "10.34847/nkl.test123"

            # Test loading folder collections
            collections_data = client._load_folder_collections(folder_collections_csv)
            assert len(collections_data) == 1
            assert (
                "fr:Collection Test|en:Test Collection" in collections_data[0]["title"]
            )

    def test_curator_modification_workflow(self, test_config, mock_api_responses):
        """Test curator batch modifications."""

        # Create temporary modifications CSV
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(["id", "action", "new_keywords", "new_relation"])
            writer.writerow(
                [
                    "10.34847/nkl.test123",
                    "modify",
                    "fr:nouveau;mot|en:new;keyword",
                    "fr:Relation test|en:Test relation",
                ]
            )
            modifications_path = f.name

        try:
            with patch("requests.get") as mock_get, patch("requests.put") as mock_put:
                # Mock GET response for retrieving current metadata
                mock_get_response = MagicMock()
                mock_get_response.status_code = 200
                mock_get_response.json.return_value = mock_api_responses[
                    "data_item_response"
                ]
                mock_get.return_value = mock_get_response

                # Mock PUT response for updating metadata
                mock_put_response = MagicMock()
                mock_put_response.status_code = 204
                mock_put.return_value = mock_put_response

                # Test loading modifications
                modifications = []
                with open(modifications_path, "r") as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        modifications.append(row)

                assert len(modifications) == 1
                assert modifications[0]["id"] == "10.34847/nkl.test123"
                assert "nouveau" in modifications[0]["new_keywords"]

        finally:
            os.unlink(modifications_path)

    def test_complete_workflow_integration(
        self,
        test_config,
        temp_dataset_dir,
        folder_data_items_csv,
        folder_collections_csv,
        mock_api_responses,
    ):
        """Test complete workflow integration."""

        # Update config
        test_config.base_path = temp_dataset_dir

        with patch("requests.Session") as mock_session:
            # Mock all API responses
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = mock_api_responses["upload_response"]
            mock_session.return_value.post.return_value = mock_response

            # Step 1: Upload
            upload_client = NakalaUploadClient(test_config)

            # Test that validation passes
            upload_client.validate_dataset(
                mode="folder", folder_config=folder_data_items_csv
            )

            # Step 2: Collections
            collection_client = NakalaCollectionClient(test_config)

            # Test collections validation would work
            collections_data = collection_client._load_folder_collections(
                folder_collections_csv
            )
            assert len(collections_data) == 1

            # Test the workflow coordination
            assert upload_client.config.api_key == collection_client.config.api_key
            assert upload_client.config.api_url == collection_client.config.api_url

    def test_error_handling_in_workflow(self, test_config, temp_dataset_dir):
        """Test error handling throughout the workflow."""

        test_config.base_path = temp_dataset_dir

        # Test with invalid CSV file
        invalid_csv = Path(temp_dataset_dir) / "invalid.csv"
        invalid_csv.write_text("invalid,csv,format")

        upload_client = NakalaUploadClient(test_config)

        # Should handle invalid CSV gracefully (logs warning, doesn't crash)
        try:
            upload_client.validate_dataset(
                mode="folder", folder_config=str(invalid_csv)
            )
            # Should complete without crashing, but with warnings
        except Exception as e:
            # If an exception is raised, it should be a meaningful one
            assert "CSV" in str(e) or "validation" in str(e)

    def test_api_key_configuration(self, temp_dataset_dir):
        """Test API key configuration and validation."""

        # Test with environment variable
        with patch.dict(os.environ, {"NAKALA_API_KEY": "env-api-key"}):
            config = NakalaConfig(base_path=temp_dataset_dir)
            assert config.api_key == "env-api-key"

        # Test with explicit API key
        config = NakalaConfig(api_key="explicit-key", base_path=temp_dataset_dir)
        assert config.api_key == "explicit-key"

        # Test that config validates paths
        assert config.validate_paths() == True

    def test_multilingual_metadata_handling(self, test_config):
        """Test handling of multilingual metadata throughout workflow."""

        upload_client = NakalaUploadClient(test_config)

        # Test multilingual field parsing
        multilingual_value = "fr:Titre français|en:English title"
        parsed = upload_client.utils.parse_multilingual_field(multilingual_value)

        assert len(parsed) == 2
        assert parsed[0] == ("fr", "Titre français")
        assert parsed[1] == ("en", "English title")

        # Test metadata preparation
        metadata_dict = {
            "title": "fr:Titre|en:Title",
            "description": "fr:Description|en:Description",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
        }

        prepared = upload_client.prepare_metadata_from_dict(metadata_dict)

        # Should have multiple metadata entries for multilingual fields
        title_entries = [m for m in prepared if "title" in m.get("propertyUri", "")]
        assert len(title_entries) == 2  # French and English

        # Type should be single entry
        type_entries = [m for m in prepared if "type" in m.get("propertyUri", "")]
        assert len(type_entries) == 1

    def test_file_validation_workflow(self, test_config, temp_dataset_dir):
        """Test file validation throughout the workflow."""

        test_config.base_path = temp_dataset_dir

        upload_client = NakalaUploadClient(test_config)

        # Test file exists
        test_file = Path(temp_dataset_dir) / "test.txt"
        test_file.write_text("test content")

        assert upload_client.file_processor.validate_file(str(test_file)) == True

        # Test file doesn't exist
        missing_file = Path(temp_dataset_dir) / "missing.txt"
        assert upload_client.file_processor.validate_file(str(missing_file)) == False

    def test_workflow_output_files(
        self, test_config, temp_dataset_dir, folder_data_items_csv, mock_api_responses
    ):
        """Test that workflow generates expected output files."""

        test_config.base_path = temp_dataset_dir
        test_config.output_path = str(Path(temp_dataset_dir) / "test_output.csv")

        with patch("requests.Session") as mock_session:
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = mock_api_responses["upload_response"]
            mock_session.return_value.post.return_value = mock_response

            upload_client = NakalaUploadClient(test_config)

            # Test that output path is configured
            assert test_config.output_path.endswith("test_output.csv")

            # Test that validation doesn't create output files
            upload_client.validate_dataset(
                mode="folder", folder_config=folder_data_items_csv
            )

            # Validation should not create output file
            assert not Path(test_config.output_path).exists()


@pytest.mark.integration
class TestRealAPIIntegration:
    """
    Integration tests that can run against real NAKALA test API.

    These tests are marked with @pytest.mark.integration and can be run separately
    with: pytest -m integration
    """

    def test_api_connection(self):
        """Test basic API connectivity."""

        # Only run if API key is available
        api_key = os.getenv("NAKALA_TEST_API_KEY")
        if not api_key:
            pytest.skip("NAKALA_TEST_API_KEY not set")

        config = NakalaConfig(
            api_key=api_key,
            api_url="https://apitest.nakala.fr",
            base_path="examples/sample_dataset",
        )

        # Test that configuration is valid
        assert config.validate() == True
        assert config.api_key == api_key
        assert config.api_url == "https://apitest.nakala.fr"

    def test_real_workflow_validation(self):
        """Test workflow validation against real test API."""

        api_key = os.getenv("NAKALA_TEST_API_KEY")
        if not api_key:
            pytest.skip("NAKALA_TEST_API_KEY not set")

        config = NakalaConfig(
            api_key=api_key,
            api_url="https://apitest.nakala.fr",
            base_path="examples/sample_dataset",
        )

        # Test upload validation
        upload_client = NakalaUploadClient(config)

        if Path("examples/sample_dataset/folder_data_items.csv").exists():
            # This should complete without errors
            upload_client.validate_dataset(
                mode="folder",
                folder_config="examples/sample_dataset/folder_data_items.csv",
            )
        else:
            pytest.skip("Sample dataset not available")
