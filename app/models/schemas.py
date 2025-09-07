"""
Pydantic data models for the Knowledge Graph MCP Server
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
import validators


class Source(BaseModel):
    """Source node model"""
    type: str = Field(..., description="Type of the source (e.g., 'Website', 'User', 'Publication')")
    url: Optional[str] = Field(None, description="URL of the source (if applicable)")
    name: str = Field(..., description="Name of the source")
    trustworthiness: int = Field(..., ge=-10, le=10, description="Trustworthiness metric (-10 to +10)")
    expertise: List[str] = Field(..., description="Array of domains or fields of expertise")

    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        """Validate URL format if provided"""
        if v is not None and not validators.url(v):
            raise ValueError(f"Invalid URL format: {v}")
        return v

    @field_validator('expertise')
    @classmethod
    def validate_expertise(cls, v):
        """Validate expertise domains contain only alphanumeric values"""
        for domain in v:
            if not domain.replace(' ', '').replace('-', '').replace('_', '').isalnum():
                raise ValueError(f"Expertise domain must contain only alphanumeric values, spaces, hyphens, and underscores: {domain}")
        return v

    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        """Validate source type"""
        valid_types = ['Website', 'User', 'Publication', 'Book', 'Journal', 'Conference', 'Other']
        if v not in valid_types:
            raise ValueError(f"Source type must be one of: {valid_types}")
        return v


class Knowledge(BaseModel):
    """Knowledge node model"""
    type: str = Field(..., description="Type of knowledge (e.g., 'Algorithm', 'Theorem', 'Definition', 'API')")
    title: str = Field(..., description="Title or name of the knowledge")
    content: str = Field(..., description="Content or description of the knowledge")
    properties: Optional[Dict[str, Any]] = Field(default={}, description="Additional properties specific to the knowledge type")
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        """Validate knowledge type"""
        valid_types = ['Algorithm', 'Theorem', 'Definition', 'API', 'Concept', 'Fact', 'Process', 'Tool', 'Other']
        if v not in valid_types:
            raise ValueError(f"Knowledge type must be one of: {valid_types}")
        return v


class KnowledgeWithSources(BaseModel):
    """Knowledge node with associated sources"""
    knowledge: Knowledge
    sources: List[Source] = Field(..., min_length=1, description="At least one source is required")


class CypherQuery(BaseModel):
    """Model for Cypher query requests"""
    query: str = Field(..., description="Cypher query to execute")
    parameters: Optional[Dict[str, Any]] = Field(default={}, description="Query parameters")

    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        """Basic Cypher query validation"""
        if not v.strip():
            raise ValueError("Query cannot be empty")
        
        # For read operations, ensure only safe operations are allowed
        dangerous_operations = ['DELETE', 'REMOVE', 'SET', 'CREATE', 'MERGE', 'DROP']
        query_upper = v.upper()
        for operation in dangerous_operations:
            if operation in query_upper:
                raise ValueError(f"Query contains potentially dangerous operation: {operation}")
        
        return v


class QueryResponse(BaseModel):
    """Response model for query results"""
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class CreateResponse(BaseModel):
    """Response model for create operations"""
    success: bool
    knowledge_id: Optional[str] = None
    source_ids: Optional[List[str]] = None
    error: Optional[str] = None