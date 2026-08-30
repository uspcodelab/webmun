import asyncio
from contextlib import asynccontextmanager, suppress

import redis.asyncio as redis
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from app.access.views import router as access_router
from app.core.config import get_settings
from app.core.database import create_db
from app.core.exceptions import AppException
from app.core.logging import configure_logging
from app.core.openapi import add_websocket_message_schemas
from app.session.engine import SessionEngine
from app.session.manager import ConnectionManager
from app.session.store import subscriber_worker
from app.session.views import router as session_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup phase
    logger = configure_logging(settings.LOG_LEVEL)
    app.state.logger = logger
    engine, session_factory = create_db(settings)
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory

    app.state.session_engine = SessionEngine()
    app.state.connection_manager = ConnectionManager()

    redis_client = redis.from_url(
        settings.REDIS_URL.get_secret_value(),
    )
    await redis_client.ping()

    app.state.redis = redis_client
    logger.info("Connected to Redis")
    task = asyncio.create_task(
        subscriber_worker(
            client=redis_client,
            connection_manager=app.state.connection_manager,
            logger=logger,
        )
    )

    try:
        yield

    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task

        await app.state.redis.aclose()
        await engine.dispose()
        logger.info("Application shutdown complete")


app = FastAPI(
    title="WebMUN API",
    lifespan=lifespan,
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


# CORS config for Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.list_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    if settings.ENVIRONMENT == "production"
    else ["*"],
    allow_headers=["Authorization", "Content-Type", "Accept"]
    if settings.ENVIRONMENT == "production"
    else ["*"],
)

# include commitees here?
app.include_router(session_router, prefix="/committees", tags=["committees"])
app.include_router(access_router, prefix="/access", tags=["access"])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    add_websocket_message_schemas(openapi_schema)
    app.openapi_schema = openapi_schema
    return openapi_schema


app.openapi = custom_openapi
