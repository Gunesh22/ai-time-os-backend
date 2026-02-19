from fastapi import APIRouter
from pydantic import BaseModel
from app.services.grok_service import GrokService

router = APIRouter()

class VoiceInputSchema(BaseModel):
    text: str

@router.post("/process")
async def process_voice_input(input_data: VoiceInputSchema):
    grok = GrokService()
    reply = await grok.process_command(input_data.text)
    
    return {
        "status": "success",
        "reply": reply,
        "action": "acknowledge"
    }
