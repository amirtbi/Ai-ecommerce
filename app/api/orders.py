from fastapi import APIRouter,HTTPException,Depends
from typing import List
from sqlmodel import Session
from app.core.database import get_session
from datetime import datetime
from app.schemas.orders import CreateOrder,OrderResponse
from app.models.order import OrderItem,Order
from app.models.product import Product
from app.crud.order import get_orders

router = APIRouter(prefix="/orders",tags=["Orders"])



@router.post("/add")
def add_order(order_data:CreateOrder,session:Session=Depends(get_session)):
    
    order = Order()
    session.add(order)
    
    for data in order_data.items:
        product = session.get(Product, data.product_id)

        print("product stock",product.stocks)

        if product.stocks<=0 or data.quantity > product.stocks:
            raise HTTPException(status_code=400,detail=f"There are not any stocks availabel for the {product.name.capitalize()}")
        
        if product is None:
            raise HTTPException(status_code=400, detail="Product not found")
        
        order_item = OrderItem(
            product=product, 
            quantity=data.quantity, 
            unit_price=product.price,
            order=order
        )
        product.stocks-=data.quantity
        
        session.add(order_item)

    session.commit()
    session.refresh(order)
    return OrderResponse(id=order.id, items=order.orderItems)

   


@router.get("/list")
def get_orders_list(session:Session=Depends(get_session)):
    orders = get_orders(session)

    results = []

    for order in orders:
        for item in order.orderItems:
            products = session.get(Product,item.product_id)
            results.append({
                "id":item.order_id,
                "products":products
                

            })

    return {
        "results":results,
        "total":len(results)
    }
