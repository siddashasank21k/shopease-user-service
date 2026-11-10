from typing import List, Dict, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import get_current_user_claims
from app.schemas.address_schema import AddressCreate, AddressUpdate, AddressResponse
from app.services.address_service import AddressService

router = APIRouter(prefix="/api/users/addresses", tags=["User Addresses"])

@router.post("", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def add_address(
    payload: AddressCreate,
    claims: Dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db)
):
    return AddressService.add_address(db, claims["auth_user_id"], payload)

@router.get("", response_model=List[AddressResponse])
def list_addresses(
    claims: Dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db)
):
    return AddressService.list_addresses(db, claims["auth_user_id"])

@router.get("/{address_id}", response_model=AddressResponse)
def get_address(
    address_id: int,
    claims: Dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db)
):
    return AddressService.get_address(db, claims["auth_user_id"], address_id)

@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    payload: AddressUpdate,
    claims: Dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db)
):
    return AddressService.update_address(db, claims["auth_user_id"], address_id, payload)

@router.patch("/{address_id}/default", response_model=AddressResponse)
def set_default_address(
    address_id: int,
    claims: Dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db)
):
    return AddressService.set_default(db, claims["auth_user_id"], address_id)

@router.delete("/{address_id}")
def delete_address(
    address_id: int,
    claims: Dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db)
):
    return AddressService.delete_address(db, claims["auth_user_id"], address_id)
