from fastapi import HTTPException, status, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from common.utils import hash_pass, verify_password
from common.auth import Auth
from models.users import User
from db_setup import get_db

router = APIRouter(
    tags=["Authentication"]
)

auth = Auth()

@router.post("/login")
async def login(user_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_object = db.query(User).filter(User.user_name == user_details.username).first()

    if not user_object:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail={"message": "The user does not exist!"})
    
    if not verify_password(user_details.password, user_object.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail={"message": "The passwords do not match"})
    
    access_token = auth.create_access_token(subject=user_object.id)

    return {"access_token": access_token, "token_type": "bearer"}