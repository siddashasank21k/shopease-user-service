from typing import Dict, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import get_current_user_claims
from app.schemas.user_schema import ProfileCreate, ProfileUpdate, ProfilePatch, ProfileResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users/profile", tags=["User Profile"])

@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    payload: ProfileCreate,
    claims: Dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db)
):
    return UserService.create_profile(db, claims["auth_user_id"], payload)

@router.get("", response_model=ProfileResponse)
def get_profile(
    claims: Dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db)
):
    return UserService.get_profile_by_auth_id(db, claims["auth_user_id"])

@router.put("", response_model=ProfileResponse)
def update_profile(
    payload: ProfileUpdate,
    claims: Dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db)
):
    return UserService.update_profile(db, claims["auth_user_id"], payload)

@router.patch("", response_model=ProfileResponse)
def patch_profile(
    payload: ProfilePatch,
    claims: Dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db)
):
    return UserService.patch_profile(db, claims["auth_user_id"], payload)

@router.delete("")
def delete_profile(
    claims: Dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db)
):
    return UserService.delete_profile(db, claims["auth_user_id"])
