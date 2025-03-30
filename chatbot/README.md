# AI Chatbot System

A full-stack AI chatbot platform with training capabilities and multi-platform integration.

## Features

- **Backend**: Python FastAPI with PostgreSQL database
- **Frontend**: React.js admin dashboard
- **Training**: Script-based learning with NLP
- **Integrations**: WhatsApp, Telegram, Instagram, Discord
- **Multi-bot support**: Different personalities per bot

## Prerequisites

- Docker and Docker Compose
- Node.js (for frontend development)
- Python 3.9+ (for backend development)

## Installation

1. Clone the repository
2. Run the following commands:

```bash
# Start all services
docker-compose up -d

# Initialize database (run after services are up)
docker-compose exec backend python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"

# Create admin user (optional)
docker-compose exec backend python -c "from auth import get_password_hash; print(get_password_hash('admin'))"
# Then manually add user to database
```

## Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Environment Variables

Create `.env` files in both `backend` and `frontend` directories:

**backend/.env**
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/chatbot
SECRET_KEY=your-secret-key-here
```

**frontend/.env**
```
REACT_APP_API_URL=http://localhost:8000
```

## API Documentation

After starting the backend, visit:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## License

MIT