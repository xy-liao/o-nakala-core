"""
Nakala API Client

This module provides a high-level interface for interacting with the Nakala API.
It encapsulates all the functionality provided by the underlying services.
"""

from typing import Optional, Dict, Any, List, Union
from datetime import datetime, date

from .client import NakalaClient
from .services import DataService, FileService, CollectionService, SearchService
from .metadata import MetadataBuilder
from .exceptions import NakalaError, NakalaAPIError, NakalaValidationError


class NakalaAPI:
    """High-level client for the Nakala API.
    
    This class provides a simplified interface to the Nakala API, combining
    the functionality of the various service classes.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize the Nakala API client.
        
        Args:
            api_key: Your Nakala API key. If not provided, the NAKALA_API_KEY
                    environment variable will be used.
            base_url: Base URL for the API (defaults to production API).
        """
        self.client = NakalaClient(api_key=api_key, base_url=base_url)
        
        # Initialize services
        self.data = DataService(self.client)
        self.files = FileService(self.client)
        self.collections = CollectionService(self.client)
        self.search = SearchService(self.client)
    
    def metadata_builder(self) -> MetadataBuilder:
        """Create a new metadata builder instance.
        
        Returns:
            A new MetadataBuilder instance
        """
        return MetadataBuilder()
    
    # High-level convenience methods
    
    def upload_data(
        self,
        metadata: Dict[str, Any],
        file_paths: List[Union[str, Dict[str, Any]]],
        collection_ids: Optional[List[str]] = None,
        validate: bool = True
    ) -> Dict[str, Any]:
        """Upload a new data object with files.
        
        This is a convenience method that combines creating metadata and
        uploading files into a single operation.
        
        Args:
            metadata: Metadata for the data object
            file_paths: List of file paths or file info dictionaries with 'path' and 'mime_type'
            collection_ids: Optional list of collection IDs to add this data to
            validate: If True, validate metadata before uploading
            
        Returns:
            The created data object
        """
        return self.data.create_data(
            metadata=metadata,
            files=file_paths,
            collection_ids=collection_ids,
            validate=validate
        )
    
    def upload_file(
        self,
        file_path: str,
        mime_type: Optional[str] = None,
        chunk_size: int = 1024 * 1024  # 1MB chunks
    ) -> Dict[str, Any]:
        """Upload a file to Nakala's temporary storage.
        
        This is a convenience method that delegates to FileService.upload_file().
        
        Args:
            file_path: Path to the file to upload
            mime_type: MIME type of the file (optional, will be guessed if not provided)
            chunk_size: Size of chunks to use for streaming upload (in bytes)
            
        Returns:
            Dictionary containing file metadata including 'sha1' and 'embargo'
        """
        return self.files.upload_file(file_path, mime_type, chunk_size)
    
    def create_collection(
        self,
        title: str,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        data_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a new collection.
        
        This is a convenience method that delegates to CollectionService.create_collection().
        
        Args:
            title: Title of the collection
            description: Description of the collection
            metadata: Additional metadata for the collection
            data_ids: List of data object IDs to include in the collection
            
        Returns:
            The created collection
        """
        return self.collections.create_collection(
            title=title,
            description=description,
            metadata=metadata or {},
            data_ids=data_ids or []
        )
    
    def search_data(
        self,
        query: str = "*",
        filters: Optional[Dict[str, Any]] = None,
        collections: Optional[List[str]] = None,
        data_types: Optional[List[str]] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Search for data objects.
        
        This is a convenience method that delegates to SearchService.search().
        
        Args:
            query: Search query string (supports Lucene query syntax)
            filters: Additional filters as key-value pairs
            collections: Filter by collection IDs
            data_types: Filter by data types (e.g., ['Dataset', 'Image'])
            limit: Maximum number of results to return (default: 20)
            offset: Number of results to skip (for pagination)
            
        Returns:
            Dictionary containing search results and pagination info
        """
        return self.search.search(
            query=query,
            filters=filters or {},
            collections=collections,
            data_types=data_types,
            limit=limit,
            offset=offset
        )
    
    def close(self):
        """Close the underlying client session."""
        self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Export the main classes and functions
__all__ = [
    'NakalaAPI',
    'NakalaError',
    'NakalaAPIError',
    'NakalaValidationError'
]
