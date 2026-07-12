from fastapi import APIRouter, Depends,HTTPException
from sqlmodel import Session
from app.crud.user import create_user,find_user_by_email,find_user
from app.core.database import get_session
from app.services.password_services import hash_password

from app.models.user import User

from app.schemas.users import UserCreate,UserResponse

router = APIRouter(prefix="/users",tags=["Users"])


@router.post("/register")
def register_user(user_data:UserCreate,session:Session = Depends(get_session)):



    hashed_password = hash_password(user_data.password)

    user_existed = find_user(session,user_data)

    if user_existed:
        raise HTTPException(status_code=400,detail="User already exists")
    

    user = User(username=user_data.username,email=user_data.email,hashed_password=hashed_password,roles=user_data.roles)

    return create_user(session,user)



@router.get("/find")
def get_user_by_email(email:str,session:Session = Depends(get_session)):
    

    print("Email",email)
    if not email:
        raise HTTPException(status_code=400,detail="Email is required")
    
    user = find_user_by_email(session,email)

    if not user:
        raise HTTPException(status_code=400,detail="Not found the user")

    return {"email":user.email,"id":user.id,"username":user.username}


