from datetime import timedelta, datetime
from pydantic import ValidationError
from typing import Union, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session

from db_setup import get_db
from schemas.auth import TokenPayload
from models.users import User



SECRET_KEY = "ead4afad860838cd802e057c0fcd2d163f9f9adbe9635f2386d28f05a351a174"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3


class Auth:

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


    def encode_token(self, payload):
        return jwt.encode(payload, SECRET_KEY, algorithms=[ALGORITHM])
    

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Expired signature"}
            )
        except(JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"message": "Could not validate credentials"},
            )
    

    def create_access_token(self, subject: Union[str, Any], expires_delta: int = None):
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {
            "exp": expires_delta,
            "iat": datetime.utcnow(),
            "sub": str(subject)
        }
        encoded_jwt = self.encode_token(payload)
        return encoded_jwt


    def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        payload = self.decode_token(token=token)
        token_data = TokenPayload(**payload)

        user = db.query(User).filter(User.id == token_data.sub).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Invalid crendentials"},
            )

        return user