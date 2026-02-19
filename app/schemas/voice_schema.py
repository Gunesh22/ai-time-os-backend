from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class VoiceInputSchema(BaseModel):
    text: str

class EventProposal(BaseModel):
    title: str
    start_time: str
    end_time: str
    priority: str
    is_fixed: bool

class VoiceResponse(BaseModel):
    status: str
    original_text: str
    intent: str  # "create_event", "reschedule", "query", "unknown"
    proposal: Optional[EventProposal] = None
    suggestion_text: str
    auto_executed: bool
    warnings: List[str] = []
