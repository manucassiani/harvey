from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.supabase_client import supabase
from app.routers import auth

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Harvey Backend starting up...")
    print(f"📊 Connected to Supabase: {os.getenv('VITE_SUPABASE_URL', 'Not configured')}")
    
    # Test Supabase connection
    try:
        response = supabase.table("profiles").select("*").limit(1).execute()
        print("✅ Supabase connection successful")
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
    
    yield
    
    # Shutdown
    print("🛑 Harvey Backend shutting down...")

app = FastAPI(
    title="Harvey Medical API",
    description="API for Harvey Medical Assistant with Supabase",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Harvey Medical API with Supabase", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    try:
        # Test Supabase connection
        response = supabase.table("profiles").select("*").limit(1).execute()
        return {
            "status": "healthy",
            "database": "connected",
            "supabase_url": os.getenv("VITE_SUPABASE_URL", "Not configured")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 