from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.session.engine import SessionEngine
from app.session.manager import ConnectionManager
from app.session.views import router as session_router

app = FastAPI(title="WebMUN API")

# CORS config for Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()
engine = SessionEngine()

# lets manager and engine be long lived
app.state.connection_manager = manager
app.state.engine = engine

# include commitees here?
app.include_router(session_router, prefix="/committees", tags=["committees"])
