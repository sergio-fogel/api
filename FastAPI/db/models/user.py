from pydantic import BaseModel
from typing import Optional

# user entity
class User(BaseModel):
    id: Optional[str]
    username: str
    email: str

