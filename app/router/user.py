from typing import List, Optional
from fastapi import APIRouter, Depends, Response, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.db import schemas, models, crud
from app.router import get_current_active_user

router = APIRouter(dependencies=[Depends(get_current_active_user)])

# user


@router.get("/user", tags=['user'], response_model=List[schemas.User])
def get_all_user(
    response: Response, page: int = 1, limit: int = 100, db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    db_categories = crud.user.get_multi(db, offset, limit)
    db_user_cnt = crud.user.count(db)
    response.headers["X-Total-Count"] = str(db_user_cnt)
    return db_categories


@router.get(
    "/user/{user_id}", tags=["user"], response_model=schemas.UserDetail
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get_or_404(db, user_id)
    return db_user


@router.post("/user", tags=['user'], response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.user.create(db, user)
    return db_user


@router.put(
    "/user/{user_id}", tags=["user"], response_model=schemas.User
)
def edit_user(
    user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)
):
    db_user = crud.user.get_or_404(db, user_id)
    db_user = crud.user.update(db, user, db_user)
    return db_user


@router.delete("/user/{user_id}", tags=['user'])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get_or_404(db, user_id)
    crud.user.delete(db, db_user)
    return {"ok": True}
