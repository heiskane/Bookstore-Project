from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.api import deps

router = APIRouter()


@router.get("/orders/", response_model=List[schemas.Order])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    curr_user: schemas.User = Depends(deps.require_admin),
) -> Any:
    return crud.get_orders(db=db, skip=skip, limit=limit)
