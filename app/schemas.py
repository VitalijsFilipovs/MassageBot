from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class UserMe(BaseModel):
    id: int
    role: str
    name_display: Optional[str] = None

class MasseuseOut(BaseModel):
    user_id: int
    city: str
    description: str = ""
    services: Dict = Field(default_factory=dict)
    photos: List[str] = Field(default_factory=list)
    schedule: Dict = Field(default_factory=dict)
    subscription_status: str

class SearchQuery(BaseModel):
    city: Optional[str] = None
    service: Optional[str] = None
