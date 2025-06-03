"""
Metadata models for Nakala API.

This module defines Pydantic models for Nakala metadata, providing
validation and serialization of metadata according to Nakala's schema.
"""

from datetime import date, datetime
from enum import Enum
from typing import List, Optional, Union, Dict, Any, Literal
from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
    ConfigDict
)
from pydantic_core.core_schema import ValidationInfo

class MetadataValue(BaseModel):
    """A single metadata value with optional language and type information."""
    value: str
    lang: Optional[str] = Field(
        None,
        description="Language tag (e.g., 'fr', 'en') for multilingual values"
    )
    type_uri: Optional[str] = Field(
        None,
        alias="typeUri",
        description="URI identifying the value's data type (e.g., 'http://www.w3.org/2001/XMLSchema#string')"
    )
    
    class Config:
        populate_by_name = True


class MetadataEntry(BaseModel):
    """A metadata entry with a property URI and one or more values."""
    property_uri: str = Field(
        ...,
        alias="propertyUri",
        description="URI identifying the metadata property (e.g., 'http://purl.org/dc/terms/title')"
    )
    values: List[Union[str, MetadataValue]] = Field(
        ...,
        description="One or more values for this metadata property"
    )
    
    class Config:
        populate_by_name = True
    
    @model_validator(mode='after')
    def validate_values(self) -> 'MetadataEntry':
        """Ensure values are properly formatted."""
        if not self.values:
            raise ValueError("At least one value is required")
        return self


class Creator(BaseModel):
    """A creator of the resource."""
    given_name: Optional[str] = Field(
        None,
        alias="givenName",
        description="Creator's given name"
    )
    family_name: Optional[str] = Field(
        None,
        alias="familyName",
        description="Creator's family name"
    )
    name: Optional[str] = Field(
        None,
        description="Full name of the creator (if not using given/family name)"
    )
    identifier: Optional[str] = Field(
        None,
        description="ORCID or other persistent identifier for the creator"
    )
    affiliation: Optional[str] = Field(
        None,
        description="Creator's institutional affiliation"
    )
    
    @model_validator(mode='after')
    def validate_creator(self) -> 'Creator':
        """Validate that either name or given_name/family_name is provided."""
        if not self.name and not (self.given_name or self.family_name):
            raise ValueError("Either 'name' or both 'given_name' and 'family_name' must be provided")
        return self


class Contributor(Creator):
    """A contributor to the resource."""
    role: Optional[str] = Field(
        None,
        description="Role of the contributor (e.g., 'Editor', 'Translator')"
    )


class Subject(BaseModel):
    """A subject or keyword describing the resource."""
    value: str
    scheme: Optional[str] = Field(
        None,
        description="Controlled vocabulary scheme (e.g., 'keywords', 'mesh')"
    )
    lang: Optional[str] = Field(
        None,
        description="Language tag for the subject"
    )


class TemporalCoverage(BaseModel):
    """Temporal coverage of the resource."""
    start_date: Optional[Union[date, str]] = Field(
        None,
        alias="startDate",
        description="Start date of the temporal coverage"
    )
    end_date: Optional[Union[date, str]] = Field(
        None,
        alias="endDate",
        description="End date of the temporal coverage"
    )
    period: Optional[str] = Field(
        None,
        description="Named period (e.g., 'Middle Ages', 'Renaissance')"
    )


class SpatialCoverage(BaseModel):
    """Geographic coverage of the resource."""
    name: Optional[str] = Field(
        None,
        description="Name of the geographic location"
    )
    point: Optional[str] = Field(
        None,
        description="Geographic point in 'latitude,longitude' format"
    )
    box: Optional[str] = Field(
        None,
        description="Bounding box in 'westlimit,southlimit,eastlimit,northlimit' format"
    )
    geoname_id: Optional[str] = Field(
        None,
        alias="geonameId",
        description="GeoNames ID for the location"
    )


class RelationType(str, Enum):
    """Types of relations between resources."""
    IS_PART_OF = "isPartOf"
    HAS_PART = "hasPart"
    IS_VERSION_OF = "isVersionOf"
    HAS_VERSION = "hasVersion"
    IS_REFERENCED_BY = "isReferencedBy"
    REFERENCES = "references"
    IS_REPLACED_BY = "isReplacedBy"
    REPLACES = "replaces"
    REQUIRES = "requires"
    IS_REQUIRED_BY = "isRequiredBy"
    IS_FORMAT_OF = "isFormatOf"
    HAS_FORMAT = "hasFormat"
    IS_SOURCE_OF = "isSourceOf"
    SOURCE = "source"


class Relation(BaseModel):
    """A relationship to another resource."""
    type: RelationType
    identifier: str
    title: Optional[str] = None
    relation_type: Optional[str] = Field(
        None,
        alias="relationType",
        description="Type of relationship (e.g., 'cites', 'isCitedBy')"
    )


class License(BaseModel):
    """License information for the resource."""
    uri: HttpUrl = Field(..., description="URI of the license")
    name: Optional[str] = Field(
        None,
        description="Human-readable name of the license"
    )
    identifier: Optional[str] = Field(
        None,
        description="Short identifier for the license (e.g., 'CC-BY-4.0')"
    )


class Rights(BaseModel):
    """Rights information for the resource."""
    license: Optional[License] = None
    rights_statement: Optional[str] = Field(
        None,
        alias="rightsStatement",
        description="Human-readable rights statement"
    )
    access_rights: Optional[str] = Field(
        None,
        alias="accessRights",
        description="Access rights information"
    )
    embargo: Optional[Union[date, str]] = Field(
        None,
        description="Embargo date until which access is restricted"
    )


class MetadataBuilder:
    """Builder for constructing Nakala metadata."""
    
    def __init__(self):
        self.metadata: Dict[str, Any] = {
            "status": "pending",
            "metas": [],
            "rights": {}
        }
    
    def set_status(self, status: str) -> 'MetadataBuilder':
        """Set the status of the resource."""
        self.metadata["status"] = status
        return self
    
    def add_metadata_entry(self, entry: MetadataEntry) -> 'MetadataBuilder':
        """Add a metadata entry."""
        self.metadata["metas"].append(entry.model_dump(by_alias=True, exclude_none=True))
        return self
    
    def add_title(self, title: str, lang: str = "fr") -> 'MetadataBuilder':
        """Add a title to the metadata."""
        entry = MetadataEntry(
            propertyUri="http://nakala.fr/terms#title",
            values=[{"value": title, "lang": lang, "typeUri": "http://www.w3.org/2001/XMLSchema#string"}]
        )
        return self.add_metadata_entry(entry)
    
    def add_description(self, description: str, lang: str = "fr") -> 'MetadataBuilder':
        """Add a description to the metadata."""
        entry = MetadataEntry(
            propertyUri="http://purl.org/dc/terms/description",
            values=[{"value": description, "lang": lang}]
        )
        return self.add_metadata_entry(entry)
    
    def add_creator(self, creator: Union[Creator, Dict[str, Any]]) -> 'MetadataBuilder':
        """Add a creator to the metadata."""
        if isinstance(creator, dict):
            creator = Creator(**creator)
        
        creator_dict = creator.model_dump(by_alias=True, exclude_none=True)
        
        entry = MetadataEntry(
            propertyUri="http://purl.org/dc/terms/creator",
            values=[{"value": creator_dict}]
        )
        return self.add_metadata_entry(entry)
    
    def add_subject(self, subject: Union[Subject, Dict[str, Any], str]) -> 'MetadataBuilder':
        """Add a subject or keyword to the metadata."""
        if isinstance(subject, str):
            subject = Subject(value=subject)
        elif isinstance(subject, dict):
            subject = Subject(**subject)
        
        subject_dict = subject.model_dump(exclude_none=True)
        
        entry = MetadataEntry(
            propertyUri="http://purl.org/dc/terms/subject",
            values=[{"value": subject_dict}]
        )
        return self.add_metadata_entry(entry)
    
    def set_rights(self, rights: Union[Rights, Dict[str, Any]]) -> 'MetadataBuilder':
        """Set the rights information for the resource."""
        if isinstance(rights, dict):
            rights = Rights(**rights)
        self.metadata["rights"] = rights.model_dump(by_alias=True, exclude_none=True)
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build and return the final metadata dictionary."""
        return self.metadata
