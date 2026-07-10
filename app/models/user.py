from enum import Enum
from sqlmodel import SQLModel,Field
from typing import Optional
from datetime import datetime,timezone



class UserRole(str,Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    SELLER = "seller"



class User(SQLModel,table=True):

    id: Optional[int] = Field(default=None,primary_key=True)
    username:str = Field(index=True,max_length=50,unique=True)
    email:str = Field(unique=True,index=True)
    hashed_password:str
    is_active:bool = True
    is_superuser:bool = False
    roles:UserRole = Field(default=UserRole.CUSTOMER)
    created_at:datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
