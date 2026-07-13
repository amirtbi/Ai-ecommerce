from sqlmodel import Field,SQLModel,Relationship
from typing import Optional,List

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.user import User




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
    user_id:str = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="orders")



