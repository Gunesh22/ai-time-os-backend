from fastapi import APIRouter
from pydantic import BaseModel
from app.services.grok_service import GrokService

router = APIRouter()

class VoiceInputSchema(BaseModel):
    text: str

@router.post("/process")
async def process_voice_input(input_data: VoiceInputSchema):
    grok_response = await grok.process_command(input_data.text)
    
    # Store Event in Firebase (TODO: In next step)
    
    return {
        "status": "success",
        "reply": grok_response.get("reply_text", "Done."),
        "action_data": grok_response,
        "action": "acknowledge"
    }
