from app.core.firebase import get_db
from app.schemas.event_schema import EventCreate, EventResponse
from datetime import datetime, date
from typing import List, Optional

# Hardcoded user ID for MVP (single-user)
# Replace with Firebase Auth UID when multi-user is implemented
DEFAULT_USER_ID = "user_001"

class EventService:
    def __init__(self):
        self.db = get_db()
        if self.db is None:
            raise Exception("Firestore not initialized")

    def _get_events_ref(self, user_id: str = DEFAULT_USER_ID):
        """Returns reference to user's events collection"""
        return self.db.collection("users").document(user_id).collection("events")

    def create_event(self, event: EventCreate, user_id: str = DEFAULT_USER_ID) -> dict:
        """Create a new event in Firestore"""
        event_data = event.dict()
        event_data["created_at"] = datetime.now().isoformat()
        event_data["date"] = date.today().isoformat()  # Today by default
        
        doc_ref = self._get_events_ref(user_id).add(event_data)
        event_id = doc_ref[1].id
        
        return {"id": event_id, **event_data}

    def get_today_events(self, user_id: str = DEFAULT_USER_ID) -> List[dict]:
        """Get all events for today, sorted by start_time"""
        today = date.today().isoformat()
        
        events_ref = self._get_events_ref(user_id)
        query = events_ref.where("date", "==", today).order_by("start_time")
        
        events = []
        for doc in query.stream():
            event = doc.to_dict()
            event["id"] = doc.id
            events.append(event)
        
        return events

    def get_all_events(self, user_id: str = DEFAULT_USER_ID) -> List[dict]:
        """Get all events for user"""
        events = []
        for doc in self._get_events_ref(user_id).order_by("start_time").stream():
            event = doc.to_dict()
            event["id"] = doc.id
            events.append(event)
        return events

    def update_event(self, event_id: str, updates: dict, user_id: str = DEFAULT_USER_ID) -> dict:
        """Update an existing event"""
        doc_ref = self._get_events_ref(user_id).document(event_id)
        doc_ref.update(updates)
        updated = doc_ref.get().to_dict()
        updated["id"] = event_id
        return updated

    def delete_event(self, event_id: str, user_id: str = DEFAULT_USER_ID) -> bool:
        """Delete an event"""
        self._get_events_ref(user_id).document(event_id).delete()
        return True

    def update_status(self, event_id: str, status: str, user_id: str = DEFAULT_USER_ID) -> dict:
        """Mark event as completed/skipped"""
        return self.update_event(event_id, {"status": status}, user_id)
