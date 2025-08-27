"""
Comprehensive tests for Nakala Upload functionality
"""

import os
import tempfile
import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from o_nakala_core.upload import NakalaUploadClient, NakalaFileProcessor
from o_nakala_core.common.config import NakalaConfig
from o_nakala_core.common.exceptions import (
    NakalaAPIError,
    NakalaValidationError,
    NakalaFileError,
)


class TestNakalaFileProcessor:
    """Test file processing functionality."""

    @pytest.fixture
    def mock_config(self):
        """Create mock configuration."""
        config = NakalaConfig(api_key="test-key")
        config.base_path = tempfile.gettempdir()
        return config

    @pytest.fixture
    def processor(self, mock_config):
        """Create file processor instance."""
        return NakalaFileProcessor(mock_config)

    def test_processor_initialization(self, processor, mock_config):
        """Test processor initialization."""
        assert processor.config == mock_config
        assert processor.path_resolver is not None
        assert processor.utils is not None

    def test_calculate_file_hash(self, processor):
        """Test file hash calculation."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write("test content for hashing")
            tmp_path = tmp.name

        try:
            hash_value = processor._calculate_file_hash(tmp_path)
            assert isinstance(hash_value, str)
            assert len(hash_value) == 40  # SHA1 hash length
            # Test same content produces same hash
            hash_value2 = processor._calculate_file_hash(tmp_path)
            assert hash_value == hash_value2
        finally:
            os.unlink(tmp_path)

    def test_get_file_metadata(self, processor):
        """Test file metadata extraction."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp:
            tmp.write("test content")
            tmp_path = tmp.name

        try:
            metadata = processor._get_file_metadata(tmp_path)
            assert "size" in metadata
            assert "mimetype" in metadata
            assert "sha1" in metadata
            assert metadata["size"] > 0
            assert "text" in metadata["mimetype"]
        finally:
            os.unlink(tmp_path)

    def test_get_file_metadata_nonexistent(self, processor):
        """Test metadata extraction for non-existent file."""
        with pytest.raises(NakalaFileError):
            processor._get_file_metadata("/nonexistent/file.txt")

    @patch("os.path.exists")
    def test_process_folder_structure_file_not_found(self, mock_exists, processor):
        """Test folder processing with non-existent config file."""
        mock_exists.return_value = False

        with pytest.raises(NakalaFileError):
            processor.process_folder_structure("/nonexistent/config.csv")


class TestNakalaUploadClient:
    """Test upload client functionality."""

    @pytest.fixture
    def mock_config(self):
        """Create mock configuration."""
        api_key = os.environ.get("NAKALA_API_KEY", "test-key")
        config = NakalaConfig(api_key=api_key)
        config.base_url = "https://apitest.nakala.fr"
        return config

    @pytest.fixture
    def upload_client(self, mock_config):
        """Create upload client instance."""
        return NakalaUploadClient(mock_config)

    def test_client_initialization(self, upload_client, mock_config):
        """Test client initialization."""
        assert upload_client.config == mock_config
        assert upload_client.session is not None
        assert upload_client.file_processor is not None
        assert upload_client.utils is not None

    def test_validate_dataset_config_success(self, upload_client):
        """Test successful dataset configuration validation."""
        config = {
            "title": "Test Dataset",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "description": "A test dataset",
            "files": ["test.txt"],
        }

        # Should not raise exception
        upload_client._validate_dataset_config(config)

    def test_validate_dataset_config_missing_title(self, upload_client):
        """Test validation with missing title."""
        config = {
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "files": ["test.txt"],
        }

        with pytest.raises(NakalaValidationError, match="title"):
            upload_client._validate_dataset_config(config)

    def test_validate_dataset_config_missing_type(self, upload_client):
        """Test validation with missing type."""
        config = {"title": "Test Dataset", "files": ["test.txt"]}

        with pytest.raises(NakalaValidationError, match="type"):
            upload_client._validate_dataset_config(config)

    def test_validate_dataset_config_with_files(self, upload_client):
        """Test validation with files list."""
        config = {
            "title": "Test Dataset",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "files": ["test.txt"],
        }

        # Should not raise exception
        upload_client._validate_dataset_config(config)

    def test_upload_file_success(self, upload_client):
        """Test successful file upload."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"sha1": "test-sha1-hash"}

        with patch.object(upload_client.session, "post", return_value=mock_response):
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(b"test file content")
                tmp_path = tmp.name

            try:
                result = upload_client._upload_file(tmp_path)
                assert result == "test-sha1-hash"
            finally:
                os.unlink(tmp_path)

    def test_upload_file_failure(self, upload_client):
        """Test file upload failure handling."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad request - invalid file"
        mock_response.raise_for_status.side_effect = Exception("HTTP 400")

        with patch.object(upload_client.session, "post", return_value=mock_response):
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(b"test content")
                tmp_path = tmp.name

            try:
                with pytest.raises(Exception):
                    upload_client._upload_file(tmp_path)
            finally:
                os.unlink(tmp_path)

    def test_create_dataset_success(self, upload_client):
        """Test successful dataset creation."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"identifier": "test-dataset-id"}

        with patch.object(
            upload_client.session, "post", return_value=mock_response
        ) as mock_post:
            metadata = [
                {
                    "propertyUri": "http://nakala.fr/terms#title",
                    "value": "Test Dataset",
                    "lang": "en",
                },
                {
                    "propertyUri": "http://purl.org/coar/resource_type",
                    "value": "http://purl.org/coar/resource_type/c_ddb1",
                },
            ]
            files = [{"sha1": "test-sha1", "name": "test.txt"}]

            result = upload_client._create_dataset(metadata, files)
            assert result == "test-dataset-id"
            mock_post.assert_called_once()

            # Check that request was made with correct data
            call_args = mock_post.call_args
            assert "json" in call_args.kwargs

    def test_create_dataset_api_error(self, upload_client):
        """Test dataset creation API error handling."""
        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.text = "Validation failed"
        mock_response.json.return_value = {"errors": ["Invalid metadata"]}

        with patch.object(upload_client.session, "post", return_value=mock_response):
            metadata = [{"propertyUri": "invalid", "value": "test"}]
            files = [{"sha1": "test-sha1", "name": "test.txt"}]

            with pytest.raises(NakalaAPIError):
                upload_client._create_dataset(metadata, files)

    @patch("o_nakala_core.upload.NakalaUploadClient._upload_file")
    @patch("o_nakala_core.upload.NakalaUploadClient._create_dataset")
    def test_upload_single_dataset_success(
        self, mock_create, mock_upload, upload_client
    ):
        """Test complete single dataset upload workflow."""
        mock_upload.return_value = "test-sha1"
        mock_create.return_value = "test-dataset-id"

        config = {
            "title": "Test Dataset",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "description": "Test description",
            "files": ["test.txt"],
        }

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp:
            tmp.write("test content")
            tmp_path = tmp.name

        try:
            with patch("os.path.exists", return_value=True):
                with patch("os.path.abspath", return_value=tmp_path):
                    result = upload_client.upload_single_dataset(config)
                    assert result == "test-dataset-id"
                    mock_upload.assert_called()
                    mock_create.assert_called_once()
        finally:
            os.unlink(tmp_path)


class TestUploadIntegration:
    """Integration tests for upload functionality."""

    def test_complete_upload_workflow_mocked(self):
        """Test complete upload workflow with mocked API."""
        api_key = os.environ.get("NAKALA_API_KEY", "test-key")
        config = NakalaConfig(api_key=api_key)
        config.base_url = "https://apitest.nakala.fr"

        client = NakalaUploadClient(config)

        # Mock successful responses
        upload_response = Mock()
        upload_response.status_code = 201
        upload_response.json.return_value = {"sha1": "file-hash-123"}

        dataset_response = Mock()
        dataset_response.status_code = 201
        dataset_response.json.return_value = {"identifier": "dataset-123"}

        with patch.object(client.session, "post") as mock_post:
            mock_post.side_effect = [upload_response, dataset_response]

            dataset_config = {
                "title": "Integration Test Dataset",
                "type": "http://purl.org/coar/resource_type/c_ddb1",
                "description": "Test dataset for integration testing",
                "files": [],
            }

            # Mock file validation and processing
            with patch(
                "o_nakala_core.upload.NakalaUploadClient._validate_dataset_config"
            ):
                with patch(
                    "o_nakala_core.upload.NakalaUploadClient._upload_file",
                    return_value="file-hash-123",
                ):
                    result = client.upload_single_dataset(dataset_config)
                    assert result is not None
                    assert mock_post.call_count >= 1

    def test_error_handling_workflow(self):
        """Test error handling in upload workflow."""
        api_key = os.environ.get("NAKALA_API_KEY", "test-key")
        config = NakalaConfig(api_key=api_key)

        client = NakalaUploadClient(config)

        # Test with invalid configuration
        invalid_config = {"title": "Missing required fields"}

        with pytest.raises(NakalaValidationError):
            client.upload_single_dataset(invalid_config)

    def test_file_processing_workflow(self):
        """Test file processing components."""
        api_key = os.environ.get("NAKALA_API_KEY", "test-key")
        config = NakalaConfig(api_key=api_key)
        config.base_path = tempfile.gettempdir()

        processor = NakalaFileProcessor(config)

        # Create test files
        test_files = []
        for i in range(3):
            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=f"_test_{i}.txt"
            ) as tmp:
                tmp.write(f"Test content {i}")
                test_files.append(tmp.name)

        try:
            # Test metadata extraction for multiple files
            metadata_list = []
            for file_path in test_files:
                metadata = processor._get_file_metadata(file_path)
                metadata_list.append(metadata)
                assert "sha1" in metadata
                assert "size" in metadata
                assert "mimetype" in metadata

            # Verify different files have different hashes
            hashes = [m["sha1"] for m in metadata_list]
            assert len(set(hashes)) == len(hashes)  # All unique

        finally:
            for file_path in test_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
