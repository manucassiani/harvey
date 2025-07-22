from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from pydantic import BaseModel
import uuid
import hashlib

from ..supabase_client import supabase
from ..auth import get_current_active_user

router = APIRouter()

class ConsultationCreate(BaseModel):
    title: str
    description: str = ""
    doctor_id: str = None

class ConsultationUpdate(BaseModel):
    title: str = None
    description: str = None
    status: str = None

@router.post("/", response_model=Dict[str, Any])
async def create_consultation(
    consultation: ConsultationCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new consultation"""
    try:
        # Generate share hash
        share_hash = hashlib.md5(f"{current_user['id']}{consultation.title}".encode()).hexdigest()[:16]
        
        consultation_data = {
            "patient_id": current_user["id"],
            "doctor_id": consultation.doctor_id,
            "title": consultation.title,
            "description": consultation.description,
            "share_hash": share_hash,
            "status": "pending",
            "created_at": "now()",
            "updated_at": "now()"
        }
        
        response = supabase.table("consultations").insert(consultation_data).execute()
        
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create consultation"
            )
            
    except Exception as e:
        print(f"Error creating consultation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/", response_model=List[Dict[str, Any]])
async def get_consultations(
    current_user: dict = Depends(get_current_active_user)
):
    """Get user consultations"""
    try:
        response = supabase.table("consultations").select("*").eq("patient_id", current_user["id"]).execute()
        return response.data if response.data else []
        
    except Exception as e:
        print(f"Error getting consultations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/{consultation_id}", response_model=Dict[str, Any])
async def get_consultation(
    consultation_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Get specific consultation"""
    try:
        response = supabase.table("consultations").select("*").eq("id", consultation_id).single().execute()
        
        if response.data:
            consultation = response.data
            # Check if user has access to this consultation
            if consultation["patient_id"] != current_user["id"] and consultation.get("doctor_id") != current_user["id"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )
            return consultation
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting consultation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/share/{share_hash}", response_model=Dict[str, Any])
async def get_consultation_by_share(share_hash: str):
    """Get consultation by share hash (public access)"""
    try:
        response = supabase.table("consultations").select("*").eq("share_hash", share_hash).single().execute()
        
        if response.data:
            return response.data
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting consultation by share: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/{consultation_id}", response_model=Dict[str, Any])
async def update_consultation(
    consultation_id: str,
    consultation: ConsultationUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """Update consultation"""
    try:
        # Check if consultation exists and user has access
        existing_response = supabase.table("consultations").select("*").eq("id", consultation_id).single().execute()
        
        if not existing_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation not found"
            )
            
        existing_consultation = existing_response.data
        if existing_consultation["patient_id"] != current_user["id"] and existing_consultation.get("doctor_id") != current_user["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Update consultation
        update_data = {k: v for k, v in consultation.dict().items() if v is not None}
        update_data["updated_at"] = "now()"
        
        response = supabase.table("consultations").update(update_data).eq("id", consultation_id).execute()
        
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update consultation"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating consultation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 