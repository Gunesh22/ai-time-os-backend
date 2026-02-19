from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    start_time: str         # "09:00"
    end_time: str            # "11:00"
    priority: str = "medium" # high, medium, low
    is_fixed: bool = False
    energy_level_required: str = "medium"  # high, medium, low
    created_via: str = "manual"            # voice, manual, ai
    status: str = "scheduled"              # scheduled, completed, skipped
    notes: Optional[str] = None

class EventResponse(BaseModel):
    id: str
    title: str
    start_time: str
    end_time: str
    priority: str
    is_fixed: bool
    energy_level_required: str
    created_via: str
    status: str
    notes: Optional[str] = None
    created_at: Optional[str] = None
