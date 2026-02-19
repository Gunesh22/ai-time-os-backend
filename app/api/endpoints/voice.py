from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class VoiceInputSchema(BaseModel):
    text: str

@router.post("/process")
async def process_voice_input(input_data: VoiceInputSchema):
    # This is where we will hook up Grok later
    print(f"Received from Phone: {input_data.text}")
    
    # Mock Response for now
    mock_reply = f"I heard you say: '{input_data.text}'. Processing with Grok..."
    return {
        "status": "success",
        "reply": mock_reply,
        "action": "acknowledge"
    }
