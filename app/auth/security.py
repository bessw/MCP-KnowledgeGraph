"""
Authentication module for the Knowledge Graph MCP Server
"""
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import ConfigManager

security = HTTPBearer()
config_manager: ConfigManager = None


def init_auth(config_mgr: ConfigManager):
    """Initialize authentication with configuration manager"""
    global config_manager
    config_manager = config_mgr


def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Verify API key and return the associated user.
    This function is used as a dependency for protected endpoints.
    """
    if not config_manager:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authentication system not initialized"
        )
    
    api_key = credentials.credentials
    user = config_manager.verify_api_key(api_key)
    
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return user


def get_current_user(user: str = Depends(verify_api_key)) -> str:
    """Get current authenticated user (alias for verify_api_key)"""
    return user