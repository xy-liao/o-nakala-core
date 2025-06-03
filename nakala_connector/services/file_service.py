"""
Service for managing files in Nakala.

This module provides functionality for uploading, retrieving,
and managing files in Nakala's storage system.
"""

import os
import mimetypes
from typing import Dict, List, Optional, Union, BinaryIO, Tuple

from ..exceptions import NakalaError, NakalaAPIError
from .base import BaseService


class FileService(BaseService):
    """Service for managing files in Nakala."""
    
    def upload_file(
        self,
        file_path: str,
        mime_type: Optional[str] = None,
        chunk_size: int = 1024 * 1024  # 1MB chunks
    ) -> Dict[str, Any]:
        """
        Upload a file to Nakala's temporary storage.
        
        Args:
            file_path: Path to the file to upload
            mime_type: MIME type of the file (optional, will be guessed if not provided)
            chunk_size: Size of chunks to use for streaming upload (in bytes)
            
        Returns:
            Dictionary containing file metadata including 'sha1' and 'embargo'
            
        Raises:
            NakalaError: If the file cannot be read or uploaded
        """
        if not os.path.isfile(file_path):
            raise NakalaError(f"File not found: {file_path}")
        
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'application/octet-stream'
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, mime_type)}
                return self._post("/datas/uploads", files=files)
        except OSError as e:
            raise NakalaError(f"Failed to read file {file_path}: {str(e)}") from e
    
    def get_file_info(self, file_id: str) -> Dict[str, Any]:
        """
        Get information about a file.
        
        Args:
            file_id: The ID or SHA1 hash of the file
            
        Returns:
            Dictionary containing file metadata
        """
        return self._get(f"/files/{file_id}")
    
    def download_file(
        self,
        file_id: str,
        output_path: Optional[str] = None,
        chunk_size: int = 1024 * 1024  # 1MB chunks
    ) -> str:
        """
        Download a file from Nakala.
        
        Args:
            file_id: The ID or SHA1 hash of the file to download
            output_path: Path where to save the downloaded file. If not provided,
                       the file will be saved in the current directory with its original name.
            chunk_size: Size of chunks to use for streaming download (in bytes)
            
        Returns:
            Path to the downloaded file
            
        Raises:
            NakalaError: If the download fails
        """
        # First get file info to get the filename
        file_info = self.get_file_info(file_id)
        filename = file_info.get('filename', file_id)
        
        # Determine output path
        if not output_path:
            output_path = filename
        elif os.path.isdir(output_path):
            output_path = os.path.join(output_path, filename)
        
        # Stream the download
        try:
            response = self.client._request(
                "GET",
                f"/files/{file_id}/download",
                stream=True
            )
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            
            return output_path
            
        except Exception as e:
            # Clean up partially downloaded file if it exists
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except OSError:
                    pass
            
            raise NakalaError(f"Failed to download file {file_id}: {str(e)}") from e
    
    def delete_file(self, file_id: str) -> bool:
        """
        Delete a file from Nakala.
        
        Args:
            file_id: The ID or SHA1 hash of the file to delete
            
        Returns:
            True if deletion was successful
            
        Raises:
            NakalaAPIError: If the deletion fails
        """
        self._delete(f"/files/{file_id}")
        return True
    
    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Get metadata for a file.
        
        Args:
            file_id: The ID or SHA1 hash of the file
            
        Returns:
            Dictionary containing file metadata
        """
        return self._get(f"/files/{file_id}/metadata")
    
    def update_file_metadata(
        self,
        file_id: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update metadata for a file.
        
        Args:
            file_id: The ID or SHA1 hash of the file
            metadata: Dictionary of metadata to update
            
        Returns:
            The updated file metadata
        """
        return self._put(f"/files/{file_id}/metadata", metadata)
    
    def list_files(
        self,
        data_id: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List files with optional filtering and pagination.
        
        Args:
            data_id: Filter by data object ID
            limit: Maximum number of results to return (default: 20)
            offset: Number of results to skip (for pagination)
            
        Returns:
            A dictionary containing the list of files and pagination info
        """
        params = {"limit": limit, "offset": offset}
        
        if data_id:
            params["dataId"] = data_id
        
        return self._get("/files", params=params)
