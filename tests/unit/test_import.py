"""
Basic import tests for nakala_client modules
"""

import os
import pytest
from nakala_client.common.config import NakalaConfig


class TestBasicImports:
    """Test basic import functionality."""
    
    def test_import_core_modules(self):
        """Test importing core modules."""
        from nakala_client.upload import NakalaUploadClient
        from nakala_client.collection import NakalaCollectionClient
        from nakala_client.common.config import NakalaConfig
        from nakala_client.common.exceptions import NakalaAPIError, NakalaValidationError
        
        from nakala_client.cli.upload import main as upload_main
        from nakala_client.cli.collection import main as collection_main
        from nakala_client.cli.curator import main as curator_main
        from nakala_client.cli.user_info import main as user_info_main
        
        assert callable(upload_main)
        assert callable(collection_main)
        assert callable(curator_main)
        assert callable(user_info_main)
    
    def test_config_initialization(self):
        """Test configuration initialization."""
        api_key = os.environ.get('NAKALA_API_KEY', 'test-key')
        
        config = NakalaConfig(api_key=api_key)
        assert config.api_key == api_key
        assert config.api_url == "https://apitest.nakala.fr"
        assert config.timeout == 600
        assert config.max_retries == 5
    
    def test_client_initialization(self):
        """Test client initialization with API key."""
        from nakala_client.upload import NakalaUploadClient
        from nakala_client.collection import NakalaCollectionClient
        
        api_key = os.environ.get('NAKALA_API_KEY', 'test-key')
        
        config = NakalaConfig(api_key=api_key)
        
        upload_client = NakalaUploadClient(config)
        collection_client = NakalaCollectionClient(config)
        
        assert upload_client.config.api_key == api_key
        assert collection_client.config.api_key == api_key