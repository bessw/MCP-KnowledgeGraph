"""
Knowledge Graph MCP Server
A FastAPI-based server for managing knowledge graphs with Neo4j backend.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ConfigManager
from app.database.neo4j_ops import Neo4jOperations
from app.validation.validators import DataValidator
from app.auth.security import init_auth
from app.api.endpoints import router as api_router, init_api_dependencies

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for dependency injection
config_manager: ConfigManager = None
db_operations: Neo4jOperations = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    global config_manager, db_operations
    
    try:
        # Initialize configuration
        config_manager = ConfigManager()
        logger.info("Configuration loaded successfully")
        
        # Initialize database operations
        read_config = config_manager.get_neo4j_config('read_only')
        write_config = config_manager.get_neo4j_config('write')
        db_operations = Neo4jOperations(read_config, write_config)
        logger.info("Database connections initialized")
        
        # Initialize authentication
        init_auth(config_manager)
        logger.info("Authentication system initialized")
        
        # Initialize API dependencies
        data_validator = DataValidator()
        init_api_dependencies(db_operations, data_validator)
        logger.info("API dependencies initialized")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise
    finally:
        # Cleanup
        if db_operations:
            db_operations.close_connections()
            logger.info("Database connections closed")


app = FastAPI(
    title="Knowledge Graph MCP Server",
    description="A server for storing, querying, and managing structured knowledge",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1", tags=["Knowledge Graph"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Knowledge Graph MCP Server is running"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)