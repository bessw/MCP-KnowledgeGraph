"""
Configuration management for the Knowledge Graph MCP Server
"""
import yaml
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel, field_validator
from passlib.context import CryptContext


class Neo4jConfig(BaseModel):
    """Neo4j database configuration"""
    host: str
    username: str
    password: str


class ApiKeyConfig(BaseModel):
    """API key configuration"""
    key: str
    user: str


class Config(BaseModel):
    """Main configuration model"""
    neo4j: Dict[str, Neo4jConfig]
    api_keys: List[ApiKeyConfig]

    @field_validator('neo4j')
    @classmethod
    def validate_neo4j_config(cls, v):
        required_users = {'read_only', 'write'}
        if not required_users.issubset(v.keys()):
            raise ValueError(f"Neo4j config must contain {required_users}")
        return v


class ConfigManager:
    """Configuration manager for loading and managing app configuration"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.config: Config = self._load_config()
        self._hashed_api_keys = self._hash_api_keys()

    def _load_config(self) -> Config:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            config_data = yaml.safe_load(f)

        # Add host to each Neo4jConfig mapping
        host = config_data['neo4j'].pop('host')
        neo4j_configs = {}
        for key, neo4j_data in config_data['neo4j'].items():
            neo4j_data['host'] = host
            neo4j_configs[key] = Neo4jConfig(**neo4j_data)

        config_data['neo4j'] = neo4j_configs
        config_data['api_keys'] = [ApiKeyConfig(**api_key) for api_key in config_data['api_keys']]

        return Config(**config_data)

    def _hash_api_keys(self) -> Dict[str, str]:
        """Hash API keys for secure storage"""
        hashed_keys = {}
        for api_key_config in self.config.api_keys:
            hashed_key = self.pwd_context.hash(api_key_config.key)
            hashed_keys[hashed_key] = api_key_config.user
        return hashed_keys

    def verify_api_key(self, api_key: str) -> str | None:
        """Verify an API key and return the associated user if valid"""
        for hashed_key, user in self._hashed_api_keys.items():
            if self.pwd_context.verify(api_key, hashed_key):
                return user
        return None

    def get_neo4j_config(self, access_type: str) -> Neo4jConfig:
        """Get Neo4j configuration for read_only or write access"""
        if access_type not in ['read_only', 'write']:
            raise ValueError("access_type must be 'read_only' or 'write'")
        return self.config.neo4j[access_type]