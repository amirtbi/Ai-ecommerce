from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime

class CreateProduct(BaseModel):
    name:str
    price:float
    stocks:int
    description:str
    categories:List[str]
    images:List[str]


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stocks: int
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    images: List[str] = []  
    categories: List[str] = [] 
    
    class Config:
        from_attributes = True  



class ProductUpdate(BaseModel):
    id:int
    name: Optional[str] = None  # ✅ Default is None
    price: Optional[float] = None  # ✅ Default is None
    stocks: Optional[int] = None  # ✅ Default is None
    description: Optional[str] = None  # ✅ Default is None
    images: Optional[List[str]] =None  # ✅ Default is None
    categories: Optional[List[str]] =None

class ProductQuery(BaseModel):
    name:Optional[str] = None
    id:Optional[int] = None