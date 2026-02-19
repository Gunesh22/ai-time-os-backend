from fastapi import APIRouter, HTTPException
from app.schemas.event_schema import EventCreate
from app.services.event_service import EventService

router = APIRouter()

@router.post("/")
async def create_event(event: EventCreate):
    """Create a new event"""
    try:
        service = EventService()
        result = service.create_event(event)
        return {"status": "success", "event": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/today")
async def get_today_events():
    """Get all events for today"""
    try:
        service = EventService()
        events = service.get_today_events()
        return {"status": "success", "events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_all_events():
    """Get all events"""
    try:
        service = EventService()
        events = service.get_all_events()
        return {"status": "success", "events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{event_id}")
async def update_event(event_id: str, updates: dict):
    """Update an event"""
    try:
        service = EventService()
        result = service.update_event(event_id, updates)
        return {"status": "success", "event": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    """Delete an event"""
    try:
        service = EventService()
        service.delete_event(event_id)
        return {"status": "success", "message": "Event deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{event_id}/status")
async def update_event_status(event_id: str, status: str):
    """Mark event as completed/skipped"""
    try:
        service = EventService()
        result = service.update_status(event_id, status)
        return {"status": "success", "event": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
