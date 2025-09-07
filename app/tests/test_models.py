"""
Basic tests for the Knowledge Graph MCP Server models and validation
"""
import pytest
import asyncio
from app.models.schemas import Knowledge, Source, KnowledgeWithSources
from app.validation.validators import DataValidator


class TestDataModels:
    """Test data models"""
    
    def test_valid_source_creation(self):
        """Test creating a valid Source"""
        source = Source(
            type="Website",
            url="https://example.com",
            name="Example Website",
            trustworthiness=5,
            expertise=["Computer Science", "Web Development"]
        )
        assert source.type == "Website"
        assert source.trustworthiness == 5
        assert len(source.expertise) == 2
    
    def test_invalid_source_trustworthiness(self):
        """Test Source with invalid trustworthiness range"""
        with pytest.raises(ValueError):
            Source(
                type="Website",
                url="https://example.com",
                name="Example Website",
                trustworthiness=15,  # Invalid: > 10
                expertise=["Computer Science"]
            )
    
    def test_invalid_source_url(self):
        """Test Source with invalid URL"""
        with pytest.raises(ValueError):
            Source(
                type="Website",
                url="not-a-valid-url",
                name="Example Website",
                trustworthiness=5,
                expertise=["Computer Science"]
            )
    
    def test_valid_knowledge_creation(self):
        """Test creating a valid Knowledge node"""
        knowledge = Knowledge(
            type="Algorithm",
            title="Binary Search",
            content="A search algorithm that finds the position of a target value within a sorted array.",
            properties={"complexity": "O(log n)"}
        )
        assert knowledge.type == "Algorithm"
        assert knowledge.title == "Binary Search"
        assert knowledge.properties["complexity"] == "O(log n)"
    
    def test_knowledge_with_sources(self):
        """Test KnowledgeWithSources model"""
        source = Source(
            type="Website",
            url="https://wikipedia.org",
            name="Wikipedia",
            trustworthiness=8,
            expertise=["General Knowledge"]
        )
        
        knowledge = Knowledge(
            type="Definition",
            title="Artificial Intelligence",
            content="The simulation of human intelligence by machines."
        )
        
        knowledge_with_sources = KnowledgeWithSources(
            knowledge=knowledge,
            sources=[source]
        )
        
        assert len(knowledge_with_sources.sources) == 1
        assert knowledge_with_sources.knowledge.title == "Artificial Intelligence"


class TestDataValidator:
    """Test data validation"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.validator = DataValidator()
    
    def test_validate_knowledge_basic(self):
        """Test basic knowledge validation"""
        valid_knowledge = Knowledge(
            type="Algorithm",
            title="Quick Sort",
            content="A divide-and-conquer algorithm that sorts an array by partitioning it."
        )
        
        errors = self.validator.validate_knowledge(valid_knowledge)
        assert len(errors) == 0
    
    def test_validate_knowledge_invalid_title(self):
        """Test knowledge validation with invalid title"""
        invalid_knowledge = Knowledge(
            type="Algorithm",
            title="QS",  # Too short
            content="A divide-and-conquer algorithm that sorts an array."
        )
        
        errors = self.validator.validate_knowledge(invalid_knowledge)
        assert len(errors) > 0
        assert any("title must be at least 3 characters" in error for error in errors)
    
    def test_validate_knowledge_invalid_content(self):
        """Test knowledge validation with invalid content"""
        invalid_knowledge = Knowledge(
            type="Algorithm",
            title="Quick Sort",
            content="Short"  # Too short
        )
        
        errors = self.validator.validate_knowledge(invalid_knowledge)
        assert len(errors) > 0
        assert any("content must be at least 10 characters" in error for error in errors)


if __name__ == "__main__":
    pytest.main([__file__])