from fastapi import Request
from app.session.manager import ConnectionManager
from app.session.engine import SessionEngine
import logging


def get_connection_manager(request: Request) -> ConnectionManager:
    """Dependency injection for the app connection manager"""
    return request.app.state.connection_manager


def get_session_engine(request: Request) -> SessionEngine:
    """Dependency injection for the app session engine"""
    return request.app.state.session_engine


def get_logger() -> logging.Logger:
    return logging.getLogger("uvicorn.error")
