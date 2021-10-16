from datetime import timedelta
from typing import Any
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app import models
from app import schemas
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()

# Maybe put this somewhere else
def authenticate_user(
    db: Session, username: str, password: str
) -> Optional[models.User]:
    db_user = crud.get_user_by_name(db=db, username=username)
    if not db_user:
        return None
    if not security.verify_password(password, db_user.password_hash):
        return None
    return db_user


@router.post("/login/", response_model=schemas.Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)
) -> Any:
    user = authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Login failed")

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )  # Change later

    return {
        "access_token": security.create_access_token(
            user, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
