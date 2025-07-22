from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# Auth schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Profile schemas
class ProfileBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_history: Optional[str] = None
    avatar_url: Optional[str] = None
    is_doctor: bool = False
    doctor_license: Optional[str] = None
    specialization: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_history: Optional[str] = None
    avatar_url: Optional[str] = None
    is_doctor: Optional[bool] = None
    doctor_license: Optional[str] = None
    specialization: Optional[str] = None

class Profile(ProfileBase):
    id: UUID
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Appointment schemas
class AppointmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    scheduled_for: datetime
    duration_minutes: int = 30
    location: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    doctor_id: Optional[UUID] = None

class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_for: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: Optional[str] = None
    location: Optional[str] = None

class Appointment(AppointmentBase):
    id: UUID
    patient_id: UUID
    doctor_id: Optional[UUID] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Consultation schemas
class ConsultationBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    location: Optional[str] = None
    status: str = "pending"

class ConsultationCreate(ConsultationBase):
    doctor_id: Optional[UUID] = None

class ConsultationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None
    status: Optional[str] = None
    audio_url: Optional[str] = None

class Consultation(ConsultationBase):
    id: UUID
    patient_id: UUID
    doctor_id: Optional[UUID] = None
    audio_url: Optional[str] = None
    share_hash: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Transcription schemas
class TranscriptionBase(BaseModel):
    text: str
    confidence: Optional[float] = None
    language: Optional[str] = "en"

class TranscriptionCreate(TranscriptionBase):
    consultation_id: UUID

class TranscriptionUpdate(BaseModel):
    text: Optional[str] = None
    confidence: Optional[float] = None
    language: Optional[str] = None

class Transcription(TranscriptionBase):
    id: UUID
    consultation_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Summary schemas
class SummaryBase(BaseModel):
    type: str  # "patient", "medical", "comprehensive"
    content: str
    version: int = 1

class SummaryCreate(SummaryBase):
    consultation_id: UUID

class SummaryUpdate(BaseModel):
    content: Optional[str] = None
    version: Optional[int] = None

class Summary(SummaryBase):
    id: UUID
    consultation_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Email whitelist schemas
class EmailWhitelistBase(BaseModel):
    email: EmailStr

class EmailWhitelistCreate(EmailWhitelistBase):
    pass

class EmailWhitelist(EmailWhitelistBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

# Response schemas
class APIResponse(BaseModel):
    message: str
    data: Optional[dict] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict 