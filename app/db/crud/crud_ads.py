import os
from typing import List, Optional
from fastapi import HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.db import schemas, models


class CRUDAds:
    def count(self, db: Session) -> int:
        return db.query(models.Ads).count()

    def get_all(self, db: Session) -> List[models.Ads]:
        db_adses = db.query(models.Ads).all()
        return db_adses

    def get_or_404(self, db: Session, ads_id: int) -> models.Ads:
        db_ads = (
            db.query(models.Ads).filter(models.Ads.id == ads_id).first()
        )
        if not db_ads:
            raise HTTPException(404, detail="Ads not found")
        return db_ads

    def get_multi(
        self, db: Session, offset: int = 0, limit: int = 100, title: Optional[str] = ""
    ) -> List[models.Ads]:
        db_adses = db.query(models.Ads).filter(models.Ads.title.like(
            f"%{title}%")).offset(offset).limit(limit).all()
        return db_adses

    def create(
        self,
        db: Session,
        ads: schemas.AdsCreate,
        owner_id: int
    ) -> models.Ads:
        db_ads = models.Ads(**ads.dict(), owner_id=owner_id)
        db.add(db_ads)
        db.commit()
        db.refresh(db_ads)
        return db_ads

    def update(
        self,
        db: Session,
        new_ads: schemas.AdsUpdate,
        old_ads: models.Ads,
    ) -> models.Ads:
        db_ads = db.query(models.Ads).filter(models.Ads.id == old_ads.id)
        db_ads.update(new_ads.dict())
        db.commit()
        db_ads = db_ads.first()
        return db_ads

    def delete(self, db: Session, ads: models.Ads):
        try:
            db.query(models.Ads).filter(models.Ads.id == ads.id).delete()
        except IntegrityError:
            raise HTTPException(status_code=423)

        db.commit()
        return None


ads = CRUDAds()
