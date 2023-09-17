

from app.dependencies import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Union
from app.db import schemas, models, crud

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "ali": {
        "username": "ali",
        "full_name": "admin",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$Bsz73tnfgBwFxVDXS/.wbeeM7MQKmPFroy31S3wzs5wVYbgICbmLq",
        "disabled": False,
    },
    "ikco": {
        "username": "ikco",
        "full_name": "ikco",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$IDB0JAD3yqK7/UTi8Oht/ehUh3TbumYag2ej.2kxwUBjPf.T8xspu",
        "disabled": False,
    }
}


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     username: Union[str, None] = None


# class User(BaseModel):
#     username: str
#     email: Union[str, None] = None
#     full_name: Union[str, None] = None
#     disabled: Union[bool, None] = None


# class UserInDB(User):
#     hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("heeee----------------------")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            print("heeee----------------------2")

            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        print("heeee----------------------3")

        raise credentials_exception
    db_user = db.query(models.User).filter(
        models.User.email == token_data.username).first()
    if db_user is None:
        raise credentials_exception

    return db_user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # user = authenticate_user(
    #     fake_users_db, form_data.username, form_data.password)

    db_user = db.query(models.User).filter(
        models.User.email == form_data.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: schemas.User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


# @router.post("/login")
# async def login(user: models.User, db: Session = Depends(get_db)):
#     # Query the database to find the user by username
#     db_user = db.query(models.User).filter(
#         models.User.username == user.username).first()

#     if db_user is None:
#         raise HTTPException(status_code=400, detail="User not found")

#     # Compare the hashed password (use a password hashing library)
#     if not verify_password(user.password, db_user.password):
#         raise HTTPException(status_code=401, detail="Incorrect password")

#     # Generate and return the JWT token
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}
