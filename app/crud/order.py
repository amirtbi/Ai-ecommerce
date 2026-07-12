from app.models.order import Order
from sqlmodel import Session


def create_order(session:Session,order:Order):
    session.add(order)
    session.commit()
    session.refresh(order)

    return order