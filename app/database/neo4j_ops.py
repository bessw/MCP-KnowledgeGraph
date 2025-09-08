"""
Neo4j database connection and operations
"""
import logging
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable, AuthError

from app.config import Neo4jConfig
from app.models.schemas import Knowledge, Source, KnowledgeWithSources

logger = logging.getLogger(__name__)


class Neo4jConnection:
    """Neo4j database connection manager"""
    
    def __init__(self, config: Neo4jConfig):
        self.config = config
        self._driver: Optional[Driver] = None

    def connect(self) -> Driver:
        """Create and return a Neo4j driver"""
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(
                    self.config.host,
                    auth=(self.config.username, self.config.password)
                )
                # Test the connection
                with self._driver.session() as session:
                    session.run("RETURN 1").single()
                logger.info(f"Successfully connected to Neo4j at {self.config.host}")
            except (ServiceUnavailable, AuthError) as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
                raise
        return self._driver

    def close(self):
        """Close the Neo4j driver connection"""
        if self._driver:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j connection closed")

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Neo4jOperations:
    """Neo4j database operations"""
    
    def __init__(self, read_config: Neo4jConfig, write_config: Neo4jConfig):
        self.read_connection = Neo4jConnection(read_config)
        self.write_connection = Neo4jConnection(write_config)

    def execute_read_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a read-only query"""
        if parameters is None:
            parameters = {}
        
        try:
            with self.read_connection.connect() as driver:
                with driver.session() as session:
                    result = session.run(query, parameters)
                    return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Error executing read query: {e}")
            raise

    def execute_write_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a write query"""
        if parameters is None:
            parameters = {}
        
        try:
            with self.write_connection.connect() as driver:
                with driver.session() as session:
                    result = session.run(query, parameters)
                    return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Error executing write query: {e}")
            raise

    def create_source(self, source: Source) -> str:
        """Create a Source node and return its ID"""
        query = """
        CREATE (s:Source {
            type: $type,
            url: $url,
            name: $name,
            trustworthiness: $trustworthiness,
            expertise: $expertise,
            created_at: timestamp()
        })
        RETURN elementId(s) as id
        """
        
        parameters = {
            'type': source.type,
            'url': source.url,
            'name': source.name,
            'trustworthiness': source.trustworthiness,
            'expertise': source.expertise
        }
        
        result = self.execute_write_query(query, parameters)
        return result[0]['id']

    def create_knowledge(self, knowledge: Knowledge) -> str:
        """Create a Knowledge node and return its ID"""
        query = """
        CREATE (k:Knowledge {
            type: $type,
            title: $title,
            content: $content,
            properties: $properties,
            created_at: timestamp()
        })
        RETURN elementId(k) as id
        """
        
        parameters = {
            'type': knowledge.type,
            'title': knowledge.title,
            'content': knowledge.content,
            'properties': knowledge.properties or {}
        }
        
        result = self.execute_write_query(query, parameters)
        return result[0]['id']

    def link_knowledge_to_sources(self, knowledge_id: str, source_ids: List[str]) -> None:
        """Create DERIVED_FROM relationships between Knowledge and Source nodes"""
        query = """
        MATCH (k:Knowledge), (s:Source)
        WHERE elementId(k) = $knowledge_id AND elementId(s) IN $source_ids
        CREATE (k)-[:DERIVED_FROM {created_at: timestamp()}]->(s)
        """
        
        parameters = {
            'knowledge_id': knowledge_id,
            'source_ids': source_ids
        }
        
        self.execute_write_query(query, parameters)

    def create_knowledge_with_sources(self, knowledge_data: KnowledgeWithSources) -> Dict[str, Any]:
        """Create Knowledge node with associated Sources and relationships"""
        # Create sources first
        source_ids = []
        for source in knowledge_data.sources:
            source_id = self.create_source(source)
            source_ids.append(source_id)

        # Create knowledge node
        knowledge_id = self.create_knowledge(knowledge_data.knowledge)

        # Create relationships
        self.link_knowledge_to_sources(knowledge_id, source_ids)

        return {
            'knowledge_id': knowledge_id,
            'source_ids': source_ids
        }

    def get_knowledge_with_sources(self, knowledge_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a Knowledge node with its associated Sources"""
        query = """
        MATCH (k:Knowledge)-[:DERIVED_FROM]->(s:Source)
        WHERE elementId(k) = $knowledge_id
        RETURN k, collect(s) as sources
        """
        
        parameters = {'knowledge_id': knowledge_id}
        result = self.execute_read_query(query, parameters)
        
        if result:
            return result[0]
        return None

    def search_knowledge(self, search_term: str, knowledge_type: str = None) -> List[Dict[str, Any]]:
        """Search for Knowledge nodes by title or content"""
        query_parts = [
            "MATCH (k:Knowledge)-[:DERIVED_FROM]->(s:Source)",
            "WHERE k.title CONTAINS $search_term OR k.content CONTAINS $search_term"
        ]
        
        parameters = {'search_term': search_term}
        
        if knowledge_type:
            query_parts.append("AND k.type = $knowledge_type")
            parameters['knowledge_type'] = knowledge_type
        
        query_parts.append("RETURN k, collect(s) as sources")
        query = "\n".join(query_parts)
        
        return self.execute_read_query(query, parameters)

    def close_connections(self):
        """Close all database connections"""
        self.read_connection.close()
        self.write_connection.close()