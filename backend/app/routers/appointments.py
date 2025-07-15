from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import User, Appointment
from ..schemas import AppointmentCreate, AppointmentUpdate, Appointment as AppointmentSchema
from ..auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=AppointmentSchema)
async def create_appointment(
    appointment: AppointmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    db_appointment = Appointment(
        patient_id=current_user.id,
        **appointment.dict()
    )
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    
    return db_appointment

@router.get("/", response_model=List[AppointmentSchema])
async def get_user_appointments(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(
            or_(
                Appointment.patient_id == current_user.id,
                Appointment.doctor_id == current_user.id
            )
        ).order_by(Appointment.scheduled_for)
    )
    appointments = result.scalars().all()
    return appointments

@router.get("/upcoming", response_model=List[AppointmentSchema])
async def get_upcoming_appointments(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    now = datetime.utcnow()
    result = await db.execute(
        select(Appointment).where(
            and_(
                or_(
                    Appointment.patient_id == current_user.id,
                    Appointment.doctor_id == current_user.id
                ),
                Appointment.scheduled_for >= now,
                Appointment.status == "scheduled"
            )
        ).order_by(Appointment.scheduled_for)
    )
    appointments = result.scalars().all()
    return appointments

@router.get("/past", response_model=List[AppointmentSchema])
async def get_past_appointments(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    now = datetime.utcnow()
    result = await db.execute(
        select(Appointment).where(
            and_(
                or_(
                    Appointment.patient_id == current_user.id,
                    Appointment.doctor_id == current_user.id
                ),
                or_(
                    Appointment.scheduled_for < now,
                    Appointment.status == "completed"
                )
            )
        ).order_by(Appointment.scheduled_for.desc())
    )
    appointments = result.scalars().all()
    return appointments

@router.get("/{appointment_id}", response_model=AppointmentSchema)
async def get_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user has access to this appointment
    if appointment.patient_id != current_user.id and appointment.doctor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return appointment

@router.put("/{appointment_id}", response_model=AppointmentSchema)
async def update_appointment(
    appointment_id: str,
    appointment_update: AppointmentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user has access to this appointment
    if appointment.patient_id != current_user.id and appointment.doctor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update appointment fields
    update_data = appointment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(appointment, field, value)
    
    await db.commit()
    await db.refresh(appointment)
    
    return appointment

@router.delete("/{appointment_id}")
async def delete_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user has access to this appointment
    if appointment.patient_id != current_user.id and appointment.doctor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    await db.delete(appointment)
    await db.commit()
    
    return {"message": "Appointment deleted successfully"} 