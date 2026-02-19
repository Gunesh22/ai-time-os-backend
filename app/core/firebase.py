import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings
import os
import json

db = None  # Global Firestore client

def init_firebase():
    """
    Initializes the Firebase Admin SDK.
    Call this on application startup.
    """
    global db
    
    # Check if already initialized
    if firebase_admin._apps:
        db = firestore.client()
        return

    try:
        # 1. Try Loading from Environment Variable (Render / Cloud)
        if settings.FIREBASE_CREDENTIALS_JSON:
            print("Loading Firebase credentials from ENV Variable...")
            cred_dict = json.loads(settings.FIREBASE_CREDENTIALS_JSON)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            
        # 2. Try Loading from Local File
        elif os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
            print(f"Loading Firebase credentials from file: {settings.FIREBASE_CREDENTIALS_PATH}")
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            
        else:
            # Fallback for when path is not set or file missing (e.g. cloud run using default credentials)
            print("Warning: serviceAccountKey.json not found. Attempting default credentials.")
            firebase_admin.initialize_app()
            
        db = firestore.client()
        print("Firebase Admin SDK & Firestore Client initialized successfully.")
        
    except Exception as e:
        print(f"CRITICAL: Failed to initialize Firebase: {e}")
        # In production, you might want to raise this to stop startup
        pass

def get_db():
    return db
