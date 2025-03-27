from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.routers.websockets import router as websocket_router
from backend.routers.chats import router as chat_router
from .socket_stuff import ConnectionManager
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(websocket_router)
app.include_router(chat_router)
# MongoDB Connection


# WebSocket Connection Manager
manager = ConnectionManager()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
