# Harvey Medical API (Backend)

FastAPI-based backend for the Harvey Medical Assistant application.

## Features

- **Authentication**: JWT-based authentication with email whitelist
- **User Management**: User profiles with admin and doctor roles
- **Medical Appointments**: Create, update, and manage medical appointments
- **Consultations**: Medical consultation management with audio recording
- **Transcriptions**: Audio transcription processing
- **Summaries**: AI-generated medical summaries
- **File Storage**: Audio files, avatars, and document uploads
- **Admin Panel**: Administrative functions for user and system management

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Virtual environment tool (venv, virtualenv, or conda)

### Installation

1. Clone the repository and navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Set up the database:
```bash
# Create a PostgreSQL database
createdb harvey_db

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://username:password@localhost/harvey_db
```

6. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   └── routers/             # API route handlers
│       ├── auth.py
│       ├── appointments.py
│       ├── consultations.py
│       ├── transcriptions.py
│       ├── summaries.py
│       ├── profiles.py
│       └── admin.py
├── static/                  # Static files and uploads
├── requirements.txt
├── .env.example
└── README.md
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `GOOGLE_AI_API_KEY`: Google AI API key for transcription
- `UPLOAD_DIR`: Directory for file uploads
- `MAX_FILE_SIZE`: Maximum file size for uploads

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user
- `GET /api/auth/me/profile` - Get current user profile

### Appointments
- `POST /api/appointments` - Create appointment
- `GET /api/appointments` - Get user appointments
- `GET /api/appointments/upcoming` - Get upcoming appointments
- `GET /api/appointments/past` - Get past appointments
- `GET /api/appointments/{id}` - Get specific appointment
- `PUT /api/appointments/{id}` - Update appointment
- `DELETE /api/appointments/{id}` - Delete appointment

### Consultations
- `POST /api/consultations` - Create consultation
- `GET /api/consultations` - Get user consultations
- `GET /api/consultations/{id}` - Get specific consultation
- `GET /api/consultations/share/{hash}` - Get consultation by share hash
- `PUT /api/consultations/{id}` - Update consultation
- `POST /api/consultations/{id}/audio` - Upload audio file

### Transcriptions
- `POST /api/transcriptions` - Create transcription
- `GET /api/transcriptions/consultation/{id}` - Get transcription by consultation
- `GET /api/transcriptions/{id}` - Get specific transcription

### Summaries
- `POST /api/summaries` - Create summary
- `GET /api/summaries/consultation/{id}` - Get summaries by consultation
- `GET /api/summaries/consultation/{id}/type/{type}` - Get summary by type
- `GET /api/summaries/{id}` - Get specific summary

### Admin
- `POST /api/admin/whitelist` - Add email to whitelist
- `GET /api/admin/whitelist` - Get whitelisted emails
- `DELETE /api/admin/whitelist/{id}` - Remove email from whitelist
- `GET /api/admin/users` - Get all users
- `PUT /api/admin/users/{id}/admin` - Toggle admin status
- `PUT /api/admin/users/{id}/doctor` - Toggle doctor status

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Code Formatting
```bash
black .
isort .
```

## Production Deployment

1. Set up a production PostgreSQL database
2. Configure environment variables for production
3. Use a production WSGI server like Gunicorn:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Security Considerations

- Keep `SECRET_KEY` secure and unique
- Use HTTPS in production
- Regularly update dependencies
- Implement proper database access controls
- Monitor and log API access 