"""
Pytest configuration and fixtures for Nakala Client tests.
"""

import pytest
import os
from unittest.mock import Mock, patch
from o_nakala_core.common.config import NakalaConfig


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def mock_config(mock_api_key):
    """Provide a mock configuration for testing."""
    with patch.dict(os.environ, {"NAKALA_API_KEY": mock_api_key}):
        config = NakalaConfig()
        config.api_key = mock_api_key
        config.base_url = "https://apitest.nakala.fr"
        return config


@pytest.fixture
def mock_requests_session():
    """Provide a mock requests session for API testing."""
    session = Mock()
    session.post.return_value.status_code = 201
    session.post.return_value.json.return_value = {"status": "success"}
    session.get.return_value.status_code = 200
    session.get.return_value.json.return_value = {"data": []}
    session.put.return_value.status_code = 204
    session.delete.return_value.status_code = 204
    return session


@pytest.fixture
def sample_metadata():
    """Provide sample metadata for testing."""
    return [
        {
            "propertyUri": "http://nakala.fr/terms#title",
            "value": "Test Dataset",
            "lang": "en",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
        },
        {
            "propertyUri": "http://nakala.fr/terms#description",
            "value": "A test dataset for unit testing",
            "lang": "en",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
        },
    ]


@pytest.fixture
def sample_file_data():
    """Provide sample file data for testing."""
    return {
        "name": "test_file.txt",
        "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "description": "Test file for unit testing",
    }
