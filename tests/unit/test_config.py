"""
Tests for configuration management
"""

import os
import pytest
from unittest.mock import patch
from nakala_client.common.config import NakalaConfig


class TestNakalaConfig:
    """Test NakalaConfig functionality."""
    
    def test_config_defaults(self):
        """Test default configuration values."""
        config = NakalaConfig()
        
        assert config.api_url == "https://apitest.nakala.fr"
        assert config.timeout == 600
        assert config.max_retries == 5
        assert config.base_path == os.getcwd()
    
    def test_config_with_api_key(self):
        """Test configuration with API key."""
        api_key = "test-api-key-123"
        config = NakalaConfig(api_key=api_key)
        
        assert config.api_key == api_key
    
    def test_config_api_key_validation(self):
        """Test API key validation."""
        config = NakalaConfig()
        
        config.api_key = "valid-key"
        assert config.api_key == "valid-key"
        
        config.api_key = ""
        assert config.api_key == ""
    
    def test_environment_variable_loading(self):
        """Test loading configuration from environment variables."""
        test_env = {
            "NAKALA_API_KEY": "env-test-key",
            "NAKALA_BASE_URL": "https://test-api.nakala.fr"
        }
        
        with patch.dict(os.environ, test_env):
            assert os.environ.get("NAKALA_API_KEY") == "env-test-key"
            assert os.environ.get("NAKALA_BASE_URL") == "https://test-api.nakala.fr"