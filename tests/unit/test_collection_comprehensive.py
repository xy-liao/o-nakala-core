"""
Comprehensive tests for Nakala Collection functionality
"""

import os
import tempfile
import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from o_nakala_core.collection import NakalaCollectionClient, CollectionResult
from o_nakala_core.common.config import NakalaConfig
from o_nakala_core.common.exceptions import (
    NakalaAPIError,
    NakalaValidationError,
    NakalaFileError,
)


class TestNakalaCollectionClient:
    """Test collection client functionality."""

    @pytest.fixture
    def mock_config(self):
        """Create mock configuration."""
        api_key = os.environ.get("NAKALA_API_KEY", "test-key")
        config = NakalaConfig(api_key=api_key)
        config.base_url = "https://apitest.nakala.fr"
        return config

    @pytest.fixture
    def collection_client(self, mock_config):
        """Create collection client instance."""
        return NakalaCollectionClient(mock_config)

    def test_client_initialization(self, collection_client, mock_config):
        """Test client initialization."""
        assert collection_client.config == mock_config
        assert collection_client.session is not None
        assert collection_client.utils is not None

    def test_validate_collection_config_success(self, collection_client):
        """Test successful collection configuration validation."""
        config = {
            "title": "Test Collection",
            "description": "A test collection",
            "data_ids": ["data-1", "data-2", "data-3"],
        }

        # Should not raise exception
        collection_client._validate_collection_config(config)

    def test_validate_collection_config_missing_title(self, collection_client):
        """Test validation with missing title."""
        config = {"description": "A test collection", "data_ids": ["data-1", "data-2"]}

        with pytest.raises(NakalaValidationError, match="title"):
            collection_client._validate_collection_config(config)

    def test_validate_collection_config_missing_data_ids(self, collection_client):
        """Test validation with missing data_ids."""
        config = {"title": "Test Collection", "description": "A test collection"}

        with pytest.raises(
            NakalaValidationError,
            match="Either 'data_ids' or 'upload_data' must be provided",
        ):
            collection_client._validate_collection_config(config)

    def test_validate_collection_config_with_upload_data(self, collection_client):
        """Test validation with upload_data instead of data_ids."""
        config = {"title": "Test Collection", "upload_data": [{"identifier": "data-1"}]}

        # Should not raise exception
        collection_client._validate_collection_config(config)

    def test_create_collection_success(self, collection_client):
        """Test successful collection creation."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"identifier": "test-collection-id"}

        with patch.object(
            collection_client.session, "post", return_value=mock_response
        ) as mock_post:
            metadata = [
                {
                    "propertyUri": "http://nakala.fr/terms#title",
                    "value": "Test Collection",
                    "lang": "en",
                }
            ]
            data_ids = ["data-1", "data-2", "data-3"]

            result = collection_client._create_collection(metadata, data_ids)
            assert result == "test-collection-id"
            mock_post.assert_called_once()

            # Verify request structure
            call_args = mock_post.call_args
            assert "json" in call_args.kwargs
            request_data = call_args.kwargs["json"]
            assert "metas" in request_data
            assert "datas" in request_data

    def test_create_collection_api_error(self, collection_client):
        """Test collection creation API error handling."""
        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.text = "Validation failed"
        mock_response.json.return_value = {"errors": ["Invalid collection data"]}

        with patch.object(
            collection_client.session, "post", return_value=mock_response
        ):
            metadata = [{"propertyUri": "invalid", "value": "test"}]
            data_ids = ["data-1"]

            with pytest.raises(NakalaAPIError):
                collection_client._create_collection(metadata, data_ids)

    def test_create_single_collection_success(self, collection_client):
        """Test single collection creation workflow."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"identifier": "collection-123"}

        with patch.object(
            collection_client.session, "post", return_value=mock_response
        ):
            config = {
                "title": "Test Collection",
                "description": "A test collection for unit testing",
                "data_ids": ["data-1", "data-2", "data-3"],
            }

            result = collection_client.create_single_collection(config)
            assert result == "collection-123"

    def test_process_upload_output_csv(self, collection_client):
        """Test processing upload output CSV file."""
        csv_content = """title,identifier,status,collection
Dataset 1,data-1,success,Research Collection
Dataset 2,data-2,success,Research Collection
Dataset 3,data-3,success,Archive Collection
Dataset 4,data-4,failed,Research Collection"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            result = collection_client._process_upload_output_csv(tmp_path)
            assert len(result) == 4
            assert result[0]["identifier"] == "data-1"
            assert result[0]["status"] == "success"
            assert result[0]["collection"] == "Research Collection"
            assert result[3]["status"] == "failed"
        finally:
            os.unlink(tmp_path)

    def test_process_upload_output_csv_file_not_found(self, collection_client):
        """Test processing non-existent CSV file."""
        with pytest.raises(NakalaFileError):
            collection_client._process_upload_output_csv("/nonexistent/file.csv")

    def test_group_data_by_collection(self, collection_client):
        """Test grouping data items by collection name."""
        upload_data = [
            {
                "identifier": "data-1",
                "title": "Dataset 1",
                "collection": "Research Collection",
            },
            {
                "identifier": "data-2",
                "title": "Dataset 2",
                "collection": "Research Collection",
            },
            {
                "identifier": "data-3",
                "title": "Dataset 3",
                "collection": "Archive Collection",
            },
            {
                "identifier": "data-4",
                "title": "Dataset 4",
                "collection": "Research Collection",
            },
            {
                "identifier": "data-5",
                "title": "Dataset 5",
                "collection": "Archive Collection",
            },
        ]

        result = collection_client._group_data_by_collection(upload_data)

        assert "Research Collection" in result
        assert "Archive Collection" in result
        assert len(result["Research Collection"]) == 3
        assert len(result["Archive Collection"]) == 2

        # Check specific items
        research_ids = [item["identifier"] for item in result["Research Collection"]]
        assert "data-1" in research_ids
        assert "data-2" in research_ids
        assert "data-4" in research_ids

        archive_ids = [item["identifier"] for item in result["Archive Collection"]]
        assert "data-3" in archive_ids
        assert "data-5" in archive_ids

    def test_group_data_by_collection_empty_input(self, collection_client):
        """Test grouping with empty input."""
        result = collection_client._group_data_by_collection([])
        assert result == {}

    def test_group_data_by_collection_missing_collection_field(self, collection_client):
        """Test grouping with missing collection field."""
        upload_data = [
            {"identifier": "data-1", "title": "Dataset 1"},
            {
                "identifier": "data-2",
                "title": "Dataset 2",
                "collection": "Test Collection",
            },
        ]

        # Should handle gracefully
        result = collection_client._group_data_by_collection(upload_data)
        assert "Test Collection" in result
        assert len(result["Test Collection"]) == 1


class TestCollectionResult:
    """Test CollectionResult TypedDict."""

    def test_collection_result_creation(self):
        """Test creating CollectionResult instance."""
        result: CollectionResult = {
            "id": "test-123",
            "title": "Test Collection",
            "status": "success",
            "data_count": 5,
            "data_ids": ["data-1", "data-2"],
            "creation_status": "completed",
            "error": "",
        }

        assert result["id"] == "test-123"
        assert result["title"] == "Test Collection"
        assert result["status"] == "success"
        assert result["data_count"] == 5
        assert len(result["data_ids"]) == 2

    def test_collection_result_with_errors(self):
        """Test CollectionResult with errors."""
        result: CollectionResult = {
            "id": "test-456",
            "title": "Failed Collection",
            "status": "failed",
            "data_count": 0,
            "data_ids": [],
            "creation_status": "failed",
            "error": "Invalid collection data",
        }

        assert result["status"] == "failed"
        assert result["error"] == "Invalid collection data"
        assert len(result["data_ids"]) == 0


class TestCollectionIntegration:
    """Integration tests for collection functionality."""

    def test_complete_collection_workflow_mocked(self):
        """Test complete collection creation workflow with mocked API."""
        api_key = os.environ.get("NAKALA_API_KEY", "test-key")
        config = NakalaConfig(api_key=api_key)
        config.base_url = "https://apitest.nakala.fr"

        client = NakalaCollectionClient(config)

        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"identifier": "integration-test-collection"}

        with patch.object(client.session, "post", return_value=mock_response):
            collection_config = {
                "title": "Integration Test Collection",
                "description": "Collection created during integration testing",
                "data_ids": ["data-1", "data-2", "data-3"],
            }

            result = client.create_single_collection(collection_config)
            assert result == "integration-test-collection"

    def test_csv_processing_workflow(self):
        """Test complete CSV processing workflow."""
        api_key = os.environ.get("NAKALA_API_KEY", "test-key")
        config = NakalaConfig(api_key=api_key)

        client = NakalaCollectionClient(config)

        # Create test CSV with multiple collections
        csv_content = """title,identifier,status,collection
Dataset 1,data-1,success,Research Collection
Dataset 2,data-2,success,Research Collection
Dataset 3,data-3,success,Archive Collection
Dataset 4,data-4,success,Archive Collection
Dataset 5,data-5,success,Teaching Collection"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            # Process CSV and group data
            upload_data = client._process_upload_output_csv(tmp_path)
            grouped_data = client._group_data_by_collection(upload_data)

            assert len(grouped_data) == 3  # Three different collections
            assert "Research Collection" in grouped_data
            assert "Archive Collection" in grouped_data
            assert "Teaching Collection" in grouped_data

            assert len(grouped_data["Research Collection"]) == 2
            assert len(grouped_data["Archive Collection"]) == 2
            assert len(grouped_data["Teaching Collection"]) == 1

        finally:
            os.unlink(tmp_path)

    def test_error_handling_workflow(self):
        """Test error handling in collection workflow."""
        api_key = os.environ.get("NAKALA_API_KEY", "test-key")
        config = NakalaConfig(api_key=api_key)

        client = NakalaCollectionClient(config)

        # Test with invalid configuration (missing data sources)
        invalid_config = {"title": "Missing data IDs"}

        with pytest.raises(
            NakalaValidationError,
            match="Either 'data_ids' or 'upload_data' must be provided",
        ):
            client.create_single_collection(invalid_config)

        # Test with empty title
        empty_title_config = {"title": "", "data_ids": ["data-1"]}

        with pytest.raises(NakalaValidationError, match="Title cannot be empty"):
            client.create_single_collection(empty_title_config)

    def test_batch_collection_creation(self):
        """Test creating multiple collections from grouped data."""
        api_key = os.environ.get("NAKALA_API_KEY", "test-key")
        config = NakalaConfig(api_key=api_key)

        client = NakalaCollectionClient(config)

        # Mock API responses
        mock_response = Mock()
        mock_response.status_code = 201

        def mock_json_response():
            # Return different IDs for each call
            mock_json_response.counter = getattr(mock_json_response, "counter", 0) + 1
            return {"identifier": f"collection-{mock_json_response.counter}"}

        mock_response.json = mock_json_response

        grouped_data = {
            "Research Collection": [
                {"identifier": "data-1", "title": "Dataset 1"},
                {"identifier": "data-2", "title": "Dataset 2"},
            ],
            "Archive Collection": [{"identifier": "data-3", "title": "Dataset 3"}],
        }

        with patch.object(client.session, "post", return_value=mock_response):
            results = []
            for collection_name, data_items in grouped_data.items():
                config = {
                    "title": collection_name,
                    "data_ids": [item["identifier"] for item in data_items],
                }
                result = client.create_single_collection(config)
                results.append(result)

            assert len(results) == 2
            assert "collection-1" in results
            assert "collection-2" in results
