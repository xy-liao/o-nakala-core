"""
Nakala API client implementation.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, Union
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    NakalaError,
    NakalaAPIError,
    NakalaAuthenticationError,
    NakalaNotFoundError,
    NakalaRateLimitError
)

class NakalaClient:
    """Main client for interacting with the Nakala API.
    
    This client handles authentication, request/response processing,
    and provides access to various API services.
    """
    
    BASE_URL = "https://api.nakala.fr"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """Initialize the Nakala client.
        
        Args:
            api_key: Your Nakala API key. If not provided, will look for NAKALA_API_KEY environment variable.
            base_url: Base URL for the API (defaults to production API).
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
        """
        self.api_key = api_key or os.getenv("NAKALA_API_KEY")
        if not self.api_key:
            raise NakalaAuthenticationError(
                "API key is required. Either pass it to the constructor or set NAKALA_API_KEY environment variable."
            )
            
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        
        # Configure session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Set default headers
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict] = None,
        stream: bool = False
    ) -> Any:
        """Make an HTTP request to the Nakala API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., '/datas')
            params: Query parameters
            json_data: JSON payload for POST/PUT requests
            files: Files to upload (for multipart/form-data)
            stream: Whether to stream the response
            
        Returns:
            Parsed JSON response or raw response if stream=True
            
        Raises:
            NakalaAPIError: If the API returns an error
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # Create a copy of headers to modify
        headers = {}
        
        # For file uploads, don't set Content-Type header (let requests handle it with boundary)
        if not files:
            headers.update(self.session.headers)
        else:
            # Only include necessary headers for file uploads
            headers['X-API-KEY'] = self.api_key
            headers['Accept'] = 'application/json'
        
        try:
            # For file uploads, use data instead of json
            if files:
                logger = logging.getLogger(__name__)
                logger.debug(f"Sending {method} request to {url}")
                logger.debug(f"Headers: {headers}")
                logger.debug(f"Files: {list(files.keys())}")
                
                # Log file info without the file object itself
                file_info = {}
                for field, (filename, fileobj, content_type) in files.items():
                    file_info[field] = {
                        'filename': filename,
                        'content_type': content_type,
                        'size': getattr(fileobj, 'tell', lambda: 'unknown')()
                    }
                logger.debug(f"File details: {file_info}")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data={},  # Empty dict for multipart/form-data
                    files=files,
                    stream=stream,
                    timeout=self.timeout
                )
                
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response headers: {dict(response.headers)}")
                try:
                    logger.debug(f"Response body: {response.text[:500]}")
                except Exception as e:
                    logger.debug(f"Could not log response body: {str(e)}")
            else:
                logger = logging.getLogger(__name__)
                logger.debug(f"Sending {method} request to {url}")
                logger.debug(f"Headers: {headers}")
                if json_data:
                    logger.debug(f"JSON data: {json_data}")
                if params:
                    logger.debug(f"Params: {params}")
                    
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json_data,
                    stream=stream,
                    timeout=self.timeout
                )
                
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response headers: {dict(response.headers)}")
                try:
                    logger.debug(f"Response body: {response.text[:500]}")
                except Exception as e:
                    logger.debug(f"Could not log response body: {str(e)}")
            
            # Handle error responses
            if response.status_code >= 400:
                self._handle_error_response(response)
                
            # Return appropriate response
            if stream:
                return response
                
            if response.status_code == 204:  # No Content
                return None
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise NakalaAPIError(f"Request failed: {str(e)}") from e
    
    def _handle_error_response(self, response: requests.Response) -> None:
        """Handle API error responses."""
        try:
            error_data = response.json()
            message = error_data.get('message', 'Unknown error')
        except ValueError:
            message = response.text or 'Unknown error'
        
        if response.status_code == 401:
            raise NakalaAuthenticationError("Authentication failed. Check your API key.")
        elif response.status_code == 404:
            raise NakalaNotFoundError(message)
        elif response.status_code == 429:
            raise NakalaRateLimitError("Rate limit exceeded. Please try again later.")
        else:
            raise NakalaAPIError(
                f"API request failed with status {response.status_code}: {message}",
                status_code=response.status_code,
                response=response
            )
    
    # Convenience methods for common HTTP methods
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return self._request("GET", endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return self._request("POST", endpoint, json_data=json_data, **kwargs)
    
    def put(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return self._request("PUT", endpoint, json_data=json_data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Any:
        return self._request("DELETE", endpoint, **kwargs)
    
    def upload_file(self, file_path: str, mime_type: Optional[str] = None) -> Dict[str, Any]:
        """Upload a file to Nakala's temporary storage.
        
        Args:
            file_path: Path to the file to upload
            mime_type: MIME type of the file (optional, will be guessed if not provided)
            
        Returns:
            Dictionary containing file metadata including 'sha1' and 'embargo'
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, mime_type)}
                return self.post("/datas/uploads", files=files)
        except OSError as e:
            raise NakalaError(f"Failed to read file {file_path}: {str(e)}") from e

    def close(self):
        """Close the underlying session."""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
