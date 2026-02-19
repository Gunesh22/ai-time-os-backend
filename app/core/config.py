from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Time OS"
    API_V1_STR: str = "/api/v1"
    
    # AI Credentials (xAI)
    GROK_API_KEY: str = "your_key_here"  # Override in .env or Render Vars
    
    # Firebase Credential Path (Local)
    FIREBASE_CREDENTIALS_PATH: str = "serviceAccountKey.json"
    
    # Firebase Credential JSON (Cloud / Render)
    # Copy the entire content of serviceAccountKey.json into this ENV var on Render
    FIREBASE_CREDENTIALS_JSON: Optional[str] = None
    FIREBASE_CLIENT_EMAIL: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
