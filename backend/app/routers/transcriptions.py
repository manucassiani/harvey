from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..database import get_db
from ..models import User, Consultation, Transcription
from ..schemas import TranscriptionCreate, Transcription as TranscriptionSchema
from ..auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=TranscriptionSchema)
async def create_transcription(
    transcription: TranscriptionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if consultation exists and user has access
    result = await db.execute(
        select(Consultation).where(Consultation.id == transcription.consultation_id)
    )
    consultation = result.scalar_one_or_none()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Check if user has access to this consultation
    if consultation.patient_id != current_user.id and consultation.doctor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db_transcription = Transcription(**transcription.dict())
    db.add(db_transcription)
    
    # Update consultation status
    consultation.status = "completed"
    
    await db.commit()
    await db.refresh(db_transcription)
    
    return db_transcription

@router.get("/consultation/{consultation_id}", response_model=TranscriptionSchema)
async def get_transcription_by_consultation(
    consultation_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if consultation exists and user has access
    result = await db.execute(
        select(Consultation).where(Consultation.id == consultation_id)
    )
    consultation = result.scalar_one_or_none()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Check if user has access to this consultation
    if consultation.patient_id != current_user.id and consultation.doctor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get transcription
    result = await db.execute(
        select(Transcription).where(Transcription.consultation_id == consultation_id)
    )
    transcription = result.scalar_one_or_none()
    
    if not transcription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcription not found"
        )
    
    return transcription

@router.get("/{transcription_id}", response_model=TranscriptionSchema)
async def get_transcription(
    transcription_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Transcription).where(Transcription.id == transcription_id)
    )
    transcription = result.scalar_one_or_none()
    
    if not transcription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcription not found"
        )
    
    # Check if user has access to this transcription's consultation
    result = await db.execute(
        select(Consultation).where(Consultation.id == transcription.consultation_id)
    )
    consultation = result.scalar_one_or_none()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated consultation not found"
        )
    
    # Check if user has access to this consultation
    if consultation.patient_id != current_user.id and consultation.doctor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return transcription 