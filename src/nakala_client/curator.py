"""
Nakala Curator Client

Provides data curation and quality management tools including batch modifications,
metadata validation, duplicate detection, and data consistency checking.
"""

import csv
import json
import logging
import argparse
import time
import requests
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

# Import common utilities
from .common.config import NakalaConfig
from .common.exceptions import NakalaAPIError
from .common.utils import NakalaCommonUtils, setup_common_logging

from .user_info import NakalaUserInfoClient

logger = logging.getLogger(__name__)


# Comprehensive field mapping for CSV parsing
CSV_FIELD_MAPPINGS = {
    'new_title': {
        'api_field': 'title',
        'property_uri': 'http://nakala.fr/terms#title',
        'multilingual': True,
        'required': True
    },
    'new_description': {
        'api_field': 'description',
        'property_uri': 'http://purl.org/dc/terms/description',
        'multilingual': True,
        'required': True
    },
    'new_keywords': {
        'api_field': 'keywords',
        'property_uri': 'http://purl.org/dc/terms/subject',
        'multilingual': True,
        'required': False
    },
    'new_author': {
        'api_field': 'creator',
        'property_uri': 'http://nakala.fr/terms#creator',
        'multilingual': False,
        'required': True,
        'format': 'array'
    },
    'new_contributor': {
        'api_field': 'contributor',
        'property_uri': 'http://purl.org/dc/terms/contributor',
        'multilingual': False,
        'required': False,
        'format': 'array'
    },
    'new_license': {
        'api_field': 'license',
        'property_uri': 'http://nakala.fr/terms#license',
        'multilingual': False,
        'required': True
    },
    'new_type': {
        'api_field': 'type',
        'property_uri': 'http://nakala.fr/terms#type',
        'multilingual': False,
        'required': True
    },
    'new_date': {
        'api_field': 'date',
        'property_uri': 'http://nakala.fr/terms#created',
        'multilingual': False,
        'required': True
    },
    'new_language': {
        'api_field': 'language',
        'property_uri': 'http://purl.org/dc/terms/language',
        'multilingual': False,
        'required': False
    },
    'new_temporal': {
        'api_field': 'temporal',
        'property_uri': 'http://purl.org/dc/terms/coverage',
        'multilingual': False,
        'required': False
    },
    'new_spatial': {
        'api_field': 'spatial',
        'property_uri': 'http://purl.org/dc/terms/coverage',
        'multilingual': False,
        'required': False
    },
    'new_relation': {
        'api_field': 'relation',
        'property_uri': 'http://purl.org/dc/terms/relation',
        'multilingual': False,
        'required': False
    },
    'new_source': {
        'api_field': 'source',
        'property_uri': 'http://purl.org/dc/terms/source',
        'multilingual': False,
        'required': False
    },
    'new_identifier': {
        'api_field': 'identifier',
        'property_uri': 'http://purl.org/dc/terms/identifier',
        'multilingual': False,
        'required': False
    },
    'new_alternative': {
        'api_field': 'alternative',
        'property_uri': 'http://purl.org/dc/terms/alternative',
        'multilingual': True,
        'required': False
    },
    'new_publisher': {
        'api_field': 'publisher',
        'property_uri': 'http://purl.org/dc/terms/publisher',
        'multilingual': False,
        'required': False
    }
}


class CuratorConfig:
    """Extended configuration for curator operations."""

    def __init__(self, **kwargs):
        # Extract curator-specific settings
        self.batch_size = kwargs.pop("batch_size", 50)
        self.concurrent_operations = kwargs.pop("concurrent_operations", 3)
        self.validation_batch_size = kwargs.pop("validation_batch_size", 100)
        self.skip_existing = kwargs.pop("skip_existing", True)
        self.validate_before_modification = kwargs.pop(
            "validate_before_modification", True
        )
        self.backup_before_changes = kwargs.pop("backup_before_changes", True)
        self.duplicate_threshold = kwargs.pop("duplicate_threshold", 0.85)
        self.max_modifications_per_batch = kwargs.pop(
            "max_modifications_per_batch", 100
        )
        self.require_confirmation = kwargs.pop("require_confirmation", True)
        self.dry_run_default = kwargs.pop("dry_run_default", True)

        # Initialize base config with remaining kwargs
        self.base_config = NakalaConfig(**kwargs)

    def __getattr__(self, name):
        """Delegate attribute access to base config."""
        return getattr(self.base_config, name)


class BatchModificationResult:
    """Container for batch modification results."""

    def __init__(self):
        self.successful: List[Dict[str, Any]] = []
        self.failed: List[Dict[str, Any]] = []
        self.skipped: List[Dict[str, Any]] = []
        self.warnings: List[str] = []
        self.start_time: datetime = datetime.now()
        self.end_time: Optional[datetime] = None

    def add_success(self, item_id: str, changes: Dict[str, Any]):
        """Record successful modification."""
        self.successful.append(
            {"id": item_id, "changes": changes, "timestamp": datetime.now().isoformat()}
        )

    def add_failure(self, item_id: str, error: str, attempted_changes: Dict[str, Any]):
        """Record failed modification."""
        self.failed.append(
            {
                "id": item_id,
                "error": error,
                "attempted_changes": attempted_changes,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def add_skip(self, item_id: str, reason: str):
        """Record skipped modification."""
        self.skipped.append(
            {"id": item_id, "reason": reason, "timestamp": datetime.now().isoformat()}
        )

    def add_warning(self, message: str):
        """Add warning message."""
        self.warnings.append(f"{datetime.now().isoformat()}: {message}")

    def finalize(self):
        """Mark operation as complete."""
        self.end_time = datetime.now()

    def get_summary(self) -> Dict[str, Any]:
        """Get operation summary."""
        duration = None
        if self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()

        return {
            "total_processed": len(self.successful)
            + len(self.failed)
            + len(self.skipped),
            "successful": len(self.successful),
            "failed": len(self.failed),
            "skipped": len(self.skipped),
            "warnings": len(self.warnings),
            "duration_seconds": duration,
            "success_rate": len(self.successful)
            / max(1, len(self.successful) + len(self.failed))
            * 100,
        }


class NakalaMetadataValidator:
    """Validates metadata against Nakala requirements and best practices."""

    def __init__(self, config: CuratorConfig):
        self.config = config
        self.utils = NakalaCommonUtils()

    def validate_required_fields(
        self, metadata: Dict[str, Any], validation_mode: str = "creation"
    ) -> List[str]:
        """Validate required metadata fields with different modes for creation vs modification.

        Args:
            metadata: The metadata to validate
            validation_mode: 'creation' (strict) or 'modification' (permissive)
        """
        errors = []

        if validation_mode == "creation":
            # Strict validation for new resources
            required_fields = ["title", "creator", "description"]
            for field in required_fields:
                if not metadata.get(field):
                    errors.append(f"Required field '{field}' is missing or empty")

        elif validation_mode == "modification":
            # Permissive validation for modifications - only validate fields that are present
            # This allows partial updates without requiring all fields

            # Only validate structure/format of fields that are provided
            if "title" in metadata:
                title = metadata.get("title", "").strip()
                if not title:
                    errors.append("Title cannot be empty when provided")

            if "description" in metadata:
                desc = metadata.get("description", "").strip()
                if not desc:
                    errors.append("Description cannot be empty when provided")

            # Note: 'creator' is not required for modifications as it might be inherited
            # from existing metadata or handled at the API level

        return errors

    def validate_controlled_vocabularies(self, metadata: Dict[str, Any]) -> List[str]:
        """Validate controlled vocabulary values."""
        warnings = []

        # Language validation
        if "language" in metadata:
            lang = metadata["language"]
            if lang not in ["fr", "en", "de", "es", "it"]:
                warnings.append(f"Language '{lang}' might not be supported")

        # License validation
        if "license" in metadata:
            license_val = metadata["license"]
            valid_licenses = ["CC-BY-4.0", "CC-BY-SA-4.0", "CC-BY-NC-4.0", "CC0-1.0"]
            if license_val not in valid_licenses:
                warnings.append(f"License '{license_val}' is not in recommended list")

        return warnings

    def validate_metadata_quality(
        self, metadata: Dict[str, Any], validation_mode: str = "creation"
    ) -> Dict[str, List[str]]:
        """Comprehensive metadata quality validation.

        Args:
            metadata: The metadata to validate
            validation_mode: 'creation' (strict) or 'modification' (permissive)
        """
        results = {
            "errors": self.validate_required_fields(metadata, validation_mode),
            "warnings": self.validate_controlled_vocabularies(metadata),
            "suggestions": [],
        }

        # Quality suggestions
        if metadata.get("title") and len(metadata["title"]) < 10:
            results["suggestions"].append("Title is very short, consider expanding")

        if metadata.get("description") and len(metadata["description"]) < 50:
            results["suggestions"].append(
                "Description is brief, consider adding more detail"
            )

        if not metadata.get("keywords"):
            results["suggestions"].append(
                "Consider adding keywords for better discoverability"
            )

        return results


class NakalaDuplicateDetector:
    """Detects potential duplicates in datasets and collections."""

    def __init__(self, config: CuratorConfig):
        self.config = config
        self.threshold = config.duplicate_threshold

    def calculate_similarity(
        self, item1: Dict[str, Any], item2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between two items based on metadata."""
        # Simple text-based similarity for now
        text1 = f"{item1.get('title', '')} {item1.get('description', '')}"
        text2 = f"{item2.get('title', '')} {item2.get('description', '')}"

        # Jaccard similarity on words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 and not words2:
            return 0.0

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return intersection / union if union > 0 else 0.0

    def find_duplicates(
        self, items: List[Dict[str, Any]]
    ) -> List[Tuple[Dict[str, Any], Dict[str, Any], float]]:
        """Find potential duplicates in a list of items."""
        duplicates = []

        for i, item1 in enumerate(items):
            for item2 in items[i + 1 :]:
                similarity = self.calculate_similarity(item1, item2)
                if similarity >= self.threshold:
                    duplicates.append((item1, item2, similarity))

        return duplicates


class NakalaCuratorClient:
    """Main curator client for batch operations and quality management."""

    def __init__(self, config):
        # Handle both NakalaConfig and CuratorConfig for backward compatibility
        if isinstance(config, NakalaConfig):
            # Auto-wrap NakalaConfig in CuratorConfig
            self.config = CuratorConfig(
                api_url=config.api_url,
                api_key=config.api_key,
                timeout=getattr(config, 'timeout', 30)
            )
        elif isinstance(config, CuratorConfig):
            self.config = config
        else:
            raise TypeError(f"Expected NakalaConfig or CuratorConfig, got {type(config)}")
            
        self.utils = NakalaCommonUtils()
        self.validator = NakalaMetadataValidator(self.config)
        self.duplicate_detector = NakalaDuplicateDetector(self.config)
        self.user_client = NakalaUserInfoClient(self.config)

    def parse_csv_modifications(self, csv_path: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Parse CSV modifications with comprehensive field support.
        
        Returns:
            Tuple of (modifications_list, unsupported_fields_list)
        """
        modifications = []
        unsupported_fields = set()
        
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, start=2):  # Start at 2 for line numbers (header is line 1)
                    if row.get("action") == "modify":
                        changes = {}
                        
                        # Process all potential modification fields
                        for csv_field, value in row.items():
                            if csv_field and csv_field.startswith('new_') and value and str(value).strip():
                                if csv_field in CSV_FIELD_MAPPINGS:
                                    field_config = CSV_FIELD_MAPPINGS[csv_field]
                                    api_field = field_config['api_field']
                                    
                                    # Handle array format fields (like creator, contributor)
                                    if field_config.get('format') == 'array':
                                        # Convert semicolon-separated values to array
                                        changes[api_field] = [v.strip() for v in str(value).split(';') if v.strip()]
                                    else:
                                        changes[api_field] = str(value).strip()
                                        
                                    logger.debug(f"Row {row_num}: Mapped {csv_field} -> {api_field} = {changes[api_field]}")
                                else:
                                    unsupported_fields.add(csv_field)
                        
                        if changes:
                            modifications.append({
                                "id": row["id"], 
                                "changes": changes,
                                "row_number": row_num
                            })
                        elif not any(row.get(f) for f in CSV_FIELD_MAPPINGS.keys()):
                            logger.warning(f"Row {row_num}: No recognized modification fields found")
        
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        except Exception as e:
            raise Exception(f"Error parsing CSV file {csv_path}: {e}")
        
        # Log warnings for unsupported fields
        if unsupported_fields:
            logger.warning(f"Unsupported CSV fields ignored: {sorted(unsupported_fields)}")
            logger.info(f"Supported fields: {sorted(CSV_FIELD_MAPPINGS.keys())}")
        
        return modifications, list(unsupported_fields)

    def _format_field_value(self, value: str, field_config: Dict[str, Any]) -> Any:
        """Format field value according to its configuration."""
        if field_config.get('format') == 'array':
            # Convert semicolon-separated values to array
            return [v.strip() for v in value.split(';') if v.strip()]
        return value.strip()

    def batch_validate_metadata(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate metadata for multiple items."""
        logger.info(f"Validating metadata for {len(items)} items...")

        results = {
            "total_items": len(items),
            "valid_items": 0,
            "items_with_errors": 0,
            "items_with_warnings": 0,
            "validation_details": [],
        }

        for item in items:
            item_id = item.get("id", "unknown")
            validation = self.validator.validate_metadata_quality(item)

            has_errors = len(validation["errors"]) > 0
            has_warnings = len(validation["warnings"]) > 0

            if not has_errors:
                results["valid_items"] += 1
            else:
                results["items_with_errors"] += 1

            if has_warnings:
                results["items_with_warnings"] += 1

            results["validation_details"].append(
                {
                    "id": item_id,
                    "title": item.get("title", ""),
                    "errors": validation["errors"],
                    "warnings": validation["warnings"],
                    "suggestions": validation["suggestions"],
                }
            )

        return results

    def batch_modify_metadata(
        self, modifications: List[Dict[str, Any]], dry_run: bool = True
    ) -> BatchModificationResult:
        """Apply metadata modifications in batches."""
        logger.info(
            f"{'DRY RUN: ' if dry_run else ''}Processing {len(modifications)} metadata modifications..."
        )

        result = BatchModificationResult()

        # Process in batches
        for batch_start in range(0, len(modifications), self.config.batch_size):
            batch_end = min(batch_start + self.config.batch_size, len(modifications))
            batch = modifications[batch_start:batch_end]

            logger.info(
                f"Processing batch {batch_start//self.config.batch_size + 1}: items {batch_start+1}-{batch_end}"
            )

            self._process_modification_batch(batch, result, dry_run)

            # Small delay between batches to avoid overwhelming API
            time.sleep(0.5)

        result.finalize()
        return result

    def _process_modification_batch(
        self,
        batch: List[Dict[str, Any]],
        result: BatchModificationResult,
        dry_run: bool,
    ):
        """Process a single batch of modifications."""
        for modification in batch:
            item_id = modification.get("id", "unknown")
            changes = modification.get("changes", {})

            try:
                # Validate before modification if enabled
                if self.config.validate_before_modification:
                    # Use modification-specific validation (more permissive than creation)
                    # Only validate the changes being made, not the complete metadata
                    validation = self.validator.validate_metadata_quality(
                        changes, validation_mode="modification"
                    )

                    if validation["errors"]:
                        result.add_failure(
                            item_id,
                            f"Validation failed: {validation['errors']}",
                            changes,
                        )
                        continue

                # Apply modification (or simulate in dry run)
                if dry_run:
                    logger.debug(
                        f"DRY RUN: Would modify {item_id} with changes: {changes}"
                    )
                    result.add_success(item_id, changes)
                else:
                    # Here you would make actual API calls to modify the item
                    success = self._apply_modification(item_id, changes)
                    if success:
                        result.add_success(item_id, changes)
                    else:
                        result.add_failure(item_id, "API modification failed", changes)

            except Exception as e:
                result.add_failure(item_id, str(e), changes)

    def _determine_item_type(self, item_id: str) -> str:
        """Determine if an item is a collection or dataset by trying both endpoints."""
        headers = {"X-API-KEY": self.config.api_key}

        # Try collections endpoint first
        try:
            url = f"{self.config.api_url}/collections/{item_id}"
            response = requests.get(url, headers=headers, timeout=self.config.timeout)
            if response.status_code == 200:
                return "collection"
        except:
            pass

        # Try datasets endpoint
        try:
            url = f"{self.config.api_url}/datas/{item_id}"
            response = requests.get(url, headers=headers, timeout=self.config.timeout)
            if response.status_code == 200:
                return "dataset"
        except:
            pass

        return "unknown"

    def _apply_modification(self, item_id: str, changes: Dict[str, Any]) -> bool:
        """Apply actual modification via API with comprehensive field support."""
        try:
            headers = {"X-API-KEY": self.config.api_key}

            # Try datasets first (most common), then collections if 404
            dataset_url = f"{self.config.api_url}/datas/{item_id}"
            collection_url = f"{self.config.api_url}/collections/{item_id}"
            
            # Single API call to get current data
            response = requests.get(dataset_url, headers=headers, timeout=self.config.timeout)
            
            if response.status_code == 404:
                # Try collections endpoint
                response = requests.get(collection_url, headers=headers, timeout=self.config.timeout)
                if response.status_code == 404:
                    logger.error(f"Item {item_id} not found in datasets or collections")
                    return False
                url = collection_url
            else:
                response.raise_for_status()
                url = dataset_url

            current_data = response.json()
            current_metas = current_data.get("metas", [])

            # Build new metadata array
            new_metas = []

            # Find field configurations for the changes being made
            changing_uris = set()
            for field_name in changes.keys():
                field_config = self._find_field_config_by_api_name(field_name)
                if field_config:
                    changing_uris.add(field_config['property_uri'])

            # Keep existing metas that we're not changing
            for meta in current_metas:
                property_uri = meta.get("propertyUri", "")
                if property_uri not in changing_uris:
                    new_metas.append(meta)

            # Add new/modified metadata using comprehensive field mapping
            for field_name, new_value in changes.items():
                field_config = self._find_field_config_by_api_name(field_name)
                if not field_config:
                    logger.warning(f"No configuration found for field {field_name}, skipping")
                    continue

                property_uri = field_config['property_uri']
                is_multilingual = field_config.get('multilingual', False)
                is_array = field_config.get('format') == 'array'

                if is_array:
                    # Handle array fields like creator, contributor
                    if isinstance(new_value, list):
                        new_metas.append({
                            "value": new_value,
                            "propertyUri": property_uri,
                            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
                        })
                    else:
                        # Convert string to array if needed
                        array_value = [v.strip() for v in str(new_value).split(';') if v.strip()]
                        new_metas.append({
                            "value": array_value,
                            "propertyUri": property_uri,
                            "typeUri": "http://www.w3.org/2001/XMLSchema#string"
                        })
                elif is_multilingual:
                    # Handle multilingual fields like title, description, keywords
                    if "|" in str(new_value):
                        parts = str(new_value).split("|")
                        for part in parts:
                            if part.startswith("fr:"):
                                content = part[3:]
                                if field_name == "keywords":
                                    # Handle semicolon-separated keywords
                                    keywords = content.split(";")
                                    for keyword in keywords:
                                        if keyword.strip():
                                            new_metas.append({
                                                "value": keyword.strip(),
                                                "lang": "fr",
                                                "propertyUri": property_uri,
                                            })
                                else:
                                    new_metas.append({
                                        "value": content,
                                        "lang": "fr",
                                        "propertyUri": property_uri,
                                    })
                            elif part.startswith("en:"):
                                content = part[3:]
                                if field_name == "keywords":
                                    # Handle semicolon-separated keywords
                                    keywords = content.split(";")
                                    for keyword in keywords:
                                        if keyword.strip():
                                            new_metas.append({
                                                "value": keyword.strip(),
                                                "lang": "en",
                                                "propertyUri": property_uri,
                                            })
                                else:
                                    new_metas.append({
                                        "value": content,
                                        "lang": "en",
                                        "propertyUri": property_uri,
                                    })
                    else:
                        # Default to French if no language specified
                        new_metas.append({
                            "value": str(new_value),
                            "lang": "fr",
                            "propertyUri": property_uri,
                        })
                else:
                    # Handle simple non-multilingual fields
                    meta_entry = {
                        "value": str(new_value),
                        "propertyUri": property_uri,
                    }
                    
                    # Add typeUri for certain fields
                    if field_name == "type":
                        meta_entry["typeUri"] = "http://purl.org/dc/terms/URI"
                    
                    new_metas.append(meta_entry)

            # Prepare update payload
            update_payload = {"metas": new_metas}

            # Debug: Log the payload being sent
            logger.debug(f"Sending payload for {item_id}: {update_payload}")

            # Apply the modification
            headers["Content-Type"] = "application/json"
            response = requests.put(
                url, headers=headers, json=update_payload, timeout=self.config.timeout
            )
            
            # Log error details for debugging
            if response.status_code != 204:
                logger.error(f"API Error {response.status_code}: {response.text}")
            
            response.raise_for_status()

            logger.info(f"Successfully applied changes to {item_id}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to apply modification to {item_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error processing modification for {item_id}: {e}")
            return False

    def _find_field_config_by_api_name(self, api_field_name: str) -> Optional[Dict[str, Any]]:
        """Find field configuration by API field name."""
        for config in CSV_FIELD_MAPPINGS.values():
            if config['api_field'] == api_field_name:
                return config
        return None

    def detect_duplicates_in_collections(
        self, collection_ids: List[str]
    ) -> Dict[str, Any]:
        """Detect duplicates across multiple collections."""
        logger.info(f"Analyzing {len(collection_ids)} collections for duplicates...")

        all_items = []
        collection_items = {}

        # Gather all items from collections
        for collection_id in collection_ids:
            try:
                # Here you would fetch collection items via API
                items = self._get_collection_items(collection_id)
                collection_items[collection_id] = items
                all_items.extend(items)
            except Exception as e:
                logger.error(
                    f"Failed to get items from collection {collection_id}: {e}"
                )

        # Find duplicates
        duplicates = self.duplicate_detector.find_duplicates(all_items)

        return {
            "total_items_analyzed": len(all_items),
            "duplicate_pairs_found": len(duplicates),
            "collections_analyzed": collection_ids,
            "duplicates": [
                {
                    "item1": {"id": dup[0].get("id"), "title": dup[0].get("title")},
                    "item2": {"id": dup[1].get("id"), "title": dup[1].get("title")},
                    "similarity": dup[2],
                }
                for dup in duplicates
            ],
        }

    def _get_collection_items(self, collection_id: str) -> List[Dict[str, Any]]:
        """Get items from a collection via API."""
        try:
            url = f"{self.config.api_url}/collections/{collection_id}/datas"
            headers = {"X-API-KEY": self.config.api_key}

            response = requests.get(url, headers=headers, timeout=self.config.timeout)

            # Handle access denied for private collections
            if response.status_code == 403:
                logger.warning(
                    f"Access denied to collection {collection_id} - may be private or require special permissions"
                )
                return []

            response.raise_for_status()

            result = response.json()
            items = []

            if "data" in result:
                for item in result["data"]:
                    # Extract metadata for duplicate detection
                    title = self._extract_meta_value(item.get("metas", []), "title")
                    description = self._extract_meta_value(
                        item.get("metas", []), "description"
                    )

                    items.append(
                        {
                            "id": item.get("identifier"),
                            "title": title,
                            "description": description,
                            "status": item.get("status", ""),
                            "files": item.get("files", []),
                            "metas": item.get("metas", []),
                        }
                    )

            logger.info(f"Retrieved {len(items)} items from collection {collection_id}")
            return items

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get items from collection {collection_id}: {e}")
            return []

    def _extract_meta_value(
        self, metas: List[Dict], property_name: str, language: str = "fr"
    ) -> str:
        """Extract metadata value by property name."""
        if not metas:
            return ""

        for meta in metas:
            property_uri = meta.get("propertyUri", "")
            meta_lang = meta.get("lang", "")

            if property_name in property_uri.lower() and meta_lang == language:
                return meta.get("value", "")

        # Fall back to any language
        for meta in metas:
            property_uri = meta.get("propertyUri", "")
            if property_name in property_uri.lower():
                return meta.get("value", "")

        return ""

    def generate_quality_report(self, scope: str = "all") -> Dict[str, Any]:
        """Generate comprehensive quality report for user's data."""
        logger.info("Generating data quality report...")

        # Get user's data
        user_profile = self.user_client.get_complete_user_profile()

        report = {
            "generated_at": datetime.now().isoformat(),
            "scope": scope,
            "summary": user_profile["summary"],
            "collections_analysis": {},
            "datasets_analysis": {},
            "overall_quality_score": 0.0,
            "recommendations": [],
        }

        # Analyze collections
        if user_profile["collections"]:
            validation_result = self.batch_validate_metadata(
                user_profile["collections"]
            )
            report["collections_analysis"] = validation_result

        # Analyze datasets
        if user_profile["datasets"]:
            validation_result = self.batch_validate_metadata(user_profile["datasets"])
            report["datasets_analysis"] = validation_result

        # Calculate overall quality score
        total_items = len(user_profile["collections"]) + len(user_profile["datasets"])
        if total_items > 0:
            valid_collections = report["collections_analysis"].get("valid_items", 0)
            valid_datasets = report["datasets_analysis"].get("valid_items", 0)
            report["overall_quality_score"] = (
                (valid_collections + valid_datasets) / total_items * 100
            )

        # Generate recommendations
        self._generate_recommendations(report)

        return report

    def _generate_recommendations(self, report: Dict[str, Any]):
        """Generate quality improvement recommendations."""
        recommendations = []

        collections_analysis = report.get("collections_analysis", {})
        datasets_analysis = report.get("datasets_analysis", {})

        # Check for metadata quality issues
        if collections_analysis.get("items_with_errors", 0) > 0:
            recommendations.append(
                f"Fix metadata errors in {collections_analysis['items_with_errors']} collections"
            )

        if datasets_analysis.get("items_with_errors", 0) > 0:
            recommendations.append(
                f"Fix metadata errors in {datasets_analysis['items_with_errors']} datasets"
            )

        # Check overall quality score
        quality_score = report.get("overall_quality_score", 0)
        if quality_score < 80:
            recommendations.append(
                "Consider improving metadata quality - current score is below 80%"
            )

        if quality_score < 60:
            recommendations.append(
                "Urgent: Metadata quality is critically low - review and update metadata"
            )

        report["recommendations"] = recommendations

    def get_collection_data_items(self, collection_id: str) -> List[Dict[str, Any]]:
        """Get data items from a collection via API.

        Args:
            collection_id: The identifier of the collection

        Returns:
            List of data items with their metadata
        """
        return self._get_collection_items(collection_id)

    def export_modifications_template(
        self, items: List[Dict[str, Any]], output_path: str
    ):
        """Export a CSV template for batch modifications."""
        logger.info(
            f"Exporting modification template for {len(items)} items to {output_path}"
        )

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Header
            writer.writerow(
                [
                    "id",
                    "current_title",
                    "new_title",
                    "current_description",
                    "new_description",
                    "current_keywords",
                    "new_keywords",
                    "current_license",
                    "new_license",
                    "current_language",
                    "new_language",
                    "action",
                ]
            )

            # Data rows
            for item in items:
                writer.writerow(
                    [
                        item.get("id", ""),
                        item.get("title", ""),
                        "",  # new_title - to be filled
                        item.get("description", ""),
                        "",  # new_description - to be filled
                        item.get("keywords", ""),
                        "",  # new_keywords - to be filled
                        item.get("license", ""),
                        "",  # new_license - to be filled
                        item.get("language", ""),
                        "",  # new_language - to be filled
                        "modify",  # action
                    ]
                )

        logger.info(f"Template exported to {output_path}")


def print_field_reference():
    """Print comprehensive field reference for curator operations."""
    print("\n" + "=" * 80)
    print("NAKALA CURATOR - FIELD REFERENCE")
    print("=" * 80)

    print("\n📋 DATA ITEM FIELDS")
    print("-" * 40)

    data_fields = [
        (
            "title",
            "http://nakala.fr/terms#title",
            "Yes",
            "Required",
            '"fr:French|en:English"',
        ),
        (
            "description",
            "http://purl.org/dc/terms/description",
            "Yes",
            "Required",
            '"fr:Description|en:Description"',
        ),
        (
            "keywords",
            "http://purl.org/dc/terms/subject",
            "Yes",
            "Optional",
            '"fr:mot1;mot2|en:word1;word2"',
        ),
        (
            "author",
            "http://nakala.fr/terms#creator",
            "No",
            "Required",
            '"Surname,Givenname"',
        ),
        (
            "contributor",
            "http://purl.org/dc/terms/contributor",
            "No",
            "Optional",
            '"Smith,John;Martin,Alice"',
        ),
        (
            "type",
            "http://nakala.fr/terms#type",
            "No",
            "Required",
            "COAR Resource Type URI",
        ),
        ("license", "http://nakala.fr/terms#license", "No", "Required", '"CC-BY-4.0"'),
        (
            "date",
            "http://nakala.fr/terms#created",
            "No",
            "Required",
            '"2024-01-15" or "2024"',
        ),
        (
            "language",
            "http://purl.org/dc/terms/language",
            "No",
            "Optional",
            '"fr" or "en"',
        ),
        (
            "temporal",
            "http://purl.org/dc/terms/coverage",
            "No",
            "Optional",
            '"2020/2023"',
        ),
        ("spatial", "http://purl.org/dc/terms/coverage", "No", "Optional", '"France"'),
        (
            "relation",
            "http://purl.org/dc/terms/relation",
            "No",
            "Optional",
            "URI or text",
        ),
        (
            "source",
            "http://purl.org/dc/terms/source",
            "No",
            "Optional",
            "Source reference",
        ),
        (
            "identifier",
            "http://purl.org/dc/terms/identifier",
            "No",
            "Optional",
            '"DOI:10.1234/example"',
        ),
    ]

    print(f"{'Field':<12} {'Multilingual':<12} {'Required':<10} {'Example':<25}")
    print("-" * 70)
    for field, _, multilingual, required, example in data_fields:
        print(f"{field:<12} {multilingual:<12} {required:<10} {example:<25}")

    print("\n📚 COLLECTION FIELDS")
    print("-" * 40)

    collection_fields = [
        ("title", "Required", '"fr:Collection|en:Collection"'),
        ("status", "Required", '"private" or "public"'),
        ("description", "Optional", '"fr:Description|en:Description"'),
        ("keywords", "Optional", '"fr:mot1;mot2|en:word1;word2"'),
        ("creator", "Optional", '"Surname,Givenname"'),
        ("data_items", "Optional", "Folder patterns or IDs"),
    ]

    print(f"{'Field':<12} {'Required':<10} {'Example':<30}")
    print("-" * 55)
    for field, required, example in collection_fields:
        print(f"{field:<12} {required:<10} {example:<30}")

    print("\n🔧 BATCH MODIFICATION CSV FORMAT")
    print("-" * 40)
    print("id,action,current_title,new_title,current_description,new_description")
    print(
        '10.34847/nkl.abc123,update,"Old Title","fr:New|en:Title","Old desc","fr:New|en:Description"'
    )

    print("\n🌐 MULTILINGUAL FORMAT")
    print("-" * 40)
    print('Format: "language_code:content|language_code:content"')
    print("Examples:")
    print('  Single:   "Simple English Title"')
    print('  Multiple: "fr:Titre français|en:English Title"')
    print('  Keywords: "fr:mot1;mot2|en:word1;word2"')

    print("\n⚡ QUICK COMMANDS")
    print("-" * 40)
    print("# Show this reference")
    print("nakala-curator --list-fields")
    print("")
    print("# Generate quality report")
    print("nakala-curator --quality-report --api-key YOUR_KEY")
    print("")
    print("# Batch modify from CSV (dry run)")
    print("nakala-curator --batch-modify changes.csv --dry-run --api-key YOUR_KEY")
    print("")
    print("# Validate metadata")
    print("nakala-curator --validate-metadata --scope datasets --api-key YOUR_KEY")

    print("\n📖 COMPLETE REFERENCE")
    print("-" * 40)
    print("For detailed documentation with all fields, formats, and examples:")
    print("See: docs/curator-field-reference.md")

    print("\n" + "=" * 80)


def main():
    """Main entry point for the curator script."""
    parser = argparse.ArgumentParser(
        description="Nakala Curator - Data curation and quality management tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate quality report
  python nakala-curator.py --quality-report
  
  # Validate metadata for all collections
  python nakala-curator.py --validate-metadata --scope collections
  
  # Detect duplicates
  python nakala-curator.py --detect-duplicates --collections col1,col2
  
  # Apply batch modifications from CSV
  python nakala-curator.py --batch-modify modifications.csv --dry-run
        """,
    )

    parser.add_argument(
        "--api-key", help="Nakala API key (or set NAKALA_API_KEY environment variable)"
    )

    parser.add_argument(
        "--api-url",
        default="https://apitest.nakala.fr",
        help="Nakala API URL (default: test API)",
    )

    parser.add_argument(
        "--quality-report",
        action="store_true",
        help="Generate comprehensive quality report",
    )

    parser.add_argument(
        "--validate-metadata",
        action="store_true",
        help="Validate metadata for specified scope",
    )

    parser.add_argument(
        "--detect-duplicates", action="store_true", help="Detect potential duplicates"
    )

    parser.add_argument(
        "--batch-modify", help="CSV file with batch modifications to apply"
    )

    parser.add_argument(
        "--export-template", help="Export modification template CSV for specified items"
    )

    parser.add_argument(
        "--scope",
        default="all",
        choices=["all", "collections", "datasets"],
        help="Scope for operations",
    )

    parser.add_argument("--collections", help="Comma-separated list of collection IDs")

    parser.add_argument(
        "--output", "-o", help="Output file path for reports and exports"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate operations without making changes",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Batch size for processing (default: 50)",
    )

    parser.add_argument(
        "--list-fields",
        action="store_true",
        help="Display complete field reference with examples",
    )

    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip client-side validation before modifications (use with caution)",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_common_logging(level=log_level)

    try:
        # Handle --list-fields before configuration validation
        if args.list_fields:
            print_field_reference()
            return 0

        # Create configuration
        config = CuratorConfig(
            api_url=args.api_url,
            api_key=args.api_key,
            batch_size=args.batch_size,
            dry_run_default=args.dry_run,
            validate_before_modification=not args.skip_validation,
        )

        if not config.validate():
            logger.error("Configuration validation failed")
            return 1

        # Create curator client
        curator = NakalaCuratorClient(config)

        # Execute requested operations
        if args.quality_report:
            report = curator.generate_quality_report(scope=args.scope)

            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(report, f, indent=2, ensure_ascii=False, default=str)
                logger.info(f"Quality report exported to: {args.output}")
            else:
                print(json.dumps(report, indent=2, ensure_ascii=False, default=str))

        elif args.validate_metadata:
            # Get user data for validation
            user_client = NakalaUserInfoClient(config)
            profile = user_client.get_complete_user_profile()

            items = []
            if args.scope == "collections":
                items = profile["collections"]
            elif args.scope == "datasets":
                items = profile["datasets"]
            else:
                items = profile["collections"] + profile["datasets"]

            validation_result = curator.batch_validate_metadata(items)
            print(json.dumps(validation_result, indent=2, ensure_ascii=False))

        elif args.detect_duplicates:
            if not args.collections:
                logger.error("--collections parameter required for duplicate detection")
                return 1

            collection_ids = [cid.strip() for cid in args.collections.split(",")]
            duplicates = curator.detect_duplicates_in_collections(collection_ids)

            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(duplicates, f, indent=2, ensure_ascii=False, default=str)
                logger.info(f"Duplicate analysis exported to: {args.output}")
            else:
                print(json.dumps(duplicates, indent=2, ensure_ascii=False, default=str))

        elif args.export_template:
            # Export modification template
            user_client = NakalaUserInfoClient(config)
            profile = user_client.get_complete_user_profile()

            items = []
            if args.scope == "collections":
                items = profile["collections"]
            elif args.scope == "datasets":
                items = profile["datasets"]
            else:
                items = profile["collections"] + profile["datasets"]

            # Filter by specific collections if provided
            if args.collections:
                collection_ids = [cid.strip() for cid in args.collections.split(",")]
                if args.scope == "collections":
                    items = [item for item in items if item.get("id") in collection_ids]
                elif args.scope == "datasets":
                    # For datasets, get items from specified collections
                    collection_items = []
                    for collection_id in collection_ids:
                        collection_data = curator.get_collection_data_items(
                            collection_id
                        )
                        collection_items.extend(collection_data)
                    items = collection_items

            curator.export_modifications_template(items, args.export_template)
            logger.info(f"Modification template exported to: {args.export_template}")

        elif args.batch_modify:
            # Load modifications from CSV using comprehensive parser
            try:
                modifications, unsupported_fields = curator.parse_csv_modifications(args.batch_modify)
                
                if unsupported_fields:
                    logger.warning(f"Found {len(unsupported_fields)} unsupported fields: {unsupported_fields}")
                    logger.info("Continuing with supported fields only...")
                
                logger.info(f"Parsed {len(modifications)} modifications from CSV")
                
            except Exception as e:
                logger.error(f"Failed to parse CSV file: {e}")
                return 1

            if modifications:
                result = curator.batch_modify_metadata(
                    modifications, dry_run=args.dry_run
                )
                summary = result.get_summary()

                print(
                    f"Batch modification {'simulation' if args.dry_run else 'completed'}:"
                )
                print(f"  Total processed: {summary['total_processed']}")
                print(f"  Successful: {summary['successful']}")
                print(f"  Failed: {summary['failed']}")
                print(f"  Skipped: {summary['skipped']}")
                print(f"  Success rate: {summary['success_rate']:.1f}%")

                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        json.dump(
                            result.__dict__,
                            f,
                            indent=2,
                            ensure_ascii=False,
                            default=str,
                        )
            else:
                logger.error("No valid modifications found in CSV file")
                logger.info("Check that:")
                logger.info("- CSV has 'action' column with 'modify' values")
                logger.info("- CSV has 'id' column with valid item identifiers") 
                logger.info(f"- CSV has one or more supported fields: {list(CSV_FIELD_MAPPINGS.keys())}")
                if unsupported_fields:
                    logger.info(f"- Remove unsupported fields: {unsupported_fields}")
                return 1

        else:
            parser.print_help()
            return 1

        return 0

    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
