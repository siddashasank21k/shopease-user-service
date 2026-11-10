from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import UserProfile
from app.schemas.user_schema import ProfileCreate, ProfileUpdate, ProfilePatch

class UserService:
    @staticmethod
    def get_profile_by_auth_id(db: Session, auth_user_id: int) -> UserProfile:
        profile = db.query(UserProfile).filter(UserProfile.auth_user_id == auth_user_id).first()
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found.")
        return profile

    @staticmethod
    def create_profile(db: Session, auth_user_id: int, payload: ProfileCreate) -> UserProfile:
        existing = db.query(UserProfile).filter(UserProfile.auth_user_id == auth_user_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile already exists for this user.")
        profile = UserProfile(
            auth_user_id=auth_user_id,
            full_name=payload.full_name,
            phone_number=payload.phone_number,
            date_of_birth=payload.date_of_birth,
            gender=payload.gender,
            profile_image=payload.profile_image,
            is_active=True,
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def update_profile(db: Session, auth_user_id: int, payload: ProfileUpdate) -> UserProfile:
        profile = UserService.get_profile_by_auth_id(db, auth_user_id)
        profile.full_name = payload.full_name
        profile.phone_number = payload.phone_number
        profile.date_of_birth = payload.date_of_birth
        profile.gender = payload.gender
        profile.profile_image = payload.profile_image
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def patch_profile(db: Session, auth_user_id: int, payload: ProfilePatch) -> UserProfile:
        profile = UserService.get_profile_by_auth_id(db, auth_user_id)
        data = payload.model_dump(exclude_unset=True)
        for key, val in data.items():
            setattr(profile, key, val)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def delete_profile(db: Session, auth_user_id: int):
        profile = UserService.get_profile_by_auth_id(db, auth_user_id)
        db.delete(profile)
        db.commit()
        return {"message": "User profile and associated data deleted successfully."}
