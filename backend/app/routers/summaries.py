from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..database import get_db
from ..models import User, Consultation, Summary
from ..schemas import SummaryCreate, Summary as SummarySchema
from ..auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=SummarySchema)
async def create_summary(
    summary: SummaryCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if consultation exists and user has access
    result = await db.execute(
        select(Consultation).where(Consultation.id == summary.consultation_id)
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
    
    db_summary = Summary(**summary.dict())
    db.add(db_summary)
    await db.commit()
    await db.refresh(db_summary)
    
    return db_summary

@router.get("/consultation/{consultation_id}", response_model=List[SummarySchema])
async def get_summaries_by_consultation(
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
    
    # Get summaries
    result = await db.execute(
        select(Summary).where(Summary.consultation_id == consultation_id)
        .order_by(Summary.created_at.desc())
    )
    summaries = result.scalars().all()
    
    return summaries

@router.get("/consultation/{consultation_id}/type/{summary_type}", response_model=SummarySchema)
async def get_summary_by_type(
    consultation_id: str,
    summary_type: str,
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
    
    # Get summary by type
    result = await db.execute(
        select(Summary).where(
            Summary.consultation_id == consultation_id,
            Summary.type == summary_type
        ).order_by(Summary.created_at.desc())
    )
    summary = result.scalar_one_or_none()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Summary of type '{summary_type}' not found"
        )
    
    return summary

@router.get("/{summary_id}", response_model=SummarySchema)
async def get_summary(
    summary_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Summary).where(Summary.id == summary_id)
    )
    summary = result.scalar_one_or_none()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary not found"
        )
    
    # Check if user has access to this summary's consultation
    result = await db.execute(
        select(Consultation).where(Consultation.id == summary.consultation_id)
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
    
    return summary 