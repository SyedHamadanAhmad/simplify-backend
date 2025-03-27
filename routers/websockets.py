from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import asyncio
from socket_stuff import ConnectionManager
import json
import textblob  # Sentiment Analysis
import yake  # Keyword Extraction
import google.generativeai as genai  # Gemini API
from classes import SummarizeRequest
from routers.chats import db

router = APIRouter()
manager = ConnectionManager()
genai.configure(api_key="AIzaSyD0aTssp3d7WGmpa4MuIXkmfBMsAfZMhwU")


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg_data = json.loads(data)
                print(f"Message Data received by {user_id}: {msg_data}")
                if 'message' not in msg_data:
                    continue
                
                if msg_data.get('recipient'):
                    recipient = msg_data['recipient']
                    message = msg_data['message']
                    await manager.send_personal_message(
                        json.dumps({
                            'sender': user_id, 
                            'message': message, 
                            'type': 'direct'
                        }), 
                        recipient
                    )
                else:
                    await manager.broadcast(
                        json.dumps({
                            'sender': user_id, 
                            'message': msg_data['message'], 
                            'type': 'broadcast'
                        }), 
                        user_id
                    )
            except json.JSONDecodeError:
                await manager.broadcast(f"{user_id}: {data}", user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)

@router.websocket("/ws/users")
async def get_active_users(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            users = manager.get_active_users()  # returns a list of active users
            await websocket.send_json({"users": users})
            await asyncio.sleep(2)  # Update every 2 seconds
    except WebSocketDisconnect:
        pass


@router.websocket("/ws/chats/summarize")
async def summarize_chats_ws(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            conversation_id = data.get("conversation_id")

            if not conversation_id:
                await websocket.send_json({"error": "Missing conversation_id"})
                continue
            
            chats = await db.messages.find({"conversation_id": conversation_id}).sort("created_at", -1).to_list(None)
            
            if not chats:
                await websocket.send_json({"error": "No chats found for this conversation"})
                continue
            
            chat_texts = "\n".join([msg["message"] for msg in chats])
            
            try:
                model = genai.GenerativeModel(
            "gemini-2.0-flash-exp", generation_config={"response_mime_type": "application/json"})
                
                prompt = f"""
                Analyze the following chat conversation and return a JSON response with:
                - "summary": A short summary of the conversation.
                - "sentiment": One of ["Positive", "Negative", "Neutral"] based on the overall tone.
                - "keywords": A list of the main topics discussed.

                Respond ONLY in valid JSON format.

                Chat transcript:
                {chat_texts}
                """
                
                response = model.generate_content(prompt)

                # Extract JSON response
                import json
                try:
                    parsed_response = json.loads(response.text)
                    await websocket.send_json({
                        "conversation_id": conversation_id,
                        "summary": parsed_response.get("summary", "No summary available"),
                        "sentiment": parsed_response.get("sentiment", "Unknown"),
                        "keywords": parsed_response.get("keywords", [])
                    })
                except json.JSONDecodeError:
                    await websocket.send_json({"error": "Invalid JSON response from Gemini"})

            except Exception as e:
                await websocket.send_json({"error": f"Gemini API error: {str(e)}"})
    
    except WebSocketDisconnect:
        print("Client disconnected")