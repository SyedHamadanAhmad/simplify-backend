from fastapi import APIRouter, HTTPException, Query
from typing import List
from classes import MessageCreate, MessageResponse, SummarizeRequest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import google.generativeai as genai  # Gemini API

MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client.chat_db
router=APIRouter()

# genai.configure(api_key="AIzaSyD0aTssp3d7WGmpa4MuIXkmfBMsAfZMhwU")


# Store Chat Messages (POST /chats)
@router.post("/chats", response_model=MessageResponse)
async def store_chat_messages(msg: MessageCreate):
    message = {
        "conversation_id": msg.conversation_id,
        "sender_id": msg.sender_id,
        "recipient_id": msg.recipient_id,
        "message": msg.message,
        "created_at": str(asyncio.get_event_loop().time()),
    }
    result = await db.messages.insert_one(message)
    print(f"Chat saved! Chat from {msg.sender_id} to {msg.recipient_id}: {msg.message}")
    message["id"] = str(result.inserted_id)
    return message

# Retrieve Chats by Conversation ID (GET /chats/{conversation_id})
@router.get("/chats/{conversation_id}", response_model=List[MessageResponse])
async def get_chats_by_convo_id(conversation_id: str):
    messages = await db.messages.find({"conversation_id": conversation_id}).sort("created_at", -1).to_list(None)
    return [{"id": str(msg["_id"]), **msg} for msg in messages]

# Chat Summarization (POST /chats/summarize)
@router.post("/chats/summarize")
async def summarize_chats(request: SummarizeRequest):
    conversation_id = request.conversation_id  # Extract from request body
    chats = await db.messages.find({"conversation_id": conversation_id}).sort("created_at", -1).to_list(None)

    if not chats:
        raise HTTPException(status_code=404, detail="No chats found for this conversation")

    chat_texts = "\n".join([msg["message"] for msg in chats])

    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"Summarize the following chat:\n\n{chat_texts}")
        summary = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

    return {"conversation_id": conversation_id, "summary": summary}



@router.get("/users/{user_id}/chats", response_model=List[MessageResponse])
async def get_user_chats(user_id: str, page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=50)):
    skip = (page - 1) * limit
    messages = await db.messages.find({"sender_id": user_id}).sort("created_at", -1).skip(skip).limit(limit).to_list(None)
    return [{"id": str(msg["_id"]), **msg} for msg in messages]


@router.delete("/chats/{conversation_id}")
async def delete_chat(conversation_id: str):
    result = await db.messages.delete_many({"conversation_id": conversation_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No chats found to delete")
    return {"message": f"Deleted {result.deleted_count} messages from conversation {conversation_id}"}