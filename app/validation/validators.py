"""
Validation logic for the Knowledge Graph MCP Server
"""
import asyncio
import httpx
import validators
from typing import List, Optional
from urllib.parse import urlparse

from app.models.schemas import Source, Knowledge, KnowledgeWithSources


class URLValidator:
    """Validator for URL existence and accessibility"""
    
    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout
    
    async def validate_url_exists(self, url: str) -> bool:
        """Check if URL exists and is accessible"""
        if not validators.url(url):
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.head(url, timeout=self.timeout)
                return response.status_code < 400
        except (httpx.RequestError, httpx.TimeoutException):
            # If HEAD fails, try GET with a small amount of data
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, timeout=self.timeout)
                    return response.status_code < 400
            except (httpx.RequestError, httpx.TimeoutException):
                return False


class DataValidator:
    """Main data validator class"""
    
    def __init__(self):
        self.url_validator = URLValidator()
    
    async def validate_source(self, source: Source) -> List[str]:
        """
        Validate a Source object and return list of validation errors
        """
        errors = []
        
        # Validate URL if provided
        if source.url:
            if not await self.url_validator.validate_url_exists(source.url):
                errors.append(f"URL does not exist or is not accessible: {source.url}")
        
        # Trustworthiness validation is handled by Pydantic model
        # Expertise validation is handled by Pydantic model
        
        return errors
    
    def validate_knowledge(self, knowledge: Knowledge) -> List[str]:
        """
        Validate a Knowledge object and return list of validation errors
        """
        errors = []
        
        # Basic content validation
        if len(knowledge.title.strip()) < 3:
            errors.append("Knowledge title must be at least 3 characters long")
        
        if len(knowledge.content.strip()) < 10:
            errors.append("Knowledge content must be at least 10 characters long")
        
        return errors
    
    async def validate_knowledge_with_sources(self, data: KnowledgeWithSources) -> List[str]:
        """
        Validate KnowledgeWithSources object and return list of validation errors
        """
        errors = []
        
        # Validate knowledge
        knowledge_errors = self.validate_knowledge(data.knowledge)
        errors.extend(knowledge_errors)
        
        # Validate each source
        source_validation_tasks = [
            self.validate_source(source) for source in data.sources
        ]
        
        source_results = await asyncio.gather(*source_validation_tasks)
        
        for i, source_errors in enumerate(source_results):
            for error in source_errors:
                errors.append(f"Source {i+1}: {error}")
        
        # Ensure at least one source (handled by Pydantic min_items=1)
        
        return errors