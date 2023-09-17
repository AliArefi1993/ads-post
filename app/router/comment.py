from typing import List, Optional
from fastapi import APIRouter, Depends, Response, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.db import schemas, models, crud
from app.router import get_current_active_user

# router = APIRouter(dependencies=[Depends(get_current_active_user)])
router = APIRouter()


@router.get("/comment", tags=['comment'], response_model=List[schemas.Comment])
def get_all_comment(
    response: Response, page: int = 1, limit: int = 100, db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    db_categories = crud.comment.get_multi(db, offset, limit)
    db_comment_cnt = crud.comment.count(db)
    response.headers["X-Total-Count"] = str(db_comment_cnt)
    return db_categories


@router.get(
    "/comment/{comment_id}", tags=["comment"], response_model=schemas.CommentDetail
)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.comment.get_or_404(db, comment_id)
    return db_comment


@router.post("/comment", tags=['comment'], response_model=schemas.Comment, dependencies=[Depends(get_current_active_user)])
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    print("get_current_active_user.id")
    db_comment = crud.comment.create(db, comment, current_user.id)
    return db_comment


@router.put(
    "/comment/{comment_id}", tags=["comment"], response_model=schemas.Comment, dependencies=[Depends(get_current_active_user)]
)
def edit_comment(
    comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)
):
    db_comment = crud.comment.get_or_404(db, comment_id)
    if db_comment.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    db_comment = crud.comment.update(db, comment, db_comment)
    return db_comment


@router.delete("/comment/{comment_id}", tags=['comment'], dependencies=[Depends(get_current_active_user)])
def delete_comment(comment_id: int,  db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_comment = crud.comment.get_or_404(db, comment_id)
    if db_comment.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    crud.comment.delete(db, db_comment)
    return {"ok": True}
