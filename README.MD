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

Once the application is running, you can access:
- Swagger UI documentation at `http://localhost:8000/docs`
- ReDoc documentation at `http://localhost:8000/redoc`

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

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request






