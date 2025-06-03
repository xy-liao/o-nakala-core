"""
Service for managing Nakala data objects.

This module provides functionality for creating, retrieving, updating,
and deleting Nakala data objects, which are the primary entities in Nakala.
"""

import os
import json
from typing import Dict, List, Optional, Union, Any, BinaryIO, Tuple
from datetime import datetime, date

from ..exceptions import NakalaError, NakalaAPIError, NakalaValidationError
from .base import BaseService
from ..metadata import validate_metadata, validate_metadata_structure


class DataService(BaseService):
    """Service for managing Nakala data objects."""
    
    def create_data(
        self,
        metadata: Dict[str, Any],
        files: Optional[List[Union[str, Dict[str, Any]]]] = None,
        collection_ids: Optional[List[str]] = None,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new data object in Nakala.
        
        Args:
            metadata: Metadata for the data object
            files: List of files to attach to the data object. Can be file paths or 
                  dictionaries with 'path' and optional 'mime_type' keys.
            collection_ids: List of collection IDs to add this data object to
            validate: If True, validate metadata before sending to the API
            
        Returns:
            The created data object
            
        Raises:
            NakalaValidationError: If metadata validation fails
            NakalaAPIError: If the API request fails
        """
        # Validate metadata if requested
        if validate:
            is_valid, errors = self._validate_metadata(metadata)
            if not is_valid:
                raise NakalaValidationError("Invalid metadata", errors=errors)
        
        # Prepare the request payload
        payload = {
            "status": metadata.get("status", "pending"),
            "metas": metadata.get("metas", []),
            "rights": metadata.get("rights", {})
        }
        
        # Add collection IDs if provided
        if collection_ids:
            payload["collectionIds"] = collection_ids
        
        # Add files if provided
        if files:
            uploaded_files = []
            for file_info in files:
                if isinstance(file_info, str):
                    file_path = file_info
                    mime_type = None
                else:
                    file_path = file_info.get("path")
                    mime_type = file_info.get("mime_type")
                
                if not file_path:
                    continue
                
                # Upload the file
                try:
                    upload_result = self.client.upload_file(file_path, mime_type)
                    uploaded_files.append({
                        "sha1": upload_result.get("sha1"),
                        "filename": os.path.basename(file_path),
                        "mimeType": mime_type
                    })
                except Exception as e:
                    raise NakalaError(f"Failed to upload file {file_path}: {str(e)}") from e
            
            if uploaded_files:
                payload["files"] = uploaded_files
        
        # Create the data object
        return self._post("/datas", payload)
    
    def get_data(self, data_id: str) -> Dict[str, Any]:
        """
        Get a data object by ID.
        
        Args:
            data_id: The ID of the data object to retrieve
            
        Returns:
            The data object
            
        Raises:
            NakalaAPIError: If the data object is not found or another error occurs
        """
        return self._get(f"/datas/{data_id}")
    
    def update_data(
        self,
        data_id: str,
        metadata: Optional[Dict[str, Any]] = None,
        files: Optional[List[Union[str, Dict[str, Any]]]] = None,
        collection_ids: Optional[List[str]] = None,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Update an existing data object.
        
        Args:
            data_id: The ID of the data object to update
            metadata: Updated metadata (only fields to update)
            files: List of files to add or update
            collection_ids: Updated list of collection IDs (replaces existing)
            validate: If True, validate metadata before sending to the API
            
        Returns:
            The updated data object
            
        Raises:
            NakalaValidationError: If metadata validation fails
            NakalaAPIError: If the update fails
        """
        # Get existing data
        current_data = self.get_data(data_id)
        
        # Prepare the update payload
        payload = {}
        
        # Update metadata if provided
        if metadata is not None:
            if validate:
                # For updates, we only validate the structure, not required fields
                is_valid, errors = self._validate_metadata(metadata, strict=False)
                if not is_valid:
                    raise NakalaValidationError("Invalid metadata", errors=errors)
            
            payload.update({
                "status": metadata.get("status", current_data.get("status")),
                "metas": metadata.get("metas", current_data.get("metas", [])),
                "rights": metadata.get("rights", current_data.get("rights", {}))
            })
        
        # Update collection IDs if provided
        if collection_ids is not None:
            payload["collectionIds"] = collection_ids
        
        # Handle file uploads if provided
        if files:
            uploaded_files = current_data.get("files", []).copy()
            
            for file_info in files:
                if isinstance(file_info, str):
                    file_path = file_info
                    mime_type = None
                    file_metadata = {}
                else:
                    file_path = file_info.get("path")
                    mime_type = file_info.get("mime_type")
                    file_metadata = {k: v for k, v in file_info.items() 
                                   if k not in ("path", "mime_type")}
                
                if not file_path:
                    continue
                
                # Upload the file
                try:
                    upload_result = self.client.upload_file(file_path, mime_type)
                    
                    # Check if file with same name exists
                    filename = os.path.basename(file_path)
                    file_exists = False
                    
                    for i, f in enumerate(uploaded_files):
                        if f.get("filename") == filename:
                            # Update existing file
                            uploaded_files[i] = {
                                "sha1": upload_result.get("sha1"),
                                "filename": filename,
                                "mimeType": mime_type or f.get("mimeType"),
                                **file_metadata,
                                "updatedAt": datetime.utcnow().isoformat() + "Z"
                            }
                            file_exists = True
                            break
                    
                    if not file_exists:
                        # Add new file
                        uploaded_files.append({
                            "sha1": upload_result.get("sha1"),
                            "filename": filename,
                            "mimeType": mime_type,
                            **file_metadata,
                            "createdAt": datetime.utcnow().isoformat() + "Z"
                        })
                        
                except Exception as e:
                    raise NakalaError(f"Failed to upload file {file_path}: {str(e)}") from e
            
            if uploaded_files:
                payload["files"] = uploaded_files
        
        # Send the update
        return self._put(f"/datas/{data_id}", payload)
    
    def delete_data(self, data_id: str) -> bool:
        """
        Delete a data object.
        
        Args:
            data_id: The ID of the data object to delete
            
        Returns:
            True if deletion was successful
            
        Raises:
            NakalaAPIError: If the deletion fails
        """
        self._delete(f"/datas/{data_id}")
        return True
    
    def list_data(
        self,
        status: Optional[str] = None,
        collection_id: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List data objects with optional filtering and pagination.
        
        Args:
            status: Filter by status (e.g., 'published', 'pending')
            collection_id: Filter by collection ID
            limit: Maximum number of results to return (default: 20)
            offset: Number of results to skip (for pagination)
            
        Returns:
            A dictionary containing the list of data objects and pagination info
        """
        params = {"limit": limit, "offset": offset}
        
        if status:
            params["status"] = status
        if collection_id:
            params["collectionId"] = collection_id
        
        return self._get("/datas", params=params)
    
    def get_data_files(self, data_id: str) -> List[Dict[str, Any]]:
        """
        Get the files associated with a data object.
        
        Args:
            data_id: The ID of the data object
            
        Returns:
            List of file metadata dictionaries
        """
        data = self.get_data(data_id)
        return data.get("files", [])
