from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import create_db
from app.access.views import router as access_router
from app.session.engine import SessionEngine
from app.session.manager import ConnectionManager
from app.session.views import router as session_router


# Startup and shutdown logic for shared variables (db session, settings, connection manager, etc)
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

# CORS config for Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# include commitees here?
app.include_router(session_router, prefix="/committees", tags=["committees"])
app.include_router(access_router, prefix="/access", tags=["access"])
