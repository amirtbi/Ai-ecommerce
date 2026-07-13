from pydantic import BaseModel,ConfigDict
from typing import List
from app.models.user import UserRole


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    roles:List[UserRole] = [UserRole.CUSTOMER]


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    roles:List[UserRole]
    model_config = ConfigDict(from_attributes=True) 



