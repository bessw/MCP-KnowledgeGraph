"""
API endpoints for the Knowledge Graph MCP Server
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from app.models.schemas import (
    KnowledgeWithSources, 
    CypherQuery, 
    QueryResponse, 
    CreateResponse
)
from app.auth.security import get_current_user
from app.database.neo4j_ops import Neo4jOperations
from app.validation.validators import DataValidator

router = APIRouter()

# Global variables to be initialized in main.py
db_operations: Neo4jOperations = None
data_validator: DataValidator = None


def init_api_dependencies(db_ops: Neo4jOperations, validator: DataValidator):
    """Initialize API dependencies"""
    global db_operations, data_validator
    db_operations = db_ops
    data_validator = validator


@router.post("/knowledge", response_model=CreateResponse)
async def create_knowledge(
    knowledge_data: KnowledgeWithSources,
    current_user: str = Depends(get_current_user)
):
    """
    Create a new Knowledge node with associated Source nodes
    """
    try:
        # Validate the input data
        validation_errors = await data_validator.validate_knowledge_with_sources(knowledge_data)
        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Validation failed", "errors": validation_errors}
            )
        
        # Create the knowledge with sources
        result = db_operations.create_knowledge_with_sources(knowledge_data)
        
        return CreateResponse(
            success=True,
            knowledge_id=result['knowledge_id'],
            source_ids=result['source_ids']
        )
    
    except HTTPException:
        raise
    except Exception as e:
        return CreateResponse(
            success=False,
            error=f"Failed to create knowledge: {str(e)}"
        )


@router.post("/query", response_model=QueryResponse)
async def execute_query(
    query_request: CypherQuery,
    current_user: str = Depends(get_current_user)
):
    """
    Execute a read-only Cypher query against the knowledge graph
    """
    try:
        # Execute the query using read-only connection
        result = db_operations.execute_read_query(
            query_request.query, 
            query_request.parameters
        )
        
        return QueryResponse(
            success=True,
            data=result,
            metadata={
                "query": query_request.query,
                "user": current_user,
                "result_count": len(result)
            }
        )
    
    except Exception as e:
        return QueryResponse(
            success=False,
            error=f"Query execution failed: {str(e)}"
        )


@router.get("/knowledge/{knowledge_id}", response_model=QueryResponse)
async def get_knowledge(
    knowledge_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Retrieve a Knowledge node by its ID along with associated Sources
    """
    try:
        result = db_operations.get_knowledge_with_sources(knowledge_id)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Knowledge node with ID {knowledge_id} not found"
            )
        
        return QueryResponse(
            success=True,
            data=[result],
            metadata={
                "knowledge_id": knowledge_id,
                "user": current_user
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        return QueryResponse(
            success=False,
            error=f"Failed to retrieve knowledge: {str(e)}"
        )


@router.get("/knowledge/search/{search_term}", response_model=QueryResponse)
async def search_knowledge(
    search_term: str,
    knowledge_type: str = None,
    current_user: str = Depends(get_current_user)
):
    """
    Search for Knowledge nodes by title or content
    """
    try:
        result = db_operations.search_knowledge(search_term, knowledge_type)
        
        return QueryResponse(
            success=True,
            data=result,
            metadata={
                "search_term": search_term,
                "knowledge_type": knowledge_type,
                "user": current_user,
                "result_count": len(result)
            }
        )
    
    except Exception as e:
        return QueryResponse(
            success=False,
            error=f"Search failed: {str(e)}"
        )