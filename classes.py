from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: str
    sender_id: str
    recipient_id: str
    message: str

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender_id: str
    recipient_id: str
    message: str
    created_at: str


class SummarizeRequest(BaseModel):
    conversation_id: str



