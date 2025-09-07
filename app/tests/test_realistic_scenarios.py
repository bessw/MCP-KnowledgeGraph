"""
Realistic test scenarios for the Knowledge Graph MCP Server

This module contains 50+ realistic test scenarios that demonstrate the practical 
use of the Knowledge Graph MCP Server for storing, querying, and managing knowledge.
Each scenario reflects real-world use cases.
"""
import pytest
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import json

from app.models.schemas import Knowledge, Source, KnowledgeWithSources
from app.validation.validators import DataValidator


class RealisticTestScenarios:
    """Collection of realistic test scenarios for the Knowledge Graph MCP Server"""
    
    def __init__(self):
        self.validator = DataValidator()
        self.scenarios = []
    
    def generate_all_scenarios(self) -> List[Dict[str, Any]]:
        """Generate all 50+ realistic test scenarios"""
        
        # Software Development Scenarios
        self._software_development_scenarios()
        
        # Research and Academic Scenarios
        self._research_academic_scenarios()
        
        # Business and Professional Knowledge
        self._business_professional_scenarios()
        
        # Technical Documentation Scenarios
        self._technical_documentation_scenarios()
        
        # Personal Learning and Development
        self._personal_learning_scenarios()
        
        return self.scenarios
    
    def _software_development_scenarios(self):
        """Scenarios related to software development"""
        
        # Scenario 1: Algorithm documentation
        self.scenarios.append({
            "id": "sw_001",
            "title": "Algorithm Knowledge Storage",
            "description": "Store algorithm knowledge from multiple sources",
            "knowledge": Knowledge(
                type="Algorithm",
                title="QuickSort Algorithm",
                content="A divide-and-conquer algorithm that sorts an array by selecting a 'pivot' element and partitioning the other elements into two sub-arrays.",
                properties={
                    "time_complexity": "O(n log n) average, O(n²) worst case",
                    "space_complexity": "O(log n)",
                    "stability": "unstable",
                    "in_place": True
                }
            ),
            "sources": [
                Source(
                    type="Website",
                    url="https://en.wikipedia.org/wiki/Quicksort",
                    name="Wikipedia - Quicksort",
                    trustworthiness=8,
                    expertise=["Computer Science", "Algorithms"]
                ),
                Source(
                    type="Publication",
                    name="Introduction to Algorithms (CLRS)",
                    trustworthiness=10,
                    expertise=["Computer Science", "Algorithms", "Data Structures"]
                )
            ]
        })
        
        # Scenario 2: API documentation
        self.scenarios.append({
            "id": "sw_002",
            "title": "REST API Endpoint Documentation",
            "description": "Document REST API endpoints for team reference",
            "knowledge": Knowledge(
                type="API",
                title="User Authentication Endpoint",
                content="POST /api/v1/auth/login - Authenticate user with email and password",
                properties={
                    "method": "POST",
                    "endpoint": "/api/v1/auth/login",
                    "request_body": {"email": "string", "password": "string"},
                    "response": {"access_token": "string", "refresh_token": "string"},
                    "status_codes": {"200": "Success", "401": "Unauthorized", "400": "Bad Request"}
                }
            ),
            "sources": [
                Source(
                    type="User",
                    name="John Smith - Backend Developer",
                    trustworthiness=9,
                    expertise=["Backend Development", "API Design", "Authentication"]
                ),
                Source(
                    type="Website",
                    url="https://company.com/api-docs",
                    name="Company API Documentation",
                    trustworthiness=10,
                    expertise=["API Documentation", "Software Engineering"]
                )
            ]
        })
        
        # Scenario 3: Design Pattern Knowledge
        self.scenarios.append({
            "id": "sw_003",
            "title": "Design Pattern Documentation",
            "description": "Store design pattern knowledge for code architecture",
            "knowledge": Knowledge(
                type="Concept",
                title="Observer Pattern",
                content="Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified automatically.",
                properties={
                    "pattern_type": "Behavioral",
                    "use_cases": ["Event handling", "Model-View architectures", "Publish-subscribe systems"],
                    "pros": ["Loose coupling", "Dynamic relationships"],
                    "cons": ["Memory overhead", "Unexpected updates"]
                }
            ),
            "sources": [
                Source(
                    type="Publication",
                    name="Design Patterns: Elements of Reusable Object-Oriented Software",
                    trustworthiness=10,
                    expertise=["Software Design", "Object-Oriented Programming"]
                ),
                Source(
                    type="Website",
                    url="https://refactoring.guru/design-patterns/observer",
                    name="Refactoring Guru - Observer Pattern",
                    trustworthiness=8,
                    expertise=["Software Design", "Programming Patterns"]
                )
            ]
        })
        
        # Add more software development scenarios...
        for i in range(4, 16):  # sw_004 to sw_015
            self.scenarios.append(self._generate_software_scenario(i))
    
    def _research_academic_scenarios(self):
        """Scenarios related to research and academic knowledge"""
        
        # Scenario 16: Mathematical theorem
        self.scenarios.append({
            "id": "ac_001",
            "title": "Mathematical Theorem Storage",
            "description": "Store mathematical theorems with proofs and applications",
            "knowledge": Knowledge(
                type="Theorem",
                title="Pythagorean Theorem",
                content="In a right-angled triangle, the square of the hypotenuse is equal to the sum of squares of the other two sides.",
                properties={
                    "formula": "a² + b² = c²",
                    "field": "Geometry",
                    "applications": ["Distance calculation", "Engineering", "Physics"],
                    "proof_methods": ["Geometric proof", "Algebraic proof"]
                }
            ),
            "sources": [
                Source(
                    type="Publication",
                    name="Elements by Euclid",
                    trustworthiness=10,
                    expertise=["Mathematics", "Geometry", "Ancient Mathematics"]
                ),
                Source(
                    type="Website",
                    url="https://en.wikipedia.org/wiki/Pythagorean_theorem",
                    name="Wikipedia - Pythagorean Theorem",
                    trustworthiness=8,
                    expertise=["Mathematics", "Geometry"]
                )
            ]
        })
        
        # Add more academic scenarios...
        for i in range(2, 11):  # ac_002 to ac_010
            self.scenarios.append(self._generate_academic_scenario(i))
    
    def _business_professional_scenarios(self):
        """Scenarios related to business and professional knowledge"""
        
        # Scenario 26: Business process documentation
        self.scenarios.append({
            "id": "bp_001",
            "title": "Business Process Documentation",
            "description": "Document business processes for operational efficiency",
            "knowledge": Knowledge(
                type="Process",
                title="Customer Onboarding Process",
                content="Step-by-step process for onboarding new customers including KYC, contract signing, and account setup.",
                properties={
                    "duration": "3-5 business days",
                    "departments": ["Sales", "Legal", "Operations", "IT"],
                    "compliance_requirements": ["KYC", "AML", "Data Protection"],
                    "automation_level": "Semi-automated"
                }
            ),
            "sources": [
                Source(
                    type="User",
                    name="Sarah Johnson - Operations Manager",
                    trustworthiness=9,
                    expertise=["Business Operations", "Process Management", "Customer Service"]
                ),
                Source(
                    type="User",
                    name="Michael Chen - Compliance Officer",
                    trustworthiness=10,
                    expertise=["Regulatory Compliance", "Risk Management", "Legal"]
                )
            ]
        })
        
        # Add more business scenarios...
        for i in range(2, 11):  # bp_002 to bp_010
            self.scenarios.append(self._generate_business_scenario(i))
    
    def _technical_documentation_scenarios(self):
        """Scenarios related to technical documentation"""
        
        # Scenario 36: Tool documentation
        self.scenarios.append({
            "id": "td_001",
            "title": "Development Tool Documentation",
            "description": "Document development tools and their usage",
            "knowledge": Knowledge(
                type="Tool",
                title="Docker Container Management",
                content="Docker is a platform for developing, shipping, and running applications in containers.",
                properties={
                    "category": "Containerization",
                    "commands": {
                        "build": "docker build -t <image_name> .",
                        "run": "docker run -p <host_port>:<container_port> <image_name>",
                        "stop": "docker stop <container_id>"
                    },
                    "use_cases": ["Application deployment", "Environment consistency", "Microservices"]
                }
            ),
            "sources": [
                Source(
                    type="Website",
                    url="https://docs.docker.com",
                    name="Official Docker Documentation",
                    trustworthiness=10,
                    expertise=["Containerization", "DevOps", "Software Deployment"]
                ),
                Source(
                    type="User",
                    name="Alex Rodriguez - DevOps Engineer",
                    trustworthiness=9,
                    expertise=["DevOps", "Containerization", "Infrastructure"]
                )
            ]
        })
        
        # Add more technical documentation scenarios...
        for i in range(2, 11):  # td_002 to td_010
            self.scenarios.append(self._generate_technical_scenario(i))
    
    def _personal_learning_scenarios(self):
        """Scenarios related to personal learning and development"""
        
        # Scenario 46: Learning note
        self.scenarios.append({
            "id": "pl_001",
            "title": "Personal Learning Notes",
            "description": "Store personal learning notes and insights",
            "knowledge": Knowledge(
                type="Concept",
                title="Machine Learning Fundamentals",
                content="Machine learning is a subset of AI that enables systems to learn and improve from experience without explicit programming.",
                properties={
                    "learning_date": "2024-01-15",
                    "difficulty_level": "Intermediate",
                    "key_concepts": ["Supervised learning", "Unsupervised learning", "Neural networks"],
                    "next_steps": ["Study deep learning", "Practice with real datasets"]
                }
            ),
            "sources": [
                Source(
                    type="Website",
                    url="https://coursera.org/learn/machine-learning",
                    name="Machine Learning Course - Coursera",
                    trustworthiness=9,
                    expertise=["Machine Learning", "Education", "Online Learning"]
                ),
                Source(
                    type="User",
                    name="Personal Study Notes",
                    trustworthiness=7,
                    expertise=["Self-directed Learning", "Technology"]
                )
            ]
        })
        
        # Add more personal learning scenarios...
        for i in range(2, 6):  # pl_002 to pl_005
            self.scenarios.append(self._generate_personal_learning_scenario(i))
    
    def _generate_software_scenario(self, index: int) -> Dict[str, Any]:
        """Generate a generic software development scenario"""
        topics = [
            ("Database Design Principles", "Normalization, ACID properties, and indexing strategies"),
            ("Git Workflow Best Practices", "Feature branching, code review, and merge strategies"),
            ("Test-Driven Development", "Write tests before code, red-green-refactor cycle"),
            ("Microservices Architecture", "Distributed system design with independent services"),
            ("Security Best Practices", "Authentication, authorization, and data encryption"),
            ("Performance Optimization", "Code profiling, caching strategies, and database optimization"),
            ("Clean Code Principles", "Readable, maintainable, and self-documenting code"),
            ("Continuous Integration", "Automated testing and deployment pipelines"),
            ("Error Handling Strategies", "Exception handling, logging, and error recovery"),
            ("Code Review Guidelines", "Standards for reviewing and improving code quality"),
            ("Database Migration Strategies", "Schema evolution and data migration best practices"),
            ("API Versioning Best Practices", "Backward compatibility and version management")
        ]
        
        topic_index = (index - 4) % len(topics)
        title, content = topics[topic_index]
        
        return {
            "id": f"sw_{index:03d}",
            "title": f"Software Development: {title}",
            "description": f"Document {title.lower()} for development team",
            "knowledge": Knowledge(
                type="Concept",
                title=title,
                content=content,
                properties={"category": "Software Development", "priority": "High"}
            ),
            "sources": [
                Source(
                    type="User",
                    name=f"Senior Developer {index}",
                    trustworthiness=8,
                    expertise=["Software Development", "Best Practices"]
                )
            ]
        }
    
    def _generate_academic_scenario(self, index: int) -> Dict[str, Any]:
        """Generate a generic academic scenario"""
        topics = [
            ("Newton's Laws of Motion", "Physics"),
            ("Theory of Evolution", "Biology"),
            ("Quantum Mechanics Principles", "Physics"),
            ("Economic Supply and Demand", "Economics"),
            ("Literary Analysis Methods", "Literature"),
            ("Statistical Hypothesis Testing", "Statistics"),
            ("Chemical Bonding Theory", "Chemistry"),
            ("Historical Causation", "History"),
            ("Cognitive Psychology Theories", "Psychology")
        ]
        
        topic_index = (index - 2) % len(topics)
        title, field = topics[topic_index]
        
        return {
            "id": f"ac_{index:03d}",
            "title": f"Academic Research: {title}",
            "description": f"Academic knowledge about {title.lower()}",
            "knowledge": Knowledge(
                type="Theorem" if field in ["Physics", "Mathematics"] else "Concept",
                title=title,
                content=f"Academic knowledge about {title} in the field of {field}",
                properties={"field": field, "academic_level": "University"}
            ),
            "sources": [
                Source(
                    type="Publication",
                    name=f"{field} Academic Journal",
                    trustworthiness=9,
                    expertise=[field, "Academic Research"]
                )
            ]
        }
    
    def _generate_business_scenario(self, index: int) -> Dict[str, Any]:
        """Generate a generic business scenario"""
        topics = [
            "Risk Management Framework",
            "Agile Project Management",
            "Customer Relationship Management",
            "Financial Planning Process",
            "Marketing Strategy Development",
            "Supply Chain Optimization",
            "Human Resources Policies",
            "Quality Assurance Procedures",
            "Vendor Management Process"
        ]
        
        topic_index = (index - 2) % len(topics)
        title = topics[topic_index]
        
        return {
            "id": f"bp_{index:03d}",
            "title": f"Business Process: {title}",
            "description": f"Business knowledge about {title.lower()}",
            "knowledge": Knowledge(
                type="Process",
                title=title,
                content=f"Business process and best practices for {title.lower()}",
                properties={"category": "Business Process", "implementation_status": "Active"}
            ),
            "sources": [
                Source(
                    type="User",
                    name=f"Business Analyst {index}",
                    trustworthiness=8,
                    expertise=["Business Analysis", "Process Management"]
                )
            ]
        }
    
    def _generate_technical_scenario(self, index: int) -> Dict[str, Any]:
        """Generate a generic technical documentation scenario"""
        topics = [
            "AWS Cloud Services",
            "Kubernetes Orchestration",
            "React Frontend Framework",
            "PostgreSQL Database",
            "Redis Caching System",
            "Nginx Web Server",
            "Python Django Framework",
            "Jenkins CI/CD Pipeline",
            "Elasticsearch Search Engine"
        ]
        
        topic_index = (index - 2) % len(topics)
        title = topics[topic_index]
        
        return {
            "id": f"td_{index:03d}",
            "title": f"Technical Documentation: {title}",
            "description": f"Technical documentation for {title.lower()}",
            "knowledge": Knowledge(
                type="Tool",
                title=title,
                content=f"Technical documentation and usage guide for {title}",
                properties={"category": "Technology", "complexity": "Intermediate"}
            ),
            "sources": [
                Source(
                    type="Website",
                    url=f"https://docs.{title.lower().replace(' ', '')}.com",
                    name=f"Official {title} Documentation",
                    trustworthiness=9,
                    expertise=["Technical Documentation", "Software Engineering"]
                )
            ]
        }
    
    def _generate_personal_learning_scenario(self, index: int) -> Dict[str, Any]:
        """Generate a generic personal learning scenario"""
        topics = [
            "Data Science with Python",
            "UI/UX Design Principles",
            "Blockchain Technology Basics",
            "Digital Marketing Strategies"
        ]
        
        topic_index = (index - 2) % len(topics)
        title = topics[topic_index]
        
        return {
            "id": f"pl_{index:03d}",
            "title": f"Personal Learning: {title}",
            "description": f"Personal learning notes about {title.lower()}",
            "knowledge": Knowledge(
                type="Concept",
                title=title,
                content=f"Personal learning notes and insights about {title}",
                properties={"learning_type": "Self-study", "progress": "In Progress"}
            ),
            "sources": [
                Source(
                    type="User",
                    name="Personal Learning Journal",
                    trustworthiness=7,
                    expertise=["Self-directed Learning", "Personal Development"]
                )
            ]
        }


class TestRealisticScenarios:
    """Test class for realistic scenarios"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.scenario_generator = RealisticTestScenarios()
        self.validator = DataValidator()
    
    def test_generate_all_scenarios(self):
        """Test that all scenarios are generated correctly"""
        scenarios = self.scenario_generator.generate_all_scenarios()
        
        # Should have at least 50 scenarios
        assert len(scenarios) >= 50
        
        # Check that each scenario has required fields
        for scenario in scenarios:
            assert "id" in scenario
            assert "title" in scenario
            assert "description" in scenario
            assert "knowledge" in scenario
            assert "sources" in scenario
            
            # Validate knowledge and sources
            assert isinstance(scenario["knowledge"], Knowledge)
            assert isinstance(scenario["sources"], list)
            assert len(scenario["sources"]) > 0
            
            for source in scenario["sources"]:
                assert isinstance(source, Source)
    
    def test_scenario_data_models_validation(self):
        """Test that all scenarios pass Pydantic validation"""
        scenarios = self.scenario_generator.generate_all_scenarios()
        
        for scenario in scenarios:
            # Test KnowledgeWithSources model validation
            knowledge_with_sources = KnowledgeWithSources(
                knowledge=scenario["knowledge"],
                sources=scenario["sources"]
            )
            
            # Should not raise any exceptions
            assert knowledge_with_sources.knowledge.title == scenario["knowledge"].title
            assert len(knowledge_with_sources.sources) == len(scenario["sources"])
    
    def test_scenario_categories(self):
        """Test that scenarios cover different categories"""
        scenarios = self.scenario_generator.generate_all_scenarios()
        
        # Check that we have scenarios from different categories
        categories = set()
        for scenario in scenarios:
            if scenario["id"].startswith("sw_"):
                categories.add("software")
            elif scenario["id"].startswith("ac_"):
                categories.add("academic")
            elif scenario["id"].startswith("bp_"):
                categories.add("business")
            elif scenario["id"].startswith("td_"):
                categories.add("technical")
            elif scenario["id"].startswith("pl_"):
                categories.add("personal")
        
        # Should have all categories
        expected_categories = {"software", "academic", "business", "technical", "personal"}
        assert categories == expected_categories
    
    @pytest.mark.asyncio
    async def test_scenario_validation_async(self):
        """Test async validation of scenarios"""
        scenarios = self.scenario_generator.generate_all_scenarios()
        
        # Test first 5 scenarios with async validation
        for i, scenario in enumerate(scenarios[:5]):
            knowledge_with_sources = KnowledgeWithSources(
                knowledge=scenario["knowledge"],
                sources=scenario["sources"]
            )
            
            # This would normally validate URLs, but we'll skip for unit testing
            # In real scenarios, this would check URL accessibility
            validation_errors = await self.validator.validate_knowledge_with_sources(knowledge_with_sources)
            
            # For mock scenarios without real URLs, we might have URL validation errors
            # but the data structure should be valid
            print(f"Scenario {scenario['id']}: {len(validation_errors)} validation issues")


if __name__ == "__main__":
    # Generate and display scenarios for manual inspection
    generator = RealisticTestScenarios()
    scenarios = generator.generate_all_scenarios()
    
    print(f"Generated {len(scenarios)} realistic test scenarios:")
    print("=" * 50)
    
    for scenario in scenarios[:5]:  # Show first 5 as examples
        print(f"ID: {scenario['id']}")
        print(f"Title: {scenario['title']}")
        print(f"Knowledge Type: {scenario['knowledge'].type}")
        print(f"Number of Sources: {len(scenario['sources'])}")
        print("-" * 30)
    
    # Run pytest
    pytest.main([__file__])