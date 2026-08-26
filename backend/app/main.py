from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from fastapi.responses import JSONResponse

import app.core.exceptions as exceptions
from app.access.views import router as access_router
from app.conference.views import router as conference_router
from app.core.config import get_settings
from app.core.database import create_db
from app.core.openapi import add_websocket_message_schemas
from app.session.engine import SessionEngine
from app.session.manager import ConnectionManager
from app.session.views import router as session_router


# Startup and shutdown logic for shared variables, such as
# (db session, settings, connection manager, etc)
# You can view more of this on "FastAPI Lifespan"
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup phase
    settings = get_settings()
    engine, session_factory = create_db(settings)
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory

    app.state.session_engine = SessionEngine()
    app.state.connection_manager = ConnectionManager()

    yield

    await engine.dispose()


app = FastAPI(
    title="WebMUN API",
    lifespan=lifespan,
)

# --- Exception Handlers


@app.exception_handler(exceptions.NotFoundError)
async def not_found_handler(request: Request, exc: exceptions.NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.exception_handler(exceptions.AccessDeniedError)
async def access_denied_handler(request: Request, exc: exceptions.AccessDeniedError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.message},
    )


@app.exception_handler(exceptions.ConflictError)
async def conflict_handler(request: Request, exc: exceptions.ConflictError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message},
    )


# --- Middlewares

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes

app.include_router(conference_router, prefix="/conferences", tags=["conferences"])
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
