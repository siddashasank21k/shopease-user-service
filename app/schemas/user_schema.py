from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field

class ProfileCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: Optional[str] = Field(None, pattern=r"^\+?[0-9]{10,15}$")
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    profile_image: Optional[str] = Field(None, max_length=255)

class ProfileUpdate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: Optional[str] = Field(None, pattern=r"^\+?[0-9]{10,15}$")
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    profile_image: Optional[str] = Field(None, max_length=255)

class ProfilePatch(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone_number: Optional[str] = Field(None, pattern=r"^\+?[0-9]{10,15}$")
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    profile_image: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

class ProfileResponse(BaseModel):
    id: int
    auth_user_id: int
    full_name: str
    phone_number: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]
    profile_image: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
