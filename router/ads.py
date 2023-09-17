from typing import List, Optional
from fastapi import APIRouter, Depends, Response, UploadFile, File, Form
from sqlalchemy.orm import Session
from dependencies import get_db
from db import schemas, models, crud
from router import get_current_active_user

router = APIRouter(dependencies = [Depends(get_current_active_user)])

# ads
@router.get("/ads", tags=['ads'], response_model=List[schemas.Ads])
def get_all_ads(
    response: Response, page: int = 1, limit: int = 100, title: Optional[str] = "", db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    db_categories = crud.ads.get_multi(db, offset, limit, title)
    db_ads_cnt = crud.ads.count(db)
    response.headers["X-Total-Count"] = str(db_ads_cnt)
    return db_categories

@router.get(
    "/ads/{ads_id}", tags=["ads"], response_model=schemas.AdsDetail
)
def get_ads(ads_id: int, db: Session = Depends(get_db)):
    db_ads = crud.ads.get_or_404(db, ads_id)
    return db_ads

@router.post("/ads", tags=['ads'], response_model=schemas.Ads)
def create_ads(ads: schemas.AdsCreate, db: Session = Depends(get_db)):
    db_ads = crud.ads.create(db, ads)
    return db_ads

@router.put(
    "/ads/{ads_id}", tags=["ads"], response_model=schemas.Ads
)
def edit_ads(
    ads_id: int, ads: schemas.AdsUpdate, db: Session = Depends(get_db)
):
    db_ads = crud.ads.get_or_404(db, ads_id)
    db_ads = crud.ads.update(db, ads, db_ads)
    return db_ads


@router.delete("/ads/{ads_id}", tags=['ads'])
def delete_ads(ads_id: int, db: Session = Depends(get_db)):
    db_ads = crud.ads.get_or_404(db, ads_id)
    crud.ads.delete(db, db_ads)
    return {"ok": True}
