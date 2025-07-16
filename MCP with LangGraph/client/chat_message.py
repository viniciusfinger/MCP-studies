from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from message_role import MessageRole


class ChatMessage(BaseModel):
    session_id: str = Field(..., description="Session unique idenitifier")
    message: str = Field(..., description="Message")
    role: MessageRole = Field(..., description="Role of the message sender (e.g. user, assistant)")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the message")
