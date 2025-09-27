from pydantic import BaseModel

class UserMe(BaseModel):
    id: int
    role: str
    name_display: str | None = None
