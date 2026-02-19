from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.firebase import init_firebase, get_db
from app.api.endpoints.voice import router as voice_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Firebase Admin SDK
    print(f"Starting {settings.PROJECT_NAME}...")
    init_firebase()
    
    # Check if DB is reachable
    db = get_db()
    if db:
        print("Backend connected to Firestore.")
    else:
        print("Firestore not connected.")
        
    yield
    # Shutdown
    print(f"Shutting down {settings.PROJECT_NAME}...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    version="1.0.1",
    description="Voice-First Daily Operating System Backend (Firebase)"
)

# Allow all origins for development (so mobile can connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voice_router, prefix="/api/v1/voice", tags=["Voice"])

@app.get("/")
async def root():
    return {
        "status": "online",
        "system": "AI Time OS (Firebase)",
        "version": app.version
    }

@app.get("/health")
async def health_check():
    db = get_db()
    status = "healthy" if db else "unhealthy"
    return {"status": status, "service": "Logic Engine + Firebase"}
