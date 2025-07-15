from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any
from pydantic import BaseModel, EmailStr

from ..supabase_client import supabase
from ..auth import get_current_active_user

router = APIRouter()

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]

@router.post("/register", response_model=Dict[str, Any])
async def register(user: UserRegister):
    """Register a new user with Supabase"""
    try:
        # Sign up user with Supabase
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "full_name": user.full_name
                }
            }
        })
        
        if response.user:
            # Create profile in database - usar id del usuario como primary key
            profile_data = {
                "id": response.user.id,  # Usar el ID del usuario como primary key
                "full_name": user.full_name,
                "is_doctor": False,
                "created_at": "now()",
                "updated_at": "now()"
            }
            
            profile_response = supabase.table("profiles").insert(profile_data).execute()
            
            return {
                "message": "User registered successfully",
                "user": response.user,
                "profile": profile_response.data[0] if profile_response.data else None
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed"
            )
            
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    """Login user with Supabase"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        if response.user and response.session:
            # Set the session for the supabase client
            supabase.auth.set_session(response.session.access_token, response.session.refresh_token)
            
            # Get user profile using user ID
            profile_response = supabase.table("profiles").select("*").eq("id", response.user.id).execute()
            
            profile_data = None
            if profile_response.data:
                profile_data = profile_response.data[0]
            else:
                # Si no existe el perfil, crearlo automáticamente
                print(f"Creating profile for user: {response.user.id}")
                try:
                    # Obtener el nombre del usuario metadata
                    display_name = response.user.user_metadata.get('full_name', 'Usuario')
                    
                    profile_create_data = {
                        "id": response.user.id,
                        "full_name": display_name,
                        "is_doctor": False,
                        "is_admin": False,
                        "created_at": "now()",
                        "updated_at": "now()"
                    }
                    
                    create_response = supabase.table("profiles").insert(profile_create_data).execute()
                    if create_response.data:
                        profile_data = create_response.data[0]
                        print(f"Profile created successfully: {profile_data}")
                    else:
                        print("Failed to create profile")
                        
                except Exception as profile_error:
                    print(f"Error creating profile: {profile_error}")
                    # Continue without profile for now
                    pass
            
            return {
                "access_token": response.session.access_token,
                "token_type": "bearer",
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "profile": profile_data
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
            
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

@router.post("/logout")
async def logout():
    """Logout user"""
    try:
        supabase.auth.sign_out()
        return {"message": "Successfully logged out"}
    except Exception as e:
        print(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Logout failed"
        )

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

@router.get("/me/profile")
async def get_current_user_profile(current_user: dict = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user.get("profile", {}) 