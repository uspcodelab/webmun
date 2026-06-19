from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.session.views import create_session_router
from app.session.manager import ConnectionManager
from app.session.engine import SessionEngine
from app.session.service import SessionService

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
session_service = SessionService(manager, engine)

# include commitees here?
app.include_router(
        create_session_router(session_service),
        prefix="/committees",
        tags=["committees"]
)
