from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends

from app import models
from app import schemas
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/profile/library/", response_model=List[schemas.Book])
def get_user_library(curr_user: models.User = Depends(get_current_user)) -> Any:
    return curr_user.books
