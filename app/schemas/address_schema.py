from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class AddressCreate(BaseModel):
    address_type: str = Field("Home", max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    address_line_1: str = Field(..., min_length=5, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    country: str = Field("India", min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=3, max_length=20)
    is_default: bool = False

class AddressUpdate(BaseModel):
    address_type: str = Field("Home", max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    address_line_1: str = Field(..., min_length=5, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    country: str = Field("India", min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=3, max_length=20)
    is_default: Optional[bool] = False

class AddressResponse(BaseModel):
    id: int
    user_id: int
    address_type: str
    full_name: str
    phone_number: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state: str
    country: str
    postal_code: str
    is_default: bool
    created_at: datetime

    class Config:
        from_attributes = True
