from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.committee.views import router as committee_router # Import different domains routers

app = FastAPI(title="WebMUN API")

# CORS config for Vite 
app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"]
)

# include commitees here?
app.include_router(committee_router, prefix="/committees", tags=["Committees"])

