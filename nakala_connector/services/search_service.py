"""
Search service for Nakala API.

This module provides functionality for searching and discovering
Nakala data objects and collections using various criteria.
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime, date

from ..exceptions import NakalaError, NakalaAPIError
from .base import BaseService


class SearchService(BaseService):
    """Service for searching Nakala data objects and collections."""
    
    def search(
        self,
        query: str = "*",
        filters: Optional[Dict[str, Any]] = None,
        collections: Optional[List[str]] = None,
        data_types: Optional[List[str]] = None,
        creators: Optional[List[str]] = None,
        contributors: Optional[List[str]] = None,
        subjects: Optional[List[str]] = None,
        temporal_start: Optional[Union[datetime, date, str]] = None,
        temporal_end: Optional[Union[datetime, date, str]] = None,
        spatial: Optional[List[Dict[str, Any]]] = None,
        licenses: Optional[List[str]] = None,
        status: Optional[str] = None,
        owner: Optional[str] = None,
        sort: Optional[str] = None,
        sort_order: str = "desc",
        limit: int = 20,
        offset: int = 0,
        facets: Optional[List[str]] = None,
        facet_limit: int = 10,
        facet_min_count: int = 1
    ) -> Dict[str, Any]:
        """
        Search for data objects in Nakala.
        
        Args:
            query: Search query string (supports Lucene query syntax)
            filters: Additional filters as key-value pairs
            collections: Filter by collection IDs
            data_types: Filter by data types (e.g., ['Dataset', 'Image'])
            creators: Filter by creator names or IDs
            contributors: Filter by contributor names or IDs
            subjects: Filter by subject terms
            temporal_start: Filter by start date (inclusive)
            temporal_end: Filter by end date (inclusive)
            spatial: Filter by spatial coverage (list of GeoJSON objects)
            licenses: Filter by license URIs
            status: Filter by status (e.g., 'published', 'pending')
            owner: Filter by owner ID
            sort: Field to sort by (e.g., 'title', 'created', 'modified')
            sort_order: Sort order ('asc' or 'desc')
            limit: Maximum number of results to return (default: 20)
            offset: Number of results to skip (for pagination)
            facets: List of fields to compute facets for
            facet_limit: Maximum number of facet values to return
            facet_min_count: Minimum count for a facet value to be included
            
        Returns:
            Dictionary containing search results and facets
        """
        params = {
            "q": query,
            "limit": limit,
            "offset": offset,
            "facet.limit": facet_limit,
            "facet.mincount": facet_min_count
        }
        
        # Add filters
        if filters:
            for field, value in filters.items():
                params[f"fq"] = f"{field}:{value}"
        
        # Add collection filters
        if collections:
            params["collection"] = collections
        
        # Add data type filters
        if data_types:
            params["type"] = data_types
        
        # Add creator filters
        if creators:
            params["creator"] = creators
        
        # Add contributor filters
        if contributors:
            params["contributor"] = contributors
        
        # Add subject filters
        if subjects:
            params["subject"] = subjects
        
        # Add temporal filters
        if temporal_start:
            if isinstance(temporal_start, (datetime, date)):
                temporal_start = temporal_start.isoformat()
            params["temporal_start"] = temporal_start
        
        if temporal_end:
            if isinstance(temporal_end, (datetime, date)):
                temporal_end = temporal_end.isoformat()
            params["temporal_end"] = temporal_end
        
        # Add spatial filters
        if spatial:
            params["spatial"] = spatial
        
        # Add license filters
        if licenses:
            params["license"] = licenses
        
        # Add status filter
        if status:
            params["status"] = status
        
        # Add owner filter
        if owner:
            params["owner"] = owner
        
        # Add sorting
        if sort:
            sort_order = sort_order.lower()
            if sort_order not in ("asc", "desc"):
                sort_order = "desc"
            params["sort"] = f"{sort} {sort_order}"
        
        # Add facets
        if facets:
            params["facet.field"] = facets
        
        return self._get("/search", params=params)
    
    def search_collections(
        self,
        query: str = "*",
        owner: Optional[str] = None,
        sort: Optional[str] = None,
        sort_order: str = "desc",
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for collections in Nakala.
        
        Args:
            query: Search query string (supports Lucene query syntax)
            owner: Filter by owner ID
            sort: Field to sort by (e.g., 'title', 'created', 'modified')
            sort_order: Sort order ('asc' or 'desc')
            limit: Maximum number of results to return (default: 20)
            offset: Number of results to skip (for pagination)
            
        Returns:
            Dictionary containing search results and pagination info
        """
        params = {
            "q": query,
            "limit": limit,
            "offset": offset
        }
        
        # Add owner filter
        if owner:
            params["owner"] = owner
        
        # Add sorting
        if sort:
            sort_order = sort_order.lower()
            if sort_order not in ("asc", "desc"):
                sort_order = "desc"
            params["sort"] = f"{sort} {sort_order}"
        
        return self._get("/search/collections", params=params)
    
    def get_facets(
        self,
        field: str,
        query: str = "*",
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        min_count: int = 1
    ) -> Dict[str, int]:
        """
        Get facet counts for a specific field.
        
        Args:
            field: The field to get facets for
            query: Search query to filter the results
            filters: Additional filters as key-value pairs
            limit: Maximum number of facet values to return
            min_count: Minimum count for a facet value to be included
            
        Returns:
            Dictionary mapping facet values to their counts
        """
        params = {
            "q": query,
            "facet.field": field,
            "facet": "true",
            "facet.limit": limit,
            "facet.mincount": min_count,
            "rows": 0  # We only want facets, not results
        }
        
        # Add filters
        if filters:
            for f, v in filters.items():
                params[f"fq"] = f"{f}:{v}"
        
        response = self._get("/search", params=params)
        
        # Extract facets from response
        facets = {}
        if "facet_counts" in response and "facet_fields" in response["facet_counts"]:
            facet_data = response["facet_counts"]["facet_fields"].get(field, [])
            # Facet data comes as a flat list of [value, count, value, count, ...]
            for i in range(0, len(facet_data), 2):
                if i + 1 < len(facet_data):
                    facets[facet_data[i]] = facet_data[i + 1]
        
        return facets
    
    def suggest(
        self,
        query: str,
        field: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get search suggestions for a query.
        
        Args:
            query: The query to get suggestions for
            field: The field to get suggestions from (e.g., 'title', 'creator')
            limit: Maximum number of suggestions to return
            
        Returns:
            List of suggestion dictionaries with 'term' and 'count' keys
        """
        params = {
            "q": query,
            "suggest": "true",
            "suggest.dictionary": field if field else "default",
            "suggest.count": limit
        }
        
        response = self._get("/suggest", params=params)
        
        # Extract suggestions from response
        suggestions = []
        if "suggest" in response and field in response["suggest"]:
            suggestions = [
                {"term": term, "count": data["numFound"]}
                for term, data in response["suggest"][field].items()
            ]
        
        return suggestions
