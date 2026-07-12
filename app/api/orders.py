from fastapi import APIRouter,HTTPException,Depends
from typing import List
from sqlmodel import Session
from app.core.database import get_session
from datetime import datetime
from app.schemas.orders import CreateOrder,OrderResponse
from app.models.order import OrderItem,Order
from app.models.product import Product

router = APIRouter(prefix="/orders",tags=["Orders"])



@router.post("/add")
def add_order(order_data:CreateOrder,session:Session=Depends(get_session)):
    
    order = Order()

    for data in order_data.items:

        product = session.get(Product,data.product_id)

        if product is None:
            raise HTTPException(status_code=400,detail="Product not found")

        order_item = OrderItem(product=product,quantity=data.quantity,unit_price=product.price)
        order.orderItems.append(order_item)

    


    try:
        session.add(order)
        session.commit()
        session.refresh(order)

        order = session.get(Order, order.id)

        return OrderResponse(id=order.id,items=order.orderItems)

    except:
        session.rollback()

   