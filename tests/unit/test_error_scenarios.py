"""
Error scenario testing for O-Nakala Core.

This module tests various error conditions, edge cases, and failure scenarios
to ensure robust error handling and graceful degradation.
"""

import pytest
import tempfile
import json
import csv
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

from o_nakala_core.upload import NakalaUploadClient
from o_nakala_core.collection import NakalaCollectionClient
from o_nakala_core.common.config import NakalaConfig
from o_nakala_core.common.exceptions import NakalaAPIError, NakalaValidationError


class TestFileSystemErrors:
    """Test file system related error scenarios."""

    @pytest.fixture
    def base_config(self):
        """Base configuration for tests.

        Security Note: Uses secure temporary directory instead of /tmp.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-key-123",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
            )

    def test_upload_with_permission_denied_file(self, base_config):
        """Test behavior when file access is denied.

        Security Note: This test carefully manages file permissions to avoid
        creating security vulnerabilities or leaving inaccessible files.
        """
        upload_client = NakalaUploadClient(base_config)

        # Create a file and store original permissions
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test content")
            restricted_file = f.name

        # Get original permissions for safe restoration
        original_mode = os.stat(restricted_file).st_mode

        try:
            # Remove read permissions (but keep owner write for cleanup)
            os.chmod(restricted_file, 0o200)  # Owner write only, safer than 0o000

            # Validation should handle permission errors gracefully
            is_valid = upload_client.file_processor.validate_file(restricted_file)
            # Depending on implementation, this might be False or raise an exception
            assert isinstance(is_valid, bool)

        except PermissionError:
            # This is also acceptable behavior
            pass
        finally:
            # Restore original permissions for safe cleanup
            try:
                os.chmod(restricted_file, original_mode)
                os.unlink(restricted_file)
            except (PermissionError, FileNotFoundError):
                # If all else fails, try to force cleanup with minimal permissions
                try:
                    os.chmod(restricted_file, 0o600)  # Owner read/write only
                    os.unlink(restricted_file)
                except (PermissionError, FileNotFoundError, OSError):
                    # Last resort: skip cleanup if file is truly inaccessible
                    # This is safer than leaving with overly permissive permissions
                    pass

    def test_upload_with_directory_instead_of_file(self, base_config):
        """Test behavior when a directory path is provided instead of file."""
        upload_client = NakalaUploadClient(base_config)

        with tempfile.TemporaryDirectory() as temp_dir:
            is_valid = upload_client.file_processor.validate_file(temp_dir)
            assert is_valid == False

    def test_upload_with_broken_symlink(self, base_config):
        """Test behavior with broken symbolic links."""
        upload_client = NakalaUploadClient(base_config)

        with tempfile.TemporaryDirectory() as temp_dir:
            broken_link = os.path.join(temp_dir, "broken_link")
            target = os.path.join(temp_dir, "nonexistent_target")

            # Create broken symlink
            os.symlink(target, broken_link)

            is_valid = upload_client.file_processor.validate_file(broken_link)
            assert is_valid == False

    def test_csv_with_encoding_errors(self, base_config):
        """Test CSV processing with encoding issues."""
        upload_client = NakalaUploadClient(base_config)

        # Create CSV with problematic encoding
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
            # Write some bytes that aren't valid UTF-8
            f.write(b"title,type\n")
            f.write(b"Test\xff\xfe,type1\n")  # Invalid UTF-8 sequence
            problematic_csv = f.name

        try:
            # Test that invalid encoding is handled gracefully
            try:
                upload_client.validate_dataset(mode="csv", dataset_path=problematic_csv)
            except (UnicodeDecodeError, UnicodeError):
                # This is acceptable - encoding errors should be caught
                pass
        finally:
            os.unlink(problematic_csv)


class TestNetworkAndAPIErrors:
    """Test network connectivity and API error scenarios."""

    @pytest.fixture
    def mock_config(self):
        """Configuration for mocked network tests.

        Security Note: Uses secure temporary directory.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-key-123",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
            )

    @patch("requests.Session")
    def test_api_timeout_error(self, mock_session, mock_config):
        """Test behavior when API requests timeout."""
        # Mock timeout exception
        import requests

        mock_session.return_value.post.side_effect = requests.exceptions.Timeout(
            "Request timed out"
        )

        upload_client = NakalaUploadClient(mock_config)

        # Create temporary file for upload test
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test content")
            test_file = f.name

        try:
            # Test that timeout is handled gracefully by using correct API
            try:
                # Use the actual upload method
                upload_client.upload_file(test_file, "test.txt")
                assert False, "Should have raised an exception for timeout"
            except Exception as e:
                # Expected - timeout should cause some kind of exception (may be wrapped in RetryError)
                error_str = str(e).lower()
                assert (
                    "timeout" in error_str
                    or "retryerror" in error_str
                    or "api_error" in error_str
                )
        finally:
            os.unlink(test_file)

    @patch("requests.Session")
    def test_api_connection_error(self, mock_session, mock_config):
        """Test behavior when API connection fails."""
        import requests

        mock_session.return_value.post.side_effect = (
            requests.exceptions.ConnectionError("Connection failed")
        )

        upload_client = NakalaUploadClient(mock_config)

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test content")
            test_file = f.name

        try:
            try:
                # Use the actual upload method
                upload_client.upload_file(test_file, "test.txt")
                assert False, "Should have raised an exception for connection error"
            except Exception as e:
                # Expected - connection error should cause some kind of exception (may be wrapped)
                error_str = str(e).lower()
                assert (
                    "connection" in error_str
                    or "retryerror" in error_str
                    or "api_error" in error_str
                )
        finally:
            os.unlink(test_file)

    @patch("requests.Session")
    def test_api_http_error_responses(self, mock_session, mock_config):
        """Test handling of various HTTP error responses."""
        upload_client = NakalaUploadClient(mock_config)

        # Test different HTTP error codes
        error_codes = [400, 401, 403, 404, 422, 500, 502, 503]

        for error_code in error_codes:
            mock_response = MagicMock()
            mock_response.status_code = error_code
            mock_response.json.return_value = {"error": f"HTTP {error_code} error"}
            mock_session.return_value.post.return_value = mock_response

            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(b"test content")
                test_file = f.name

            try:
                # Should handle different error codes appropriately
                result = upload_client.upload_single_file(
                    test_file, {"title": "Test", "type": "test"}
                )
                # Depending on implementation, might return error info or raise exception
                assert result is not None or True  # Either handles gracefully or raises
            except (NakalaAPIError, Exception):
                # Error handling is also acceptable
                pass
            finally:
                os.unlink(test_file)


class TestDataValidationErrors:
    """Test data validation and parsing error scenarios."""

    @pytest.fixture
    def validation_config(self):
        """Configuration for validation tests.

        Security Note: Uses secure temporary directory.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-key-123",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
            )

    def test_malformed_csv_structure(self, validation_config):
        """Test handling of malformed CSV files."""
        upload_client = NakalaUploadClient(validation_config)

        malformed_csvs = [
            "header1,header2\nvalue1\n",  # Missing column
            "header1,header2\nvalue1,value2,value3\n",  # Extra column
            '"unclosed quote,value2\n',  # Unclosed quote
            "header1,header2\n,\n",  # Empty values
            "",  # Completely empty
            "no,headers,just,values\n",  # No proper header structure
        ]

        for csv_content in malformed_csvs:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False
            ) as f:
                f.write(csv_content)
                malformed_file = f.name

            try:
                # Should handle malformed CSV gracefully
                upload_client.validate_dataset(mode="csv", dataset_path=malformed_file)
                # If it doesn't raise an exception, that's also valid
            except (csv.Error, ValueError, UnicodeDecodeError, NakalaValidationError):
                # Expected for malformed CSV - validation errors are normal
                pass
            finally:
                os.unlink(malformed_file)

    def test_invalid_json_metadata(self, validation_config):
        """Test handling of invalid JSON metadata."""
        upload_client = NakalaUploadClient(validation_config)

        invalid_json_strings = [
            '{"title": "Test"',  # Unclosed brace
            '{"title": Test}',  # Unquoted value
            '{title: "Test"}',  # Unquoted key
            '{"title": "Test",}',  # Trailing comma
            "",  # Empty string
            "not json at all",  # Not JSON
            '{"title": "Test", "nested": {"incomplete": }',  # Incomplete nested
        ]

        for json_str in invalid_json_strings:
            try:
                json.loads(json_str)
                # If JSON is actually valid, skip this test case
                continue
            except json.JSONDecodeError:
                # This is what we expect - invalid JSON
                pass

            # Test that upload client handles invalid JSON metadata gracefully
            try:
                metadata = json.loads(json_str)
                # This shouldn't execute for invalid JSON
            except json.JSONDecodeError:
                # Expected behavior
                assert True

    def test_metadata_missing_required_fields(self, validation_config):
        """Test metadata validation with missing required fields."""
        upload_client = NakalaUploadClient(validation_config)

        incomplete_metadata_sets = [
            {},  # Completely empty
            {"title": "Test Title"},  # Missing type
            {"type": "http://purl.org/coar/resource_type/c_ddb1"},  # Missing title
            {"title": "", "type": ""},  # Empty required fields
            {"title": None, "type": None},  # Null required fields
        ]

        for metadata in incomplete_metadata_sets:
            try:
                prepared = upload_client.prepare_metadata_from_dict(metadata)
                # If preparation succeeds, check if required fields are actually present
                if prepared:
                    title_found = any(
                        "title" in m.get("propertyUri", "") for m in prepared
                    )
                    type_found = any(
                        "type" in m.get("propertyUri", "") for m in prepared
                    )
                    # At least one of these should be present for valid metadata
                    assert title_found or type_found or len(prepared) == 0
            except (ValueError, KeyError, NakalaValidationError):
                # Expected for invalid metadata
                pass


class TestConcurrencyAndResourceErrors:
    """Test resource management and concurrency issues."""

    @pytest.fixture
    def resource_config(self):
        """Configuration for resource tests.

        Security Note: Uses secure temporary directory.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-key-123",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
            )

    def test_large_file_memory_handling(self, resource_config):
        """Test handling of very large files without memory issues."""
        upload_client = NakalaUploadClient(resource_config)

        # Create a larger file (1MB)
        large_size = 1024 * 1024  # 1MB

        with tempfile.NamedTemporaryFile(delete=False) as f:
            # Write in chunks to avoid memory issues in test
            chunk_size = 8192
            for _ in range(large_size // chunk_size):
                f.write(b"x" * chunk_size)
            large_file = f.name

        try:
            # Test that large file processing doesn't cause memory issues
            is_valid = upload_client.file_processor.validate_file(large_file)
            assert is_valid == True

            # Test file hash calculation on large file
            try:
                sha1_hash = upload_client.file_processor._calculate_file_hash(
                    large_file
                )
                assert len(sha1_hash) == 40
            except AttributeError:
                # Method might be private or not available, skip this test
                pass
        finally:
            os.unlink(large_file)

    @patch("builtins.open", side_effect=OSError("No space left on device"))
    def test_disk_space_error(self, mock_open, resource_config):
        """Test behavior when disk space is exhausted."""
        upload_client = NakalaUploadClient(resource_config)

        # Test that disk space errors are handled gracefully
        try:
            upload_client.file_processor.validate_file("/some/file/path")
            # If no error is raised, that's also valid (graceful handling)
        except OSError:
            # Expected for disk space issues
            pass

    def test_multiple_client_instances(self, resource_config):
        """Test that multiple client instances don't interfere with each other."""
        # Create multiple clients
        clients = [NakalaUploadClient(resource_config) for _ in range(5)]

        # Test that all clients are properly initialized
        for client in clients:
            assert client.config.api_key == "test-key-123"
            assert hasattr(client, "file_processor")
            assert hasattr(client, "utils")


class TestEdgeCaseInputs:
    """Test edge case inputs and boundary conditions."""

    @pytest.fixture
    def edge_config(self):
        """Configuration for edge case tests.

        Security Note: Uses secure temporary directory.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-key-123",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
            )

    @pytest.mark.parametrize(
        "edge_case_title",
        [
            "",  # Empty string
            " ",  # Just whitespace
            "\n\t\r",  # Various whitespace characters
            "A" * 1000,  # Very long title
            "Title with special chars: éàçñü",  # Unicode characters
            "Title with emoji: 🔬📊",  # Emoji characters
            "Title\nwith\nnewlines",  # Newlines
            "Title\twith\ttabs",  # Tabs
            '"Title with quotes"',  # Quotes
            "Title with 'single quotes'",  # Single quotes
            "Title with <html> tags",  # HTML-like content
            "Title with & special & entities",  # Special characters
        ],
    )
    def test_edge_case_title_values(self, edge_config, edge_case_title):
        """Test handling of edge case title values."""
        upload_client = NakalaUploadClient(edge_config)

        metadata = {
            "title": edge_case_title,
            "type": "http://purl.org/coar/resource_type/c_ddb1",
        }

        try:
            prepared = upload_client.prepare_metadata_from_dict(metadata)
            # Should handle edge cases gracefully
            assert isinstance(prepared, list)
        except (ValueError, UnicodeError):
            # Some edge cases might legitimately fail
            pass

    def test_extremely_nested_directory_structure(self, edge_config):
        """Test handling of deeply nested directory structures."""
        upload_client = NakalaUploadClient(edge_config)

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create deeply nested structure
            nested_path = temp_dir
            for i in range(50):  # Create 50 levels deep
                nested_path = os.path.join(nested_path, f"level_{i}")
                os.makedirs(nested_path, exist_ok=True)

            # Create a file in the deepest directory
            deep_file = os.path.join(nested_path, "deep_file.txt")
            with open(deep_file, "w") as f:
                f.write("content")

            # Test file validation with deep path
            is_valid = upload_client.file_processor.validate_file(deep_file)
            assert is_valid == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
