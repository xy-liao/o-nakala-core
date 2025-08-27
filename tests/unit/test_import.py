"""
Basic import tests for o_nakala_core modules
"""

import os
import pytest
from o_nakala_core.common.config import NakalaConfig


class TestBasicImports:
    """Test basic import functionality."""

    def test_import_core_modules(self):
        """Test importing core modules."""
        from o_nakala_core.upload import NakalaUploadClient
        from o_nakala_core.collection import NakalaCollectionClient
        from o_nakala_core.common.config import NakalaConfig
        from o_nakala_core.common.exceptions import (
            NakalaAPIError,
            NakalaValidationError,
        )

        from o_nakala_core.cli.upload import main as upload_main
        from o_nakala_core.cli.collection import main as collection_main
        from o_nakala_core.cli.curator import main as curator_main
        from o_nakala_core.cli.user_info import main as user_info_main

        assert callable(upload_main)
        assert callable(collection_main)
        assert callable(curator_main)
        assert callable(user_info_main)

    def test_config_initialization(self):
        """Test configuration initialization."""
        api_key = os.environ.get("NAKALA_API_KEY", "test-key")

        config = NakalaConfig(api_key=api_key)
        assert config.api_key == api_key
        assert config.api_url == "https://apitest.nakala.fr"
        assert config.timeout == 600
        assert config.max_retries == 5

    def test_client_initialization(self):
        """Test client initialization with API key."""
        from o_nakala_core.upload import NakalaUploadClient
        from o_nakala_core.collection import NakalaCollectionClient

        api_key = os.environ.get("NAKALA_API_KEY", "test-key")

        config = NakalaConfig(api_key=api_key)

        upload_client = NakalaUploadClient(config)
        collection_client = NakalaCollectionClient(config)

        assert upload_client.config.api_key == api_key
        assert collection_client.config.api_key == api_key
