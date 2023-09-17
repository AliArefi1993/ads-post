import os
from typing import List, Optional
from fastapi import HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.db import schemas, models


class CRUDUser:
    def count(self, db: Session) -> int:
        return db.query(models.User).count()

    def get_all(self, db: Session) -> List[models.User]:
        db_users = db.query(models.User).all()
        return db_users

    def get_or_404(self, db: Session, user_id: int) -> models.User:
        db_user = (
            db.query(models.User).filter(models.User.id == user_id).first()
        )
        if not db_user:
            raise HTTPException(404, detail="User not found")
        return db_user

    def get_multi(
        self, db: Session, offset: int = 0, limit: int = 100
    ) -> List[models.User]:
        db_users = db.query(models.User).filter().offset(
            offset).limit(limit).all()
        return db_users

    def create(
        self,
        db: Session,
        user: schemas.UserCreate,
        hased_password: str
    ) -> models.User:
        db_user = models.User(**{"email": user.email, "full_name": user.full_name,
                              "disabled": user.disabled, "hashed_password": hased_password})
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(
        self,
        db: Session,
        new_user: schemas.UserUpdate,
        old_user: models.User,
        hashed_password: str
    ) -> models.User:
        db_user = db.query(models.User).filter(models.User.id == old_user.id)
        db_user.update({"email": new_user.email, "full_name": new_user.full_name,
                        "disabled": new_user.disabled, "hashed_password": hashed_password})
        db.commit()
        db_user = db_user.first()
        return db_user

    def delete(self, db: Session, user: models.User):
        try:
            db.query(models.User).filter(models.User.id == user.id).delete()
        except IntegrityError:
            raise HTTPException(status_code=423)

        db.commit()
        return None


user = CRUDUser()
