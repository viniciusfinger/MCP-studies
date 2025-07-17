from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from message_role import MessageRole


class ChatMessage(BaseModel):
    session_id: str = Field(..., description="Session unique idenitifier")
    message: str = Field(..., description="Message")
    role: MessageRole = Field(default=MessageRole.HUMAN, description="Role of the message sender (ex: human, assistant)")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the message")
