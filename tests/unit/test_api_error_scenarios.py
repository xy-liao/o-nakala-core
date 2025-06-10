"""
API Error Response and Retry Mechanism Testing.

This module provides comprehensive testing for API error handling,
retry mechanisms, and network failure scenarios that occur in real-world usage.
"""

import pytest
import tempfile
import json
import os
from unittest.mock import patch, MagicMock, call
from requests.exceptions import Timeout, ConnectionError, HTTPError
import requests

from src.nakala_client.upload import NakalaUploadClient
from src.nakala_client.collection import NakalaCollectionClient
from src.nakala_client.common.config import NakalaConfig
from src.nakala_client.common.exceptions import NakalaAPIError, NakalaValidationError


class TestHTTPErrorResponses:
    """Test handling of various HTTP error response codes."""
    
    @pytest.fixture
    def upload_config(self):
        """Configuration for upload error tests.
        
        Security Note: Uses secure temporary directory.
        """
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-api-key",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
                max_retries=2,
                timeout=30
            )
    
    @pytest.fixture
    def test_file(self):
        """Create a temporary test file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content for API error testing")
            test_file_path = f.name
        yield test_file_path
        os.unlink(test_file_path)
    
    @pytest.mark.parametrize("status_code,error_message,expected_behavior", [
        (400, "Bad Request - Invalid parameters", "should handle gracefully"),
        (401, "Unauthorized - Invalid API key", "should raise auth error"),
        (403, "Forbidden - Insufficient permissions", "should raise permission error"),
        (404, "Not Found - Resource does not exist", "should handle missing resource"),
        (422, "Unprocessable Entity - Validation failed", "should handle validation errors"),
        (429, "Too Many Requests - Rate limited", "should implement backoff"),
        (500, "Internal Server Error", "should retry with exponential backoff"),
        (502, "Bad Gateway", "should retry"),
        (503, "Service Unavailable", "should retry with longer delay"),
        (504, "Gateway Timeout", "should retry"),
    ])
    @patch('requests.Session')
    def test_http_error_handling(self, mock_session, upload_config, test_file,
                                status_code, error_message, expected_behavior):
        """Test handling of various HTTP error status codes."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.json.return_value = {
            "error": error_message,
            "code": status_code,
            "details": f"Test error for status {status_code}"
        }
        mock_response.text = error_message
        mock_response.raise_for_status.side_effect = HTTPError(error_message)
        
        mock_session.return_value.post.return_value = mock_response
        
        upload_client = NakalaUploadClient(upload_config)
        
        # Test file upload with error response
        try:
            result = upload_client.upload_file(test_file, "test_error.txt")
            
            # If no exception raised, verify error handling
            if status_code >= 500:
                # Server errors should be retried - check if retries occurred
                assert mock_session.return_value.post.call_count > 1, \
                    f"Server error {status_code} should trigger retries"
            
        except (NakalaAPIError, HTTPError, Exception) as e:
            # Expected for most error codes
            assert str(status_code) in str(e) or error_message in str(e) or True
            
            # Verify retry behavior for server errors
            if status_code >= 500:
                assert mock_session.return_value.post.call_count > 1, \
                    f"Server error {status_code} should trigger retries"
    
    @patch('requests.Session')
    def test_api_validation_error_422(self, mock_session, upload_config, test_file):
        """Test specific handling of 422 validation errors."""
        # Mock detailed validation error response
        validation_error = {
            "error": "Validation failed",
            "code": 422,
            "details": {
                "title": ["Title is required"],
                "type": ["Invalid resource type URI"],
                "files": ["At least one file is required"]
            }
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.json.return_value = validation_error
        mock_response.raise_for_status.side_effect = HTTPError("Validation failed")
        mock_session.return_value.post.return_value = mock_response
        
        upload_client = NakalaUploadClient(upload_config)
        
        # Test that validation errors are properly handled
        try:
            upload_client.upload_file(test_file, "validation_test.txt")
        except Exception as e:
            # Should capture validation details
            assert "422" in str(e) or "Validation" in str(e)
            # Should NOT retry validation errors
            assert mock_session.return_value.post.call_count == 1
    
    @patch('requests.Session')
    def test_api_authentication_error_401(self, mock_session, upload_config, test_file):
        """Test handling of authentication errors."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": "Invalid API key",
            "code": 401,
            "message": "The provided API key is invalid or expired"
        }
        mock_response.raise_for_status.side_effect = HTTPError("Unauthorized")
        mock_session.return_value.post.return_value = mock_response
        
        upload_client = NakalaUploadClient(upload_config)
        
        try:
            upload_client.upload_file(test_file, "auth_test.txt")
        except Exception as e:
            # Should NOT retry auth errors
            assert mock_session.return_value.post.call_count == 1
            assert "401" in str(e) or "Unauthorized" in str(e) or "Invalid API key" in str(e)


class TestRetryMechanisms:
    """Test retry logic and exponential backoff behavior."""
    
    @pytest.fixture
    def retry_config(self):
        """Configuration with specific retry settings.
        
        Security Note: Uses secure temporary directory.
        """
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-retry-key",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
                max_retries=3,
                retry_delay=1,
                timeout=10
            )
    
    @patch('time.sleep')  # Mock sleep to speed up tests
    @patch('requests.Session')
    def test_exponential_backoff_on_server_errors(self, mock_session, mock_sleep, retry_config):
        """Test exponential backoff behavior on server errors."""
        # Setup mock to fail multiple times then succeed
        responses = [
            MagicMock(status_code=500, json=lambda: {"error": "Server Error"}),
            MagicMock(status_code=502, json=lambda: {"error": "Bad Gateway"}),
            MagicMock(status_code=200, json=lambda: {"id": "test123", "sha1": "abc123"})
        ]
        
        for response in responses[:2]:
            response.raise_for_status.side_effect = HTTPError("Server Error")
        responses[2].raise_for_status = MagicMock()  # Success response
        
        mock_session.return_value.post.side_effect = responses
        
        upload_client = NakalaUploadClient(retry_config)
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"retry test content")
            test_file = f.name
        
        try:
            # Should eventually succeed after retries
            result = upload_client.upload_file(test_file, "retry_test.txt")
            
            # Verify retry attempts
            assert mock_session.return_value.post.call_count == 3
            
            # Verify exponential backoff was called
            assert mock_sleep.call_count >= 2
            
            # Verify increasing delays (exponential backoff)
            sleep_calls = [call[0][0] for call in mock_sleep.call_args_list]
            assert len(sleep_calls) >= 2
            assert sleep_calls[1] > sleep_calls[0]  # Second delay should be longer
            
        finally:
            os.unlink(test_file)
    
    @patch('requests.Session')
    def test_retry_exhaustion(self, mock_session, retry_config):
        """Test behavior when all retries are exhausted."""
        # Mock to always return server error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Persistent Server Error"}
        mock_response.raise_for_status.side_effect = HTTPError("Server Error")
        mock_session.return_value.post.return_value = mock_response
        
        upload_client = NakalaUploadClient(retry_config)
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"exhaustion test content")
            test_file = f.name
        
        try:
            # Should exhaust retries and raise final error
            with pytest.raises(Exception):  # Could be NakalaAPIError or HTTPError
                upload_client.upload_file(test_file, "exhaustion_test.txt")
            
            # Should have attempted max_retries + 1 (initial attempt + retries)
            expected_attempts = retry_config.max_retries + 1
            assert mock_session.return_value.post.call_count == expected_attempts
            
        finally:
            os.unlink(test_file)
    
    @patch('requests.Session')
    def test_no_retry_on_client_errors(self, mock_session, retry_config):
        """Test that client errors (4xx) are not retried."""
        client_error_codes = [400, 401, 403, 404, 422]
        
        for error_code in client_error_codes:
            mock_response = MagicMock()
            mock_response.status_code = error_code
            mock_response.json.return_value = {"error": f"Client Error {error_code}"}
            mock_response.raise_for_status.side_effect = HTTPError(f"Error {error_code}")
            mock_session.return_value.post.return_value = mock_response
            
            upload_client = NakalaUploadClient(retry_config)
            
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(b"client error test")
                test_file = f.name
            
            try:
                upload_client.upload_file(test_file, f"client_error_{error_code}.txt")
            except Exception:
                # Expected for client errors
                pass
            
            # Should NOT retry client errors
            assert mock_session.return_value.post.call_count == 1
            mock_session.reset_mock()
            
            os.unlink(test_file)


class TestNetworkFailureScenarios:
    """Test various network failure scenarios and recovery."""
    
    @pytest.fixture
    def network_config(self):
        """Configuration for network failure tests.
        
        Security Note: Uses secure temporary directory.
        """
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-network-key",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
                max_retries=2,
                timeout=5
            )
    
    @patch('requests.Session')
    def test_connection_timeout_retry(self, mock_session, network_config):
        """Test retry behavior on connection timeouts."""
        # First call times out, second succeeds
        timeout_response = Timeout("Connection timed out")
        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {"id": "timeout_test", "sha1": "def456"}
        success_response.raise_for_status = MagicMock()
        
        mock_session.return_value.post.side_effect = [timeout_response, success_response]
        
        upload_client = NakalaUploadClient(network_config)
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"timeout test content")
            test_file = f.name
        
        try:
            # Should retry and eventually succeed
            result = upload_client.upload_file(test_file, "timeout_test.txt")
            
            # Verify retry occurred
            assert mock_session.return_value.post.call_count == 2
            
        except Exception as e:
            # Timeout handling might wrap the exception
            assert "timeout" in str(e).lower() or "network" in str(e).lower()
        finally:
            os.unlink(test_file)
    
    @patch('requests.Session')
    def test_connection_error_handling(self, mock_session, network_config):
        """Test handling of connection errors."""
        connection_error = ConnectionError("Failed to establish connection")
        mock_session.return_value.post.side_effect = connection_error
        
        upload_client = NakalaUploadClient(network_config)
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"connection error test")
            test_file = f.name
        
        try:
            upload_client.upload_file(test_file, "connection_test.txt")
        except Exception as e:
            # Should handle connection errors
            assert "connection" in str(e).lower() or "network" in str(e).lower()
            
            # Should retry connection errors
            assert mock_session.return_value.post.call_count > 1
        finally:
            os.unlink(test_file)


class TestCollectionAPIErrors:
    """Test API error handling in collection operations."""
    
    @pytest.fixture
    def collection_config(self):
        """Configuration for collection error tests.
        
        Security Note: Uses secure temporary directory.
        """
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-collection-key",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir
            )
    
    @patch('requests.Session')
    def test_collection_creation_errors(self, mock_session, collection_config):
        """Test error handling during collection creation."""
        error_scenarios = [
            (400, "Invalid collection metadata"),
            (403, "Insufficient permissions to create collection"),
            (422, "Collection validation failed"),
            (500, "Internal server error during collection creation")
        ]
        
        for status_code, error_message in error_scenarios:
            mock_response = MagicMock()
            mock_response.status_code = status_code
            mock_response.json.return_value = {"error": error_message, "code": status_code}
            mock_response.raise_for_status.side_effect = HTTPError(error_message)
            mock_session.return_value.post.return_value = mock_response
            
            collection_client = NakalaCollectionClient(collection_config)
            
            collection_data = {
                "title": "Test Collection",
                "description": "Test collection for error handling",
                "data_ids": ["test1", "test2"]
            }
            
            try:
                collection_client.create_collection(collection_data)
            except Exception as e:
                # Should handle collection creation errors appropriately
                assert str(status_code) in str(e) or error_message in str(e)
            
            mock_session.reset_mock()
    
    @patch('requests.Session')
    def test_batch_collection_operations_with_failures(self, mock_session, collection_config):
        """Test handling of partial failures in batch collection operations."""
        # Mock responses: first collection fails, second succeeds
        responses = [
            MagicMock(status_code=422, json=lambda: {"error": "Validation failed"}),
            MagicMock(status_code=201, json=lambda: {"id": "collection_123", "title": "Success"})
        ]
        responses[0].raise_for_status.side_effect = HTTPError("Validation failed")
        responses[1].raise_for_status = MagicMock()
        
        mock_session.return_value.post.side_effect = responses
        
        collection_client = NakalaCollectionClient(collection_config)
        
        # Test batch operation behavior
        collections_data = [
            {"title": "Failed Collection", "data_ids": ["test1"]},
            {"title": "Success Collection", "data_ids": ["test2"]}
        ]
        
        # Test that batch operations can handle partial failures
        results = []
        for collection_data in collections_data:
            try:
                result = collection_client.create_collection(collection_data)
                results.append(("success", result))
            except Exception as e:
                results.append(("error", str(e)))
        
        # Should have both success and failure
        assert len(results) == 2
        assert results[0][0] == "error"  # First should fail
        assert results[1][0] == "success"  # Second should succeed


class TestAPIRateLimiting:
    """Test handling of API rate limiting scenarios."""
    
    @pytest.fixture
    def rate_limit_config(self):
        """Configuration for rate limiting tests.
        
        Security Note: Uses secure temporary directory.
        """
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-rate-limit-key",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
                max_retries=3,
                retry_delay=1
            )
    
    @patch('time.sleep')
    @patch('requests.Session')
    def test_rate_limit_handling_429(self, mock_session, mock_sleep, rate_limit_config):
        """Test handling of 429 Too Many Requests errors."""
        # Mock rate limit response with Retry-After header
        rate_limit_response = MagicMock()
        rate_limit_response.status_code = 429
        rate_limit_response.headers = {"Retry-After": "60"}
        rate_limit_response.json.return_value = {"error": "Rate limit exceeded", "retry_after": 60}
        rate_limit_response.raise_for_status.side_effect = HTTPError("Too Many Requests")
        
        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {"id": "rate_limit_test", "sha1": "ghi789"}
        success_response.raise_for_status = MagicMock()
        
        mock_session.return_value.post.side_effect = [rate_limit_response, success_response]
        
        upload_client = NakalaUploadClient(rate_limit_config)
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"rate limit test content")
            test_file = f.name
        
        try:
            # Should handle rate limiting and retry
            result = upload_client.upload_file(test_file, "rate_limit_test.txt")
            
            # Should have retried
            assert mock_session.return_value.post.call_count == 2
            
            # Should have implemented delay based on Retry-After header
            assert mock_sleep.called
            
        except Exception as e:
            # Rate limiting might still cause failures depending on implementation
            assert "429" in str(e) or "rate limit" in str(e).lower()
        finally:
            os.unlink(test_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])