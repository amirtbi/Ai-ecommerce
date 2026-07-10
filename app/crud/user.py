from app.models.user import User
from sqlmodel import Session ,select

def create_user(session:Session,user:User):
    session.add(user)
    session.commit()

    session.refresh(user)

    return user



def find_user(session:Session,user_data:User):

    query = select(User).where(user_data.email == User.email or user_data.username==User.username)

    return session.exec(query).first()


def find_user_by_email(session:Session,email:str):

    query = select(User).where(User.email== email)

    return session.exec(query).first()
