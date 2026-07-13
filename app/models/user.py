from enum import Enum
from sqlmodel import SQLModel,Field,Column,JSON,Relationship
from typing import Optional,List,TYPE_CHECKING
from datetime import datetime,timezone


if TYPE_CHECKING:
    from app.models.order import Order

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
    roles:List[UserRole] = Field(default_factory=lambda: ["customer"],
    sa_column=Column(JSON))
    created_at:datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    orders:List[Order] = Relationship(back_populates="user")
