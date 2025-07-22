from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import os
import shutil
from uuid import uuid4

from ..database import get_db
from ..models import User, Profile
from ..schemas import ProfileCreate, ProfileUpdate, Profile as ProfileSchema
from ..auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=ProfileSchema)
async def create_profile(
    profile: ProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if profile already exists
    if current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists"
        )
    
    db_profile = Profile(
        user_id=current_user.id,
        **profile.dict()
    )
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    
    return db_profile

@router.get("/{user_id}", response_model=ProfileSchema)
async def get_profile(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Profile).where(Profile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

@router.put("/", response_model=ProfileSchema)
async def update_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update profile fields
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user.profile, field, value)
    
    await db.commit()
    await db.refresh(current_user.profile)
    
    return current_user.profile

@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Create uploads directory if it doesn't exist
    upload_dir = "static/uploads/avatars"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update profile with avatar URL
    current_user.profile.avatar_url = f"/static/uploads/avatars/{filename}"
    await db.commit()
    
    return {"avatar_url": current_user.profile.avatar_url}

@router.get("/doctors/list", response_model=List[ProfileSchema])
async def get_doctors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Profile).where(Profile.is_doctor == True)
    )
    doctors = result.scalars().all()
    return doctors 