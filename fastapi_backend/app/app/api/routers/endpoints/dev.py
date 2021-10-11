from typing import Any

from fastapi import APIRouter
from fastapi import Depends

from app import models
from app import schemas
from app.api import deps
from app.database import engine

router = APIRouter()


@router.get("/admin_required/", response_model=schemas.User)
def admin_required(curr_user: schemas.User = Depends(deps.require_admin)) -> Any:
    return curr_user


# Require authentication
@router.get("/auth_required/", response_model=schemas.User)
def auth_required(curr_user: schemas.User = Depends(deps.get_current_user)) -> Any:
    return curr_user


@router.get("/auth_optional/", response_model=schemas.User)
def auth_optional(
    curr_user: schemas.User = Depends(deps.get_current_user_or_none),
) -> Any:
    return curr_user


@router.get("/drop_tables/")
def drop_tables() -> None:
    models.Base.metadata.drop_all(bind=engine, checkfirst=True)
    return


@router.get("/create_tables")
def create_tables() -> None:
    models.Base.metadata.create_all(bind=engine, checkfirst=True)
    return
