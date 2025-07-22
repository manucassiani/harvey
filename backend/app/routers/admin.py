from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List

from ..database import get_db
from ..models import User, Profile, EmailWhitelist
from ..schemas import (
    User as UserSchema, 
    Profile as ProfileSchema,
    EmailWhitelistCreate, 
    EmailWhitelist as EmailWhitelistSchema
)
from ..auth import get_current_active_user

router = APIRouter()

async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Dependency to verify current user is admin"""
    if not current_user.profile or not current_user.profile.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

@router.get("/users", response_model=List[UserSchema])
async def get_all_users(
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all users - Admin only"""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific user - Admin only"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.post("/users/{user_id}/toggle-status")
async def toggle_user_status(
    user_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Toggle user active status - Admin only"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = not user.is_active
    await db.commit()
    
    return {"message": f"User {'activated' if user.is_active else 'deactivated'} successfully"}

@router.get("/profiles", response_model=List[ProfileSchema])
async def get_all_profiles(
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all profiles - Admin only"""
    result = await db.execute(select(Profile))
    profiles = result.scalars().all()
    return profiles

@router.post("/profiles/{profile_id}/toggle-admin")
async def toggle_admin_status(
    profile_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Toggle profile admin status - Admin only"""
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    profile.is_admin = not profile.is_admin
    await db.commit()
    
    return {"message": f"Admin status {'granted' if profile.is_admin else 'revoked'} successfully"}

@router.post("/profiles/{profile_id}/toggle-doctor")
async def toggle_doctor_status(
    profile_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Toggle profile doctor status - Admin only"""
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    profile.is_doctor = not profile.is_doctor
    await db.commit()
    
    return {"message": f"Doctor status {'granted' if profile.is_doctor else 'revoked'} successfully"}

@router.get("/email-whitelist", response_model=List[EmailWhitelistSchema])
async def get_email_whitelist(
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get email whitelist - Admin only"""
    result = await db.execute(select(EmailWhitelist))
    whitelist = result.scalars().all()
    return whitelist

@router.post("/email-whitelist", response_model=EmailWhitelistSchema)
async def add_email_to_whitelist(
    email_data: EmailWhitelistCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Add email to whitelist - Admin only"""
    # Check if email already exists
    result = await db.execute(
        select(EmailWhitelist).where(EmailWhitelist.email == email_data.email)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in whitelist"
        )
    
    whitelist_entry = EmailWhitelist(
        email=email_data.email,
        notes=email_data.notes,
        created_by=current_admin.id
    )
    
    db.add(whitelist_entry)
    await db.commit()
    await db.refresh(whitelist_entry)
    
    return whitelist_entry

@router.delete("/email-whitelist/{email_id}")
async def remove_email_from_whitelist(
    email_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove email from whitelist - Admin only"""
    result = await db.execute(
        select(EmailWhitelist).where(EmailWhitelist.id == email_id)
    )
    whitelist_entry = result.scalar_one_or_none()
    
    if not whitelist_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found in whitelist"
        )
    
    await db.execute(delete(EmailWhitelist).where(EmailWhitelist.id == email_id))
    await db.commit()
    
    return {"message": "Email removed from whitelist successfully"}

@router.get("/stats")
async def get_admin_stats(
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get admin dashboard stats - Admin only"""
    # Count users
    user_result = await db.execute(select(User))
    total_users = len(user_result.scalars().all())
    
    # Count active users
    active_user_result = await db.execute(select(User).where(User.is_active == True))
    active_users = len(active_user_result.scalars().all())
    
    # Count profiles
    profile_result = await db.execute(select(Profile))
    total_profiles = len(profile_result.scalars().all())
    
    # Count doctors
    doctor_result = await db.execute(select(Profile).where(Profile.is_doctor == True))
    total_doctors = len(doctor_result.scalars().all())
    
    # Count admins
    admin_result = await db.execute(select(Profile).where(Profile.is_admin == True))
    total_admins = len(admin_result.scalars().all())
    
    # Count whitelist entries
    whitelist_result = await db.execute(select(EmailWhitelist))
    total_whitelist = len(whitelist_result.scalars().all())
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_profiles": total_profiles,
        "total_doctors": total_doctors,
        "total_admins": total_admins,
        "total_whitelist": total_whitelist
    } 