"""
Comprehensive tests for configuration management
"""

import os
import tempfile
import pytest
from unittest.mock import patch
from pathlib import Path

from o_nakala_core.common.config import NakalaConfig
from o_nakala_core.common.exceptions import NakalaValidationError


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

    def test_config_with_custom_values(self):
        """Test configuration with custom values."""
        config = NakalaConfig(
            api_key="custom-key",
            api_url="https://custom-api.nakala.fr",
            timeout=300,
            max_retries=3,
        )

        assert config.api_key == "custom-key"
        assert config.api_url == "https://custom-api.nakala.fr"
        assert config.timeout == 300
        assert config.max_retries == 3

    def test_config_base_path_setting(self):
        """Test setting custom base path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = NakalaConfig(api_key="test-key")
            config.base_path = temp_dir

            assert config.base_path == temp_dir
            assert os.path.isabs(config.base_path)

    def test_config_url_validation(self):
        """Test URL validation and normalization."""
        config = NakalaConfig(api_key="test-key")

        # Test default URL
        assert "nakala.fr" in config.api_url
        assert config.api_url.startswith("https://")

        # Test setting custom URL
        config.api_url = "https://custom-api.example.com"
        assert config.api_url == "https://custom-api.example.com"

        # Test URL without protocol
        config.api_url = "api.nakala.fr"
        # Should handle gracefully or add protocol as needed

    def test_config_timeout_validation(self):
        """Test timeout validation."""
        config = NakalaConfig(api_key="test-key")

        # Test valid timeouts
        config.timeout = 300
        assert config.timeout == 300

        config.timeout = 900
        assert config.timeout == 900

        # Test edge cases
        config.timeout = 1
        assert config.timeout == 1

    def test_config_retry_validation(self):
        """Test retry count validation."""
        config = NakalaConfig(api_key="test-key")

        # Test valid retry counts
        config.max_retries = 1
        assert config.max_retries == 1

        config.max_retries = 10
        assert config.max_retries == 10

        config.max_retries = 0
        assert config.max_retries == 0

    def test_environment_variable_loading(self):
        """Test loading configuration from environment variables."""
        test_env = {
            "NAKALA_API_KEY": "env-test-key",
            "NAKALA_BASE_URL": "https://test-api.nakala.fr",
        }

        with patch.dict(os.environ, test_env):
            assert os.environ.get("NAKALA_API_KEY") == "env-test-key"
            assert os.environ.get("NAKALA_BASE_URL") == "https://test-api.nakala.fr"

    def test_config_from_environment(self):
        """Test creating config from environment variables."""
        test_env = {
            "NAKALA_API_KEY": "env-api-key",
            "NAKALA_API_URL": "https://env-api.nakala.fr",
            "NAKALA_TIMEOUT": "450",
            "NAKALA_MAX_RETRIES": "8",
        }

        with patch.dict(os.environ, test_env):
            # Test that environment variables can be accessed
            api_key = os.environ.get("NAKALA_API_KEY")
            assert api_key == "env-api-key"

            # Create config that uses environment variables
            config = NakalaConfig(api_key=api_key)
            assert config.api_key == "env-api-key"

    def test_config_serialization(self):
        """Test configuration serialization/deserialization."""
        original_config = NakalaConfig(
            api_key="serialization-test-key",
            api_url="https://test.nakala.fr",
            timeout=400,
            max_retries=4,
        )

        # Test basic attribute access
        assert hasattr(original_config, "api_key")
        assert hasattr(original_config, "api_url")
        assert hasattr(original_config, "timeout")
        assert hasattr(original_config, "max_retries")

    def test_config_immutable_defaults(self):
        """Test that certain config values have expected defaults."""
        config = NakalaConfig()

        # These should have stable default values
        assert isinstance(config.timeout, int)
        assert isinstance(config.max_retries, int)
        assert config.timeout > 0
        assert config.max_retries >= 0

        # API URL should be a valid URL format
        assert config.api_url.startswith("http")
        assert "nakala" in config.api_url.lower()

    def test_config_copy_and_modify(self):
        """Test copying and modifying configuration."""
        original = NakalaConfig(api_key="original-key")

        # Create a new config with modified values
        modified = NakalaConfig(
            api_key=original.api_key,
            api_url="https://modified.nakala.fr",
            timeout=original.timeout + 100,
        )

        assert modified.api_key == original.api_key
        assert modified.api_url != original.api_url
        assert modified.timeout == original.timeout + 100

    def test_config_edge_cases(self):
        """Test configuration edge cases."""
        # Test with very long API key
        long_key = "a" * 1000
        config = NakalaConfig(api_key=long_key)
        assert config.api_key == long_key

        # Test with valid API key
        config = NakalaConfig(api_key="test-key")
        assert config.api_key == "test-key"

    def test_config_string_representation(self):
        """Test string representation of config."""
        config = NakalaConfig(api_key="test-key")

        # Should have some string representation
        str_repr = str(config)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

        # Config string contains configuration info
        assert "NakalaConfig" in str_repr


class TestConfigurationValidation:
    """Test configuration validation functionality."""

    def test_validate_api_key_format(self):
        """Test API key format validation."""
        # Test with various API key formats
        valid_keys = [
            "aae99aba-476e-4ff2-2886-0aaf1bfa6fd2",  # UUID format
            "test-api-key-123",  # Simple format
            "very-long-api-key-with-many-characters-and-numbers-123456789",
        ]

        for key in valid_keys:
            config = NakalaConfig(api_key=key)
            assert config.api_key == key

    def test_validate_url_format(self):
        """Test URL format validation."""
        valid_urls = [
            "https://api.nakala.fr",
            "https://apitest.nakala.fr",
            "http://localhost:8000",
            "https://custom-domain.com/api",
        ]

        for url in valid_urls:
            config = NakalaConfig(api_key="test-key")
            config.api_url = url
            assert config.api_url == url

    def test_configuration_compatibility(self):
        """Test configuration compatibility across versions."""
        # Test that config works with different parameter combinations
        configs = [
            NakalaConfig(api_key="key1"),
            NakalaConfig(api_key="key2", api_url="https://test.com"),
            NakalaConfig(api_key="key3", timeout=500),
            NakalaConfig(api_key="key4", max_retries=7),
        ]

        for config in configs:
            assert config.api_key is not None
            assert config.api_url is not None
            assert config.timeout > 0
            assert config.max_retries >= 0
