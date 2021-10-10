from typing import List
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post("/users/", response_model=schemas.Token)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
	db_user = crud.get_user_by_name(db=db, username=user.username)
	if db_user:
		raise HTTPException(status_code=400, detail="Username taken")

	created_user = crud.create_user(db=db, user=user)

	# Login user when registered
	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

	return {
		"access_token": security.create_access_token(
			created_user, expires_delta=access_token_expires
		),
		"token_type": "bearer"
	}


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
	return crud.get_users(db=db, skip=skip, limit=limit)


@router.get("/user/{username}", response_model=schemas.User)
def read_user(username: str, db: Session = Depends(deps.get_db)):
	return crud.get_user_by_name(db=db, username=username)
