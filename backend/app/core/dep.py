from fastapi.requests import HTTPConnection
from app.session.manager import ConnectionManager
from app.session.engine import SessionEngine
import logging


def get_connection_manager(connection: HTTPConnection) -> ConnectionManager:
    """Dependency injection for the app connection manager"""
    return connection.app.state.connection_manager


def get_session_engine(connection: HTTPConnection) -> SessionEngine:
    """Dependency injection for the app session engine"""
    return connection.app.state.session_engine


def get_logger() -> logging.Logger:
    return logging.getLogger("uvicorn.error")
