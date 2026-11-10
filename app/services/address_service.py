from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import UserProfile
from app.models.address_model import UserAddress
from app.schemas.address_schema import AddressCreate, AddressUpdate

class AddressService:
    @staticmethod
    def _get_user_profile(db: Session, auth_user_id: int) -> UserProfile:
        profile = db.query(UserProfile).filter(UserProfile.auth_user_id == auth_user_id).first()
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found. Please create profile first.")
        return profile

    @staticmethod
    def add_address(db: Session, auth_user_id: int, payload: AddressCreate) -> UserAddress:
        profile = AddressService._get_user_profile(db, auth_user_id)

        if payload.is_default:
            db.query(UserAddress).filter(UserAddress.user_id == profile.id).update({"is_default": False})

        existing_count = db.query(UserAddress).filter(UserAddress.user_id == profile.id).count()
        is_default = True if existing_count == 0 else payload.is_default

        address = UserAddress(
            user_id=profile.id,
            address_type=payload.address_type,
            full_name=payload.full_name,
            phone_number=payload.phone_number,
            address_line_1=payload.address_line_1,
            address_line_2=payload.address_line_2,
            city=payload.city,
            state=payload.state,
            country=payload.country,
            postal_code=payload.postal_code,
            is_default=is_default,
        )
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    @staticmethod
    def list_addresses(db: Session, auth_user_id: int) -> List[UserAddress]:
        profile = AddressService._get_user_profile(db, auth_user_id)
        return db.query(UserAddress).filter(UserAddress.user_id == profile.id).all()

    @staticmethod
    def get_address(db: Session, auth_user_id: int, address_id: int) -> UserAddress:
        profile = AddressService._get_user_profile(db, auth_user_id)
        address = db.query(UserAddress).filter(UserAddress.id == address_id, UserAddress.user_id == profile.id).first()
        if not address:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found or does not belong to you.")
        return address

    @staticmethod
    def update_address(db: Session, auth_user_id: int, address_id: int, payload: AddressUpdate) -> UserAddress:
        address = AddressService.get_address(db, auth_user_id, address_id)

        if payload.is_default:
            db.query(UserAddress).filter(UserAddress.user_id == address.user_id).update({"is_default": False})

        for key, val in payload.model_dump().items():
            setattr(address, key, val)

        db.commit()
        db.refresh(address)
        return address

    @staticmethod
    def set_default(db: Session, auth_user_id: int, address_id: int) -> UserAddress:
        address = AddressService.get_address(db, auth_user_id, address_id)
        db.query(UserAddress).filter(UserAddress.user_id == address.user_id).update({"is_default": False})
        address.is_default = True
        db.commit()
        db.refresh(address)
        return address

    @staticmethod
    def delete_address(db: Session, auth_user_id: int, address_id: int):
        address = AddressService.get_address(db, auth_user_id, address_id)
        was_default = address.is_default
        user_id = address.user_id
        db.delete(address)
        db.commit()

        if was_default:
            next_addr = db.query(UserAddress).filter(UserAddress.user_id == user_id).first()
            if next_addr:
                next_addr.is_default = True
                db.commit()

        return {"message": "Address deleted successfully."}
