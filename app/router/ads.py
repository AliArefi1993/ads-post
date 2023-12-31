from typing import List, Optional
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.db import schemas, models, crud
from app.router import get_current_active_user

router = APIRouter()


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


@router.post("/ads", tags=['ads'], response_model=schemas.Ads, dependencies=[Depends(get_current_active_user)])
def create_ads(ads: schemas.AdsCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_ads = crud.ads.create(db, ads, current_user.id)
    return db_ads


@router.put(
    "/ads/{ads_id}", tags=["ads"], response_model=schemas.Ads, dependencies=[Depends(get_current_active_user)]
)
def edit_ads(
    ads_id: int, ads: schemas.AdsUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)
):
    db_ads = crud.ads.get_or_404(db, ads_id)
    if db_ads.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    db_ads = crud.ads.update(db, ads, db_ads)
    return db_ads


@router.delete("/ads/{ads_id}", tags=['ads'], dependencies=[Depends(get_current_active_user)])
def delete_ads(ads_id: int,  db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_ads = crud.ads.get_or_404(db, ads_id)
    if db_ads.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    crud.ads.delete(db, db_ads)
    return {"ok": True}
