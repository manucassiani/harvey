# Harvey Medical Assistant

A comprehensive medical assistant application that helps patients and doctors manage consultations, appointments, and medical records with AI-powered transcription and summary generation.

## 🏗️ Architecture

Harvey is built with a modern **separated architecture**:

- **Backend**: FastAPI REST API (Python) with Supabase integration
- **Frontend**: React web application (TypeScript + Vite)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **Storage**: Supabase Storage

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Supabase account and project

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd harvey
   ```

2. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase configuration
   ```

3. **Start Harvey (Automated)**
   ```bash
   ./start_harvey.sh
   ```

4. **Access the application**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🎯 Features

### Core Functionality
- **🔐 User Authentication**: Supabase Auth with profile management
- **📅 Medical Appointments**: Schedule, manage, and track medical appointments
- **🎙️ Consultation Recording**: Audio recording and transcription capabilities
- **🤖 AI-Powered Summaries**: Generate medical summaries using AI
- **📁 File Management**: Upload and manage medical documents and audio files
- **🔗 Secure Sharing**: Share consultation summaries via secure links
- **🚨 Emergency Access**: QR codes for emergency medical information

### User Roles
- **👤 Patients**: Schedule appointments, record consultations, view medical history
- **👨‍⚕️ Doctors**: Manage patient appointments, review consultations, approve summaries
- **🔧 Admins**: User management, system configuration, email whitelist management

### Technical Features
- **🔌 RESTful API**: Well-documented FastAPI backend
- **⚡ Modern Frontend**: React with TypeScript, Vite, and Tailwind CSS
- **🔄 Real-time Updates**: Efficient state management
- **📱 Responsive Design**: Mobile-first responsive interface
- **🔒 Security**: Supabase Auth, input validation, secure file uploads

## 📁 Project Structure

```
harvey/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── routers/           # API route handlers
│   │   │   ├── auth.py        # Authentication endpoints
│   │   │   ├── consultations.py # Medical consultations
│   │   │   ├── appointments.py # Medical appointments
│   │   │   ├── transcriptions.py # Audio transcriptions
│   │   │   ├── summaries.py   # AI-generated summaries
│   │   │   ├── profiles.py    # User profiles
│   │   │   └── admin.py       # Admin functionality
│   │   ├── supabase_client.py # Supabase configuration
│   │   ├── auth.py            # Authentication utilities
│   │   └── schemas.py         # Pydantic schemas
│   ├── static/                # Static files and uploads
│   ├── requirements.txt       # Python dependencies
│   └── main.py                # Application entry point
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── ui/           # Shadcn/ui components
│   │   │   ├── Auth.tsx      # Authentication UI
│   │   │   ├── AudioRecorder.tsx # Audio recording
│   │   │   ├── TranscriptionView.tsx # Transcription display
│   │   │   └── ...
│   │   ├── pages/            # Page components
│   │   │   ├── Dashboard.tsx # Main dashboard
│   │   │   ├── Notes.tsx     # Medical notes
│   │   │   ├── Appointments.tsx # Appointments
│   │   │   ├── Profile.tsx   # User profile
│   │   │   ├── Emergency.tsx # Emergency info
│   │   │   └── ...
│   │   ├── lib/              # Utilities and API client
│   │   │   ├── auth-context.tsx # Authentication context
│   │   │   ├── supabase.ts   # Supabase client
│   │   │   └── *-service.ts  # API services
│   │   └── types/            # TypeScript definitions
│   ├── public/               # Static assets
│   └── package.json
├── start_harvey.sh            # Start both services
├── stop_harvey.sh             # Stop all services
├── logs_harvey.sh             # Monitor logs
└── README.md
```

## 🔧 Development

### Quick Start with Scripts
For development, we provide convenient scripts to manage both services:

```bash
# Start both backend and frontend automatically
./start_harvey.sh

# Monitor logs in real-time (in another terminal)
./logs_harvey.sh

# Stop all services cleanly
./stop_harvey.sh
```

### Manual Development

#### Backend Development
```bash
cd backend
pyenv activate harvey  # or your virtual environment
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development
```bash
cd frontend
npm run dev
```

### Available Scripts

- **`start_harvey.sh`**: Automatically starts both backend and frontend services
  - Activates Python virtual environment
  - Installs dependencies if needed
  - Starts FastAPI backend on port 8000
  - Starts React frontend on port 8080
  - Monitors both services and provides status updates

- **`logs_harvey.sh`**: Monitor logs from both services in real-time
  - Shows colored output for better readability
  - Distinguishes between backend and frontend logs
  - Useful for debugging and monitoring

- **`stop_harvey.sh`**: Cleanly stops all Harvey services
  - Kills processes on ports 8000 and 8080
  - Cleans up log files
  - Ensures no background processes remain

## 📚 API Documentation

The backend provides comprehensive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key API Endpoints

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

#### Consultations
- `POST /api/consultations` - Create new consultation
- `GET /api/consultations` - Get user consultations
- `GET /api/consultations/{id}` - Get specific consultation

#### Appointments
- `POST /api/appointments` - Create appointment
- `GET /api/appointments` - Get user appointments
- `PUT /api/appointments/{id}` - Update appointment

#### Transcriptions & Summaries
- `POST /api/transcriptions` - Create transcription
- `POST /api/summaries` - Create summary
- `GET /api/summaries/consultation/{id}` - Get consultation summaries

## 🗄️ Database Schema

The application uses Supabase (PostgreSQL) with the following main entities:

- **`profiles`**: User profiles and medical information
- **`consultations`**: Medical consultations with audio recordings
- **`appointments`**: Medical appointments between patients and doctors
- **`transcriptions`**: Audio transcriptions of consultations
- **`summaries`**: AI-generated medical summaries

## 🔒 Security

- **Authentication**: Supabase Auth with JWT tokens
- **Authorization**: Role-based access control (Patient, Doctor, Admin)
- **Row Level Security**: Supabase RLS policies
- **Input Validation**: Pydantic schemas and TypeScript types
- **File Upload**: Secure file handling with Supabase Storage

## 🌍 Environment Variables

### Backend (.env)
```env
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
VITE_GEMINI_API_KEY=your-gemini-api-key
VITE_DEEPGRAM_API_KEY=your-deepgram-api-key
```

### Frontend (.env)
```env
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
VITE_GEMINI_API_KEY=your-gemini-api-key
VITE_DEEPGRAM_API_KEY=your-deepgram-api-key
```

## 🚀 Deployment

### Backend (FastAPI)
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend (React)
```bash
npm run build
# Deploy the dist/ folder to your static hosting service
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, please create an issue in the repository or contact the development team.

---

**Harvey** - Putting patients in control of their health data while revolutionizing doctor-patient communication.
