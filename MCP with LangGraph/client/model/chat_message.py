from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from model.message_role import MessageRole


class ChatMessage(BaseModel):
    thread_id: str = Field(..., description="Thread unique idenitifier")
    content: str = Field(..., description="Message content")
    role: MessageRole = Field(default=MessageRole.HUMAN, description="Role of the message sender (ex: human, assistant)")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the message")
