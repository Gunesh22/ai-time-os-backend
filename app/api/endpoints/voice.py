from fastapi import APIRouter
from pydantic import BaseModel
from app.services.grok_service import GrokService
from app.services.event_service import EventService
from app.schemas.event_schema import EventCreate

router = APIRouter()
grok = GrokService()

class VoiceInputSchema(BaseModel):
    text: str

@router.post("/process")
async def process_voice_input(input_data: VoiceInputSchema):
    grok_response = await grok.process_command(input_data.text)
    
    saved_event = None
    
    # Auto-save to Firestore if Grok detected an event creation
    if grok_response.get("action") == "create_event" and grok_response.get("event"):
        try:
            event_data = grok_response["event"]
            event = EventCreate(
                title=event_data.get("title", "Untitled"),
                start_time=event_data.get("start_time", "00:00"),
                end_time=event_data.get("end_time", "00:00"),
                priority=event_data.get("priority", "medium"),
                is_fixed=event_data.get("is_fixed", False),
                created_via="voice",
            )
            service = EventService()
            saved_event = service.create_event(event)
        except Exception as e:
            print(f"Failed to save event: {e}")
    
    return {
        "status": "success",
        "reply": grok_response.get("reply_text", "Done."),
        "action_data": grok_response,
        "saved_event": saved_event,
        "action": "acknowledge"
    }
