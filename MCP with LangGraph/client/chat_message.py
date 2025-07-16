from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ChatMessage(BaseModel):
    session_id: Optional[str] = Field(None, description="Session unique idenitifier")
    message: str = Field(..., description="Message")
    role: str = Field(..., description="Role of the message sender (e.g. user, assistant)") #TODO: create a enum for the role
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the message")
