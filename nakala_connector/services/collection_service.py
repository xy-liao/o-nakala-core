"""
Service for managing Nakala collections.

This module provides functionality for creating, retrieving, updating,
and deleting collections of data objects in Nakala.
"""

from typing import Dict, List, Optional, Any

from ..exceptions import NakalaError, NakalaAPIError, NakalaValidationError
from .base import BaseService


class CollectionService(BaseService):
    """Service for managing Nakala collections."""
    
    def create_collection(
        self,
        title: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        data_ids: Optional[List[str]] = None,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new collection.
        
        Args:
            title: Title of the collection
            description: Description of the collection
            metadata: Additional metadata for the collection
            data_ids: List of data object IDs to include in the collection
            validate: If True, validate metadata before sending to the API
            
        Returns:
            The created collection
            
        Raises:
            NakalaValidationError: If metadata validation fails
            NakalaAPIError: If the creation fails
        """
        payload = {
            "title": title,
            "description": description or "",
            "metadata": metadata or {},
            "dataIds": data_ids or []
        }
        
        return self._post("/collections", payload)
    
    def get_collection(self, collection_id: str) -> Dict[str, Any]:
        """
        Get a collection by ID.
        
        Args:
            collection_id: The ID of the collection to retrieve
            
        Returns:
            The collection
            
        Raises:
            NakalaAPIError: If the collection is not found or another error occurs
        """
        return self._get(f"/collections/{collection_id}")
    
    def update_collection(
        self,
        collection_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        data_ids: Optional[List[str]] = None,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Update a collection.
        
        Args:
            collection_id: The ID of the collection to update
            title: New title for the collection
            description: New description for the collection
            metadata: Updated metadata (replaces existing metadata)
            data_ids: Updated list of data object IDs (replaces existing data objects)
            validate: If True, validate metadata before sending to the API
            
        Returns:
            The updated collection
            
        Raises:
            NakalaAPIError: If the update fails
        """
        # Get current collection data
        current = self.get_collection(collection_id)
        
        # Prepare update payload
        payload = {
            "title": title if title is not None else current["title"],
            "description": description if description is not None else current.get("description", ""),
            "metadata": metadata if metadata is not None else current.get("metadata", {}),
            "dataIds": data_ids if data_ids is not None else current.get("dataIds", [])
        }
        
        return self._put(f"/collections/{collection_id}", payload)
    
    def delete_collection(self, collection_id: str) -> bool:
        """
        Delete a collection.
        
        Args:
            collection_id: The ID of the collection to delete
            
        Returns:
            True if deletion was successful
            
        Raises:
            NakalaAPIError: If the deletion fails
        """
        self._delete(f"/collections/{collection_id}")
        return True
    
    def list_collections(
        self,
        query: Optional[str] = None,
        owner: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List collections with optional filtering and pagination.
        
        Args:
            query: Search query to filter collections by title or description
            owner: Filter by owner ID
            limit: Maximum number of results to return (default: 20)
            offset: Number of results to skip (for pagination)
            
        Returns:
            A dictionary containing the list of collections and pagination info
        """
        params = {"limit": limit, "offset": offset}
        
        if query:
            params["q"] = query
        if owner:
            params["owner"] = owner
        
        return self._get("/collections", params=params)
    
    def add_to_collection(self, collection_id: str, data_ids: List[str]) -> Dict[str, Any]:
        """
        Add data objects to a collection.
        
        Args:
            collection_id: The ID of the collection
            data_ids: List of data object IDs to add to the collection
            
        Returns:
            The updated collection
        """
        current = self.get_collection(collection_id)
        current_ids = set(current.get("dataIds", []))
        updated_ids = list(current_ids.union(data_ids))
        
        return self.update_collection(collection_id, data_ids=updated_ids)
    
    def remove_from_collection(self, collection_id: str, data_ids: List[str]) -> Dict[str, Any]:
        """
        Remove data objects from a collection.
        
        Args:
            collection_id: The ID of the collection
            data_ids: List of data object IDs to remove from the collection
            
        Returns:
            The updated collection
        """
        current = self.get_collection(collection_id)
        current_ids = set(current.get("dataIds", []))
        updated_ids = list(current_ids - set(data_ids))
        
        return self.update_collection(collection_id, data_ids=updated_ids)
    
    def get_collection_data(
        self,
        collection_id: str,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get the data objects in a collection.
        
        Args:
            collection_id: The ID of the collection
            status: Filter by data object status (e.g., 'published', 'pending')
            limit: Maximum number of results to return (default: 20)
            offset: Number of results to skip (for pagination)
            
        Returns:
            A dictionary containing the list of data objects and pagination info
        """
        params = {"limit": limit, "offset": offset}
        
        if status:
            params["status"] = status
        
        return self._get(f"/collections/{collection_id}/datas", params=params)
