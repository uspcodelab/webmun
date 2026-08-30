import logging

from fastapi.requests import HTTPConnection
from redis.asyncio import Redis

from app.session.engine import SessionEngine
from app.session.manager import ConnectionManager


def get_connection_manager(connection: HTTPConnection) -> ConnectionManager:
    """Dependency injection for the app connection manager"""
    return connection.app.state.connection_manager


def get_session_engine(connection: HTTPConnection) -> SessionEngine:
    """Dependency injection for the app session engine"""
    return connection.app.state.session_engine


def get_logger(connection: HTTPConnection) -> logging.Logger:
    return connection.app.state.logger


def get_session_store(connection: HTTPConnection) -> Redis:
    """Dependency injection for Cache pool"""
    return connection.app.state.redis
