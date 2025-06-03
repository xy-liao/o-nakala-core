"""
Base service class for Nakala API services.

This module provides a base class for all Nakala API services,
handling common functionality like request/response processing.
"""

from typing import Any, Dict, Optional, Union, List, Tuple
import json
import logging
from urllib.parse import urljoin, quote_plus

from ..client import NakalaClient
from ..exceptions import NakalaError, NakalaAPIError, NakalaValidationError
from ..metadata import validate_metadata, validate_metadata_structure

logger = logging.getLogger(__name__)

class BaseService:
    """Base class for Nakala API services."""
    
    def __init__(self, client: NakalaClient):
        """Initialize the service with a Nakala client."""
        if not isinstance(client, NakalaClient):
            raise ValueError("client must be an instance of NakalaClient")
        self.client = client
        self.base_url = client.base_url
    
    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """Make a GET request to the API."""
        return self.client.get(endpoint, params=params, **kwargs)
    
    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """Make a POST request to the API."""
        return self.client.post(endpoint, json_data=data, **kwargs)
    
    def _put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """Make a PUT request to the API."""
        return self.client.put(endpoint, json_data=data, **kwargs)
    
    def _delete(self, endpoint: str, **kwargs) -> Any:
        """Make a DELETE request to the API."""
        return self.client.delete(endpoint, **kwargs)
    
    def _build_url(self, *parts: str) -> str:
        """Build a URL from parts, handling slashes properly."""
        return "/".join(str(part).strip("/") for part in parts if part)
    
    def _validate_metadata(self, metadata: Dict[str, Any], strict: bool = True) -> Tuple[bool, List[str]]:
        """
        Validate metadata against the Nakala schema.
        
        Args:
            metadata: Metadata dictionary to validate
            strict: If True, perform full validation including required fields and vocabularies.
                   If False, only validate the basic structure.
                   
        Returns:
            Tuple of (is_valid, error_messages)
        """
        if strict:
            return validate_metadata(metadata)
        return validate_metadata_structure(metadata)
    
    def _process_response(self, response: Any, expected_status: int = 200) -> Any:
        """
        Process an API response.
        
        Args:
            response: The response object from the requests library
            expected_status: The expected HTTP status code
            
        Returns:
            The parsed JSON response, or raises an exception
            
        Raises:
            NakalaAPIError: If the response status code doesn't match the expected status
        """
        if response.status_code != expected_status:
            try:
                error_data = response.json()
                message = error_data.get('message', 'Unknown error')
            except ValueError:
                message = response.text or 'Unknown error'
            
            raise NakalaAPIError(
                f"API request failed with status {response.status_code}: {message}",
                status_code=response.status_code,
                response=response
            )
        
        # For 204 No Content, return None
        if response.status_code == 204:
            return None
            
        # Try to parse JSON response
        try:
            return response.json()
        except ValueError:
            return response.text
