"""
Workflow Configuration Management

Handles API keys, environment setup, and configuration validation
for the NAKALA ultimate workflow.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import logging

class WorkflowConfig:
    """Configuration manager for NAKALA workflow operations."""
    
    def __init__(self, api_key: Optional[str] = None, base_path: Optional[str] = None):
        """
        Initialize workflow configuration.
        
        Args:
            api_key: NAKALA API key (if not provided, will check environment)
            base_path: Base path for data files (defaults to sample_dataset)
        """
        self.api_key = api_key or self._get_api_key()
        self.base_path = Path(base_path) if base_path else self._get_default_base_path()
        self.api_url = "https://apitest.nakala.fr"  # Default to test environment
        
        # Setup logging
        self._setup_logging()
        
        # Validate configuration
        self.validate()
    
    def _get_api_key(self) -> str:
        """Get API key from environment or prompt user."""
        api_key = os.getenv('NAKALA_API_KEY')
        if not api_key:
            # Provide test key as fallback for workshops
            api_key = "33170cfe-f53c-550b-5fb6-4814ce981293"
            print("⚠️  Using default test API key for demonstration")
            print("   For production use, set NAKALA_API_KEY environment variable")
        return api_key
    
    def _get_default_base_path(self) -> Path:
        """Get default base path to sample dataset."""
        # Assuming we're in notebooks/ and need to go to ../sample_dataset/
        current_dir = Path.cwd()
        if current_dir.name == "notebooks":
            return current_dir.parent / "sample_dataset"
        else:
            # Try to find sample_dataset directory
            for parent in [current_dir] + list(current_dir.parents):
                sample_dataset = parent / "examples" / "sample_dataset"
                if sample_dataset.exists():
                    return sample_dataset
            raise FileNotFoundError("Could not locate sample_dataset directory")
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        errors = []
        
        # Check API key
        if not self.api_key or len(self.api_key) < 10:
            errors.append("Invalid API key")
        
        # Check base path exists
        if not self.base_path.exists():
            errors.append(f"Base path does not exist: {self.base_path}")
        
        # Check required CSV files
        required_files = [
            "folder_data_items.csv",
            "folder_collections.csv"
        ]
        
        for file in required_files:
            file_path = self.base_path / file
            if not file_path.exists():
                errors.append(f"Required file missing: {file}")
        
        # Check files directory
        files_dir = self.base_path / "files"
        if not files_dir.exists():
            errors.append("Sample files directory missing")
        
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            raise ValueError(error_msg)
        
        self.logger.info("✅ Configuration validated successfully")
        return True
    
    def get_file_path(self, filename: str) -> Path:
        """Get full path to a file in the base directory."""
        return self.base_path / filename
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary for passing to other modules."""
        return {
            'api_key': self.api_key,
            'api_url': self.api_url,
            'base_path': str(self.base_path),
            'dataset_csv': str(self.get_file_path('folder_data_items.csv')),
            'collections_csv': str(self.get_file_path('folder_collections.csv')),
            'files_dir': str(self.get_file_path('files'))
        }
    
    def display_info(self):
        """Display configuration information."""
        print("🔧 Workflow Configuration")
        print("=" * 50)
        print(f"API Key: {self.api_key[:10]}...")
        print(f"API URL: {self.api_url}")
        print(f"Base Path: {self.base_path}")
        print(f"Dataset CSV: {self.get_file_path('folder_data_items.csv')}")
        print(f"Collections CSV: {self.get_file_path('folder_collections.csv')}")
        print(f"Files Directory: {self.get_file_path('files')}")
        print("=" * 50)