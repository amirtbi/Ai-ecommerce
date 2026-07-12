from sqlmodel import Field,Column,SQLModel,Relationship
from typing import Optional,List
from datetime import datetime,timezone

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.product import Product


class OrderItem(SQLModel,table=True):
    order_id:int = Field(foreign_key="order.id",primary_key=True)
    product_id:int = Field(foreign_key="product.id",primary_key=True)

    unit_price:int
    quantity:int

    product:Product = Relationship(back_populates="orderItems")
    order:Order = Relationship(back_populates="orderItems")


class Order(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)

    orderItems:List[OrderItem] =  Relationship(back_populates="order")



