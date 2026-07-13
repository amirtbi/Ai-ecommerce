from app.models.order import Order,OrderItem
from sqlmodel import Session,select
from sqlalchemy.orm import joinedload,selectinload


def create_order(session:Session,order:Order):
    session.add(order)
    session.commit()
    session.refresh(order)

    return order


def get_orders(session:Session):
    
    query = select(Order).options(selectinload(Order.orderItems))
    return session.exec(query).all()