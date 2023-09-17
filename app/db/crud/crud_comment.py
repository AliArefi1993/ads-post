import os
from typing import List, Optional
from fastapi import HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.db import schemas, models


class CRUDComment:
    def count(self, db: Session) -> int:
        return db.query(models.Comment).count()

    def get_all(self, db: Session) -> List[models.Comment]:
        db_commentes = db.query(models.Comment).all()
        return db_commentes

    def get_or_404(self, db: Session, comment_id: int) -> models.Comment:
        db_comment = (
            db.query(models.Comment).filter(
                models.Comment.id == comment_id).first()
        )
        if not db_comment:
            raise HTTPException(404, detail="Comment not found")
        return db_comment

    def get_multi(
        self, db: Session, offset: int = 0, limit: int = 100
    ) -> List[models.Comment]:
        db_commentes = db.query(models.Comment).filter().offset(
            offset).limit(limit).all()
        return db_commentes

    def create(
        self,
        db: Session,
        comment: schemas.CommentCreate,
        owner_id: int
    ) -> models.Comment:
        db_comment = models.Comment(**comment.dict(), owner_id=owner_id)
        try:
            db.add(db_comment)
            db.commit()
            db.refresh(db_comment)
        except IntegrityError:
            raise HTTPException(status_code=423)

        return db_comment

    def update(
        self,
        db: Session,
        new_comment: schemas.CommentUpdate,
        old_comment: models.Comment,
    ) -> models.Comment:
        db_comment = db.query(models.Comment).filter(
            models.Comment.id == old_comment.id)
        db_comment.update(new_comment.dict())
        db.commit()
        db_comment = db_comment.first()
        return db_comment

    def delete(self, db: Session, comment: models.Comment):
        try:
            db.query(models.Comment).filter(
                models.Comment.id == comment.id).delete()
        except IntegrityError:
            raise HTTPException(status_code=423)

        db.commit()
        return None


comment = CRUDComment()
