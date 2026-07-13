from pydantic import BaseModel,ConfigDict
from typing import List,Optional
from datetime import datetime


class CreateOrderItem(BaseModel):
    product_id:int
    quantity:int

class CreateOrder(BaseModel):
   items:List[CreateOrderItem]
   user_id:str




class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)



class OrderResponse(BaseModel):
    id: int
    items: list[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)