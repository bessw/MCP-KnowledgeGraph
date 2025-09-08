"""
Integration tests for the Knowledge Graph MCP Server API endpoints
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import json

from main import app
from app.config import ConfigManager
from app.database.neo4j_ops import Neo4jOperations
from app.validation.validators import DataValidator
from app.auth.security import init_auth
from app.api.endpoints import init_api_dependencies


class TestAPIIntegration:
    """Test API endpoints with mocked database operations"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Set up test fixtures"""
        # Mock configuration
        self.mock_config = Mock(spec=ConfigManager)
        self.mock_config.verify_api_key.return_value = "test_user"
        
        # Mock database operations
        self.mock_db_ops = Mock(spec=Neo4jOperations)
        
        # Mock validator
        self.mock_validator = Mock(spec=DataValidator)
        self.mock_validator.validate_knowledge_with_sources.return_value = []
        
        # Initialize app dependencies with mocks
        init_auth(self.mock_config)
        init_api_dependencies(self.mock_db_ops, self.mock_validator)
        
        # Create test client
        self.client = TestClient(app)
        
        # Test data
        self.test_knowledge_data = {
            "knowledge": {
                "type": "Algorithm",
                "title": "Binary Search",
                "content": "A search algorithm that finds the position of a target value within a sorted array by repeatedly dividing the search interval in half.",
                "properties": {"complexity": "O(log n)", "space_complexity": "O(1)"}
            },
            "sources": [
                {
                    "type": "Website",
                    "url": "https://en.wikipedia.org/wiki/Binary_search_algorithm",
                    "name": "Wikipedia - Binary Search Algorithm",
                    "trustworthiness": 8,
                    "expertise": ["Computer Science", "Algorithms"]
                }
            ]
        }
        
        self.headers = {"Authorization": "Bearer test_api_key_123"}

    def test_health_endpoints(self):
        """Test health check endpoints"""
        response = self.client.get("/")
        assert response.status_code == 200
        assert "Knowledge Graph MCP Server is running" in response.json()["message"]
        
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_create_knowledge_success(self):
        """Test successful knowledge creation"""
        # Mock database response
        self.mock_db_ops.create_knowledge_with_sources.return_value = {
            'knowledge_id': 'k123',
            'source_ids': ['s456']
        }
        
        response = self.client.post(
            "/api/v1/knowledge",
            json=self.test_knowledge_data,
            headers=self.headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["knowledge_id"] == "k123"
        assert data["source_ids"] == ["s456"]
        
        # Verify mocks were called
        self.mock_validator.validate_knowledge_with_sources.assert_called_once()
        self.mock_db_ops.create_knowledge_with_sources.assert_called_once()

    def test_create_knowledge_validation_error(self):
        """Test knowledge creation with validation errors"""
        # Mock validation error
        self.mock_validator.validate_knowledge_with_sources.return_value = [
            "Source 1: URL does not exist or is not accessible"
        ]
        
        response = self.client.post(
            "/api/v1/knowledge",
            json=self.test_knowledge_data,
            headers=self.headers
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Validation failed" in data["detail"]["message"]
        assert len(data["detail"]["errors"]) == 1

    def test_create_knowledge_unauthorized(self):
        """Test knowledge creation without authorization"""
        response = self.client.post(
            "/api/v1/knowledge",
            json=self.test_knowledge_data
        )
        
        assert response.status_code == 403

    def test_execute_query_success(self):
        """Test successful Cypher query execution"""
        query_data = {
            "query": "MATCH (k:Knowledge) RETURN k.title LIMIT 10",
            "parameters": {}
        }
        
        # Mock database response
        self.mock_db_ops.execute_read_query.return_value = [
            {"k.title": "Binary Search"},
            {"k.title": "Quick Sort"}
        ]
        
        response = self.client.post(
            "/api/v1/query",
            json=query_data,
            headers=self.headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 2
        assert data["metadata"]["result_count"] == 2

    def test_execute_query_invalid_query(self):
        """Test query execution with invalid Cypher"""
        query_data = {
            "query": "DELETE (k:Knowledge)",  # Dangerous operation
            "parameters": {}
        }
        
        response = self.client.post(
            "/api/v1/query",
            json=query_data,
            headers=self.headers
        )
        
        # Should fail validation at the Pydantic model level
        assert response.status_code == 422

    def test_get_knowledge_success(self):
        """Test successful knowledge retrieval"""
        knowledge_id = "k123"
        
        # Mock database response
        self.mock_db_ops.get_knowledge_with_sources.return_value = {
            "k": {"title": "Binary Search", "type": "Algorithm"},
            "sources": [{"name": "Wikipedia", "trustworthiness": 8}]
        }
        
        response = self.client.get(
            f"/api/v1/knowledge/{knowledge_id}",
            headers=self.headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 1
        assert data["metadata"]["knowledge_id"] == knowledge_id

    def test_get_knowledge_not_found(self):
        """Test knowledge retrieval with non-existent ID"""
        knowledge_id = "nonexistent"
        
        # Mock database response
        self.mock_db_ops.get_knowledge_with_sources.return_value = None
        
        response = self.client.get(
            f"/api/v1/knowledge/{knowledge_id}",
            headers=self.headers
        )
        
        assert response.status_code == 404
        assert f"Knowledge node with ID {knowledge_id} not found" in response.json()["detail"]

    def test_search_knowledge_success(self):
        """Test successful knowledge search"""
        search_term = "binary"
        
        # Mock database response
        self.mock_db_ops.search_knowledge.return_value = [
            {
                "k": {"title": "Binary Search", "type": "Algorithm"},
                "sources": [{"name": "Wikipedia"}]
            }
        ]
        
        response = self.client.get(
            f"/api/v1/knowledge/search/{search_term}",
            headers=self.headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 1
        assert data["metadata"]["search_term"] == search_term

    def test_search_knowledge_with_type_filter(self):
        """Test knowledge search with type filter"""
        search_term = "sort"
        knowledge_type = "Algorithm"
        
        # Mock database response
        self.mock_db_ops.search_knowledge.return_value = [
            {
                "k": {"title": "Quick Sort", "type": "Algorithm"},
                "sources": [{"name": "Algorithm Book"}]
            }
        ]
        
        response = self.client.get(
            f"/api/v1/knowledge/search/{search_term}?knowledge_type={knowledge_type}",
            headers=self.headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["metadata"]["knowledge_type"] == knowledge_type
        
        # Verify the search was called with the type filter
        self.mock_db_ops.search_knowledge.assert_called_once_with(search_term, knowledge_type)


if __name__ == "__main__":
    pytest.main([__file__])