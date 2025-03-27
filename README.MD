# Simplify Money Backend

A FastAPI-based backend service for the Simplify Money application.

## Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized deployment)
- pip (Python package manager)

## Project Setup

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/SyedHamadanAhmad/simplify-backend.git
   cd simplify-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python3 main.py
   ```

The application will be available at `http://localhost:8000`

### Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t simplify-money-backend .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 simplify-money-backend
   ```

The application will be available at `http://localhost:8000`

## API Documentation

### REST Endpoints

#### Chat Management

##### Store Chat Message
- **POST** `/chats`
- **Description**: Store a new chat message
- **Request Body**:
  ```json
  {
    "conversation_id": "string",
    "sender_id": "string",
    "recipient_id": "string",
    "message": "string"
  }
  ```
- **Response**: MessageResponse object with stored message details

##### Get Chats by Conversation ID
- **GET** `/chats/{conversation_id}`
- **Description**: Retrieve all messages for a specific conversation
- **Parameters**:
  - `conversation_id` (path): ID of the conversation
- **Response**: List of MessageResponse objects

##### Get User Chats
- **GET** `/users/{user_id}/chats`
- **Description**: Retrieve paginated chat messages for a specific user
- **Parameters**:
  - `user_id` (path): ID of the user
  - `page` (query): Page number (default: 1)
  - `limit` (query): Messages per page (default: 10, max: 50)
- **Response**: List of MessageResponse objects

##### Delete Chat
- **DELETE** `/chats/{conversation_id}`
- **Description**: Delete all messages in a conversation
- **Parameters**:
  - `conversation_id` (path): ID of the conversation
- **Response**: Deletion confirmation message

##### Summarize Chats
- **POST** `/chats/summarize`
- **Description**: Generate a summary of a conversation using AI
- **Request Body**:
  ```json
  {
    "conversation_id": "string"
  }
  ```
- **Response**: Summary of the conversation

### WebSocket Endpoints

#### Real-time Chat
- **WebSocket** `/ws/{user_id}`
- **Description**: WebSocket endpoint for real-time chat functionality
- **Parameters**:
  - `user_id` (path): ID of the user connecting
- **Message Format**:
  ```json
  {
    "message": "string",
    "recipient": "string"  // Optional, for direct messages
  }
  ```

#### Active Users
- **WebSocket** `/ws/users`
- **Description**: Get real-time list of active users
- **Response**: List of active user IDs (updates every 2 seconds)

#### Real-time Chat Summarization
- **WebSocket** `/ws/chats/summarize`
- **Description**: Real-time chat analysis with AI
- **Request Format**:
  ```json
  {
    "conversation_id": "string"
  }
  ```
- **Response Format**:
  ```json
  {
    "conversation_id": "string",
    "summary": "string",
    "sentiment": "string",
    "keywords": ["string"]
  }
  ```

## Project Structure

```
.
├── main.py              # Main application entry point
├── classes.py           # Core classes and models
├── socket_stuff.py      # WebSocket related functionality
├── routers/            # API route handlers
├── requirements.txt    # Project dependencies
└── Dockerfile         # Container configuration
```

## Development

- The application uses FastAPI framework
- WebSocket support is implemented for real-time features
- MongoDB is used as the database (via motor)
- AI-powered features using Google's Gemini API
- Real-time sentiment analysis and keyword extraction

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.






