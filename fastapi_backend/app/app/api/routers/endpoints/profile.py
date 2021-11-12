from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.api import deps

router = APIRouter()


@router.get("/profile/", response_model=schemas.User)
def get_profile(curr_user: models.User = Depends(deps.get_current_user)) -> Any:
    return curr_user


@router.get("/profile/library/", response_model=List[schemas.Book])
def get_user_library(curr_user: models.User = Depends(deps.get_current_user)) -> Any:
    return curr_user.books


@router.get("/profile/wishlist/", response_model=schemas.Wishlist)
def get_user_wishlist(
    curr_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    return curr_user.wishlist
