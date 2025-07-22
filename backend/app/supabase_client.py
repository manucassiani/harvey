import os
from typing import Optional, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Supabase configuration - using the same env vars as frontend
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY must be set in environment variables")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_from_token(token: str) -> Optional[Any]:
    """Get user information from JWT token"""
    try:
        response = supabase.auth.get_user(token)
        if response and hasattr(response, 'user'):
            return response.user
        return None
    except Exception as e:
        print(f"Error getting user from token: {e}")
        return None

def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user profile from database using the user ID as primary key"""
    try:
        response = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return response.data
    except Exception as e:
        print(f"Error getting user profile: {e}")
        return None 