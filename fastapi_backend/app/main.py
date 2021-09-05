from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

description = """

Backend API for the Bookstore project

"""

app = FastAPI(description=description)

# Remember to change later and use .env
SECRET_KEY = "a155c5104f0f8fcc9c2c2506588a218476c72fb0c40897f3f93d501c75c8db32"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def verify_password(password_plain: str, password_hash: str):
	return pwd_context.verify(password_plain, password_hash)


def authenticate_user(db: Session, username: str, password: str):
	db_user = crud.get_user_by_name(db=db, username=username)
	if not db_user:
		return False
	if not verify_password(password, db_user.password_hash):
		return False
	return db_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = timedelta(minutes=30)):
	to_encode = data.copy()
	expire = datetime.utcnow() + expires_delta
	to_encode.update({"exp": expire})
	return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	credentials_exception = HTTPException(
		status_code=401,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception
		token_data = schemas.TokenData(username=username)
	except JWTError:
		raise credentials_exception
	user = crud.get_user_by_name(db=db, username=token_data.username)
	if user is None:
		raise credentials_exception
	return user


# Require authentication
@app.get("/auth_required/", response_model=schemas.User)
def auth_required(curr_user: schemas.User = Depends(get_current_user)):
	return curr_user

# Fix pls
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
	# This endpoint might not be needed
	db_author = crud.get_author_by_name(db=db, name=author.name)
	if db_author:
		raise HTTPException(status_code=400, detail="Author already exists")
	return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	authors = crud.get_authors(db, skip=skip, limit=limit)
	return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
	db_author = crud.get_author(db=db, author_id=author_id)
	if not db_author:
		raise HTTPException(status_code=404, detail="Author not found")
	return db_author


@app.get("/authors/{author_id}/books", response_model=List[schemas.Book])
def read_author_books(author_id: int, db: Session = Depends(get_db)):
	db_author = crud.get_author(db=db, author_id=author_id)
	if not db_author:
		raise HTTPException(status_code=404, detail="Author not found")
	return db_author.books


@app.post("/books/", response_model=schemas.Book)
def create_book(
		authors: List[schemas.AuthorCreate],
		book: schemas.BookCreate,
		db: Session = Depends(get_db)):

	db_book = crud.get_book_by_title(db, title=book.title)
	if db_book:
		raise HTTPException(status_code=400, detail="Book with this tile already exists")

	return crud.create_book(db=db, book=book, authors=authors)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
	db_book = crud.get_book(db=db, book_id=book_id)
	if not db_book:
		raise HTTPException(status_code=404, detail="Book not found")
	return db_book


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_name(db=db, username=user.username)
	if db_user:
		raise HTTPException(status_code=400, detail="Username taken")
	return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	return crud.get_users(db=db, skip=skip, limit=limit)


@app.get("/user/{username}", response_model=schemas.User)
def read_user(username: str, db: Session = Depends(get_db)):
	return crud.get_user_by_name(db=db, username=username)


@app.post("/login/", response_model=schemas.Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
	if not user:
		raise HTTPException(status_code=401, detail="Login failed")
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data = {
			"sub": user.username,
			"is_admin": user.is_admin,
			"is_active": user.is_active
		}, expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}
