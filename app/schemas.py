from pydantic import BaseModel, EmailStr
from typing import  Optional

class LeadCreate(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None 
    course: Optional[str] = None
    format: Optional[str] = None
    source: Optional[str] = None
    note: Optional[str] = None

    model_config = {
        "extra": "forbid"
    }
